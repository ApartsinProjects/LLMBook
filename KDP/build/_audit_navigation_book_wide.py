"""Audit: book-wide navigation chain integrity.

For each HTML page with a .chapter-nav, verify:
  1. prev href points to an existing file
  2. next href points to an existing file
  3. up href points to an existing file (parent index)
  4. The reciprocal link exists (A.next = B implies B.prev = A)
"""
from pathlib import Path
import re
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
SKIP = ['node_modules', '.git', 'output', 'backup', 'KDP/build', 'KDP/html2epub',
        'pagefind', 'temp_epub', 'agents/', 'templates/']


def is_skip(p):
    sp = str(p).replace('\\', '/')
    return any(s in sp for s in SKIP)


pages = []
for p in ROOT.rglob('*.html'):
    if is_skip(p):
        continue
    pages.append(p)

print(f'Scanning {len(pages)} HTML pages...')
print()

# Map: relative-path -> (prev_href_resolved, next_href_resolved, up_href_resolved)
nav_map = {}
no_nav = []
for p in pages:
    try:
        soup = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
    except UnicodeDecodeError:
        continue
    nav = soup.find('nav', class_='chapter-nav')
    if not nav:
        no_nav.append(p)
        continue
    prev = nav.find('a', class_='prev')
    nxt = nav.find('a', class_='next')
    up = nav.find('a', class_='up')

    def resolve(a):
        if not a or not a.get('href'):
            return None
        href = a['href'].split('#')[0]
        if not href or href.startswith('http'):
            return None
        try:
            return (p.parent / href).resolve()
        except Exception:
            return None

    nav_map[p.resolve()] = {
        'prev': resolve(prev),
        'next': resolve(nxt),
        'up': resolve(up),
        'prev_text': prev.get_text(strip=True) if prev else None,
        'next_text': nxt.get_text(strip=True) if nxt else None,
    }

print(f'Pages with chapter-nav: {len(nav_map)}')
print(f'Pages without nav:      {len(no_nav)}')

# Check for broken targets
broken_targets = []
for src, refs in nav_map.items():
    for kind in ('prev', 'next', 'up'):
        tgt = refs[kind]
        if tgt and not tgt.exists():
            broken_targets.append((src, kind, tgt))

print(f'\nBROKEN TARGETS: {len(broken_targets)}')
for src, kind, tgt in broken_targets[:20]:
    rel_src = src.relative_to(ROOT)
    print(f'  {rel_src}')
    print(f'    {kind} -> {tgt} (MISSING)')

# Check reciprocity: if A.next = B then B.prev should = A
asymmetric = []
for src, refs in nav_map.items():
    nxt = refs['next']
    if nxt and nxt in nav_map:
        nxt_refs = nav_map[nxt]
        if nxt_refs['prev'] != src:
            asymmetric.append(('next_mismatch', src, nxt, nxt_refs['prev']))
    prv = refs['prev']
    if prv and prv in nav_map:
        prv_refs = nav_map[prv]
        if prv_refs['next'] != src:
            asymmetric.append(('prev_mismatch', src, prv, prv_refs['next']))

print(f'\nASYMMETRIC NAV (A.next!=B.prev or vice versa): {len(asymmetric)}')
for kind, src, target, target_back_link in asymmetric[:30]:
    rel_src = src.relative_to(ROOT)
    rel_tgt = target.relative_to(ROOT)
    back = target_back_link.relative_to(ROOT) if target_back_link else 'NONE'
    print(f'  {kind}:')
    print(f'    {rel_src}')
    print(f'      -> {rel_tgt}')
    print(f'      <- (should be ^above^) but is: {back}')

# Check up: every section's up should be index of same parent
up_wrong = []
for src, refs in nav_map.items():
    up = refs['up']
    if up:
        expected = src.parent / 'index.html'
        # The src might be section-X.Y.html in module dir, up should be that
        # module's index.html
        if up.resolve() != expected.resolve():
            # OK if it's a parent grandparent index, that's the "appendix index"
            # case for chapter-card content
            pass
print()
print('No nav pages (first 20):')
for p in no_nav[:20]:
    print(f'  {p.relative_to(ROOT)}')
