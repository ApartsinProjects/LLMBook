"""
Audit all <table> elements in source HTML, classify by problem severity for
narrow-viewport (Kindle) reading, propose simplification approach per type.

Outputs: KDP/validation/tables_audit.md (analysis only, no source modified)
"""
from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from bs4 import BeautifulSoup

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUT_PATH = PROJECT_ROOT / "KDP" / "validation" / "tables_audit.md"

# Kindle viewport heuristics (compressed widths after device chrome)
KINDLE_NARROW_PX = 600   # Paperwhite portrait reading area
KINDLE_WIDE_PX   = 1000  # Scribe / iPad Mini portrait

# Severity thresholds (cols)
COLS_SEVERE = 6   # 6+ cols definitely won't fit narrow Kindle
COLS_WARN   = 4   # 4-5 cols may overflow on narrow Kindle
ROWS_LARGE  = 15  # rows × cols matters for scroll burden


def all_source_html() -> list[Path]:
    files: list[Path] = []
    for p in PROJECT_ROOT.rglob("*.html"):
        rel = p.relative_to(PROJECT_ROOT)
        if rel.parts and rel.parts[0] in {"KDP", "scripts", "vendor", "templates", "md", "node_modules"}:
            continue
        files.append(p)
    return files


def analyze_table(table_soup: BeautifulSoup) -> dict:
    """Return shape + content stats for one table."""
    rows = table_soup.find_all("tr")
    n_rows = len(rows)
    # Get max cell count across all rows
    n_cols = 0
    has_thead = bool(table_soup.find("thead"))
    has_caption = bool(table_soup.find("caption"))
    cell_chars = []
    for row in rows:
        cells = row.find_all(["td", "th"])
        n_cols = max(n_cols, len(cells))
        for cell in cells:
            cell_chars.append(len(cell.get_text(strip=True)))
    avg_cell = sum(cell_chars) // max(len(cell_chars), 1)
    max_cell = max(cell_chars) if cell_chars else 0
    return {
        "rows": n_rows,
        "cols": n_cols,
        "has_thead": has_thead,
        "has_caption": has_caption,
        "cells": len(cell_chars),
        "avg_cell_chars": avg_cell,
        "max_cell_chars": max_cell,
        "total_chars": sum(cell_chars),
    }


def classify_severity(stats: dict) -> tuple[str, str, str]:
    """Return (severity, problem, suggestion)."""
    cols = stats["cols"]
    rows = stats["rows"]
    avg = stats["avg_cell_chars"]

    if cols >= COLS_SEVERE:
        if avg <= 25 and rows <= 12:
            return ("HIGH", f"{cols}-column comparison/matrix table won't fit narrow Kindle (~600 px reading width)",
                    "**Convert to definition list (<dl>)** if rows describe items, OR rotate (transpose rows<->cols), OR split into 2 narrower tables")
        elif avg > 25 or stats["max_cell_chars"] > 80:
            return ("HIGH", f"{cols} wide columns with {avg}-char avg cell content; will overflow on Kindle",
                    "**Convert to bulleted list per row**, with header items as the bullet label and other cells as nested sub-bullets")
        else:
            return ("HIGH", f"{cols} columns × {rows} rows = wide grid",
                    "**Split into multiple tables** by logical category, OR redesign as a section per item with prose")
    elif cols >= COLS_WARN:
        if avg > 30:
            return ("MEDIUM", f"{cols}-col table with verbose cells (avg {avg} chars) - text wrap will be ugly",
                    "Consider definition list or 2-column transposed layout")
        else:
            return ("LOW", f"{cols}-col table, manageable",
                    "Likely fits if cells stay short; verify in Kindle Previewer")
    else:
        return ("LOW", f"{cols}-col table",
                "Fine on most readers")


