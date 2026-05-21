"""Wave 9 step H sub-task: close the section 7.3 gap in Ch 7 (Modern LLM Landscape).

Ch 7 has section-7.1, section-7.2, section-7.4 (skipping 7.3). Renumber 7.4 -> 7.3.
"""
from pathlib import Path
import re
import subprocess
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
CH7_DIR = ROOT / 'part-2-understanding-llms' / 'module-07-modern-llm-landscape'

SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs'}


def rewrite_section_metadata(file_path, old_y, new_y):
    text = file_path.read_text(encoding='utf-8')
    text = re.sub(rf'<title>Section 7\.{old_y}:', f'<title>Section 7.{new_y}:', text)
    text = re.sub(rf'(<meta content=")Section 7\.{old_y}:', rf'\1Section 7.{new_y}:', text)
    text = re.sub(r'<div class="page-current">Section 7\.\d+</div>',
                  f'<div class="page-current">Section 7.{new_y}</div>', text)
    text = re.sub(r'<span class="bc-current">Section 7\.\d+</span>',
                  f'<span class="bc-current">Section 7.{new_y}</span>', text)
    text = re.sub(rf'\bid="7-{old_y}-', f'id="7-{new_y}-', text)
    text = re.sub(rf'\bhref="#7-{old_y}-', f'href="#7-{new_y}-', text)
    text = re.sub(rf'\bSection 7\.{old_y}\b', f'Section 7.{new_y}', text)
    text = re.sub(rf'\b7\.{old_y}\.(\d+)\b', rf'7.{new_y}.\1', text)
    file_path.write_text(text, encoding='utf-8')


def main():
    src = CH7_DIR / 'section-7.4.html'
    tmp = CH7_DIR / 'section-7.3.html.__tmp__'
    dst = CH7_DIR / 'section-7.3.html'

    if not src.exists():
        print('  src does not exist; nothing to do')
        return
    if dst.exists():
        print('  dst already exists; conflict — abort')
        return

    subprocess.run(['git', 'mv', str(src), str(tmp)], cwd=ROOT, capture_output=True)
    subprocess.run(['git', 'mv', str(tmp), str(dst)], cwd=ROOT, capture_output=True)
    rewrite_section_metadata(dst, 4, 3)
    print('Renamed 7.4 -> 7.3')

    # Global cross-ref rewrite
    n_files = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        orig = text
        text = re.sub(
            r'(href="[^"]*?module-07-modern-llm-landscape/)section-7\.4\.html',
            r'\1section-7.3.html',
            text
        )
        if text != orig:
            p.write_text(text, encoding='utf-8')
            n_files += 1
    print(f'Cross-refs updated in {n_files} files')

    # Update Ch 7 index — replace 7.4 card with 7.3
    idx = CH7_DIR / 'index.html'
    text = idx.read_text(encoding='utf-8')
    text = text.replace('section-7.4.html', 'section-7.3.html')
    text = text.replace('7.4', '7.3')
    idx.write_text(text, encoding='utf-8')
    print('Ch 7 index updated')


if __name__ == '__main__':
    main()
