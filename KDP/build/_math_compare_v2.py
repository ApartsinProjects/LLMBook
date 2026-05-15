"""Math pipeline comparison v2 — refined variants per pipeline.

After the v1 comparison, each pipeline's failure pattern is known:
  MathML: renders but at ~10% size (KPV3 ignores CSS on <math>)
  SVG:    renders correctly but at small (16px-equivalent) MathJax default
  HTML:   uses body Georgia font, no math typography
  PNG:    already publication-quality

This v2 tests REFINEMENTS for each pipeline side-by-side:

  Cols:
    1. MathML default (stripped <semantics>)
    2. MathML w/ mathsize="big" displaystyle="true" + outer span font-size:1.5em
    3. SVG MathJax default (fontCache='none', fill=black)
    4. SVG with scale=1.5 + outer span CSS
    5. HTML w/ <sub>/<sup>/<i>+ CSS .frac
    6. HTML w/ Unicode math italic letters (𝑥 𝑦) + larger size
    7. PNG matplotlib CM 300dpi
    8. PNG matplotlib STIX (different fontset)

Single self-contained HTML at KDP/output/math-compare-v2.html and
matching EPUB at math-compare-v2.epub.
"""
from __future__ import annotations
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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


TESTS = [
    # (label, latex, display, html_v1, html_v2_unicode)
    # html_v1 uses plain <sub>/<sup>/<i>; html_v2 uses Unicode math italics.
    ("y_i",
     r"y_i", False,
     '<i>y</i><sub><i>i</i></sub>',
     '𝑦<sub>𝑖</sub>'),
    ("x^2",
     r"x^2", False,
     '<i>x</i><sup>2</sup>',
     '𝑥<sup>2</sup>'),
    ("1/n fraction",
     r"\frac{1}{n}", False,
     '<span class="frac"><span class="num">1</span><span class="den"><i>n</i></span></span>',
     '<span class="frac"><span class="num">1</span><span class="den">𝑛</span></span>'),
    ("MSE block",
     r"MSE = \frac{1}{n}\sum_{i=1}^{n}(\hat{y}_i - y_i)^2", True,
     'MSE = <span class="frac"><span class="num">1</span><span class="den"><i>n</i></span></span>'
     'Σ<sub><i>i</i>=1</sub><sup><i>n</i></sup> '
     '(<span class="hat"><i>y</i></span><sub><i>i</i></sub> − '
     '<i>y</i><sub><i>i</i></sub>)<sup>2</sup>',
     '<span style="font-size:1.1em;">MSE = '
     '<span class="frac"><span class="num">1</span><span class="den">𝑛</span></span>'
     '∑<sub>𝑖=1</sub><sup>𝑛</sup> '
     '(<span class="hat">𝑦</span><sub>𝑖</sub> − 𝑦<sub>𝑖</sub>)<sup>2</sup>'
     '</span>'),
]


# ---------- pipeline renderers ----------

def render_mathml_default(items):
    payload = [{"id": str(i), "tex": t[1], "display": t[2]} for i, t in enumerate(items)]
    proc = subprocess.run(
        ["node", str(KATEX_RENDER)],
        input=json.dumps(payload),
        capture_output=True, text=True,
        env={**os.environ, "NODE_PATH": str(KATEX_MODULES)},
        timeout=60, encoding="utf-8")
    proc.check_returncode()
    out = {}
    for r in json.loads(proc.stdout):
        html = r["html"]
        # Strip <semantics>/<annotation>
        html = re.sub(
            r"<semantics>(.*?)<annotation\b[^>]*>.*?</annotation>\s*</semantics>",
            r"\1", html, flags=re.DOTALL)
        out[r["id"]] = html
    return out


def render_mathml_big(mathml_default):
    """Variant: inject mathsize='big' + displaystyle='true' + wrap in outer
    span with explicit larger font-size. Tests whether KPV3 honors any of:
    - <math> attributes (mathsize, displaystyle)
    - CSS font-size on a parent <span>
    - CSS font-size directly on <math>
    """
    out = {}
    for k, html in mathml_default.items():
        # Add attrs to <math> tag
        modified = re.sub(
            r'<math\b',
            '<math mathsize="big" displaystyle="true" style="font-size: 1.5em;"',
            html, count=1)
        # Wrap in outer span with CSS font-size
        modified = (
            f'<span style="font-size: 1.5em; line-height: 1.4;">'
            f'{modified}</span>'
        )
        out[k] = modified
    return out


