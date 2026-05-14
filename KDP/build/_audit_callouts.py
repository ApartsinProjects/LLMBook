"""Audit all callout variants used book-wide."""
import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('KDP/build/source_fix_backups', 'KDP/html2pub/tests', 'pagefind',
        'node_modules', 'temp_epub', '.git', 'venv', 'templates')


def should_skip(p):
    sp = str(p).replace('\\', '/')
    return any(s in sp for s in SKIP)


counter = Counter()
title_glyphs = Counter()  # what icons/glyphs appear in callout-title
sample = {}

for hp in ROOT.rglob('*.html'):
    if should_skip(hp):
        continue
    try:
        s = hp.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue
    for m in re.finditer(r'class="callout ([a-z-]+)"', s):
        kind = m.group(1)
        counter[kind] += 1
        if kind not in sample:
            # Capture the title that follows
            tail = s[m.end(): m.end() + 400]
            tm = re.search(
                r'<(?:p|div|h[1-6])\s+class="callout-title"[^>]*>(.+?)</',
                tail, re.DOTALL)
            if tm:
                title_text = re.sub(r'<[^>]+>', '', tm.group(1)).strip()
                sample[kind] = title_text[:80]

print(f'{"COUNT":>6}  {"VARIANT":<22}  EXAMPLE TITLE')
print('-' * 90)
for k, v in counter.most_common():
    print(f'{v:>6}  {k:<22}  {sample.get(k, "(no callout-title)")}')
print(f'\nTotal callout variants: {len(counter)}')
print(f'Total callout instances: {sum(counter.values())}')
