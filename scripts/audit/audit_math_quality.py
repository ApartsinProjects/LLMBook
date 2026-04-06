#!/usr/bin/env python3
"""Audit math quality issues in KaTeX blocks."""
import re
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")

slash_not_frac = 0
slash_files = []

for f in sorted(BOOK_ROOT.rglob("section-*.html")):
    if "_archive" in str(f):
        continue
    text = f.read_text(encoding="utf-8")

    # Find $...$ math blocks (single dollar)
    found = False
    for m in re.finditer(r'(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)', text):
        math = m.group(1)
        if "<" in math:
            continue
        # Look for a/b patterns that should be \frac{a}{b}
        if re.search(r'[a-zA-Z0-9}]\s*/\s*[a-zA-Z0-9{]', math):
            if "\\frac" not in math and "http" not in math:
                slash_not_frac += 1
                if not found:
                    slash_files.append(str(f.relative_to(BOOK_ROOT)))
                    found = True

print(f"Slash-not-frac occurrences: {slash_not_frac}")
print(f"Files affected: {len(slash_files)}")
for f in slash_files[:15]:
    print(f"  {f}")
if len(slash_files) > 15:
    print(f"  ... and {len(slash_files) - 15} more")
