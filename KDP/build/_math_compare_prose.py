"""Math pipeline comparison: PROSE LAYOUT (no table).

Every test EPUB so far has used a <table> for layout. Kindle's
built-in `svg { max-width: 100% }` lets SVGs expand to fill the
table cell, which makes the SVG pipeline look misleadingly great.
Real chapters use prose paragraphs, where SVGs render at their
intrinsic px size with no expansion.

This test puts each expression in real prose context (h2 + paragraph
with inline math + paragraph), once per pipeline. The same LaTeX
expression appears 4 times consecutively, once each via MathML,
SVG, HTML, and PNG, so the visual differences are obvious.

Output:
  math-compare-prose.html  (browser baseline; data: URIs for PNG)
  math-compare-prose.epub  (Kindle Previewer 3; PNGs as files)
"""
from __future__ import annotations
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
matplotlib.rcParams['mathtext.fontset'] = 'cm'

from pathlib import Path
import base64
import io
import json
import os
import re
import subprocess
import uuid
import zipfile

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "KDP" / "output"
KATEX_RENDER = ROOT / "KDP" / "build" / "render_math.js"
KATEX_MODULES = Path("E:/Tools/katex/node_modules")
MATHJAX_RENDER = Path("E:/Tools/mathjax/tex2svg.js")
MATHJAX_MODULES = Path("E:/Tools/mathjax/node_modules")


# (label, latex, display, prose_before, prose_after, html_inline)
TESTS = [
    ("y subscript i",
     r"y_i", False,
     "The output for the i-th example is denoted",
     ", where i runs from 1 to N.",
     '<i>y</i><sub><i>i</i></sub>'),
    ("x squared",
     r"x^2", False,
     "We square the residual as",
     "before summing across examples.",
     '<i>x</i><sup>2</sup>'),
    ("one over n",
     r"\frac{1}{n}", False,
     "Averaging the loss gives the factor",
     "in front of the sum.",
     '<span class="frac"><span class="num">1</span><span class="den"><i>n</i></span></span>'),
    ("MSE block equation",
     r"MSE = \frac{1}{n}\sum_{i=1}^{n}(\hat{y}_i - y_i)^2",
     True,
     "For regression, the most common loss is Mean Squared Error:",
     "Squaring the residual penalizes large errors more heavily.",
     'MSE = <span class="frac"><span class="num">1</span><span class="den"><i>n</i></span></span>'
     'Σ<sub><i>i</i>=1</sub><sup><i>n</i></sup> '
     '(<span class="hat"><i>y</i></span><sub><i>i</i></sub> − '
     '<i>y</i><sub><i>i</i></sub>)<sup>2</sup>'),
]


def render_mathml(items):
    payload = [{"id": str(i), "tex": t[1], "display": t[2]} for i, t in enumerate(items)]
    proc = subprocess.run(
        ["node", str(KATEX_RENDER)],
        input=json.dumps(payload), capture_output=True, text=True,
        env={**os.environ, "NODE_PATH": str(KATEX_MODULES)},
        timeout=60, encoding="utf-8")
    proc.check_returncode()
    out = {}
    for r in json.loads(proc.stdout):
        html = r["html"]
        html = re.sub(
            r"<semantics>(.*?)<annotation\b[^>]*>.*?</annotation>\s*</semantics>",
            r"\1", html, flags=re.DOTALL)
        out[r["id"]] = html
    return out


def render_svg(items):
    payload = [{"id": str(i), "tex": t[1], "display": t[2]} for i, t in enumerate(items)]
    proc = subprocess.run(
        ["node", str(MATHJAX_RENDER)],
        input=json.dumps(payload), capture_output=True, text=True,
        env={**os.environ, "NODE_PATH": str(MATHJAX_MODULES)},
        timeout=120, encoding="utf-8")
    proc.check_returncode()
    out = {}
    for r in json.loads(proc.stdout):
        svg = r.get("svg", "")
        svg = svg.replace('stroke="currentColor"', 'stroke="#000"')
        svg = svg.replace('fill="currentColor"', 'fill="#000"')
        def _u(m):
            attr, val, unit = m.group(1), float(m.group(2)), m.group(3)
            r = {'ex': 12, 'em': 24, 'pt': 1.33, 'px': 1}.get(unit, 1)
            return f'{attr}="{val * r:.1f}px"'
        svg = re.sub(r'(width|height)="(\d+(?:\.\d+)?)(ex|em|pt)"', _u, svg)
        out[r["id"]] = svg
    return out


