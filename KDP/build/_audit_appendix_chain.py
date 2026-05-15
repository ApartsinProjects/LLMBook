"""Audit: appendix navigation chain consistency.

Each section.next should reference the next section in numerical order,
or appendix's index.html as the boundary. Same with .prev.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import re

ROOT = Path('E:/Projects/BookBlogsHome/LLMBook/appendices')


def sort_key(p):
    """Sort section files by numerical section index."""
    stem = p.stem  # e.g., 'section-s.4'
    if stem == 'index':
        return -1
    m = re.match(r'section-([a-zA-Z]+)\.(\d+)', stem)
    if not m:
        return 999
    return int(m.group(2))


def get_nav(p):
    try:
        s = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
    except Exception:
        return None, None, None
    nav = s.find('nav', class_='chapter-nav')
    if not nav:
        return None, None, None
    prev = nav.find('a', class_='prev')
    nxt = nav.find('a', class_='next')
    up = nav.find('a', class_='up')
    return (prev.get('href') if prev else None,
            nxt.get('href') if nxt else None,
            up.get('href') if up else None)


issues = []
for app_dir in sorted(ROOT.iterdir()):
    if not app_dir.is_dir():
        continue
    files = sorted(app_dir.glob('*.html'), key=sort_key)
    if not files:
        continue
    # files[0] = index.html, then sections
    for i, f in enumerate(files):
        prev_href, next_href, up_href = get_nav(f)
        if next_href is None and prev_href is None:
            continue

        # Expected prev/next based on order
        expected_prev = files[i - 1].name if i > 0 else None
        expected_next = files[i + 1].name if i < len(files) - 1 else None

        # For first section (index.html), prev should be from previous appendix
        # For last section, next should be from next appendix
        if f.name == 'index.html':
            # prev should be from previous appendix's last section
            if prev_href and prev_href.startswith('section-'):
                issues.append(f'{f}: index.prev is local section: {prev_href} '
                              f'(should be from previous appendix)')
            if next_href != 'section-' + app_dir.name.split('-')[1] + '.1.html' \
               and next_href and not next_href.startswith('section-'):
                pass
        else:
            # section file - prev should be prev section or index
            if expected_prev and prev_href:
                if prev_href != expected_prev and not prev_href.startswith('../'):
                    issues.append(f'{f.relative_to(ROOT)}: prev={prev_href} '
                                  f'(expected {expected_prev})')
            if expected_next and next_href:
                if next_href != expected_next and not next_href.startswith('../'):
                    issues.append(f'{f.relative_to(ROOT)}: next={next_href} '
                                  f'(expected {expected_next})')
            # Last section: next should be next-appendix/index.html
            if i == len(files) - 1 and next_href:
                if not next_href.startswith('../'):
                    issues.append(f'{f.relative_to(ROOT)}: last section next={next_href} '
                                  f'(should be next appendix)')

        # First section after index: prev should be 'index.html', not external
        if i == 1 and prev_href and prev_href != 'index.html':
            issues.append(f'{f.relative_to(ROOT)}: first section prev={prev_href} '
                          f'(should be index.html)')


# Also check: which appendices have "first section.prev=appendix/index" vs
# "first section.prev=prev_appendix/last_section"
print('=== APPENDIX FIRST-SECTION.PREV PATTERN ===')
for app_dir in sorted(ROOT.iterdir()):
    if not app_dir.is_dir():
        continue
    files = sorted(app_dir.glob('*.html'), key=sort_key)
    if len(files) < 2:
        continue
    first_section = files[1]
    prev_href, _, _ = get_nav(first_section)
    print(f'{app_dir.name}: section1.prev = {prev_href}')

print()
print(f'=== ISSUES ({len(issues)}) ===')
for issue in issues[:60]:
    print(f'  {issue}')
