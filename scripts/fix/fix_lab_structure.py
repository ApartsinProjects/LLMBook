#!/usr/bin/env python3
"""
Standardize lab structure across the book.

Fixes three patterns:

Pattern A (54 files): <h2>N. Lab: ...</h2> followed by loose content
  -> <h3 class="lab-title">Lab: ...</h3> + <div class="lab">...content...</div>

Pattern B (2 files): <div class="callout lab"> intro boxes
  -> Remove (redundant with lab-collapse summary)

Pattern C (8 files): <div class="callout exercise"><div class="callout-title">Hands-On Lab</div>...</div>
  -> Remove (already hidden by book.js step 2b, just cleaning source)

The correct pattern used by book.js step 6:
  <h3 class="lab-title">Lab: Title Here</h3>
  <div class="lab">
    ... lab content ...
  </div>

Usage:
  python fix_lab_structure.py          # Dry run
  python fix_lab_structure.py --fix    # Apply changes
"""

import re
import sys
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")
SKIP_DIRS = {".git", "node_modules", "__pycache__", "_archive", "agents", "vendor"}

# Pattern A: <h2> with Lab in the title (many variations)
# Matches: "Lab: X", "N. Lab: X", "N. Practical Lab: X", "Hands-On Lab: X",
#          "N. Capstone Lab: X", etc.
LAB_H2_RE = re.compile(
    r'<h2>'
    r'(?:\d+\.\s*)?'                    # Optional "N. " prefix
    r'(?:(?:Practical|Hands-On|Capstone)\s+)?'  # Optional qualifier
    r'Lab:\s*'                          # "Lab:" required
    r'(.*?)'                            # Capture title
    r'</h2>',
    re.IGNORECASE
)

# Boundaries that end a lab section
BOUNDARY_PATTERNS = [
    r'<h2>',                         # Next major section
    r'<div class="callout exercise"', # Exercise callout
    r'<div class="callout self-check"', # Self-check
    r'<div class="whats-next"',      # What's Next
    r'<section class="bibliography"', # Bibliography
    r'</main>',                      # End of main content
    r'</article>',                   # End of article
]


def find_lab_end(content, start_pos):
    """Find where the lab content ends (next boundary element)."""
    # Search for the earliest boundary after start_pos
    earliest = len(content)
    for pattern in BOUNDARY_PATTERNS:
        idx = content.find(pattern, start_pos)
        if idx != -1 and idx < earliest:
            earliest = idx
    return earliest


def fix_pattern_a(content, dry_run=True):
    """Wrap <h2>Lab:</h2> + loose content in <div class="lab">."""
    changes = 0

    # Collect all matches first, then process in reverse to avoid offset issues
    matches = list(LAB_H2_RE.finditer(content))
    replacements = []

    for match in matches:
        pos = match.start()
        end_of_h2 = match.end()

        # Skip if already inside a <div class="lab"> or <section class="lab">
        preceding = content[max(0, pos - 300):pos]
        skip = False
        for lab_open in ['<div class="lab"', '<section class="lab"']:
            idx = preceding.rfind(lab_open)
            if idx >= 0:
                # Check if there is a matching close tag after the open
                close_tag = '</div>' if 'div' in lab_open else '</section>'
                after = preceding[idx:]
                if close_tag not in after:
                    skip = True
                    break
        if skip:
            continue

        lab_title = match.group(1).strip()

        # Find where the lab content ends
        lab_end = find_lab_end(content, end_of_h2)

        # Trim trailing whitespace before boundary
        while lab_end > end_of_h2 and content[lab_end - 1] in '\n\r\t ':
            lab_end -= 1

        lab_content = content[end_of_h2:lab_end].strip()

        if not lab_content:
            continue

        changes += 1

        if dry_run:
            line_num = content[:pos].count('\n') + 1
            print(f"    L{line_num}: [PATTERN A] Lab: {lab_title[:60]}")
            continue

        replacements.append((pos, lab_end, lab_title, lab_content))

    # Apply replacements in reverse order (last first) to preserve positions
    for pos, lab_end, lab_title, lab_content in reversed(replacements):
        new_h3 = f'<h3 class="lab-title">Lab: {lab_title}</h3>'
        new_block = f'{new_h3}\n\n<div class="lab">\n{lab_content}\n</div>'
        content = content[:pos] + new_block + '\n\n' + content[lab_end:]

    return content, changes


def fix_pattern_b(content, dry_run=True):
    """Remove <div class="callout lab"> intro boxes."""
    pattern = re.compile(
        r'\s*<div class="callout lab">\s*'
        r'<div class="callout-title">.*?</div>\s*'
        r'<p>.*?</p>\s*'
        r'</div>',
        re.DOTALL
    )
    matches = list(pattern.finditer(content))
    changes = len(matches)

    if dry_run:
        for m in matches:
            line_num = content[:m.start()].count('\n') + 1
            print(f"    L{line_num}: [PATTERN B] callout lab intro box")
        return content, changes

    content = pattern.sub('', content)
    return content, changes


def fix_pattern_c(content, dry_run=True):
    """Remove <div class="callout exercise"> with Hands-On Lab title."""
    pattern = re.compile(
        r'\s*<div class="callout exercise">\s*'
        r'<div class="callout-title">Hands-On Lab</div>\s*'
        r'<p>.*?</p>\s*'
        r'</div>',
        re.DOTALL
    )
    matches = list(pattern.finditer(content))
    changes = len(matches)

    if dry_run:
        for m in matches:
            line_num = content[:m.start()].count('\n') + 1
            print(f"    L{line_num}: [PATTERN C] callout exercise Hands-On Lab")
        return content, changes

    content = pattern.sub('', content)
    return content, changes


def process_file(filepath, dry_run=True):
    content = filepath.read_text(encoding="utf-8")
    original = content

    total_changes = 0

    # Fix Pattern A
    content, a_changes = fix_pattern_a(content, dry_run)
    total_changes += a_changes

    # Fix Pattern B
    content, b_changes = fix_pattern_b(content, dry_run)
    total_changes += b_changes

    # Fix Pattern C
    content, c_changes = fix_pattern_c(content, dry_run)
    total_changes += c_changes

    if not dry_run and content != original:
        filepath.write_text(content, encoding="utf-8")

    return total_changes


def main():
    fix = '--fix' in sys.argv

    all_files = sorted(BOOK_ROOT.glob("part-*/module-*/section-*.html"))
    all_files += sorted(BOOK_ROOT.glob("appendices/*/section-*.html"))

    total_changes = 0
    files_changed = 0

    for f in all_files:
        if any(s in str(f) for s in SKIP_DIRS):
            continue
        changes = process_file(f, dry_run=not fix)
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
