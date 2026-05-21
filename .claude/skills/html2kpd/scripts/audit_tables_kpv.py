"""Audit: table markup patterns that break Kindle.

Find:
  1. Wide tables (>= 6 columns; >= 4 if --strict).
  2. Tables not wrapped in .comparison-table / .table-wrapper /
     .complex-table-wrap / .table-wide-wrap.
  3. Tables containing <img> (image + table competing for width).
  4. Tables containing <pre> or <code> (code wider than column).
  5. Tables with rowspan/colspan (renderer quirks on Kindle).
  6. Math expressions inside table cells.

Usage:
    python audit_tables_kpv.py --root <book-root>
    python audit_tables_kpv.py --root <book-root> --strict   # flag >=4-col tables
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

WRAPPER_CLASSES = ('comparison-table', 'table-wrapper', 'table-container',
                   'wide-table', 'complex-table-wrap', 'table-wide-wrap')


def is_skip(p: Path, skip: list[str]) -> bool:
    sp = str(p).replace('\\', '/')
    return any(s in sp for s in skip)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, required=True)
    ap.add_argument('--skip', nargs='*', default=DEFAULT_SKIP)
    ap.add_argument('--strict', action='store_true',
                    help='Flag >=4-col tables as wide (default >=6)')
    args = ap.parse_args(argv)

    root: Path = args.root.resolve()
    if not root.exists():
        print(f'ERROR: root does not exist: {root}', file=sys.stderr)
        return 2

    wide_threshold = 4 if args.strict else 6

    tables_by_cols = {}
    wide_tables = []
    unwrapped_tables = []
    tables_with_images = []
    tables_with_code = []
    tables_with_merges = []
    tables_with_math = []
    n_tables = 0
    n_files_with_tables = 0

    for p in root.rglob('*.html'):
        if is_skip(p, args.skip):
            continue
        try:
            s = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
        except Exception:
            continue
        tables = s.find_all('table')
        if not tables:
            continue
        n_files_with_tables += 1
        for tbl in tables:
            n_tables += 1
            first_row = tbl.find('tr')
            ncols = len(first_row.find_all(['th', 'td'])) if first_row else 0
            tables_by_cols[ncols] = tables_by_cols.get(ncols, 0) + 1
            if ncols >= wide_threshold:
                wide_tables.append((str(p.relative_to(root)), ncols))

            # Wrapper check
            parent = tbl.parent
            cls = ''
            if parent and parent.name == 'div':
                cls = ' '.join(parent.get('class', []))
            wrapped = any(c in cls for c in WRAPPER_CLASSES)
            if not wrapped and parent and parent.parent:
                gp = parent.parent
                if gp.name == 'div':
                    gp_cls = ' '.join(gp.get('class', []))
                    if any(c in gp_cls for c in WRAPPER_CLASSES):
                        wrapped = True
            if not wrapped:
                unwrapped_tables.append(str(p.relative_to(root)))

            if tbl.find('img'):
                tables_with_images.append(str(p.relative_to(root)))
            if tbl.find('pre') or tbl.find('code'):
                tables_with_code.append(str(p.relative_to(root)))
            if (tbl.find(['th', 'td'], rowspan=True)
                    or tbl.find(['th', 'td'], colspan=True)):
                tables_with_merges.append(str(p.relative_to(root)))
            math_inside = tbl.find_all(['math']) + tbl.find_all(
                ['span', 'div'], class_=['math', 'math-block'])
            if math_inside:
                tables_with_math.append(
                    (str(p.relative_to(root)), len(math_inside)))

    print(f'Files with tables: {n_files_with_tables}')
    print(f'Total tables:      {n_tables}')
    print()
    print('Column count distribution:')
    for c in sorted(tables_by_cols.keys()):
        flag = '  (WIDE)' if c >= wide_threshold else ''
        print(f'  {c} cols: {tables_by_cols[c]} tables{flag}')
    print()
    print(f'Wide tables (>={wide_threshold} cols): {len(wide_tables)}')
    for f, c in wide_tables[:20]:
        print(f'  {f}: {c} cols')
    print()
    print(f'Unwrapped tables: {len(unwrapped_tables)}')
    print(f'Tables with images: {len(set(tables_with_images))}')
    for f in sorted(set(tables_with_images))[:10]:
        print(f'  {f}')
    print(f'Tables with code: {len(set(tables_with_code))}')
    for f in sorted(set(tables_with_code))[:10]:
        print(f'  {f}')
    print(f'Tables with rowspan/colspan: {len(set(tables_with_merges))}')
    for f in sorted(set(tables_with_merges))[:10]:
        print(f'  {f}')
    print(f'Tables containing math: {len(tables_with_math)}')
    for f, n in tables_with_math[:10]:
        print(f'  {f}: {n} math elements')

    bad = (len(wide_tables) + len(set(tables_with_images))
           + len(set(tables_with_code)) + len(set(tables_with_merges)))
    return 0 if bad == 0 else 1


if __name__ == '__main__':
    raise SystemExit(main())
