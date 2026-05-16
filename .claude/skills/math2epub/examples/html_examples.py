"""Comprehensive plain-HTML math examples.

Produces math-html-examples.html (browser) and math-html-examples.epub
(Kindle Previewer 3) exercising every category of HTML math the
LLMBook needs:

    1. Inline math threaded through prose
    2. Display equations (centered, own line)
    3. Math inside a table
    4. Formula gallery: 12 staple ML / probability / calculus formulas
    5. Reference: Greek alphabet and operator inventory
    6. Subtle typography cases: stacked subscripts, hat over fraction,
       multi-character operators (sin, MSE, KL), bracket grouping
"""
from __future__ import annotations

import sys
import uuid
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

from html_math import (  # noqa: E402
    HTML_MATH_CSS,
    GREEK, OPS,
    var, op, frac, hat, bar, vec, sqrt,
    summation, integral, product,
    inline, display, sub, sup,
)

# Write to the project's main output folder when running inside the
# LLMBook repo, otherwise fall back to a local demo-output subdir.
def _resolve_out_dir() -> Path:
    candidate = HERE
    for _ in range(6):
        if (candidate / "KDP" / "output").is_dir():
            return candidate / "KDP" / "output"
        candidate = candidate.parent
    return HERE / "demo-output"

OUT_DIR = _resolve_out_dir()
OUT_DIR.mkdir(parents=True, exist_ok=True)


# Shorthand bindings used heavily below.
y, x, n, i, j, k = (var(c) for c in "yxnijk")
yh = hat(var("y"))             # ŷ
yh_i = hat(var("y")) + sub(var("i"))   # ŷᵢ (positioned via CSS)
y_i = var("y", sub="i")
x_i = var("x", sub="i")
mu = GREEK["mu"]
sigma = GREEK["sigma"]
theta = GREEK["theta"]
alpha = GREEK["alpha"]
beta = GREEK["beta"]
gamma = GREEK["gamma"]
eta = GREEK["eta"]
pi_l = GREEK["pi"]
Sigma = GREEK["Sigma"]
Theta_u = GREEK["Theta"]
PROPTO = OPS["propto"]
APPROX = OPS["approx"]
NEQ = OPS["neq"]
IN = OPS["in"]
TIMES = OPS["times"]
CDOT = OPS["cdot"]
PARTIAL = OPS["partial"]
NABLA = OPS["nabla"]
INFTY = OPS["infty"]
PM = OPS["pm"]
TO = OPS["to"]
LEQ = OPS["leq"]
GEQ = OPS["geq"]
SUM = summation        # convenience alias
INT = integral


# ============================================================================
# Section 1: Inline math in prose
# ============================================================================
PROSE_HTML = f"""
<h2>1. Inline math in prose</h2>
<p>The output of a model for the {inline(f'{i}-th')} example is written
{inline(y_i)}, and its prediction is {inline(yh + sub('i'))}. The training set
consists of {inline(n)} examples, indexed by {inline(i)} = 1, 2, &#8230;, {inline(n)}.
Each example contributes a residual {inline(yh + sub('i') + ' &#8722; ' + y_i)}
which we square before averaging.</p>

<p>For a binary classifier we model the probability of the positive class as
{inline(f'P({var("y")} = 1 | {var("x")}) = {sigma}({var("z")})')}, where
{inline(sigma)} is the sigmoid and {inline(var("z"))} is the pre-activation
{inline(f'{var("w")}{sup("T")}{var("x")} + {var("b")}')}.
Multi-class generalizes via softmax: the probability of class {inline(k)} is
proportional to {inline('e' + sup(var('z') + sub('k')))}, normalized by
{inline(SUM(low='j') + ' e' + sup(var('z') + sub('j')))}.</p>

<p>Gradient descent updates parameters by {inline(theta + sub('t+1') + ' = '
+ theta + sub('t') + ' &#8722; ' + eta + ' ' + NABLA + ' ' + var('L') + '(' + theta + sub('t') + ')')},
where {inline(eta)} is the learning rate and {inline(NABLA + ' ' + var('L'))} is
the gradient of the loss with respect to {inline(theta)}.</p>

<p>Two events {inline(var('A'))} and {inline(var('B'))} are independent when
{inline(f'P({var("A")} {IN} {var("B")}) = P({var("A")}){CDOT}P({var("B")})')}.
The conditional probability of {inline(var('A'))} given {inline(var('B'))} is
{inline(f'P({var("A")} | {var("B")}) = ' + frac(f'P({var("A")} {IN} {var("B")})', f'P({var("B")})'))}.</p>
"""