def render_svg_default(items):
    payload = [{"id": str(i), "tex": t[1], "display": t[2]} for i, t in enumerate(items)]
    proc = subprocess.run(
        ["node", str(MATHJAX_RENDER)],
        input=json.dumps(payload),
        capture_output=True, text=True,
        env={**os.environ, "NODE_PATH": str(MATHJAX_MODULES)},
        timeout=120, encoding="utf-8")
    proc.check_returncode()
    out = {}
    for r in json.loads(proc.stdout):
        svg = r.get("svg", "")
        # 1. Replace currentColor with explicit black (Kindle Previewer
        #    doesn't resolve currentColor through <use> shadow DOM and
        #    can leave glyphs invisible).
        svg = svg.replace('stroke="currentColor"', 'stroke="#000"')
        svg = svg.replace('fill="currentColor"', 'fill="#000"')
        # 2. Convert ex-unit width/height to explicit pixels. KPV3
        #    sometimes ignores ex/em units and falls back to width=0/
        #    height=0; explicit px guarantees a visible bounding box.
        #    Conversion: 1 ex ≈ 12 px (matches the em:24 / ex:12 we set
        #    in tex2svg.js).
        def _ex_to_px(m):
            attr = m.group(1)
            val = float(m.group(2))
            unit = m.group(3)
            unit_to_px = {'ex': 12, 'em': 24, 'pt': 1.33, 'px': 1}
            return f'{attr}="{val * unit_to_px.get(unit, 1):.1f}px"'
        svg = re.sub(
            r'(width|height)="(\d+(?:\.\d+)?)(ex|em|pt)"',
            _ex_to_px, svg)
        out[r["id"]] = svg
    return out


def render_svg_scaled(svg_default, scale=1.5):
    """Variant: further multiply px sizes by `scale`, NO wrapper span.

    Earlier (v15.20) the wrapper span had display: inline-block which
    actually shrank the rendered size on Kindle Previewer 3 (because
    KPV3's default `svg { max-width: 100% }` was letting unwrapped
    SVGs expand to fill their container in test-table cells; wrapping
    in inline-block defeated that expansion). In real prose context
    there is no container to expand into, so the wrapper was the only
    case where it mattered, and there it hurt. Drop it.
    """
    out = {}
    for k, svg in svg_default.items():
        def mult_px(m):
            attr = m.group(1)
            val = float(m.group(2))
            return f'{attr}="{val * scale:.1f}px"'
        modified = re.sub(
            r'(width|height)="(\d+(?:\.\d+)?)px"',
            mult_px, svg)
        out[k] = modified
    return out


def render_png_cm(tex, display, fontsize=None):
    """matplotlib mathtext, Computer Modern."""
    fs = fontsize if fontsize is not None else (16 if display else 14)
    matplotlib.rcParams['mathtext.fontset'] = 'cm'
    fig = plt.figure(figsize=(0.1, 0.1), dpi=300)
    fig.patch.set_alpha(0)
    fig.text(0.5, 0.5, f"${tex}$", fontsize=fs, ha='center', va='center', color='black')
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=300, transparent=True,
                bbox_inches='tight', pad_inches=0.05)
    plt.close(fig)
    return buf.getvalue()


def render_png_stix(tex, display, fontsize=None):
    """matplotlib mathtext, STIX (similar to Times Math)."""
    fs = fontsize if fontsize is not None else (16 if display else 14)
    matplotlib.rcParams['mathtext.fontset'] = 'stix'
    fig = plt.figure(figsize=(0.1, 0.1), dpi=300)
    fig.patch.set_alpha(0)
    fig.text(0.5, 0.5, f"${tex}$", fontsize=fs, ha='center', va='center', color='black')
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=300, transparent=True,
                bbox_inches='tight', pad_inches=0.05)
    plt.close(fig)
    return buf.getvalue()


# ---------- HTML / EPUB assembly ----------

CSS = """\
body { font-family: Georgia, serif; line-height: 1.7; margin: 1em auto;
       max-width: 80em; padding: 0 1em; color: #222; background: #fff; }
h1 { font-size: 1.3em; border-bottom: 2px solid #1a4078; padding-bottom: 0.3em; }
.note { background: #fffbea; border-left: 3px solid #d4b96a;
        padding: 0.5em 0.8em; margin: 1em 0; font-size: 0.85em; }

table { width: 100%; border-collapse: collapse; margin: 0.5em 0 1.5em;
        font-size: 0.88em; }
th, td { border: 1px solid #ccc; padding: 0.5em; vertical-align: middle;
         text-align: center; }
th { background: #f0f4f8; font-weight: 700; font-size: 0.85em; }
th.legend { background: #e8eef5; }
td.expr { width: 12%; text-align: left; font-size: 0.78em; color: #555;
          font-style: italic; }
td.expr code { font-style: normal; background: #f4f4f4;
               padding: 0.1em 0.3em; border-radius: 3px; font-size: 0.95em; }

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

img.math { vertical-align: middle; max-height: 2em; }
img.math-display { max-width: 100%; height: auto; }
"""


