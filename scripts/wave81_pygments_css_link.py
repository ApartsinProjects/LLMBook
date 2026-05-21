"""Wave 81: Add pygments.css link to pages that have pygments-highlighted
code spans but don't link the stylesheet (so the code shows up plain).

For each affected page, insert
  <link href="{path-to-styles}/pygments.css" rel="stylesheet"/>
right after the existing book.css link.

Detected: 20 pages (front-matter/look-inside-preview, module-XX-tools-of-the-trade
indexes, several module-36 sections, etc.).
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

BOOK_CSS_LINK_RE = re.compile(
    r'(<link\s+href="([^"]*?)styles/book\.css"\s+rel="stylesheet"/>)',
    re.IGNORECASE,
)


def fix_file(p: Path) -> int:
    text = p.read_text(encoding='utf-8')
    if 'pygments.css' in text:
        return 0
    if 'pygments-highlighted' not in text:
        return 0

    m = BOOK_CSS_LINK_RE.search(text)
    if not m:
        return 0
    book_link = m.group(1)
    css_prefix = m.group(2)  # e.g., "../" or "../../"
    pyg_link = f'<link href="{css_prefix}styles/pygments.css" rel="stylesheet"/>'
    new_text = text.replace(book_link, book_link + '\n' + pyg_link, 1)
    if new_text == text:
        return 0
    p.write_text(new_text, encoding='utf-8')
    return 1


def main():
    n = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        if fix_file(p):
            n += 1
            print(f'  + pygments.css link: {p.relative_to(ROOT)}')
    print(f'\nTotal pages updated: {n}')


if __name__ == '__main__':
    main()
