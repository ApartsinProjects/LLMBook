"""Dense MathML vs Plain-HTML comparison for empirical recipe finding.

The goal: lay out 25 staple math expressions, each in two columns
(MathML rendered by KaTeX, plain HTML built by html_math.py helpers),
plus a tiny recommendation column the user fills in by screenshot
inspection. The output is dense enough that 15-20 rows fit per
screenshot, so one or two captures cover the whole comparison.

After the user marks which expressions render well in which pipeline,
the recipe is committed to LESSONS.md as "use MathML for these
categories, fall back to plain HTML for these others."

Outputs:
    KDP/output/math-recipe.html  - browser baseline
    KDP/output/math-recipe.epub  - Kindle Previewer 3 baseline
"""
from __future__ import annotations

import json
import os
import re
import subprocess
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


def _resolve_out_dir() -> Path:
    candidate = HERE
    for _ in range(6):
        if (candidate / "KDP" / "output").is_dir():
            return candidate / "KDP" / "output"
        candidate = candidate.parent
    return HERE / "demo-output"


OUT_DIR = _resolve_out_dir()
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Locate the existing KaTeX renderer; reuse instead of duplicating
RENDER_MATH_JS = HERE.parent.parent.parent.parent / "KDP" / "build" / "render_math.js"
KATEX_MODULES = Path("E:/Tools/katex/node_modules")


# ============================================================================
# Test corpus: every expression we want to settle the recipe for.
#
# Each row: (category, latex, display, html_construction, why_it_matters)
#   html_construction is a function that takes no args and returns the HTML
#   string for the expression (assembled from html_math helpers).
# ============================================================================
def _html_y_i():           return var("y", sub="i")
def _html_x_sq():          return var("x", sup="2")
def _html_y_sub_sup():     return var("y", sub="i") + sup("2")
def _html_z_multi():       return var("z", sub="ij") + sup("(k)")
def _html_alpha_beta():    return GREEK["alpha"] + " + " + GREEK["beta"]

def _html_frac_1n():       return frac("1", var("n"))
def _html_frac_compound(): return frac(var("a") + "+" + var("b"), var("c") + "+" + var("d"))
def _html_sigmoid_den():   return frac("1", "1 + " + var("e") + sup("&#8722;" + var("x")))
def _html_partial():       return frac(OPS["partial"] + var("L"), OPS["partial"] + GREEK["theta"])
def _html_pq():            return frac(var("p") + "(" + var("x") + ")", var("q") + "(" + var("x") + ")")

def _html_sum():           return summation(low=var("i") + "=1", high=var("n"))
def _html_int():           return integral(low="&#8722;" + OPS["infty"], high=OPS["infty"])
def _html_prod():          return product(low=var("j") + "=1", high=var("k"))
def _html_lim():           return op("lim", sub=var("n") + " " + OPS["to"] + " " + OPS["infty"])
def _html_max():           return op("max", sub=var("x") + " " + OPS["in"] + " " + var("X"))

def _html_sqrt_x():        return sqrt(var("x"))
def _html_sqrt_ab():       return sqrt(var("a") + "+" + var("b"))
def _html_sqrt_disc():     return sqrt(var("b") + sup("2") + " &#8722; 4" + var("a") + var("c"))
def _html_hat_y():         return hat(var("y"))
def _html_bar_x():         return bar(var("x"))
def _html_vec_v():         return vec(var("v"))

def _html_mse():
    return (op("MSE") + " = " + frac("1", var("n")) + " "
            + summation(low=var("i") + "=1", high=var("n")) + " ("
            + hat(var("y")) + sub("i") + " &#8722; " + var("y", sub="i") + ")"
            + sup("2"))

def _html_sigmoid():
    return (GREEK["sigma"] + "(" + var("x") + ") = "
            + frac("1", "1 + " + var("e") + sup("&#8722;" + var("x"))))

def _html_softmax():
    return (GREEK["sigma"] + "(" + var("z") + ")" + sub("k") + " = "
            + frac(var("e") + sup(var("z") + sub("k")),
                   summation(low=var("j") + "=1", high=var("K"))
                   + " " + var("e") + sup(var("z") + sub("j"))))

def _html_bayes():
    return (var("P") + "(" + var("A") + " | " + var("B") + ") = "
            + frac(var("P") + "(" + var("B") + " | " + var("A") + ") "
                   + var("P") + "(" + var("A") + ")",
                   var("P") + "(" + var("B") + ")"))

