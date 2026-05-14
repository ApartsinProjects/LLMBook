import os, re
base = r'E:\Projects\BookBlogsHome\LLMBook'
modules = []
for root, dirs, files in os.walk(base):
    norm = root.replace('\\','/')
    if '/KDP' in norm or '/node_modules' in norm or '/pagefind' in norm or '/temp_epub' in norm:
        continue
    if 'index.html' in files and ('module-' in os.path.basename(root) or 'appendix-' in os.path.basename(root)):
        modules.append(root)

for m in modules:
    idx = os.path.join(m, 'index.html')
    with open(idx, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    # match both 'section-X.Y.html' and 'path/section-X.Y.html'
    refs = set(re.findall(r'(section-[^"\'/\s]+\.html)', content))
    on_disk = set(f for f in os.listdir(m) if f.startswith('section-') and f.endswith('.html'))
    missing = refs - on_disk
    orphan = on_disk - refs
    if missing or orphan:
        print(m)
        if missing:
            print('  MISSING:', sorted(missing))
        if orphan:
            print('  ORPHAN:', sorted(orphan))
