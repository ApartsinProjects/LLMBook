"""Compact HTML test page — 4 math expressions × 4 rendering pipelines.

Produces ONE self-contained HTML file (no external resources) at:
  KDP/output/math-compare.html

Each row is one math expression. Each column is one pipeline. The user
can open the file in any browser OR drop it as an EPUB into Kindle
Previewer 3 (also produced: math-compare.epub).

Use case: take a screenshot of the file in the target reader, feed
back to the model for diagnosis.

Pipelines:
  1. MathML   — KaTeX output:'mathml' (semantics stripped)
  2. SVG      — MathJax output:svg, fontCache:'none', fill:black
  3. HTML     — plain <sub>/<sup>/<i> + CSS .frac/.hat
  4. PNG      — matplotlib mathtext, 300 DPI, embedded as data: URL
"""
from __future__ import annotations
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['text.color'] = 'black'

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


# 4 representative expressions. Keep the set small so the comparison
# fits on one screen.
TESTS = [
    # (label, latex, html_inline, display)
    ("y subscript i (inline)",
     r"y_i",
     '<i>y</i><sub><i>i</i></sub>',
     False),
    ("x squared (inline)",
     r"x^2",
     '<i>x</i><sup>2</sup>',
     False),
    ("one over n fraction",
     r"\frac{1}{n}",
     '<span class="frac"><span class="num">1</span><span class="den"><i>n</i></span></span>',
     False),
    ("MSE block equation",
     r"MSE = \frac{1}{n}\sum_{i=1}^{n}(\hat{y}_i - y_i)^2",
     'MSE = <span class="frac"><span class="num">1</span><span class="den"><i>n</i></span></span>'
     'Σ<sub><i>i</i>=1</sub><sup><i>n</i></sup> '
     '(<span class="hat"><i>y</i></span><sub><i>i</i></sub> − '
     '<i>y</i><sub><i>i</i></sub>)<sup>2</sup>',
     True),
]


def render_mathml() -> dict[str, str]:
    payload = [{"id": str(i), "tex": t[1], "display": t[3]} for i, t in enumerate(TESTS)]
    proc = subprocess.run(
        ["node", str(KATEX_RENDER)],
        input=json.dumps(payload),
        capture_output=True, text=True,
        env={**os.environ, "NODE_PATH": str(KATEX_MODULES)},
        timeout=60, encoding="utf-8",
    )
    proc.check_returncode()
    out = {}
    for r in json.loads(proc.stdout):
        html = r["html"]
        # Strip <semantics>/<annotation>
        html = re.sub(
            r"<semantics>(.*?)<annotation\b[^>]*>.*?</annotation>\s*</semantics>",
            r"\1", html, flags=re.DOTALL,
        )
        out[r["id"]] = html
    return out


def render_svg() -> dict[str, str]:
    payload = [{"id": str(i), "tex": t[1], "display": t[3]} for i, t in enumerate(TESTS)]
    proc = subprocess.run(
        ["node", str(MATHJAX_RENDER)],
        input=json.dumps(payload),
        capture_output=True, text=True,
        env={**os.environ, "NODE_PATH": str(MATHJAX_MODULES)},
        timeout=120, encoding="utf-8",
    )
    proc.check_returncode()
    out = {}
    for r in json.loads(proc.stdout):
        svg = r.get("svg", "")
        svg = svg.replace('stroke="currentColor"', 'stroke="#000"')
        svg = svg.replace('fill="currentColor"', 'fill="#000"')
        out[r["id"]] = svg
    return out


def render_png(tex: str, display: bool) -> str:
    """Return a base64 data: URL for an inline <img>."""
    fontsize = 16 if display else 14
    fig = plt.figure(figsize=(0.1, 0.1), dpi=300)
    fig.patch.set_alpha(0)
    fig.text(0.5, 0.5, f"${tex}$", fontsize=fontsize, ha='center', va='center',
             color='black')
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=300, transparent=True,
                bbox_inches='tight', pad_inches=0.05)
    plt.close(fig)
    b64 = base64.b64encode(buf.getvalue()).decode('ascii')
    return f'data:image/png;base64,{b64}'


CSS = """\
body { font-family: Georgia, serif; line-height: 1.7; margin: 1em auto;
       max-width: 60em; padding: 0 1em; color: #222; background: #fff; }
h1 { font-size: 1.4em; border-bottom: 2px solid #1a4078; padding-bottom: 0.3em; }
h2 { font-size: 1.1em; margin: 1.5em 0 0.3em; color: #1a4078; }
table { width: 100%; border-collapse: collapse; margin: 0.5em 0 1.5em; }
th, td { border: 1px solid #ccc; padding: 0.6em 0.8em; vertical-align: middle;
         text-align: left; font-size: 0.95em; }
th { background: #f4f4f4; font-weight: 700; }
th.col-label { width: 18%; }
th.col-cell { width: 20.5%; text-align: center; }
td.col-label { font-size: 0.85em; color: #555; font-style: italic; }
td.col-cell { text-align: center; }
code { background: #f4f4f4; padding: 0.1em 0.3em; border-radius: 3px;
       font-size: 0.85em; font-family: 'Source Code Pro', Consolas, monospace; }
img.math-inline { vertical-align: middle; max-height: 1.5em; }
img.math-display { max-width: 100%; height: auto; }
/* HTML pipeline visuals */
.frac { display: inline-block; vertical-align: -0.5em; margin: 0 0.15em;
        text-align: center; line-height: 1; }
.frac > .num { display: block; border-bottom: 1px solid currentColor;
               padding: 0 0.2em 0.05em; font-size: 0.9em; }
.frac > .den { display: block; padding: 0.05em 0.2em 0; font-size: 0.9em; }
.hat { display: inline-block; position: relative; padding-top: 0.2em; }
.hat::before { content: "^"; position: absolute; top: -0.4em; left: 0; right: 0;
               text-align: center; font-size: 0.85em; }
sub, sup { line-height: 0; font-size: 0.78em; }
sub { vertical-align: -0.3em; }
sup { vertical-align: 0.55em; }
.note { background: #fffbea; border-left: 3px solid #d4b96a; padding: 0.5em 0.8em;
        margin: 1em 0; font-size: 0.9em; }
"""


