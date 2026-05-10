"""Scan for H3 headings that are still using OLD flat sub-numbering."""
import re
from pathlib import Path

ROOT = Path('E:/Projects/BookBlogsHome/LLMBook')
SEC_RE = re.compile(r'section-(\d+)\.(\d+[a-z]?)\.html$')
H3_RE = re.compile(r'<h3[^>]*>\s*([^<]+?)\s*</h3>', re.IGNORECASE)

files_with_stale = []
for p in ROOT.rglob('*.html'):
    if any(part in p.parts for part in ('KDP', 'vendor', 'scripts', 'templates', 'md', 'node_modules')):
        continue
    m = SEC_RE.search(p.name)
    if not m:
        continue
    prefix = f"{m.group(1)}.{m.group(2)}"
    text = p.read_text(encoding='utf-8', errors='replace')
    stale = []
    for hm in H3_RE.finditer(text):
        title = hm.group(1).strip()
        nm = re.match(r'^(\d+(?:\.\d+)?)[\.\s]', title)
        if nm and not title.startswith(prefix + '.'):
            stale.append(title[:60])
    if stale:
        rel = str(p.relative_to(ROOT)).replace(chr(92), '/')
        files_with_stale.append((rel, prefix, stale))

print(f"Files with stale H3 numbering: {len(files_with_stale)}")
total_stale = sum(len(s) for _, _, s in files_with_stale)
print(f"Total stale H3s: {total_stale}")
print()
for f, pref, ex in files_with_stale[:10]:
    print(f"  [{pref}] {f} ({len(ex)} stale)")
    for e in ex[:3]:
        print(f"      {e}")
