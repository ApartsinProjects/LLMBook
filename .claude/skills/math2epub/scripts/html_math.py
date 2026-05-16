"""Plain-HTML math: helpers and CSS for Kindle-safe inline/display math.

Why plain HTML beats SVG and PNG for the LLMBook:
    - No raster: math reflows with body text, scales with font size, stays
      crisp at any zoom level. SVG and PNG are fixed-pixel images.
    - No converter risk: KDP has stripped SVG attributes and data URIs in
      past versions. <i>, <sub>, <sup>, <span>, CSS borders all pass
      through every Kindle conversion pipeline unchanged.
    - Visual weight matches body text. SVG glyphs come out heavier (see
      LESSONS L12). Plain HTML uses the same font family as the surrounding
      prose, so italic `y` reads at the same weight as italic body text.
    - Tiny markup: an inline expression is 20-50 bytes vs 500+ for SVG.
    - Accessibility: screen readers handle <i>y</i><sub>i</sub> natively.

When to fall back to SVG or PNG (rare in the LLMBook):
    - Multi-line aligned equations (linear algebra derivations, multi-step
      proofs). CSS cannot easily replicate align/gather environments.
    - Tensor notation with nested subscripts beyond depth 2.
    - Anything where typographic precision matters more than reflow.

This module exposes:
    HTML_MATH_CSS  : the stylesheet string. Inline into <style> or save as a file.
    var(letter, sub=None, sup=None) : italic variable with optional sub/super
    frac(num, den)                  : two-line CSS fraction
    hat(content)                    : overhat (^)
    bar(content)                    : overbar (-)
    vec(content)                    : overarrow (->)
    sqrt(content)                   : square root with bar over the contents
    sub(content)                    : subscript
    sup(content)                    : superscript
    summation(low=None, high=None)  : Σ with optional limits
    integral(low=None, high=None)   : ∫ with optional limits
    product(low=None, high=None)    : Π with optional limits
    GREEK   : dict of common Greek lowercase / uppercase symbols
    OPS     : dict of common math operators / set-theory symbols
    inline(content) / display(content) : wrap markup as inline or display math
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# Stylesheet. Inline this into <style> or write to a file referenced from <link>.
# ---------------------------------------------------------------------------

HTML_MATH_CSS = """\
/* ----- math2epub plain-HTML math styles --------------------------------- */
/* All measurements are relative (em/percent) so math scales with body text. */

/* Italic variable: the surrounding I tag already does this. Use this class
   to opt out of italic for multi-letter operators like MSE, KL, sin, cos. */
.mvar      { font-style: italic; }
.mop       { font-style: normal; }

/* Subscripts and superscripts. Browser defaults are too cramped at body
   sizes; these overrides give breathing room. */
sub, sup   { line-height: 0; font-size: 0.78em; font-style: normal; }
sub        { vertical-align: -0.30em; }
sup        { vertical-align:  0.55em; }
/* Subscript inside an italic var should also be italic for vars like y_i. */
i sub, i sup,
.mvar sub, .mvar sup { font-style: italic; }

/* CSS fraction: classic inline-block + block-level rows. The block-level
   .num and .den children of an inline-block .frac stack vertically and
   each take the parent's shrink-to-fit width (= max child intrinsic
   width). This pattern is universally supported across every reader
   we test in (Kindle Previewer, Thorium, iBooks, Chrome, Firefox).
   An earlier attempt used `inline-grid` + `grid-template-rows: auto
   auto` but without an explicit `grid-template-columns: 1fr`, the
   default `grid-auto-flow: row` placed both children in row 1 side by
   side instead of stacking; reverting is safer than fighting grid. */
.frac {
    display: inline-block;
    vertical-align: -0.55em;
    margin: 0 0.2em;
    text-align: center;
    line-height: 1.15;
}
.frac > .num {
    display: block;
    border-bottom: 1px solid currentColor;
    padding: 0 0.3em 0.08em;
    font-size: 0.95em;
}
.frac > .den {
    display: block;
    padding: 0.08em 0.3em 0;
    font-size: 0.95em;
}

/* Hat fallback for cases where Unicode pre-composed characters can't be
   used (hat over a fraction, multi-letter variable, etc.). Layout math:
   padding-top reserves a 0.65em strip at the top of the .hat box; the
   :before caret is positioned at top:-0.55em with small font-size and
   small line-height so its glyph occupies y=-0.55em to ~y=0 (rendered
   ENTIRELY above the .hat's content area). For the common single-letter
   case, hat() returns Unicode ŷ etc. directly and this CSS is never hit. */
