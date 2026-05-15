"""Math rendering test v2: PROSE-layout test EPUBs (no <table> wrapper)
plus a parallel SVG variant.

The v1 _math_test_sample.py wrapped each expression in a <td> cell of a
table. Per the agent's Kindle MathML research and our analysis, narrow
table cells are the dominant cause of bad fraction/mover rendering on
Kindle. v2 fixes the test by putting every math fragment in real prose
context, the way a real chapter does:

  - One <h2> per pattern
  - One paragraph of context text WITH the math expression inline
  - One <div class="math-block"> for the block version

Produces TWO EPUBs:

  math-test-v2-mathml.epub    KaTeX -> MathML (current main pipeline)
  math-test-v2-svg.epub       MathJax -> inline SVG (per-expression)

Drag both into Kindle Previewer 3 and compare side-by-side. If
mathml renders cleanly in prose context, the table-cell hypothesis is
confirmed. If svg renders cleanly but mathml still doesn't, switch the
main book pipeline to SVG.
"""
from __future__ import annotations
from pathlib import Path
import subprocess
import json
import zipfile
import os
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "KDP" / "output"
KATEX_RENDER = ROOT / "KDP" / "build" / "render_math.js"
KATEX_MODULES = Path("E:/Tools/katex/node_modules")
MATHJAX_RENDER = Path("E:/Tools/mathjax/tex2svg.js")
MATHJAX_MODULES = Path("E:/Tools/mathjax/node_modules")


# Each item gets a real-prose context: a heading, a sentence with inline math,
# and (for display-mode items) a display-math block + after-sentence.
TESTS = [
    # (label, latex_tex, mode, prose_before, prose_after)
    ("Subscript (inline)",
     r"y_{i}", "inline",
     "The output for the i-th example is denoted",
     ", where i runs from 1 to N."),
    ("Superscript (inline)",
     r"x^{2}", "inline",
     "We square the residual as",
     "before summing across examples."),
    ("Sub + super (inline)",
     r"x_{i}^{2}", "inline",
     "The squared i-th input",
     "appears in the variance computation."),
    ("Hat accent (inline)",
     r"\hat{y}_{i}", "inline",
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
     r"\operatorname{MSE} = \frac{1}{n}\sum_{i=1}^{n} (\hat{y}_{i} - y_{i})^{2}",
     "block",
     "For regression, the most common loss is Mean Squared Error:",
     "Squaring the error penalizes large mistakes."),
    ("Cross-entropy (block)",
     r"L = -\frac{1}{n}\sum_{i=1}^{n} y_i \log(p_i)",
     "block",
     "For classification, the standard is cross-entropy loss:",
     "where p_i is the model's predicted probability."),
    ("Weight update (block)",
     r"w_{\text{new}} = w_{\text{old}} - \eta \nabla L(w_{\text{old}})",
     "block",
     "Stochastic gradient descent updates weights at every step:",
     "where eta is the learning rate."),
    ("Sigmoid (block)",
     r"\sigma(x) = \frac{1}{1 + e^{-x}}",
     "block",
     "The sigmoid activation squashes any real value into (0, 1):",
     "used in binary classification heads."),
]


# ----------------------------------------------------------------------
# Render via KaTeX (MathML) or MathJax (SVG)
# ----------------------------------------------------------------------

