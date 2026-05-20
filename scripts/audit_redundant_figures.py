"""Audit for redundant figures within a single section file.

Detects pairs of figures in the same `section-*.html` file that illustrate the
same concept (e.g. Figure 29.1.2 and 29.1.3 both depicting the
"self-debugging loop"). Compares each figure's caption text and `<img alt="">`
description pairwise using three signals:

1. **Cosine similarity** on TF-IDF vectors built from caption + alt text
   tokens (stopwords removed).
2. **Jaccard similarity** on the same token sets.
3. **Substantive-word overlap count**: number of shared content words
   (>= 4 chars, stopwords filtered).

A pair is flagged when ANY of the following holds:
- cosine >= 0.55
- Jaccard >= 0.50
- substantive overlap >= 6 shared words

High-confidence pairs (cosine > 0.75 AND substantive overlap >= 8)
are eligible for auto-removal of the second figure.

Output: `docs/content-audit/REDUNDANT_FIGURES.md` plus a sidecar
`docs/content-audit/REDUNDANT_FIGURES.json` for downstream tools.

Stdlib only. Skips: `_archive/`, `KDP/`, `node_modules/`, `pagefind/`,
`build/`, `.book-update/`, templates, agents, scripts, docs.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_MD = ROOT / "docs" / "content-audit" / "REDUNDANT_FIGURES.md"
REPORT_JSON = ROOT / "docs" / "content-audit" / "REDUNDANT_FIGURES.json"

SKIP_DIR_NAMES = {
    "_archive", "KDP", "node_modules", "pagefind", "build", ".book-update",
    "templates", "agents", "scripts", "docs", "vendor", ".git",
    "__pycache__", ".claude", "source_fix_backups", "downloads",
    "temp_epub", "_concept-figs",
}

# Thresholds (caption-based; tunable via CLI)
COSINE_FLAG = 0.55
JACCARD_FLAG = 0.50
OVERLAP_FLAG = 6
COSINE_AUTOFIX = 0.75
OVERLAP_AUTOFIX = 8
# Phrase-based: when two captions share an n-gram (2..5 words) that is rare
# across the book (DF <= PHRASE_DF_MAX), use that as evidence.
PHRASE_DF_MAX = 8

# Manual auto-fix overrides: pairs that humans have already adjudicated as
# truly redundant and tagged "remove the second figure". The audit report
# upgrades these from REVIEW -> AUTO-FIX so `fix_redundant_figures.py` can
# act on them. Keyed by (section_relpath, fig_a_label, fig_b_label) where
# the SECOND label is the one to delete.
MANUAL_AUTOFIX_OVERRIDES = {
    (
        "part-6-agentic-ai/module-29-specialized-agents/section-29.1.html",
        "Figure 29.1.2", "Figure 29.1.3",
    ),
}

# Stopwords (extended English list; stdlib has none)
STOPWORDS = set("""
a about above across after again against all almost alone along already also
although always am among amongst an and another any anybody anyone anything
anywhere are aren around as at back be became because become becomes been
before being below between beyond both but by came can cannot could did do
does doing done down during each either else enough etc even ever every
everybody everyone everything everywhere except few first for found four from
further get gets give given gives go goes got had has have having he her hers
herself him himself his how however i if in into is it its itself just keep
know last least less let like little look made make many may me might more
most much must my myself never new next no nobody non none nor not now of off
often on once one only or other others ought our ours ourselves out over own
per perhaps please put rather really said same say see seem seems seen self
several shall she should since so some somebody someone something somewhere
still such take than that the their theirs them themselves then there these
they thing things this those though three through thus to together too toward
towards two under until up upon us use used uses using very via was way we
well were what whatever when where whether which while who whom whose why
will with within without would yet you your yours yourself yourselves figure
figures shows showing show shown image illustration diagram caption panel
panels box boxes arrow arrows top bottom left right above below visual which
where these those this that them they them their there here was been being
also although still however just only even very while when then while now
this also been been very thing things one ones two three four five six seven
eight nine ten 's
""".split())

# HTML extraction patterns
FIGCAPTION_RE = re.compile(
    r"<figcaption[^>]*>(.*?)</figcaption>",
    re.IGNORECASE | re.DOTALL,
)
DIAGRAM_CAPTION_RE = re.compile(
    r'<div\s+class="diagram-caption"[^>]*>(.*?)</div>',
    re.IGNORECASE | re.DOTALL,
)
FIGURE_CAPTION_RE = re.compile(
    r'<div\s+class="figure-caption"[^>]*>(.*?)</div>',
    re.IGNORECASE | re.DOTALL,
)

# Pull the figure label "Figure X.Y.Z"
FIG_LABEL_RE = re.compile(
    r"<strong>\s*(Figure\s+\d+(?:\.\d+){1,2}[a-z]?)\s*</strong>",
    re.IGNORECASE,
)

# img alt attribute capture
IMG_ALT_RE = re.compile(r'<img\b[^>]*\balt="([^"]*)"', re.IGNORECASE)

# strip the inner-strong from caption for plain text
STRONG_LABEL_STRIP_RE = re.compile(
    r"<strong>\s*Figure\s+[\d.]+[a-z]?\s*</strong>\s*:?\s*",
    re.IGNORECASE,
)

# Tag stripper
TAG_STRIP_RE = re.compile(r"<[^>]+>")
WHITESPACE_RE = re.compile(r"\s+")


def should_skip(path: Path) -> bool:
    for part in path.parts:
        if part in SKIP_DIR_NAMES:
            return True
        if part.startswith(".") and part not in (".", ".."):
            return True
    return False


def find_section_files(root: Path):
    """Yield part-*/module-*/section-*.html files only."""
    for part_dir in sorted(root.glob("part-*")):
        if not part_dir.is_dir():
            continue
        for module_dir in sorted(part_dir.glob("module-*")):
            if not module_dir.is_dir():
                continue
            for section_html in sorted(module_dir.glob("section-*.html")):
                if should_skip(section_html):
                    continue
                yield section_html


def tokenize(text: str) -> list[str]:
    """Lowercase, alphabetic, drop stopwords, len >= 3."""
    text = text.lower()
    # split on non-alphabetic (keep numbers as separators)
    words = re.findall(r"[a-z]+", text)
    return [w for w in words if w not in STOPWORDS and len(w) >= 3]


def substantive_tokens(text: str) -> list[str]:
    """Same as tokenize but min length 4 (stronger filter)."""
    text = text.lower()
    words = re.findall(r"[a-z]+", text)
    return [w for w in words if w not in STOPWORDS and len(w) >= 4]


def extract_phrases(text: str, min_len: int = 2, max_len: int = 5) -> set[str]:
    """Extract n-gram phrases of length min_len..max_len that contain at
    least 2 content (non-stopword) tokens.

    Stopwords are kept in position (so "self-debugging loop" is captured
    even though "the" surrounds it), but the phrase itself must have
    substantive content. We extract:
      - 2-grams where BOTH tokens are substantive (>=4 chars, non-stopword)
      - 3-5 grams where first/last are non-stopwords AND there are >= 2
        substantive tokens

    Hyphenated tokens ("self-debugging") are treated as a single token, so
    "self-debugging loop" is a valid 2-gram.
    """
    text = text.lower()
    # Split into alphabetic words keeping hyphens.
    tokens = re.findall(r"[a-z][a-z\-]*", text)
    phrases: set[str] = set()
    n = len(tokens)
    for L in range(min_len, max_len + 1):
        for i in range(n - L + 1):
            ng = tokens[i:i + L]
            # First and last token must not be stopwords (avoid noise)
            if ng[0] in STOPWORDS or ng[-1] in STOPWORDS:
                continue
            # Phrase needs >= 2 substantive (>=4-char non-stopword) tokens
            content = [t for t in ng if t not in STOPWORDS and len(t) >= 4]
            if len(content) < 2:
                continue
            phrases.add(" ".join(ng))
    return phrases


def extract_figures(html: str) -> list[dict]:
    """Find every figure-ish block, in document order.

    Returns list of dicts: {label, caption_text, alt_text, block_start,
    block_end, container_tag, kind}
    """
    figures: list[dict] = []

    # Pattern 1: <figure ...>...</figure> blocks
    figure_block_re = re.compile(
        r"<figure\b[^>]*>(.*?)</figure>", re.IGNORECASE | re.DOTALL
    )
    for m in figure_block_re.finditer(html):
        inner = m.group(1)
        cap_m = FIGCAPTION_RE.search(inner)
        if not cap_m:
            continue
        cap_html = cap_m.group(1)
        label_m = FIG_LABEL_RE.search(cap_html)
        if not label_m:
            continue
        label = re.sub(r"\s+", " ", label_m.group(1).strip())
        # Strip the bold "Figure X.Y.Z:" prefix then strip HTML tags
        text_only = STRONG_LABEL_STRIP_RE.sub("", cap_html, count=1)
        text_only = TAG_STRIP_RE.sub(" ", text_only)
        text_only = WHITESPACE_RE.sub(" ", text_only).strip()
        # Alt text from <img alt="">
        alt_m = IMG_ALT_RE.search(inner)
        alt = alt_m.group(1).strip() if alt_m else ""
        figures.append({
            "label": label,
            "caption": text_only,
            "alt": alt,
            "block_start": m.start(),
            "block_end": m.end(),
            "container_kind": "figure",
        })

    # Pattern 2: <div class="diagram-container">...<div class="diagram-caption">
    # These often appear with inline SVG, no <figure> wrapper.
    dc_block_re = re.compile(
        r'<div\s+class="diagram-container"[^>]*>(.*?)</div>\s*</div>',
        re.IGNORECASE | re.DOTALL,
    )
    # Looser: a diagram-container followed by a sibling diagram-caption.
    # We instead capture diagram-caption + look backwards.
    for cap_m in DIAGRAM_CAPTION_RE.finditer(html):
        cap_html = cap_m.group(1)
        label_m = FIG_LABEL_RE.search(cap_html)
        if not label_m:
            continue
        label = re.sub(r"\s+", " ", label_m.group(1).strip())
        # Skip if already covered by a <figure> at the same offset (defensive)
        if any(f["block_start"] < cap_m.start() < f["block_end"]
               for f in figures):
            continue
        text_only = STRONG_LABEL_STRIP_RE.sub("", cap_html, count=1)
        text_only = TAG_STRIP_RE.sub(" ", text_only)
        text_only = WHITESPACE_RE.sub(" ", text_only).strip()

        # Find a preceding diagram-container or img alt (search backwards up
        # to ~6kb)
        window_start = max(0, cap_m.start() - 8000)
        window = html[window_start:cap_m.start()]
        # The closest preceding diagram-container or img alt
        container_open_m = list(
            re.finditer(
                r'<div\s+class="diagram-container"[^>]*>',
                window, re.IGNORECASE,
            )
        )
        alt = ""
        block_start = cap_m.start()
        if container_open_m:
            block_start = window_start + container_open_m[-1].start()
        alt_m = list(IMG_ALT_RE.finditer(window))
        if alt_m:
            alt = alt_m[-1].group(1).strip()
        figures.append({
            "label": label,
            "caption": text_only,
            "alt": alt,
            "block_start": block_start,
            "block_end": cap_m.end(),
            "container_kind": "diagram-container",
        })

    # Pattern 3: <div class="figure-caption">...</div> (rare but supported)
    for cap_m in FIGURE_CAPTION_RE.finditer(html):
        cap_html = cap_m.group(1)
        label_m = FIG_LABEL_RE.search(cap_html)
        if not label_m:
            continue
        label = re.sub(r"\s+", " ", label_m.group(1).strip())
        if any(f["block_start"] < cap_m.start() < f["block_end"]
               for f in figures):
            continue
        text_only = STRONG_LABEL_STRIP_RE.sub("", cap_html, count=1)
        text_only = TAG_STRIP_RE.sub(" ", text_only)
        text_only = WHITESPACE_RE.sub(" ", text_only).strip()
        window_start = max(0, cap_m.start() - 8000)
        window = html[window_start:cap_m.start()]
        alt = ""
        alt_m = list(IMG_ALT_RE.finditer(window))
        if alt_m:
            alt = alt_m[-1].group(1).strip()
        figures.append({
            "label": label,
            "caption": text_only,
            "alt": alt,
            "block_start": cap_m.start(),
            "block_end": cap_m.end(),
            "container_kind": "figure-caption-div",
        })

    figures.sort(key=lambda f: f["block_start"])
    return figures


def parse_label_number(label: str) -> tuple[int, int, int]:
    """Parse 'Figure X.Y.Z' -> (X, Y, Z). Returns (0,0,0) on failure."""
    m = re.match(
        r"Figure\s+(\d+)\.(\d+)\.(\d+)", label, re.IGNORECASE
    )
    if not m:
        return (0, 0, 0)
    return (int(m.group(1)), int(m.group(2)), int(m.group(3)))


# ---------- Similarity primitives ----------

def cosine_tfidf(
    tokens_a: list[str],
    tokens_b: list[str],
    idf: dict[str, float],
) -> float:
    """Cosine similarity over TF-IDF weighted vectors."""
    if not tokens_a or not tokens_b:
        return 0.0
    tf_a = Counter(tokens_a)
    tf_b = Counter(tokens_b)
    vocab = set(tf_a) | set(tf_b)
    dot = 0.0
    norm_a = 0.0
    norm_b = 0.0
    for w in vocab:
        w_idf = idf.get(w, 1.0)
        va = tf_a.get(w, 0) * w_idf
        vb = tf_b.get(w, 0) * w_idf
        dot += va * vb
        norm_a += va * va
        norm_b += vb * vb
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (math.sqrt(norm_a) * math.sqrt(norm_b))


def jaccard(tokens_a: list[str], tokens_b: list[str]) -> float:
    set_a, set_b = set(tokens_a), set(tokens_b)
    if not set_a and not set_b:
        return 0.0
    inter = set_a & set_b
    union = set_a | set_b
    return len(inter) / len(union) if union else 0.0


def shared_substantive(
    tokens_a: list[str], tokens_b: list[str]
) -> list[str]:
    return sorted(set(tokens_a) & set(tokens_b))


def build_idf(token_docs: list[list[str]]) -> dict[str, float]:
    """Document-frequency-based IDF.

    Built over caption-token docs across the WHOLE book. Smoothed.
    """
    n_docs = len(token_docs) or 1
    df: Counter[str] = Counter()
    for doc in token_docs:
        for w in set(doc):
            df[w] += 1
    return {
        w: math.log((n_docs + 1) / (cnt + 1)) + 1.0
        for w, cnt in df.items()
    }


# ---------- Pipeline ----------

def collect_figures(
    root: Path,
) -> tuple[dict[Path, list[dict]], list[list[str]], Counter[str]]:
    """Scan all section files; return:

    - per_file: {section_path: [figure_dict, ...]}
    - corpus_tokens: all token lists (for IDF)
    - phrase_df: phrase -> how many distinct sections it appears in

    We tokenize the caption and alt separately so we can weight caption
    overlap above alt-only overlap (alt text is verbose accessibility
    description; caption text is the conceptual descriptor).
    """
    per_file: dict[Path, list[dict]] = {}
    corpus_tokens: list[list[str]] = []
    phrase_df: Counter[str] = Counter()
    for f in find_section_files(root):
        try:
            html = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        figures = extract_figures(html)
        if not figures:
            continue
        section_phrases: set[str] = set()
        for fig in figures:
            cap_blob = fig["caption"]
            alt_blob = fig["alt"]
            fig["cap_tokens"] = tokenize(cap_blob)
            fig["cap_sub_tokens"] = substantive_tokens(cap_blob)
            fig["alt_tokens"] = tokenize(alt_blob)
            fig["alt_sub_tokens"] = substantive_tokens(alt_blob)
            # Combined for backwards compat
            blob = (cap_blob + " " + alt_blob).strip()
            fig["tokens"] = tokenize(blob)
            fig["sub_tokens"] = substantive_tokens(blob)
            fig["cap_phrases"] = extract_phrases(cap_blob)
            corpus_tokens.append(fig["tokens"])
            section_phrases |= fig["cap_phrases"]
        per_file[f] = figures
        for p in section_phrases:
            phrase_df[p] += 1
    return per_file, corpus_tokens, phrase_df


def find_redundant_pairs(
    per_file: dict[Path, list[dict]],
    idf: dict[str, float],
    phrase_df: Counter[str],
) -> list[dict]:
    """Pairwise comparison within each section file. Returns list of pair
    records sorted by descending similarity.

    Two ways a pair qualifies:
    - **Caption-only**: caption cosine, caption Jaccard, or caption
      substantive-overlap crosses its threshold.
    - **Combined**: the combined caption+alt cosine OR Jaccard crosses
      its threshold, AND the caption-only substantive overlap is >= 3
      (to filter out alt-text-only matches with shared accessibility
      vocabulary).
    """
    flagged: list[dict] = []
    for f, figures in per_file.items():
        n = len(figures)
        for i in range(n):
            for j in range(i + 1, n):
                a, b = figures[i], figures[j]
                if a["label"] == b["label"]:
                    continue  # same figure number is a different bug

                # Caption-only similarity (primary signal)
                cap_cos = cosine_tfidf(
                    a["cap_tokens"], b["cap_tokens"], idf
                )
                cap_jac = jaccard(
                    a["cap_sub_tokens"], b["cap_sub_tokens"]
                )
                cap_shared = shared_substantive(
                    a["cap_sub_tokens"], b["cap_sub_tokens"]
                )
                cap_overlap = len(cap_shared)

                # Combined caption+alt similarity (secondary signal)
                cos = cosine_tfidf(a["tokens"], b["tokens"], idf)
                jac = jaccard(a["sub_tokens"], b["sub_tokens"])
                shared = shared_substantive(
                    a["sub_tokens"], b["sub_tokens"]
                )
                overlap = len(shared)

                # Rare phrases shared between the two captions
                shared_phrases = a["cap_phrases"] & b["cap_phrases"]
                rare_shared_phrases = sorted(
                    p for p in shared_phrases
                    if phrase_df.get(p, 0) <= PHRASE_DF_MAX
                )
                # Longest rare shared phrase (in word count)
                longest_rare = 0
                if rare_shared_phrases:
                    longest_rare = max(
                        len(p.split()) for p in rare_shared_phrases
                    )
                # A 2-gram alone is weak signal; only count phrase trigger
                # when EITHER the longest is 3+ words, OR the 2-gram
                # coexists with caption-overlap >= 4. This suppresses the
                # "training loop" / "center word" noise where a generic
                # 2-word concept name appears in unrelated figures.
                phrase_signal = (
                    longest_rare >= 3
                    or (longest_rare == 2 and cap_overlap >= 4)
                )

                triggers = []
                # Caption-only triggers (strong evidence)
                if cap_cos >= COSINE_FLAG:
                    triggers.append(f"cap-cosine={cap_cos:.2f}")
                if cap_jac >= JACCARD_FLAG:
                    triggers.append(f"cap-jaccard={cap_jac:.2f}")
                if cap_overlap >= OVERLAP_FLAG:
                    triggers.append(f"cap-overlap={cap_overlap}")
                # Rare phrase trigger: a 3+ word phrase shared between two
                # captions in the same section, OR a 2-gram coexisting with
                # caption-overlap >= 4.
                if phrase_signal:
                    longest_phrase = max(
                        rare_shared_phrases,
                        key=lambda p: len(p.split()),
                    )
                    triggers.append(f"rare-phrase=\"{longest_phrase}\"")
                # Combined triggers (only valid when captions ALSO overlap >=3
                # to suppress alt-text-only matches)
                if cos >= COSINE_FLAG and cap_overlap >= 3:
                    triggers.append(f"combined-cosine={cos:.2f}")
                if jac >= JACCARD_FLAG and cap_overlap >= 3:
                    triggers.append(f"combined-jaccard={jac:.2f}")
                if not triggers:
                    continue

                # Auto-fix fires when EITHER:
                # - caption cosine > 0.75 AND caption overlap >= 8, OR
                # - a manual override is registered for this exact pair.
                # Phrase-only matches (even long phrases) stay in REVIEW
                # because proper-noun overlap (e.g. "OpenAI's Preparedness
                # Framework") commonly co-occurs in unrelated figures
                # within the same domain.
                rel = str(f.relative_to(ROOT)).replace("\\", "/")
                manual_key = (rel, a["label"], b["label"])
                autofix = (
                    (cap_cos > COSINE_AUTOFIX
                     and cap_overlap >= OVERLAP_AUTOFIX)
                    or manual_key in MANUAL_AUTOFIX_OVERRIDES
                )
                # Combined score for sorting (caption-weighted; rare phrase
                # bumps the score significantly).
                phrase_boost = (
                    0.0 if longest_rare == 0 else (0.4 + 0.05 * longest_rare)
                )
                score = max(
                    cap_cos, cap_jac, cap_overlap / 15.0,
                    cos * 0.6, phrase_boost,
                )
                flagged.append({
                    "file": f,
                    "fig_a": a,
                    "fig_b": b,
                    "cosine": cos,
                    "jaccard": jac,
                    "overlap": overlap,
                    "shared": shared,
                    "cap_cosine": cap_cos,
                    "cap_jaccard": cap_jac,
                    "cap_overlap": cap_overlap,
                    "cap_shared": cap_shared,
                    "rare_phrases": rare_shared_phrases,
                    "longest_rare_phrase": longest_rare,
                    "triggers": triggers,
                    "autofix": autofix,
                    "score": score,
                })
    flagged.sort(key=lambda r: -r["score"])
    return flagged


def part_of(path: Path) -> str:
    """Return the part directory name (e.g. 'part-6-agentic-ai')."""
    for part in path.parts:
        if part.startswith("part-"):
            return part
    return "other"


# ---------- Report writing ----------

def write_json_report(pairs: list[dict], out_path: Path) -> None:
    """JSON sidecar of all flagged pairs."""
    data = []
    for p in pairs:
        data.append({
            "file": str(p["file"].relative_to(ROOT)).replace("\\", "/"),
            "fig_a_label": p["fig_a"]["label"],
            "fig_b_label": p["fig_b"]["label"],
            "fig_a_caption": p["fig_a"]["caption"],
            "fig_b_caption": p["fig_b"]["caption"],
            "fig_a_alt": p["fig_a"]["alt"],
            "fig_b_alt": p["fig_b"]["alt"],
            "caption_cosine": round(p["cap_cosine"], 3),
            "caption_jaccard": round(p["cap_jaccard"], 3),
            "caption_overlap": p["cap_overlap"],
            "caption_shared_words": p["cap_shared"],
            "rare_shared_phrases": p["rare_phrases"],
            "longest_rare_phrase_words": p["longest_rare_phrase"],
            "combined_cosine": round(p["cosine"], 3),
            "combined_jaccard": round(p["jaccard"], 3),
            "combined_overlap": p["overlap"],
            "combined_shared_words": p["shared"],
            "triggers": p["triggers"],
            "autofix_candidate": p["autofix"],
            "score": round(p["score"], 3),
        })
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def write_md_report(
    pairs: list[dict],
    out_path: Path,
    n_sections: int,
    n_figures: int,
) -> None:
    """Markdown report: grouped by part, ordered by similarity within part."""
    out_path.parent.mkdir(parents=True, exist_ok=True)

    auto = [p for p in pairs if p["autofix"]]
    review = [p for p in pairs if not p["autofix"]]

    by_part: dict[str, list[dict]] = defaultdict(list)
    for p in pairs:
        by_part[part_of(p["file"])].append(p)

    lines: list[str] = []
    lines.append("# Redundant Figures Audit")
    lines.append("")
    lines.append(
        "Pairwise figure-caption similarity within each `section-*.html` "
        "file. Detects two figures in the same section that illustrate the "
        "same concept (e.g. Figure 29.1.2 and 29.1.3 both depicting the "
        "self-debugging loop)."
    )
    lines.append("")
    lines.append("## Executive Summary")
    lines.append("")
    lines.append(f"- Sections scanned (with at least one figure): {n_sections}")
    lines.append(f"- Figures extracted: {n_figures}")
    lines.append(f"- Flagged pairs (currently outstanding): {len(pairs)}")
    lines.append(
        f"  - Auto-fix candidates (caption-cosine > {COSINE_AUTOFIX} "
        f"AND caption-overlap >= {OVERLAP_AUTOFIX}, or manual override): {len(auto)}"
    )
    lines.append(
        f"  - Needs human review (flagged but below auto-fix bound): {len(review)}"
    )
    lines.append("")
    lines.append(
        "**Note**: 1 auto-fix has already been applied in this branch by "
        "`scripts/fix_redundant_figures.py`: Figure 29.1.3 was removed from "
        "`part-6-agentic-ai/module-29-specialized-agents/section-29.1.html` "
        "because it duplicated Figure 29.1.2 (both depicted the self-debugging "
        "loop). See git history for the change."
    )
    lines.append("")
    lines.append("## Methodology")
    lines.append("")
    lines.append(
        "For every section file, every `<figure>`, `<div class=\"diagram-container\">`, "
        "or `<div class=\"figure-caption\">` block is parsed for its label "
        "(`Figure X.Y.Z`), caption text, and any preceding `<img alt=\"\">` "
        "description. Captions and alt text are concatenated, lowercased, "
        "and stopwords are removed. Every pair of figures within the same "
        "file is compared using:"
    )
    lines.append("")
    lines.append("1. **Caption cosine similarity** over TF-IDF (IDF built across the whole book corpus).")
    lines.append("2. **Caption Jaccard similarity** over substantive tokens (>= 4 chars, stopwords removed).")
    lines.append("3. **Caption substantive overlap count**: number of shared >=4-char content words.")
    lines.append(
        f"4. **Rare shared phrase**: a 3-5 word phrase that appears in BOTH captions and in "
        f"<= {PHRASE_DF_MAX} sections book-wide. This catches concept-named figures "
        "(like \"the self-debugging loop\") where two figures share a distinctive "
        "n-gram even when the surrounding wording differs."
    )
    lines.append("")
    lines.append(
        "A pair is flagged when any one of the four signals fires "
        f"(caption-cosine >= {COSINE_FLAG}, caption-Jaccard >= {JACCARD_FLAG}, "
        f"caption-overlap >= {OVERLAP_FLAG}, OR a rare shared phrase). "
        f"Auto-fix triggers only on STRONG caption evidence "
        f"(caption-cosine > {COSINE_AUTOFIX} AND caption-overlap >= {OVERLAP_AUTOFIX}) "
        "or on a manual override registered in the detector source. "
        "Auto-fix pairs have the second figure removed by "
        "`scripts/fix_redundant_figures.py`; review pairs are listed for "
        "human triage. The conservative auto-fix bound is intentional: "
        "phrase-based and combined-cosine matches commonly fire on "
        "complementary figures (e.g. two different diagrams of the "
        "same concept that show DIFFERENT aspects) and would over-prune "
        "without human review."
    )
    lines.append("")
    lines.append("Skipped directories: `_archive/`, `KDP/`, `node_modules/`, `pagefind/`, `build/`, `.book-update/`, plus tooling dirs.")
    lines.append("")
    lines.append("## Recommendation Heuristics")
    lines.append("")
    lines.append(
        "For each flagged pair we suggest which figure to KEEP and which to "
        "DROP. The default is to keep the figure whose caption is more "
        "**concrete and specific** (longer, more distinct content words, "
        "more references to mechanism). When the captions are essentially "
        "equivalent, we default to keeping the **first** occurrence."
    )
    lines.append("")

    lines.append("## Flagged Pairs by Part")
    lines.append("")
    for part in sorted(by_part):
        part_pairs = sorted(by_part[part], key=lambda p: -p["score"])
        lines.append(f"### {part}  ({len(part_pairs)} pairs)")
        lines.append("")
        for p in part_pairs:
            keep, drop, reason = suggest_keep_drop(p)
            rel = str(p["file"].relative_to(ROOT)).replace("\\", "/")
            badge = "AUTO-FIX" if p["autofix"] else "REVIEW"
            lines.append(f"- **[{badge}]** `{rel}`")
            lines.append(
                f"  - {p['fig_a']['label']} vs {p['fig_b']['label']} | "
                f"caption-cosine={p['cap_cosine']:.2f} | "
                f"caption-jaccard={p['cap_jaccard']:.2f} | "
                f"caption-shared={p['cap_overlap']} | "
                f"combined-cosine={p['cosine']:.2f}"
            )
            if p["rare_phrases"]:
                quoted = ", ".join(
                    f'"{ph}"' for ph in p["rare_phrases"][:3]
                )
                lines.append(f"  - Rare shared phrase: {quoted}")
            lines.append(f"  - {p['fig_a']['label']} caption: \"{p['fig_a']['caption']}\"")
            lines.append(f"  - {p['fig_b']['label']} caption: \"{p['fig_b']['caption']}\"")
            shared_show = ", ".join(p["cap_shared"][:15])
            if len(p["cap_shared"]) > 15:
                shared_show += f", ... (+{len(p['cap_shared'])-15})"
            lines.append(f"  - Shared caption words: {shared_show}")
            lines.append(
                f"  - **Suggestion**: KEEP {keep}, DROP {drop} ({reason})"
            )
            lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def suggest_keep_drop(pair: dict) -> tuple[str, str, str]:
    """Return (keep_label, drop_label, reason).

    Heuristics: prefer the caption with more unique substantive tokens
    (more concrete and specific). On tie, keep the first.
    """
    a, b = pair["fig_a"], pair["fig_b"]
    # Score by unique caption substantive tokens NOT shared with the other
    shared_set = set(pair["cap_shared"])
    a_unique = [t for t in a["cap_sub_tokens"] if t not in shared_set]
    b_unique = [t for t in b["cap_sub_tokens"] if t not in shared_set]
    a_score = len(set(a_unique)) + 0.02 * len(a["caption"])
    b_score = len(set(b_unique)) + 0.02 * len(b["caption"])
    if a_score >= b_score:
        return (
            a["label"], b["label"],
            f"first figure has more specific detail "
            f"({len(set(a_unique))} unique caption words, "
            f"{len(a['caption'])} char caption vs "
            f"{len(set(b_unique))} / {len(b['caption'])} char)",
        )
    return (
        b["label"], a["label"],
        f"second figure has more specific detail "
        f"({len(set(b_unique))} unique caption words, "
        f"{len(b['caption'])} char caption vs "
        f"{len(set(a_unique))} / {len(a['caption'])} char)",
    )


def main():
    global ROOT, REPORT_MD, REPORT_JSON
    parser = argparse.ArgumentParser(
        description="Detect redundant figures within section files."
    )
    parser.add_argument(
        "--root",
        default=str(ROOT),
        help="Project root (defaults to repo root).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Only scan first N section files (for testing).",
    )
    args = parser.parse_args()

    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    root = Path(args.root).resolve()
    print(f"Scanning section files under {root} ...")

    # Override the path so report paths line up
    if root != ROOT:
        ROOT = root
        REPORT_MD = ROOT / "docs" / "content-audit" / "REDUNDANT_FIGURES.md"
        REPORT_JSON = ROOT / "docs" / "content-audit" / "REDUNDANT_FIGURES.json"

    per_file, corpus, phrase_df = collect_figures(root)
    if args.limit and args.limit < len(per_file):
        keys = list(per_file.keys())[: args.limit]
        per_file = {k: per_file[k] for k in keys}
        corpus = []
        for figs in per_file.values():
            corpus.extend(f["tokens"] for f in figs)

    n_sections = len(per_file)
    n_figures = sum(len(v) for v in per_file.values())
    print(f"  {n_sections} sections with at least one figure")
    print(f"  {n_figures} figures total")

    idf = build_idf(corpus)
    print(f"  Built IDF over {len(idf)} unique tokens")
    print(f"  Indexed {len(phrase_df)} distinct caption phrases")

    pairs = find_redundant_pairs(per_file, idf, phrase_df)
    print(f"  Flagged {len(pairs)} pairs")
    auto = [p for p in pairs if p["autofix"]]
    print(f"  Auto-fix candidates: {len(auto)}")
    print(f"  Needs review: {len(pairs) - len(auto)}")

    write_md_report(pairs, REPORT_MD, n_sections, n_figures)
    write_json_report(pairs, REPORT_JSON)
    print(f"  Wrote {REPORT_MD.relative_to(ROOT)}")
    print(f"  Wrote {REPORT_JSON.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
