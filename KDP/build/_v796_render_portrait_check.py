"""v796: Render specific chapters in portrait single-column (Kindle
Paperwhite shape) and capture EXACT pixel proof of:
  1. Math floating (eta, nabla L)
  2. Tall math-block boxes (L_total formula)
  3. About-the-authors layout (bio card starts after header)

Output:
  E:/temp/epub_audit_v796/<slug>_p<n>.png

This is a fidelity check: NO injected column-count CSS, just the
actual EPUB CSS in a portrait-shaped page.
"""
from __future__ import annotations
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from pathlib import Path

try:
    import fitz
except ImportError:
    print("Install pymupdf: pip install pymupdf", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[2]
EPUB = ROOT / 'KDP/output/building-conversational-ai-llms-agents.epub'
OUT = Path('E:/temp/epub_audit_v796')
EDGE = Path('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe')

# Slugs of chapters we want to check
TARGETS = [
    # Math floating: appendix-a section 3 ("eta" / "nabla L")
    'appendices-appendix-a-mathematical-foundations-section-a-3',
    # Tall math-block: section 0.1 ("L_total" regularization formula)
    'part-1-foundations-module-00-ml-pytorch-foundations-section-0-1',
    # About the Authors
    'front-matter-about-authors',
]

# Portrait Kindle Paperwhite aspect: 6 inches x 8 inches (close to 1080 x 1440 px).
PORTRAIT_INJECT = '''
<style id="portrait-render">
@page {
    size: 6in 8in;     /* portrait, Kindle Paperwhite shape */
    margin: 0.4in 0.4in;
}
html, body {
    column-count: 1 !important;
    max-width: none !important;
    width: 100% !important;
    font-size: 14px !important;
}
main.content {
    max-width: none !important;
    padding: 0 !important;
    margin: 0 !important;
}
</style>
'''


def render(html_path: Path, out_pdf: Path) -> bool:
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    user_data_dir = tempfile.mkdtemp(prefix='portrait_', dir='E:/temp')
    try:
        cmd = [str(EDGE), '--headless=new', '--disable-gpu', '--no-sandbox',
               '--no-pdf-header-footer',
               '--run-all-compositor-stages-before-draw',
               '--virtual-time-budget=15000',
               f'--user-data-dir={user_data_dir}',
               f'--print-to-pdf={str(out_pdf).replace("/", chr(92))}',
               html_path.resolve().as_uri()]
        subprocess.run(cmd, capture_output=True, text=True, timeout=240)
        return out_pdf.exists() and out_pdf.stat().st_size > 1000
    finally:
        shutil.rmtree(user_data_dir, ignore_errors=True)


def main():
    if OUT.exists():
        shutil.rmtree(OUT, ignore_errors=True)
    OUT.mkdir(parents=True)
    extract_dir = OUT / '_extracted'
    extract_dir.mkdir()
    with zipfile.ZipFile(EPUB) as zf:
        zf.extractall(extract_dir)
    chapters_dir = extract_dir / 'EPUB' / 'chapters'
    found = []
    for slug in TARGETS:
        for f in chapters_dir.glob(f'*{slug}*.xhtml'):
            found.append((slug, f))
            break
    print(f'Rendering {len(found)} chapters in portrait shape')
    for slug, src in found:
        # Inject portrait CSS
        content = src.read_text(encoding='utf-8')
        if '</head>' in content:
            content = content.replace('</head>', PORTRAIT_INJECT + '</head>', 1)
        else:
            content = PORTRAIT_INJECT + content
        modified = src.with_suffix('.portrait.xhtml')
        modified.write_text(content, encoding='utf-8')
        pdf_path = OUT / f'{slug}.pdf'
        if not render(modified, pdf_path):
            print(f'  FAIL {slug}')
            continue
        doc = fitz.open(str(pdf_path))
        n = min(8, len(doc))
        print(f'  {slug}: {n} pages')
        for i in range(n):
            page = doc.load_page(i)
            mat = fitz.Matrix(1.8, 1.8)   # 1.8x for high-res look
            pix = page.get_pixmap(matrix=mat, alpha=False)
            out_png = OUT / f'{slug}_p{i+1}.png'
            pix.save(str(out_png))
        doc.close()
    print(f'\nDone. {OUT}')


if __name__ == '__main__':
    main()
