"""v771: Canonicalize display-math wrappers.

The audit found two non-canonical wrappers still in use:
  - <p>$$...$$</p>           (7 occurrences in 6 files)
  - <p class="math-display">$$...$$</p>  (1 occurrence in section 8.1)

Canonical wrapper is <div class="math-block">$$...$$</div>.

Replace both forms with the canonical wrapper.
Idempotent.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('KDP/build/source_fix_backups', 'KDP/html2pub/tests',
        'pagefind', 'node_modules', 'temp_epub', '.git', 'venv')


def should_skip(p: Path) -> bool:
    sp = str(p).replace('\\', '/')
    return any(s in sp for s in SKIP)


# Two patterns. We replace the wrapping element only; preserve the math.
PATTERNS = [
    # <p class="math-display">$$...$$</p> -> <div class="math-block">$$...$$</div>
    (re.compile(r'<p\s+class="math-display">(\s*\$\$.*?\$\$\s*)</p>',
                re.DOTALL),
     r'<div class="math-block">\1</div>',
     '<p class="math-display"> -> <div class="math-block">'),

    # <p>$$...$$</p> -> <div class="math-block">$$...$$</div>
    # Be conservative: only when the <p> contains ONLY the $$..$$ math,
    # nothing else.
    (re.compile(r'<p>(\s*\$\$[^$]+\$\$\s*)</p>',
                re.DOTALL),
     r'<div class="math-block">\1</div>',
     '<p>$$..$$</p> -> <div class="math-block">'),
]

n_files = 0
n_total = 0
for p in ROOT.rglob('*.html'):
    if should_skip(p):
        continue
    try:
        s = p.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue
    new = s
    file_count = 0
    for pat, rep, label in PATTERNS:
        new2, c = pat.subn(rep, new)
        if c:
            new = new2
            file_count += c
    if new != s:
        p.write_text(new, encoding='utf-8')
        n_files += 1
        n_total += file_count
        print(f'  [{p.relative_to(ROOT)}] {file_count} fixes')
print(f'\nTotal wrapper fixes: {n_total} across {n_files} files')
