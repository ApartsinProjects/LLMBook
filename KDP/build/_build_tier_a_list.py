"""Build canonical Tier A orphan list with surrounding prose context."""
import re
import json
from pathlib import Path

SKIP = {'agents', 'KDP', 'node_modules', 'scripts', '.git',
        'chapter_review', 'downloads', '_archive', '_lab_fragments',
        'templates'}
CAP = re.compile(
    r'<div class="code-caption">[^<]*<strong>(Code Fragment [^<]+):</strong>([^<]{0,400})</div>',
    re.IGNORECASE,
)

orphans = []
for p in sorted(Path('.').rglob('*.html')):
    if p.parts and p.parts[0] in SKIP:
        continue
    text = p.read_text('utf-8', errors='replace')
    for m in CAP.finditer(text):
        win = text[max(0, m.start() - 1500):m.start()]
        last_pre = win.rfind('</pre>')
        last_cap = win.rfind('<div class="code-caption">')
        if last_pre == -1 or (last_cap != -1 and last_cap > last_pre):
            cap_num = m.group(1).replace('Code Fragment ', '').strip().rstrip(':')
            cap_desc = m.group(2).strip()
            ctx_start = max(0, m.start() - 2500)
            ctx = text[ctx_start:m.start()]
            ctx_clean = re.sub(r'<[^>]+>', ' ', ctx)
            ctx_clean = re.sub(r'\s+', ' ', ctx_clean)
            orphans.append({
                'file': str(p.relative_to('.')).replace('\\', '/'),
                'cap_num': cap_num,
                'desc': cap_desc[:300],
                'pos': m.start(),
                'preceding_prose': ctx_clean[-1500:],
            })

# Save
out = Path('KDP/build/_orphan_tier_a_list.json')
out.write_text(json.dumps(orphans, indent=2), encoding='utf-8')
print(f'Wrote {len(orphans)} orphans to {out}')
print('\nQuick summary by file:')
from collections import Counter
files = Counter(o['file'] for o in orphans)
for f, n in files.most_common():
    print(f'  {n:>2}x  {f}')