# ============================================================================
# Section 2: Display equations
# ============================================================================
DISPLAY_HTML = f"""
<h2>2. Display equations</h2>

<p>Mean squared error, written as a centered display equation:</p>
{display(op('MSE') + ' = ' + frac('1', n) + ' ' + SUM(low=f'{i}=1', high=n)
         + ' (' + yh + sub('i') + ' &#8722; ' + y_i + ')' + sup('2'))}

<p>The sigmoid activation:</p>
{display(sigma + '(' + var('x') + ') = ' + frac('1', f'1 + e{sup("&#8722;" + var("x"))}'))}

<p>Scaled dot-product attention, the heart of the transformer:</p>
{display(op('Attention') + '(' + var('Q') + ', ' + var('K') + ', ' + var('V') + ') = '
         + op('softmax') + '&#8202;'
         + '(' + frac(var('Q') + var('K') + sup('T'), sqrt(var('d') + sub('k'))) + ')'
         + ' ' + var('V'))}

<p>The quadratic formula:</p>
{display(var('x') + ' = '
         + frac('&#8722;' + var('b') + ' ' + PM + ' ' + sqrt(var('b') + sup('2') + ' &#8722; 4' + var('a') + var('c')),
                '2' + var('a')))}
"""


# ============================================================================
# Section 3: Math in a table
# ============================================================================
TABLE_HTML = f"""
<h2>3. Math inside a table</h2>
<p>Tables let you compare loss functions and their derivatives side by side.
Math survives the cell-level layout without expanding to fill the cell,
because plain HTML has no intrinsic image dimensions to fight.</p>

<table>
<thead>
<tr><th>Name</th><th>Formula</th><th>Derivative</th></tr>
</thead>
<tbody>
<tr>
  <td>L1 / MAE</td>
  <td>{inline(var('L') + ' = ' + frac('1', n) + ' ' + SUM(low=f'{i}=1', high=n)
              + ' |' + yh + sub('i') + ' &#8722; ' + y_i + '|')}</td>
  <td>{inline(PARTIAL + var('L') + ' / ' + PARTIAL + yh + sub('i') + ' = '
              + op('sign') + '(' + yh + sub('i') + ' &#8722; ' + y_i + ')')}</td>
</tr>
<tr>
  <td>L2 / MSE</td>
  <td>{inline(var('L') + ' = ' + frac('1', n) + ' ' + SUM(low=f'{i}=1', high=n)
              + ' (' + yh + sub('i') + ' &#8722; ' + y_i + ')' + sup('2'))}</td>
  <td>{inline(PARTIAL + var('L') + ' / ' + PARTIAL + yh + sub('i') + ' = '
              + frac('2', n) + ' (' + yh + sub('i') + ' &#8722; ' + y_i + ')')}</td>
</tr>
<tr>
  <td>Cross-entropy</td>
  <td>{inline(var('L') + ' = &#8722;' + SUM(low=f'{i}=1', high=n) + ' ' + y_i
              + ' ' + op('log') + ' ' + yh + sub('i'))}</td>
  <td>{inline(PARTIAL + var('L') + ' / ' + PARTIAL + yh + sub('i') + ' = '
              + '&#8722;' + frac(y_i, yh + sub('i')))}</td>
</tr>
<tr>
  <td>Huber ({inline(f'|{yh}{sub("i")} &#8722; {y_i}| {LEQ} {GREEK["delta"]}')})</td>
  <td>{inline(var('L') + ' = ' + frac('1', '2')
              + ' (' + yh + sub('i') + ' &#8722; ' + y_i + ')' + sup('2'))}</td>
  <td>{inline(yh + sub('i') + ' &#8722; ' + y_i)}</td>
</tr>
</tbody>
</table>
"""


