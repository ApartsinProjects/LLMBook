"""Build a tiny test EPUB with a small set of representative math
expressions, to verify Kindle rendering after each CSS change.

The test page hits all the script/limit/fraction patterns the user
reported as broken:
  - subscript:        y_i
  - superscript:      x^2
  - sub-and-sup:      x_i^2
  - hat (mover):      \hat{y}
  - fraction:         \frac{1}{n}
  - square root:      \sqrt{x}
  - sum with limits:  \sum_{i=1}^{n}
  - gradient:         \nabla L
  - inline sentences with mixed math
  - block (display) math expressions
"""
from pathlib import Path
import subprocess
import shutil
import json
import zipfile
import io
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "KDP" / "output"
OUT_EPUB = OUT_DIR / "math-sample.epub"
KATEX_RENDER = ROOT / "KDP" / "build" / "render_math.js"
KATEX_MODULES = Path("E:/Tools/katex/node_modules")

# Test expressions (LaTeX → label)
TESTS = [
    # (label, tex, display)
    ("inline-subscript",   r"y_{i}",                          False),
    ("inline-superscript", r"x^{2}",                          False),
    ("inline-subsup",      r"x_{i}^{2}",                      False),
    ("inline-hat",         r"\hat{y}",                        False),
    ("inline-frac",        r"\frac{1}{n}",                    False),
    ("inline-sqrt",        r"\sqrt{x}",                       False),
    ("inline-sum",         r"\sum_{i=1}^{n} x_i",             False),
    ("inline-grad",        r"\nabla L",                       False),
    ("inline-eta",         r"\eta",                           False),
    ("block-MSE",          r"\operatorname{MSE} = (1/n) \sum (\hat{y}_{i} - y_{i})^{2}", True),
    ("block-CE",           r"L = -\frac{1}{n}\sum_{i=1}^{n} y_i \log(p_i)",            True),
    ("block-weight-update",r"w_{\text{new}} = w_{\text{old}} - \eta \nabla L(w_{\text{old}})", True),
    ("block-sigmoid",      r"\sigma(x) = \frac{1}{1 + e^{-x}}",                          True),
]


def render_via_katex(tex_items):
    """Call render_math.js to get the MathML HTML for each item."""
    payload = json.dumps([
        {"id": str(i), "tex": tex, "display": disp}
        for i, (_, tex, disp) in enumerate(tex_items)
    ])
    proc = subprocess.run(
        ["node", str(KATEX_RENDER)],
        input=payload,
        capture_output=True,
        text=True,
        env={**__import__("os").environ, "NODE_PATH": str(KATEX_MODULES)},
        timeout=30,
        encoding="utf-8",
    )
    if proc.returncode != 0:
        raise RuntimeError(f"katex failed: {proc.stderr}")
    rendered = json.loads(proc.stdout)
    return {r["id"]: r["html"] for r in rendered}


def main():
    print("Rendering math expressions via KaTeX...")
    rendered = render_via_katex(TESTS)

    # Build a single XHTML page that exercises each pattern
    rows_html = []
    for i, (label, tex, disp) in enumerate(TESTS):
        math_html = rendered.get(str(i), "")
        marker = "BLOCK" if disp else "INLINE"
        rows_html.append(
            f'<tr><td>{label}</td>'
            f'<td><code>{tex}</code></td>'
            f'<td>{marker}</td>'
            f'<td class="math-cell">{math_html}</td></tr>'
        )

    rows_html.append(
        '<tr><td colspan="4" style="padding:1em 0;">'
        '<strong>Inline sentence:</strong> The gradient '
        f'{rendered.get("7","")} tells us the direction of steepest descent. '
        'The learning rate '
        f'{rendered.get("8","")} controls step size. '
        'For each example, the sub-index '
        f'{rendered.get("0","")} runs from 1 to N.'
        '</td></tr>'
    )

    body = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head>
<meta charset="utf-8" />
<title>Math Rendering Sample</title>
<link rel="stylesheet" type="text/css" href="../styles/katex.min.css" />
<link rel="stylesheet" type="text/css" href="../styles/epub_overrides.css" />
</head>
<body>
<h1>Math Rendering Test Sample</h1>
<p>One row per math pattern that has rendered badly on Kindle. The
"Rendered" column should show proper sub/superscripts, fractions
stacked, hats above letters, etc.</p>
<table>
<thead>
<tr>
  <th>Label</th><th>LaTeX source</th><th>Mode</th><th>Rendered</th>
</tr>
</thead>
<tbody>
{chr(10).join(rows_html)}
</tbody>
</table>
</body>
</html>
"""
    # Assemble a minimal EPUB so we can open in Kindle Previewer
    print("Assembling test EPUB...")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # Use the production CSS file
    katex_css_src = Path("E:/Tools/katex/node_modules/katex/dist/katex.min.css")
    overrides_css_src = ROOT / "KDP" / "build" / "epub_overrides.css"

    with zipfile.ZipFile(OUT_EPUB, "w") as z:
        # mimetype (uncompressed, first)
        zi = zipfile.ZipInfo("mimetype")
        zi.compress_type = zipfile.ZIP_STORED
        z.writestr(zi, "application/epub+zip")
        z.writestr("META-INF/container.xml", """<?xml version="1.0"?>
<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">
  <rootfiles><rootfile media-type="application/oebps-package+xml" full-path="EPUB/content.opf"/></rootfiles>
</container>""")
        # OPF
        z.writestr("EPUB/content.opf", """<?xml version="1.0"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="id" version="3.0" prefix="rendition: http://www.idpf.org/vocab/rendition/#">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="id">urn:uuid:math-sample</dc:identifier>
    <dc:title>Math Rendering Sample</dc:title>
    <dc:language>en</dc:language>
    <meta property="dcterms:modified">2026-05-15T19:00:00Z</meta>
    <meta property="rendition:layout">reflowable</meta>
  </metadata>
  <manifest>
    <item id="page" href="page.xhtml" media-type="application/xhtml+xml" properties="mathml"/>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="katex" href="styles/katex.min.css" media-type="text/css"/>
    <item id="overrides" href="styles/epub_overrides.css" media-type="text/css"/>
  </manifest>
  <spine><itemref idref="nav"/><itemref idref="page"/></spine>
</package>""")
        z.writestr("EPUB/nav.xhtml", """<?xml version="1.0"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head><meta charset="utf-8"/><title>Nav</title></head>
<body><nav epub:type="toc"><ol><li><a href="page.xhtml">Math Sample</a></li></ol></nav></body>
</html>""")
        z.writestr("EPUB/page.xhtml", body)
        # CSS files
        if katex_css_src.exists():
            z.writestr("EPUB/styles/katex.min.css", katex_css_src.read_text(encoding="utf-8"))
        if overrides_css_src.exists():
            z.writestr("EPUB/styles/epub_overrides.css", overrides_css_src.read_text(encoding="utf-8"))

    size = OUT_EPUB.stat().st_size
    print(f"Wrote {OUT_EPUB.relative_to(ROOT)}  ({size:,} bytes)")
    print()
    print("Open in Kindle Previewer 3 (drag-drop) to inspect math rendering.")
    print("Each row of the table should show one MathML pattern.")


if __name__ == "__main__":
    main()