def main() -> int:
    files = all_source_html()
    print(f"Scanning {len(files)} source HTML files for <table> elements...")

    tables_data = []  # (file_rel, table_index_in_file, stats, severity, problem, suggestion, sample)

    for file in files:
        try:
            html = file.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        if "<table" not in html:
            continue
        soup = BeautifulSoup(html, "lxml")
        tables = soup.find_all("table")
        for i, t in enumerate(tables):
            stats = analyze_table(t)
            sev, problem, suggestion = classify_severity(stats)
            # Sample first row content for context
            first_row = t.find("tr")
            sample = ""
            if first_row:
                cells = first_row.find_all(["td", "th"])
                sample = " | ".join(c.get_text(strip=True)[:30] for c in cells[:6])
            rel = str(file.relative_to(PROJECT_ROOT)).replace("\\", "/")
            tables_data.append({
                "file": rel,
                "idx": i + 1,
                "stats": stats,
                "severity": sev,
                "problem": problem,
                "suggestion": suggestion,
                "sample": sample,
            })

    print(f"Found {len(tables_data)} tables across {len(set(t['file'] for t in tables_data))} files")

    # Summary stats
    sev_counter = Counter(t["severity"] for t in tables_data)
    cols_dist = Counter(t["stats"]["cols"] for t in tables_data)

    # Build markdown report
    md: list[str] = []
    md.append("# Tables Audit — Simplification Recommendations")
    md.append("")
    md.append(f"_Generated by `KDP/validation/audit_tables.py`. Analysis only; no source modified._")
    md.append("")
    md.append("## Why this matters")
    md.append("")
    md.append(f"Kindle Paperwhite has a ~600 px reading width in portrait. "
              f"Tables with **6+ columns** or **wide cells (50+ chars)** overflow horizontally, "
              f"making them either truncated, scrolled, or unreadable. This audit finds those "
              f"and proposes per-table simplifications.")
    md.append("")
    md.append("## Summary")
    md.append("")
    md.append(f"- **Total tables**: {len(tables_data)}")
    md.append(f"- **Files with tables**: {len(set(t['file'] for t in tables_data))}")
    md.append("")
    md.append("| Severity | Count | What it means |")
    md.append("|----------|------:|---------------|")
    md.append(f"| **HIGH** | {sev_counter.get('HIGH', 0)} | Won't fit narrow Kindle; needs simplification before publication |")
    md.append(f"| **MEDIUM** | {sev_counter.get('MEDIUM', 0)} | May overflow depending on cell content; verify in Kindle Previewer |")
    md.append(f"| **LOW** | {sev_counter.get('LOW', 0)} | Should be fine on most readers |")
    md.append("")
    md.append("## Column count distribution")
    md.append("")
    md.append("| Columns | Tables | Notes |")
    md.append("|--------:|-------:|-------|")
    for cols in sorted(cols_dist.keys()):
        note = ""
        if cols >= 6:
            note = "— overflow risk on Kindle"
        elif cols >= 4:
            note = "— borderline"
        else:
            note = "— fits"
        md.append(f"| {cols} | {cols_dist[cols]} | {note} |")
    md.append("")

    # ---- HIGH severity per-file
    high_tables = [t for t in tables_data if t["severity"] == "HIGH"]
    md.append(f"## HIGH-severity tables ({len(high_tables)} tables — fix before publication)")
    md.append("")
    md.append("Grouped by file. Each table links to its source location and includes a simplification proposal.")
    md.append("")
    by_file: dict[str, list[dict]] = defaultdict(list)
    for t in high_tables:
        by_file[t["file"]].append(t)
    # Sort files by number of HIGH tables descending
    for file_rel, tables in sorted(by_file.items(), key=lambda kv: -len(kv[1])):
        md.append(f"### `{file_rel}` ({len(tables)} HIGH tables)")
        md.append("")
        for t in tables:
            md.append(f"**Table #{t['idx']}** — {t['stats']['cols']} cols × {t['stats']['rows']} rows "
                      f"(~{t['stats']['total_chars']} chars; "
                      f"avg cell {t['stats']['avg_cell_chars']} chars)")
            md.append("")
            md.append(f"- **Header sample**: `{t['sample']}`")
            md.append(f"- **Problem**: {t['problem']}")
            md.append(f"- **Suggestion**: {t['suggestion']}")
            md.append("")

    # ---- MEDIUM severity summary table
    medium_tables = [t for t in tables_data if t["severity"] == "MEDIUM"]
    if medium_tables:
        md.append(f"## MEDIUM-severity tables ({len(medium_tables)} tables)")
        md.append("")
        md.append("| File | Table# | Cols × Rows | Avg cell chars | Suggestion |")
        md.append("|------|-------:|------------:|---------------:|------------|")
        for t in sorted(medium_tables, key=lambda x: -x["stats"]["cols"])[:30]:
            md.append(f"| `{t['file']}` | {t['idx']} | "
                      f"{t['stats']['cols']}×{t['stats']['rows']} | "
                      f"{t['stats']['avg_cell_chars']} | "
                      f"{t['suggestion'].split(',')[0]} |")
        if len(medium_tables) > 30:
            md.append(f"| ... | ... | ... | ... | _and {len(medium_tables) - 30} more_ |")
        md.append("")

    # ---- Reusable simplification patterns
    md.append("## Simplification patterns (reusable)")
    md.append("")
    md.append("### Pattern 1: 6-col comparison table → definition list")
    md.append("")
    md.append("**Before:**")
    md.append("```html")
    md.append('<table>')
    md.append('  <thead><tr><th>Model</th><th>Params</th><th>Context</th><th>Cost</th><th>License</th><th>Notes</th></tr></thead>')
    md.append('  <tbody>')
    md.append('    <tr><td>GPT-4o</td><td>?</td><td>128k</td><td>$2.50/1M</td><td>Commercial</td><td>Best for X</td></tr>')
    md.append('    <tr><td>Claude 3.5</td><td>?</td><td>200k</td><td>$3/1M</td><td>Commercial</td><td>Best for Y</td></tr>')
    md.append('  </tbody>')
    md.append('</table>')
    md.append("```")
    md.append("")
    md.append("**After (Kindle-friendly):**")
    md.append("```html")
    md.append('<dl class="model-comparison">')
    md.append('  <dt>GPT-4o</dt>')
    md.append('  <dd><strong>Params:</strong> ? · <strong>Context:</strong> 128k · <strong>Cost:</strong> $2.50/1M · <strong>License:</strong> Commercial. Best for X.</dd>')
    md.append('  <dt>Claude 3.5</dt>')
    md.append('  <dd><strong>Params:</strong> ? · <strong>Context:</strong> 200k · <strong>Cost:</strong> $3/1M · <strong>License:</strong> Commercial. Best for Y.</dd>')
    md.append('</dl>')
    md.append("```")
    md.append("")
    md.append("### Pattern 2: Wide grid → split by category")
    md.append("")
    md.append("If columns split naturally by topic (e.g. \"costs\" + \"specs\" + \"performance\"), present as 2-3 stacked narrower tables, each with the model name + 2-3 attributes.")
    md.append("")
    md.append("### Pattern 3: Long verbose comparison → bulleted list per row")
    md.append("")
    md.append("**Before:** 6-col table with paragraph-length cells.")
    md.append("**After:**")
    md.append("```html")
    md.append('<h4>GPT-4o</h4>')
    md.append('<ul>')
    md.append('  <li><strong>Strengths:</strong> reasoning, code generation, multilingual</li>')
    md.append('  <li><strong>Weaknesses:</strong> cost at scale, no on-device option</li>')
    md.append('  <li><strong>Best for:</strong> production agents needing top-tier reasoning</li>')
    md.append('</ul>')
    md.append("```")
    md.append("")
    md.append("### Pattern 4: Transpose")
    md.append("")
    md.append("If you have 8 columns × 4 rows, transpose to 4 cols × 8 rows. Now the wide axis is vertical (scrolls), narrow axis is horizontal (fits).")
    md.append("")
    md.append("### Pattern 5: Mark as \"complex — read on tablet\"")
    md.append("")
    md.append("For a few irreducibly wide tables (e.g. a hyperparameter grid), wrap in `<div class=\"complex-table\">` and add a callout:")
    md.append("")
    md.append("```html")
    md.append('<div class="callout note">')
    md.append('  <div class="callout-title">Complex Table</div>')
    md.append('  <p>This table is dense — for best readability, view on a tablet, computer, or in landscape orientation.</p>')
    md.append('</div>')
    md.append("```")
    md.append("")
    md.append("### Recommended fix sequence")
    md.append("")
    md.append("1. Tackle HIGH-severity files in order of count (most-table-heavy first)")
    md.append("2. For each table, pick the pattern that best matches the data shape")
    md.append("3. Test in Kindle Previewer at narrow portrait setting")
    md.append("4. For irreducibly wide tables, leave as-is and add the \"complex\" note")
    md.append("")
    md.append("Estimated total effort to fix all HIGH-severity: ~30-60 minutes per file across most chapters; ~2 hours for the worst (appendix-v, appendix-h, fm-8).")
    md.append("")
    md.append("---")
    md.append("")
    md.append(f"_Audit completed; see source files referenced above for the actual table markup._")

    OUT_PATH.write_text("\n".join(md), encoding="utf-8")
    print(f"Wrote {OUT_PATH.relative_to(PROJECT_ROOT)} ({sum(len(l) for l in md):,} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