def build_html(mathml, svg, png_urls):
    rows = []
    for i, (label, tex, html_inline, display) in enumerate(TESTS):
        idx = str(i)
        # XML-escape the latex source (escape `\` and special chars only)
        tex_esc = tex.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        rows.append(
            f'<tr>'
            f'<td class="col-label">{label}<br/><code>{tex_esc}</code></td>'
            f'<td class="col-cell">{mathml[idx]}</td>'
            f'<td class="col-cell">{svg[idx]}</td>'
            f'<td class="col-cell">{html_inline}</td>'
            f'<td class="col-cell"><img class="{"math-display" if display else "math-inline"}" '
            f'src="{png_urls[idx]}" alt="{tex}"/></td>'
            f'</tr>'
        )
    rows_html = "\n".join(rows)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head>
<meta charset="utf-8" />
<title>Math Pipeline Comparison</title>
<style>{CSS}</style>
</head>
<body>
<h1>Math Pipeline Comparison — 4 expressions × 4 pipelines</h1>
<p class="note">Each <strong>column</strong> is a different rendering pipeline.
Each <strong>row</strong> is the same LaTeX expression rendered four ways.
Screenshot this page in the target reader (browser, Kindle Previewer 3, etc.)
and send back for diagnosis.</p>
<table>
<thead>
<tr>
  <th class="col-label">Expression</th>
  <th class="col-cell">1. MathML</th>
  <th class="col-cell">2. SVG (MathJax)</th>
  <th class="col-cell">3. Plain HTML</th>
  <th class="col-cell">4. PNG (matplotlib)</th>
</tr>
</thead>
<tbody>
{rows_html}
</tbody>
</table>
</body>
</html>
"""


def render_png_bytes(tex: str, display: bool) -> bytes:
    """Same as render_png but return raw bytes (for EPUB file embedding)."""
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


def main():
    print("Rendering MathML (KaTeX)...")
    mathml = render_mathml()
    print("Rendering SVG (MathJax)...")
    svg = render_svg()
    print("Rendering PNG (matplotlib)...")
    # Two forms: data: URIs for the standalone HTML, raw bytes for EPUB file
    png_urls_data = {str(i): render_png(t[1], t[3]) for i, t in enumerate(TESTS)}
    png_bytes_map = {str(i): render_png_bytes(t[1], t[3]) for i, t in enumerate(TESTS)}

    # Single-file HTML (data: URIs are FINE in browsers, OPEN IT IN A BROWSER)
    html_browser = build_html(mathml, svg, png_urls_data)
    html_path = OUT_DIR / "math-compare.html"
    html_path.write_text(html_browser, encoding="utf-8")
    print(f"Wrote {html_path.relative_to(ROOT)} ({html_path.stat().st_size:,} bytes)")

    # EPUB version: KDP strips data: URIs; use img/eq###.png file refs instead.
    # Replace the data: URL src= with relative paths to bundled PNG files.
    png_file_urls = {str(i): f"img/eq{int(i)+1:03d}.png" for i in png_urls_data}
    html_epub = build_html(mathml, svg, png_file_urls)
    epub_path = OUT_DIR / "math-compare.epub"
    bookid = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_OID, "math-compare"))
    # Build manifest items for the PNG files we bundle
    png_manifest_items = "\n    ".join(
        f'<item id="img{int(i)+1:03d}" href="img/eq{int(i)+1:03d}.png" media-type="image/png"/>'
        for i in sorted(png_bytes_map)
    )
    opf = f"""<?xml version="1.0"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="id" version="3.0"
         prefix="rendition: http://www.idpf.org/vocab/rendition/#">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="id">{bookid}</dc:identifier>
    <dc:title>Math Pipeline Comparison</dc:title>
    <dc:language>en</dc:language>
    <meta property="dcterms:modified">2026-05-15T22:00:00Z</meta>
    <meta property="rendition:layout">reflowable</meta>
    <meta property="rendition:orientation">auto</meta>
    <meta property="rendition:spread">auto</meta>
  </metadata>
  <manifest>
    <item id="page" href="page.xhtml" media-type="application/xhtml+xml" properties="mathml svg"/>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    {png_manifest_items}
  </manifest>
  <spine><itemref idref="page"/></spine>
</package>"""
    nav = """<?xml version="1.0"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head><meta charset="utf-8"/><title>Nav</title></head>
<body><nav epub:type="toc"><h1>Contents</h1>
<ol><li><a href="page.xhtml">Math Pipeline Comparison</a></li></ol></nav></body></html>"""

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
        for i, png_bytes in sorted(png_bytes_map.items()):
            z.writestr(f"EPUB/img/eq{int(i)+1:03d}.png", png_bytes)
    print(f"Wrote {epub_path.relative_to(ROOT)} ({epub_path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