def render_png(tex, display):
    fontsize = 16 if display else 14
    fig = plt.figure(figsize=(0.1, 0.1), dpi=300)
    fig.patch.set_alpha(0)
    fig.text(0.5, 0.5, f"${tex}$", fontsize=fontsize, ha='center', va='center',
             color='black')
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=300, transparent=True,
                bbox_inches='tight', pad_inches=0.05)
    plt.close(fig)
    return buf.getvalue()


CSS = """\
body { font-family: Georgia, serif; line-height: 1.7; margin: 1em auto;
       max-width: 38em; padding: 0 1em; color: #222; background: #fff; }
h1 { font-size: 1.4em; border-bottom: 2px solid #1a4078; padding-bottom: 0.3em;
     margin-top: 0; }
h2 { font-size: 1.15em; color: #1a4078; margin: 1.8em 0 0.2em;
     border-bottom: 1px solid #ddd; padding-bottom: 0.15em; }
h3 { font-size: 0.95em; color: #555; margin: 0.6em 0 0.1em;
     text-transform: uppercase; letter-spacing: 0.05em; font-weight: 700; }
p { margin: 0.3em 0 0.7em; }
code { background: #f4f4f4; padding: 0.1em 0.3em; border-radius: 3px;
       font-size: 0.85em; font-family: Consolas, monospace; }
.section-card { background: #fafafa; border-left: 3px solid #1a4078;
                padding: 0.5em 0.9em; margin: 0.4em 0 1.2em; }
.note { background: #fffbea; border-left: 3px solid #d4b96a;
        padding: 0.5em 0.8em; margin: 1em 0; font-size: 0.88em; }
.math-block { text-align: center; margin: 0.6em 0; }
.math-block img.math-display { max-width: 100%; height: auto; }
img.math-inline { vertical-align: middle; max-height: 1.5em; }
/* HTML pipeline visuals */
.frac { display: inline-block; vertical-align: -0.5em; margin: 0 0.15em;
        text-align: center; line-height: 1; }
.frac > .num { display: block; border-bottom: 1px solid currentColor;
               padding: 0 0.2em 0.05em; font-size: 0.9em; }
.frac > .den { display: block; padding: 0.05em 0.2em 0; font-size: 0.9em; }
.hat { display: inline-block; position: relative; padding-top: 0.2em; }
.hat::before { content: "^"; position: absolute; top: -0.4em; left: 0;
               right: 0; text-align: center; font-size: 0.85em; }
sub, sup { line-height: 0; font-size: 0.78em; }
sub { vertical-align: -0.3em; }
sup { vertical-align: 0.55em; }
"""


def build_chapter(mathml, svg, png_urls):
    """Each expression as h2 + 4 pipeline sections, each section being
    a real-prose paragraph + (display math block if applicable) + closer.
    """
    sections = []
    for i, (label, tex, display, pre, post, html_inline) in enumerate(TESTS):
        idx = str(i)
        tex_esc = tex.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

        def block_for(rendered, png=False):
            """Wrap rendered math in a prose context."""
            if display:
                if png:
                    inner = (
                        f'<p>{pre}</p>'
                        f'<div class="math-block">'
                        f'<img class="math-display" src="{rendered}" alt="{tex_esc}"/>'
                        f'</div>'
                        f'<p>{post}</p>'
                    )
                else:
                    inner = (
                        f'<p>{pre}</p>'
                        f'<div class="math-block">{rendered}</div>'
                        f'<p>{post}</p>'
                    )
            else:
                if png:
                    inner = (
                        f'<p>{pre} '
                        f'<img class="math-inline" src="{rendered}" alt="{tex_esc}"/>'
                        f' {post}</p>'
                    )
                else:
                    inner = f'<p>{pre} {rendered} {post}</p>'
            return inner

        sections.append(
            f'<h2>Expression <code>{tex_esc}</code> (&#8220;{label}&#8221;)</h2>\n'
            f'<div class="section-card">\n'
            f'<h3>1. MathML</h3>\n{block_for(mathml[idx])}\n'
            f'</div>\n'
            f'<div class="section-card">\n'
            f'<h3>2. SVG (MathJax)</h3>\n{block_for(svg[idx])}\n'
            f'</div>\n'
            f'<div class="section-card">\n'
            f'<h3>3. Plain HTML</h3>\n{block_for(html_inline)}\n'
            f'</div>\n'
            f'<div class="section-card">\n'
            f'<h3>4. PNG (matplotlib)</h3>\n{block_for(png_urls[idx], png=True)}\n'
            f'</div>'
        )

    body = "\n".join(sections)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head>
