"""v788: Make code blocks ACTUALLY break across pages on Kindle, plus
hide the .header-search wrapper, and tighten remaining margins.

ROOT CAUSE OF CODE CLIPPING (still happening after v787):
  1. `box-decoration-break: clone` on <pre> forces Kindle to treat
     the element as ONE box (clone semantics need full geometry up
     front). Removing clone from <pre> while keeping it on .callout.
  2. `.code-block-wrapper` has `overflow: hidden` from book.css that
     traps the inner <pre>. We set wrapper overflow:visible and let
     the <pre> itself flow.
  3. Some Kindle KFX renderers honor only `break-inside` not
     `page-break-inside`. We set BOTH plus `-webkit-column-break-inside`.
  4. `widows: 3; orphans: 3` from default_overrides.css means a code
     block needs 3+ lines on each page-fragment - if only 2 fit at
     the bottom, the whole thing pushes. Reduce to widows:1; orphans:1
     for <pre> specifically.

OTHER FIXES:
  - .header-search wrapper (hides empty search box rectangle still
    visible in chapters' top-of-page area)
  - Stronger callout-title bottom-margin tightening (the big gap
    between WARNING title and content)
  - Math wrapper top/bottom margin reduction
  - Stronger overflow: hidden on math container including
    .math-display, .equation, .math-block parent divs
  - Search box wrapper .header-search must die (root cause of "search
    box at chapter header" complaint)
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
overrides = ROOT / 'KDP' / 'build' / 'epub_overrides.css'
s = overrides.read_text(encoding='utf-8')

NEW_BLOCK = '''
/* ============================================================
 * v788 truly break <pre> + remaining chrome / margin tightening
 * ============================================================ */

/* HIDE the search-box wrapper (root cause of the empty rectangle at
 * top of every chapter). v786 only hid inner #search; the wrapper
 * div still rendered as empty space. */
.header-search,
div.header-search,
nav.header-nav,
.header-nav,
header > nav,
.chapter-header > nav.header-nav,
.toc-icon,
.book-title-link {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
    visibility: hidden !important;
}

/* CODE BLOCKS - actually break across pages.
 *
 * Strategy:
 *   - Remove clone (it forces atomic on KFX)
 *   - widows/orphans 1 (any 1 line is OK to leave on a page)
 *   - parent .code-block-wrapper overflow visible (was hidden)
 *   - explicit min-height: 0 (Kindle infers tall min-heights)
 *   - explicit max-height: none (likewise)
 */
.code-block-wrapper,
div.code-block-wrapper {
    overflow: visible !important;
    overflow-x: visible !important;
    overflow-y: visible !important;
    page-break-inside: auto !important;
    break-inside: auto !important;
    -webkit-column-break-inside: auto !important;
    min-height: 0 !important;
    max-height: none !important;
    height: auto !important;
    /* No background / border on wrapper - the <pre> itself paints */
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin: 0.6em 0 !important;
}
pre,
pre.pygments-highlighted,
pre[class*="language-"],
.code-block-wrapper > pre,
.callout pre,
.callout > pre,
.callout .code-block-wrapper > pre {
    page-break-inside: auto !important;
    break-inside: auto !important;
    -webkit-column-break-inside: auto !important;
    /* CRITICAL: NO clone on pre - it forces atomic layout */
    -webkit-box-decoration-break: slice !important;
    box-decoration-break: slice !important;
    /* Allow 1-line widows/orphans so a 2-line tail can stay */
    widows: 1 !important;
    orphans: 1 !important;
    min-height: 0 !important;
    max-height: none !important;
    height: auto !important;
    overflow-x: visible !important;
    overflow-y: visible !important;
    /* Wrap long lines so horizontal clipping doesn't happen either */
    white-space: pre-wrap !important;
    word-wrap: break-word !important;
    overflow-wrap: anywhere !important;
    word-break: break-word !important;
}

/* TABLES: same treatment - remove clone, allow row-by-row break */
table {
    page-break-inside: auto !important;
    break-inside: auto !important;
    -webkit-column-break-inside: auto !important;
    -webkit-box-decoration-break: slice !important;
    box-decoration-break: slice !important;
    widows: 1 !important;
    orphans: 1 !important;
    min-height: 0 !important;
    max-height: none !important;
    height: auto !important;
}
/* Each row stays whole, table breaks BETWEEN rows */
tr {
    page-break-inside: avoid !important;
    break-inside: avoid !important;
    -webkit-column-break-inside: avoid !important;
}

/* CALLOUT-TITLE bottom margin: the WARNING / TIP / NOTE title had a
 * big gap between itself and the body text. Cut it sharper. */
.callout-title,
.callout > .callout-title,
.callout > p.callout-title,
.callout > div.callout-title,
.callout > h3.callout-title,
.callout > h4.callout-title,
div.callout-title {
    margin: 0 0 0.25em 0 !important;
    padding: 0 !important;
    line-height: 1.25 !important;
}
.callout > p:first-of-type,
.callout > div:not(.callout-title):first-of-type,
.callout-title + p,
.callout-title + ul,
.callout-title + ol,
.callout-title + pre,
.callout-title + .code-block-wrapper {
    margin-top: 0.2em !important;
}
/* Callout body padding-top was eating space */
.callout {
    padding-top: 0.5em !important;
    padding-bottom: 0.5em !important;
}
.callout > *:last-child {
    margin-bottom: 0 !important;
    padding-bottom: 0 !important;
}

/* MATH BLOCKS - top/bottom margin trim + scrollbar suppression
 * everywhere */
.math-block,
div.math-block,
.math-display,
div.math-display,
.equation,
div.equation,
.katex-display,
.katex-rendered,
math {
    margin: 0.4em 0 !important;
    padding: 0.2em 0 !important;
    overflow: hidden !important;
    overflow-x: hidden !important;
    overflow-y: hidden !important;
    scrollbar-width: none !important;
    -ms-overflow-style: none !important;
    max-height: none !important;
    min-height: 0 !important;
    height: auto !important;
}
.math-block::-webkit-scrollbar,
.math-display::-webkit-scrollbar,
.equation::-webkit-scrollbar,
.katex-display::-webkit-scrollbar,
.katex-rendered::-webkit-scrollbar,
math::-webkit-scrollbar,
*::-webkit-scrollbar {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
    background: transparent !important;
}
/* Some renderers add a scrollbar via ::scrollbar-thumb pseudo */
*::-webkit-scrollbar-thumb,
*::-webkit-scrollbar-track {
    display: none !important;
    background: transparent !important;
}

/* ROOT-CAUSE callout margin: many callouts have huge above/below
 * margin from book.css `.callout { margin: 1.5rem 0 }`. Force a tighter
 * single value. */
.callout,
div.callout,
aside.callout {
    margin-top: 0.7em !important;
    margin-bottom: 0.7em !important;
}
/* Adjacent callouts: collapse margin so two boxes don't have 1.4em
 * between them. */
.callout + .callout,
.callout + div.callout,
.callout + .code-block-wrapper,
.callout + pre,
pre + .callout,
.code-block-wrapper + .callout,
h2 + .callout,
h3 + .callout,
h4 + .callout,
p + .callout {
    margin-top: 0.4em !important;
}

/* Section headings followed by callout/box: tight spacing */
h2 + .callout,
h2 + .code-block-wrapper,
h2 + figure,
h2 + table,
h3 + .callout,
h3 + .code-block-wrapper,
h3 + figure,
h3 + table {
    margin-top: 0.3em !important;
}

/* Hands-On Lab card spacing tightening (the lab card with Objective
 * sub-callout had huge bottom margin) */
.callout.lab,
.lab-card,
div.lab-card {
    padding-bottom: 0.5em !important;
    margin-bottom: 0.7em !important;
}
.callout.lab > *:last-child {
    margin-bottom: 0 !important;
}
'''

START = '/* ============================================================\n * v788'

if START in s:
    idx = s.index(START)
    s = s[:idx].rstrip() + '\n' + NEW_BLOCK
    print('  [v788 block REPLACED in epub_overrides.css]')
else:
    s = s.rstrip() + '\n' + NEW_BLOCK
    print(f'  [v788 block ADDED to epub_overrides.css ({len(NEW_BLOCK)} chars)]')

overrides.write_text(s, encoding='utf-8')
