"""Math rendering test v4: PNG images via matplotlib mathtext.

This is the PRODUCTION-RECOMMENDED pipeline per multiple authoritative
sources (Leanpub, Pandoc --webtex, Amazon KDP Image Guidelines:
"SVG tags can lead to errors. Amazon recommends removing SVG tags and
using the image tag in HTML for images"). Math expressions rendered to
transparent PNGs at 300 DPI and embedded as <img> with vertical-align:
middle for inline flow.

Pros:
  - Renders on EVERY Kindle device and reflowable reader (no MathML
    quirks, no SVG <use> indirection).
  - Identical visual output across readers (the rasterized image is the
    image).
  - Works with KDP's KFX converter without surprises.

Cons:
  - Not text-selectable.
  - Larger file footprint (each math ≈ 1-3 KB PNG).
  - Fixed at one DPI; small on high-density displays, but matplotlib's
    300 DPI is sharp enough on Kindle Paperwhite (300 ppi) and below.

Produces:
  math-test-v4-png.epub
"""
from __future__ import annotations
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
matplotlib.rcParams['mathtext.fontset'] = 'cm'  # Computer Modern (LaTeX style)
matplotlib.rcParams['text.color'] = 'black'

from pathlib import Path
import io
import uuid
import zipfile

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "KDP" / "output"


# (label, latex (matplotlib-mathtext syntax), mode, prose_before, prose_after)
TESTS = [
    ("Subscript (inline)",
     r"y_i", "inline",
     "The output for the i-th example is denoted",
     ", where i runs from 1 to N."),
    ("Superscript (inline)",
     r"x^2", "inline",
     "We square the residual as",
     "before summing across examples."),
    ("Sub + super (inline)",
     r"x_i^2", "inline",
     "The squared i-th input",
     "appears in the variance computation."),
    ("Hat accent (inline)",
     r"\hat{y}_i", "inline",
     "The model prediction",
     "is compared against the ground-truth label."),
    ("Fraction (inline)",
     r"\frac{1}{n}", "inline",
     "Averaging gives the",
     "factor in front of the sum."),
    ("Square root (inline)",
     r"\sqrt{x^2 + y^2}", "inline",
     "The 2-D distance is",
     "by the Pythagorean theorem."),
    ("Sum with limits (inline)",
     r"\sum_{i=1}^{n} x_i", "inline",
     "Sigma notation",
     "is shorthand for the total."),
    ("Gradient (inline)",
     r"\nabla L", "inline",
     "Gradient descent moves opposite the gradient",
     "of the loss with respect to parameters."),
    ("Greek letter eta (inline)",
     r"\eta", "inline",
     "The learning rate",
     "controls step size in each update."),
    ("MSE (block)",
     r"MSE = \frac{1}{n}\sum_{i=1}^{n} (\hat{y}_i - y_i)^2",
     "block",
     "For regression, the most common loss is Mean Squared Error:",
     "Squaring the error penalizes large mistakes."),
    ("Cross-entropy (block)",
     r"L = -\frac{1}{n}\sum_{i=1}^{n} y_i \log(p_i)",
     "block",
     "For classification, the standard is cross-entropy loss:",
     "where p_i is the model's predicted probability."),
    ("Weight update (block)",
     r"w_{new} = w_{old} - \eta \nabla L(w_{old})",
     "block",
     "Stochastic gradient descent updates weights at every step:",
     "where eta is the learning rate."),
    ("Sigmoid (block)",
     r"\sigma(x) = \frac{1}{1 + e^{-x}}",
     "block",
     "The sigmoid activation squashes any real value into (0, 1):",
     "used in binary classification heads."),
]


def render_png(tex: str, display: bool, dpi: int = 300) -> bytes:
    """Render a LaTeX math expression to a transparent-background PNG."""
    fontsize = 14 if display else 12
    fig = plt.figure(figsize=(0.1, 0.1), dpi=dpi)
    fig.patch.set_alpha(0)
    fig.text(0.5, 0.5, f"${tex}$", fontsize=fontsize, ha='center', va='center',
             color='black')
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, transparent=True,
                bbox_inches='tight', pad_inches=0.05)
    plt.close(fig)
    return buf.getvalue()


