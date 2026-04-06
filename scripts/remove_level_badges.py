"""Remove all level-badge <span> elements from HTML files in the book."""

import re
import os
from pathlib import Path

ROOT = Path(r"E:/Projects/LLMCourse")
DIRS = [d.name for d in ROOT.iterdir()
        if d.is_dir() and (d.name.startswith("part-") or d.name in ("appendices", "front-matter"))]

# Match <span class="level-badge ...">...</span> with optional whitespace before it
BADGE_RE = re.compile(r'\s*<span\s+class="level-badge[^"]*"[^>]*>[^<]*</span>')

total = 0
for d in DIRS:
    dirpath = ROOT / d
    if not dirpath.exists():
        continue
    for html_file in sorted(dirpath.rglob("*.html")):
        text = html_file.read_text(encoding="utf-8")
        new_text, count = BADGE_RE.subn("", text)
        if count > 0:
            # Clean up double spaces that may remain
            new_text = re.sub(r"  +", " ", new_text)
            html_file.write_text(new_text, encoding="utf-8")
            rel = html_file.relative_to(ROOT)
            print(f"  {rel}: {count} badge(s) removed")
            total += count

print(f"\nTotal badges removed: {total}")
