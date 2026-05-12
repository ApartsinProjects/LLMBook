"""Find remaining bare 'Section X.Y' that look like broken placeholders."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/')

# Strip <a>...</a> blocks before checking, then look for "Section N.M" preceded
# by prose that suggests a noun should follow (e.g. "the Section 4.1 models").
LIKELY_BROKEN_PRECONTEXT = re.compile(
    r'(?:\b(?:the|a|an|with standard|consider|own|into a|own internal|class-weighted|the dominant|via)\s+)Section\s+\d+\.\d+',
)

hits = []
for p in ROOT.rglob('*.html'):
    sp = str(p).replace('\\', '/')
    if any(s in sp for s in SKIP):
        continue
    try:
        text = p.read_text(encoding='utf-8', errors='replace')
    except Exception:
        continue
    stripped = re.sub(r'<a\b[^>]*>.*?</a>', '', text, flags=re.DOTALL)
    for m in LIKELY_BROKEN_PRECONTEXT.finditer(stripped):
        start = max(0, m.start() - 30)
        end = min(len(stripped), m.end() + 60)
        ctx = stripped[start:end].replace('\n', ' ')
        hits.append((str(p.relative_to(ROOT)).replace('\\', '/'), ctx))

print(f'Likely-broken bare Section refs: {len(hits)}')
for f, ctx in hits[:30]:
    print(f'  {f}')
    print(f'    ...{ctx}...')
