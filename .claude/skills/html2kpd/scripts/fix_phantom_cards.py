"""Remove phantom section cards from index.html files.

Phantom card = an <a class="section-card"> entry in an index.html that
points to a real file but whose title doesn't match the target's <h1>.
This is the typical result of section consolidation/renumbering: the
index page kept the OLD cards pointing to the NEW (consolidated) files.

Strategy per index.html:
  1. Group cards by RESOLVED href (so `./section-X` and
     `../module-X/section-X` are recognized as the same target).
  2. For each href group, keep ONE card: the one whose section-title
     matches the target file's <h1>. If no match, keep first.
  3. Consolidate trailing <div class="section-grid"> cards into the
     main <ul class="sections-list"> (dedup by resolved href).
  4. Sort cards by section number from the section-num span.
  5. Normalize hrefs (drop ../$samemodule/ prefix).

Usage:
    python fix_phantom_cards.py --root <book-root>           # dry-run
    python fix_phantom_cards.py --root <book-root> --apply   # write

Idempotent: re-running on a clean tree produces no changes.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup


DEFAULT_SKIP = [
    'node_modules', '.git', 'output', 'backup', 'pagefind',
    'temp_epub', 'agents/', 'templates/', 'KDP/build', 'KDP/html2pub',
]


def is_skip(p: Path, skip: list[str]) -> bool:
    sp = str(p).replace('\\', '/')
    return any(s in sp for s in skip)


def get_section_title(section_file: Path) -> str | None:
    if not section_file.exists():
        return None
    try:
        s = BeautifulSoup(section_file.read_text(encoding='utf-8'),
                           'html.parser')
        h1 = s.find('h1')
        return h1.get_text(strip=True) if h1 else None
    except Exception:
        return None


def normalize_href(href: str, base_dir: Path) -> str:
    try:
        return str((base_dir / href).resolve())
    except Exception:
        return href


def section_sort_key(li) -> tuple:
    card = li.find('a', class_='section-card')
    if not card:
        return (999, 999)
    num_el = card.find(class_='section-num')
    if not num_el:
        return (999, 999)
    num_text = num_el.get_text(strip=True)
    m = re.match(r'([A-Z]*)(\d*)\.(\d+)', num_text, re.IGNORECASE)
    if m:
        chap = int(m.group(2)) if m.group(2) else 0
        sec = int(m.group(3))
        return (chap, sec)
    return (999, 999)


def fix_index(idx: Path, root: Path, dry_run: bool) -> int:
    s = BeautifulSoup(idx.read_text(encoding='utf-8'), 'html.parser')
    cards = s.find_all('a', class_='section-card')
    if not cards:
        return 0

    base = idx.parent
    by_href = {}
    for c in cards:
        href = c.get('href', '')
        key = normalize_href(href, base)
        by_href.setdefault(key, []).append(c)

    n_removed = 0
    for resolved_key, group in by_href.items():
        if len(group) <= 1:
            continue
        tgt = Path(resolved_key)
        actual_title = get_section_title(tgt)
        if not actual_title:
            # Can't determine canonical; keep first
            keep = group[0]
            for c in group[1:]:
                li = c.find_parent('li')
                if li and len(li.find_all('a', class_='section-card')) == 1:
                    li.decompose()
                else:
                    c.decompose()
                n_removed += 1
            continue

        keep = None
        for c in group:
            title_el = c.find(class_='section-title')
            if title_el and title_el.get_text(strip=True) == actual_title:
                keep = c
                break
        if keep is None:
            keep = group[0]

        for c in group:
            if c is keep:
                continue
            title_el = c.find(class_='section-title')
            phantom_title = (title_el.get_text(strip=True)
                              if title_el else '?')
            phantom_href = c.get('href', '')
            li = c.find_parent('li')
            if li and len(li.find_all('a', class_='section-card')) == 1:
                li.decompose()
            else:
                c.decompose()
            n_removed += 1
            if dry_run:
                print(f'    WOULD REMOVE phantom: href={phantom_href}'
                      f' title="{phantom_title}"')

    # Clean up empty <li>
    for li in s.find_all('li'):
        if not li.find('a') and not li.get_text(strip=True):
            li.decompose()

    # Consolidate <div class="section-grid"> cards into main list
    main_list = s.find('ul', class_='sections-list')
    for grid in s.find_all('div', class_='section-grid'):
        existing = set()
        if main_list:
            for c in main_list.find_all('a', class_='section-card'):
                existing.add(normalize_href(c.get('href', ''), base))
        for c in grid.find_all('a', class_='section-card'):
            href = c.get('href', '')
            key = normalize_href(href, base)
            if key in existing:
                c.decompose()
                n_removed += 1
            elif main_list:
                new_li = s.new_tag('li')
                new_li.append(c.extract())
                main_list.append(new_li)
                existing.add(key)
        if not grid.get_text(strip=True):
            grid.decompose()

    # Sort + normalize hrefs in main list
    if main_list:
        items = main_list.find_all('li', recursive=False)
        cur_mod = idx.parent.name
        prefix = f'../{cur_mod}/'
        for li in items:
            card = li.find('a', class_='section-card')
            if not card:
                continue
            href = card.get('href', '')
            if href.startswith(prefix):
                card['href'] = href[len(prefix):]
        items_sorted = sorted(items, key=section_sort_key)
        if items != items_sorted:
            for li in items_sorted:
                main_list.append(li.extract())

    if n_removed > 0 and not dry_run:
        idx.write_text(str(s), encoding='utf-8')
    return n_removed


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, required=True)
    ap.add_argument('--skip', nargs='*', default=DEFAULT_SKIP)
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args(argv)

    root: Path = args.root.resolve()
    if not root.exists():
        print(f'ERROR: root does not exist: {root}', file=sys.stderr)
        return 2

    dry = not args.apply
    if dry:
        print('DRY RUN. Pass --apply to write changes.')
    print()

    total = 0
    n_files = 0
    for p in root.rglob('index.html'):
        if is_skip(p, args.skip):
            continue
        n = fix_index(p, root, dry)
        if n:
            total += n
            n_files += 1
            print(f'  {p.relative_to(root)}: {n} phantom cards removed')

    print(f'\nTotal phantom cards removed: {total} across {n_files} files')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
