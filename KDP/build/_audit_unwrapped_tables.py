"""Audit: tables not wrapped in a flow-controlled wrapper.

These tables will be atomic (display: table) and won't split across pages.
"""
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
SKIP = ['node_modules', '.git', 'output', 'backup', 'KDP/build',
        'KDP/html2epub', 'pagefind', 'temp_epub', 'agents/', 'templates/']


def is_skip(p):
    sp = str(p).replace('\\', '/')
    return any(s in sp for s in SKIP)


# Track parent context
parent_contexts = {}
unwrapped_samples = []
n_unwrapped = 0
n_total = 0

for p in ROOT.rglob('*.html'):
    if is_skip(p):
        continue
    try:
        s = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
    except Exception:
        continue
    for tbl in s.find_all('table'):
        n_total += 1
        # Get full parent chain context
        parent = tbl.parent
        if parent is None:
            continue
        parent_name = parent.name
        parent_cls = ' '.join(parent.get('class', []))

        # Check if in a flow-friendly wrapper
        flow_wrappers = ['comparison-table', 'table-wrapper', 'table-container',
                         'wide-table', 'data-table']
        if any(c in parent_cls for c in flow_wrappers):
            continue
        # Check grandparent
        if parent.parent:
            gp_cls = ' '.join(parent.parent.get('class', []))
            if any(c in gp_cls for c in flow_wrappers):
                continue

        n_unwrapped += 1

        # Categorize
        ctx_key = f'{parent_name}.{parent_cls or "no-class"}'[:60]
        parent_contexts[ctx_key] = parent_contexts.get(ctx_key, 0) + 1

        if len(unwrapped_samples) < 30:
            # Count rows for sample
            nrows = len(tbl.find_all('tr'))
            first_row = tbl.find('tr')
            ncols = len(first_row.find_all(['th', 'td'])) if first_row else 0
            unwrapped_samples.append((
                str(p.relative_to(ROOT)), parent_name, parent_cls, nrows, ncols
            ))

print(f'Total tables:    {n_total}')
print(f'Unwrapped:       {n_unwrapped}')
print()
print('Unwrapped parent contexts:')
for ctx, n in sorted(parent_contexts.items(), key=lambda kv: -kv[1]):
    print(f'  {n:4d}  parent={ctx}')
print()
print('Sample unwrapped tables:')
for f, pn, pc, nr, nc in unwrapped_samples[:20]:
    print(f'  {f}: <{pn} class="{pc[:30]}">  rows={nr} cols={nc}')
