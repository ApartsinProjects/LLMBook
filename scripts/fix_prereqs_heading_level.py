"""Promote the Prerequisites box heading from <h3> to <h2>.

Every section page is `<h1> ... <h3 id="prerequisites">Prerequisites</h3> ...
<h2 id="X.Y.1">first subsection</h2>`, so the prereqs h3 appears BEFORE the first
h2, creating an h1->h3 heading-level skip (flagged by accessibility/structure
audits; 379 instances book-wide). The prereqs box is the page's first top-level
section, so h2 is the correct level and removes the skip (h1->h2->h2->h3...).

The heading is authored as a one-liner, so a line-scoped rewrite is safe.

Usage: py -3 scripts/fix_prereqs_heading_level.py [--apply]
Default is dry-run; pass --apply to write.
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APPLY = "--apply" in sys.argv

# <h3 ... id="prerequisites" ...>...</h3>  (id may carry other attrs; one line)
PAT = re.compile(r'<h3(\s+[^>]*\bid="prerequisites"[^>]*)>(.*?)</h3>', re.IGNORECASE)

changed = 0
files = 0
skipped = []
for f in sorted(ROOT.rglob("*.html")):
    sp = f.as_posix()
    if "/_archive/" in sp or "/KDP/" in sp or "/node_modules/" in sp:
        continue
    txt = f.read_text(encoding="utf-8", errors="replace")
    if 'id="prerequisites"' not in txt:
        continue
    new, n = PAT.subn(r'<h2\1>\2</h2>', txt)
    if n == 0:
        # has the id but not in expected <h3 ...>...</h3> one-line form
        if "<h3" in txt and 'id="prerequisites"' in txt:
            skipped.append(sp)
        continue
    files += 1
    changed += n
    if APPLY and new != txt:
        f.write_text(new, encoding="utf-8")

print(f"{'APPLIED' if APPLY else 'DRY-RUN'}: {changed} prereqs <h3>-><h2> in {files} files")
if skipped:
    print(f"SKIPPED (id present but not one-line h3): {len(skipped)}")
    for s in skipped[:10]:
        print("  ", s)
