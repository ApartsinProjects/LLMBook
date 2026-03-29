"""
Remove redundant inline style attributes from <a> tags inside
.part-label and .chapter-label elements across all HTML files.

The CSS in styles/book.css already defines:
  .part-label a    { color: rgba(255,255,255,0.85); }
  .chapter-label a { color: rgba(255,255,255,0.7);  }

So inline style="color: rgba(255,255,255,...); text-decoration: none;"
on those links is redundant and should be removed.
"""

import os
import re
import glob

ROOT = os.path.dirname(os.path.abspath(__file__))

# Pattern: style attribute containing color: rgba(255,255,255,...) with optional
# text-decoration and border properties. Matches the full style="..." attribute.
STYLE_ATTR_RE = re.compile(
    r'\s+style="color:\s*rgba\(255,\s*255,\s*255,\s*[\d.]+\)[^"]*"'
)

total_fixes = 0
fixed_files = 0

# Collect all HTML files, excluding agents/ directory
all_html = []
for pattern in [
    "part-*/**/*.html",
    "appendices/**/*.html",
    "capstone/**/*.html",
    "*.html",
]:
    all_html.extend(glob.glob(os.path.join(ROOT, pattern), recursive=True))

# Deduplicate and exclude agents/
seen = set()
html_files = []
for f in all_html:
    norm = os.path.normpath(f)
    if norm in seen:
        continue
    seen.add(norm)
    # Skip agents/ directory
    rel = os.path.relpath(norm, ROOT)
    if rel.startswith("agents"):
        continue
    html_files.append(norm)

html_files.sort()

for filepath in html_files:
    with open(filepath, "r", encoding="utf-8") as fh:
        content = fh.read()

    # Find style attributes on <a> tags that are inside part-label or chapter-label contexts
    # Strategy: find all <a ...> tags with the rgba(255,255,255) inline style and remove the style attr
    # We target: <a href="..." style="color: rgba(255,255,255,...); text-decoration: none;">
    # These appear in part-label divs, chapter-label divs, or elements with class="chapter-label"

    new_content, count = STYLE_ATTR_RE.subn("", content)

    if count > 0:
        with open(filepath, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(new_content)
        rel = os.path.relpath(filepath, ROOT)
        print(f"  Fixed {count} instance(s) in {rel}")
        total_fixes += count
        fixed_files += 1

print(f"\nDone: {total_fixes} inline style(s) removed across {fixed_files} file(s).")
