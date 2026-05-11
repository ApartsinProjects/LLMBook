"""Re-audit current orphans and split into focused batches for parallel agents."""
import json
import re
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
            ctx_start = max(0, m.start() - 2500)
            ctx = re.sub(r'<[^>]+>', ' ', text[ctx_start:m.start()])
            ctx = re.sub(r'\s+', ' ', ctx)
            orphans.append({
                'file': str(p.relative_to('.')).replace('\\', '/'),
                'cap_num': cap_num,
                'desc': m.group(2).strip()[:250],
                'pos': m.start(),
                'preceding_prose': ctx[-1200:],
            })

print(f'Current orphan count: {len(orphans)}')

batch_app = [o for o in orphans if o['file'].startswith('appendices/')]
batch_main = [o for o in orphans if not o['file'].startswith('appendices/')]
print(f'  Appendix batch: {len(batch_app)}')
print(f'  Main book batch: {len(batch_main)}')

Path('KDP/build/_orphan_batch_appendix.json').write_text(
    json.dumps(batch_app, indent=2), encoding='utf-8')
Path('KDP/build/_orphan_batch_chapters.json').write_text(
    json.dumps(batch_main, indent=2), encoding='utf-8')
print('\nWrote 2 batch files in KDP/build/')
