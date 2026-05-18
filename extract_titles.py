"""Extract h1 titles and meta descriptions from affected sections."""
import json, re, os, glob

d = json.load(open('audit_targets.json'))

file_titles = {}
for f in sorted(set(d['prereq'] + d['epigraph'] + d['big_picture'])):
    p = f.replace('\\', os.sep)
    full = os.path.join(os.getcwd(), p)
    if os.path.exists(full):
        txt = open(full, encoding='utf-8').read()
        h1 = re.search(r'<h1>([^<]+)</h1>', txt)
        meta = re.search(r'<meta content="([^"]+)" name="description"', txt)
        h2s = re.findall(r'<h2 id="[^"]*">([^<]+)</h2>', txt)
        cross_refs = re.findall(r'href="(\.\./[^"]+\.html|[^"]+\.html)"', txt)[:5]
        if h1:
            file_titles[p] = {
                'title': h1.group(1).strip(),
                'meta': meta.group(1)[:300] if meta else '',
                'h2s': h2s[:6],
                'crossrefs': cross_refs[:5]
            }

with open('section_titles.json', 'w', encoding='utf-8') as out:
    json.dump(file_titles, out, indent=2, ensure_ascii=False)
print(f'Captured {len(file_titles)} section titles')
