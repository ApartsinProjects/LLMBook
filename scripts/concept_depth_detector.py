"""Concept-explanation depth detector.

Theory
------
A textbook should treat each technical concept ONCE with depth, and
elsewhere refer back. Depth signals:
  - Math block (KaTeX / <div class="math-block"> nearby)
  - Code block (concrete implementation)
  - Algorithm callout (<div class="callout algorithm">)
  - Numeric example (<div class="callout numeric-example">)
  - Diagram (<svg> or <figure class="illustration"> or
    <div class="diagram-container">)
  - Step-by-step list (<ol> with >=4 items in the body of the
    concept's introducing paragraph)
  - Worked example (<div class="callout practical-example">)
  - A concept-link or hyperlink to a deeper section (the section
    OUTSOURCES the depth)

For each `<strong>EntityName</strong>` that LOOKS LIKE a concept
introduction (entity in the curated dictionary + bold + within a
paragraph), count the depth signals in a window of 800 chars after the
bold. Score:
  - 0 signals = SHALLOW, no link out, no depth here
  - has-link-out = OK (defers to canonical home)
  - >= 2 signals = DEEP TREATMENT
  - 1 signal = MEDIUM

Report:
  - SHALLOW + NO-LINK: highest priority for enrichment (or for adding
    a cross-link to the canonical deep home)
  - SHALLOW + WITH-LINK: fine (defers properly)
  - DEEP: candidates for being the canonical home

Cross-referenced with the dedup_detector's hot-entity hub list, this
identifies the gap: concepts that are mentioned book-wide but get
shallow treatment everywhere they appear.

Usage
-----
    /c/Python314/python scripts/concept_depth_detector.py
"""
from __future__ import annotations

import argparse
import html as html_mod
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "node_modules", "KDP", "build", "source_fix_backups",
             "pagefind", ".book-update", "vendor", ".claude", "_archive",
             "agents", "templates", "docs", "scripts"}

# Reuse entity list from dedup_detector
CONCEPT_ENTITIES = [
    # Methods + algorithms (concepts that should have depth)
    "LoRA", "QLoRA", "DoRA", "AdaLoRA",
    "RLHF", "DPO", "IPO", "KTO", "ORPO", "GRPO", "PPO", "REINFORCE",
    "RLAIF", "Constitutional AI",
    "YaRN", "NTK-aware", "RoPE", "ALiBi", "position interpolation",
    "FlashAttention", "PagedAttention", "speculative decoding",
    "Medusa", "EAGLE",
    "Mixture-of-Experts", "MoE",
    "Chain-of-Thought", "CoT", "Tree-of-Thoughts",
    "Self-Consistency", "Self-Refine", "Reflexion",
    "ReAct", "RAG", "Self-RAG", "GraphRAG", "HyDE", "RAGAS",
    "BM25", "TF-IDF", "Reciprocal Rank Fusion",
    "knowledge distillation", "pruning", "quantization",
    "GPTQ", "AWQ", "GGUF",
    "BLEU", "ROUGE", "BERTScore", "METEOR",
    "perplexity", "bits-per-byte",
    "Needle-in-a-Haystack", "RULER",
    "byte-pair encoding", "BPE", "WordPiece",
    "self-attention", "multi-head attention", "cross-attention",
    "KV cache",
    "context window", "context length",
    "covariate shift", "distribution shift", "drift",
    "position bias", "verbosity bias",
    "Goodhart's Law",
    "differential privacy", "federated learning",
    "diffusion", "score matching",
]

STRONG_RE = re.compile(r'<strong[^>]*>([^<]{2,80})</strong>', re.IGNORECASE)
MATH_BLOCK_RE = re.compile(
    r'<div\s+class="math-block"|class="math"', re.IGNORECASE,
)
CODE_BLOCK_RE = re.compile(
    r'<div\s+class="code-block-wrapper"', re.IGNORECASE,
)
ALGORITHM_RE = re.compile(
    r'<div\s+class="callout algorithm"', re.IGNORECASE,
)
NUMERIC_EX_RE = re.compile(
    r'<div\s+class="callout numeric-example"', re.IGNORECASE,
)
DIAGRAM_RE = re.compile(
    r'<svg\b|<figure\s+class="illustration"|<div\s+class="diagram-container"',
    re.IGNORECASE,
)
PRACTICAL_EX_RE = re.compile(
    r'<div\s+class="callout practical-example"', re.IGNORECASE,
)
ORDERED_STEP_RE = re.compile(
    r'<ol\b[^>]*>(?:.*?<li\b[^>]*>.*?</li>){4,}', re.DOTALL | re.IGNORECASE,
)
LINK_OUT_RE = re.compile(
    r'<a\s+[^>]*(?:concept-link|cross-ref|class="prereq-link")[^>]*href="([^"]+)"',
    re.IGNORECASE,
)


