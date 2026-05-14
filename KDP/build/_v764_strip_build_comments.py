"""v764: Strip <!-- v7XX --> / <!-- Wave N --> / <!-- Tier X --> comments.

These HTML comments leak the editorial workflow (wave plans, version
sentinels, tier markers). They are invisible to readers but represent
edit-history pollution that we want gone before publication.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('KDP/build/source_fix_backups', 'pagefind', 'node_modules',
        'temp_epub', '.git', 'venv')

PATTERNS = [
    re.compile(r'<!--\s*v[0-9]{3,4}[-_][^>]{0,120}-->'),
    re.compile(r'<!--\s*w[0-9]{1,3}[-_ ][^>]{0,120}-->'),
    re.compile(r'<!--\s*[Ww]ave\s+[0-9]+[^>]{0,120}-->'),
    re.compile(r'<!--\s*[Tt]ier\s+[A-Z][^>]{0,120}-->'),
]

n_files = 0
total = 0
for p in ROOT.rglob('*.html'):
    sp = str(p).replace('\\', '/')
    if any(s in sp for s in SKIP):
        continue
    try:
        src = p.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue
    new = src
    file_count = 0
    for pat in PATTERNS:
        matches = pat.findall(new)
        if matches:
            new = pat.sub('', new)
            file_count += len(matches)
    if new != src:
        p.write_text(new, encoding='utf-8')
        n_files += 1
        total += file_count
print(f'stripped {total} build-marker comments across {n_files} files')
