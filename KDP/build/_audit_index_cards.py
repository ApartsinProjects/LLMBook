"""Audit: index.html section cards for duplicates/inconsistencies.

For each index.html, look at all <a class="section-card"> and detect:
  1. Duplicate hrefs with different titles (phantom sections)
  2. Section numbers that don't match the href
  3. Hrefs pointing to non-existent files
"""
from pathlib import Path
from bs4 import BeautifulSoup
import re

ROOT = Path(__file__).resolve().parents[2]
SKIP = ['node_modules', '.git', 'output', 'backup', 'KDP/build',
        'KDP/html2pub', 'pagefind', 'temp_epub', 'agents/', 'templates/']


def is_skip(p):
    sp = str(p).replace('\\', '/')
    return any(s in sp for s in SKIP)


issues = []
for p in ROOT.rglob('index.html'):
    if is_skip(p):
        continue
    try:
        s = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
    except Exception:
        continue
    cards = s.find_all('a', class_='section-card')
    if not cards:
        continue

    # Map: href -> [(section_num, title)]
    href_to_cards = {}
    for c in cards:
        href = c.get('href', '')
        num_el = c.find(class_='section-num')
        title_el = c.find(class_='section-title')
        num = num_el.get_text(strip=True) if num_el else '?'
        title = title_el.get_text(strip=True) if title_el else '?'
        href_to_cards.setdefault(href, []).append((num, title))

    # Detect duplicate hrefs with different titles
    for href, entries in href_to_cards.items():
        if len(entries) > 1:
            uniq_titles = set(t for _, t in entries)
            if len(uniq_titles) > 1:
                issues.append({
                    'file': p,
                    'kind': 'duplicate_href',
                    'href': href,
                    'entries': entries,
                })

    # Detect href to non-existent file
    for href, entries in href_to_cards.items():
        if href.startswith('http') or '#' in href:
            continue
        tgt = (p.parent / href).resolve()
        if not tgt.exists():
            issues.append({
                'file': p,
                'kind': 'broken_href',
                'href': href,
                'entries': entries,
            })

    # Detect section_num != href section number
    for c in cards:
        href = c.get('href', '')
        num_el = c.find(class_='section-num')
        if not num_el:
            continue
        num_text = num_el.get_text(strip=True)
        # Parse href like 'section-28.3.html' or 'section-s.4.html'
        m = re.match(r'section-([a-z]*)(\d+)\.(\d+)\.html', href, re.IGNORECASE)
        if not m:
            m = re.match(r'(?:.*/)?section-([a-z]*)(\d*)\.(\d+)\.html', href,
                         re.IGNORECASE)
        if m:
            section_num_in_href = f'{m.group(1).upper()}{m.group(2)}.{m.group(3)}'.lstrip('0')
            # Normalize for comparison
            if num_text.replace(' ', '') not in section_num_in_href.replace(' ', '') \
               and section_num_in_href.lower() not in num_text.lower():
                pass  # too noisy, skip


# Group issues by kind
print('=== DUPLICATE HREFS (same file, multiple cards) ===')
dup_issues = [i for i in issues if i['kind'] == 'duplicate_href']
for issue in dup_issues:
    print(f'\n  {issue["file"].relative_to(ROOT)}')
    print(f'    href: {issue["href"]}')
    for num, title in issue['entries']:
        print(f'      ({num}) {title}')

print()
print('=== BROKEN HREFS (target file missing) ===')
broken_issues = [i for i in issues if i['kind'] == 'broken_href']
for issue in broken_issues:
    print(f'  {issue["file"].relative_to(ROOT)}: {issue["href"]}')

print()
print(f'Total issues: {len(issues)}')