.hat       { display: inline-block; position: relative; padding-top: 0.65em; }
.hat::before {
    content: "\\02C6";
    position: absolute;
    top: -0.55em;
    left: 0;
    right: 0;
    text-align: center;
    font-size: 0.85em;
    line-height: 0.6;
    font-style: normal;
}

/* Overbar: drawn via top border on a padded span. */
.bar       { display: inline-block; border-top: 1px solid currentColor;
             padding-top: 0.05em; }

/* Overarrow fallback: U+2192 floated above. Same geometry as .hat
   fallback. For the common single-letter case vec() uses the U+20D7
   combining-arrow Unicode form instead. */
.vec       { display: inline-block; position: relative; padding-top: 0.65em; }
.vec::before {
    content: "\\2192";
    position: absolute;
    top: -0.55em;
    left: 0;
    right: 0;
    text-align: center;
    font-size: 0.85em;
    line-height: 0.6;
}

/* Square root: a √ glyph + an overlined radicand that contains ALL its
   children (variables, digits, sub/sup, operators) as one inline atom.
   The radicand uses white-space:nowrap + keep-all + no-hyphens so the
   reader cannot split "b^2 - 4ac" across the radical bar (a bug we hit
   on phi = (1 + sqrt(5)) / 2 where the "5" got broken outside the bar).
   border-top draws the rule tight to the radicand's actual width. */
.sqrt              { display: inline-block; white-space: nowrap; }
.sqrt > .radical   { display: inline-block; vertical-align: top; }
.sqrt > .radicand  {
    display: inline-block;
    white-space: nowrap;
    word-break: keep-all;
    overflow-wrap: normal;
    -webkit-hyphens: none;
    hyphens: none;
    border-top: 1px solid currentColor;
    padding: 0.1em 0.2em 0;
    margin-left: -0.05em;
    vertical-align: top;
}

/* Stacked limits on Σ / ∫ / Π. The big operator sits at body height; the
   low/high limits float above and below in subscript/superscript size. */
.bigop     { display: inline-block; vertical-align: middle; margin: 0 0.15em;
             text-align: center; line-height: 1; }
.bigop > .op  { display: block; font-size: 1.4em; font-style: normal; line-height: 1; }
.bigop > .lo  { display: block; font-size: 0.7em; line-height: 1; }
.bigop > .hi  { display: block; font-size: 0.7em; line-height: 1; }

/* Display (block) math: centered on its own line, with breathing room
   above and below. The combination of white-space:nowrap, word-break:keep-all
   and overflow-wrap:normal blocks every flavor of mid-formula breaking
   the renderer might try (including word-internal hyphenation that was
   breaking 'softmax' across two lines). overflow-x:auto rescues
   equations that genuinely cannot fit. */
.math-display {
    text-align: center;
    margin: 1em auto;
    padding: 0.6em 0;
    line-height: 1.6;
    white-space: nowrap;
    word-break: keep-all;
    overflow-wrap: normal;
    -webkit-hyphens: none;
    hyphens: none;
    overflow-x: auto;
    overflow-y: visible;
}

/* Inline math wrapper. display:inline-block + nowrap + keep-all + no-hyphens
   makes the entire math expression behave as one indivisible atom that
   flows inline with prose but never splits internally, no matter the
   reader's hyphenation settings or column width. */
.math-inline {
    display: inline-block;
    white-space: nowrap;
    word-break: keep-all;
    overflow-wrap: normal;
    -webkit-hyphens: none;
    hyphens: none;
    vertical-align: middle;
}

/* When math appears inside a table cell, give the cell a touch more padding
   so descenders on fractions don't crash into the cell border. */
table .math-inline, table .math-display { padding: 0.1em 0; }

/* Inside a narrow table cell, allow inline math to still flow rather than
   force-overflow the cell: switch to nowrap-but-shrinkable using a wrapper
   pattern. The default rule above wins everywhere else. */