# ============================================================================
# Section 4: Formula gallery
# ============================================================================
def formula_card(title: str, formula_html: str, description: str = "") -> str:
    return f"""
<div class="formula-card">
  <div class="formula-title">{title}</div>
  {display(formula_html)}
  {('<p class="formula-note">' + description + '</p>') if description else ''}
</div>
"""


FORMULAS = [
    ("Sigmoid",
     sigma + '(' + var('x') + ') = ' + frac('1', f'1 + e{sup("&#8722;" + var("x"))}'),
     "Squashes any real number into the open interval (0, 1)."),

    ("Softmax (k-th output)",
     sigma + '(' + var('z') + ')' + sub('k') + ' = '
     + frac(f'e{sup(var("z") + sub("k"))}',
            SUM(low='j=1', high='K') + ' e' + sup(var('z') + sub('j'))),
     "Generalizes sigmoid to K classes. Each output lies in (0, 1) and the K outputs sum to 1."),

    ("Tanh",
     op('tanh') + '(' + var('x') + ') = '
     + frac(f'e{sup(var("x"))} &#8722; e{sup("&#8722;" + var("x"))}',
            f'e{sup(var("x"))} + e{sup("&#8722;" + var("x"))}'),
     "Squashes to (&#8722;1, 1). Zero-centered, unlike sigmoid."),

    ("ReLU",
     op('ReLU') + '(' + var('x') + ') = ' + op('max') + '(0, ' + var('x') + ')',
     "Identity for positive inputs, zero otherwise. The workhorse activation of modern deep nets."),

    ("Cross-entropy loss",
     var('L') + ' = &#8722;' + frac('1', n)
     + ' ' + SUM(low=f'{i}=1', high=n)
     + ' ' + SUM(low='k=1', high='K') + ' ' + y_i + sub('k')
     + ' ' + op('log') + ' ' + yh + sub('i') + sub('k'),
     "Multi-class classification objective. The negative log-likelihood of the correct class."),

    ("Adam update",
     theta + sub('t+1') + ' = ' + theta + sub('t')
     + ' &#8722; ' + frac(eta + ' ' + hat('m') + sub('t'),
                          sqrt(hat('v') + sub('t')) + ' + ' + GREEK['epsilon']),
     "Adaptive learning rate per parameter, using running estimates of the first and second moments of the gradient."),

    ("Layer normalization",
     hat(var('x')) + sub('i') + ' = ' + frac(x_i + ' &#8722; ' + mu, sqrt(sigma + sup('2') + ' + ' + GREEK['epsilon'])),
     "Normalizes each input across feature dimensions to zero mean and unit variance, then applies a learned affine."),

    ("Scaled dot-product attention",
     op('Attention') + '(' + var('Q') + ', ' + var('K') + ', ' + var('V') + ') = '
     + op('softmax') + '(' + frac(var('Q') + var('K') + sup('T'), sqrt(var('d') + sub('k'))) + ') ' + var('V'),
     "Transformer attention. Scaling by &#8730;d&#8342; keeps the softmax in a useful range as dimensionality grows."),

    ("KL divergence",
     op('KL') + '(' + var('P') + ' || ' + var('Q') + ') = '
     + SUM(low='x') + ' ' + var('P') + '(' + var('x') + ') ' + op('log')
     + ' ' + frac(var('P') + '(' + var('x') + ')', var('Q') + '(' + var('x') + ')'),
     "Asymmetric measure of how much distribution Q diverges from a reference P. Never negative; zero iff P = Q."),

    ("Bayes' theorem",
     var('P') + '(' + var('A') + ' | ' + var('B') + ') = '
     + frac(var('P') + '(' + var('B') + ' | ' + var('A') + ') ' + var('P') + '(' + var('A') + ')',
            var('P') + '(' + var('B') + ')'),
     "Posterior is proportional to likelihood times prior."),

    ("Gaussian density",
     op('p') + '(' + var('x') + ') = ' + frac('1', sqrt('2' + pi_l) + ' ' + sigma)
     + ' e' + sup('&#8722;' + frac('(' + var('x') + ' &#8722; ' + mu + ')' + sup('2'),
                                   '2' + sigma + sup('2'))),
     "Univariate normal distribution with mean &#956; and standard deviation &#963;."),

    ("Expectation of a function of X",
     op('E') + '[' + var('f') + '(' + var('X') + ')] = '
     + INT(low='&#8722;' + INFTY, high=INFTY) + ' ' + var('f') + '(' + var('x') + ') '
     + op('p') + '(' + var('x') + ') ' + var('dx'),
     "Linear operator. For a discrete X, replace the integral with a sum."),
]


