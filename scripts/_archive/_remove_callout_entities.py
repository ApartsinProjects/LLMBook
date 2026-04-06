"""Remove HTML entity icons from callout-title elements.

Strips leading HTML entities (&#NNN;, &#xHHHH;, optional &#xFE0F; variation
selectors) from callout-title divs, leaving only the descriptive text.
"""

import re
import glob
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# Pattern explanation:
#   Match the opening of a callout-title div,
#   then one or more HTML entities (decimal or hex, possibly followed by
#   a variation selector entity),
#   then optional whitespace before the remaining title text.
PATTERN = re.compile(
    r'(<div class="callout-title">)'   # group 1: opening tag
    r'((?:&#x?[0-9A-Fa-f]+;)+)'       # group 2: one or more HTML entities
    r'\s*'                              # optional whitespace after entities
)

total_replacements = 0
files_changed = 0

html_files = glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)

for filepath in sorted(html_files):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    new_content, count = PATTERN.subn(r'\1', content)

    if count > 0:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        rel = os.path.relpath(filepath, ROOT)
        print(f"  {rel}: {count} entities removed")
        total_replacements += count
        files_changed += 1

print(f"\nDone. Removed {total_replacements} entity icons from {files_changed} files.")
