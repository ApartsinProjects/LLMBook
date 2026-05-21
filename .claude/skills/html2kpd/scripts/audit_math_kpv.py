"""Audit: math markup patterns that break Kindle Previewer (KPV).

Find:
  1. <div class="math-block"> directly inside a non-empty <p> (HTML5
     parser auto-closes the <p>, orphaning surrounding text).
  2. <mtable> with empty columnspacing/rowspacing/columnalign/rowalign
     attributes (fails epubcheck RSC-005).
  3. <msub>/<msup>/<msubsup> with a third <mo> child containing a
     function-application invisible char (U+2061..U+2064). Violates
     MathML schema; triggers RSC-005.
  4. Very long MathML expressions (>1500 chars per expression).
  5. Deeply nested <mfrac> (>= 4 levels).
  6. Math inside table cells (reflow oddly on Kindle).
  7. <semantics> wrappers (some readers render as block).
  8. <annotation> tags (leak raw TeX on fallback).

Usage:
    python audit_math_kpv.py --root <book-root>

Exit code:
    0 if clean; 1 if any KPV-risk patterns found.
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

INVISIBLE_FUNC_APP_CHARS = ('⁡', '⁢', '⁣', '⁤')


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

    stats = {
        'pages_scanned': 0,
        'pages_with_math': 0,
        'inline_math_total': 0,
        'block_math_total': 0,
        'math_in_table': 0,
        'long_math_expr': [],
        'math_with_p_wrapper': [],
        'deeply_nested_mfrac': [],
        'empty_mtable_attrs': [],
        'invisible_func_app_in_msub': [],
        'semantics_count': 0,
        'annotation_count': 0,
    }

    for p in root.rglob('*.html'):
        if is_skip(p, args.skip):
            continue
        try:
            s = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
        except Exception:
            continue
        stats['pages_scanned'] += 1

        math_blocks = s.find_all('div', class_='math-block')
        math_inlines = s.find_all('span', class_='math')
        math_tags = s.find_all('math')

        if not (math_blocks or math_inlines or math_tags):
            continue
        stats['pages_with_math'] += 1
        stats['inline_math_total'] += len(math_inlines)
        stats['block_math_total'] += len(math_blocks)

        for tbl in s.find_all('table'):
            in_tbl_math = tbl.find_all(['span', 'div'],
                                        class_=['math', 'math-block'])
            in_tbl_math += tbl.find_all('math')
            stats['math_in_table'] += len(in_tbl_math)

        # Math wrapped in non-empty <p>
        p_wrapped = 0
        for blk in math_blocks:
            parent = blk.parent
            if parent and parent.name == 'p':
                # Check parent isn't empty (just the math)
                txt = parent.get_text(strip=True)
                math_txt = blk.get_text(strip=True)
                if len(txt) > len(math_txt):
                    p_wrapped += 1
        if p_wrapped:
            stats['math_with_p_wrapper'].append(
                (str(p.relative_to(root)), p_wrapped))

        # Long math expressions
        for m in math_blocks + math_inlines + math_tags:
            ml = str(m)
            if len(ml) > 1500:
                stats['long_math_expr'].append(
                    (str(p.relative_to(root)), len(ml)))

        # Deeply nested mfrac
        for m in math_tags:
            for mf in m.find_all('mfrac'):
                depth = 1
                parent = mf.parent
                while parent and parent.name in ('mfrac', 'mrow', 'mn', 'mi', 'mo'):
                    if parent.name == 'mfrac':
                        depth += 1
                    parent = parent.parent
                if depth >= 4:
                    stats['deeply_nested_mfrac'].append(
                        (str(p.relative_to(root)), depth))

        # Empty mtable layout attrs
        for mtable in s.find_all('mtable'):
            for attr in ('columnspacing', 'rowspacing',
                          'columnalign', 'rowalign'):
                v = mtable.get(attr)
                if v is not None and not v.strip():
                    stats['empty_mtable_attrs'].append(
                        (str(p.relative_to(root)), attr))

        # Invisible function-app char in msub/msup/msubsup
        for parent in s.find_all(['msub', 'msup', 'msubsup']):
            for child in parent.find_all('mo', recursive=False):
                txt = child.get_text() or ''
                if any(c in txt for c in INVISIBLE_FUNC_APP_CHARS):
                    stats['invisible_func_app_in_msub'].append(
                        (str(p.relative_to(root)), parent.name))
                    break

        stats['semantics_count'] += len(s.find_all('semantics'))
        stats['annotation_count'] += len(s.find_all('annotation'))

    print('=== MATH KPV AUDIT ===')
    print(f'Pages scanned:        {stats["pages_scanned"]}')
    print(f'Pages with math:      {stats["pages_with_math"]}')
    print(f'Inline math (spans):  {stats["inline_math_total"]}')
    print(f'Block math (divs):    {stats["block_math_total"]}')
    print(f'Math inside tables:   {stats["math_in_table"]}')
    print()
    print(f'<semantics> wrappers (strip recommended): {stats["semantics_count"]}')
    print(f'<annotation> tags (strip recommended):    {stats["annotation_count"]}')
    print()
    print(f'Math inside non-empty <p> (HTML5 auto-close bug): '
          f'{len(stats["math_with_p_wrapper"])}')
    for f, n in stats['math_with_p_wrapper'][:10]:
        print(f'  {f}: {n} blocks')
    print()
    print(f'Empty mtable layout attrs (RSC-005): '
          f'{len(stats["empty_mtable_attrs"])}')
    for f, attr in stats['empty_mtable_attrs'][:10]:
        print(f'  {f}: {attr}=""')
    print()
    print(f'Invisible function-app char in msub/msup (RSC-005): '
          f'{len(stats["invisible_func_app_in_msub"])}')
    for f, tag in stats['invisible_func_app_in_msub'][:10]:
        print(f'  {f}: <{tag}>')
    print()
    print(f'Long math (>1500 chars):  {len(stats["long_math_expr"])}')
    for f, n in sorted(stats['long_math_expr'], key=lambda t: -t[1])[:5]:
        print(f'  {f}: {n} chars')
    print()
    print(f'Deeply nested mfrac (>=4): {len(stats["deeply_nested_mfrac"])}')
    for f, d in stats['deeply_nested_mfrac'][:5]:
        print(f'  {f}: depth {d}')

    bad = (len(stats['math_with_p_wrapper'])
           + len(stats['empty_mtable_attrs'])
           + len(stats['invisible_func_app_in_msub']))
    return 0 if bad == 0 else 1


if __name__ == '__main__':
    raise SystemExit(main())
