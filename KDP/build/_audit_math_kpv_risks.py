"""Audit: math markup that might break in KPV.

Look for:
1. Display math without page-break-inside protection
2. Very long MathML expressions
3. Math inside table cells (table parser conflicts)
4. Math with unusual constructs (mover/munder stacks, mfrac depth > 3)
5. Math wrapped in <p> tags causing flow issues
6. Math with the empty-p-wrapper bug (the v810 fix area)
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


stats = {
    'pages_scanned': 0,
    'pages_with_math': 0,
    'inline_math_total': 0,
    'block_math_total': 0,
    'math_in_table': 0,
    'long_math_expr': [],  # (file, expr_len)
    'math_with_p_wrapper': [],  # (file, count)
    'deeply_nested_mfrac': [],  # (file, depth)
    'orphan_semantics': [],  # math without proper structure
}

for p in ROOT.rglob('*.html'):
    if is_skip(p):
        continue
    try:
        s = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
    except Exception:
        continue
    stats['pages_scanned'] += 1

    math_blocks = s.find_all('div', class_='math-block')
    math_inlines = s.find_all('span', class_='math')

    if not math_blocks and not math_inlines:
        continue
    stats['pages_with_math'] += 1
    stats['inline_math_total'] += len(math_inlines)
    stats['block_math_total'] += len(math_blocks)

    # Check math in table cells
    for tbl in s.find_all('table'):
        in_tbl_math = tbl.find_all(['span', 'div'], class_=['math', 'math-block'])
        stats['math_in_table'] += len(in_tbl_math)

    # Check for math wrapped in <p> (the empty-p bug pattern)
    p_wrapped = 0
    for blk in math_blocks:
        parent = blk.parent
        if parent and parent.name == 'p':
            p_wrapped += 1
    if p_wrapped:
        stats['math_with_p_wrapper'].append((str(p.relative_to(ROOT)), p_wrapped))

    # Check long math expressions (> 1500 chars MathML)
    for m in math_blocks + math_inlines:
        ml = str(m)
        if len(ml) > 1500:
            stats['long_math_expr'].append((str(p.relative_to(ROOT)), len(ml)))

    # Deeply nested mfrac
    for m in math_blocks + math_inlines:
        mfracs = m.find_all('mfrac')
        for mf in mfracs:
            depth = 1
            parent = mf.parent
            while parent and parent.name in ('mfrac', 'mrow', 'mn', 'mi', 'mo'):
                if parent.name == 'mfrac':
                    depth += 1
                parent = parent.parent
            if depth >= 4:
                stats['deeply_nested_mfrac'].append(
                    (str(p.relative_to(ROOT)), depth))

print('=== MATH AUDIT ===')
print(f'Pages scanned:        {stats["pages_scanned"]}')
print(f'Pages with math:      {stats["pages_with_math"]}')
print(f'Inline math (spans):  {stats["inline_math_total"]}')
print(f'Block math (divs):    {stats["block_math_total"]}')
print(f'Math inside tables:   {stats["math_in_table"]}')
print()
print(f'Math with <p> wrapper (bug): {len(stats["math_with_p_wrapper"])}')
for f, n in stats['math_with_p_wrapper'][:10]:
    print(f'  {f}: {n} blocks')
print()
print(f'Long math expressions (>1500 chars): {len(stats["long_math_expr"])}')
worst = sorted(stats['long_math_expr'], key=lambda t: -t[1])[:10]
for f, n in worst:
    print(f'  {f}: {n} chars')
print()
print(f'Deeply nested mfrac (>=4): {len(stats["deeply_nested_mfrac"])}')
for f, d in stats['deeply_nested_mfrac'][:10]:
    print(f'  {f}: depth {d}')