def build_chapter(images: list[tuple]) -> str:
    """images: list of (filename, mode) tuples per TESTS row."""
    sections = []
    for (label, tex, mode, pre, post), (fname, _mode) in zip(TESTS, images):
        # Inline math: img inside paragraph with vertical-align: middle
        if mode == "block":
            block = (
                f'<p>{pre}</p>\n'
                f'<div class="math-block">'
                f'<img src="img/{fname}" alt="{tex}" class="math-display"/>'
                f'</div>\n'
                f'<p>{post}</p>'
            )
        else:
            block = (
                f'<p>{pre} '
                f'<img src="img/{fname}" alt="{tex}" class="math-inline"/>'
                f' {post}</p>'
            )
        sections.append(
            f'<section>\n'
            f'<h2>{label}</h2>\n'
            f'<p><code>{tex}</code></p>\n'
            f'{block}\n'
            f'</section>'
        )
    body = "\n".join(sections)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head>
<meta charset="utf-8" />
<title>Math Test v4 (PNG)</title>
<link rel="stylesheet" type="text/css" href="styles/test.css" />
</head>
<body>
<h1>Math Rendering Test v4 — PNG images</h1>
<p>Each math expression is rendered server-side to a transparent PNG
via matplotlib mathtext (Computer Modern font). Embedded as inline
<code>&lt;img&gt;</code> with <code>vertical-align: middle</code> so it flows with text.
Per Amazon KDP Image Guidelines: "SVG tags can lead to errors. Amazon
recommends removing SVG tags and using the image tag in HTML for images."</p>
{body}
</body>
</html>
"""


CSS = """\
body { font-family: Georgia, serif; line-height: 1.6; margin: 1em; max-width: 40em; }
h1 { font-size: 1.5em; border-bottom: 2px solid #1a4078; padding-bottom: 0.3em; }
h2 { font-size: 1.15em; color: #1a4078; margin-top: 1.5em; }
code { background: #f4f4f4; padding: 0.15em 0.4em; border-radius: 3px; font-size: 0.9em; }
.math-block { text-align: center; margin: 0.8em 0; }
.math-block img.math-display { max-width: 100%; height: auto; }
img.math-inline { vertical-align: middle; max-height: 1.6em; }
"""


def main():
    out_path = OUT_DIR / "math-test-v4-png.epub"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    bookid = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_OID, out_path.stem))

    # Render each expression
    print("Rendering math to PNG via matplotlib...")
    images = []  # (filename, png_bytes)
    for i, (label, tex, mode, _pre, _post) in enumerate(TESTS):
        png_bytes = render_png(tex, display=(mode == "block"))
        fname = f"eq{i+1:03d}.png"
        images.append((fname, png_bytes))
        print(f"  {fname}  ({len(png_bytes):>5} B)  {label}")

    chapter = build_chapter([(f, m) for (f, _), (_, _, m, _, _) in zip(images, TESTS)])

    opf_manifest_img = "\n    ".join(
        f'<item id="img{i+1:03d}" href="img/{fname}" media-type="image/png"/>'
        for i, (fname, _) in enumerate(images)
    )

    opf = f"""<?xml version="1.0"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="id" version="3.0"
         prefix="rendition: http://www.idpf.org/vocab/rendition/#">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="id">{bookid}</dc:identifier>
    <dc:title>Math Test v4 (PNG)</dc:title>
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
    {opf_manifest_img}
  </manifest>
  <spine><itemref idref="page"/></spine>
</package>"""

    nav = """<?xml version="1.0"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head><meta charset="utf-8"/><title>Nav</title></head>
<body><nav epub:type="toc" id="toc" role="doc-toc"><h1>Contents</h1>
<ol><li><a href="page.xhtml">Math Test v4 (PNG)</a></li></ol></nav></body></html>"""

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
        for fname, png_bytes in images:
            z.writestr(f"EPUB/img/{fname}", png_bytes)

    print()
    print(f"Wrote {out_path.relative_to(ROOT)} ({out_path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