def render_mathml(items: list[dict]) -> dict[str, str]:
    payload = [{"id": str(i), "tex": it[1], "display": it[2] == "block"}
               for i, it in enumerate(items)]
    proc = subprocess.run(
        ["node", str(KATEX_RENDER)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        env={**os.environ, "NODE_PATH": str(KATEX_MODULES)},
        timeout=60,
        encoding="utf-8",
    )
    if proc.returncode != 0:
        raise RuntimeError(f"katex failed: {proc.stderr}")
    raw = {r["id"]: r["html"] for r in json.loads(proc.stdout)}
    # Inject alttext on each <math> for screen-reader accessibility.
    # KaTeX with output:'mathml' does not emit alttext by default; DAISY
    # MathML best practices and Kindle Enhanced Typesetting both prefer
    # an alttext attribute as the fallback for non-MathML readers.
    out = {}
    import re as _re
    for idx, html in raw.items():
        tex = items[int(idx)][1]
        alt = " ".join(tex.split())
        alt_xml = (alt.replace("&", "&amp;")
                      .replace('"', "&quot;")
                      .replace("<", "&lt;")
                      .replace(">", "&gt;"))
        # 1. Strip <semantics>...<annotation>tex</annotation></semantics>
        # wrapper, leaving the bare <mrow> children inside <math>. Some
        # Kindle MathML pathways look only at the first <mrow> child of
        # <math> and ignore semantic markup; rare renderers display the
        # raw <annotation> text. Simpler structure is more robust.
        stripped = _re.sub(
            r"<semantics>(.*?)<annotation\b[^>]*>.*?</annotation>\s*</semantics>",
            r"\1",
            html,
            flags=_re.DOTALL,
        )
        # 2. Inject alttext on the <math> tag (callable replacement so
        # backslashes in the LaTeX source aren't interpreted as regex
        # escapes).
        replacement = f'<math alttext="{alt_xml}"'
        injected = _re.sub(
            r'<math\b(?![^>]*\balttext=)',
            lambda m: replacement,
            stripped,
            count=1,
        )
        out[idx] = injected
    return out


def render_svg(items: list[dict]) -> dict[str, str]:
    payload = [{"id": str(i), "tex": it[1], "display": it[2] == "block"}
               for i, it in enumerate(items)]
    proc = subprocess.run(
        ["node", str(MATHJAX_RENDER)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        env={**os.environ, "NODE_PATH": str(MATHJAX_MODULES)},
        timeout=120,
        encoding="utf-8",
    )
    if proc.returncode != 0:
        raise RuntimeError(f"mathjax failed: {proc.stderr}")
    out = {}
    for r in json.loads(proc.stdout):
        svg = r.get("svg", "")
        # MathJax SVG uses stroke="currentColor" fill="currentColor" to
        # inherit text color. Kindle Previewer's SVG renderer doesn't
        # resolve currentColor inside inline SVG -- the paths draw
        # transparent or are skipped. Replace with explicit black.
        svg = svg.replace('stroke="currentColor"', 'stroke="#000"')
        svg = svg.replace('fill="currentColor"', 'fill="#000"')
        # Convert ex-unit dimensions to px (a single ex ≈ 8px at base
        # font size). ex units are technically valid but some Kindle
        # readers ignore them and fall back to width=0/height=0.
        import re as _re
        def _ex_to_px(m):
            ex = float(m.group(1))
            return f'{m.group(2)}="{int(ex * 8)}px"'
        svg = _re.sub(r'(\d+(?:\.\d+)?)ex"', lambda m: f'{m.group(1)}ex"', svg)
        # actually leave ex units alone; per-renderer it's hit-or-miss
        # but converting introduces its own quirks. Focus on currentColor
        # which is the more likely culprit.
        out[r["id"]] = svg
    return out


# ----------------------------------------------------------------------
# Build the chapter content (shared shape for both EPUBs)
# ----------------------------------------------------------------------

def build_chapter(rendered: dict[str, str], variant: str) -> str:
    """variant: 'mathml' or 'svg' (affects only the label in the heading)."""
    sections = []
    for i, (label, tex, mode, pre, post) in enumerate(TESTS):
        rendered_html = rendered.get(str(i), "")
        if mode == "block":
            block = (
                f'<p>{pre}</p>\n'
                f'<div class="math-block">{rendered_html}</div>\n'
                f'<p>{post}</p>'
            )
        else:
            block = (
                f'<p>{pre} {rendered_html} {post}</p>'
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
<title>Math Test v2 ({variant})</title>
<link rel="stylesheet" type="text/css" href="styles/test.css" />
</head>
<body>
<h1>Math Rendering Test v2 — {variant.upper()}</h1>
<p>Each pattern is shown in prose context — the way real chapters use math.
This is a fair comparison to the user's reading experience.</p>
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
.math-block math { display: block; }
.math-block svg { max-width: 100%; height: auto; }
/* For inline SVG math: align to text baseline */
p svg { vertical-align: middle; }
"""


# ----------------------------------------------------------------------
# Assemble an EPUB from a chapter body
# ----------------------------------------------------------------------

def build_epub(out_path: Path, chapter_body: str, title: str,
               include_mathml_property: bool,
               include_svg_property: bool = False):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    props_parts = []
    if include_mathml_property:
        props_parts.append("mathml")
    if include_svg_property:
        props_parts.append("svg")
    chapter_props = f' properties="{" ".join(props_parts)}"' if props_parts else ""

    # Deterministic v5 UUID from out_path.stem (so re-runs produce same id)
    import uuid as _uuid
    bookid = "urn:uuid:" + str(_uuid.uuid5(_uuid.NAMESPACE_OID, out_path.stem))

    opf = f"""<?xml version="1.0"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="id" version="3.0"
         prefix="rendition: http://www.idpf.org/vocab/rendition/#">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="id">{bookid}</dc:identifier>
    <dc:title>{title}</dc:title>
    <dc:language>en</dc:language>
    <dc:creator>KPVDebug math test harness</dc:creator>
    <dc:description>Per-pattern math rendering reference EPUB for Kindle Previewer 3 debugging.</dc:description>
    <dc:rights>Public domain test EPUB; no copyright claimed.</dc:rights>
    <dc:date>2026-05-15</dc:date>
    <meta property="dcterms:modified">2026-05-15T20:00:00Z</meta>
    <meta property="rendition:layout">reflowable</meta>
    <meta property="rendition:orientation">auto</meta>
    <meta property="rendition:spread">auto</meta>
  </metadata>
  <manifest>
    <item id="page" href="page.xhtml" media-type="application/xhtml+xml"{chapter_props}/>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="css" href="styles/test.css" media-type="text/css"/>
  </manifest>
  <spine><itemref idref="page"/></spine>
</package>"""

    nav = f"""<?xml version="1.0"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head><meta charset="utf-8"/><title>Nav</title></head>
<body><nav epub:type="toc" id="toc" role="doc-toc"><h1>Contents</h1>
<ol><li><a href="page.xhtml">{title}</a></li></ol></nav></body></html>"""

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
        z.writestr("EPUB/page.xhtml", chapter_body)
        z.writestr("EPUB/styles/test.css", CSS)
    print(f"  Wrote {out_path.relative_to(ROOT)}  ({out_path.stat().st_size:,} bytes)")


def main():
    print("Rendering MathML via KaTeX...")
    mathml = render_mathml(TESTS)
    chapter_mathml = build_chapter(mathml, variant="mathml")
    build_epub(
        OUT_DIR / "math-test-v2-mathml.epub",
        chapter_mathml,
        title="Math Test v2 (MathML)",
        include_mathml_property=True,
    )

    print("Rendering SVG via MathJax...")
    svg = render_svg(TESTS)
    chapter_svg = build_chapter(svg, variant="svg")
    build_epub(
        OUT_DIR / "math-test-v2-svg.epub",
        chapter_svg,
        title="Math Test v2 (SVG)",
        include_mathml_property=False,
        include_svg_property=True,  # MathJax outputs inline <svg>
    )

    print()
    print("Open both EPUBs in Kindle Previewer 3 to compare:")
    print(f"  {OUT_DIR / 'math-test-v2-mathml.epub'}")
    print(f"  {OUT_DIR / 'math-test-v2-svg.epub'}")


if __name__ == "__main__":
    main()
