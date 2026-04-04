#!/usr/bin/env python3
"""Fix chapter-nav prev/next links across all section files.

Normalizes all section files to the format used in chapters 0-9:

<nav class="chapter-nav">
    <a href="PREV_FILE" class="prev">&#8592; Previous: PREV_TITLE</a>
    <a href="NEXT_FILE" class="next">Next: NEXT_TITLE &#8594;</a>
</nav>

- First section in chapter: no prev link (only next)
- Last section in chapter: no next link (only prev)
- Middle sections: both prev and next
"""

import os
import re
import glob
from pathlib import Path

ROOT = Path(r"E:\Projects\LLMCourse")

# Build ordered list of all module directories
MODULE_DIRS = []
for part_dir in sorted(ROOT.glob("part-*")):
    if not part_dir.is_dir():
        continue
    for mod_dir in sorted(part_dir.glob("module-*")):
        if not mod_dir.is_dir():
            continue
        MODULE_DIRS.append(mod_dir)

# Sort by module number
def mod_num(p):
    m = re.search(r'module-(\d+)', p.name)
    return int(m.group(1)) if m else 999

MODULE_DIRS.sort(key=mod_num)

def extract_h1_title(filepath):
    """Extract the title from the first <h1> tag in an HTML file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return None

    # Try various h1 patterns
    # Pattern 1: <h1>TITLE</h1> or <h1 ...>TITLE</h1>
    m = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
    if m:
        title = m.group(1)
        # Strip HTML tags from inside (e.g., <span> for section numbers)
        title = re.sub(r'<[^>]+>', ' ', title)
        # Collapse whitespace
        title = re.sub(r'\s+', ' ', title).strip()
        # Decode common HTML entities
        title = title.replace('&amp;', '&')
        title = title.replace('&#8212;', ',')
        title = title.replace('&mdash;', ',')
        title = title.replace('&#8211;', ',')
        title = title.replace('&ndash;', ',')
        title = title.replace('&middot;', '\u00b7')
        return title
    return None


def get_section_files(mod_dir):
    """Get sorted list of section-*.html files in a module directory."""
    files = list(mod_dir.glob("section-*.html"))

    def section_sort_key(p):
        m = re.search(r'section-(\d+)\.(\d+)\.html', p.name)
        if m:
            return (int(m.group(1)), int(m.group(2)))
        return (999, 999)

    files.sort(key=section_sort_key)
    return files


def build_nav_html(prev_file, prev_title, next_file, next_title):
    """Build the chapter-nav HTML block."""
    lines = ['<nav class="chapter-nav">']
    if prev_file and prev_title:
        lines.append(f'    <a href="{prev_file}" class="prev">&#8592; Previous: {prev_title}</a>')
    if next_file and next_title:
        lines.append(f'    <a href="{next_file}" class="next">Next: {next_title} &#8594;</a>')
    lines.append('</nav>')
    return '\n'.join(lines)


def replace_nav_in_file(filepath, new_nav):
    """Replace existing chapter-nav block or insert before </main> or <footer>."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match existing chapter-nav block (with possible inline styles)
    # Match from <nav class="chapter-nav"...> to </nav>
    nav_pattern = re.compile(
        r'<nav\s+class="chapter-nav"[^>]*>.*?</nav>',
        re.DOTALL
    )

    match = nav_pattern.search(content)
    if match:
        old_nav = match.group(0)
        if old_nav.strip() == new_nav.strip():
            return False  # No change needed
        content = content[:match.start()] + new_nav + content[match.end():]
    else:
        # Insert before footer or </main>
        footer_match = re.search(r'\s*<footer', content)
        main_match = re.search(r'\s*</main>', content)
        insert_pos = None
        if footer_match:
            insert_pos = footer_match.start()
        elif main_match:
            insert_pos = main_match.start()

        if insert_pos:
            content = content[:insert_pos] + '\n' + new_nav + '\n' + content[insert_pos:]
        else:
            # Append before </body> as last resort
            body_match = re.search(r'</body>', content)
            if body_match:
                content = content[:body_match.start()] + new_nav + '\n' + content[body_match.start():]
            else:
                content += '\n' + new_nav + '\n'

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True


def escape_html(text):
    """Escape & for HTML attributes, but not already-escaped entities."""
    # Replace & that are not part of existing entities
    text = re.sub(r'&(?!amp;|lt;|gt;|quot;|#\d+;|#x[0-9a-fA-F]+;)', '&amp;', text)
    return text


def main():
    total_fixed = 0
    total_checked = 0

    for mod_dir in MODULE_DIRS:
        sections = get_section_files(mod_dir)
        if not sections:
            continue

        mod_name = mod_dir.name
        # Extract module number
        m = re.search(r'module-(\d+)', mod_name)
        if not m:
            continue
        mod_num = int(m.group(1))

        # Get titles for all sections
        titles = {}
        for sf in sections:
            title = extract_h1_title(sf)
            if title:
                titles[sf.name] = title
            else:
                # Fallback: use filename
                sm = re.search(r'section-(\d+\.\d+)', sf.name)
                titles[sf.name] = f"Section {sm.group(1)}" if sm else sf.stem

        for i, sf in enumerate(sections):
            total_checked += 1
            # Determine prev and next
            if i == 0:
                prev_file = None
                prev_title = None
            else:
                prev_file = sections[i - 1].name
                prev_title = escape_html(titles.get(prev_file, prev_file))

            if i == len(sections) - 1:
                next_file = None
                next_title = None
            else:
                next_file = sections[i + 1].name
                next_title = escape_html(titles.get(next_file, next_file))

            new_nav = build_nav_html(prev_file, prev_title, next_file, next_title)
            changed = replace_nav_in_file(sf, new_nav)
            if changed:
                total_fixed += 1
                print(f"  FIXED: {mod_name}/{sf.name}")
            # else:
            #     print(f"  OK:    {mod_name}/{sf.name}")

    print(f"\nDone. Checked {total_checked} section files, fixed {total_fixed}.")


if __name__ == '__main__':
    main()
