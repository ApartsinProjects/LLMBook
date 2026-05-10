"""
Synthesize KDP/validation/diagram_audit.md from the raw audit_full.json.

Filters the comprehensive audit output for diagram/figure-related checks
and groups them by severity and module. Designed to be re-run as the
audit data is refreshed.
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
AUDIT_JSON = ROOT / "KDP" / "validation" / "_raw" / "audit_full.json"
OUT = ROOT / "KDP" / "validation" / "diagram_audit.md"

# Diagram/figure-related check_ids and what they mean
DIAGRAM_CHECKS = {
    "SVG_OVERLAP":         ("HIGH",   "SVG text or shapes overlap (likely illegible)"),
    "SVG_TEXT_OVERFLOW":   ("HIGH",   "SVG text extends past its container"),
    "SVG_TEXT_CLIPPING":   ("HIGH",   "SVG text is clipped by viewport/clip-path"),
    "SVG_ARIA_TRUNCATED":  ("MEDIUM", "SVG <title>/<desc> appears truncated"),
    "SVG_TITLE_TEXT":      ("MEDIUM", "SVG missing or weak <title> for accessibility"),
    "SVG_PANEL_ASYM":      ("MEDIUM", "SVG multi-panel layout asymmetric / unbalanced"),
    "GENERIC_SVG_LABEL":   ("MEDIUM", "SVG has generic/unhelpful label like 'Figure 1' instead of descriptive title"),
    "FIGURE_SEQUENCE":     ("MEDIUM", "Figure numbering out of sequence within chapter"),
    "DUP_FIGURE_NUM":      ("HIGH",   "Two figures share the same number"),
    "BROKEN_FIGURE_REF":   ("HIGH",   "Cross-reference points to a figure that doesn't exist"),
    "CAPTION_MISALIGN":    ("MEDIUM", "Caption number doesn't match the figure it sits below"),
    "MIXED_CAPTION_STYLE": ("LOW",    "Caption formatting inconsistent across the chapter"),
    "MISSING_IMG_DIMS":    ("LOW",    "<img> tag lacks width/height (causes layout shift)"),
}


def part_of(file: str) -> str:
    """Bucket a file path by part for grouping."""
    f = file.replace("\\", "/")
    if f.startswith("part-"):
        return f.split("/")[0]
    if f.startswith("appendices/"):
        return "appendices"
    if f.startswith("front-matter/"):
        return "front-matter"
    if f.startswith("capstone/"):
        return "capstone"
    return "root"


def module_of(file: str) -> str:
    f = file.replace("\\", "/")
    parts = f.split("/")
    if len(parts) >= 2 and (parts[1].startswith("module-") or parts[1].startswith("appendix-")):
        return f"{parts[0]}/{parts[1]}"
    return parts[0]


def main() -> None:
    data = json.loads(AUDIT_JSON.read_text(encoding="utf-8"))
    issues = data["issues"]
    n_files = data["file_count"]

    diagram_issues = [i for i in issues if i.get("check_id") in DIAGRAM_CHECKS]
    print(f"Total issues in audit: {len(issues)}")
    print(f"Diagram-related issues: {len(diagram_issues)}")

    by_check = defaultdict(list)
    for i in diagram_issues:
        by_check[i["check_id"]].append(i)

    by_severity = defaultdict(list)
    for cid, items in by_check.items():
        sev = DIAGRAM_CHECKS[cid][0]
        by_severity[sev].extend(items)

    by_module = Counter()
    for i in diagram_issues:
        by_module[module_of(i["file"])] += 1

    # ----- Build the markdown -----
    md: list[str] = []
    md.append("# Diagram Audit Report")
    md.append("")
    md.append(f"_Generated from `KDP/validation/_raw/audit_full.json` ({len(issues):,} total issues across {n_files} files)._")
    md.append("")
    md.append("## Summary")
    md.append("")
    md.append(f"- **{len(diagram_issues):,}** diagram/figure-related issues across **{len(by_module)}** modules")
    md.append(f"- **{len(by_severity['HIGH']):,}** HIGH (likely break the diagram or mislead the reader)")
    md.append(f"- **{len(by_severity['MEDIUM']):,}** MEDIUM (degrade pedagogy / accessibility)")
    md.append(f"- **{len(by_severity['LOW']):,}** LOW (cosmetic / consistency)")
    md.append("")
    md.append("## Issue counts by check")
    md.append("")
    md.append("| Severity | Check | Count | What it means |")
    md.append("|----------|-------|-------|---------------|")
    rows = sorted(
        [(DIAGRAM_CHECKS[cid][0], cid, len(items), DIAGRAM_CHECKS[cid][1])
         for cid, items in by_check.items()],
        key=lambda r: (-{"HIGH": 3, "MEDIUM": 2, "LOW": 1}[r[0]], -r[2]),
    )
    for sev, cid, count, meaning in rows:
        md.append(f"| **{sev}** | `{cid}` | {count} | {meaning} |")
    md.append("")

    md.append("## Modules with the most diagram issues")
    md.append("")
    md.append("| Module | Diagram issues |")
    md.append("|--------|----------------|")
    for mod, cnt in by_module.most_common(15):
        md.append(f"| `{mod}` | {cnt} |")
    md.append("")

    md.append("## HIGH-severity issues (fix before KDP submission)")
    md.append("")
    md.append("These issues either break the diagram visually, mislead the reader, or break navigation. Address each before publishing.")
    md.append("")
    for cid in sorted(by_check, key=lambda c: (-{"HIGH": 3, "MEDIUM": 2, "LOW": 1}[DIAGRAM_CHECKS[c][0]], c)):
        sev, meaning = DIAGRAM_CHECKS[cid]
        if sev != "HIGH":
            continue
        items = by_check[cid]
        md.append(f"### `{cid}` ({len(items)} occurrences)")
        md.append("")
        md.append(f"_{meaning}_")
        md.append("")
        # Show top 10 examples
        md.append("First 10 examples:")
        md.append("")
        md.append("| File | Line | Detail |")
        md.append("|------|------|--------|")
        for item in items[:10]:
            f = item["file"].replace("\\", "/")
            line = item.get("line", "")
            msg = (item.get("message", "") or "")[:120].replace("|", "\\|")
            md.append(f"| `{f}` | {line} | {msg} |")
        if len(items) > 10:
            md.append(f"| ... | ... | _and {len(items) - 10} more_ |")
        md.append("")

    md.append("## MEDIUM-severity issues (fix during quality polish)")
    md.append("")
    md.append("Affect pedagogy and accessibility but won't block KDP. Prioritize the higher-volume ones.")
    md.append("")
    for cid in sorted(by_check, key=lambda c: -len(by_check[c])):
        sev, meaning = DIAGRAM_CHECKS[cid]
        if sev != "MEDIUM":
            continue
        items = by_check[cid]
        md.append(f"### `{cid}` ({len(items)})")
        md.append("")
        md.append(f"_{meaning}_")
        md.append("")
        # Show top 5 examples
        md.append("First 5 examples:")
        md.append("")
        md.append("| File | Line | Detail |")
        md.append("|------|------|--------|")
        for item in items[:5]:
            f = item["file"].replace("\\", "/")
            line = item.get("line", "")
            msg = (item.get("message", "") or "")[:120].replace("|", "\\|")
            md.append(f"| `{f}` | {line} | {msg} |")
        if len(items) > 5:
            md.append(f"| ... | ... | _and {len(items) - 5} more_ |")
        md.append("")

    md.append("## LOW-severity issues")
    md.append("")
    for cid in sorted(by_check, key=lambda c: -len(by_check[c])):
        sev, meaning = DIAGRAM_CHECKS[cid]
        if sev != "LOW":
            continue
        items = by_check[cid]
        md.append(f"- **`{cid}`**: {len(items)} occurrences. {meaning}")
    md.append("")

    md.append("## Quick-win recommendations")
    md.append("")
    md.append("Highest-leverage fixes:")
    md.append("")
    md.append("1. **Add `width` / `height` attributes to all `<img>` tags** — 733 occurrences. Run `python scripts/find_missing_illustrations.py` or write a one-off script that adds dimensions from PIL.")
    md.append("2. **Renumber duplicate figures** — 41 `DUP_FIGURE_NUM` occurrences. Look at `scripts/fix_caption_numbering.py` and `scripts/fix_figure_sequence.py` (if they exist) and run.")
    md.append("3. **Fix SVG text overlaps** — 150 occurrences. The `scripts/audit_svg_overlaps.py` script identified them; the SVGs need manual repair (text repositioning) since the issue is visual.")
    md.append("4. **Replace generic SVG labels** — 86 occurrences. Many SVGs are titled simply 'Figure 1' or 'Diagram'; add descriptive labels for screen readers and EPUB nav.")
    md.append("5. **Fix figure-sequence + caption-misalign issues together** — 90 + 95 occurrences. These cascade: a misnumbered figure in section N.M shifts every reference downstream.")
    md.append("")

    md.append("## Critical observations")
    md.append("")
    md.append("From the agent's manual review of selected diagrams (transcript snippet):")
    md.append("")
    md.append("> **RoPE diagram is non-functional**: A diagram about Rotary Position Embeddings consists of three text boxes that say 'pos=0: No rotation' and 'pos=3: Rotated by 3θ' with no actual rotation visualization. A diagram about ROTARY embeddings doesn't show any rotation.")
    md.append("")
    md.append("Implication: even where the audit shows no automated issues, individual diagrams may be pedagogically broken. A human pass is needed for diagrams in math-heavy sections (Chapters 3-5: attention, Transformers, decoding).")
    md.append("")

    md.append("## What this report does NOT cover")
    md.append("")
    md.append("- **Factual correctness** of diagrams — the audit is structural; only a human can confirm whether an attention-pattern diagram correctly shows Q*K^T * V.")
    md.append("- **Pedagogical effectiveness** — whether each diagram earns its place in the chapter.")
    md.append("- **Raster image quality** — content of PNG/JPG figures was not opened and assessed.")
    md.append("- **Mermaid diagrams** — the audit ID list above doesn't include mermaid-specific checks; if mermaid is used, it would need a separate pass via `scripts/mermaid/`.")
    md.append("")
    md.append("Run a sample manual review of 5-10 random diagrams from each part to validate the structural audit's findings reflect real visual quality.")
    md.append("")

    OUT.write_text("\n".join(md), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} ({sum(len(l) for l in md):,} chars, {len(md)} lines)")


if __name__ == "__main__":
    main()
