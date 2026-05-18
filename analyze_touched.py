import json, os
from backfill_content import CONTENT

d = json.load(open('audit.json'))
touched = set(p.replace('/', os.sep) for p in CONTENT.keys())
# Add 31.1b
touched.add(os.sep.join(['part-7-retrieval-information-extraction-with-llms', 'module-31-embeddings-vector-db', 'section-31.1b.html']))

new_issues = {}
for i in d['issues']:
    if i['file'] in touched and i['check_id'] != 'SECTION_PAGE_LAYOUT':
        k = (i['file'], i['check_id'])
        new_issues.setdefault(k, []).append(i.get('message','')[:120])

from collections import Counter
ct = Counter()
for (f, c), msgs in new_issues.items():
    ct[c] += len(msgs)

print('Per-check counts in touched files:')
for k,v in sorted(ct.items(), key=lambda x: -x[1])[:15]:
    print(f'  {k:40s} {v}')
print(f'Total issues in touched files: {sum(len(m) for m in new_issues.values())}')
print()
# Show 5 sample messages for top categories
shown = 0
for k, v in sorted(ct.items(), key=lambda x: -x[1])[:5]:
    print(f'\n=== {k} ===')
    for (f, c), msgs in new_issues.items():
        if c == k:
            for m in msgs[:1]:
                print(f'  {f}: {m}')
                shown += 1
                if shown > 25: break
        if shown > 25: break
