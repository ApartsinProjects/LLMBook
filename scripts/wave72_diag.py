"""Diagnose files where dry-run says no-change but issues exist."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from wave72_reorder_callouts import locate_singletons, needs_reorder

ROOT = Path('E:/Projects/BookBlogsHome/LLMBook')

with open(ROOT / 'docs' / 'content-audit' / 'cycle_snapshots' / 'cycle_38.json',
          'r', encoding='utf-8') as f:
    data = json.load(f)

co = [i for i in data['issues'] if i['check_id'] == 'CALLOUT_ORDER']
files = sorted({i['file'] for i in co})

count = 0
for f in files:
    fp = ROOT / f.replace('\\', '/')
    if not fp.exists():
        continue
    html = fp.read_text(encoding='utf-8', errors='ignore')
    spans = locate_singletons(html)
    if not needs_reorder(spans):
        count += 1
        if count <= 10:
            print(f'NO REORDER NEEDED: {f}')
            print('  Original issues:')
            for i in co:
                if i['file'] == f:
                    print('   -', i['message'])
            print('  Detected ranks:', [(n, r) for r, _, _, n in spans])
            print()
print(f'TOTAL: {count}')
