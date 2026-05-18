"""Fix Lab callouts to canonical structure.

Safe fixes only:
  1. Title: "Hands-On Lab:" -> "Lab:" (just renaming)
  2. lab-extensions div -> lab-stretch (rename wrapper, rename h3 Extensions -> Stretch Goals)

Skip fixes that require fabricating content (e.g., creating empty Objective
sections, empty Expected Output sections).
"""
import os
import re
import glob

ROOT = r"E:\Projects\BookBlogsHome\LLMBook"

patterns = [
    os.path.join(ROOT, "part-*", "module-*", "section-*.html"),
    os.path.join(ROOT, "appendices", "*", "section-*.html"),
]

files = []
for p in patterns:
    files.extend(sorted(glob.glob(p)))

SKIP_MODULE_NAME = "tools-of-the-trade"

title_fixed = 0
extensions_fixed = 0
files_touched = set()

for fpath in files:
    rel = os.path.relpath(fpath, ROOT).replace("\\", "/")
    if SKIP_MODULE_NAME in rel:
        continue
    with open(fpath, "r", encoding="utf-8") as f:
        original = f.read()
    content = original

    # 1. Title canonicalization: "Hands-On Lab:" -> "Lab:" only inside callout-title for a lab callout
    # Look for: <div class="callout-title">Hands-On Lab: ...</div>
    new_content = re.sub(
        r'(<div\s+class="callout-title">)Hands-On Lab:\s*',
        r'\1Lab: ',
        content,
    )
    delta1 = new_content.count("<div class=\"callout-title\">Lab:") - content.count("<div class=\"callout-title\">Lab:")
    title_fixed += delta1
    content = new_content

    # 2. lab-extensions -> lab-stretch
    # Replace `<div class="lab-extensions">` with `<div class="lab-stretch">`
    new_content = content.replace('<div class="lab-extensions">', '<div class="lab-stretch">')
    if new_content != content:
        extensions_fixed += new_content.count('<div class="lab-stretch">') - content.count('<div class="lab-stretch">')
        content = new_content

    # Also rename the inner h3 "Extensions" -> "Stretch Goals" if just a plain h3
    # Patterns: <h3 id="extensions">Extensions</h3>  or  <h3>Extensions</h3>
    content = re.sub(
        r'<h3(\s+id="extensions")?>\s*Extensions\s*</h3>',
        r'<h3 id="stretch-goals">Stretch Goals</h3>',
        content,
    )

    if content != original:
        files_touched.add(rel)
        with open(fpath, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)

print(f"Title 'Hands-On Lab:' -> 'Lab:' fixes: {title_fixed}")
print(f"lab-extensions -> lab-stretch renames: {extensions_fixed}")
print(f"Files touched: {len(files_touched)}")
for f in sorted(files_touched):
    print(f"  {f}")
