"""v802: Replace simple inline MathML with plain HTML sub/sup tags.

ROOT CAUSE (confirmed by user: "each math symbol cause new line")
==================================================================
Every EPUB reader I've tested (Thorium, Calibre, Edge headless print,
Kindle KFX) renders inline <math> elements with vertical extent
larger than line-height. The result: each math symbol triggers a
line break before AND after, creating output like:

    where
    p_i
    is the model's predicted probability...

Or worse, in numbered lists:

    1. Split the data into
    K
    equal folds.

CSS fixes don't work (display:inline doesn't override the renderer's
MathML layout module). The fundamental issue is that <math> elements
are rendered by a separate engine that doesn't fully honor inline
flow.

FIX
===
Add a post-process hook that REPLACES simple inline MathML wrappers
with plain HTML using <sub> and <sup> tags. Patterns handled:
  - <math><mrow><mi>K</mi></mrow></math>          → K
  - <math><mrow><msub><mi>p</mi><mi>i</mi></msub></mrow></math> → p<sub>i</sub>
  - <math><mrow><msup><mi>x</mi><mn>2</mn></msup></mrow></math> → x<sup>2</sup>
  - <math><mrow><msubsup>...</msubsup></mrow></math> → x<sub>i</sub><sup>2</sup>

Complex MathML (fractions, sums, integrals, matrices) is LEFT alone
as MathML — readers handle these differently and full block-style
rendering is appropriate for them anyway.

The new hook runs in fix_math_alignment AFTER math rendering and
AFTER <semantics> unwrapping.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
hooks_path = ROOT / 'KDP/build/_html2pub_hooks.py'
hs = hooks_path.read_text(encoding='utf-8')

INSERT_AFTER = '    for sem in soup.find_all("semantics"):\n        sem.unwrap()'

NEW_CODE = '''
    # v13.5: Convert simple inline MathML to plain HTML sub/sup.
    # Inline <math> elements with single-letter or letter+sub/sup
    # patterns get replaced with <span><sub>i</sub></span>-style
    # markup. Eliminates line-break-around-math bug in EPUB readers
    # that treat <math> as block-level.
    n_simplified = simplify_inline_mathml(soup)
'''

if 'simplify_inline_mathml(soup)' not in hs:
    hs = hs.replace(INSERT_AFTER, INSERT_AFTER + NEW_CODE)
    print('  [v802 wired simplify_inline_mathml into fix_math_alignment]')

# Add the simplify function just before fix_math_alignment
FUNC_DEF = '''
def simplify_inline_mathml(soup: BeautifulSoup) -> int:
    """Replace simple inline <math> wrappers with plain HTML sub/sup.
    Returns count of replacements made.

    Patterns handled (inline only -- display math is left alone):
      <math><mrow><mi>K</mi></mrow></math>                → K
      <math><mrow><mi>K</mi><mi>i</mi></mrow></math>      → Ki (rare)
      <math><mrow><msub>...</msub></mrow></math>          → x<sub>i</sub>
      <math><mrow><msup>...</msup></mrow></math>          → x<sup>2</sup>
      <math><mrow><msubsup>...</msubsup></mrow></math>    → x<sub>i</sub><sup>2</sup>

    The replacement is a plain <span class="inline-math"> wrapping
    HTML <sub>/<sup>. The original wrapper class (katex-rendered)
    is removed so the EPUB reader treats it as normal inline text
    with proper line flow.
    """
    from bs4 import NavigableString

    n = 0

    def render_token(tok):
        """Return text content of <mi>, <mn>, <mo>, etc. as str."""
        if tok is None:
            return None
        name = getattr(tok, "name", None)
        if name in ("mi", "mn", "mo", "ms", "mtext"):
            return tok.get_text()
        return None

    def convert_mrow(mrow):
        """If mrow content is simple enough, return a list of
        NavigableString / Tag pieces. Otherwise return None."""
        children = [c for c in mrow.children if getattr(c, "name", None)]
        if not children:
            return None
        pieces = []
        for c in children:
            name = c.name
            if name in ("mi", "mn", "mo", "ms", "mtext"):
                t = c.get_text()
                if t:
                    pieces.append(NavigableString(t))
            elif name == "msub":
                ch = [x for x in c.children if getattr(x, "name", None)]
                if len(ch) != 2:
                    return None
                base_text = render_token(ch[0])
                sub_text = render_token(ch[1])
                if base_text is None or sub_text is None:
                    return None
                if base_text:
                    pieces.append(NavigableString(base_text))
                sub_tag = soup.new_tag("sub")
                sub_tag.string = sub_text
                pieces.append(sub_tag)
            elif name == "msup":
                ch = [x for x in c.children if getattr(x, "name", None)]
                if len(ch) != 2:
                    return None
                base_text = render_token(ch[0])
                sup_text = render_token(ch[1])
                if base_text is None or sup_text is None:
                    return None
                if base_text:
                    pieces.append(NavigableString(base_text))
                sup_tag = soup.new_tag("sup")
                sup_tag.string = sup_text
                pieces.append(sup_tag)
            elif name == "msubsup":
                ch = [x for x in c.children if getattr(x, "name", None)]
                if len(ch) != 3:
                    return None
                base_text = render_token(ch[0])
                sub_text = render_token(ch[1])
                sup_text = render_token(ch[2])
                if any(t is None for t in (base_text, sub_text, sup_text)):
                    return None
                if base_text:
                    pieces.append(NavigableString(base_text))
                sub_tag = soup.new_tag("sub")
                sub_tag.string = sub_text
                pieces.append(sub_tag)
                sup_tag = soup.new_tag("sup")
                sup_tag.string = sup_text
                pieces.append(sup_tag)
            else:
                # Unknown / complex element (mfrac, msqrt, mover, mtable...)
                return None
        return pieces

    for math in list(soup.find_all("math")):
        # Skip display math
        if math.get("display") == "block":
            continue
        # Walk inside mrow
        mrow = math.find("mrow")
        if mrow is None:
            mrow = math
        pieces = convert_mrow(mrow)
        if pieces is None:
            continue   # too complex, keep MathML
        # Find the enclosing wrapper span (.katex.katex-rendered)
        wrapper = math.parent
        if wrapper is None or wrapper.name != "span":
            wrapper = math
        # Replace wrapper with a plain span containing the pieces
        new_span = soup.new_tag("span")
        new_span["class"] = ["inline-math"]
        for p in pieces:
            new_span.append(p)
        wrapper.replace_with(new_span)
        n += 1

    return n


'''

# Insert the function definition BEFORE fix_math_alignment
if 'def simplify_inline_mathml' not in hs:
    marker = 'def fix_math_alignment'
    if marker in hs:
        idx = hs.index(marker)
        hs = hs[:idx] + FUNC_DEF + hs[idx:]
        print('  [v802 simplify_inline_mathml function ADDED]')

hooks_path.write_text(hs, encoding='utf-8')

# Add CSS for .inline-math wrapper (defensive — also bookwide)
overrides = ROOT / 'KDP/build/epub_overrides.css'
s = overrides.read_text(encoding='utf-8')

CSS_ADD = '''
/* ============================================================
 * v13.5 INLINE-MATH WRAPPER (replacement for MathML)
 * ============================================================
 * Simple inline math (p_i, x^2, K) is converted to plain HTML by
 * the simplify_inline_mathml hook. The replacement span uses
 * standard <sub>/<sup> tags which render correctly inline in
 * every EPUB reader. */
span.inline-math {
    display: inline !important;
    white-space: nowrap !important;
    vertical-align: baseline !important;
    font-family: "Cambria Math", "Times New Roman", serif !important;
    font-style: italic !important;
}
span.inline-math sub,
span.inline-math sup {
    font-style: normal !important;
    font-size: 0.75em !important;
    line-height: 0 !important;
}
span.inline-math sub {
    vertical-align: sub !important;
}
span.inline-math sup {
    vertical-align: super !important;
}

'''

if 'INLINE-MATH WRAPPER' not in s:
    s = s.rstrip() + '\n' + CSS_ADD
    overrides.write_text(s, encoding='utf-8')
    print('  [v802 CSS for .inline-math added]')

print('  Done.')
