"""Scan for <img> nested inside inline-only HTML5 elements that
historically break Kindle Mobi/KFX conversion (E21018)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
INLINE = ['cite', 'abbr', 'dfn', 'kbd', 'var', 'code', 'samp', 'q',
          'sub', 'sup', 'small', 'b', 'i', 'em', 'strong', 'mark', 'time']
SKIP = ('KDP/build/source_fix_backups', 'pagefind', 'node_modules', '.git', 'venv')

PAT = {tag: re.compile(
    rf'<{tag}\b[^>]*>(?:(?!</{tag}>).){{0,1500}}<img\b',
    re.IGNORECASE | re.DOTALL)
    for tag in INLINE}

results = {tag: [] for tag in INLINE}
for p in ROOT.rglob('*.html'):
    sp = str(p).replace('\\', '/')
    if any(s in sp for s in SKIP):
        continue
    try:
        t = p.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue
    for tag, pat in PAT.items():
        if pat.search(t):
            results[tag].append(str(p.relative_to(ROOT)))

print('Inline-parent <img> scan:')
for tag, files in results.items():
    if files:
        print(f'  <{tag}> with nested <img>: {len(files)} files')
        for f in files[:3]:
            print(f'     - {f}')
print()
print('(Empty categories omitted.)')
