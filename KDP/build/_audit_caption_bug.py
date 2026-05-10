"""Find code-caption divs nested inside callout divs (BeautifulSoup-based)."""
from pathlib import Path
from bs4 import BeautifulSoup
ROOT = Path('.')
sep = chr(92)
hits = []
for p in ROOT.rglob('*.html'):
    if any(part in p.parts for part in ('KDP', 'vendor', 'scripts', 'templates', 'md',
                                         'node_modules', 'temp_epub')):
        continue
    try:
        text = p.read_text(encoding='utf-8', errors='replace')
    except Exception:
        continue
    if 'code-caption' not in text or 'callout' not in text:
        continue
    soup = BeautifulSoup(text, 'lxml')
    n_nested = 0
    for callout in soup.find_all('div', class_=lambda c: c and 'callout' in c):
        if callout.find('div', class_='code-caption'):
            n_nested += 1
    if n_nested:
        rel = str(p).replace(sep, '/')
        hits.append((rel, n_nested))

print(f'{len(hits)} files with code-caption nested inside a callout')
for rel, n in hits[:30]:
    print(f'  {n}x  {rel}')
