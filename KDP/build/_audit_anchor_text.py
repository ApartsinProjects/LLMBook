"""Find anchor-text Section X.Y where href section number does not match."""
import os, re
base = r'E:\Projects\BookBlogsHome\LLMBook'
SKIP_DIRS = {'KDP', 'node_modules', 'pagefind', 'temp_epub', 'vendor', 'agents'}
# match: <a ... href="...section-A.B.html..."...>Section C.D</a>
A_RE = re.compile(
    r'<a\b[^>]*href="([^"]*?section-([0-9a-z]+)\.([0-9a-z]+)\.html[^"]*)"[^>]*>([^<]*?)</a>',
    re.I)
TEXT_RE = re.compile(r'Section\s+([0-9a-z]+)\.([0-9a-z]+)\b', re.I)

mismatches = []
for root, dirs, files in os.walk(base):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for f in files:
        if not f.endswith('.html'):
            continue
        path = os.path.join(root, f)
        try:
            content = open(path, 'r', encoding='utf-8', errors='ignore').read()
        except Exception:
            continue
        for m in A_RE.finditer(content):
            href, ha, hb, text = m.group(1), m.group(2), m.group(3), m.group(4)
            tm = TEXT_RE.search(text)
            if not tm:
                continue
            ta, tb = tm.group(1), tm.group(2)
            if ha.lower() != ta.lower() or hb.lower() != tb.lower():
                mismatches.append((os.path.relpath(path, base), text.strip(), f"section-{ha}.{hb}.html"))

print(f"MISMATCHES: {len(mismatches)}")
for p, t, h in mismatches[:40]:
    print(f"  {p}: anchor='{t}' -> href={h}")
