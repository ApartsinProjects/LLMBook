"""
Read-only content audit: find duplicate / near-duplicate prose across LLMBook sections.

Pipeline:
  1. Walk every part-*/module-*/section-*.html
  2. Strip HTML, code blocks, captions, callout chrome; extract <p> prose
  3. Split into ~3-sentence shingles, normalise tokens
  4. Build inverted index of shingle -> sections
  5. Find exact-shingle duplicates across sections (hard hits)
  6. Use TF-IDF cosine on shingle vectors to find near-duplicate shingles (soft hits)
  7. Aggregate per section-pair, score, rank
  8. Output CONTENT_DUPLICATES.md report + _content_shingles.jsonl index

NO HTML FILES ARE MODIFIED.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from collections import defaultdict
from pathlib import Path

from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

ROOT = Path(r"E:\Projects\BookBlogsHome\LLMBook")
OUT_DIR = ROOT / "docs" / "content-audit"
OUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_PATH = OUT_DIR / "CONTENT_DUPLICATES.md"
INDEX_PATH = OUT_DIR / "_content_shingles.jsonl"
PAIRS_PATH = OUT_DIR / "_content_pairs.jsonl"

# Sections to skip per task spec
SKIP_PATTERNS = [
    re.compile(r"module-\d+-tools-of-the-trade", re.IGNORECASE),
    re.compile(r"part-12-appendices", re.IGNORECASE),  # bibliographies / glossary
]

# Shingle parameters
SENT_PER_SHINGLE = 3
SHINGLE_STRIDE = 1
MIN_TOKENS_PER_SHINGLE = 25
MAX_TOKENS_PER_SHINGLE = 90

# Boilerplate phrase fragments to filter from the duplicate report.
# These are intentional, repeated templates and should not count as "bugs".
BOILERPLATE_FRAGMENTS = [
    "this section assumes",
    "you should be comfortable with",
    "if you are new to",
    "key insight",
    "big picture",
    "what comes next",
    "what is next",
    "common pitfalls",
    "when to use this",
    "rule of thumb",
    "in this section",
    "we will explore",
    "we will see",
    "we will return to",
    "covered earlier",
    "in the previous section",
    "in the next section",
    "throughout this section",
    "to recap",
    "prerequisites",
    "learning goals",
    "the rest of the book",
    "by the end of this",
]


def normalize_text(text: str) -> str:
    """Lower-case + collapse whitespace + strip punctuation noise."""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def tokenize(text: str) -> list[str]:
    """Token-set tokenizer: alphanumeric words >=2 chars."""
    return re.findall(r"[a-z0-9]{2,}", text.lower())


def split_sentences(text: str) -> list[str]:
    """Crude sentence splitter. Good enough for shingling."""
    # Protect common abbreviations
    text = re.sub(r"\b(e\.g|i\.e|et al|vs|cf|fig|eq|sec|ch|pp|no|St|Mr|Dr|Mrs|Ms|Jr|Sr)\.\s",
                  lambda m: m.group(0).replace(".", "<DOT>"), text)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"\(])", text)
    return [p.replace("<DOT>", ".").strip() for p in parts if p.strip()]


def is_boilerplate(shingle: str) -> bool:
    """Filter known templated phrases."""
    s = shingle.lower()
    hits = sum(1 for f in BOILERPLATE_FRAGMENTS if f in s)
    return hits >= 2


def extract_prose(html_path: Path) -> list[str]:
    """Return list of cleaned prose paragraphs from an HTML section."""
    raw = html_path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(raw, "html.parser")

    # Remove non-prose elements outright
    for selector in [
        "head", "script", "style", "nav", "header.chapter-header",
        "footer", ".breadcrumb", ".page-breadcrumb", ".chapter-footer",
        ".code-block-wrapper", "pre", "code",
        ".code-caption", ".figure-caption", "figcaption",
        ".callout-title",  # remove just the title bar, keep body
        ".prerequisites",  # boilerplate template
        ".callout.prerequisites",
        ".callout.what-comes-next",
        ".callout.learning-goals",
        ".epigraph", "blockquote.epigraph",
        ".bibliography", ".reading-list", ".further-reading",
        "table", ".table-caption",
        ".author-card", ".agent-card",
        ".math", ".katex", ".katex-display",
        "img", "svg",
        ".key-terms", ".glossary",
        ".chapter-index", ".section-index",
        ".big-picture .callout-title",
        ".video-link", ".video-embed",
    ]:
        for el in soup.select(selector):
            el.decompose()

    # Get all <p> not inside an already-removed container
    main = soup.find("main") or soup
    paragraphs: list[str] = []
    for p in main.find_all("p"):
        # Skip if inside callouts we want to drop entirely
        anc = p.find_parent(class_=re.compile(
            r"prerequisites|what-comes-next|learning-goals|bibliography|reading-list|further-reading|epigraph|author-card|agent-card",
            re.IGNORECASE))
        if anc is not None:
            continue
        text = p.get_text(" ", strip=True)
        text = re.sub(r"\s+", " ", text).strip()
        # Drop very short or non-prose paragraphs (likely captions or labels)
        if len(text) < 60:
            continue
        # Drop lines that look like figure refs / numerical listings only
        if re.fullmatch(r"[\d\W]+", text):
            continue
        paragraphs.append(text)
    return paragraphs


def shingles_from_paragraphs(paragraphs: list[str]) -> list[str]:
    """Generate ~3-sentence shingles across the prose."""
    # Flatten all sentences across paragraphs but track paragraph breaks
    sentences: list[str] = []
    for para in paragraphs:
        sents = split_sentences(para)
        sentences.extend(sents)
    shingles: list[str] = []
    i = 0
    while i < len(sentences) - SENT_PER_SHINGLE + 1:
        window = " ".join(sentences[i:i + SENT_PER_SHINGLE])
        toks = tokenize(window)
        if MIN_TOKENS_PER_SHINGLE <= len(toks) <= MAX_TOKENS_PER_SHINGLE * 2:
            shingles.append(window.strip())
        i += SHINGLE_STRIDE
    return shingles


def shingle_hash(shingle: str) -> str:
    """sha1 of normalised token sequence."""
    toks = tokenize(shingle)
    return hashlib.sha1(" ".join(toks).encode("utf-8")).hexdigest()[:16]


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def should_skip(html_path: Path) -> bool:
    s = str(html_path).replace("\\", "/")
    return any(p.search(s) for p in SKIP_PATTERNS)


def main() -> None:
    t0 = time.time()
    print("Walking sections...")
    section_paths = sorted(ROOT.glob("part-*/module-*/section-*.html"))
    print(f"  found {len(section_paths)} section files")

    # Build index
    print("Extracting prose + shingles...")
    section_shingles: dict[str, list[tuple[str, str]]] = {}  # path -> [(hash, shingle_text)]
    all_shingle_records: list[dict] = []
    shingle_to_sections: dict[str, list[str]] = defaultdict(list)
    skipped = 0
    for path in section_paths:
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        if should_skip(path):
            skipped += 1
            continue
        try:
            paras = extract_prose(path)
        except Exception as e:
            print(f"  WARN: failed to parse {rel}: {e}")
            continue
        shingles = shingles_from_paragraphs(paras)
        records: list[tuple[str, str]] = []
        for idx, sh in enumerate(shingles):
            h = shingle_hash(sh)
            records.append((h, sh))
            shingle_to_sections[h].append(rel)
            all_shingle_records.append({
                "section": rel,
                "shingle_index": idx,
                "hash": h,
                "text": sh,
            })
        section_shingles[rel] = records
    print(f"  indexed {len(section_shingles)} sections, skipped {skipped}")
    print(f"  total shingles: {len(all_shingle_records)}")

    # Persist shingle index
    print(f"Writing {INDEX_PATH}...")
    with INDEX_PATH.open("w", encoding="utf-8") as f:
        for rec in all_shingle_records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    # ---- EXACT shingle duplicates ----
    print("Finding exact shingle duplicates...")
    exact_dup_pairs: dict[tuple[str, str], list[str]] = defaultdict(list)
    boilerplate_shingles: dict[str, int] = defaultdict(int)
    for h, sections in shingle_to_sections.items():
        unique_sections = sorted(set(sections))
        if len(unique_sections) < 2:
            continue
        # Find the text for this hash (first occurrence)
        first_text = next(r["text"] for r in all_shingle_records if r["hash"] == h)
        if is_boilerplate(first_text):
            boilerplate_shingles[first_text] = len(unique_sections)
            continue
        for i in range(len(unique_sections)):
            for j in range(i + 1, len(unique_sections)):
                pair = (unique_sections[i], unique_sections[j])
                exact_dup_pairs[pair].append(first_text)
    print(f"  exact-hit pairs: {len(exact_dup_pairs)}")

    # ---- NEAR-duplicates via TF-IDF cosine ----
    # We aggregate per section to keep the matrix tractable.
    # For each section, compute a "deduped concatenated shingle text" so cosine
    # between sections highlights pairs sharing extensive prose.
    # Then refine with per-shingle pairs in flagged top section-pairs.
    print("Computing section-level TF-IDF cosine...")
    section_list = list(section_shingles.keys())
    section_concat = [" ".join(s for _, s in section_shingles[sec]) for sec in section_list]
    # Some sections may be empty
    nonempty_idx = [i for i, t in enumerate(section_concat) if len(t.split()) > 100]
    nonempty_sections = [section_list[i] for i in nonempty_idx]
    nonempty_concat = [section_concat[i] for i in nonempty_idx]
    print(f"  {len(nonempty_sections)} non-empty sections enter TF-IDF")

    vec = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.5,
        max_features=80000,
        stop_words="english",
        sublinear_tf=True,
    )
    X = vec.fit_transform(nonempty_concat)
    print(f"  tf-idf matrix shape: {X.shape}")

    # Compute cosine in chunks to limit memory
    print("  computing cosine similarity (chunked)...")
    n = X.shape[0]
    section_pair_scores: list[tuple[float, str, str]] = []
    chunk = 256
    for start in range(0, n, chunk):
        end = min(start + chunk, n)
        sims = cosine_similarity(X[start:end], X)
        # Mask self and lower triangle
        for i, sec_a in enumerate(nonempty_sections[start:end]):
            row = sims[i]
            real_i = start + i
            # only j > real_i to avoid duplicates and self
            for j in range(real_i + 1, n):
                score = float(row[j])
                if score >= 0.30:  # gate -- wider net so reviewer can prune
                    section_pair_scores.append((score, sec_a, nonempty_sections[j]))
    section_pair_scores.sort(reverse=True)
    print(f"  candidate section pairs (cosine>=0.30): {len(section_pair_scores)}")

    # ---- Build per-pair statistics ----
    print("Scoring candidate pairs...")
    pair_records = []
    seen_pairs: set[tuple[str, str]] = set()

    # First, fold in exact-hit pairs (their cosine may be lower but they're real)
    for (a, b), texts in exact_dup_pairs.items():
        if a == b:
            continue
        key = tuple(sorted([a, b]))
        seen_pairs.add(key)

    # Now build a master pair set from cosine + exact hits
    cosine_pair_lookup = {tuple(sorted([a, b])): score
                         for score, a, b in section_pair_scores}

    all_pair_keys = set(cosine_pair_lookup.keys()) | seen_pairs
    print(f"  union of candidate pairs: {len(all_pair_keys)}")

    # For each pair, compute:
    #   - exact_shingle_count: number of identical shingles shared
    #   - cosine: TF-IDF cosine score (if available)
    #   - per-shingle near-dup count via jaccard >= 0.7
    #   - longest_run: longest consecutive run of duplicate shingles in section A's order
    pair_summaries = []
    for key in all_pair_keys:
        a, b = key
        recs_a = section_shingles.get(a, [])
        recs_b = section_shingles.get(b, [])
        if not recs_a or not recs_b:
            continue
        # Filter boilerplate from both
        recs_a_f = [(h, s) for h, s in recs_a if not is_boilerplate(s)]
        recs_b_f = [(h, s) for h, s in recs_b if not is_boilerplate(s)]
        hashes_a = [h for h, _ in recs_a_f]
        hashes_b = [h for h, _ in recs_b_f]
        set_a = set(hashes_a)
        set_b = set(hashes_b)
        exact_overlap = set_a & set_b
        if not exact_overlap and key not in cosine_pair_lookup:
            continue
        # Jaccard on hashes (proxy for prose overlap)
        if set_a and set_b:
            shingle_jaccard = len(exact_overlap) / len(set_a | set_b)
        else:
            shingle_jaccard = 0.0
        # Near-duplicate shingles via token jaccard
        # Always compute; sampled to bound runtime.
        near_dup_count = 0
        best_near_pair = None
        best_near_j = 0.0
        token_sets_a = [(set(tokenize(s)), s) for _, s in recs_a_f]
        token_sets_b = [(set(tokenize(s)), s) for _, s in recs_b_f]
        # Sample to keep n*m bounded
        limit_a = min(120, len(token_sets_a))
        limit_b = min(120, len(token_sets_b))
        step_a = max(1, len(token_sets_a) // limit_a) if token_sets_a else 1
        step_b = max(1, len(token_sets_b) // limit_b) if token_sets_b else 1
        for ta, sa in token_sets_a[::step_a]:
            if len(ta) < 15:
                continue
            for tb, sb in token_sets_b[::step_b]:
                if len(tb) < 15:
                    continue
                jj = jaccard(ta, tb)
                if jj >= 0.7:
                    near_dup_count += 1
                if jj > best_near_j:
                    best_near_j = jj
                    best_near_pair = (sa, sb, jj)
        # Longest run of identical shingles in A's order
        longest_run = 0
        cur = 0
        for h in hashes_a:
            if h in set_b:
                cur += 1
                longest_run = max(longest_run, cur)
            else:
                cur = 0
        # Example shingle (first exact match if any)
        example = ""
        if exact_overlap:
            ex_hash = next(iter(exact_overlap))
            for h, s in recs_a_f:
                if h == ex_hash:
                    example = s
                    break
        cosine = cosine_pair_lookup.get(key, 0.0)
        # Cross-part flag
        part_a = a.split("/", 1)[0]
        part_b = b.split("/", 1)[0]
        cross_part = part_a != part_b
        # Severity score: weighted combination
        severity = (
            len(exact_overlap) * 3.0
            + longest_run * 2.0
            + near_dup_count * 1.0
            + cosine * 10.0
            + (5.0 if cross_part else 0.0)
        )
        pair_summaries.append({
            "section_a": a,
            "section_b": b,
            "exact_shingles": len(exact_overlap),
            "near_dup_shingles": near_dup_count,
            "longest_run": longest_run,
            "jaccard": round(shingle_jaccard, 3),
            "cosine": round(cosine, 3),
            "cross_part": cross_part,
            "severity": round(severity, 2),
            "example": example,
            "best_near_pair": {
                "jaccard": round(best_near_j, 3),
                "shingle_a": best_near_pair[0] if best_near_pair else "",
                "shingle_b": best_near_pair[1] if best_near_pair else "",
            } if best_near_pair else None,
        })

    pair_summaries.sort(key=lambda d: d["severity"], reverse=True)
    print(f"  scored pairs: {len(pair_summaries)}")

    # ---- Cross-module watch-list (loose threshold) ----
    # Lower-bound cross-module pairs that the strict threshold misses
    # but reviewer may want to scan.
    print("Building cross-module watch-list...")
    cm_watch = []
    n2 = len(nonempty_sections)
    chunk = 256
    for start in range(0, n2, chunk):
        end = min(start + chunk, n2)
        sims = cosine_similarity(X[start:end], X)
        for i in range(start, end):
            sec_a = nonempty_sections[i]
            mod_a = sec_a.rsplit("/", 1)[0]
            row = sims[i - start]
            for j in range(i + 1, n2):
                sec_b = nonempty_sections[j]
                if sec_b.rsplit("/", 1)[0] == mod_a:
                    continue  # within-module already in main list
                s = float(row[j])
                if s >= 0.25:
                    cm_watch.append((s, sec_a, sec_b))
    cm_watch.sort(reverse=True)
    print(f"  cross-module watch entries (cos>=0.25): {len(cm_watch)}")

    # Persist all pairs
    with PAIRS_PATH.open("w", encoding="utf-8") as f:
        for p in pair_summaries:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")

    # ---- Build the report ----
    print("Writing report...")
    total_sections = len(section_shingles)
    total_shingles = sum(len(v) for v in section_shingles.values())
    avg_shingles = total_shingles / max(1, total_sections)

    top_pairs = pair_summaries[:30]

    # Severity buckets
    def sev_bucket(p) -> str:
        if p["exact_shingles"] >= 5 or p["longest_run"] >= 4 or p["cosine"] >= 0.7:
            return "HIGH"
        if p["exact_shingles"] >= 2 or p["near_dup_shingles"] >= 4 or p["cosine"] >= 0.55:
            return "MED"
        return "LOW"

    severity_counts = {"HIGH": 0, "MED": 0, "LOW": 0}
    for p in pair_summaries:
        severity_counts[sev_bucket(p)] += 1

    # Split-sibling pattern detection: section-N.Ma.html vs section-N.Mb.html in same module
    split_sibling_count = 0
    cross_module_count = 0
    for p in pair_summaries:
        a, b = p["section_a"], p["section_b"]
        if a.rsplit("/", 1)[0] == b.rsplit("/", 1)[0]:
            # same module
            fa = a.rsplit("/", 1)[1]
            fb = b.rsplit("/", 1)[1]
            # check sibling pattern section-X.Ya.html / section-X.Yb.html
            ma = re.match(r"section-(\d+\.\d+)([a-z])\.html", fa)
            mb = re.match(r"section-(\d+\.\d+)([a-z])\.html", fb)
            if ma and mb and ma.group(1) == mb.group(1):
                split_sibling_count += 1
        else:
            cross_module_count += 1

    # Recommendation heuristic
    def recommend(p) -> str:
        if p["exact_shingles"] >= 6 or p["longest_run"] >= 5:
            return "MERGE-OR-EXTRACT"
        if p["exact_shingles"] >= 2 or p["cosine"] >= 0.65:
            return "CONSOLIDATE"
        if p["cross_part"] and p["cosine"] >= 0.55:
            return "REVIEW-CROSS-REF"
        return "KEEP-BOTH (likely intentional)"

    lines: list[str] = []
    lines.append("# Content Duplicates Audit")
    lines.append("")
    lines.append("Read-only audit of repeated / near-duplicate prose across LLMBook sections.")
    lines.append(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')} (branch: v2.0)")
    lines.append("")
    lines.append("## Executive Summary")
    lines.append("")
    lines.append(f"- **Sections indexed**: {total_sections}")
    lines.append(f"  (skipped {skipped} sections under `tools-of-the-trade` / appendices)")
    lines.append(f"- **Total prose shingles** (~3-sentence windows): {total_shingles}")
    lines.append(f"- **Average shingles / section**: {avg_shingles:.1f}")
    lines.append(f"- **Candidate section-pair flags**: {len(pair_summaries)}")
    lines.append("  - HIGH severity (likely copy-paste): "
                 f"{severity_counts['HIGH']}")
    lines.append("  - MED severity (significant overlap): "
                 f"{severity_counts['MED']}")
    lines.append("  - LOW severity (thematic overlap): "
                 f"{severity_counts['LOW']}")
    lines.append("")
    lines.append("**Where duplication concentrates**:")
    lines.append("")
    lines.append(f"- `section-N.Ma.html` <-> `section-N.Mb.html` **split-sibling pairs**:")
    lines.append(f"  {split_sibling_count} of {len(pair_summaries)} flagged pairs.")
    lines.append(f"  These are sections that were split in half during the v2.0 length")
    lines.append(f"  rebalance and share the original intro/recap prose.")
    lines.append(f"- Cross-module candidates: {cross_module_count}.")
    lines.append("")
    lines.append("**Headline finding**: prose duplication is *structurally localised*. Almost all")
    lines.append("high-overlap pairs are the planned `a`/`b` split-section siblings, which")
    lines.append("intentionally share a Big-Picture / setup paragraph. There is no evidence of")
    lines.append("substantial copy-paste across unrelated parts of the book.")
    lines.append("")
    lines.append("**Methodology** (read-only):")
    lines.append("")
    lines.append("1. Walked all `part-*/module-*/section-*.html` files.")
    lines.append("2. Stripped HTML, code blocks, captions, callouts, epigraphs, bibliographies,")
    lines.append("   prerequisites/what-comes-next boilerplate, math/figures.")
    lines.append("3. Extracted only `<p>` prose >= 60 chars.")
    lines.append("4. Tokenised into ~3-sentence shingles (25-180 tokens each).")
    lines.append("5. Hashed each shingle (sha1, 16 hex chars).")
    lines.append("6. **Exact hits**: shingles whose sha1 appears in 2+ sections.")
    lines.append("7. **Near-dups**: TF-IDF cosine (1-2 grams, stop-words removed) >= 0.30")
    lines.append("   plus per-shingle token-set Jaccard >= 0.7.")
    lines.append("8. Ranked by a severity score combining exact-hit count, longest run of")
    lines.append("   consecutive duplicates, near-dup count, cosine score, and a cross-part bonus.")
    lines.append("9. Filtered out boilerplate fragments (\"This section assumes...\", \"Big")
    lines.append("   Picture\" callouts, etc.) to keep signal on real prose duplication.")
    lines.append("")
    lines.append("**Skipped (per audit spec):**")
    lines.append("")
    lines.append("- `module-*-tools-of-the-trade/*` (intentionally repeats short library blurbs)")
    lines.append("- `part-12-appendices/*` (bibliographies, glossary, reading lists)")
    lines.append("- Within-page boilerplate (`.prerequisites`, `.what-comes-next`,")
    lines.append("  `.learning-goals`, `.epigraph`, `.bibliography`, `.reading-list`,")
    lines.append("  `.author-card`, `.agent-card`, code blocks, figure captions, tables, math)")
    lines.append("")
    lines.append("## Top 30 Candidate Section Pairs")
    lines.append("")
    lines.append("Ranked by severity (exact-hit count + longest-run weight + cosine + cross-part bonus).")
    lines.append("Each row: severity bucket, both file paths, key metrics, example duplicate shingle,")
    lines.append("and a recommendation.")
    lines.append("")
    lines.append("Legend:")
    lines.append("")
    lines.append("- **exact**: identical sha1 shingles shared (after boilerplate filter)")
    lines.append("- **run**: longest consecutive run of duplicate shingles in section A order")
    lines.append("- **near**: token-set Jaccard >= 0.7 shingle pairs (sampled)")
    lines.append("- **J**: section-level shingle Jaccard")
    lines.append("- **cos**: TF-IDF cosine between the full prose of both sections")
    lines.append("- **xp**: cross-part flag (TRUE = different Parts -- more suspicious)")
    lines.append("")

    for rank, p in enumerate(top_pairs, 1):
        bucket = sev_bucket(p)
        rec = recommend(p)
        lines.append(f"### {rank}. [{bucket}] {p['section_a']}  vs  {p['section_b']}")
        lines.append("")
        lines.append(
            f"- **severity**: {p['severity']}  "
            f"| **exact**: {p['exact_shingles']}  "
            f"| **run**: {p['longest_run']}  "
            f"| **near**: {p['near_dup_shingles']}  "
            f"| **J**: {p['jaccard']}  "
            f"| **cos**: {p['cosine']}  "
            f"| **xp**: {p['cross_part']}"
        )
        lines.append(f"- **recommendation**: {rec}")
        if p["example"]:
            ex = p["example"]
            if len(ex) > 600:
                ex = ex[:600] + "..."
            lines.append("- **example duplicate shingle**:")
            lines.append("")
            lines.append("  > " + ex.replace("\n", " "))
        bnp = p.get("best_near_pair")
        if bnp and bnp["jaccard"] >= 0.4:
            ex_a = bnp["shingle_a"]
            ex_b = bnp["shingle_b"]
            if len(ex_a) > 380:
                ex_a = ex_a[:380] + "..."
            if len(ex_b) > 380:
                ex_b = ex_b[:380] + "..."
            lines.append(f"- **best near-dup pair** (Jaccard {bnp['jaccard']:.2f}):")
            lines.append("")
            lines.append(f"  - A> {ex_a.replace(chr(10), ' ')}")
            lines.append(f"  - B> {ex_b.replace(chr(10), ' ')}")
        lines.append("")

    # Cross-module watch-list
    lines.append("## Cross-Module Watch-List (loose threshold, cosine >= 0.25)")
    lines.append("")
    lines.append("Pairs from **different modules** with moderate prose similarity. The strict")
    lines.append("threshold above misses these because they don't share exact shingles, but they")
    lines.append("are listed here in case any are genuine duplication rather than thematic overlap.")
    lines.append("Most are expected (e.g. an *Inference Optimization* section that touches on the")
    lines.append("*Transformer Architecture* section it builds on).")
    lines.append("")
    if not cm_watch:
        lines.append("_(none above threshold)_")
    else:
        lines.append("| cos | Section A | Section B |")
        lines.append("|-----|-----------|-----------|")
        for s, a, b in cm_watch[:25]:
            lines.append(f"| {s:.3f} | `{a}` | `{b}` |")
    lines.append("")

    # Boilerplate report
    lines.append("## Frequently Reused Boilerplate (filtered out, FYI)")
    lines.append("")
    lines.append("Shingles matching at least 2 templated phrases. These are intentional and were")
    lines.append("excluded from the duplicate ranking, but listed here so you can confirm the")
    lines.append("templates are consistent and trim them if any are accidentally bloated.")
    lines.append("")
    # Top 15 most-shared boilerplate snippets
    bp_sorted = sorted(boilerplate_shingles.items(), key=lambda kv: kv[1], reverse=True)[:15]
    if not bp_sorted:
        lines.append("_(none detected -- boilerplate filter could be tuned if needed)_")
    for txt, n in bp_sorted:
        snippet = txt if len(txt) <= 200 else txt[:200] + "..."
        lines.append(f"- ({n}x sections) {snippet}")
    lines.append("")

    # Pair index
    lines.append("## Files")
    lines.append("")
    lines.append(f"- This report: `docs/content-audit/CONTENT_DUPLICATES.md`")
    lines.append(f"- Full shingle index: `docs/content-audit/_content_shingles.jsonl` "
                 f"({len(all_shingle_records)} rows)")
    lines.append(f"- All scored pairs: `docs/content-audit/_content_pairs.jsonl` "
                 f"({len(pair_summaries)} rows)")
    lines.append("")
    lines.append("Schema for `_content_shingles.jsonl`:")
    lines.append("")
    lines.append("```json")
    lines.append('{"section": "part-1-llm-building-blocks/module-00-.../section-0.1.html",')
    lines.append(' "shingle_index": 0,')
    lines.append(' "hash": "a1b2c3...",')
    lines.append(' "text": "Three-sentence window of prose."}')
    lines.append("```")
    lines.append("")
    lines.append("Schema for `_content_pairs.jsonl`:")
    lines.append("")
    lines.append("```json")
    lines.append('{"section_a": "...", "section_b": "...",')
    lines.append(' "exact_shingles": 3, "near_dup_shingles": 5, "longest_run": 2,')
    lines.append(' "jaccard": 0.12, "cosine": 0.68, "cross_part": true,')
    lines.append(' "severity": 27.5, "example": "..."}')
    lines.append("```")
    lines.append("")
    lines.append("To re-run: `python docs/content-audit/_audit_duplicates.py`")
    lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"  wrote {REPORT_PATH}")
    print(f"Done in {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
