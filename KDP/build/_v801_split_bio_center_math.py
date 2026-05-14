"""v801: Two fixes from user feedback:
A. Make .author-card splittable across pages (so bio starts right
   after the heading instead of jumping to next page).
B. Center display math properly (text-align:center doesn't center
   block-display math; need inline-block + margin:auto).

PROBLEM A: bio jumps to next page
==================================
After "About the Authors" heading, the first .author-card (Alexander)
moved to a fresh page leaving the heading alone. Cause: every prior
rule on `.author-card` declared `page-break-inside: avoid !important`
(8 occurrences in epub_overrides.css). This forces the WHOLE card to
stay on one page; if it doesn't fit, it moves to the next page
entirely, leaving empty space.

Fix: switch .author-card to `page-break-inside: auto` so the card
can split across pages. Also keep `page-break-before: avoid` on
the FIRST card after the heading so it starts flush with the heading
(can split its body to next page if needed, but the first lines stay
adjacent to "About the Authors").

PROBLEM B: MSE formula left-aligned + tall box
================================================
The display math (MSE formula) renders LEFT-aligned inside the
.math-block box. Root cause:
- .math-block has `text-align: center !important` ✓
- BUT the inner katex-display span is `display: block` (full-width)
- A full-width block can't be centered by text-align (text-align
  only centers INLINE content, and block takes the full width)
- Same for `math[display="block"]` — block-level math takes full
  width regardless of text-align on parent

Fix: make the inner katex-display / math[display=block] use
`display: inline-block` so it shrinks to content width, then the
parent's `text-align: center` actually centers it.

For LARGE box padding: book.css has `padding: 1.2em 1.5em` on
.math-block. Tighten further to .5em vertical, .8em horizontal
so the box hugs the formula.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
overrides = ROOT / 'KDP/build/epub_overrides.css'
s = overrides.read_text(encoding='utf-8')

ADD = '''
/* ============================================================
 * v801 — bio splittable + display math centering
 * ============================================================ */

/* A. AUTHOR CARDS: splittable so bio starts adjacent to heading.
 *    Override prior `page-break-inside: avoid` rules. The heading-
 *    keep-with-first-card rule is kept so the title doesn't sit
 *    alone above blank space. */
.author-card,
div.author-card,
.author-cards .author-card,
.about-authors .author-card,
.about-the-authors .author-card {
    page-break-inside: auto !important;
    break-inside: auto !important;
    -webkit-box-decoration-break: slice !important;
    box-decoration-break: slice !important;
    widows: 2 !important;
    orphans: 2 !important;
}

/* Keep heading and first card glued. First card content can flow to
 * next page if too tall, but its TOP must stay adjacent to heading. */
h1 + .author-card,
h2 + .author-card,
h1 + .author-cards .author-card:first-child,
h2 + .author-cards .author-card:first-child,
.about-authors h1 + .author-card,
.about-authors h2 + .author-card,
.about-the-authors h1 + .author-card,
.about-the-authors h2 + .author-card {
    page-break-before: avoid !important;
    break-before: avoid !important;
    margin-top: 0.4em !important;
    padding-top: 0.4em !important;
}

/* B. CENTER DISPLAY MATH (root cause: block-display math can't be
 *    centered via text-align). Make inner content inline-block so
 *    text-align:center on parent actually centers it.
 *    Also tighten box padding so the formula doesn't sit in an
 *    overly large empty box. */
.math-block,
div.math-block,
.math-display,
div.math-display {
    text-align: center !important;
    padding: 0.5em 0.8em !important;
    margin: 0.6em 0 !important;
}
/* Inner katex/math: inline-block so it can be centered */
.math-block > span,
.math-block > .katex,
.math-block > .katex-display,
.math-block > .katex-rendered,
.math-block > math,
.math-display > span,
.math-display > .katex,
.math-display > .katex-display,
.math-display > math,
.math-block > span.katex.katex-rendered.katex-display,
div.math-block > span.katex.katex-rendered.katex-display {
    display: inline-block !important;
    margin: 0 auto !important;
    text-align: left !important;  /* internal layout stays normal */
    max-width: 100% !important;
}
/* The math element itself, when in display mode */
math[display="block"] {
    display: inline-block !important;
    margin: 0 auto !important;
    text-align: left !important;
    vertical-align: middle !important;
}
/* Tablet/landscape: keep tighter horizontal padding */
.math-block,
div.math-block {
    /* override book.css mobile @media `padding: .8em 1em` and
     * `padding: 1.2em 1.5em` */
    padding: 0.5em 0.8em !important;
}
'''

START = '/* ============================================================\n * v801 — bio splittable'

if START in s:
    idx = s.index(START)
    s = s[:idx].rstrip() + '\n' + ADD
    print('  [v801 block REPLACED]')
else:
    s = s.rstrip() + '\n' + ADD
    print(f'  [v801 block APPENDED ({len(ADD)} chars)]')

overrides.write_text(s, encoding='utf-8')
print(f'  CSS size: {len(s):,} chars')
