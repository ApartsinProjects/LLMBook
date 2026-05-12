"""Find pages where the header's toc-icon is not wrapped in a toc-link."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/')

broken = []
for p in ROOT.rglob('*.html'):
    sp = str(p).replace('\\', '/')
    if any(s in sp for s in SKIP):
        continue
    try:
        text = p.read_text(encoding='utf-8', errors='replace')
    except Exception:
        continue
    nav_m = re.search(r'<nav class="header-nav">(.*?)</nav>', text, re.DOTALL)
    if not nav_m:
        continue
    nav = nav_m.group(1)
    if '<span class="toc-icon">' in nav and 'class="toc-link"' not in nav:
        broken.append(str(p.relative_to(ROOT)).replace('\\', '/'))

print(f'{len(broken)} pages with unwrapped toc-icon (the icon floats centered):')
for x in broken[:30]:
    print(f'  {x}')
