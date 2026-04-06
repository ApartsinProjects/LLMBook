#!/usr/bin/env python3
"""
Fix lab visual consistency across the book.

Three fix types:

Fix 1: h2 inside div.lab -> h3.lab-title inside div.lab
  <div class="lab">
    <h2>Hands-On Lab: Title</h2>  ->  <h3 class="lab-title">Lab: Title</h3>

Fix 2: h3 without lab-title class -> add class
  <h3>Lab: Title</h3>  ->  <h3 class="lab-title">Lab: Title</h3>
  <h3>Hands-On Lab: Title</h3>  ->  <h3 class="lab-title">Lab: Title</h3>

Fix 3: h2 NOT inside div.lab -> h3.lab-title + wrap in div.lab
  (uses the fix_lab_structure.py approach with boundary detection)

Fix 4: Remove <div class="callout lab"> intro boxes (redundant)

All "Hands-On Lab:", "Practical Lab:", "Capstone Lab:", "N. Lab:",
"N. Practical Lab:" normalized to "Lab:" prefix.

Usage:
  python fix_lab_visual_consistency.py          # Dry run
  python fix_lab_visual_consistency.py --fix    # Apply
"""

import re
import sys
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")

# Matches h2 with lab-like title
H2_LAB_RE = re.compile(
    r'<h2>'
    r'(?:\d+\.\s*)?'
    r'(?:(?:Practical|Hands-On|Capstone)\s+)?'
    r'Lab:\s*'
    r'(.*?)'
    r'</h2>',
    re.IGNORECASE
)

# Matches h3 without lab-title class, with lab-like title
H3_NO_CLASS_RE = re.compile(
    r'<h3>'
    r'(?:(?:Practical|Hands-On|Capstone)\s+)?'
    r'Lab:\s*'
    r'(.*?)'
    r'</h3>',
    re.IGNORECASE
)

# Boundaries for wrapping loose lab content
BOUNDARY_PATTERNS = [
    r'<h2>',
    r'<div class="callout exercise"',
    r'<div class="callout self-check"',
    r'<div class="whats-next"',
    r'<section class="bibliography"',
    r'</main>',
    r'</article>',
]


def find_lab_end(content, start_pos):
    """Find where lab content ends (next boundary element)."""
    earliest = len(content)
    for pattern in BOUNDARY_PATTERNS:
        idx = content.find(pattern, start_pos)
        if idx != -1 and idx < earliest:
            earliest = idx
    return earliest


def is_inside_div_lab(content, pos):
    """Check if position is inside a <div class="lab"> block."""
    preceding = content[max(0, pos - 300):pos]
    if '<div class="lab"' not in preceding:
        return False
    # Make sure there's no closing </div> between the div.lab and pos
    idx = preceding.rfind('<div class="lab"')
    after = preceding[idx:]
    # Count div depth from the opening
    depth = 0
    for i in range(len(after)):
        if after[i:i+4] == '<div':
            depth += 1
        elif after[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                return False  # div.lab closed before our position
    return True


def process_file(filepath, fix=False):
    content = filepath.read_text(encoding="utf-8")
    original = content
    changes = 0

    # Fix 1 & 3: h2 labs
    matches = list(H2_LAB_RE.finditer(content))
    replacements = []

    for match in reversed(matches):
        pos = match.start()
        title = match.group(1).strip()
        inside = is_inside_div_lab(content, pos)
        ln = content[:pos].count('\n') + 1

        if inside:
            # Fix 1: Just replace h2 with h3.lab-title inside existing div.lab
            changes += 1
            if not fix:
                print(f"    L{ln}: [FIX1] h2 -> h3.lab-title inside div.lab: Lab: {title[:50]}")
                continue
            new_tag = f'<h3 class="lab-title">Lab: {title}</h3>'
            content = content[:match.start()] + new_tag + content[match.end():]
        else:
            # Fix 3: h2 not inside div.lab, need to wrap
            changes += 1
            if not fix:
                print(f"    L{ln}: [FIX3] h2 -> h3.lab-title + wrap in div.lab: Lab: {title[:50]}")
                continue
            end_of_h2 = match.end()
            lab_end = find_lab_end(content, end_of_h2)
            while lab_end > end_of_h2 and content[lab_end - 1] in '\n\r\t ':
                lab_end -= 1
            lab_content = content[end_of_h2:lab_end].strip()
            new_h3 = f'<h3 class="lab-title">Lab: {title}</h3>'
            new_block = f'{new_h3}\n\n<div class="lab">\n{lab_content}\n</div>'
            content = content[:match.start()] + new_block + '\n\n' + content[lab_end:]

    # Fix 2: h3 without lab-title class
    matches = list(H3_NO_CLASS_RE.finditer(content))
    for match in reversed(matches):
        pos = match.start()
        title = match.group(1).strip()
        ln = content[:pos].count('\n') + 1
        changes += 1
        if not fix:
            print(f"    L{ln}: [FIX2] h3 -> h3.lab-title: Lab: {title[:50]}")
            continue
        new_tag = f'<h3 class="lab-title">Lab: {title}</h3>'
        content = content[:match.start()] + new_tag + content[match.end():]

    # Fix 4: Remove callout lab intro boxes
    callout_lab_re = re.compile(
        r'\s*<div class="callout lab">\s*'
        r'<div class="callout-title">.*?</div>\s*'
        r'<p>.*?</p>\s*'
        r'</div>',
        re.DOTALL
    )
    for match in reversed(list(callout_lab_re.finditer(content))):
        ln = content[:match.start()].count('\n') + 1
        changes += 1
        if not fix:
            print(f"    L{ln}: [FIX4] Remove callout lab intro box")
            continue
        content = content[:match.start()] + content[match.end():]

    if fix and content != original:
        filepath.write_text(content, encoding="utf-8")

    return changes


def main():
    fix = '--fix' in sys.argv

    all_files = sorted(BOOK_ROOT.glob("part-*/module-*/section-*.html"))
    all_files += sorted(BOOK_ROOT.glob("appendices/*/section-*.html"))

    total_changes = 0
    files_changed = 0

    for f in all_files:
        changes = process_file(f, fix=fix)
        if changes > 0:
            files_changed += 1
            total_changes += changes
            rel = f.relative_to(BOOK_ROOT)
            if fix:
                print(f"  FIXED: {rel} ({changes} changes)")
            else:
                print(f"  ({changes} changes in {rel})")

    print(f"\n{'=' * 60}")
    print(f"Total changes: {total_changes}")
    print(f"Files affected: {files_changed}")
    if not fix and total_changes > 0:
        print(f"\nRun with --fix to apply changes.")


if __name__ == "__main__":
    main()