GALLERY_HTML = (
    "<h2>4. Formula gallery</h2>\n"
    "<p>Twelve common formulas, each rendered as a display block. "
    "Every formula uses only plain HTML and the CSS in <code>html_math.py</code>.</p>\n"
    + "\n".join(formula_card(t, f, d) for t, f, d in FORMULAS)
)


# ============================================================================
# Section 5: Reference inventories (Greek + operators)
# ============================================================================
def greek_table() -> str:
    pairs = [
        ("Lowercase",
         ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta",
          "iota", "kappa", "lambda", "mu", "nu", "xi", "pi", "rho", "sigma",
          "tau", "upsilon", "phi", "chi", "psi", "omega"]),
        ("Uppercase",
         ["Gamma", "Delta", "Theta", "Lambda", "Xi", "Pi", "Sigma", "Phi",
          "Psi", "Omega"]),
    ]
    rows = []
    for header, names in pairs:
        cells = " ".join(
            f'<td><span class="ref-glyph">{GREEK[n]}</span> '
            f'<span class="ref-name">{n}</span></td>'
            for n in names
        )
        # Break into rows of 6 cells each
        chunks = [names[k:k+6] for k in range(0, len(names), 6)]
        row_html = ""
        for chunk in chunks:
            row_cells = " ".join(
                f'<td><span class="ref-glyph">{GREEK[n]}</span> '
                f'<span class="ref-name">{n}</span></td>'
                for n in chunk
            )
            # Pad short rows
            row_cells += '<td></td>' * (6 - len(chunk))
            row_html += f"<tr>{row_cells}</tr>\n"
        rows.append(f'<h3>{header}</h3>\n<table class="ref-table">{row_html}</table>')
    return "\n".join(rows)


def ops_table() -> str:
    groups = [
        ("Arithmetic and relations",
         ["times", "div", "cdot", "pm", "mp", "minus", "neq", "approx", "equiv",
          "propto", "leq", "geq", "ll", "gg"]),
        ("Set theory",
         ["in", "notin", "subset", "subseteq", "supset", "supseteq",
          "union", "intersect", "emptyset"]),
        ("Logic and quantifiers",
         ["land", "lor", "lnot", "forall", "exists", "iff"]),
        ("Calculus and analysis",
         ["partial", "nabla", "infty", "to", "leftarrow", "mapsto", "ldots", "cdots"]),
        ("Number sets",
         ["naturals", "integers", "rationals", "reals", "complex"]),
    ]
    out = []
    for title, names in groups:
        chunks = [names[k:k+6] for k in range(0, len(names), 6)]
        row_html = ""
        for chunk in chunks:
            row_cells = " ".join(
                f'<td><span class="ref-glyph">{OPS[n]}</span> '
                f'<span class="ref-name">{n}</span></td>'
                for n in chunk
            )
            row_cells += '<td></td>' * (6 - len(chunk))
            row_html += f"<tr>{row_cells}</tr>\n"
        out.append(f'<h3>{title}</h3>\n<table class="ref-table">{row_html}</table>')
    return "\n".join(out)