td > .math-inline, th > .math-inline { max-width: 100%; }
"""


# ---------------------------------------------------------------------------
# Atomic builders. All return short HTML strings.
# ---------------------------------------------------------------------------

def var(letter: str, sub: str | None = None, sup: str | None = None) -> str:
    """Italic variable, optionally with subscript and/or superscript."""
    out = f"<i>{letter}</i>"
    if sup is not None:
        out += f"<sup>{sup}</sup>"
    if sub is not None:
        out += f"<sub>{sub}</sub>"
    return out


def op(name: str, sub: str | None = None, sup: str | None = None) -> str:
    """Upright operator (sin, cos, log, MSE, KL...) with optional sub/sup."""
    out = f'<span class="mop">{name}</span>'
    if sup is not None:
        out += f"<sup>{sup}</sup>"
    if sub is not None:
        out += f"<sub>{sub}</sub>"
    return out


def sub(content: str) -> str:
    return f"<sub>{content}</sub>"


def sup(content: str) -> str:
    return f"<sup>{content}</sup>"


def frac(numerator: str, denominator: str) -> str:
    """Two-line CSS fraction. Numerator above, denominator below."""
    return (f'<span class="frac">'
            f'<span class="num">{numerator}</span>'
            f'<span class="den">{denominator}</span>'
            f'</span>')


import re as _re

# Unicode pre-composed circumflex letters. When hat() is called on a single
# italic letter that has a pre-composed form (most ASCII letters do), prefer
# the Unicode character: it always renders correctly across all readers,
# Kindle / Thorium / iBooks / browser. CSS positioning is the fallback for
# letters that lack pre-composed forms AND for complex content (fractions,
# parenthesized groups, etc.).
_HAT_PRECOMPOSED = {
    "a": "â", "A": "Â",   # â Â
    "e": "ê", "E": "Ê",   # ê Ê
    "i": "î", "I": "Î",   # î Î
    "o": "ô", "O": "Ô",   # ô Ô
    "u": "û", "U": "Û",   # û Û
    "y": "ŷ", "Y": "Ŷ",   # ŷ Ŷ
    "c": "ĉ", "C": "Ĉ",   # ĉ Ĉ
    "g": "ĝ", "G": "Ĝ",   # ĝ Ĝ
    "h": "ĥ", "H": "Ĥ",   # ĥ Ĥ
    "j": "ĵ", "J": "Ĵ",   # ĵ Ĵ
    "s": "ŝ", "S": "Ŝ",   # ŝ Ŝ
    "w": "ŵ", "W": "Ŵ",   # ŵ Ŵ
    "z": "ẑ", "Z": "Ẑ",   # ẑ Ẑ
}

# Macron (bar) pre-composed letters
_BAR_PRECOMPOSED = {
    "a": "ā", "A": "Ā",   # ā Ā
    "e": "ē", "E": "Ē",   # ē Ē
    "i": "ī", "I": "Ī",   # ī Ī
    "o": "ō", "O": "Ō",   # ō Ō
    "u": "ū", "U": "Ū",   # ū Ū
    "x": "x̄", "X": "X̄",   # x̄ X̄ (combining macron)
    "y": "ȳ", "Y": "Ȳ",   # ȳ Ȳ
}


_SIMPLE_LETTER_RE = _re.compile(r"^<i>([a-zA-Z])</i>$")


def hat(content: str) -> str:
    """Overhat (circumflex) on the given content.

    Uses Unicode pre-composed characters when possible (ŷ, ẑ, etc.) because
    they render correctly in every EPUB reader without CSS gymnastics. Falls
    back to CSS-positioned ::before for letters without pre-composed forms
    and for complex content like hat over a fraction.

    Examples:
        hat(var("y"))         -> <i>ŷ</i>          (Unicode)
        hat(frac("1", "n"))   -> <span class="hat"><span class="frac">...
    """
    m = _SIMPLE_LETTER_RE.match(content)
    if m and m.group(1) in _HAT_PRECOMPOSED:
        return f"<i>{_HAT_PRECOMPOSED[m.group(1)]}</i>"
    return f'<span class="hat">{content}</span>'


def bar(content: str) -> str:
    """Overbar (macron) on the given content. Use for sample means: bar(x).

    Uses Unicode pre-composed characters for letters that have them, falls
    back to CSS for arbitrary content.
    """
    m = _SIMPLE_LETTER_RE.match(content)
    if m and m.group(1) in _BAR_PRECOMPOSED:
        return f"<i>{_BAR_PRECOMPOSED[m.group(1)]}</i>"
    return f'<span class="bar">{content}</span>'


def vec(content: str) -> str:
    """Overarrow on the given content. Use for vectors: vec(v).

    Uses Unicode combining right-arrow above (U+20D7) when content is a
    single ASCII letter, falls back to CSS otherwise. The combining mark
    renders as an arrow positioned directly above the preceding character
    in any reader that supports basic combining diacritics.
    """
    m = _SIMPLE_LETTER_RE.match(content)
    if m:
        # Letter + COMBINING RIGHT ARROW ABOVE
        return f"<i>{m.group(1)}⃗</i>"
    return f'<span class="vec">{content}</span>'


def sqrt(radicand: str) -> str:
    """Square root: a √ glyph followed by the radicand with an overline."""
    return (f'<span class="sqrt">'
            f'<span class="radical">&#8730;</span>'
            f'<span class="radicand">{radicand}</span>'
            f'</span>')


def bigop_(symbol: str, low: str | None, high: str | None) -> str:
    """Stacked limits on a big operator symbol (Σ, ∫, Π)."""
    lo_html = f'<span class="lo">{low}</span>' if low else ''
    hi_html = f'<span class="hi">{high}</span>' if high else ''
    return (f'<span class="bigop">'
            f'{hi_html}'
            f'<span class="op">{symbol}</span>'
            f'{lo_html}'
            f'</span>')


def summation(low: str | None = None, high: str | None = None) -> str:
    """Σ with optional stacked limits."""
    return bigop_("&#931;", low, high)


def integral(low: str | None = None, high: str | None = None) -> str:
    """∫ with optional stacked limits."""
    return bigop_("&#8747;", low, high)


def product(low: str | None = None, high: str | None = None) -> str:
    """Π with optional stacked limits."""
    return bigop_("&#928;", low, high)


def inline(content: str) -> str:
    """Wrap content as inline math (no-wrap, scoped class)."""
    return f'<span class="math-inline">{content}</span>'


def display(content: str) -> str:
    """Wrap content as a display-math block (centered, own line)."""
    return f'<div class="math-display">{content}</div>'


# ---------------------------------------------------------------------------
# Greek alphabet and common operator / set-theory symbols.
# All values are literal Unicode characters (XHTML-safe, no entity refs needed).
# Numeric character references are an alternative if a file needs ASCII-safe
# bytes; the values here are the actual glyphs.
# ---------------------------------------------------------------------------

GREEK = {
    # Lowercase
    "alpha":   "α", "beta":    "β", "gamma":   "γ",
    "delta":   "δ", "epsilon": "ε", "zeta":    "ζ",
    "eta":     "η", "theta":   "θ", "iota":    "ι",
    "kappa":   "κ", "lambda":  "λ", "mu":      "μ",
    "nu":      "ν", "xi":      "ξ", "pi":      "π",
    "rho":     "ρ", "sigma":   "σ", "tau":     "τ",
    "upsilon": "υ", "phi":     "φ", "chi":     "χ",
    "psi":     "ψ", "omega":   "ω",
    # Uppercase
    "Alpha":   "Α", "Beta":    "Β", "Gamma":   "Γ",
    "Delta":   "Δ", "Epsilon": "Ε", "Zeta":    "Ζ",
    "Eta":     "Η", "Theta":   "Θ", "Iota":    "Ι",
    "Kappa":   "Κ", "Lambda":  "Λ", "Mu":      "Μ",
    "Nu":      "Ν", "Xi":      "Ξ", "Pi":      "Π",
    "Rho":     "Ρ", "Sigma":   "Σ", "Tau":     "Τ",
    "Upsilon": "Υ", "Phi":     "Φ", "Chi":     "Χ",
    "Psi":     "Ψ", "Omega":   "Ω",
}


OPS = {
    # Binary arithmetic
    "times":     "×",  # ×
    "div":       "÷",  # ÷
    "cdot":      "⋅",  # ⋅
    "pm":        "±",  # ±
    "mp":        "∓",  # ∓
    "minus":     "−",  # − (typographic minus, not hyphen)
    # Relations
    "equals":    "=",
    "neq":       "≠",  # ≠
    "approx":    "≈",  # ≈
    "equiv":     "≡",  # ≡
    "propto":    "∝",  # ∝
    "leq":       "≤",  # ≤
    "geq":       "≥",  # ≥
    "ll":        "≪",  # ≪
    "gg":        "≫",  # ≫
    # Set theory
    "in":        "∈",  # ∈
    "notin":     "∉",  # ∉
    "subset":    "⊂",  # ⊂
    "subseteq":  "⊆",  # ⊆
    "supset":    "⊃",  # ⊃
    "supseteq":  "⊇",  # ⊇
    "union":     "∪",  # ∪
    "intersect": "∩",  # ∩
    "emptyset":  "∅",  # ∅
    # Logic
    "land":      "∧",  # ∧
    "lor":       "∨",  # ∨
    "lnot":      "¬",  # ¬
    "forall":    "∀",  # ∀
    "exists":    "∃",  # ∃
    # Calculus / analysis
    "partial":   "∂",  # ∂
    "nabla":     "∇",  # ∇
    "infty":     "∞",  # ∞
    "to":        "→",  # →
    "leftarrow": "←",  # ←
    "mapsto":    "↦",  # ↦
    "iff":       "⇔",  # ⇔
    # Number sets
    "naturals":  "ℕ",  # ℕ
    "integers":  "ℤ",  # ℤ
    "rationals": "ℚ",  # ℚ
    "reals":     "ℝ",  # ℝ
    "complex":   "ℂ",  # ℂ
    # Dots
    "ldots":     "…",  # …
    "cdots":     "⋯",  # ⋯
}
