"""v793: Address two issues found in the v792 landscape two-page
audit of 20 random EPUB pages.

ISSUE A (high severity): Wide tables broken awkwardly across columns
=====================================================================
On page 17 p2 (Appendix A.3 "Common Activation Functions and Their
Derivatives"), the 4-column 4-row table is being chopped across the
columns of a two-page landscape layout. The header lands in col 2,
two rows fit in col 2, the remaining rows spill into col 3, and 70%
of the page is empty below. Same symptom on other multi-column
landscape pages with tables narrower than the v790 wrap threshold
(6 cols), but still too wide to fit naturally in one column.

Root cause:
  - `wrap_wide_tables` in _html2epub_hooks.py only triggers at >= 6
    columns. Tables with 4-5 columns sit bare in the document.
  - In multi-column CSS contexts (Kindle Fire landscape, iPad), the
    browser/reader splits these tables column-by-column or row-by-row,
    leaving the bottom of the page empty after a partial row.

Fix:
  - CSS: any `table`, `.complex-table`, `.comparison-table` inside a
    multi-column container gets `column-span: all` so it occupies the
    full page width and continues onto the next page naturally.
  - Still allow `page-break-inside: auto` (per v790 user request).
  - Add `break-inside: avoid-column` so individual rows don't get
    split between columns.

ISSUE B (low severity): Tables with column-spans and decorative
"comparison-table-title" header get rendered with the title in one
column and the table starting in the next. The title and table
should stay together as a unit, span all columns.

Fix:
  - `.comparison-table, .complex-table-wrap` get column-span: all
    AND keep their internal title + table glued together with
    `page-break-inside: avoid` (for SHORT tables under ~10 rows) or
    `break-after: avoid` on the title to keep title and table together.

Both fixes are CSS-only; no source HTML changes required.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
overrides = ROOT / 'KDP' / 'build' / 'epub_overrides.css'
s = overrides.read_text(encoding='utf-8')

NEW_BLOCK = '''
/* ============================================================
 * v793 TABLE COLUMN-SPAN FIX (from v792 landscape audit)
 * ============================================================
 * Root cause: multi-column CSS contexts split tables awkwardly
 * across columns, leaving the bottom of pages empty when a row
 * ends mid-column. Force tables to span all columns of any
 * multi-column ancestor.
 *
 * Compatible with v790's "allow page-break inside table": tables
 * still split across PAGES, just not across COLUMNS of the same
 * page in two-page landscape.
 */
table,
.complex-table,
table.complex-table,
.comparison-table,
.comparison-table > table,
.comparison-table > .comparison-table-title,
div.table-wide-wrap,
.table-wide-wrap > table {
    -webkit-column-span: all !important;
    column-span: all !important;
}

/* Don't let individual rows be split across columns (a single row
 * fragment in column N and the rest in column N+1 looks broken). */
tr,
thead,
tbody,
tfoot,
.complex-table tr,
.comparison-table tr {
    -webkit-column-break-inside: avoid !important;
    break-inside: avoid-column !important;
}

/* Title + table must stay together as a unit: title should not
 * end up in column N while the table lands in column N+1. */
.comparison-table-title,
.complex-table-caption,
table caption {
    -webkit-column-break-after: avoid !important;
    break-after: avoid-column !important;
    page-break-after: avoid !important;
}

/* Tables wrapped in .comparison-table or .table-wide-wrap also
 * need their wrapper to span all columns (so the wrapper itself
 * doesn't end up in a single column with the table escaping it). */
div.comparison-table,
div.complex-table-wrap,
div.table-wide-wrap {
    -webkit-column-span: all !important;
    column-span: all !important;
    /* Still allow page-break (user wants tables to split pages) */
    page-break-inside: auto !important;
    break-inside: auto !important;
    margin: 0.6em 0 !important;
}

/* SHORT tables (under ~5 rows): keep together if possible. The
 * activation-functions table on page 17 has exactly this shape -
 * 4 rows, easy to fit on one page if we don't fragment it. */
table.short,
.complex-table.short,
.comparison-table.short {
    page-break-inside: avoid !important;
    break-inside: avoid !important;
}

/* Tables inside callouts/sidebars stay in their parent column
 * (they're usually narrow examples, and column-span:all would
 * break them out of the callout box). */
.callout table,
.callout .complex-table,
aside table,
.sidebar table {
    -webkit-column-span: none !important;
    column-span: none !important;
}
'''

START = '/* ============================================================\n * v793 TABLE COLUMN-SPAN'

if START in s:
    idx = s.index(START)
    s = s[:idx].rstrip() + '\n' + NEW_BLOCK
    print('  [v793 block REPLACED in epub_overrides.css]')
else:
    s = s.rstrip() + '\n' + NEW_BLOCK
    print(f'  [v793 block ADDED to epub_overrides.css ({len(NEW_BLOCK)} chars)]')

overrides.write_text(s, encoding='utf-8')
print(f'  size now: {len(s):,} chars')
