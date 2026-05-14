"""Find next/prev nav links that point at the same file (self-loop)."""
import os, re
base = r'E:\Projects\BookBlogsHome\LLMBook'
SKIP_DIRS = {'KDP', 'node_modules', 'pagefind', 'temp_epub', 'vendor', 'agents'}
NAV_RE = re.compile(r'<a class="(?:next|prev)"[^>]*href="([^"#?]+\.html)(?:[#?][^"]*)?"', re.I)

found = []
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
        for m in NAV_RE.finditer(content):
            href = m.group(1)
            target = os.path.normpath(os.path.join(root, href))
            if target == path:
                found.append((os.path.relpath(path, base), href))

print(f"SELF-LINKS: {len(found)}")
for p, h in found[:40]:
    print(f"  {p} -> {h}")
