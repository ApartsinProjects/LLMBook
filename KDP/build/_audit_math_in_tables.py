"""Audit: files with math expressions inside tables."""
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
SKIP = ['node_modules', '.git', 'output', 'backup', 'KDP/build',
        'KDP/html2pub', 'pagefind', 'temp_epub', 'agents/', 'templates/']


def is_skip(p):
    sp = str(p).replace('\\', '/')
    return any(s in sp for s in SKIP)


files = {}
for p in ROOT.rglob('*.html'):
    if is_skip(p):
        continue
    try:
        s = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
    except Exception:
        continue
    for tbl in s.find_all('table'):
        math = tbl.find_all(['span', 'div'], class_=['math', 'math-block'])
        if math:
            files.setdefault(str(p.relative_to(ROOT)), 0)
            files[str(p.relative_to(ROOT))] += len(math)

print(f'Files with math in tables: {len(files)}')
for f, n in sorted(files.items()):
    print(f'  {f}: {n} math expr')
