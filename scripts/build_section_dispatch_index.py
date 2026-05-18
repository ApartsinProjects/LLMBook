"""Build a per-section dispatch summary index for targeted agent dispatch.

Extends the existing book_content_index.jsonl with depth/quality signals
that drive "which agent should run on which section" decisions WITHOUT
re-reading the section.

Output: docs/content-audit/SECTION_DISPATCH_INDEX.jsonl

For each section (and chapter-index where useful), record:
  - core metadata: path, part/chapter/section, title, word_count
  - depth signals:
      math_blocks: count of <span class="math"> or $$
      algorithm_callouts: count of <div class="callout algorithm">
      citation_links: count of arxiv/doi anchors
      pseudocode_blocks: count of <pre><code class="lang-text">
  - image signals:
      figure_count, comic_count (fun-note callouts), opener_present
  - structure signals:
      has_prereqs, has_big_picture, has_whats_next, has_takeaway,
      has_self_check, has_lab, has_bibliography
  - "what's missing" labels (for agent triage):
      needs_algorithm_callout (no algorithm callouts in section)
      needs_figure (no figure/diagram present)
      needs_comic (no fun-note callout)
      needs_bibliography (no bibliography)
      needs_prereqs (no prerequisites)
      needs_lab (no lab callout)
      needs_self_check (no self-check)
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", "node_modules", "KDP", "build", "source_fix_backups",
        "pagefind", ".book-update", "vendor", ".claude", "_archive",
        "agents", "templates"}

OUTFILE = ROOT / "docs" / "content-audit" / "SECTION_DISPATCH_INDEX.jsonl"

CALLOUT_RE = re.compile(r'<div\s+class="callout\s+([a-z-]+)"', re.IGNORECASE)
MATH_RE = re.compile(r'<(?:span|div)\s+class="math\b|\$\$', re.IGNORECASE)
ARXIV_RE = re.compile(r'arxiv\.org/abs/|doi\.org/', re.IGNORECASE)
PSEUDOCODE_RE = re.compile(r'<code\s+class="(?:[^"]*\s)?lang-text"', re.IGNORECASE)
FIGCAPTION_RE = re.compile(r'<figcaption\b', re.IGNORECASE)
DIAGRAM_CAPTION_RE = re.compile(r'<div\s+class="diagram-caption"', re.IGNORECASE)
PREREQS_RE = re.compile(r'<div\s+class="prerequisites"|<h3[^>]*id="prerequisites"', re.IGNORECASE)
CHAPTER_OPENER_RE = re.compile(r'class="illustration[^"]*opener"', re.IGNORECASE)
BIB_RE = re.compile(r'<details\s+class="bibliography-collapsible|<section\s+class="bibliography"', re.IGNORECASE)
WORD_RE = re.compile(r'\w+')


def extract_signals(p: Path) -> dict:
    try:
        html = p.read_text(encoding="utf-8")
    except Exception:
        return {}

    callouts = [m.group(1).lower() for m in CALLOUT_RE.finditer(html)]
    n_math = len(MATH_RE.findall(html))
    n_arxiv = len(ARXIV_RE.findall(html))
    n_pseudo = len(PSEUDOCODE_RE.findall(html))
    n_figcap = len(FIGCAPTION_RE.findall(html))
    n_diagcap = len(DIAGRAM_CAPTION_RE.findall(html))

    # Word count: strip tags
    text = re.sub(r'<[^>]+>', ' ', html)
    n_words = len(WORD_RE.findall(text))

    co_count = {}
    for c in callouts:
        co_count[c] = co_count.get(c, 0) + 1

    return {
        "word_count": n_words,
        "math_blocks": n_math,
        "algorithm_callouts": co_count.get("algorithm", 0),
        "citation_links": n_arxiv,
        "pseudocode_blocks": n_pseudo,
        "figure_count": n_figcap + n_diagcap,
        "comic_count": co_count.get("fun-note", 0),
        "opener_present": bool(CHAPTER_OPENER_RE.search(html)),
        "callout_counts": co_count,
        "has_prereqs": bool(PREREQS_RE.search(html)),
        "has_big_picture": co_count.get("big-picture", 0) > 0,
        "has_whats_next": co_count.get("whats-next", 0) > 0 or '<div class="whats-next"' in html,
        "has_takeaway": co_count.get("key-takeaway", 0) > 0,
        "has_self_check": co_count.get("self-check", 0) > 0,
        "has_lab": co_count.get("lab", 0) > 0,
        "has_bibliography": bool(BIB_RE.search(html)),
    }


def compute_gaps(signals: dict, is_tools_chapter: bool) -> list:
    """Return list of 'needs_X' labels."""
    gaps = []
    if signals.get("algorithm_callouts", 0) == 0 and not is_tools_chapter:
        gaps.append("needs_algorithm_callout")
    if signals.get("figure_count", 0) == 0:
        gaps.append("needs_figure")
    if signals.get("comic_count", 0) == 0 and not is_tools_chapter:
        gaps.append("needs_comic")
    if not signals.get("has_bibliography"):
        gaps.append("needs_bibliography")
    if not signals.get("has_prereqs"):
        gaps.append("needs_prereqs")
    if not signals.get("has_lab") and not is_tools_chapter:
        gaps.append("needs_lab")
    if not signals.get("has_self_check"):
        gaps.append("needs_self_check")
    if not signals.get("has_big_picture"):
        gaps.append("needs_big_picture")
    if not signals.get("has_whats_next"):
        gaps.append("needs_whats_next")
    if signals.get("citation_links", 0) < 3:
        gaps.append("needs_more_citations")
    return gaps


def main():
    OUTFILE.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with OUTFILE.open("w", encoding="utf-8") as out:
        for p in sorted(ROOT.rglob("*.html")):
            if set(p.parts) & SKIP:
                continue
            if not (p.name.startswith("section-") or p.name == "index.html"):
                continue
            rel = p.relative_to(ROOT).as_posix()
            # Identify tools-of-trade chapters (no algorithm/lab expected)
            is_tools = any(
                pat in rel.lower()
                for pat in ("tools-of-the-trade", "scale-tools",
                            "conv-ai-tools", "retrieval-tools",
                            "responsible-ai-tools")
            )
            sig = extract_signals(p)
            if not sig:
                continue
            gaps = compute_gaps(sig, is_tools)
            record = {
                "path": rel,
                "is_tools_chapter": is_tools,
                **sig,
                "gaps": gaps,
                "gap_count": len(gaps),
            }
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
            n += 1
    print(f"Wrote {n} records to {OUTFILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
