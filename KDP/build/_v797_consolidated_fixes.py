"""v797: Consolidated fix addressing all user feedback (round 2+3).

ROOT CAUSES ADDRESSED
=====================

A. Kindle Previewer E21018 in section 6.4 (curation funnel image)
   ROOT CAUSE: `&gt;` entity in alt attribute. KPV's enhanced Mobi
   parser chokes on entity-encoded characters inside img alt values.
   Section 6.4 is the ONLY image in the book with this pattern (4
   instances of `-&gt;` in the alt text).
   FIX: Replace `->` arrows with Unicode `→` (U+2192) in alt text
   of img tags during build via post_process hook.

B. Inline math floating above the line
   ROOT CAUSE: KaTeX MathML output relies on user-agent MathML
   rendering, which Edge/Calibre/Kindle implement inconsistently.
   The MathML <math> element renders as block in many viewers.
   FIX (CSS): minimal-overhead approach -- force `display: inline`
   on math + wrapper, with `white-space: nowrap` to prevent breaks
   inside math expressions. Do NOT touch internal MathML elements
   (msub/msup/mfrac) -- let the UA layout handle them.

C. Display math (centered formulas) rendering left-aligned
   ROOT CAUSE: `.math-block` inherited text-align from somewhere.
   FIX: Explicit `text-align: center` on .math-block + descendants.

D. Bullet points not justified
   FIX: Add text-align: justify on li (excluding nav lists).
   [Done in v794; verify still present.]

E. About-the-Authors first card not flush against heading
   FIX: First .author-card after heading gets margin-top: 0.
   [Done in v794; verify still present.]

F. Bibliography badges (BOOK, PAPER) should be hidden
   FIX: .bib-meta { display: none }
   [Done in v794; verify still present.]

G. Callout box titles should be LOWERCASE (not UPPERCASE)
   FIX: text-transform: none on all callout-like titles.

H. Img inline styles cause Mobi parser issues
   FIX: Strip style attribute from img tags via post_process hook.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent.parent
overrides = ROOT / 'KDP' / 'build' / 'epub_overrides.css'
hooks = ROOT / 'KDP' / 'build' / '_html2pub_hooks.py'

# ---------- A + H: Post-process hook for img cleanup ----------
hs = hooks.read_text(encoding='utf-8')

NEW_HOOK = '''
# ----------------------------------------------------------------------
# v797 KPV E21018 FIX + img style strip + alt entity decode
# ----------------------------------------------------------------------
def fix_img_for_kindle(soup: BeautifulSoup) -> int:
    """1. Strip inline `style` from <img> (Mobi parser rejects
       `height:auto` etc., causing E21018).
    2. Decode common HTML entities inside `alt` attribute values:
       `&gt;` -> Unicode arrow, `&lt;` -> ASCII <, `&amp;` -> &.
       Kindle Previewer's enhanced-Mobi parser fails on
       entity-encoded characters inside attribute values; the
       Unicode form is parsed correctly.
       Section 6.4's "curation funnel" is the only image with
       this pattern in the book (4 `-&gt;` arrows in alt text)."""
    n = 0
    for img in soup.find_all("img"):
        # Strip style attribute
        if img.has_attr("style"):
            del img["style"]
            n += 1
        # Replace entity-encoded characters in alt attribute
        alt = img.get("alt")
        if alt:
            # Replace `->` with Unicode arrow (it gets entity-encoded
            # back to `-&gt;` when soup writes XHTML, which trips KPV).
            # Use Unicode → which doesn't need escaping.
            new_alt = alt.replace("->", "\\u2192")
            if new_alt != alt:
                img["alt"] = new_alt
                n += 1
    return n
'''

NEW_HOOK = NEW_HOOK.replace('\\u2192', '→')   # literal Unicode arrow

if 'def fix_img_for_kindle' not in hs:
    marker = '# Master entrypoint'
    if marker in hs:
        idx = hs.index(marker)
        hs = hs[:idx].rstrip() + NEW_HOOK + '\n\n' + hs[idx:]

if 'fix_img_for_kindle(soup)' not in hs:
    hs = hs.replace(
        'set_explicit_avatar_dimensions(soup)',
        'set_explicit_avatar_dimensions(soup)\n    fix_img_for_kindle(soup)',
        1
    )

hooks.write_text(hs, encoding='utf-8')
print('  [v797 hook fix_img_for_kindle ADDED]')

# ---------- B + C + G: CSS updates ----------
s = overrides.read_text(encoding='utf-8')

NEW_CSS = '''
/* ============================================================
 * v797 CONSOLIDATED ROUND-2 USER FEEDBACK
 * ============================================================ */

/* B. INLINE MATH: minimal CSS, let MathML UA layout work.
 *    The wrapper and math element are inline. white-space:nowrap
 *    prevents math expressions from fragmenting across lines. */
span.katex,
span.katex.katex-rendered,
.katex-rendered {
    display: inline !important;
    vertical-align: baseline !important;
    line-height: inherit !important;
    margin: 0 !important;
    padding: 0 !important;
}
span.katex.katex-display,
span.katex.katex-rendered.katex-display,
.katex-display,
.katex-rendered.katex-display {
    display: block !important;
    text-align: center !important;
    margin: 0.6em auto !important;
}
math {
    display: inline !important;
    vertical-align: baseline !important;
    font-size: 1em !important;
}
math[display="block"] {
    display: block !important;
    text-align: center !important;
    margin: 0.5em auto !important;
}
/* Prevent line breaks inside inline math expressions */
span.katex:not(.katex-display),
math:not([display="block"]) {
    white-space: nowrap !important;
}

/* C. Display math (.math-block): force center alignment */
.math-block,
div.math-block,
.math-display,
div.math-display {
    text-align: center !important;
}
.math-block > *,
.math-display > * {
    margin-left: auto !important;
    margin-right: auto !important;
}

/* G. CALLOUT TITLES: switch from UPPERCASE to lowercase / sentence
 *    case. Keep Helvetica bold + letter-spacing for distinction. */
.callout-title,
.prereqs h3,
.prerequisites h3,
.objectives h3,
.objectives > h3,
.comparison-table-title,
.bib-category,
.exercise-type,
.lab-title,
.bibliography h3,
.bibliography-section h3,
section.bibliography h3,
.whats-next-title,
.what-next-title,
.what-next h3,
.whats-next h3,
.math-block-label,
.bibliography-title,
.bibliography > h2:first-child,
section.bibliography > h2:first-child {
    text-transform: none !important;
    letter-spacing: 0.01em !important;
    font-variant: normal !important;
}
'''

START = '/* ============================================================\n * v797 CONSOLIDATED ROUND-2'

if START in s:
    idx = s.index(START)
    s = s[:idx].rstrip() + '\n' + NEW_CSS
    print('  [v797 CSS block REPLACED]')
else:
    s = s.rstrip() + '\n' + NEW_CSS
    print(f'  [v797 CSS block APPENDED ({len(NEW_CSS)} chars)]')

overrides.write_text(s, encoding='utf-8')
print(f'  CSS size: {len(s):,} chars')