<meta charset="utf-8" />
<title>Math Pipeline Comparison (Prose Layout)</title>
<style>{CSS}</style>
</head>
<body>
<h1>Math Pipeline Comparison (Prose Layout)</h1>
<p class="note">No tables. Each math expression appears 4 times consecutively,
once per pipeline, each in a real-prose context (paragraph + math + paragraph).
This is the TRUE production rendering: what readers will see in chapter prose.
SVGs render at their intrinsic px size (no table-cell expansion).</p>
{body}
</body>
</html>
"""


def main():
    print("Rendering MathML…")
    mathml = render_mathml(TESTS)
    print("Rendering SVG…")
    svg = render_svg(TESTS)
    print("Rendering PNG…")
    png_bytes = {str(i): render_png(t[1], t[2]) for i, t in enumerate(TESTS)}

    # HTML (data: URIs)
    png_urls_data = {k: f'data:image/png;base64,{base64.b64encode(b).decode("ascii")}'
                     for k, b in png_bytes.items()}
    html_browser = build_chapter(mathml, svg, png_urls_data)
    html_path = OUT_DIR / "math-compare-prose.html"
    html_path.write_text(html_browser, encoding="utf-8")
    print(f"Wrote {html_path.relative_to(ROOT)} ({html_path.stat().st_size:,} bytes)")

    # EPUB (PNG files)
    png_urls_files = {k: f"img/eq{int(k)+1:02d}.png" for k in png_bytes}
    html_epub = build_chapter(mathml, svg, png_urls_files)
    epub_path = OUT_DIR / "math-compare-prose.epub"
    bookid = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_OID, "math-compare-prose"))
    png_manifest = "\n    ".join(
        f'<item id="img{i+1:02d}" href="img/eq{i+1:02d}.png" media-type="image/png"/>'
        for i in range(len(TESTS))
    )
    opf = f"""<?xml version="1.0"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="id" version="3.0"
         prefix="rendition: http://www.idpf.org/vocab/rendition/#">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="id">{bookid}</dc:identifier>
    <dc:title>Math Pipeline Comparison (Prose)</dc:title>
    <dc:language>en</dc:language>
    <meta property="dcterms:modified">2026-05-15T23:30:00Z</meta>
    <meta property="rendition:layout">reflowable</meta>
    <meta property="rendition:orientation">auto</meta>
    <meta property="rendition:spread">auto</meta>
  </metadata>
  <manifest>
    <item id="page" href="page.xhtml" media-type="application/xhtml+xml" properties="mathml svg"/>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    {png_manifest}
  </manifest>
  <spine><itemref idref="page"/></spine>
</package>"""
    nav = """<?xml version="1.0"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head><meta charset="utf-8"/><title>Nav</title></head>
<body><nav epub:type="toc"><h1>Contents</h1>
<ol><li><a href="page.xhtml">Math Pipeline Comparison (Prose)</a></li></ol></nav></body></html>"""
    with zipfile.ZipFile(epub_path, "w") as z:
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
        z.writestr("EPUB/page.xhtml", html_epub)
        for i in range(len(TESTS)):
            z.writestr(f"EPUB/img/eq{i+1:02d}.png", png_bytes[str(i)])
    print(f"Wrote {epub_path.relative_to(ROOT)} ({epub_path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
