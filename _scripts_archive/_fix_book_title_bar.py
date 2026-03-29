"""
Remove the book-title-bar from files that should not have it:
- agents/*.html (internal tooling pages)
- cover.html (standalone cover page)
- team.html (standalone team page)
- introduction.html (check if standalone)
"""

import re
from pathlib import Path

ROOT = Path(r"E:/Projects/LLMCourse")

# Patterns for files that should NOT have the bar
REMOVE_FROM = []

# All agents/*.html
for f in sorted(ROOT.glob("agents/*.html")):
    REMOVE_FROM.append(f)

# Standalone root-level pages (not index.html/toc.html which were already excluded)
for name in ["cover.html", "team.html"]:
    p = ROOT / name
    if p.exists():
        REMOVE_FROM.append(p)

BAR_PATTERN = re.compile(
    r'<div class="book-title-bar">\s*\n\s*<a href="[^"]*">Building Conversational AI with LLMs and Agents</a>\s*\n\s*</div>\s*\n',
    re.MULTILINE
)

removed = 0
for f in REMOVE_FROM:
    text = f.read_text(encoding="utf-8", errors="replace")
    if 'class="book-title-bar"' in text:
        new_text = BAR_PATTERN.sub("", text)
        if new_text != text:
            f.write_text(new_text, encoding="utf-8")
            removed += 1
            print(f"  REMOVED from: {f.relative_to(ROOT)}")

print(f"\nRemoved bar from {removed} files")
