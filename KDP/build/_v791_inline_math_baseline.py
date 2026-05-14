"""v791: Fix inline math floating above the text baseline.

ROOT CAUSE
==========
epub_overrides.css line ~1744 applies the following to *every*
`math` element AND every `.katex-rendered` span:

    margin: 0.4em 0 !important;
    padding: 0.2em 0 !important;

This was intended for DISPLAY math (centered block formulas). But
the class `.katex-rendered` is shared between inline and display
math, and the bare `math` selector also matches inline `<math>`.

Consequences for inline math:
  - 0.4em top/bottom margin lifts the inline-block above the line
  - 0.2em vertical padding adds extra height to the wrapper
  - Result: the math span appears to "float" above the surrounding
    text baseline, looking visually disconnected (the reported bug).

FIX
===
Split the rule:
  - DISPLAY math (`.katex-display`, `.math-block`, `.math-display`,
    `math[display="block"]`) keeps the 0.4em margins + 0.2em padding.
  - INLINE math (`.katex-rendered:not(.katex-display)`, bare `math`
    without display="block") gets:
      margin: 0 !important;
      padding: 0 !important;
      vertical-align: baseline !important;
      line-height: inherit !important;

Defense in depth: also force `display: inline` (not inline-block) on
the inline math wrapper, so the baseline alignment uses the parent
line's baseline rather than the inline-block's last-line baseline.

WHY THIS FIXES THE FLOAT
========================
With `display: inline-block` + non-zero margin, the wrapper:
  - Establishes a new inline-block formatting box
  - Its baseline = baseline of its last in-flow line (KaTeX strut)
  - But the 0.4em top margin shifts the entire box up relative to
    the surrounding line
With `display: inline` + zero margin:
  - The wrapper participates directly in the parent line box
  - MathML glyphs sit on the same baseline as surrounding text
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
overrides = ROOT / 'KDP' / 'build' / 'epub_overrides.css'
s = overrides.read_text(encoding='utf-8')

NEW_BLOCK = '''
/* ============================================================
 * v791 INLINE MATH BASELINE FIX
 * ============================================================
 * Root cause: the global rule on `.katex-rendered, math` applies
 * 0.4em margin + 0.2em padding to *every* math element, including
 * inline math. This lifts inline math above the text baseline
 * (the "floating math" bug). Split the rule.
 */

/* 1. Reset inline math to inline + zero margin/padding +
 *    baseline alignment. This must come AFTER the prior block at
 *    line ~1744 to win the cascade. */
.katex-rendered:not(.katex-display),
span.katex-rendered:not(.katex-display),
span.katex.katex-rendered:not(.katex-display),
.katex:not(.katex-display),
math:not([display="block"]) {
    display: inline !important;
    margin: 0 !important;
    padding: 0 !important;
    vertical-align: baseline !important;
    line-height: inherit !important;
    font-size: 1em !important;
}

/* 2. Inline math children: defensive — KaTeX/MathML may wrap content
 *    in inner spans/mrows that also have inline-block. Force them
 *    to inline baseline alignment too. */
.katex-rendered:not(.katex-display) > *,
math:not([display="block"]) > * {
    vertical-align: baseline !important;
    line-height: inherit !important;
}

/* 3. DISPLAY math: re-affirm the original margin/padding (these
 *    are correct for block-level formulas). */
.katex-rendered.katex-display,
span.katex-display,
div.katex-display,
.math-block,
div.math-block,
.math-display,
div.math-display,
math[display="block"] {
    display: block !important;
    margin: 0.6em 0 !important;
    padding: 0.2em 0 !important;
    text-align: center !important;
    vertical-align: baseline !important;
}

/* 4. The inner KaTeX/MathML strut element creates the baseline.
 *    Don't let any vendor sheet override its alignment. */
.katex-rendered .strut,
.katex .strut,
.katex-rendered .vlist-t,
.katex .vlist-t {
    vertical-align: baseline !important;
}

/* 5. Math inside callout text / list items / table cells: same
 *    baseline rule applies (was already partially covered for td/th
 *    in v790, but missing for li and callout body). */
li math:not([display="block"]),
li .katex-rendered:not(.katex-display),
.callout math:not([display="block"]),
.callout .katex-rendered:not(.katex-display),
p math:not([display="block"]),
p .katex-rendered:not(.katex-display) {
    display: inline !important;
    vertical-align: baseline !important;
    margin: 0 !important;
    padding: 0 !important;
}
'''

START = '/* ============================================================\n * v791 INLINE MATH BASELINE'

if START in s:
    idx = s.index(START)
    s = s[:idx].rstrip() + '\n' + NEW_BLOCK
    print('  [v791 block REPLACED in epub_overrides.css]')
else:
    s = s.rstrip() + '\n' + NEW_BLOCK
    print(f'  [v791 block ADDED to epub_overrides.css ({len(NEW_BLOCK)} chars)]')

overrides.write_text(s, encoding='utf-8')
print(f'  size now: {len(s):,} chars')
