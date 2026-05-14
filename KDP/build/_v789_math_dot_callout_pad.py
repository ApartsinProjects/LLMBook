"""v789: Drop the leftover dot/symbol at the right of math + tighten
callout bottom-padding (root cause of the big trailing whitespace
inside boxes like 'Step 2: Implement temperature, top-k...').

A. MATH RIGHT-SIDE GLYPH
   Persists despite v786/v788 scrollbar suppression. Theories tried:
     - Scrollbar thumb (suppressed; symbol still shows)
     - <annotation> text (none in source)
     - <semantics> wrapper renders as glyph on some renderers
   New approach:
     1. Strip <semantics> wrapper from MathML in EPUB (cosmetic; the
        wrapper is a MathML feature for alternate renderings that we
        don't use). Done by post-processor.
     2. Suppress every possible ::after, scrollbar button, scrollbar
        track, scrollbar thumb on math containers + global wildcard.
     3. Set explicit padding-right: 0 on .math-block so there's no
        implicit gap on the right.
     4. Add ::-webkit-scrollbar-button { display: none } since Kindle
        sometimes adds scroll-arrow buttons even when content fits.

B. CALLOUT TRAILING-WHITESPACE BUG
   Visible in 'Step 2: Implement temperature, top-k, and top-p'
   callout: text fills only the top half; bottom 60% of the box is
   empty inside the border. Root cause: the callout has
   `display: flex` + `flex-direction: column` from book.css line 538
   (.section-card), AND the columnar layout in landscape view stretches
   it to the column height.

   Fix: explicitly set display:block + min-height:0 + height:auto on
   every callout (override flex from book.css). For Kindle landscape
   tablet, this guarantees the callout sizes to its content.
"""
from pathlib import Path
import re
import zipfile
import shutil

ROOT = Path(__file__).resolve().parent.parent.parent
overrides = ROOT / 'KDP' / 'build' / 'epub_overrides.css'
s = overrides.read_text(encoding='utf-8')

NEW_BLOCK = '''
/* ============================================================
 * v789 math dot suppression + callout trailing whitespace
 * ============================================================ */

/* MATH right-side glyph: defense-in-depth */
.math-block,
div.math-block,
.math-display,
.katex-display,
.katex-rendered,
.katex,
math,
math *,
.math-block *,
.katex-display * {
    overflow: hidden !important;
    overflow-x: hidden !important;
    overflow-y: hidden !important;
    scrollbar-width: none !important;
    -ms-overflow-style: none !important;
}
.math-block,
.math-display,
.katex-display,
math {
    padding-right: 0 !important;
    padding-left: 0 !important;
    margin-right: 0 !important;
}
/* Suppress every possible ::after / scrollbar artifact */
.math-block::after, .math-block::before,
.math-display::after, .math-display::before,
.katex-display::after, .katex-display::before,
.katex-rendered::after, .katex-rendered::before,
.katex::after, .katex::before,
math::after, math::before,
mrow::after, mrow::before,
semantics::after, semantics::before {
    content: none !important;
    display: none !important;
    visibility: hidden !important;
    width: 0 !important;
    height: 0 !important;
    background: none !important;
}
/* Scrollbar parts (Webkit) */
*::-webkit-scrollbar,
*::-webkit-scrollbar-button,
*::-webkit-scrollbar-thumb,
*::-webkit-scrollbar-track,
*::-webkit-scrollbar-track-piece,
*::-webkit-scrollbar-corner,
*::-webkit-resizer {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
    background: transparent !important;
    visibility: hidden !important;
}
/* Hide MathML semantics text leakage if Kindle shows it */
math semantics > annotation,
math annotation,
math annotation-xml {
    display: none !important;
}

/* ============================================================
 * CALLOUT TRAILING-WHITESPACE: force block (not flex), size to content
 * ============================================================ */
.callout,
div.callout,
aside.callout {
    display: block !important;            /* override any flex from book.css */
    flex: 0 0 auto !important;
    flex-grow: 0 !important;
    flex-shrink: 1 !important;
    height: auto !important;
    min-height: 0 !important;
    max-height: none !important;
    box-sizing: border-box !important;
    /* Tighter vertical padding so single-paragraph boxes don't have
     * extra space below the last line */
    padding-top: 0.55em !important;
    padding-bottom: 0.55em !important;
}
.callout > *:last-child,
.callout > p:last-child,
.callout > div:last-child,
.callout > pre:last-child,
.callout > ul:last-child,
.callout > ol:last-child {
    margin-bottom: 0 !important;
    padding-bottom: 0 !important;
}

/* Lab step cards (the 'Step 2: Implement temperature...' card) had
 * the worst trailing whitespace because they're flex containers
 * stretched to column height. */
.lab-step,
.step-card,
.callout.lab-step,
div.lab-step,
.lab-card,
.callout.lab,
.callout.exercise {
    display: block !important;
    flex: 0 0 auto !important;
    height: auto !important;
    min-height: 0 !important;
    max-height: none !important;
    padding-bottom: 0.55em !important;
}
.lab-step > *:last-child,
.step-card > *:last-child,
.callout.lab > *:last-child,
.callout.exercise > *:last-child {
    margin-bottom: 0 !important;
    padding-bottom: 0 !important;
}
'''

START = '/* ============================================================\n * v789'

if START in s:
    idx = s.index(START)
    s = s[:idx].rstrip() + '\n' + NEW_BLOCK
    print('  [v789 block REPLACED in epub_overrides.css]')
else:
    s = s.rstrip() + '\n' + NEW_BLOCK
    print(f'  [v789 block ADDED to epub_overrides.css ({len(NEW_BLOCK)} chars)]')

overrides.write_text(s, encoding='utf-8')
