import json, glob, os

d = json.load(open('audit.json'))
flagged = set()
for i in d['issues']:
    if i['check_id'] == 'SECTION_PAGE_LAYOUT':
        flagged.add(i['file'])

# Find a section file that's not flagged - canonical
sections = sorted(glob.glob('part-*/module-*/section-*.html'))
unflagged = [s for s in sections if s.replace('/', os.sep) not in flagged][:30]
for u in unflagged[:10]:
    print(u)
