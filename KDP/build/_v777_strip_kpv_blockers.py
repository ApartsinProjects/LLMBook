"""v777: Strip Kindle Previewer E21018 blockers book-wide.

Two patterns trigger KPV's "Enhanced Mobi building failure, while
parsing content. Content: <img>" error:

1. `loading="lazy"` attribute on <img> tags (392 occurrences across
   205 source files). The attribute is HTML5; KPV's enhanced Mobi
   converter rejects unknown image attributes.

2. Empty `<div class="diagram-container"></div>` placeholders left
   over from earlier draft passes (4 files). Empty divs around the
   img position confuse the converter's flow.

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


n_lazy = 0
n_lazy_files = 0
n_empty = 0
n_empty_files = 0

for hp in ROOT.rglob('*.html'):
    if should_skip(hp):
        continue
    try:
        s = hp.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue

    new = s
    counter = [0]
    file_empty = 0

    # Strip loading="lazy" with optional surrounding whitespace inside <img>
    def strip_lazy(m: re.Match) -> str:
        tag = m.group(0)
        new_tag, c = re.subn(r'\s*loading="lazy"', '', tag)
        counter[0] += c
        return new_tag

    # re.DOTALL so multiline <img alt="...
    # ..."> tags also match (alt text wraps across lines in some sources).
    new = re.sub(r'<img\b[^>]*?>', strip_lazy, new, flags=re.DOTALL)
    file_lazy = counter[0]

    # Strip empty <div class="diagram-container"></div>
    n_empty_div, c = re.subn(
        r'\s*<div class="diagram-container">\s*</div>\s*', '\n', new)
    new = n_empty_div
    file_empty = c

    if new != s:
        hp.write_text(new, encoding='utf-8')
        if file_lazy:
            n_lazy += file_lazy
            n_lazy_files += 1
        if file_empty:
            n_empty += file_empty
            n_empty_files += 1

print(f'Stripped loading="lazy": {n_lazy} occurrences across {n_lazy_files} files')
print(f'Stripped empty diagram-container: {n_empty} occurrences across {n_empty_files} files')
