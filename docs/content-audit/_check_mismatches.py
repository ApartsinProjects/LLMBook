import os, re

ROOT = r'E:\Projects\BookBlogsHome\LLMBook'

# walk part-1 and part-2 modules 00-09
files = []
for root, _, fns in os.walk(os.path.join(ROOT, 'part-1-llm-building-blocks')):
    for fn in fns:
        if fn.endswith('.html'):
            files.append(os.path.join(root, fn))
for root, _, fns in os.walk(os.path.join(ROOT, 'part-2-understanding-llms')):
    for fn in fns:
        if fn.endswith('.html'):
            files.append(os.path.join(root, fn))

# Find visible-text mismatches introduced this session: href .../section-X.Ya.html
# with visible text "Section X.Y" (where target Y is bare and visible Y matches but variant is missing)
mismatches = []
for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        c = fh.read()
    for m in re.finditer(r'<a href="([^"]*section-(\d+\.\d+)([ab])\.html)"([^>]*)>Section (\d+\.\d+)</a>', c):
        href, target_sec, variant, attrs, visible = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
        if target_sec == visible:
            mismatches.append((f, href, visible, target_sec + variant))

print('Mismatches:', len(mismatches))
for f, href, vis, actual in mismatches:
    print(f'  {os.path.relpath(f, ROOT)}: visible "Section {vis}" -> target {actual}')
