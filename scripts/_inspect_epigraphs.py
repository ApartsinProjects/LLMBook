"""Sample existing epigraph blocks to understand the AI-agent style."""
import re
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs', 'agents'}

samples = []
for p in sorted(ROOT.rglob('*.html')):
    if set(p.parts) & SKIP:
        continue
    text = p.read_text(encoding='utf-8')
    for m in re.finditer(r'<blockquote class="epigraph">([\s\S]*?)</blockquote>', text):
        rel = str(p.relative_to(ROOT)).replace('\\', '/')
        samples.append((rel, m.group(1).strip()))
        if len(samples) >= 25:
            break
    if len(samples) >= 25:
        break

for path, block in samples:
    print('=' * 80)
    print(path)
    print(block[:900])
    print()
