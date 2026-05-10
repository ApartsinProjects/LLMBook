"""Audit: find every <img src=...> in source HTML, check if file exists on disk."""
from pathlib import Path
import re

ROOT = Path('.')
sep = chr(92)
img_re = re.compile(r'<img[^>]+src="([^"]+)"', re.IGNORECASE)
missing = []
total_refs = 0
for p in ROOT.rglob('*.html'):
    if any(part in p.parts for part in ('KDP', 'vendor', 'scripts', 'templates', 'md',
                                         'node_modules', 'temp_epub')):
        continue
    text = p.read_text(encoding='utf-8', errors='replace')
    for m in img_re.finditer(text):
        src = m.group(1)
        if src.startswith(('http://', 'https://', 'data:', '//', 'mailto:')):
            continue
        total_refs += 1
        target = (p.parent / src).resolve()
        if not target.exists():
            missing.append((str(p).replace(sep, '/'), src, str(target).replace(sep, '/')))

print(f'Total local img references: {total_refs}')
print(f'Missing: {len(missing)}')
print()
for src_html, ref, target in missing[:30]:
    print(f'  {src_html}')
    print(f'    src="{ref}"')
    print(f'    -> NOT FOUND: {target}')
