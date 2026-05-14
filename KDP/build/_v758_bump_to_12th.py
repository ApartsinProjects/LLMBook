"""Bump any straggler 'Eleventh Edition' / '11th Edition' to Twelfth/12th."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
n_files = 0
n_subs = 0
for p in ROOT.rglob('*.html'):
    sp = str(p).replace('\\', '/')
    if 'KDP/build/source_fix_backups' in sp:
        continue
    try:
        src = p.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue
    new = src
    new, c1 = re.subn(r'\bEleventh Edition\b', 'Thirteenth Edition', new)
    new, c2 = re.subn(r'\b11th Edition\b', '13th Edition', new)
    if new != src:
        p.write_text(new, encoding='utf-8')
        n_files += 1
        n_subs += c1 + c2
        print(f'  [fix +{c1+c2}] {p.relative_to(ROOT)}')
print(f'\nFiles: {n_files}, Subs: {n_subs}')
