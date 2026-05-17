"""Find \$NUM patterns outside math mode that cause KaTeX-render failures."""
import re
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs', 'agents'}

hits = []
for p in sorted(ROOT.rglob('*.html')):
    if set(p.parts) & SKIP:
        continue
    text = p.read_text(encoding='utf-8')
    # Strip <pre>/<code> blocks where \$ is just text
    safe = re.sub(r'<pre[\s\S]*?</pre>', '', text)
    safe = re.sub(r'<code[\s\S]*?</code>', '', safe)
    # Find \$<digit> patterns
    matches = list(re.finditer(r'\\\$[0-9]', safe))
    if matches:
        rel = str(p.relative_to(ROOT)).replace('\\', '/')
        hits.append((rel, len(matches)))

print(f'Files with corrupt \\\\$NUM patterns: {len(hits)}')
total = sum(n for _, n in hits)
print(f'Total occurrences: {total}')
for f, n in hits[:15]:
    print(f'  {f}: {n}')
