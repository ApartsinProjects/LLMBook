"""Quick audit of the KDP conversion CSV report."""
import csv
import os
from collections import Counter

with open(r'E:/ChromeDownload/AK1P0PRVEB7LX_report (1).csv', encoding='utf-8-sig') as f:
    rows = list(csv.reader(f))
data = rows[3:]

print(f'Total entries: {len(data)}\n')

# Top files contributing to nullem
nullem_files = Counter()
for r in data:
    if len(r) >= 3 and 'nullem' in r[1]:
        f = os.path.basename(r[2].replace('\\', '/'))
        nullem_files[f] += 1

print(f'Files with nullem (top 15 of {len(nullem_files)}):')
for f, n in nullem_files.most_common(15):
    print(f'  {n:>5}x  {f[:90]}')
print()

# Top files for webkit-box-shadow
wbs_files = Counter()
for r in data:
    if len(r) >= 3 and 'webkit-box-shadow' in r[1]:
        f = os.path.basename(r[2].replace('\\', '/'))
        wbs_files[f] += 1
print(f'Files with -webkit-box-shadow (top 10 of {len(wbs_files)}):')
for f, n in wbs_files.most_common(10):
    print(f'  {n:>5}x  {f[:90]}')
print()

# All notices for the FATAL error context (entries surrounding the error)
print('Context around the single ERROR:')
for i, r in enumerate(data):
    if r[0] == 'Error':
        for j in range(max(0, i-3), min(len(data), i+3)):
            tag = '<<<' if j == i else '   '
            print(f'  {tag} [{j}] {r[0]} | {data[j][1][:80]} | src={data[j][2][-50:] if len(data[j])>=3 else ""}')
        break