def visible(s: str) -> str:
    return re.sub(r'\s+', ' ', html_mod.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()


def section_id(p: Path) -> str:
    m = re.match(r'section-([\d.]+\w*)\.html', p.name)
    return f"S{m.group(1)}" if m else p.name


# Build entity matcher
ENTITY_RE = re.compile(
    r'(?<![\w-])(?:' + '|'.join(re.escape(e) for e in CONCEPT_ENTITIES) + r')(?![\w-])',
    re.IGNORECASE,
)


def analyze_intro(html: str, intro_pos: int, window: int = 800) -> dict:
    """Look at the window of HTML after a strong-bolded entity intro and
    count depth signals."""
    snippet = html[intro_pos:intro_pos + window]
    return {
        "math": bool(MATH_BLOCK_RE.search(snippet)),
        "code": bool(CODE_BLOCK_RE.search(snippet)),
        "algorithm": bool(ALGORITHM_RE.search(snippet)),
        "numeric_example": bool(NUMERIC_EX_RE.search(snippet)),
        "diagram": bool(DIAGRAM_RE.search(snippet)),
        "practical_example": bool(PRACTICAL_EX_RE.search(snippet)),
        "step_list": bool(ORDERED_STEP_RE.search(snippet)),
        "link_out": bool(LINK_OUT_RE.search(snippet)),
    }


def scan() -> list[dict]:
    rows: list[dict] = []
    for p in sorted(ROOT.rglob("section-*.html")):
        if set(p.parts) & SKIP_DIRS:
            continue
        try:
            html = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        sid = section_id(p)
        for m in STRONG_RE.finditer(html):
            inner = m.group(1).strip()
            # Skip role-words common in callout patterns
            low = inner.lower().rstrip(':').strip()
            if low in {"who", "what", "when", "where", "why", "how",
                       "situation", "problem", "dilemma", "decision",
                       "result", "lesson", "watch for", "fix",
                       "production pattern", "key insight",
                       "real-world scenario", "note", "warning", "tip",
                       "important", "caution"}:
                continue
            # Does the bolded text contain a concept entity?
            ents = list(ENTITY_RE.finditer(inner))
            if not ents:
                continue
            entity = ents[0].group(0)
            # Skip if the bold-block is INSIDE a list item (table cell,
            # bullet label, etc.) — too noisy
            preamble = html[max(0, m.start() - 100):m.start()]
            if re.search(r'<li\b[^>]*>\s*$', preamble):
                continue
            sig = analyze_intro(html, m.end())
            depth_score = sum(1 for v in sig.values() if v and not v == sig["link_out"])
            depth_score = sum(1 for k, v in sig.items() if v and k != "link_out")
            rows.append({
                "section": sid,
                "path": str(p.relative_to(ROOT)).replace('\\', '/'),
                "entity": entity,
                "phrase": inner[:60],
                "depth_score": depth_score,
                "has_link_out": sig["link_out"],
                **sig,
            })
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    rows = scan()

    # Aggregate by entity
    entity_intros: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        entity_intros[r["entity"].lower()].append(r)

    # For each entity, count: total intros, deep intros, shallow w/ link, shallow w/o link
    summary = []
    for ent, lst in entity_intros.items():
        deep = sum(1 for r in lst if r["depth_score"] >= 2)
        shallow_linked = sum(1 for r in lst if r["depth_score"] < 2 and r["has_link_out"])
        shallow_orphan = sum(1 for r in lst if r["depth_score"] < 2 and not r["has_link_out"])
        summary.append({
            "entity": ent,
            "total": len(lst),
            "deep": deep,
            "shallow_linked": shallow_linked,
            "shallow_orphan": shallow_orphan,
        })

    summary.sort(key=lambda s: -s["shallow_orphan"])

    # Render
    lines = []
    lines.append("# Concept-Explanation Depth Report")
    lines.append("")
    lines.append("For each bolded technical concept (in the curated entity dictionary),")
    lines.append("score the depth signals in the 800-char window AFTER the bold:")
    lines.append("  - math block, code block, algorithm callout, numeric example,")
    lines.append("    diagram, practical example, step-by-step list.")
    lines.append("  - has-link-out = the intro defers to a canonical deep treatment elsewhere.")
    lines.append("")
    lines.append("Depth categories:")
    lines.append("  - DEEP (>=2 signals): this is a deep treatment, candidate canonical home")
    lines.append("  - SHALLOW + LINKED: defers properly to canonical home")
    lines.append("  - SHALLOW + ORPHAN: superficial mention with no link out, no depth — gap")
    lines.append("")
    lines.append("## Entity summary (top 30 by orphan-shallow count)")
    lines.append("")
    lines.append("| Entity | Total | Deep | Shallow+Linked | Shallow+Orphan |")
    lines.append("|---|---:|---:|---:|---:|")
    for s in summary[:30]:
        lines.append(
            f"| {s['entity']} | {s['total']} | {s['deep']} | "
            f"{s['shallow_linked']} | {s['shallow_orphan']} |"
        )
    lines.append("")
    lines.append("## Sections with shallow orphan introductions (top 50)")
    lines.append("")
    orphans = [r for r in rows if r["depth_score"] < 2 and not r["has_link_out"]]
    orphans.sort(key=lambda r: (r["section"], r["entity"]))
    lines.append("| Section | Entity | Phrase | depth | link |")
    lines.append("|---|---|---|---:|---:|")
    for r in orphans[:50]:
        lines.append(
            f"| {r['section']} | {r['entity']} | {r['phrase'][:50]} | "
            f"{r['depth_score']} | {'y' if r['has_link_out'] else 'n'} |"
        )
    if len(orphans) > 50:
        lines.append(f"\n... and {len(orphans) - 50} more orphans.")
    lines.append("")

    md = "\n".join(lines)
    out_path = Path(args.out) if args.out else ROOT / "docs" / "content-audit" / "CONCEPT_DEPTH_REPORT.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"Report: {out_path.relative_to(ROOT)}")
    print(f"\nTotal concept intros: {len(rows)}")
    print(f"  Deep (>=2 signals): {sum(1 for r in rows if r['depth_score'] >= 2)}")
    print(f"  Shallow + linked:   {sum(1 for r in rows if r['depth_score'] < 2 and r['has_link_out'])}")
    print(f"  Shallow + orphan:   {sum(1 for r in rows if r['depth_score'] < 2 and not r['has_link_out'])}")
    print(f"\nTop 5 entities by orphan count:")
    for s in summary[:5]:
        print(f"  {s['shallow_orphan']:>3} orphans / {s['total']:>3} intros : {s['entity']}")


if __name__ == "__main__":
    main()
