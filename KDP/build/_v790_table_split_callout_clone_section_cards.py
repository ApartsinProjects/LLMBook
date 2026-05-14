"""v790: Tables split between rows, callout box-decoration-break:slice
(not clone, which painted the box border down to column bottom even
with no content), table header text contrast, section-card flex
layout (number badge + text overlap), chapter-header to first main
child margin, math-in-table-cell wrapping.

ROOT CAUSE 1: Table doesn't split across pages
==============================================
v788 set table page-break-inside:auto and tr:avoid, but Kindle still
treats tables as atomic. Per user feedback: "it's ok to split table
across pages, avoid unused space (like in the left page)." So we now
allow breaks even WITHIN rows. Defense in depth:
  - table {display: block; page-break-inside: auto}
  - thead/tbody {display: table-row-group} (not block; lets thead
    repeat on each fragment if KFX honors it)
  - tr {page-break-inside: auto}  (was avoid; allow any-row breaks)
  - widows/orphans 1 on table descendants

ROOT CAUSE 2: Callout box border painted to column bottom (looks
like empty space inside the box). The box-decoration-break: clone
on .callout caused KFX to repaint the bottom border at the page-
fragment boundary, looking like the box was much taller than its
content. Switch clone -> slice (no repaint at fragment edge).

ROOT CAUSE 3: Section-card number badge overlaps title text.
The .section-card uses display:flex from book.css but the
.section-num pill is being positioned absolutely in landscape
mode somehow. Force explicit display:flex with align-items:flex-
start + gap:0.6em + flex-shrink:0 on the badge.

ROOT CAUSE 4: Chapter-header to first content block has huge gap.
The selector header + .epigraph doesn't match because .epigraph is
INSIDE main.content, not a sibling of header. Use main.content >
:first-child + main.content > .epigraph + main.content > blockquote.

ROOT CAUSE 5: Table header bad contrast. The table th has dark navy
background (#1a1a2e or similar) but text is also dark, making it
invisible. Force white text on dark th background.

ROOT CAUSE 6: Math inside table cells renders broken (e.g., tanh
formula spans 3 lines). Math inline in cells should not wrap; use
white-space: nowrap on math children of td.

ROOT CAUSE 7: Author bio cards not flowing - too tall, atomic.
Author cards with long bios should split across pages on landscape.
Switch .author-card to page-break-inside: auto for long bios.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
overrides = ROOT / 'KDP' / 'build' / 'epub_overrides.css'
s = overrides.read_text(encoding='utf-8')

NEW_BLOCK = '''
/* ============================================================
 * v790 table splits + callout slice + section-card overlap +
 * header gap + table header contrast + math-in-cell + bio flow
 * ============================================================ */

/* 1. TABLES: aggressively allow splitting (user request) */
table,
.complex-table,
.comparison-table,
table.complex-table,
table.comparison-table {
    display: table !important;          /* keep tabular layout */
    width: 100% !important;
    page-break-inside: auto !important;
    break-inside: auto !important;
    -webkit-column-break-inside: auto !important;
    -webkit-box-decoration-break: slice !important;
    box-decoration-break: slice !important;
    widows: 1 !important;
    orphans: 1 !important;
    border-collapse: collapse !important;
}
thead { display: table-header-group !important; }
tbody { display: table-row-group !important; }
tr {
    /* Allow row to split too if the row itself is taller than a page.
     * User said "it's ok to split table across pages, avoid unused
     * space" - so we now permit ANY break, even within a row. */
    page-break-inside: auto !important;
    break-inside: auto !important;
    widows: 1 !important;
    orphans: 1 !important;
}
/* 2. TABLE HEADER CONTRAST: dark navy bg with white text */
th,
table th,
thead th {
    background: #1a1a2e !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    padding: 0.5em 0.7em !important;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
    border: 1px solid #2a2a4e !important;
}
td {
    color: #1a1a2e !important;
    background: #ffffff !important;
    padding: 0.5em 0.7em !important;
    border: 1px solid #d0d7de !important;
    vertical-align: top !important;
}
/* Striped rows (already in book.css) - keep but ensure text contrast */
tbody tr:nth-child(even) td { background: #f6f8fa !important; }

/* 6. MATH INSIDE TABLE CELLS: no wrap, smaller font */
td math, td .katex, td .katex-rendered, td span.math,
th math, th .katex, th .katex-rendered, th span.math {
    white-space: nowrap !important;
    font-size: 0.9em !important;
    overflow: visible !important;
    word-break: keep-all !important;
}
td .math-block, th .math-block {
    margin: 0.2em 0 !important;
    padding: 0 !important;
}

/* 3. CALLOUT box-decoration-break: SLICE not clone.
 * Clone caused the bottom border to be repainted at every page-
 * fragment boundary, making the box look full-column-height even
 * when the content was a single paragraph. Slice = paint the border
 * once around the actual content. */
.callout,
div.callout,
aside.callout,
.callout.tip,
.callout.note,
.callout.warning,
.callout.exercise,
.callout.algorithm,
.callout.fun-note,
.callout.research-frontier,
.callout.practical-example,
.callout.big-picture,
.callout.key-insight,
.callout.library-shortcut,
.callout.production-pattern,
.callout.postmortem,
.callout.thesis-thread,
.callout.numeric-example,
.callout.self-check,
.callout.looking-back,
.callout.cross-ref,
.callout.lab,
.callout.pathway,
.callout.key-takeaway {
    -webkit-box-decoration-break: slice !important;
    box-decoration-break: slice !important;
}

/* 4. SECTION CARD layout: number badge + title overlap fix.
 * The .section-card from book.css uses flex but the badge wraps
 * under the title in landscape view. Force explicit flex with
 * proper alignment. */
.section-card,
a.section-card,
li > a.section-card,
.section-grid > a.section-card {
    display: -webkit-flex !important;
    display: flex !important;
    -webkit-flex-direction: row !important;
    flex-direction: row !important;
    -webkit-flex-wrap: wrap !important;
    flex-wrap: wrap !important;
    -webkit-align-items: flex-start !important;
    align-items: flex-start !important;
    gap: 0.6em !important;
    padding: 0.7em 0.9em !important;
    margin: 0 0 0.5em 0 !important;
    background: #ffffff !important;
    border: 1px solid #d0d7de !important;
    border-left: 4px solid #1a4078 !important;
    border-radius: 0 4px 4px 0 !important;
    text-decoration: none !important;
    color: inherit !important;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
}
.section-card .section-num,
a.section-card .section-num {
    display: inline-block !important;
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif !important;
    font-size: 0.8em !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    background: #1a4078 !important;
    padding: 0.25em 0.55em !important;
    border-radius: 4px !important;
    min-width: 2em !important;
    text-align: center !important;
    -webkit-flex-shrink: 0 !important;
    flex-shrink: 0 !important;
    margin: 0 0.5em 0.2em 0 !important;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
    /* CRITICAL: vertical-align fixes the overlap with title text */
    vertical-align: top !important;
    line-height: 1.3 !important;
}
.section-card .section-title,
a.section-card .section-title {
    font-weight: 700 !important;
    color: #1a4078 !important;
    font-size: 1em !important;
    -webkit-flex: 1 1 auto !important;
    flex: 1 1 auto !important;
    min-width: 12em !important;
    line-height: 1.3 !important;
}
.section-card .section-desc,
a.section-card .section-desc {
    display: block !important;
    -webkit-flex-basis: 100% !important;
    flex-basis: 100% !important;
    width: 100% !important;
    margin-top: 0.3em !important;
    color: #455a64 !important;
    font-size: 0.92em !important;
    line-height: 1.45 !important;
}
.section-card .badge,
a.section-card .badge {
    display: none !important;
}

/* 5. CHAPTER-HEADER -> EPIGRAPH spacing.
 * Selector header + .epigraph doesn't match because .epigraph is
 * inside <main.content>, not a sibling of <header>. */
main.content > *:first-child,
main.content > blockquote.epigraph,
main.content > .epigraph,
main.content > .pagefind-meta-injected + *,
main.content > span + blockquote.epigraph,
main.content > span + .epigraph,
main.content > span + figure,
main.content > span + .callout {
    margin-top: 0.4em !important;
}
.chapter-header + main.content > *:first-child {
    margin-top: 0.3em !important;
}
.chapter-header {
    margin-bottom: 0.4em !important;
}

/* 7. AUTHOR BIO CARDS: allow flow if long.
 * The .author-card had page-break-inside: avoid making it atomic;
 * for landscape two-page view, a tall bio that doesn't fit gets
 * pushed to the next column leaving empty space. Allow break with
 * box-decoration-break: slice. */
.author-card {
    page-break-inside: auto !important;
    break-inside: auto !important;
    -webkit-box-decoration-break: slice !important;
    box-decoration-break: slice !important;
    widows: 2 !important;
    orphans: 2 !important;
}

/* Heading "About the Authors" + first author-card MUST stay together
 * (otherwise heading sits alone on the previous page). */
h1 + .author-card,
h2 + .author-card,
h2 + p + .author-card {
    page-break-before: avoid !important;
    break-before: avoid !important;
    margin-top: 0.4em !important;
}

/* Last fix: callout that was empty (Logarithmic Magnifying Glass) -
 * could be the result of clone repainting border + content being on
 * next page. Slice mode (above) should fix it. As a safety net,
 * force min/max heights to content. */
.callout {
    min-height: 0 !important;
    max-height: none !important;
    height: auto !important;
}
'''

START = '/* ============================================================\n * v790 table splits'

if START in s:
    idx = s.index(START)
    s = s[:idx].rstrip() + '\n' + NEW_BLOCK
    print('  [v790 block REPLACED in epub_overrides.css]')
else:
    s = s.rstrip() + '\n' + NEW_BLOCK
    print(f'  [v790 block ADDED to epub_overrides.css ({len(NEW_BLOCK)} chars)]')

overrides.write_text(s, encoding='utf-8')
