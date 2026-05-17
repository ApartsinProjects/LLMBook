"""Audit table captions across the book."""
import re
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs', 'agents'}

n_tables = 0
captions_tab = 0
captions_fig = 0
captions_none = 0
fig_callers = []  # tables where the caption says "Figure" (wrong)

for p in sorted(ROOT.rglob('*.html')):
    if set(p.parts) & SKIP:
        continue
    text = p.read_text(encoding='utf-8')
    for m in re.finditer(r'<table[\s\S]*?</table>', text):
        n_tables += 1
        block = m.group(0)
        cap = re.search(r'<caption[^>]*>(.*?)</caption>', block)
        rel = str(p.relative_to(ROOT)).replace('\\', '/')
        if cap:
            txt = re.sub(r'<[^>]+>', '', cap.group(1))[:80]
            if 'Table' in txt:
                captions_tab += 1
            elif 'Figure' in txt:
                captions_fig += 1
                fig_callers.append((rel, txt))
            else:
                captions_none += 1
            continue
        # Look for adjacent figcaption
        after = text[m.end():m.end() + 400]
        fc = re.search(r'<figcaption[^>]*>([\s\S]*?)</figcaption>', after)
        if fc:
            txt = re.sub(r'<[^>]+>', '', fc.group(1))[:80]
            if 'Figure' in txt:
                fig_callers.append((rel, txt))

print(f'Total <table> elements: {n_tables}')
print(f'  with <caption> Table-prefixed: {captions_tab}')
print(f'  with <caption> Figure-prefixed (WRONG): {captions_fig}')
print(f'  with <caption> neither: {captions_none}')
print(f'  with adjacent <figcaption> saying Figure (WRONG): {len(fig_callers) - captions_fig}')
print()
for f, t in fig_callers[:15]:
    print(f'  {f}: {t}')
