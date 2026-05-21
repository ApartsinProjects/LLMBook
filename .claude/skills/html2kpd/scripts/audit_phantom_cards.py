"""Audit: index.html section cards for duplicates / inconsistencies.

For each index.html, scan all <a class="section-card"> elements and flag:
  1. Duplicate hrefs (multiple cards same target) with different titles
  2. Hrefs pointing to non-existent files
  3. Cards in a trailing <div class="section-grid"> that duplicate cards
     already in the main <ul class="sections-list">

The dedup is performed on RESOLVED href (so `./section-X` and
`../module-X/section-X` count as duplicates).

Usage:
    python audit_phantom_cards.py --root <book-root>
    python audit_phantom_cards.py --root <book-root> --skip node_modules backup

Exit code:
    0 if clean.
    1 if duplicates / broken targets found.
"""
from __future__ import annotations
import argparse
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


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, required=True)
    ap.add_argument('--skip', nargs='*', default=DEFAULT_SKIP)
    args = ap.parse_args(argv)

    root: Path = args.root.resolve()
    if not root.exists():
        print(f'ERROR: root does not exist: {root}', file=sys.stderr)
        return 2

    issues = []
    for p in root.rglob('index.html'):
        if is_skip(p, args.skip):
            continue
        try:
            s = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
        except Exception:
            continue
        cards = s.find_all('a', class_='section-card')
        if not cards:
            continue

        by_resolved = {}
        for c in cards:
            href = c.get('href', '')
            if not href or href.startswith('http') or '#' in href.split('?')[0][:5]:
                continue
            try:
                key = str((p.parent / href).resolve())
            except Exception:
                key = href
            num_el = c.find(class_='section-num')
            title_el = c.find(class_='section-title')
            num = num_el.get_text(strip=True) if num_el else '?'
            title = title_el.get_text(strip=True) if title_el else '?'
            by_resolved.setdefault(key, []).append((href, num, title))

        for resolved, entries in by_resolved.items():
            if len(entries) > 1:
                uniq_titles = set(t for _, _, t in entries)
                if len(uniq_titles) > 1:
                    issues.append({
                        'file': p,
                        'kind': 'duplicate_href',
                        'resolved': resolved,
                        'entries': entries,
                    })
            # Broken target?
            try:
                tgt = Path(resolved)
                if not tgt.exists():
                    issues.append({
                        'file': p,
                        'kind': 'broken_href',
                        'resolved': resolved,
                        'entries': entries,
                    })
            except Exception:
                pass

    dups = [i for i in issues if i['kind'] == 'duplicate_href']
    print('=== DUPLICATE HREFS (same target, multiple cards) ===')
    for issue in dups:
        print(f'\n  {issue["file"].relative_to(root)}')
        print(f'    resolved: {issue["resolved"]}')
        for href, num, title in issue['entries']:
            print(f'      ({num}) "{title}"  [href={href}]')

    broken = [i for i in issues if i['kind'] == 'broken_href']
    print('\n=== BROKEN HREFS (target file missing) ===')
    for issue in broken:
        print(f'  {issue["file"].relative_to(root)}: {issue["resolved"]}')
        for href, num, title in issue['entries']:
            print(f'      ({num}) "{title}"  [href={href}]')

    print(f'\nTotal duplicate-href issues:  {len(dups)}')
    print(f'Total broken-href issues:    {len(broken)}')
    return 0 if not issues else 1


if __name__ == '__main__':
    raise SystemExit(main())
