"""Repeated-content audit (cross-section duplication detector).

Walks `part-*/module-*/section-*.html` (skipping tools-of-the-trade modules,
appendices, front-matter, capstone, KDP, node_modules, pagefind, etc.) and
extracts, per section:

  - h2 headings
  - callout titles + body fingerprint
  - code-caption text (Code Fragment X.Y.Z label + caption)
  - long prose paragraphs (>= 200 chars) keyed by first-100-char fingerprint

Then it clusters duplicates and writes a triage report to
`docs/content-audit/REPEATED_CONTENT_AUDIT.md`.

Important: many *structural* callout titles repeat ON PURPOSE in this book
(every section has a Big Picture, a Fun Fact, a Real World Scenario, etc.,
each with unique content). These are NOT real duplication. We detect
duplication at the BODY-FINGERPRINT level, not the title level.

The exception is **lame AI-boilerplate code captions** like "Install the
required packages for this lab" or "This snippet demonstrates this approach.
Study the implementation details..." that legitimately recur verbatim and
should be rewritten with section-specific text.

READ-ONLY. No HTML files are modified.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

from bs4 import BeautifulSoup

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "docs" / "content-audit" / "REPEATED_CONTENT_AUDIT.md"
JSON_DUMP_PATH = ROOT / "docs" / "content-audit" / "_repeated_content_inventory.json"

# Directory exclusions (tools-of-the-trade modules and non-main areas)
EXCLUDE_DIR_FRAGMENTS = (
    "tools-of-the-trade",
)
EXCLUDE_TOP_LEVEL = {
    "KDP", "appendices", "front-matter", "capstone", "node_modules",
    "pagefind", "vendor", "templates", "scripts", "agents", "_concept-figs",
    "temp_epub", "styles", "images", "downloads", "docs",
}

# Boilerplate callout titles to skip (every section has these; they're intentional).
# Includes both "section structure" callouts AND themed callouts whose CONCEPT
# (not body) is repeated by design. We never flag duplication based on title
# alone for these.
BOILERPLATE_CALLOUT_TITLES = {
    # Structural per-section blocks
    "prerequisites", "what's next", "whats next", "what next",
    "key takeaways", "key takeaway", "summary", "exercises", "exercise",
    "self-check", "self check", "quiz", "review questions",
    "bibliography", "further reading", "additional resources",
    "key terms", "glossary",
    # The big "themed" callouts our book uses in EVERY section, each with
    # unique content. Skip them at the title-level detector.
    "big picture", "fun fact", "fun note", "key insight", "key insights",
    "why it matters", "in plain english", "in plain words",
    "real world scenario", "real-world scenario", "real world example",
    "practical example", "practical analogy",
    "tip", "warning", "note", "best practice", "common mistake",
    "common misconception", "pitfall", "gotcha", "caveat",
    "advanced", "deep dive", "side note", "aside",
    # Per-section recurring themed blocks that have unique content per section
    "research frontier", "research frontiers", "frontier",
    "self-check exercises", "self check exercises", "self-check",
    "active research", "open problem", "open problems",
    "what could go wrong", "edge cases", "edge case",
    "concept check", "concept-check", "knowledge check",
    "rapid review", "quick review",
    # Title-prefixed variants we see a lot ("Note: Learning Objectives",
    # "Tip: Production Alternative") -- the prefix counts as structural.
    "note: learning objectives", "note: modify and observe",
    "tip: production alternative",
    "warning: common misconception",
    "see also", "cross-ref", "cross reference",
    "library shortcut", "lab", "exercise:",
    # Comic-themed
    "agent quip", "agent banter",
}

# Title prefixes that indicate "structural" callouts. If a title starts with any
# of these (case-insensitive), it's structural and we skip title-level matching.
STRUCTURAL_TITLE_PREFIXES = (
    "note:", "tip:", "warning:", "exercise:", "lab:", "best practice:",
    "common mistake:", "key insight:", "key takeaway:",
    "fun fact:", "fun note:",
)


def collect_section_files() -> list[Path]:
    files = []
    for p in sorted(ROOT.rglob("section-*.html")):
        parts = p.parts
        if not any(part.startswith("part-") for part in parts):
            continue
        if any(part in EXCLUDE_TOP_LEVEL for part in parts):
            continue
        if any(frag in part for part in parts for frag in EXCLUDE_DIR_FRAGMENTS):
            continue
        files.append(p)
    return files


WORD_RE = re.compile(r"\w+", re.UNICODE)


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def fingerprint(text: str, length: int = 150) -> str:
    return normalize_text(text).lower()[:length]


def is_structural_title(title: str) -> bool:
    """True if this callout title is part of the book's recurring structure
    and should NOT be flagged as duplication based on title alone."""
    t = title.strip().lower()
    if not t:
        return True
    if t in BOILERPLATE_CALLOUT_TITLES:
        return True
    for pref in STRUCTURAL_TITLE_PREFIXES:
        if t.startswith(pref):
            return True
    return False


# ----------------------------------------------------------------------
# Per-section extraction
# ----------------------------------------------------------------------

def extract_section_data(html_path: Path) -> dict:
    raw = html_path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(raw, "html.parser")

    main = soup.find("main") or soup
    rel = str(html_path.relative_to(ROOT)).replace("\\", "/")

    data = {
        "path": rel,
        "h2": [],
        "callouts": [],
        "code_captions": [],
        "prose": [],
    }

    for h2 in main.find_all("h2"):
        text = normalize_text(h2.get_text(" ", strip=True))
        if text:
            data["h2"].append(text)

    # Callouts
    for div in main.find_all("div", class_="callout"):
        classes = div.get("class") or []
        title_div = div.find("div", class_="callout-title")
        title = normalize_text(title_div.get_text(" ", strip=True)) if title_div else ""
        title_lower = title.lower().strip()
        # Skip Prerequisites etc.; ALSO record the structural-flag so we can
        # filter title-level matching downstream.
        if title_lower in {"prerequisites", "what's next", "whats next",
                            "what next", "key takeaways", "summary",
                            "exercises", "exercise",
                            "self-check", "self check", "quiz",
                            "review questions", "bibliography",
                            "further reading", "additional resources",
                            "key terms", "glossary"}:
            continue
        first_p = div.find("p")
        body_text = normalize_text((first_p or div).get_text(" ", strip=True))
        if body_text.lower().startswith(title_lower) and title_lower:
            body_text = body_text[len(title_lower):].strip()
        if len(body_text) < 60:
            continue
        line_num = guess_line_number(raw, title) if title else 0
        data["callouts"].append({
            "title": title,
            "is_structural_title": is_structural_title(title),
            "classes": [c for c in classes if c != "callout"],
            "body_fingerprint": fingerprint(body_text, 150),
            "body_preview": body_text[:300],
            "body_full": body_text,
            "line": line_num,
        })

    # Code captions
    for cap in main.find_all("div", class_="code-caption"):
        text = normalize_text(cap.get_text(" ", strip=True))
        if not text:
            continue
        m = re.match(r"(Code\s*Fragment\s*[\d.]+)\s*[.:\-]?\s*(.*)", text, re.IGNORECASE)
        if m:
            label = m.group(1)
            caption = m.group(2).strip()
        else:
            label = ""
            caption = text
        if not caption:
            continue
        line_num = guess_line_number(raw, label or caption[:30])
        data["code_captions"].append({
            "label": label,
            "caption": caption,
            "caption_norm": caption.lower(),
            "fingerprint": fingerprint(caption, 80),
            "fingerprint_long": fingerprint(caption, 200),
            "line": line_num,
        })

    # Prose paragraphs (only direct content paragraphs, not inside callouts/blockquotes/biblio)
    for p in main.find_all("p"):
        skip = False
        for ancestor in p.parents:
            ac = ancestor.get("class") or []
            if any(c in ac for c in ("callout", "prerequisites", "epigraph",
                                      "bibliography", "code-output",
                                      "code-caption")):
                skip = True
                break
            if ancestor.name in ("blockquote", "footer", "header", "nav"):
                skip = True
                break
        if skip:
            continue
        text = normalize_text(p.get_text(" ", strip=True))
        if len(text) < 200:
            continue
        line_num = guess_line_number(raw, text[:50])
        data["prose"].append({
            "fingerprint": fingerprint(text, 100),
            "fingerprint_200": fingerprint(text, 200),
            "preview": text[:300],
            "char_len": len(text),
            "line": line_num,
        })

    return data


def guess_line_number(raw: str, needle: str) -> int:
    if not needle:
        return 0
    idx = raw.find(needle)
    if idx < 0:
        return 0
    return raw[:idx].count("\n") + 1


# ----------------------------------------------------------------------
# Cluster duplicates
# ----------------------------------------------------------------------

def cluster_duplicates(sections: list[dict]) -> dict:
    clusters = {
        "callout_body": defaultdict(list),
        "callout_title_non_structural": defaultdict(list),
        "code_caption_exact": defaultdict(list),
        "code_caption_long_match": defaultdict(list),
        "prose_short_fp": defaultdict(list),
        "prose_long_fp": defaultdict(list),
    }
    for sec in sections:
        for cb in sec["callouts"]:
            # Callout BODY duplications (the real signal)
            if cb["body_fingerprint"]:
                clusters["callout_body"][cb["body_fingerprint"]].append({
                    "section": sec["path"], "line": cb["line"],
                    "title": cb["title"],
                    "preview": cb["body_preview"][:240],
                    "classes": cb["classes"],
                })
            # Title-level duplications, ONLY for non-structural callout titles
            if cb["title"] and not cb["is_structural_title"]:
                title_key = cb["title"].lower()
                if len(title_key) > 6:
                    clusters["callout_title_non_structural"][title_key].append({
                        "section": sec["path"], "line": cb["line"],
                        "preview": cb["body_preview"][:200],
                        "classes": cb["classes"],
                    })
        for cc in sec["code_captions"]:
            # Exact short-fingerprint cluster (catches one-line boilerplate
            # captions like "Code example", "Install the required packages for
            # this lab.").
            if cc["fingerprint"]:
                clusters["code_caption_exact"][cc["fingerprint"]].append({
                    "section": sec["path"], "line": cc["line"],
                    "label": cc["label"], "caption": cc["caption"][:240],
                })
            # Longer (200-char) fingerprint for substantive caption duplication
            if cc["fingerprint_long"] and len(cc["caption"]) > 60:
                clusters["code_caption_long_match"][cc["fingerprint_long"]].append({
                    "section": sec["path"], "line": cc["line"],
                    "label": cc["label"], "caption": cc["caption"][:240],
                })
        for pp in sec["prose"]:
            clusters["prose_short_fp"][pp["fingerprint"]].append({
                "section": sec["path"], "line": pp["line"],
                "preview": pp["preview"][:240],
                "char_len": pp["char_len"],
            })
            if len(pp["preview"]) > 200:
                clusters["prose_long_fp"][pp["fingerprint_200"]].append({
                    "section": sec["path"], "line": pp["line"],
                    "preview": pp["preview"][:240],
                    "char_len": pp["char_len"],
                })

    out = {}
    for cat, mapping in clusters.items():
        kept = {}
        for key, items in mapping.items():
            sections_set = {it["section"] for it in items}
            # Multi-section threshold (>=2 different sections)
            if len(sections_set) >= 2:
                kept[key] = items
        out[cat] = kept
    return out


# ----------------------------------------------------------------------
# Fuzzy code-caption clustering: token-overlap heuristic
# ----------------------------------------------------------------------

CAPTION_STOPWORDS = {
    "a", "an", "the", "and", "or", "for", "of", "to", "in", "on", "with",
    "from", "by", "is", "are", "as", "this", "that", "using", "use",
    "code", "fragment", "example", "shows", "show", "we", "you", "your",
    "it", "its", "into", "at", "than", "be", "can", "if", "but", "not",
    "do", "does", "have", "has", "will", "all", "any", "some", "each",
    "between", "across", "above", "below", "such", "more", "less",
    "very", "also", "then", "so", "out", "over", "via", "no", "one",
    "two", "three", "four", "five", "function", "method", "class", "object",
    "value", "values", "data", "list", "dict", "string", "input", "output",
    "implementation", "details", "step", "steps", "snippet", "tracing",
    "approach", "study", "understand", "component", "contributes", "overall",
    "computation", "intuition", "needed", "builds", "demonstrate", "demonstrates",
    "notice", "how", "where", "when", "what", "which", "their", "they",
    "model", "models", "library", "libraries", "library's",
}


def code_caption_fuzzy_cluster(sections: list[dict]) -> list[dict]:
    """Cluster code captions by content-token overlap.

    Captures things like multiple "Embedding generation for converting text into
    dense vector representations" captions across module-10.
    """
    all_caps = []
    for sec in sections:
        for cc in sec["code_captions"]:
            tokens = [t for t in re.findall(r"[a-z0-9]+", cc["caption"].lower())
                      if t not in CAPTION_STOPWORDS and len(t) > 2]
            all_caps.append({
                "section": sec["path"], "line": cc["line"],
                "label": cc["label"], "caption": cc["caption"][:240],
                "tokens": set(tokens),
            })
    clusters = []
    used = [False] * len(all_caps)
    for i in range(len(all_caps)):
        if used[i]:
            continue
        a = all_caps[i]
        if len(a["tokens"]) < 4:
            continue
        cluster = [a]
        for j in range(i + 1, len(all_caps)):
            if used[j]:
                continue
            b = all_caps[j]
            if a["section"] == b["section"]:
                continue
            overlap = a["tokens"] & b["tokens"]
            min_size = min(len(a["tokens"]), len(b["tokens"]))
            if min_size == 0:
                continue
            # Tightened: require >=5 token overlap OR ratio >= 0.7 with >=4 tokens
            if len(overlap) >= 5 or (len(overlap) >= 4 and len(overlap) / min_size >= 0.7):
                cluster.append(b)
                used[j] = True
        if len(cluster) >= 2:
            sections_in_cluster = {c["section"] for c in cluster}
            if len(sections_in_cluster) >= 2:
                used[i] = True
                # Build a more descriptive key from intersecting top tokens
                inter = set(a["tokens"])
                for c in cluster[1:]:
                    inter &= c["tokens"]
                key = " ".join(sorted(inter)[:6]) or " ".join(sorted(a["tokens"])[:6])
                clusters.append({
                    "key": key,
                    "items": cluster,
                })
    return clusters


# ----------------------------------------------------------------------
# Canonical-home heuristic
# ----------------------------------------------------------------------

# Cluster topic tokens -> canonical-section-prefix.
TOPIC_TO_CANONICAL = [
    (["langchain", "lcel"], "part-3-working-with-llms/module-12-langchain"),
    (["llamaindex", "llama-index"], "part-3-working-with-llms/module-15-llamaindex"),
    (["vllm"], "part-12-llm-systems-at-scale"),
    (["flashattention"], "part-2-understanding-llms/module-09-inference-optimization"),
    (["dpo"], "part-4-training-adaptation/module-18-alignment-rlhf-dpo"),
    (["rlhf"], "part-4-training-adaptation/module-18-alignment-rlhf-dpo"),
    (["rag"], "part-7-retrieval-information-extraction-with-llms/module-32-rag"),
    (["lora", "qlora"], "part-4-training-adaptation/module-17-peft"),
    (["faiss"], "part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db"),
    (["pinecone"], "part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db"),
    (["weaviate"], "part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db"),
    (["chroma", "chromadb"], "part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db"),
    (["pgvector"], "part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db"),
    (["langsmith", "langfuse"], "part-9-llm-evaluation-observability"),
    (["mlflow"], "part-13-llmops-lifecycle"),
    (["wandb"], "part-13-llmops-lifecycle"),
    (["kubernetes", "k8s"], "part-13-llmops-lifecycle/module-65-containers-kubernetes"),
    (["docker"], "part-13-llmops-lifecycle/module-65-containers-kubernetes"),
    (["airflow"], "part-13-llmops-lifecycle"),
    (["openai"], "part-3-working-with-llms/module-11-llm-apis"),
    (["anthropic", "claude"], "part-3-working-with-llms/module-11-llm-apis"),
    (["bertscore", "rouge", "bleu"], "part-9-llm-evaluation-observability"),
    (["embedding", "embeddings"], "part-7-retrieval-information-extraction-with-llms/module-31"),
    (["transformer", "attention"], "part-1-llm-building-blocks/module-03-transformer-architecture"),
    (["tokenization", "bpe"], "part-1-llm-building-blocks/module-01-foundations-nlp-text-representation"),
    (["tokenizer"], "part-1-llm-building-blocks/module-01-foundations-nlp-text-representation"),
    (["beam", "search"], "part-1-llm-building-blocks/module-04-decoding-text-generation"),
    (["temperature", "top-k", "nucleus", "top-p"], "part-1-llm-building-blocks/module-04-decoding-text-generation"),
    (["pretraining", "chinchilla"], "part-2-understanding-llms/module-06-pretraining-scaling-laws"),
    (["peft", "adapter"], "part-4-training-adaptation/module-17-peft"),
    (["evaluation", "evals"], "part-9-llm-evaluation-observability"),
    (["safety", "guardrail"], "part-10-llm-security-runtime-safety"),
]


def canonical_home_for(sections_in: list[str], all_tokens: set[str]) -> str | None:
    for tokens, prefix in TOPIC_TO_CANONICAL:
        if any(tk in all_tokens for tk in tokens):
            for sec in sections_in:
                if sec.startswith(prefix):
                    return sec
    # Fallback: lowest part number
    def part_num(p: str) -> int:
        m = re.search(r"part-(\d+)", p)
        return int(m.group(1)) if m else 999
    return sorted(sections_in, key=part_num)[0] if sections_in else None


# ----------------------------------------------------------------------
# Build report
# ----------------------------------------------------------------------

def render_report(sections: list[dict], clusters: dict, fuzzy_caption_clusters: list[dict]) -> str:
    out = []
    out.append("# Repeated-Content Audit\n")
    out.append("Cross-section duplication triage for the LLM textbook.")
    out.append("")
    out.append("**READ-ONLY scan.** No HTML files have been modified. This report proposes")
    out.append("canonical homes and lists duplicates for the editor to reconcile manually.\n")
    out.append("")

    # ----------------------------------------------------------
    # Methodology
    # ----------------------------------------------------------
    n_sections = len(sections)
    n_callouts = sum(len(s["callouts"]) for s in sections)
    n_captions = sum(len(s["code_captions"]) for s in sections)
    n_prose = sum(len(s["prose"]) for s in sections)

    out.append("## Methodology")
    out.append("")
    out.append(f"- Scanned **{n_sections}** main-track section HTML files under `part-*/module-*/section-*.html`.")
    out.append("- Excluded: `tools-of-the-trade` modules, `appendices/`, `front-matter/`, `capstone/`, `KDP/`, vendor dirs.")
    out.append("- For each section extracted:")
    out.append(f"  - **{n_callouts:,}** non-boilerplate callouts (skipped Prerequisites, Key Takeaways, etc.)")
    out.append(f"  - **{n_captions:,}** code-fragment captions")
    out.append(f"  - **{n_prose:,}** prose paragraphs (>= 200 chars, outside callouts/blockquotes/bibliography)")
    out.append("")
    out.append("**Detection signals (this report only flags REAL duplication, not intentional structure):**")
    out.append("")
    out.append("1. **Callout body fingerprint match** -- first-150-char lowercase fingerprint of the callout body")
    out.append("   matches across 2+ sections. (Title-only matches are skipped for structural callout titles like")
    out.append("   `Fun Fact`, `Big Picture`, `Real World Scenario`, `Key Insight`, `Tip: ...`, `Warning: ...`, `Note: ...`.")
    out.append("   Those repeat by design with unique content per section.)")
    out.append("2. **Code-caption exact fingerprint** -- first-80-char fingerprint match. Catches lame")
    out.append("   AI-boilerplate captions like \"Install the required packages for this lab\" or \"Code example\".")
    out.append("3. **Code-caption fuzzy match** -- >=5 shared content tokens (stopwords removed) between captions.")
    out.append("   Catches paraphrased boilerplate like \"This snippet demonstrates this approach. Study the")
    out.append("   implementation details...\".")
    out.append("4. **Prose paragraph fingerprint match** -- first-100-char fingerprint of a paragraph >= 200 chars")
    out.append("   matches across 2+ sections.")
    out.append("5. **Non-structural callout title match** -- a callout title that is NOT one of the recurring")
    out.append("   structural patterns appears in 2+ sections.")
    out.append("")
    out.append("**Canonical home assignment** combines topic heuristics (RAG -> Part VII module 32, ")
    out.append("Transformers -> Part I module 3, etc.) with a fallback to the lowest-numbered part containing")
    out.append("the duplicated content.")
    out.append("")

    # ----------------------------------------------------------
    # Build a single ranked list of all clusters
    # ----------------------------------------------------------
    ranked: list[dict] = []

    for key, items in clusters["callout_body"].items():
        sections_set = {it["section"] for it in items}
        if len(sections_set) < 2:
            continue
        ranked.append({
            "type": "callout_body",
            "key": key,
            "items": items,
            "n_sections": len(sections_set),
            "score": len(sections_set) * 10 + len(items) * 2,
        })

    for key, items in clusters["callout_title_non_structural"].items():
        sections_set = {it["section"] for it in items}
        if len(sections_set) < 2:
            continue
        ranked.append({
            "type": "callout_title_nonstructural",
            "key": key,
            "items": items,
            "n_sections": len(sections_set),
            "score": len(sections_set) * 4,
        })

    for c in fuzzy_caption_clusters:
        sections_set = {it["section"] for it in c["items"]}
        if len(sections_set) < 2:
            continue
        ranked.append({
            "type": "code_caption_fuzzy",
            "key": c["key"],
            "items": c["items"],
            "n_sections": len(sections_set),
            "score": len(sections_set) * 5 + len(c["items"]),
        })

    for key, items in clusters["code_caption_exact"].items():
        sections_set = {it["section"] for it in items}
        if len(sections_set) < 2:
            continue
        ranked.append({
            "type": "code_caption_exact",
            "key": key,
            "items": items,
            "n_sections": len(sections_set),
            "score": len(sections_set) * 8,
        })

    for key, items in clusters["code_caption_long_match"].items():
        sections_set = {it["section"] for it in items}
        if len(sections_set) < 2:
            continue
        # De-dupe against exact: if same key already in exact, skip
        if key[:80] in clusters["code_caption_exact"]:
            continue
        ranked.append({
            "type": "code_caption_long",
            "key": key,
            "items": items,
            "n_sections": len(sections_set),
            "score": len(sections_set) * 6,
        })

    for key, items in clusters["prose_short_fp"].items():
        sections_set = {it["section"] for it in items}
        if len(sections_set) < 2:
            continue
        # Filter out very-generic openings ("In this section we...")
        if _is_generic_prose_opener(items[0]["preview"]):
            continue
        ranked.append({
            "type": "prose",
            "key": key,
            "items": items,
            "n_sections": len(sections_set),
            "score": len(sections_set) * 7 + sum(it["char_len"] for it in items) // 100,
        })

    ranked.sort(key=lambda r: r["score"], reverse=True)

    # ----------------------------------------------------------
    # Headline numbers
    # ----------------------------------------------------------
    by_type = defaultdict(int)
    for c in ranked:
        by_type[c["type"]] += 1
    out.append("## Headline Numbers")
    out.append("")
    out.append(f"- **{by_type['callout_body']}** callout-body fingerprint duplications (same body text in 2+ sections).")
    out.append(f"- **{by_type['callout_title_nonstructural']}** non-structural callout-title duplications.")
    out.append(f"- **{by_type['code_caption_exact']}** code-caption exact fingerprint duplications.")
    out.append(f"- **{by_type['code_caption_long']}** code-caption long-fingerprint duplications.")
    out.append(f"- **{by_type['code_caption_fuzzy']}** code-caption fuzzy (>=5 shared tokens) duplications.")
    out.append(f"- **{by_type['prose']}** prose-paragraph duplications.")
    out.append("")

    # Estimate reduction
    def excess_in(type_name):
        total_excess_blocks = 0
        total_excess_chars = 0
        for c in ranked:
            if c["type"] != type_name:
                continue
            sections_set = {it["section"] for it in c["items"]}
            excess = len(c["items"]) - 1  # keep one canonical
            total_excess_blocks += excess
            avg_len = sum(len(it.get("preview", "") or it.get("caption", "") or "") for it in c["items"]) / max(1, len(c["items"]))
            total_excess_chars += int(excess * avg_len)
        return total_excess_blocks, total_excess_chars

    cb_blocks, cb_chars = excess_in("callout_body")
    ct_blocks, ct_chars = excess_in("callout_title_nonstructural")
    ce_blocks, ce_chars = excess_in("code_caption_exact")
    cl_blocks, cl_chars = excess_in("code_caption_long")
    cf_blocks, cf_chars = excess_in("code_caption_fuzzy")
    pr_blocks, pr_chars = excess_in("prose")

    total_excess_blocks = cb_blocks + ct_blocks + ce_blocks + cl_blocks + cf_blocks + pr_blocks
    total_excess_chars = cb_chars + ct_chars + ce_chars + cl_chars + cf_chars + pr_chars
    est_words = total_excess_chars // 5  # ~5 chars per word

    out.append("## Estimated Reduction if All Duplicates Reconciled")
    out.append("")
    out.append(f"- Callout-body duplicates: **{cb_blocks}** excess blocks (~{cb_chars // 5:,} words)")
    out.append(f"- Non-structural callout-title duplicates: **{ct_blocks}** excess blocks (~{ct_chars // 5:,} words)")
    out.append(f"- Code-caption (exact) duplicates: **{ce_blocks}** excess captions (~{ce_chars // 5:,} words)")
    out.append(f"- Code-caption (long fingerprint) duplicates: **{cl_blocks}** excess captions (~{cl_chars // 5:,} words)")
    out.append(f"- Code-caption (fuzzy) duplicates: **{cf_blocks}** excess captions (~{cf_chars // 5:,} words)")
    out.append(f"- Prose-paragraph duplicates: **{pr_blocks}** excess paragraphs (~{pr_chars // 5:,} words)")
    out.append(f"- **Grand total: ~{total_excess_blocks:,} duplicate blocks, ~{est_words:,} words.**")
    out.append("")
    out.append("Note: most code-caption duplicates are short generic AI-boilerplate (\"Install the required")
    out.append("packages for this lab\"). The word count is small per occurrence; the value of fixing them is")
    out.append("clarity and avoiding the appearance of copy-paste, not word reduction.")
    out.append("")

    # ----------------------------------------------------------
    # Top 20 clusters
    # ----------------------------------------------------------
    out.append("## Top 20 Duplication Clusters")
    out.append("")
    out.append("Each cluster lists: type, canonical home (proposed), and duplicate locations.")
    out.append("")
    out.append("**Suggested actions:**")
    out.append("- **DELETE** = remove duplicate copies, replace with `<div class=\"callout cross-ref\">` See-Also pointer to the canonical")
    out.append("- **REWRITE** = the duplicate is lame boilerplate; rewrite with section-specific content")
    out.append("- **RESTRUCTURE** = duplicates overlap but are not identical; decide canonical, consolidate the rest into cross-refs")
    out.append("- **KEEP** = brief restatement is intentional for self-containment (rarely chosen)")
    out.append("")

    for idx, cluster in enumerate(ranked[:20], 1):
        items = cluster["items"]
        sections_in = sorted({it["section"] for it in items})
        all_tokens = set()
        for it in items:
            text = " ".join(str(v).lower() for k, v in it.items()
                            if k in ("preview", "caption", "title") and v)
            all_tokens |= set(re.findall(r"[a-z0-9]+", text))
        canonical = canonical_home_for(sections_in, all_tokens)

        type_label = {
            "callout_body": "CALLOUT BODY (fingerprint match)",
            "callout_title_nonstructural": "CALLOUT TITLE (non-structural, same title in 2+ sections)",
            "code_caption_exact": "CODE CAPTION (exact fingerprint)",
            "code_caption_long": "CODE CAPTION (long fingerprint, 200-char match)",
            "code_caption_fuzzy": "CODE CAPTION (fuzzy >=5 shared tokens)",
            "prose": "PROSE PARAGRAPH",
        }[cluster["type"]]

        out.append(f"### {idx}. {type_label}  |  {cluster['n_sections']} sections, {len(items)} occurrences")
        key_display = (cluster["key"] or "")[:140]
        out.append(f"- **Signature**: `{key_display}`")
        out.append(f"- **Canonical home (proposed)**: `{canonical}`")
        out.append("- **Occurrences:**")
        items_sorted = sorted(items, key=lambda it: it["section"])
        # Cap to 15 occurrences to keep report readable
        shown = items_sorted[:15]
        for it in shown:
            marker = "  *(canonical)*" if it["section"] == canonical else ""
            label_bits = []
            if "label" in it and it["label"]:
                label_bits.append(it["label"])
            if "title" in it and it["title"]:
                label_bits.append(f"\"{it['title']}\"")
            preview = it.get("preview") or it.get("caption") or ""
            line_str = f":{it['line']}" if it.get("line") else ""
            label_str = f" [{' | '.join(label_bits)}]" if label_bits else ""
            out.append(f"  - `{it['section']}{line_str}`{label_str}{marker}")
            if preview:
                preview_clean = preview.replace("|", "\\|").replace("\n", " ")[:200]
                out.append(f"    > {preview_clean}")
        if len(items_sorted) > len(shown):
            out.append(f"  - *(and {len(items_sorted) - len(shown)} more occurrences omitted)*")
        action = _suggest_action(cluster, sections_in)
        out.append(f"- **Suggested action**: {action}")
        out.append("")

    # ----------------------------------------------------------
    # Sample sketches
    # ----------------------------------------------------------
    out.append("## Sample Before/After Sketches (5)")
    out.append("")
    sketches_written = 0
    for cluster in ranked:
        if sketches_written >= 5:
            break
        items_sorted = sorted(cluster["items"], key=lambda it: it["section"])
        sections_in = sorted({it["section"] for it in items_sorted})
        if len(sections_in) < 2:
            continue
        all_tokens = set()
        for it in items_sorted:
            text = " ".join(str(v).lower() for k, v in it.items()
                            if k in ("preview", "caption", "title") and v)
            all_tokens |= set(re.findall(r"[a-z0-9]+", text))
        canonical = canonical_home_for(sections_in, all_tokens)
        non_canonical = [it for it in items_sorted if it["section"] != canonical]
        if not non_canonical:
            continue
        sketches_written += 1
        target = non_canonical[0]
        preview = target.get("preview") or target.get("caption") or ""
        out.append(f"### Sketch {sketches_written}: `{target['section']}` (cluster type: {cluster['type']})")
        out.append("")
        out.append(f"**Cluster signature**: `{(cluster['key'] or '')[:120]}`")
        out.append("")
        out.append("**Before** (duplicate content):")
        out.append("```html")
        if cluster["type"].startswith("callout"):
            ti = target.get("title") or "Big Picture"
            out.append(f'<div class="callout big-picture">')
            out.append(f'  <div class="callout-title">{ti}</div>')
            out.append(f"  <p>{preview[:240]}</p>")
            out.append(f"</div>")
        elif cluster["type"].startswith("code_caption"):
            cap = target.get("caption") or preview
            lbl = target.get("label", "Code Fragment X.Y.Z")
            out.append(f'<div class="code-caption"><strong>{lbl}</strong>: {cap[:200]}</div>')
        else:
            out.append(f"<p>{preview[:300]}</p>")
        out.append("```")
        out.append("")
        canonical_rel = _relpath(target["section"], canonical)
        out.append(f"**After** (replace with cross-ref to canonical `{canonical}`):")
        out.append("```html")
        if cluster["type"].startswith("code_caption_exact") or cluster["type"] == "code_caption_long":
            # Lame caption case: just rewrite with section-specific content
            out.append(f'<div class="code-caption"><strong>{target.get("label","Code Fragment X.Y.Z")}</strong>: ')
            out.append('  (rewrite this caption with section-specific content explaining what THIS code does.</div>')
        else:
            out.append(f'<div class="callout cross-ref">')
            out.append(f'  <div class="callout-title">See Also</div>')
            out.append(f"  <p>This concept is treated in depth in ")
            out.append(f'    <a href="{canonical_rel}">{canonical.split("/")[-1].replace(".html","")}</a>.')
            out.append(f"    The treatment there covers the full depth; the brief mention previously")
            out.append(f"    here has been removed to avoid drift.</p>")
            out.append(f"</div>")
        out.append("```")
        out.append("")

    # ----------------------------------------------------------
    # Top-5 single-line summary
    # ----------------------------------------------------------
    out.append("## Top-5 Most-Egregious Clusters (one-liners)")
    out.append("")
    for idx, cluster in enumerate(ranked[:5], 1):
        sections_set = {it["section"] for it in cluster["items"]}
        sig = (cluster["key"] or "")[:60]
        out.append(f"{idx}. **{cluster['type']}**: \"{sig}...\" -- across **{len(sections_set)}** sections, **{len(cluster['items'])}** occurrences.")
    out.append("")

    return "\n".join(out)


def _is_generic_prose_opener(text: str) -> bool:
    """Filter out prose openers that look generic (and would create false positives).
    E.g., 'In this section we' or 'This chapter covers...'."""
    if not text:
        return True
    t = text.lower().strip()
    generic_starts = (
        "in this section",
        "in this chapter",
        "this chapter covers",
        "this section covers",
        "the rest of this",
    )
    return any(t.startswith(s) for s in generic_starts)


def _suggest_action(cluster, sections_in):
    n = len(sections_in)
    ctype = cluster["type"]
    if ctype == "callout_body":
        if n >= 3:
            return "**DELETE** duplicate callouts in non-canonical sections; replace with `<div class=\"callout cross-ref\">` See-Also. Body fingerprints are identical -- this is copy-paste prone to drift."
        return "**DELETE** the duplicate callout; promote one location to canonical and cross-ref from the other."
    if ctype == "callout_title_nonstructural":
        return "**RESTRUCTURE**: same non-structural title used in multiple sections. If bodies overlap, consolidate to canonical with cross-refs; if bodies differ, rename titles to disambiguate."
    if ctype == "code_caption_exact":
        return "**REWRITE**: short generic caption (\"Code example\", \"Install the required packages for this lab\") repeated verbatim. Replace each with a section-specific one-line description of what the code actually does."
    if ctype == "code_caption_long":
        return "**REWRITE or DELETE**: long caption duplicated near-verbatim across sections. Either rewrite each to describe the section's specific code, or consolidate the actual code to a canonical home."
    if ctype == "code_caption_fuzzy":
        return "**RESTRUCTURE**: similar Code Fragments cover overlapping ground. Decide whether each is doing distinct didactic work; if not, consolidate to canonical and replace others with a 1-line See-Also pointer."
    if ctype == "prose":
        if n >= 3:
            return "**DELETE** duplicate paragraphs in non-canonical sections; this is verbatim copy-paste."
        return "**DELETE** the redundant paragraph; replace with a 1-line summary plus a link to canonical."
    return "**REVIEW**"


def _relpath(from_section_path: str, to_section_path: str) -> str:
    from_parts = from_section_path.split("/")[:-1]
    to_parts = to_section_path.split("/")
    i = 0
    while i < len(from_parts) and i < len(to_parts) - 1 and from_parts[i] == to_parts[i]:
        i += 1
    up = [".."] * (len(from_parts) - i)
    down = to_parts[i:]
    return "/".join(up + down)


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main():
    files = collect_section_files()
    print(f"Scanning {len(files)} main-track sections...", file=sys.stderr)

    sections = []
    for fp in files:
        try:
            sections.append(extract_section_data(fp))
        except Exception as e:
            print(f"WARN: failed {fp.relative_to(ROOT)}: {e}", file=sys.stderr)

    clusters = cluster_duplicates(sections)
    fuzzy_caption_clusters = code_caption_fuzzy_cluster(sections)

    report = render_report(sections, clusters, fuzzy_caption_clusters)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(report, encoding="utf-8")
    print(f"Wrote: {OUT_PATH.relative_to(ROOT)}", file=sys.stderr)

    json_dump = {
        "n_sections": len(sections),
        "stats": {
            "callouts": sum(len(s["callouts"]) for s in sections),
            "code_captions": sum(len(s["code_captions"]) for s in sections),
            "prose": sum(len(s["prose"]) for s in sections),
        },
        "clusters_summary": {
            "callout_body_clusters": len(clusters["callout_body"]),
            "callout_title_nonstructural_clusters": len(clusters["callout_title_non_structural"]),
            "code_caption_exact_clusters": len(clusters["code_caption_exact"]),
            "code_caption_long_clusters": len(clusters["code_caption_long_match"]),
            "code_caption_fuzzy_clusters": len(fuzzy_caption_clusters),
            "prose_short_fp_clusters": len(clusters["prose_short_fp"]),
            "prose_long_fp_clusters": len(clusters["prose_long_fp"]),
        },
    }
    JSON_DUMP_PATH.write_text(json.dumps(json_dump, indent=2), encoding="utf-8")
    print(f"Wrote: {JSON_DUMP_PATH.relative_to(ROOT)}", file=sys.stderr)


if __name__ == "__main__":
    main()
