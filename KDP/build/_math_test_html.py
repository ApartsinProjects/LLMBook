"""Math rendering test v3: PURE HTML approach (no MathML, no SVG).

Use `<sub>`, `<sup>`, `<i>` and CSS-styled fraction spans to render
math. This is the ONLY approach guaranteed to render on EVERY Kindle
device, every reflowable reader, and every browser, because it uses
no element beyond HTML5 basics.

Limitations:
- Plain HTML can't render true two-line fractions cleanly; we use a
  flex/inline-block "stacked" pattern with explicit CSS.
- No automatic glyph for radicals (use Unicode √ and overline).
- Greek letters and operators come from Unicode (η, σ, ∇, Σ, etc.).

Produces:
  math-test-v3-html.epub
"""
from __future__ import annotations
from pathlib import Path
import zipfile
import uuid

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "KDP" / "output"


# Each entry: (label, html_inline, mode, prose_before, prose_after).
# html_inline already contains the rendered-as-HTML math.
INLINE = '<i>y</i><sub><i>i</i></sub>'
TESTS = [
    ("Subscript (inline)",
     '<i>y</i><sub><i>i</i></sub>', "inline",
     "The output for the i-th example is denoted",
     ", where i runs from 1 to N."),
    ("Superscript (inline)",
     '<i>x</i><sup>2</sup>', "inline",
     "We square the residual as",
     "before summing across examples."),
    ("Sub + super (inline)",
     '<i>x</i><sub><i>i</i></sub><sup>2</sup>', "inline",
     "The squared i-th input",
     "appears in the variance computation."),
    ("Hat accent (inline)",
     '<span class="hat"><i>y</i></span><sub><i>i</i></sub>', "inline",
     "The model prediction",
     "is compared against the ground-truth label."),
    ("Fraction (inline)",
     '<span class="frac"><span class="num">1</span><span class="den"><i>n</i></span></span>',
     "inline",
     "Averaging gives the",
     "factor in front of the sum."),
    ("Square root (inline)",
     '√<span class="overline"><i>x</i><sup>2</sup>+<i>y</i><sup>2</sup></span>',
     "inline",
     "The 2-D distance is",
     "by the Pythagorean theorem."),
    ("Sum with limits (inline)",
     'Σ<sub><i>i</i>=1</sub><sup><i>n</i></sup><i>x</i><sub><i>i</i></sub>',
     "inline",
     "Sigma notation",
     "is shorthand for the total."),
    ("Gradient (inline)",
     '∇<i>L</i>', "inline",
     "Gradient descent moves opposite the gradient",
     "of the loss with respect to parameters."),
    ("Greek letter eta (inline)",
     'η', "inline",
     "The learning rate",
     "controls step size in each update."),
    ("MSE (block)",
     'MSE = <span class="frac"><span class="num">1</span><span class="den"><i>n</i></span></span>'
     'Σ<sub><i>i</i>=1</sub><sup><i>n</i></sup>'
     '(<span class="hat"><i>y</i></span><sub><i>i</i></sub> − '
     '<i>y</i><sub><i>i</i></sub>)<sup>2</sup>',
     "block",
     "For regression, the most common loss is Mean Squared Error:",
     "Squaring the error penalizes large mistakes."),
    ("Cross-entropy (block)",
     '<i>L</i> = −<span class="frac"><span class="num">1</span><span class="den"><i>n</i></span></span>'
     'Σ<sub><i>i</i>=1</sub><sup><i>n</i></sup>'
     '<i>y</i><sub><i>i</i></sub>log(<i>p</i><sub><i>i</i></sub>)',
     "block",
     "For classification, the standard is cross-entropy loss:",
     "where p_i is the model's predicted probability."),
    ("Weight update (block)",
     '<i>w</i><sub>new</sub> = <i>w</i><sub>old</sub> − '
     'η∇<i>L</i>(<i>w</i><sub>old</sub>)',
     "block",
     "Stochastic gradient descent updates weights at every step:",
     "where eta is the learning rate."),
    ("Sigmoid (block)",
     'σ(<i>x</i>) = '
     '<span class="frac"><span class="num">1</span>'
     '<span class="den">1 + <i>e</i><sup>−<i>x</i></sup></span></span>',
     "block",
     "The sigmoid activation squashes any real value into (0, 1):",
     "used in binary classification heads."),
]


