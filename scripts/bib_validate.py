"""Quick validation: every section file we backfilled should have the bibliography-collapsible block."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bib_data
import bib_data_tot
from bib_data import BIBLIOGRAPHIES

missing = []
for p in BIBLIOGRAPHIES.keys():
    unix_p = p.replace('\\', '/')
    if not os.path.exists(unix_p):
        missing.append((unix_p, 'file missing'))
        continue
    with open(unix_p, 'r', encoding='utf-8') as f:
        content = f.read()
    if '<details class="bibliography-collapsible"' not in content:
        missing.append((unix_p, 'no bib'))

print(f"Total entries in BIBLIOGRAPHIES: {len(BIBLIOGRAPHIES)}")
print(f"Files missing bib: {len(missing)}")
for m, reason in missing[:5]:
    print(f"  {reason}: {m}")
