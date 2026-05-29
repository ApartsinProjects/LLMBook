"""v902: Remove phantom section cards from index.html files.

Root cause: when sections were consolidated/renumbered, the index pages
kept the OLD cards pointing to the NEW (consolidated) files. This creates
"phantom cards" — multiple cards with the same href but different titles.

Strategy:
  - For each index.html, look at all .section-card links
  - Group by href
  - Keep only ONE card per href: the one whose title matches the actual
    section file's <h1>
  - If no card matches, keep the first as fallback (but log)
  - Also remove "Section 28.0.X" cards where 28.0.X has no file
"""
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
import re

ROOT = Path(__file__).resolve().parents[2]
SKIP = ['node_modules', '.git', 'output', 'backup', 'KDP/build',
        'KDP/html2epub', 'pagefind', 'temp_epub', 'agents/', 'templates/']


def is_skip(p):
    sp = str(p).replace('\\', '/')
    return any(s in sp for s in SKIP)


def get_section_title(section_file):
    if not section_file.exists():
        return None
    try:
        s = BeautifulSoup(section_file.read_text(encoding='utf-8'), 'html.parser')
        h1 = s.find('h1')
        return h1.get_text(strip=True) if h1 else None
    except Exception:
        return None


def normalize_href(href, base_dir):
    """Resolve href to an absolute path (str) for dedup comparison."""
    try:
        return str((base_dir / href).resolve())
    except Exception:
        return href


def fix_index(idx, dry_run=True):
    s = BeautifulSoup(idx.read_text(encoding='utf-8'), 'html.parser')
    cards = s.find_all('a', class_='section-card')
    if not cards:
        return 0

    base = idx.parent

    # Group by RESOLVED href (so ../module-28/section-28.6 and section-28.6 are same)
    by_href = {}
    for c in cards:
        href = c.get('href', '')
        key = normalize_href(href, base)
        by_href.setdefault(key, []).append(c)

    # For each href with duplicates, decide which to keep
    n_removed = 0
    for resolved_key, group in by_href.items():
        if len(group) <= 1:
            continue
        # Resolve href to find actual section
        tgt = Path(resolved_key)
        actual_title = get_section_title(tgt)
        if not actual_title:
            # Can't determine canonical; keep first, remove rest
            keep = group[0]
            for c in group[1:]:
                # Remove the card and its <li> wrapper if standalone
                li = c.find_parent('li')
                if li and len(li.find_all('a', class_='section-card')) == 1:
                    li.decompose()
                else:
                    c.decompose()
                n_removed += 1
                if dry_run:
                    title_el = c.find(class_='section-title') if c.parent else None
                    pass
            continue

        # Find the card whose title matches actual_title
        keep = None
        for c in group:
            title_el = c.find(class_='section-title')
            if title_el and title_el.get_text(strip=True) == actual_title:
                keep = c
                break
        if keep is None:
            # No match — keep first
            keep = group[0]

        # Remove the others
        for c in group:
            if c is keep:
                continue
            title_el = c.find(class_='section-title')
            phantom_title = title_el.get_text(strip=True) if title_el else '?'
            phantom_href = c.get('href', '')
            li = c.find_parent('li')
            if li and len(li.find_all('a', class_='section-card')) == 1:
                li.decompose()
            else:
                c.decompose()
            n_removed += 1
            if dry_run:
                print(f'    WOULD REMOVE phantom: href={phantom_href} title="{phantom_title}"')

    # Also check for orphan <li></li> empty wrappers
    for li in s.find_all('li'):
        if not li.find('a') and not li.get_text(strip=True):
            li.decompose()

    # Also: the "section-grid" div at the bottom (module 28 case) — these
    # are supplementary cards. If they duplicate existing cards (by href),
    # consolidate the unique ones into the main sections-list.
    grids = s.find_all('div', class_='section-grid')
    for grid in grids:
        # Find all RESOLVED hrefs already in the main sections-list
        main_list = s.find('ul', class_='sections-list')
        existing = set()
        if main_list:
            for c in main_list.find_all('a', class_='section-card'):
                existing.add(normalize_href(c.get('href', ''), base))

        for c in grid.find_all('a', class_='section-card'):
            href = c.get('href', '')
            key = normalize_href(href, base)
            if key in existing:
                # Already there, remove from grid
                c.decompose()
                n_removed += 1
            else:
                # Move it into main list. Wrap in <li>
                if main_list:
                    new_li = s.new_tag('li')
                    new_li.append(c.extract())
                    main_list.append(new_li)
                    existing.add(key)

        # Remove empty grid
        if not grid.get_text(strip=True):
            grid.decompose()

    # Sort sections-list items by section number from the section-num span
    main_list = s.find('ul', class_='sections-list')
    if main_list:
        def section_sort_key(li):
            card = li.find('a', class_='section-card')
            if not card:
                return (999, 999)
            num_el = card.find(class_='section-num')
            if not num_el:
                return (999, 999)
            num_text = num_el.get_text(strip=True)
            # Parse "28.3" or "S.4" or "AB.5"
            m = re.match(r'([A-Z]*)(\d*)\.(\d+)', num_text, re.IGNORECASE)
            if m:
                # For alpha prefixes use 0, for numeric use the number
                if m.group(2):
                    chap = int(m.group(2))
                else:
                    chap = 0
                sec = int(m.group(3))
                return (chap, sec)
            return (999, 999)

        items = main_list.find_all('li', recursive=False)
        # Normalize hrefs to local-relative (drop ../module-XX/ prefix when same module)
        for li in items:
            card = li.find('a', class_='section-card')
            if not card:
                continue
            href = card.get('href', '')
            # If href starts with ../$current_module/section-, strip the prefix
            cur_mod = idx.parent.name
            prefix = f'../{cur_mod}/'
            if href.startswith(prefix):
                card['href'] = href[len(prefix):]
        items_sorted = sorted(items, key=section_sort_key)
        if items != items_sorted:
            # Reorder
            for li in items_sorted:
                main_list.append(li.extract())

    if n_removed > 0 and not dry_run:
        idx.write_text(str(s), encoding='utf-8')
    return n_removed


if __name__ == '__main__':
    import sys
    DRY = '--apply' not in sys.argv
    if DRY:
        print('DRY RUN. Pass --apply to write changes.')
    print()

    total = 0
    n_files = 0
    for p in ROOT.rglob('index.html'):
        if is_skip(p):
            continue
        if DRY:
            print(f'\nChecking: {p.relative_to(ROOT)}')
        n = fix_index(p, dry_run=DRY)
        if n:
            total += n
            n_files += 1
            print(f'  {p.relative_to(ROOT)}: {n} phantom cards removed')

    print(f'\nTotal phantom cards removed: {total} across {n_files} files')
