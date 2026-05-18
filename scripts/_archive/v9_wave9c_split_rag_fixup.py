"""Wave 9 step C fixup: fix internal cross-refs and migrate images after RAG split.

After v9_wave9c_split_rag.py runs, sections within Ch 32 still have inline links
that point at "section-32.X.html" with the OLD numbering, and Ch 35 sections
have the same. Plus images referenced from Ch 35 sections still live in the
Ch 32 images dir.

This script:
  1. Rewrites bare hrefs `section-32.X.html` inside Ch 32 / Ch 35 section files
     based on the move mapping. Same-module links stay relative; cross-module
     links become `../module-XX-slug/section-Y.Z.html`.
  2. Copies images referenced by Ch 35 sections from Ch 32 images dir to Ch 35.
  3. Fixes the Ch 32 index.html — the script's auto-card replace left some
     orphan section cards in place; this rewrites them cleanly.
"""
from pathlib import Path
import re
import shutil
import subprocess
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
PART = 'part-7-retrieval-information-extraction-with-llms'
CH32_DIR = ROOT / PART / 'module-32-rag'
CH35_DIR = ROOT / PART / 'module-35-advanced-rag'

# old_y -> (new_module, new_y)
MOVE_MAP = {
    1: ('module-32-rag', 1),
    2: ('module-35-advanced-rag', 1),
    3: ('module-35-advanced-rag', 2),
    4: ('module-32-rag', 2),
    5: ('module-32-rag', 3),
    6: ('module-35-advanced-rag', 5),
    7: ('module-35-advanced-rag', 3),
    8: ('module-35-advanced-rag', 4),
    9: ('module-32-rag', 4),
}


def rewrite_bare_section_hrefs(file_path, current_module):
    """Rewrite hrefs like href="section-32.X.html" inside a section file."""
    text = file_path.read_text(encoding='utf-8')
    orig = text

    def replace(m):
        prefix = m.group(1)
        old_y = int(m.group(2))
        anchor = m.group(3) or ''
        if old_y not in MOVE_MAP:
            return m.group(0)
        new_module, new_y = MOVE_MAP[old_y]
        new_ch = 32 if new_module == 'module-32-rag' else 35
        if new_module == current_module:
            return f'{prefix}section-{new_ch}.{new_y}.html{anchor}'
        else:
            return f'{prefix}../{new_module}/section-{new_ch}.{new_y}.html{anchor}'

    text = re.sub(
        r'(href=")section-32\.(\d+)\.html(#[^"]*)?',
        replace,
        text
    )
    if text != orig:
        file_path.write_text(text, encoding='utf-8')
        return True
    return False


def migrate_images():
    """Copy images referenced by Ch 35 sections from Ch 32 images dir."""
    ch32_img = CH32_DIR / 'images'
    ch35_img = CH35_DIR / 'images'
    ch35_img.mkdir(exist_ok=True)

    # Find image refs in Ch 35 sections
    needed = set()
    for f in sorted(CH35_DIR.glob('section-*.html')):
        text = f.read_text(encoding='utf-8')
        for m in re.finditer(r'src="images/([^"]+)"', text):
            needed.add(m.group(1))

    moved = 0
    for img in needed:
        src = ch32_img / img
        dst = ch35_img / img
        if src.exists() and not dst.exists():
            # git mv to preserve history
            result = subprocess.run(
                ['git', 'mv', str(src), str(dst)],
                cwd=ROOT, capture_output=True, text=True
            )
            if result.returncode == 0:
                moved += 1
            else:
                # fallback: plain copy if git mv complains
                shutil.copy2(src, dst)
                moved += 1
        elif not src.exists():
            print(f'  MISSING: {img} not in Ch 32 images')
    print(f'Migrated {moved} images to Ch 35')


def fix_ch32_index():
    """Rewrite Ch 32 index.html cleanly: 4 section cards + chapter card."""
    idx = CH32_DIR / 'index.html'
    text = idx.read_text(encoding='utf-8')

    titles = [
        (1, 'RAG Architecture & Fundamentals'),
        (2, 'Deep Research & Agentic RAG'),
        (3, 'Structured Data & Text-to-SQL'),
        (4, 'Source Attribution and Citation in RAG'),
    ]
    cards = '\n'.join(
        f'<li><a class="section-card" href="section-32.{y}.html">\n'
        f'<span class="section-num">32.{y}</span>\n'
        f'<span class="section-title">{title}</span>\n'
        f'<span class="section-desc">RAG fundamentals.</span>\n'
        f'</a></li>'
        for y, title in titles
    )
    # Replace ALL sections-list ULs with our clean one (count=0 = all)
    text, n = re.subn(
        r'<ul class="sections-list">[\s\S]*?</ul>',
        f'<ul class="sections-list">\n{cards}\n</ul>',
        text,
        count=1
    )
    # Strip any leftover orphan <li class="section-card"...
    text = re.sub(
        r'<li><a class="section-card" href="section-32\.[5-9]\.html">[\s\S]*?</a></li>\s*',
        '',
        text
    )
    idx.write_text(text, encoding='utf-8')
    print(f'Ch 32 index: rewrote {n} sections-list block(s)')


def main():
    # 1. Fix cross-refs in Ch 32 sections
    n32 = 0
    for f in sorted(CH32_DIR.glob('section-*.html')):
        if rewrite_bare_section_hrefs(f, 'module-32-rag'):
            n32 += 1
    print(f'Ch 32 sections updated: {n32}')

    # 2. Fix cross-refs in Ch 35 sections
    n35 = 0
    for f in sorted(CH35_DIR.glob('section-*.html')):
        if rewrite_bare_section_hrefs(f, 'module-35-advanced-rag'):
            n35 += 1
    print(f'Ch 35 sections updated: {n35}')

    # 3. Migrate images
    migrate_images()

    # 4. Fix Ch 32 index
    fix_ch32_index()


if __name__ == '__main__':
    main()
