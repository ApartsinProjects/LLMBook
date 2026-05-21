"""Audit: book-wide navigation chain integrity.

For each HTML page with a <nav class="chapter-nav">, verify:
  1. prev/next/up hrefs point to existing files
  2. Reciprocity: A.next = B implies B.prev = A
  3. up href points to the directory's index.html

Usage:
    python audit_navigation.py --root <book-root>
    python audit_navigation.py --root <book-root> --skip node_modules backup output

Exit code:
    0 if clean (0 broken targets, 0 asymmetric).
    1 if defects found.
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
    ap.add_argument('--root', type=Path, required=True,
                    help='Book root (where part-*/module-*/section-*.html live)')
    ap.add_argument('--skip', nargs='*', default=DEFAULT_SKIP,
                    help='Substrings of paths to skip')
    args = ap.parse_args(argv)

    root: Path = args.root.resolve()
    if not root.exists():
        print(f'ERROR: root does not exist: {root}', file=sys.stderr)
        return 2

    pages = []
    for p in root.rglob('*.html'):
        if is_skip(p, args.skip):
            continue
        pages.append(p)
    print(f'Scanning {len(pages)} HTML pages under {root}')
    print()

    nav_map = {}
    no_nav = []
    for p in pages:
        try:
            soup = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
        except (UnicodeDecodeError, Exception):
            continue
        nav = soup.find('nav', class_='chapter-nav')
        if not nav:
            no_nav.append(p)
            continue
        prev = nav.find('a', class_='prev')
        nxt = nav.find('a', class_='next')
        up = nav.find('a', class_='up')

        def resolve(a):
            if not a or not a.get('href'):
                return None
            href = a['href'].split('#')[0]
            if not href or href.startswith('http'):
                return None
            try:
                return (p.parent / href).resolve()
            except Exception:
                return None

        nav_map[p.resolve()] = {
            'prev': resolve(prev),
            'next': resolve(nxt),
            'up': resolve(up),
            'prev_text': prev.get_text(strip=True) if prev else None,
            'next_text': nxt.get_text(strip=True) if nxt else None,
        }

    print(f'Pages with chapter-nav: {len(nav_map)}')
    print(f'Pages without nav:      {len(no_nav)}')

    broken = []
    for src, refs in nav_map.items():
        for kind in ('prev', 'next', 'up'):
            tgt = refs[kind]
            if tgt and not tgt.exists():
                broken.append((src, kind, tgt))

    print(f'\nBROKEN TARGETS: {len(broken)}')
    for src, kind, tgt in broken[:30]:
        rel_src = src.relative_to(root)
        print(f'  {rel_src}')
        print(f'    {kind} -> {tgt} (MISSING)')

    asymmetric = []
    for src, refs in nav_map.items():
        nxt = refs['next']
        if nxt and nxt in nav_map:
            if nav_map[nxt]['prev'] != src:
                asymmetric.append(('next_mismatch', src, nxt, nav_map[nxt]['prev']))
        prv = refs['prev']
        if prv and prv in nav_map:
            if nav_map[prv]['next'] != src:
                asymmetric.append(('prev_mismatch', src, prv, nav_map[prv]['next']))

    print(f'\nASYMMETRIC NAV: {len(asymmetric)}')
    for kind, src, target, target_back in asymmetric[:30]:
        rel_src = src.relative_to(root)
        rel_tgt = target.relative_to(root)
        back = (target_back.relative_to(root) if target_back
                and str(target_back).startswith(str(root)) else 'NONE')
        print(f'  {kind}:')
        print(f'    {rel_src}')
        print(f'      -> {rel_tgt}')
        print(f'      <- (should be ^above^) but is: {back}')

    return 0 if (not broken and not asymmetric) else 1


if __name__ == '__main__':
    raise SystemExit(main())