def _html_grad_descent():
    return (GREEK["theta"] + sub("t+1") + " = " + GREEK["theta"] + sub("t")
            + " &#8722; " + GREEK["eta"] + " " + OPS["nabla"] + var("L")
            + "(" + GREEK["theta"] + sub("t") + ")")


TESTS = [
    # category, label, latex, display, html_fn
    ("Atom",      "subscript",          r"y_i",                      False, _html_y_i),
    ("Atom",      "superscript",        r"x^2",                      False, _html_x_sq),
    ("Atom",      "sub+sup",            r"y_i^2",                    False, _html_y_sub_sup),
    ("Atom",      "multi-index",        r"z_{ij}^{(k)}",             False, _html_z_multi),
    ("Atom",      "Greek letters",      r"\alpha + \beta",           False, _html_alpha_beta),

    ("Fraction",  "simple",             r"\frac{1}{n}",              False, _html_frac_1n),
    ("Fraction",  "compound",           r"\frac{a+b}{c+d}",          False, _html_frac_compound),
    ("Fraction",  "sigmoid denom",      r"\frac{1}{1+e^{-x}}",       False, _html_sigmoid_den),
    ("Fraction",  "partial deriv",      r"\frac{\partial L}{\partial \theta}", False, _html_partial),
    ("Fraction",  "function ratio",     r"\frac{p(x)}{q(x)}",        False, _html_pq),

    ("Big op",    "sum w/ limits",      r"\sum_{i=1}^{n}",           True,  _html_sum),
    ("Big op",    "integral",           r"\int_{-\infty}^{\infty}",  True,  _html_int),
    ("Big op",    "product",            r"\prod_{j=1}^{k}",          True,  _html_prod),
    ("Big op",    "limit",              r"\lim_{n \to \infty}",      False, _html_lim),
    ("Big op",    "max",                r"\max_{x \in X}",           False, _html_max),

    ("Accent",    "sqrt",               r"\sqrt{x}",                 False, _html_sqrt_x),
    ("Accent",    "sqrt over expr",     r"\sqrt{a+b}",               False, _html_sqrt_ab),
    ("Accent",    "sqrt discriminant",  r"\sqrt{b^2 - 4ac}",         False, _html_sqrt_disc),
    ("Accent",    "hat",                r"\hat{y}",                  False, _html_hat_y),
    ("Accent",    "bar",                r"\bar{x}",                  False, _html_bar_x),
    ("Accent",    "vector",             r"\vec{v}",                  False, _html_vec_v),

    ("Full eqn",  "MSE",                r"\mathrm{MSE} = \frac{1}{n}\sum_{i=1}^{n}(\hat{y}_i - y_i)^2", True, _html_mse),
    ("Full eqn",  "sigmoid",            r"\sigma(x) = \frac{1}{1+e^{-x}}", True, _html_sigmoid),
    ("Full eqn",  "softmax",            r"\sigma(z)_k = \frac{e^{z_k}}{\sum_{j=1}^{K} e^{z_j}}", True, _html_softmax),
    ("Full eqn",  "Bayes",              r"P(A|B) = \frac{P(B|A)P(A)}{P(B)}", True, _html_bayes),
    ("Full eqn",  "gradient descent",   r"\theta_{t+1} = \theta_t - \eta \nabla L(\theta_t)", True, _html_grad_descent),
]


