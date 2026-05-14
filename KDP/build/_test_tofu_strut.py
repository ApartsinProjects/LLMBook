"""Test if KaTeX htmlAndMathml output has visible 'tofu strut box'
glyphs when bundled into a tiny test EPUB.

Renders 3 sample formulas (inline + display), wraps in minimal EPUB,
opens in Edge headless print-to-PDF as a Kindle Paperwhite-shape
viewport, then visually inspects via PNG.
"""
import os, subprocess, json, tempfile, shutil, zipfile
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[2]
OUT = Path('E:/temp/tofu_test')
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True)
NODE_PATH = str(ROOT / 'KDP/build/node_modules')

# Render formulas via KaTeX
samples = [
    ('inline_pi', r'p_i', False),
    ('inline_e_neg_z', r'e^{-z}', False),
    ('display_complex', r'\mathcal{L}_{\text{aux}} = \alpha \cdot N \sum_{i=1}^{N} f_i \cdot p_i', True),
]

env = os.environ.copy()
env['NODE_PATH'] = NODE_PATH
renders = {}
for name, tex, display in samples:
    js = (
        "const katex = require('katex');\n"
        f"const r = katex.renderToString({json.dumps(tex)}, "
        f"{{output: 'htmlAndMathml', displayMode: {str(display).lower()}, "
        f"throwOnError: false}});\n"
        "console.log(r);"
    )
    fd, tmp = tempfile.mkstemp(suffix='.js', dir='E:/temp')
    os.close(fd)
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(js)
    try:
        p = subprocess.run(['node', tmp], capture_output=True, text=True,
                           env=env, encoding='utf-8', timeout=30)
        renders[name] = p.stdout.strip()
    finally:
        os.unlink(tmp)
    print(f'{name}: rendered ({len(renders[name])} chars)')

# Build test HTML with the renders embedded
test_html_dir = OUT / 'test_book'
test_html_dir.mkdir()
# Copy KaTeX CSS into the test dir
shutil.copyfile(ROOT / 'vendor' / 'katex' / 'katex.min.css',
                test_html_dir / 'katex.min.css')

# Apply v789-style cleanup (strip vlist-s spans, then check rendering)
import re
def strip_struts(html: str) -> str:
    """Remove empty .vlist-s spans which cause Kindle tofu."""
    return re.sub(r'<span class="vlist-s">\s*[​]*\s*</span>', '', html)

html_body = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<title>KaTeX Tofu Test</title>
<link rel="stylesheet" href="katex.min.css">
<style>
body {{ font-family: Georgia, serif; font-size: 14px; line-height: 1.55;
       margin: 1em; max-width: 600px; }}
h2 {{ font-family: 'Helvetica Neue', sans-serif; color: #1a4078;
      font-size: 1.1em; margin-top: 1.5em; }}
.section {{ padding: 0.5em 0.8em; background: #f6f8fa; border-left: 4px solid #1a4078;
            margin: 0.8em 0; }}
</style>
</head><body>
<h1>KaTeX htmlAndMathml — Tofu Strut Test</h1>

<h2>Sample 1: inline math p<sub>i</sub></h2>
<p>Here, {renders['inline_pi']} is a simple inline subscript that should
sit flush with the surrounding text.</p>

<h2>Sample 2: inline math e<sup>-z</sup></h2>
<p>The sigmoid activation 1/(1+{renders['inline_e_neg_z']}) uses a negative
exponent inline.</p>

<h2>Sample 3: display math L<sub>aux</sub></h2>
<div class="section">{renders['display_complex']}</div>

<h2>Strut sample regions</h2>
<p>The strut spans render as visible boxes if Kindle treats <code>&amp;#8203;</code>
(zero-width space) as a glyph. Count visible boxes above:</p>
<ul>
<li>If 0 visible boxes: KaTeX HTML mode is clean for this reader.</li>
<li>If 1+ boxes per formula: tofu issue exists; need defensive CSS.</li>
</ul>
</body></html>"""

test_html_path = test_html_dir / 'test.html'
test_html_path.write_text(html_body, encoding='utf-8')

# Render in Edge headless print-to-PDF (Kindle Paperwhite shape)
EDGE = r'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
ud = tempfile.mkdtemp(prefix='tofu_', dir='E:/temp')
pdf = OUT / 'tofu_test.pdf'
cmd = [EDGE, '--headless=new', '--disable-gpu', '--no-sandbox',
       '--no-pdf-header-footer', '--run-all-compositor-stages-before-draw',
       '--virtual-time-budget=15000',
       f'--user-data-dir={ud}', f'--print-to-pdf={str(pdf).replace(chr(47), chr(92))}',
       test_html_path.resolve().as_uri()]
subprocess.run(cmd, capture_output=True, timeout=60)
shutil.rmtree(ud, ignore_errors=True)

print(f'\nPDF size: {pdf.stat().st_size} bytes')

doc = fitz.open(str(pdf))
print(f'Pages: {len(doc)}')
for i in range(min(2, len(doc))):
    page = doc.load_page(i)
    pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0), alpha=False)
    pix.save(str(OUT / f'tofu_test_p{i+1}.png'))
    print(f'  wrote tofu_test_p{i+1}.png')

# Count empty vlist-s spans in raw render
print('\n--- Strut span audit ---')
for name, html in renders.items():
    n_struts = html.count('class="vlist-s"')
    print(f'  {name}: {n_struts} vlist-s spans')
