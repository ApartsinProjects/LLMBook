"""Audit: stale section references in prose text.

Find references like "Section AB.6" or "see X.4" where X.4 doesn't exist
in the target appendix/module.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import re

ROOT = Path(__file__).resolve().parents[2]
SKIP = ['node_modules', '.git', 'output', 'backup', 'KDP/build',
        'KDP/html2pub', 'pagefind', 'temp_epub', 'agents/', 'templates/']


def is_skip(p):
    sp = str(p).replace('\\', '/')
    return any(s in sp for s in SKIP)


# First, build a catalog of which section files exist
section_catalog = {}  # 'AB.6' -> path to section-ab.6.html
for app_dir in (ROOT / 'appendices').iterdir():
    if not app_dir.is_dir():
        continue
    for f in app_dir.glob('section-*.html'):
        m = re.match(r'section-([a-z]+)\.(\d+)\.html', f.name)
        if m:
            section_catalog[f'{m.group(1).upper()}.{m.group(2)}'] = f

for part_dir in ROOT.glob('part-*'):
    if not part_dir.is_dir():
        continue
    for mod_dir in part_dir.iterdir():
        if not mod_dir.is_dir():
            continue
        for f in mod_dir.glob('section-*.html'):
            m = re.match(r'section-(\d+)\.(\d+)\.html', f.name)
            if m:
                section_catalog[f'{m.group(1)}.{m.group(2)}'] = f

print(f'Catalog: {len(section_catalog)} section files')

# Patterns to find references
# Match: Section AB.6, Section S.4, Chapter 28, Appendix AB.6
ref_pattern = re.compile(
    r'\b(Section|Chapter|Appendix|see)\s+([A-Z]{1,3}|\d{1,2})\.(\d+)\b',
    re.IGNORECASE
)
# Also: just AB.6 (e.g., "...AB.6 covers...")
plain_ref_pattern = re.compile(r'\b([A-Z]{2,3}|\d{1,2})\.(\d+)\b')

# Build set of valid refs
valid_refs = set(section_catalog.keys())
# Also include "X.0" as valid (the chapter/index page)

stale = []
for p in ROOT.rglob('*.html'):
    if is_skip(p):
        continue
    try:
        s = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
    except Exception:
        continue
    text = s.get_text(' ', strip=True)

    for m in ref_pattern.finditer(text):
        ref = f'{m.group(2).upper()}.{m.group(3)}'
        if ref not in valid_refs:
            # Skip well-known false positives:
            # - common decimal numbers like "1.0", "0.5"
            # - exercise/figure references
            ctx = text[max(0, m.start() - 30):m.end() + 30]
            # Skip if context has Figure/Table/Eq:
            if any(w in ctx.lower() for w in ['figure', 'fig.', 'eq.',
                                                'equation', 'algorithm']):
                continue
            stale.append({
                'file': str(p.relative_to(ROOT)),
                'ref': ref,
                'full': m.group(0),
                'context': ctx[:80],
            })

print(f'\nStale references found: {len(stale)}')

# Group by ref to see top offenders
from collections import Counter
by_ref = Counter(s['ref'] for s in stale)
print('\nTop stale refs:')
for ref, n in by_ref.most_common(20):
    print(f'  {ref}: {n} mentions')

# Sample
print('\nSample stale references:')
for s in stale[:30]:
    print(f'  {s["file"]}')
    print(f'    "{s["full"]}" - ctx: ...{s["context"]}...')
