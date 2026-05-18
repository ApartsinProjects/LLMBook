"""Wave 75: Normalize page headers to match canonical templates A/B/C
(part / chapter index / section) per docs/content-audit/HEADER_TEMPLATES.md.

Fixes detected by p2_header_template.py:
- 27 chapter index pages missing <div class="header-search">
- 15 section pages missing <div class="header-search">
- 8 part index pages missing breadcrumb with data-pagefind-meta="part"
- 8 part index pages incorrectly HAVE <div class="header-search">
  (part pages should NOT have search; search lives at chapter/section level)
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

CANON_SEARCH = '<div class="header-search">\n<div id="search"></div>\n</div>\n'


def _classify(filepath: Path) -> str | None:
    name = filepath.name
    parts = filepath.parts
    if name.startswith('section-') and name.endswith('.html'):
        return 'section'
    if name == 'index.html':
        for p in parts[-3:]:
            if p.startswith('module-'):
                return 'chapter'
        try:
            idx = next(i for i, p in enumerate(parts) if p.startswith('part-'))
            if idx + 1 < len(parts) and parts[idx + 1] == name:
                return 'part'
        except StopIteration:
            pass
    return None


# Patterns
HEADER_NAV_END_RE = re.compile(
    r'(<nav\s+class="header-nav">.*?</nav>)\s*\n',
    re.DOTALL | re.IGNORECASE,
)
HEADER_SEARCH_RE = re.compile(
    r'<div\s+class="header-search">.*?</div>\s*</div>\s*\n?',
    re.DOTALL | re.IGNORECASE,
)


def fix_chapter_or_section(text: str) -> tuple[str, int]:
    """Insert canonical header-search block after </nav> if missing."""
    if 'class="header-search"' in text:
        return text, 0
    m = HEADER_NAV_END_RE.search(text)
    if not m:
        return text, 0
    insertion_point = m.end()
    new = text[:insertion_point] + CANON_SEARCH + text[insertion_point:]
    return new, 1


def fix_part(text: str) -> tuple[str, int]:
    """Remove header-search from part pages."""
    new, n = HEADER_SEARCH_RE.subn('', text, count=1)
    return new, n


def main():
    n_chapter_add = 0
    n_section_add = 0
    n_part_remove = 0
    files = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        kind = _classify(p)
        if kind is None:
            continue
        text = p.read_text(encoding='utf-8')
        orig = text
        if kind in ('chapter', 'section'):
            text, n = fix_chapter_or_section(text)
            if n:
                if kind == 'chapter':
                    n_chapter_add += n
                else:
                    n_section_add += n
        elif kind == 'part':
            text, n = fix_part(text)
            if n:
                n_part_remove += n
        if text != orig:
            p.write_text(text, encoding='utf-8')
            files += 1
    print(f'Chapter pages: header-search added in {n_chapter_add}')
    print(f'Section pages: header-search added in {n_section_add}')
    print(f'Part pages: header-search removed from {n_part_remove}')
    print(f'Total files touched: {files}')


if __name__ == '__main__':
    main()
