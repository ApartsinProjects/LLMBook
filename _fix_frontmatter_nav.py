#!/usr/bin/env python3
"""Fix missing 'up' links in all front-matter chapter-nav elements."""
import os
import re

BASE = r"E:\Projects\LLMCourse\front-matter"
fixes = []

def get_up_link(filepath):
    """Determine the correct 'up' link target and label for a given file."""
    rel = os.path.relpath(filepath, BASE).replace("\\", "/")
    basename = os.path.basename(filepath)
    parent_dir = os.path.dirname(rel)

    if parent_dir == "pathways":
        if basename == "index.html":
            return ("../index.html", "Front Matter")
        else:
            return ("index.html", "FM.2: Reading Pathways")
    elif parent_dir == "syllabi":
        if basename == "index.html":
            return ("../index.html", "Front Matter")
        else:
            return ("index.html", "FM.3: Course Syllabi")
    else:
        # Direct front-matter files
        if basename == "index.html":
            return (None, None)  # The index IS the up target; skip
        else:
            return ("index.html", "Front Matter")

def fix_file(filepath):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    up_href, up_label = get_up_link(filepath)
    if up_href is None:
        # index.html doesn't need an up link, but let's verify it's consistent
        return

    # Check if "up" class already exists
    nav_match = re.search(r'(<nav class="chapter-nav">)(.*?)(</nav>)', content, re.DOTALL)
    if not nav_match:
        fixes.append((filepath, "NO CHAPTER-NAV FOUND"))
        return

    nav_content = nav_match.group(2)

    if 'class="up"' in nav_content:
        # Already has up link
        return

    # Find prev and next links
    prev_match = re.search(r'<a\s+class="prev"\s+href="([^"]+)">(.+?)</a>', nav_content)
    next_match = re.search(r'<a\s+class="next"\s+href="([^"]+)">(.+?)</a>', nav_content)
    # Also check reverse order (class before href vs href before class)
    if not prev_match:
        prev_match = re.search(r'<a\s+href="([^"]+)"\s+class="prev">(.+?)</a>', nav_content)
    if not next_match:
        next_match = re.search(r'<a\s+href="([^"]+)"\s+class="next">(.+?)</a>', nav_content)

    # Also check for middle link without class (like section-fm.5.html)
    middle_match = re.search(r'<a\s+href="([^"]+)">([^<]+)</a>', nav_content)
    if middle_match and 'class=' not in middle_match.group(0):
        # There's an unclassed link that should be the "up" link
        old_link = middle_match.group(0)
        new_link = f'<a class="up" href="{middle_match.group(1)}">{middle_match.group(2)}</a>'
        content = content.replace(old_link, new_link, 1)
        fixes.append((filepath, f"Added class='up' to existing middle link"))
    elif prev_match and next_match:
        # Build new nav with up link inserted between prev and next
        # Detect indentation from the prev line
        indent_match = re.search(r'(\s*)<a\s+(?:class="prev"|href="[^"]+"\s+class="prev")', nav_content)
        indent = indent_match.group(1) if indent_match else "\n        "

        up_link = f'<a class="up" href="{up_href}">{up_label}</a>'

        # Find the next link in the nav and insert up before it
        if prev_match and next_match:
            # Replace the entire nav content
            new_nav_content = f'{indent}<a class="prev" href="{prev_match.group(1)}">{prev_match.group(2)}</a>{indent}<a class="up" href="{up_href}">{up_label}</a>{indent}<a class="next" href="{next_match.group(1)}">{next_match.group(2)}</a>\n    '
            old_nav = nav_match.group(0)
            new_nav = f'<nav class="chapter-nav">{new_nav_content}</nav>'
            content = content.replace(old_nav, new_nav, 1)
            fixes.append((filepath, f"Added up link: {up_href}"))
    elif prev_match and not next_match:
        # Only prev, add up after it
        indent_match = re.search(r'(\s*)<a\s+class="prev"', nav_content)
        indent = indent_match.group(1) if indent_match else "\n        "

        old_nav = nav_match.group(0)
        new_nav_content = f'{indent}<a class="prev" href="{prev_match.group(1)}">{prev_match.group(2)}</a>{indent}<a class="up" href="{up_href}">{up_label}</a>\n    '
        new_nav = f'<nav class="chapter-nav">{new_nav_content}</nav>'
        content = content.replace(old_nav, new_nav, 1)
        fixes.append((filepath, f"Added up link (no next): {up_href}"))
    elif next_match and not prev_match:
        # Only next, add up before it
        indent_match = re.search(r'(\s*)<a\s+class="next"', nav_content)
        indent = indent_match.group(1) if indent_match else "\n        "

        old_nav = nav_match.group(0)
        new_nav_content = f'{indent}<a class="up" href="{up_href}">{up_label}</a>{indent}<a class="next" href="{next_match.group(1)}">{next_match.group(2)}</a>\n    '
        new_nav = f'<nav class="chapter-nav">{new_nav_content}</nav>'
        content = content.replace(old_nav, new_nav, 1)
        fixes.append((filepath, f"Added up link (no prev): {up_href}"))
    else:
        fixes.append((filepath, "COULD NOT PARSE NAV LINKS"))
        return

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

for root, dirs, files in os.walk(BASE):
    for fn in sorted(files):
        if fn.endswith(".html"):
            fix_file(os.path.join(root, fn))

print(f"=== FIXES APPLIED: {len(fixes)} ===\n")
for filepath, desc in fixes:
    rel = os.path.relpath(filepath, r"E:\Projects\LLMCourse")
    print(f"  {rel}: {desc}")