REFERENCE_HTML = f"""
<h2>5. Reference: Greek alphabet and operators</h2>
{greek_table()}
{ops_table()}
"""


# ============================================================================
# Section 6: Typography edge cases
# ============================================================================
TYPOGRAPHY_HTML = f"""
<h2>6. Typography edge cases worth checking</h2>

<p><strong>Stacked sub-subscripts.</strong> Position {inline(var('x') + sub(var('i') + sub('1')))}
inside example {inline(var('i'))} runs against the {inline('1')}st coordinate.
The inner subscript uses italic for the variable but normal weight for the digit.</p>

<p><strong>Hat over a fraction.</strong> The estimator
{inline(hat(frac('1', n)) + ' ' + SUM(low='i') + ' ' + x_i)}
puts the hat above the entire fraction, not just the numerator. The
<code>.hat</code> class wraps the whole <code>.frac</code> span.</p>

<p><strong>Multi-character operators.</strong> Names like {inline(op('MSE'))},
{inline(op('KL'))}, {inline(op('sin'))}, and {inline(op('log'))} render upright
to distinguish them from a product of italic variables (compare
{inline(var('M') + var('S') + var('E'))} which reads as a product).</p>

<p><strong>Bracket grouping.</strong> Use literal parentheses for grouping;
they reflow correctly. {inline('(' + var('a') + ' + ' + var('b') + ')' + sup('2')
                                + ' = ' + var('a') + sup('2') + ' + 2'
                                + var('a') + var('b') + ' + ' + var('b') + sup('2'))}.</p>

<p><strong>Vector and overarrow.</strong> The displacement vector
{inline(vec(var('v')))} has magnitude {inline('|' + vec(var('v')) + '|')} and
points in the direction of {inline(hat(var('n')))}.</p>

<p><strong>Sample mean with bar.</strong> The sample mean
{inline(bar(var('x')) + ' = ' + frac('1', n) + ' ' + SUM(low='i=1', high=n) + ' ' + x_i)}
is an unbiased estimator of {inline(mu)}.</p>

<p><strong>Square root with nested radicand.</strong> The golden ratio is
{inline(GREEK['phi'] + ' = ' + frac('1 + ' + sqrt('5'), '2'))}, and its conjugate is
{inline(GREEK['phi'] + sup('&#8722;1') + ' = ' + frac(sqrt('5') + ' &#8722; 1', '2'))}.</p>
"""


# ============================================================================
# Assemble full document
# ============================================================================
EXTRA_CSS = """
body { font-family: Georgia, serif; line-height: 1.7; margin: 1em auto;
       max-width: 42em; padding: 0 1em; color: #222; background: #fff; }
h1 { font-size: 1.5em; border-bottom: 2px solid #1a4078; padding-bottom: 0.3em; }
h2 { font-size: 1.2em; color: #1a4078; margin: 2em 0 0.4em;
     border-bottom: 1px solid #ccc; padding-bottom: 0.2em; }
h3 { font-size: 1.0em; color: #555; margin: 1.2em 0 0.3em; }
p { margin: 0.4em 0 0.7em; }
code { background: #f4f4f4; padding: 0.1em 0.3em; border-radius: 3px;
       font-size: 0.85em; font-family: Consolas, monospace; }
table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 0.95em; }
th, td { border: 1px solid #ddd; padding: 0.5em 0.7em; text-align: left;
         vertical-align: middle; }
th { background: #f0f4fa; color: #1a4078; }
.formula-card { background: #fafafa; border-left: 3px solid #1a4078;
                padding: 0.4em 1em; margin: 0.6em 0; }
.formula-title { font-weight: 700; color: #1a4078; font-size: 0.92em;
                 text-transform: uppercase; letter-spacing: 0.04em;
                 margin: 0.2em 0 0.4em; }
.formula-note { font-size: 0.9em; color: #555; margin: 0.2em 0 0.4em; }
.ref-table td { padding: 0.3em 0.5em; }
.ref-glyph { display: inline-block; min-width: 1.2em; text-align: center;
             font-size: 1.05em; }
.ref-name { font-size: 0.85em; color: #555; font-family: Consolas, monospace; }
"""