# Inline-stack fraction (no flex, no grid -- Kindle reflowable safe).
# The fraction renders as a vertically-stacked numerator over
# denominator with a 1-px black line between, all inline-block so it
# flows with text.
CSS = """\
body { font-family: Georgia, serif; line-height: 1.6; margin: 1em; max-width: 40em; }
h1 { font-size: 1.5em; border-bottom: 2px solid #1a4078; padding-bottom: 0.3em; }
h2 { font-size: 1.15em; color: #1a4078; margin-top: 1.5em; }
code { background: #f4f4f4; padding: 0.15em 0.4em; border-radius: 3px; font-size: 0.9em; }
.math-block { text-align: center; margin: 0.8em 0; font-size: 1.1em; }

/* Fraction: inline-block stack. Uses vertical-align: middle so the
 * fraction sits centered with the surrounding text x-height. */
.frac {
    display: inline-block;
    vertical-align: -0.5em;
    margin: 0 0.15em;
    text-align: center;
    line-height: 1;
}
.frac > .num {
    display: block;
    border-bottom: 1px solid currentColor;
    padding: 0 0.2em 0.05em 0.2em;
    font-size: 0.9em;
}
.frac > .den {
    display: block;
    padding: 0.05em 0.2em 0 0.2em;
    font-size: 0.9em;
}

/* Hat / overline accents over an arbitrary block of letters. */
.hat {
    display: inline-block;
    position: relative;
    padding-top: 0.2em;
}
.hat::before {
    content: "^";
    position: absolute;
    top: -0.4em;
    left: 0;
    right: 0;
    text-align: center;
    font-size: 0.85em;
}
.overline {
    border-top: 1px solid currentColor;
    padding-top: 0.05em;
}

/* Subscript / superscript tweak: nudge slightly down/up so the
 * default 'sub'/'sup' renders crisply on Kindle (the default is
 * sometimes too aggressive). */
sub, sup { line-height: 0; font-size: 0.78em; }
sub { vertical-align: -0.3em; }
sup { vertical-align: 0.55em; }
"""


def build_chapter():
    sections = []
    for label, html, mode, pre, post in TESTS:
        if mode == "block":
            block = (
                f'<p>{pre}</p>\n'
                f'<div class="math-block">{html}</div>\n'
                f'<p>{post}</p>'
            )
        else:
            block = (
                f'<p>{pre} {html} {post}</p>'
            )
        sections.append(
            f'<section>\n'
            f'<h2>{label}</h2>\n'
            f'{block}\n'
            f'</section>'
        )
    body = "\n".join(sections)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head>
<meta charset="utf-8" />
<title>Math Test v3 (HTML only)</title>
<link rel="stylesheet" type="text/css" href="styles/test.css" />
</head>
<body>
<h1>Math Rendering Test v3 — HTML only</h1>
<p>No MathML, no inline SVG. Math is built from
<code>&lt;sub&gt;</code>, <code>&lt;sup&gt;</code>, <code>&lt;i&gt;</code>, and CSS-styled
inline-block fractions and accents. This pipeline renders on EVERY
EPUB reader because it uses no element beyond HTML5 basics.</p>
{body}
</body>
</html>
"""


def main():
    out_path = OUT_DIR / "math-test-v3-html.epub"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    bookid = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_OID, out_path.stem))

    opf = f"""<?xml version="1.0"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="id" version="3.0"
         prefix="rendition: http://www.idpf.org/vocab/rendition/#">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="id">{bookid}</dc:identifier>
    <dc:title>Math Test v3 (HTML)</dc:title>
    <dc:language>en</dc:language>
    <dc:creator>KPVDebug math test harness</dc:creator>
    <dc:date>2026-05-15</dc:date>
    <meta property="dcterms:modified">2026-05-15T21:00:00Z</meta>
    <meta property="rendition:layout">reflowable</meta>
    <meta property="rendition:orientation">auto</meta>
    <meta property="rendition:spread">auto</meta>
  </metadata>
  <manifest>
    <item id="page" href="page.xhtml" media-type="application/xhtml+xml"/>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="css" href="styles/test.css" media-type="text/css"/>
  </manifest>
  <spine><itemref idref="page"/></spine>
</package>"""

    nav = """<?xml version="1.0"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head><meta charset="utf-8"/><title>Nav</title></head>
<body><nav epub:type="toc" id="toc" role="doc-toc"><h1>Contents</h1>
<ol><li><a href="page.xhtml">Math Test v3 (HTML)</a></li></ol></nav></body></html>"""

    chapter = build_chapter()

    with zipfile.ZipFile(out_path, "w") as z:
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
        z.writestr("EPUB/page.xhtml", chapter)
        z.writestr("EPUB/styles/test.css", CSS)
    print(f"Wrote {out_path.relative_to(ROOT)} ({out_path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
