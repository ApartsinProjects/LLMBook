"""Audit: table markup that might break in KPV.

Look for:
1. Wide tables (>5 columns) — Kindle reflows them
2. Tables not wrapped in .table-wrapper or .comparison-table
3. Tables with very long cell content
4. Tables with images or code inside
5. Tables with merged cells (rowspan/colspan)
"""
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
SKIP = ['node_modules', '.git', 'output', 'backup', 'KDP/build',
        'KDP/html2pub', 'pagefind', 'temp_epub', 'agents/', 'templates/']


def is_skip(p):
    sp = str(p).replace('\\', '/')
    return any(s in sp for s in SKIP)


tables_by_cols = {}  # ncols -> count
wide_tables = []  # files with >5 col tables
unwrapped_tables = []  # tables not in a wrapper div
tables_with_images = []  # tables with <img> inside
tables_with_code = []  # tables with <pre> or <code>
tables_with_merges = []  # rowspan/colspan
n_tables = 0
n_files_with_tables = 0

for p in ROOT.rglob('*.html'):
    if is_skip(p):
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
        # count cols from first row
        first_row = tbl.find('tr')
        if first_row:
            ncols = len(first_row.find_all(['th', 'td']))
        else:
            ncols = 0
        tables_by_cols[ncols] = tables_by_cols.get(ncols, 0) + 1
        if ncols >= 6:
            wide_tables.append((str(p.relative_to(ROOT)), ncols))

        # Check wrapper
        parent = tbl.parent
        if parent and parent.name == 'div':
            cls = ' '.join(parent.get('class', []))
        else:
            cls = ''
        if not any(c in cls for c in ('comparison-table', 'table-wrapper',
                                       'table-container', 'wide-table')):
            # check if grandparent is the wrapper
            if parent and parent.parent:
                gp = parent.parent
                if gp.name == 'div':
                    gp_cls = ' '.join(gp.get('class', []))
                    if any(c in gp_cls for c in ('comparison-table', 'table-wrapper')):
                        continue
            unwrapped_tables.append(str(p.relative_to(ROOT)))

        if tbl.find('img'):
            tables_with_images.append(str(p.relative_to(ROOT)))
        if tbl.find('pre') or tbl.find('code'):
            tables_with_code.append(str(p.relative_to(ROOT)))
        if tbl.find(['th', 'td'], rowspan=True) or tbl.find(['th', 'td'], colspan=True):
            tables_with_merges.append(str(p.relative_to(ROOT)))


print(f'Files with tables: {n_files_with_tables}')
print(f'Total tables:      {n_tables}')
print()
print('Column count distribution:')
for c in sorted(tables_by_cols.keys()):
    print(f'  {c} cols: {tables_by_cols[c]} tables')
print()
print(f'Wide tables (>=6 cols): {len(wide_tables)}')
for f, c in wide_tables[:20]:
    print(f'  {f}: {c} cols')
print()
print(f'Unwrapped tables: {len(unwrapped_tables)}')
print(f'Tables with images: {len(set(tables_with_images))}')
for f in set(tables_with_images):
    print(f'  {f}')
print(f'Tables with code: {len(set(tables_with_code))}')
for f in list(set(tables_with_code))[:10]:
    print(f'  {f}')
print(f'Tables with merges (rowspan/colspan): {len(set(tables_with_merges))}')
for f in list(set(tables_with_merges))[:10]:
    print(f'  {f}')