def build_xhtml() -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head>
<meta charset="utf-8" />
<title>Plain-HTML Math Examples</title>
<style><![CDATA[
{HTML_MATH_CSS}{EXTRA_CSS}
]]></style>
</head>
<body>
<h1>Plain-HTML Math Examples for Kindle</h1>
<p>Six sections demonstrating how to render mathematics with nothing but
<code>&lt;i&gt;</code>, <code>&lt;sub&gt;</code>, <code>&lt;sup&gt;</code>,
<code>&lt;span&gt;</code>, and CSS. Survives every KDP conversion. Reflows
with body text. Scales with font size. Matches body weight.</p>
{PROSE_HTML}
{DISPLAY_HTML}
{TABLE_HTML}
{GALLERY_HTML}
{REFERENCE_HTML}
{TYPOGRAPHY_HTML}
</body>
</html>
"""


def write_epub(xhtml: str, path: Path) -> None:
    bookid = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_OID, "math2epub-html-examples"))
    opf = f"""<?xml version="1.0"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="id" version="3.0"
         prefix="rendition: http://www.idpf.org/vocab/rendition/#">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="id">{bookid}</dc:identifier>
    <dc:title>Plain-HTML Math Examples</dc:title>
    <dc:language>en</dc:language>
    <meta property="dcterms:modified">2026-05-15T23:30:00Z</meta>
    <meta property="rendition:layout">reflowable</meta>
  </metadata>
  <manifest>
    <item id="page" href="page.xhtml" media-type="application/xhtml+xml"/>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
  </manifest>
  <spine><itemref idref="page"/></spine>
</package>"""
    nav = """<?xml version="1.0"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head><meta charset="utf-8"/><title>Nav</title></head>
<body><nav epub:type="toc"><h1>Contents</h1>
<ol><li><a href="page.xhtml">Plain-HTML Math Examples</a></li></ol></nav></body></html>"""
    with zipfile.ZipFile(path, "w") as z:
        zi = zipfile.ZipInfo("mimetype")
        zi.compress_type = zipfile.ZIP_STORED
        z.writestr(zi, "application/epub+zip")
        z.writestr("META-INF/container.xml",
                   '<?xml version="1.0"?>\n'
                   '<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">\n'
                   '<rootfiles><rootfile media-type="application/oebps-package+xml" '
                   'full-path="EPUB/content.opf"/></rootfiles></container>')
        z.writestr("EPUB/content.opf", opf)
        z.writestr("EPUB/nav.xhtml", nav)
        z.writestr("EPUB/page.xhtml", xhtml)


def main() -> None:
    xhtml = build_xhtml()
    html_path = OUT_DIR / "math-html-examples.html"
    html_path.write_text(xhtml, encoding="utf-8")
    print(f"Wrote {html_path} ({html_path.stat().st_size:,} bytes)")

    epub_path = OUT_DIR / "math-html-examples.epub"
    write_epub(xhtml, epub_path)
    print(f"Wrote {epub_path} ({epub_path.stat().st_size:,} bytes)")

    print()
    print("Next: validate with")
    print(f"  python {SCRIPTS / 'validate.py'} {epub_path}")
    print("Then drag the EPUB into Kindle Previewer 3.")


if __name__ == "__main__":
    main()
