"""Audit all chapter index navs to enumerate missing/non-standard slots."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

issues = {'no-prev-link': [], 'plain-text-middle': [], 'no-next-link': [], 'good': []}
for p in sorted(ROOT.glob('part-*/module-*/index.html')):
    text = p.read_text(encoding='utf-8', errors='replace')
    nav_m = re.search(r'<nav class="chapter-nav">(.*?)</nav>', text, re.DOTALL)
    if not nav_m:
        continue
    nav = nav_m.group(1)
    has_prev = bool(re.search(r'<a class="prev"', nav))
    has_up = bool(re.search(r'<a class="up"', nav))
    has_next = bool(re.search(r'<a class="next"', nav))
    rel = str(p.relative_to(ROOT)).replace('\\', '/')
    if not has_prev:
        issues['no-prev-link'].append(rel)
    if not has_up:
        issues['plain-text-middle'].append(rel)
    if not has_next:
        issues['no-next-link'].append(rel)
    if has_prev and has_up and has_next:
        issues['good'].append(rel)

for k, v in issues.items():
    print(f'{k}: {len(v)}')
    for x in v[:5]:
        print(f'  {x}')
    if len(v) > 5:
        print(f'  ... +{len(v) - 5} more')
