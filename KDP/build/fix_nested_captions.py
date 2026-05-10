"""Move code-caption divs OUT of callout divs (caption belongs as sibling, not child)."""
from pathlib import Path
from bs4 import BeautifulSoup
import time, shutil

ROOT = Path('.')
sep = chr(92)
backup = ROOT / f'KDP/build/source_fix_backups/nested_captions_{time.strftime("%Y%m%d_%H%M%S")}'
n_files = 0
n_moves = 0
for p in ROOT.rglob('*.html'):
    if any(part in p.parts for part in ('KDP', 'vendor', 'scripts', 'templates', 'md',
                                         'node_modules', 'temp_epub')):
        continue
    text = p.read_text(encoding='utf-8', errors='replace')
    if 'code-caption' not in text or 'callout' not in text:
        continue
    soup = BeautifulSoup(text, 'lxml')
    moved = 0
    for callout in soup.find_all('div', class_=lambda c: c and 'callout' in c):
        captions = callout.find_all('div', class_='code-caption')
        for cap in captions:
            cap.extract()
            callout.insert_before(cap)
            moved += 1
    if moved:
        # Re-serialize body content only (preserve original head/structure)
        body = soup.find('body')
        if body is None:
            continue
        body_inner = ''.join(str(c) for c in body.children)
        new_text = text[:text.find('<body')]
        head_close = text.find('>', text.find('<body')) + 1
        body_close = text.rfind('</body>')
        new_text = text[:head_close] + '\n' + body_inner + '\n' + text[body_close:]

        b = backup / p.relative_to(ROOT)
        b.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, b)
        p.write_text(new_text, encoding='utf-8')
        n_files += 1
        n_moves += moved
        print(f'  fixed {moved}x in {str(p).replace(sep, "/")}')

print(f'\nTotal: {n_moves} captions moved across {n_files} files')
print(f'Backups: {backup}')
