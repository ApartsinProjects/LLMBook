"""Audit: find href/src/srcset/etc with backslashes (Windows path separator)
that snuck into HTML attributes. Backslashes are not valid URL separators
and break EPUB navigation in some readers."""
import re
from pathlib import Path

SKIP = ['node_modules', '.git', 'output', 'backup', 'KDP/build', 'KDP/html2pub',
        'pagefind', 'temp_epub', 'agents/', 'templates/']
ROOT = Path(__file__).resolve().parents[2]

PATTERN_HREF = re.compile(r'href="([^"]*\\[^"]*)"')
PATTERN_SRC = re.compile(r'src="([^"]*\\[^"]*)"')

bad_href = []
bad_src = []
for p in ROOT.rglob('*.html'):
    sp = str(p).replace('\\', '/')
    if any(s in sp for s in SKIP):
        continue
    try:
        s = p.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue
    for m in PATTERN_HREF.finditer(s):
        bad_href.append((str(p), m.group(1)))
    for m in PATTERN_SRC.finditer(s):
        bad_src.append((str(p), m.group(1)))

print(f'Backslash href occurrences: {len(bad_href)} across {len(set(b[0] for b in bad_href))} files')
print(f'Backslash src occurrences:  {len(bad_src)} across {len(set(b[0] for b in bad_src))} files')
print()
print('Sample hrefs:')
for f, h in bad_href[:20]:
    print(f'  {h}  in  {f}')
print()
print('Sample srcs:')
for f, h in bad_src[:10]:
    print(f'  {h}  in  {f}')
