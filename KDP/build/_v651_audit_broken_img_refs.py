"""Find every <img src=> in the book where the file does NOT exist on disk."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/')

broken = []
total = 0
for p in ROOT.rglob('*.html'):
    sp = str(p).replace('\\', '/')
    if any(s in sp for s in SKIP):
        continue
    try:
        text = p.read_text(encoding='utf-8', errors='replace')
    except Exception:
        continue
    for m in re.finditer(r'<img[^>]+src="([^"]+)"', text):
        src = m.group(1)
        if src.startswith('http'):
            continue
        total += 1
        target = (p.parent / src).resolve()
        if not target.exists():
            broken.append((str(p.relative_to(ROOT)).replace('\\', '/'), src))

print(f'Scanned {total} <img> references')
print(f'Broken: {len(broken)}')
for f, src in broken[:30]:
    print(f'  {f}: src="{src}"')
