"""Audit chapter-opener images: are alt+figcaption descriptive or generic?"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

generic, descriptive = [], []
GENERIC_ALTS = {'', 'Chapter illustration', 'Chapter opener', 'Chapter image'}

for p in sorted(list(ROOT.glob('part-*/module-*/index.html')) +
                list(ROOT.glob('appendices/appendix-*/index.html'))):
    text = p.read_text(encoding='utf-8', errors='replace')
    m = re.search(
        r'<figure[^>]*>\s*<img[^>]+src="[^"]*chapter-opener[^"]*"[^>]+alt="([^"]*)"[^>]*/?>(.*?)</figure>',
        text, re.DOTALL,
    )
    if not m:
        m2 = re.search(r'<img[^>]+src="[^"]*chapter-opener[^"]*"[^>]+alt="([^"]*)"', text)
        if not m2:
            continue
        alt = m2.group(1)
        cap = '(no figcaption)'
    else:
        alt = m.group(1)
        cap_m = re.search(r'<figcaption[^>]*>(.+?)</figcaption>', m.group(2), re.DOTALL)
        cap = re.sub(r'<[^>]+>', '', cap_m.group(1)).strip() if cap_m else '(no figcaption)'

    rel = str(p.relative_to(ROOT)).replace('\\', '/')
    generic_alt = alt in GENERIC_ALTS
    generic_cap = (cap in {'Chapter illustration.', 'Chapter illustration', '(no figcaption)'}
                   or 'Chapter illustration' in cap)
    if generic_alt or generic_cap:
        generic.append((rel, alt, cap))
    else:
        descriptive.append((rel, alt, cap))

print(f'Pages with chapter-opener: {len(generic) + len(descriptive)}')
print(f'  Generic alt/caption:     {len(generic)}')
print(f'  Descriptive alt/caption: {len(descriptive)}\n')

print('=== Generic examples (need fixing) ===')
for rel, alt, cap in generic[:20]:
    print(f'  {rel}')
    print(f'    alt: {alt[:80]}')
    print(f'    cap: {cap[:80]}')
print()
if descriptive:
    print('=== Sample of descriptive (good) ===')
    for rel, alt, cap in descriptive[:3]:
        print(f'  {rel}')
        print(f'    alt: {alt[:80]}')
        print(f'    cap: {cap[:80]}')
