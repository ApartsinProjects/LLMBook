"""Audit + simplify helper for diagram round 3.

Scores every box-style SVG diagram in the book by:
- file size
- line count
- rect count
- text count
- long-text count (text > 30 chars)
- canvas size (viewBox area)
- group count
Score >= 4 flags as overly complex. SVGs intentionally containing grids
(positional-encoding heatmap, attention-head matrices, 2:4 sparsity, attention
variants) are excluded by filename pattern.

Round-3 selects the next 20 worst-offenders not touched by rounds 1+2
(commits 6da1b83e and 12878e0f).

Usage:
    python scripts/_simplify_diagrams_round3.py audit
    python scripts/_simplify_diagrams_round3.py list-candidates [N]
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {
    "node_modules", ".git", "KDP", "build", "temp_ebook", "temp_epub",
    "source_fix_backups", "pagefind", "templates", ".claude", ".book-update",
    "vendor", "scripts", "docs", "styles",
}

# Names from round 1 commit 6da1b83e (the 11 simplified)
ROUND_1 = {
    "fig-30.9.1-eu-ai-act-risk-tiers.svg",
    "diagram-32-6-1.svg",
    "diagram-32-7-1.svg",
    "diagram-32-4-1.svg",
    "fig-8.1.3-four-reasoning.svg",
    "fig-5.4.3-ar-vs-diffusion.svg",
    "fig-2.3.4-tokenizer-landscape.svg",
    # NOTE: fig-6.6.4-pipeline.svg listed in round 1 but rebuilt again in round 2 audit text
    "fig-6.6.4-pipeline.svg",
    "fig-2.1.5-token-artifacts.svg",
    "fig-28.13.1-experiment-flow.svg",
    "fig-2.2.4-unigram.svg",
}

# Names from round 2 commit 12878e0f (the 20 simplified)
ROUND_2 = {
    "fig-9.2.2-pagedattention.svg",
    "diagram-frontier-edge-device-matrix.svg",
    "diagram-frontier-fa4-memory-hierarchy.svg",
    "fig-29.6.2-framework-comparison.svg",
    "diagram-32-5-1.svg",
    "diagram-framework-selection.svg",
    "diagram-32-3-1.svg",
    "diagram-frontier-codesign-stacks.svg",
    "fig-12.6.1-dspy-optimization-loop.svg",
    "fig-4.3.5-head-behaviors.svg",
    "fig-5.4.2-diffusion.svg",
    "fig-2.2.5-byte-bpe.svg",
    "diagram-32-1-1.svg",
    "fig-20.3-graphrag-pipeline.svg",
    "fig-13.8.1-log-to-dataset-pipeline.svg",
    "fig-6.8.1-production-llm-training.svg",
    "fig-2.3.2-chat-template.svg",
    "diagram-32-8-1.svg",
    "fig-29.6.1-durable-execution-recovery.svg",
    "diagram-transformer-anatomy.svg",
}

# Skip patterns: intentional grids and intentional charts
GRID_SKIP_SUBSTRINGS = (
    "pos-encoding",
    "positional-encoding",
    "sparsity",
    "attention-head",
    "attention-variant",
    "attention-matrix",
    "heatmap",
    # quantization granularity is a per-tensor/per-channel/per-group grid;
    # the grid pattern IS the visual message.
    "quantization-granularity",
    # hand-drawn chart (line plot + log plot) - chart, not box diagram.
    "param-growth",
    # feature-evolution matrix (BERT lineage); dot-grid IS the visual.
    "encoder-timeline",
)

ALREADY_DONE = ROUND_1 | ROUND_2


def is_grid_skip(name: str) -> bool:
    n = name.lower()
    return any(sub in n for sub in GRID_SKIP_SUBSTRINGS)


def find_svgs() -> list[Path]:
    out: list[Path] = []
    for p in ROOT.rglob("*.svg"):
        rel = p.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        # Skip vector PNG previews/concept-figs scratch
        if "_concept-figs" in rel.parts:
            continue
        out.append(p)
    return out


def score_svg(p: Path) -> dict:
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return {"path": p, "score": 0, "size": 0, "lines": 0, "rects": 0,
                "texts": 0, "long_texts": 0, "vbox": (0, 0), "groups": 0}
    size = len(text)
    lines = text.count("\n") + 1
    rects = len(re.findall(r"<rect\b", text, re.I))
    text_nodes = re.findall(r"<text\b[^>]*>(.*?)</text>", text, re.I | re.S)
    texts = len(text_nodes)
    long_texts = sum(1 for t in text_nodes if len(re.sub(r"\s+", " ", t).strip()) > 30)
    groups = len(re.findall(r"<g\b", text, re.I))
    vbox_w = vbox_h = 0
    m = re.search(r"viewBox\s*=\s*['\"]([^'\"]+)['\"]", text, re.I)
    if m:
        parts = m.group(1).split()
        if len(parts) >= 4:
            try:
                vbox_w = float(parts[2]); vbox_h = float(parts[3])
            except ValueError:
                pass
    area = vbox_w * vbox_h

    score = 0
    if size > 6000: score += 1
    if size > 10000: score += 1
    if lines > 100: score += 1
    if rects > 12: score += 1
    if texts > 18: score += 1
    if long_texts > 6: score += 1
    if area > 700_000: score += 1
    if groups > 12: score += 1
    return {
        "path": p, "score": score, "size": size, "lines": lines,
        "rects": rects, "texts": texts, "long_texts": long_texts,
        "vbox": (vbox_w, vbox_h), "groups": groups,
    }


def audit() -> list[dict]:
    rows = []
    for p in find_svgs():
        r = score_svg(p)
        if r["score"] >= 4 and not is_grid_skip(p.name):
            rows.append(r)
    rows.sort(key=lambda r: (-r["score"], -r["size"]))
    return rows


def candidates(n: int = 20) -> list[dict]:
    out = []
    for r in audit():
        if r["path"].name in ALREADY_DONE:
            continue
        out.append(r)
        if len(out) >= n:
            break
    return out


def main(argv: list[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else "audit"
    if cmd == "audit":
        rows = audit()
        print(f"box-diagram over-complex (score >= 4): {len(rows)}")
        for r in rows[:30]:
            rel = r["path"].relative_to(ROOT).as_posix()
            print(f"  {r['score']}  size={r['size']:>6}  lines={r['lines']:>4}  rects={r['rects']:>3}  texts={r['texts']:>3}  long={r['long_texts']:>3}  vbox={r['vbox'][0]:>5}x{r['vbox'][1]:>4}  {rel}")
    elif cmd == "list-candidates":
        n = int(argv[2]) if len(argv) > 2 else 20
        rows = candidates(n)
        print(f"round-3 candidates (next {n} not yet simplified):")
        for r in rows:
            rel = r["path"].relative_to(ROOT).as_posix()
            print(f"  {r['score']}  {rel}")
    else:
        print(f"unknown command {cmd!r}")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
