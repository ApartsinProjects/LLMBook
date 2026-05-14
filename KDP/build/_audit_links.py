"""Find truly broken href links: target file does not exist."""
import os, re
from urllib.parse import unquote

base = r'E:\Projects\BookBlogsHome\LLMBook'
SKIP_DIRS = {'KDP', 'node_modules', 'pagefind', 'temp_epub', 'vendor'}
HREF_RE = re.compile(r'href="([^"#?]+\.html)(?:[#?][^"]*)?"')

broken = []
for root, dirs, files in os.walk(base):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for f in files:
        if not f.endswith('.html'):
            continue
        path = os.path.join(root, f)
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
                content = fh.read()
        except Exception:
            continue
        for m in HREF_RE.finditer(content):
            href = unquote(m.group(1))
            if href.startswith(('http://','https://','mailto:','javascript:')):
                continue
            target = os.path.normpath(os.path.join(root, href))
            if not os.path.exists(target):
                rel = os.path.relpath(path, base)
                broken.append((rel, href, os.path.relpath(target, base)))

print(f"TOTAL BROKEN: {len(broken)}")
seen_pairs = set()
for src, href, tgt in broken:
    key = (src, tgt)
    if key in seen_pairs:
        continue
    seen_pairs.add(key)
print(f"UNIQUE (src,tgt): {len(seen_pairs)}")
# Group by target filename
from collections import Counter
tgt_counts = Counter(b[2] for b in broken)
print("\n=== TOP 30 broken targets ===")
for t, c in tgt_counts.most_common(30):
    print(f"  {c:4d} {t}")
print("\n=== ALL broken (first 80) ===")
seen = set()
for src, href, tgt in broken:
    k = (src, href)
    if k in seen:
        continue
    seen.add(k)
    if len(seen) > 80:
        break
    print(f"  {src} -> {href}")