# ============================================================================
# MathML rendering via the existing KaTeX subprocess
# ============================================================================
def render_mathml(items: list[tuple[str, str, bool]]) -> dict[str, str]:
    """Return {id: mathml_html_string}."""
    payload = [{"id": str(i), "tex": tex, "display": disp}
               for i, (tex, _label, disp) in enumerate(items)]
    env = {**os.environ, "NODE_PATH": str(KATEX_MODULES)}
    proc = subprocess.run(
        ["node", str(RENDER_MATH_JS)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        env=env,
        timeout=60,
        encoding="utf-8",
    )
    if proc.returncode != 0:
        raise RuntimeError(f"render_math.js failed: {proc.stderr}")
    out = {}
    for r in json.loads(proc.stdout):
        # Strip the <semantics><annotation>...</annotation></semantics> wrapper
        # so the raw MathML can be measured fairly against plain HTML.
        html = r["html"]
        html = re.sub(
            r"<semantics>(.*?)<annotation\b[^>]*>.*?</annotation>\s*</semantics>",
            r"\1", html, flags=re.DOTALL,
        )
        out[r["id"]] = html
    return out


# ============================================================================
# Page assembly
# ============================================================================
EXTRA_CSS = """
/* MathML rendering: the browser needs an explicit math font and an
 * explicit font-size on <math>, otherwise it falls back to a tiny
 * default that looks like colored marks. Adding these makes the
 * MathML column actually testable. */
math {
    font-family: "Cambria Math", "STIX Two Math", "Latin Modern Math",
                 "Asana Math", "TeX Gyre Pagella Math", serif;
    font-size: 1.05em;
    line-height: 1;
    vertical-align: middle;
}

:root { --bd: #ddd; --hdr: #1a4078; --alt: #fafafa; }
body { font-family: Georgia, serif; line-height: 1.5; margin: 0.6em auto;
       max-width: 56em; padding: 0 0.8em; color: #222; background: #fff;
       font-size: 14px; }
h1 { font-size: 1.3em; border-bottom: 2px solid var(--hdr);
     padding-bottom: 0.25em; margin: 0.4em 0 0.3em; color: var(--hdr); }
p.lede { font-size: 0.9em; color: #555; margin: 0.4em 0 0.6em; }
table.recipe { border-collapse: collapse; width: 100%; font-size: 0.85em;
               table-layout: auto; margin: 0.4em 0; }
table.recipe thead th {
    background: var(--hdr); color: #fff; padding: 0.3em 0.5em;
    text-align: left; font-weight: 600; font-size: 0.85em;
    text-transform: uppercase; letter-spacing: 0.05em;
    position: sticky; top: 0; z-index: 1;
}
table.recipe tbody td {
    border-bottom: 1px solid var(--bd);
    padding: 0.35em 0.55em;
    vertical-align: middle;
    line-height: 1.4;
}
table.recipe tbody tr:nth-child(odd) td { background: var(--alt); }
table.recipe tbody tr.cat-break td {
    background: #eef0f5; font-weight: 600; font-size: 0.9em;
    color: var(--hdr); padding: 0.3em 0.55em;
    text-transform: uppercase; letter-spacing: 0.04em;
    border-top: 2px solid var(--hdr);
}
td.id    { width: 2.5em; color: #888; font-family: Consolas, monospace;
           font-size: 0.85em; text-align: right; }
td.label { width: 8em; font-size: 0.88em; color: #555; }
td.latex { width: 9em; font-family: Consolas, monospace; font-size: 0.78em;
           color: #444; word-break: break-all; }
td.mathml, td.html-col { vertical-align: middle; min-width: 10em; }
td.mathml math { font-size: 1em; }

/* Display math in narrow table cells: use horizontal scroll instead of
 * wrapping. .math-display has white-space:nowrap globally, but inside a
 * table cell the renderer may force-wrap if the inline-block atoms hit
 * the cell edge. overflow-x:auto here puts a scrollbar in the cell
 * instead of letting the atoms stack vertically. */
table.recipe .math-inline, table.recipe .math-display {
    margin: 0; padding: 0;
    max-width: 100%;
    overflow-x: auto;
    overflow-y: visible;
}
table.recipe .math-display {
    text-align: left; line-height: 1.4; padding: 0;
    white-space: nowrap;
}
/* Allow the full-equation rows to render wider rather than squeezing. */
table.recipe tbody tr.full-eqn td.html-col,
table.recipe tbody tr.full-eqn td.mathml { min-width: 16em; }

/* Compact legend at top */
.legend { font-size: 0.8em; color: #555; margin: 0.4em 0 0.8em;
          padding: 0.4em 0.6em; background: #f5f7fb; border-left: 3px solid var(--hdr); }
.legend code { background: #fff; padding: 0 0.25em; border-radius: 2px;
               font-family: Consolas, monospace; }
"""


def build_xhtml(mathml: dict[str, str]) -> str:
    rows = []
    last_cat = None
    for i, (cat, label, latex, display_mode, html_fn) in enumerate(TESTS):
        if cat != last_cat:
            rows.append(
                f'<tr class="cat-break"><td colspan="5">{cat}</td></tr>'
            )
            last_cat = cat
        latex_esc = (latex.replace("&", "&amp;")
                     .replace("<", "&lt;").replace(">", "&gt;"))
        # MathML cell - the KaTeX-rendered math wrapped in our scope class
        mml = mathml.get(str(i), "")
        # HTML cell - constructed from html_math helpers
        html_raw = html_fn()
        if display_mode:
            html_cell = display(html_raw)
            mml_cell = f'<div class="math-display">{mml}</div>'
        else:
            html_cell = inline(html_raw)
            mml_cell = f'<span class="math-inline">{mml}</span>'
        row_cls = ' class="full-eqn"' if cat == "Full eqn" else ''
        rows.append(
            f'<tr{row_cls}>'
            f'<td class="id">{i+1}</td>'
            f'<td class="label">{label}</td>'
            f'<td class="latex"><code>{latex_esc}</code></td>'
            f'<td class="mathml">{mml_cell}</td>'
            f'<td class="html-col">{html_cell}</td>'
            f'</tr>'
        )

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head>
<meta charset="utf-8" />
<title>Math Recipe Comparison: MathML vs Plain HTML</title>
<style><![CDATA[
{HTML_MATH_CSS}{EXTRA_CSS}
]]></style>
</head>
<body>
<h1>Math Recipe Comparison: MathML vs Plain HTML</h1>
<p class="lede">26 expressions, two pipelines per row, dense enough to
screenshot the whole table at once. After identifying which expressions
render well in which pipeline, the recipe goes into
<code>LESSONS.md</code> in the math2epub skill.</p>
<div class="legend">
<strong>Columns:</strong>
<code>#</code> row id |
<code>LATEX</code> source for the MathML pipeline |
<code>MATHML</code> KaTeX <code>output:'mathml'</code> render (Kindle Enhanced Typesetting interprets this) |
<code>PLAIN HTML</code> our hand-built HTML using <code>&lt;i&gt;</code>+<code>&lt;sub&gt;</code>+<code>&lt;sup&gt;</code>+<code>&lt;span class="frac"&gt;</code>+CSS.
</div>
<table class="recipe">
<thead>
<tr><th>#</th><th>Concept</th><th>LaTeX</th><th>MathML</th><th>Plain HTML</th></tr>
</thead>
<tbody>
{chr(10).join(rows)}
</tbody>
</table>
<p class="lede"><strong>How to use this comparison:</strong> screenshot
the table (or sections of it). For each row, decide whether the MathML
cell or the Plain HTML cell renders better. A pattern will emerge:
typically MathML wins for stacked limits / integrals / msubsup, and
plain HTML wins for simple variables, sub/sup, and fractions where
weight-matching matters. Once decided, send the verdicts back and
the recipe gets written into the skill.</p>
</body>
</html>
"""


def write_epub(xhtml: str, path: Path) -> None:
    bookid = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_OID, "math-recipe"))
    opf = f"""<?xml version="1.0"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="id" version="3.0"
         prefix="rendition: http://www.idpf.org/vocab/rendition/#">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="id">{bookid}</dc:identifier>
    <dc:title>Math Recipe Comparison</dc:title>
    <dc:language>en</dc:language>
    <meta property="dcterms:modified">2026-05-16T00:00:00Z</meta>
    <meta property="rendition:layout">reflowable</meta>
  </metadata>
  <manifest>
    <item id="page" href="page.xhtml" media-type="application/xhtml+xml" properties="mathml"/>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
  </manifest>
  <spine><itemref idref="page"/></spine>
</package>"""
    nav = """<?xml version="1.0"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head><meta charset="utf-8"/><title>Nav</title></head>
<body><nav epub:type="toc"><h1>Contents</h1>
<ol><li><a href="page.xhtml">Math Recipe Comparison</a></li></ol></nav></body></html>"""
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
    items_for_mathml = [(t[2], t[1], t[3]) for t in TESTS]  # (latex, label, display)
    print(f"Rendering {len(items_for_mathml)} expressions through KaTeX (MathML)...")
    mathml = render_mathml(items_for_mathml)
    print(f"  Got {len(mathml)} MathML strings")

    xhtml = build_xhtml(mathml)
    html_path = OUT_DIR / "math-recipe.html"
    html_path.write_text(xhtml, encoding="utf-8")
    print(f"Wrote {html_path} ({html_path.stat().st_size:,} bytes)")

    epub_path = OUT_DIR / "math-recipe.epub"
    write_epub(xhtml, epub_path)
    print(f"Wrote {epub_path} ({epub_path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
