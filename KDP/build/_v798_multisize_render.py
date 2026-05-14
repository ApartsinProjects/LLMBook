"""v798: Render the EPUB at multiple device shapes to verify reflow.

Devices simulated:
  paperwhite       — 6.0 x 8.0 in   (Kindle Paperwhite, portrait, 1072x1448)
  fire-portrait    — 7.0 x 10.5 in  (Kindle Fire HD, portrait)
  fire-landscape   — 10.5 x 7.0 in  (Kindle Fire HD, landscape — 2 columns)
  ipad-portrait    — 8.0 x 10.5 in  (iPad, portrait)
  ipad-landscape   — 10.5 x 8.0 in  (iPad, landscape — 2 columns)
  phone            — 4.0 x 7.0 in   (phone-sized e-reader app)

For each device, render the same 5 representative chapters so issues
can be compared side-by-side:
  - Section 0.1 (math-heavy)
  - Section 6.4 (the curation-funnel section, E21018 site)
  - Section 11.1 (code-heavy)
  - Section 19.3 (RAG, diagrams + callouts)
  - Front matter index (chapter-header / epigraph)

Output: E:/temp/epub_multisize/<device>/<slug>_p<n>.png

Independent of _v792 and _v796 scripts; sets per-device viewport
and column rules.
"""
from __future__ import annotations
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

try:
    import fitz
except ImportError:
    raise SystemExit("Install pymupdf: pip install pymupdf")

ROOT = Path(__file__).resolve().parents[2]
EPUB = ROOT / 'KDP/output/building-conversational-ai-llms-agents.epub'
OUT = Path('E:/temp/epub_multisize')
EDGE = Path('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe')

DEVICES = {
    "paperwhite": dict(page="6in 8in",      cols=1, fontpx=14),
    "fire-portrait": dict(page="7in 10.5in", cols=1, fontpx=15),
    "fire-landscape": dict(page="10.5in 7in", cols=2, fontpx=14),
    "ipad-portrait":  dict(page="8in 10.5in", cols=1, fontpx=15),
    "ipad-landscape": dict(page="10.5in 8in", cols=2, fontpx=15),
    "phone":          dict(page="4in 7in",   cols=1, fontpx=13),
}

TARGET_SLUGS = [
    'part-1-foundations-module-00-ml-pytorch-foundations-section-0-1',
    'part-2-understanding-llms-module-06-pretraining-scaling-laws-section-6-4',
    'part-3-working-with-llms-module-11-llm-apis-section-11-1',
    'part-5-retrieval-conversation-module-19-rag-section-19-3',
    'front-matter-index',
]


def device_css(cfg: dict) -> str:
    cols = cfg['cols']
    return f'''<style id="multisize">
@page {{ size: {cfg['page']}; margin: 0.4in 0.4in; }}
html, body {{
    column-count: {cols} !important;
    column-gap: {('1.5em' if cols > 1 else '0')} !important;
    column-fill: auto !important;
    font-size: {cfg['fontpx']}px !important;
    max-width: none !important;
    width: 100% !important;
}}
{('body { column-rule: 1px dashed #c0c0c0 !important; }' if cols > 1 else '')}
main.content {{ max-width: none !important; padding: 0 !important; margin: 0 !important; }}
.chapter-header {{ column-span: all !important; }}
</style>'''


def render(html: Path, pdf: Path) -> bool:
    pdf.parent.mkdir(parents=True, exist_ok=True)
    user_data = tempfile.mkdtemp(prefix='ms_', dir='E:/temp')
    try:
        cmd = [
            str(EDGE), '--headless=new', '--disable-gpu', '--no-sandbox',
            '--no-pdf-header-footer', '--run-all-compositor-stages-before-draw',
            '--virtual-time-budget=20000',
            f'--user-data-dir={user_data}',
            f'--print-to-pdf={str(pdf).replace("/", chr(92))}',
            html.resolve().as_uri(),
        ]
        subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        return pdf.exists() and pdf.stat().st_size > 1000
    finally:
        shutil.rmtree(user_data, ignore_errors=True)


def pdf_to_pngs(pdf: Path, out_dir: Path, stem: str, max_pages: int = 4):
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(str(pdf))
    n = min(max_pages, len(doc))
    for i in range(n):
        page = doc.load_page(i)
        mat = fitz.Matrix(1.4, 1.4)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        pix.save(str(out_dir / f'{stem}_p{i+1}.png'))
    doc.close()
    return n


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
    for slug in TARGET_SLUGS:
        for f in chapters_dir.glob(f'*{slug}*.xhtml'):
            found.append((slug, f))
            break

    print(f'Rendering {len(found)} chapters across {len(DEVICES)} devices')
    for dev_name, cfg in DEVICES.items():
        dev_out = OUT / dev_name
        dev_out.mkdir(parents=True, exist_ok=True)
        inject = device_css(cfg)
        print(f'\n[{dev_name}] page={cfg["page"]} cols={cfg["cols"]}')
        for slug, src in found:
            content = src.read_text(encoding='utf-8')
            if '</head>' in content:
                content = content.replace('</head>', inject + '</head>', 1)
            tmp = src.with_suffix(f'.{dev_name}.xhtml')
            tmp.write_text(content, encoding='utf-8')
            pdf = dev_out / f'{slug[:50]}.pdf'
            if not render(tmp, pdf):
                print(f'    FAIL {slug[:50]}')
                continue
            n = pdf_to_pngs(pdf, dev_out, slug[:50], max_pages=3)
            print(f'    {slug[:50]} -> {n} pages')
    print(f'\nAll done. Output: {OUT}')


if __name__ == '__main__':
    main()