def build_html(mathml_def, mathml_big, svg_def, svg_scl, png_cm, png_stix, png_format="data"):
    """png_format: 'data' → base64 data URLs, 'file' → img/eq#.png references."""
    rows = []
    for i, t in enumerate(TESTS):
        idx = str(i)
        label, tex, display, html_v1, html_v2 = t
        tex_disp = tex.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

        # PNG cells
        if png_format == "data":
            png_cm_b64 = base64.b64encode(png_cm[idx]).decode('ascii')
            png_stix_b64 = base64.b64encode(png_stix[idx]).decode('ascii')
            cm_src = f"data:image/png;base64,{png_cm_b64}"
            stix_src = f"data:image/png;base64,{png_stix_b64}"
        else:
            cm_src = f"img/eq{i+1:02d}-cm.png"
            stix_src = f"img/eq{i+1:02d}-stix.png"

        cls = "math-display" if display else "math"

        rows.append(
            f'<tr>'
            f'<td class="expr"><strong>{label}</strong><br/><code>{tex_disp}</code></td>'
            f'<td>{mathml_def[idx]}</td>'
            f'<td>{mathml_big[idx]}</td>'
            f'<td>{svg_def[idx]}</td>'
            f'<td>{svg_scl[idx]}</td>'
            f'<td>{html_v1}</td>'
            f'<td>{html_v2}</td>'
            f'<td><img class="{cls}" src="{cm_src}" alt="{tex_disp}"/></td>'
            f'<td><img class="{cls}" src="{stix_src}" alt="{tex_disp}"/></td>'
            f'</tr>'
        )

    rows_html = "\n".join(rows)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head>
<meta charset="utf-8" />
<title>Math Pipeline Comparison v2</title>
<style>{CSS}</style>
</head>
<body>
<h1>Math Pipeline Comparison v2 — refined variants per pipeline</h1>
<p class="note">Each <strong>row</strong> is the same LaTeX expression. Each
<strong>pair of columns</strong> tests two variants of one pipeline: a
default (left) and an attempted refinement (right). The goal is to
find which refinement (if any) significantly improves visual quality
in Kindle Previewer 3 compared to the default.</p>
<table>
<thead>
<tr>
  <th class="legend" rowspan="2">Expression</th>
  <th colspan="2">1. MathML</th>
  <th colspan="2">2. SVG (MathJax)</th>
  <th colspan="2">3. HTML</th>
  <th colspan="2">4. PNG (matplotlib)</th>
</tr>
<tr>
  <th>1a. default</th>
  <th>1b. mathsize="big" + 1.5em wrapper</th>
  <th>2a. default</th>
  <th>2b. scale 1.5×</th>
  <th>3a. plain &lt;sub&gt;/&lt;sup&gt;</th>
  <th>3b. Unicode math italics (𝑦 𝑖)</th>
  <th>4a. CM font</th>
  <th>4b. STIX font</th>
</tr>
</thead>
<tbody>
{rows_html}
</tbody>
</table>
</body>
</html>
"""


def main():
    print("MathML default…")
    mathml_def = render_mathml_default(TESTS)
    print("MathML big…")
    mathml_big = render_mathml_big(mathml_def)
    print("SVG default…")
    svg_def = render_svg_default(TESTS)
    print("SVG scaled…")
    svg_scl = render_svg_scaled(svg_def, scale=1.5)
    print("PNG CM…")
    png_cm = {str(i): render_png_cm(t[1], t[2]) for i, t in enumerate(TESTS)}
    print("PNG STIX…")
    png_stix = {str(i): render_png_stix(t[1], t[2]) for i, t in enumerate(TESTS)}

    # Standalone HTML (data: URIs for PNG)
    html_browser = build_html(mathml_def, mathml_big, svg_def, svg_scl,
                              png_cm, png_stix, png_format="data")
    html_path = OUT_DIR / "math-compare-v2.html"
    html_path.write_text(html_browser, encoding="utf-8")
    print(f"Wrote {html_path.relative_to(ROOT)} ({html_path.stat().st_size:,} bytes)")

    # EPUB (PNG as files)
    html_epub = build_html(mathml_def, mathml_big, svg_def, svg_scl,
                           png_cm, png_stix, png_format="file")
    epub_path = OUT_DIR / "math-compare-v2.epub"
    bookid = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_OID, "math-compare-v2"))
    png_manifest = "\n    ".join(
        f'<item id="cm{i+1:02d}" href="img/eq{i+1:02d}-cm.png" media-type="image/png"/>\n    '
        f'<item id="stix{i+1:02d}" href="img/eq{i+1:02d}-stix.png" media-type="image/png"/>'
        for i in range(len(TESTS))
    )
    opf = f"""<?xml version="1.0"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="id" version="3.0"
         prefix="rendition: http://www.idpf.org/vocab/rendition/#">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="id">{bookid}</dc:identifier>
    <dc:title>Math Pipeline Comparison v2</dc:title>
    <dc:language>en</dc:language>
    <meta property="dcterms:modified">2026-05-15T23:00:00Z</meta>
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
<ol><li><a href="page.xhtml">Math v2</a></li></ol></nav></body></html>"""
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
            z.writestr(f"EPUB/img/eq{i+1:02d}-cm.png", png_cm[str(i)])
            z.writestr(f"EPUB/img/eq{i+1:02d}-stix.png", png_stix[str(i)])
    print(f"Wrote {epub_path.relative_to(ROOT)} ({epub_path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
