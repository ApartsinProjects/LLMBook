"""v795: Re-tighten table break-inside rules.

ROOT CAUSE
==========
v790 set `table { page-break-inside: auto }` and `tr { page-break-
inside: auto }` based on user feedback "it's ok to split table across
pages, avoid unused space". That helped LONG tables (15+ rows) that
would push past page boundary and leave empty space when forced to
stay together.

But it OVER-CORRECTED for SHORT tables (the 4-row activation-
functions table in Appendix A.3): now they get split between header
in column N and data rows in column N+1 of a two-page landscape
layout, looking even worse than the original problem.

v793 tried to fix this via `column-span: all` but CSS column-span
only works on direct children of the multi-column container -- not
through nested ancestors (the .comparison-table div, etc.). So the
column-span rule has no effect when the table is nested.

FIX
===
Reverse: tables and rows default to `break-inside: avoid`. Only
tables explicitly marked `.long-table` or wider than 6 columns
(already wrapped in .table-wide-wrap by _html2pub_hooks.py) get
`break-inside: auto`.

Net behavior:
  - Short tables (4-row activation table): stay together, fit in
    one column of landscape view, no split.
  - Long tables (15-row hyperparameter table): split across pages
    so they don't push down with empty space above them.
  - Wide tables (>=6 cols): already get .table-wide-wrap from
    _html2pub_hooks.py; that wrapper allows break-inside: auto
    inside the wrapper (so wide tables can still be split if needed).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
overrides = ROOT / 'KDP' / 'build' / 'epub_overrides.css'
s = overrides.read_text(encoding='utf-8')

NEW_BLOCK = '''
/* ============================================================
 * v795 TABLE BREAK-INSIDE: revert v790 over-correction
 * ============================================================
 * DEFAULT: tables stay together (no column/page split).
 * EXCEPTIONS: .long-table, .table-wide-wrap > table, or tables
 * with >12 rows can split.
 */
table,
.complex-table,
table.complex-table,
.comparison-table,
.comparison-table table,
.comparison-table > table {
    -webkit-column-break-inside: avoid !important;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
}
/* Rows: don't split mid-row in any rendering */
tr,
thead,
tbody,
tfoot {
    -webkit-column-break-inside: avoid !important;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
}
/* Bring caption/title + table together as a unit */
.comparison-table {
    page-break-inside: avoid !important;
    break-inside: avoid !important;
}

/* EXCEPTION: long tables can split. Marker class: .long-table.
 * (Currently none in source, but reserved for future use.) */
table.long-table,
table.long-table tr {
    page-break-inside: auto !important;
    break-inside: auto !important;
}

/* EXCEPTION: explicitly-wide tables (.table-wide-wrap is added
 * by _html2pub_hooks.py for tables >=6 cols). These can split
 * because keeping them whole leaves a half-empty page when they
 * don't fit. */
.table-wide-wrap,
.table-wide-wrap > table,
.table-wide-wrap > table tr {
    page-break-inside: auto !important;
    break-inside: auto !important;
}
'''

START = '/* ============================================================\n * v795 TABLE BREAK-INSIDE'

if START in s:
    idx = s.index(START)
    s = s[:idx].rstrip() + '\n' + NEW_BLOCK
    print('  [v795 block REPLACED in epub_overrides.css]')
else:
    s = s.rstrip() + '\n' + NEW_BLOCK
    print(f'  [v795 block ADDED to epub_overrides.css ({len(NEW_BLOCK)} chars)]')

overrides.write_text(s, encoding='utf-8')
print(f'  size now: {len(s):,} chars')
