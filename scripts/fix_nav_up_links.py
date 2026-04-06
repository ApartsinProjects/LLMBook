"""Fix missing 'up' links in pathway and syllabi navigation footers."""

import glob
import re
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIGS = [
    {
        "glob": os.path.join(BASE, "front-matter", "pathways", "*.html"),
        "up_html": '<a class="up" href="index.html">Reading Pathways</a>',
        "label": "pathways",
    },
    {
        "glob": os.path.join(BASE, "front-matter", "syllabi", "*.html"),
        "up_html": '<a class="up" href="index.html">Course Syllabi</a>',
        "label": "syllabi",
    },
]

fixed = []
skipped = []
errors = []

for cfg in CONFIGS:
    for fpath in sorted(glob.glob(cfg["glob"])):
        fname = os.path.basename(fpath)
        if fname == "index.html":
            continue

        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        # Already has an up link?
        if 'class="up"' in content:
            skipped.append(fpath)
            continue

        # Find the nav block and insert up link between prev and next
        pattern = r'(<nav class="chapter-nav">\s*<a class="prev"[^<]*</a>)\s*\n(\s*<a class="next")'

        def replacement(m):
            return m.group(1) + "\n" + cfg["up_html"] + "\n" + m.group(2)

        new_content, count = re.subn(pattern, replacement, content)

        if count == 0:
            errors.append(f"  NO MATCH: {fpath}")
            continue

        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_content)

        fixed.append(fpath)

print(f"Fixed: {len(fixed)} files")
for f in fixed:
    print(f"  + {os.path.relpath(f, BASE)}")

if skipped:
    print(f"\nAlready had up link: {len(skipped)} files")
    for f in skipped:
        print(f"  = {os.path.relpath(f, BASE)}")

if errors:
    print(f"\nErrors: {len(errors)}")
    for e in errors:
        print(e)
