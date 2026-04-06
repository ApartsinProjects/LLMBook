#!/usr/bin/env python3
"""Fix chapter index.html files to match the standard structure:

    Epigraph -> Image -> Chapter Overview -> Big Picture -> Learning Objectives -> Prerequisites -> Sections List -> What's Next

Issues handled:
1. Swap Prerequisites/Learning Objectives when in wrong order (prereqs before objectives)
2. Remove extra callout elements from specific chapter index files
3. Add placeholder Big Picture callout where missing
4. Add placeholder Learning Objectives where missing

Usage:
    python fix_chapter_index_structure.py          # Dry run (report only)
    python fix_chapter_index_structure.py --fix     # Apply fixes
"""

import os
import re
import sys
import glob

BASE = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Discover all chapter index.html files (exclude _archive)
def find_chapter_indexes():
    results = []
    for pattern in ['part-*/module-*/index.html']:
        for path in glob.glob(os.path.join(BASE, pattern)):
            norm = os.path.normpath(path)
            if '_archive' not in norm:
                results.append(norm)
    results.sort()
    return results


def extract_module_num(path):
    """Extract module number from path like module-07-..."""
    m = re.search(r'module-(\d+)', path)
    return int(m.group(1)) if m else -1


def find_div_block(html, start_pos, tag_class):
    """Find a <div class="..."> block starting at or after start_pos.
    Returns (start, end) of the entire div block including closing </div>,
    or None if not found.
    Uses depth counting to handle nested divs.
    """
    # Find the opening tag
    pattern = rf'<div\s+class="{re.escape(tag_class)}"'
    match = re.search(pattern, html[start_pos:])
    if not match:
        return None

    block_start = start_pos + match.start()
    # Now count div depth from block_start
    pos = block_start
    depth = 0
    while pos < len(html):
        # Find next div open or close
        open_match = re.search(r'<div[\s>]', html[pos:])
        close_match = re.search(r'</div>', html[pos:])

        if open_match is None and close_match is None:
            break

        open_pos = pos + open_match.start() if open_match else len(html)
        close_pos = pos + close_match.start() if close_match else len(html)

        if open_pos < close_pos:
            depth += 1
            pos = open_pos + 4  # skip past "<div"
        else:
            depth -= 1
            end_pos = close_pos + 6  # skip past "</div>"
            if depth == 0:
                # Include trailing whitespace/newlines
                while end_pos < len(html) and html[end_pos] in '\r\n':
                    end_pos += 1
                return (block_start, end_pos)
            pos = end_pos

    return None


def find_block_by_class(html, css_class):
    """Find div block by CSS class anywhere in the HTML."""
    return find_div_block(html, 0, css_class)


def find_all_blocks_by_class(html, css_class):
    """Find ALL div blocks of a given class."""
    results = []
    search_start = 0
    while search_start < len(html):
        result = find_div_block(html, search_start, css_class)
        if result is None:
            break
        results.append(result)
        search_start = result[1]
    return results


# ---- Issue 1: Swap Prerequisites and Learning Objectives if in wrong order ----

def check_and_fix_order(html, path, fix_mode):
    """Ensure learning-objectives (or objectives) comes before prerequisites (or prereqs)."""
    changes = []

    # Find objectives block (can be class="objectives" or class="learning-objectives")
    obj_block = find_block_by_class(html, 'objectives')
    if obj_block is None:
        obj_block = find_block_by_class(html, 'learning-objectives')
    # Also check for "outcomes" class (module 36 uses this)
    outcomes_block = find_block_by_class(html, 'outcomes')

    # Find prerequisites block (can be class="prereqs" or class="prerequisites")
    prereq_block = find_block_by_class(html, 'prereqs')
    if prereq_block is None:
        prereq_block = find_block_by_class(html, 'prerequisites')

    # Use objectives or outcomes, whichever exists
    effective_obj = obj_block or outcomes_block

    if effective_obj and prereq_block:
        obj_start = effective_obj[0]
        prereq_start = prereq_block[0]

        if prereq_start < obj_start:
            # Wrong order: prereqs before objectives. Swap them.
            changes.append(f"  SWAP: Prerequisites (line ~{html[:prereq_start].count(chr(10))+1}) before Learning Objectives (line ~{html[:obj_start].count(chr(10))+1})")

            if fix_mode:
                # Extract both blocks
                prereq_text = html[prereq_block[0]:prereq_block[1]]
                obj_text = html[effective_obj[0]:effective_obj[1]]

                # Determine which block comes first and second
                first_block = prereq_block  # prereqs come first (wrong)
                second_block = effective_obj  # objectives come second (wrong)

                # Get the whitespace/content between them
                between = html[first_block[1]:second_block[0]]

                # Replace the entire region from first start to second end
                new_region = obj_text + between + prereq_text
                html = html[:first_block[0]] + new_region + html[second_block[1]:]

    return html, changes


# ---- Issue 2: Remove extra callout elements ----

CALLOUTS_TO_REMOVE = {
    # module_num: [(class_name, count_to_remove)]
    17: [('callout fun-note', 2)],
    31: [('callout fun-note', 1)],
    32: [('callout fun-note', 1)],
    34: [('callout warning', 1)],
}


def check_and_remove_callouts(html, path, fix_mode):
    changes = []
    mod_num = extract_module_num(path)

    if mod_num not in CALLOUTS_TO_REMOVE:
        return html, changes

    for css_class, count in CALLOUTS_TO_REMOVE[mod_num]:
        blocks = find_all_blocks_by_class(html, css_class)
        if not blocks:
            continue

        if count > len(blocks):
            count = len(blocks)

        for i in range(count):
            block = blocks[i]
            block_text = html[block[0]:block[1]]
            # Get first 80 chars for preview
            preview = block_text[:80].replace('\n', ' ').strip()
            line_num = html[:block[0]].count('\n') + 1
            changes.append(f"  REMOVE: <div class=\"{css_class}\"> at line ~{line_num}: {preview}...")

        if fix_mode:
            # Remove blocks in reverse order to preserve positions
            for i in range(count - 1, -1, -1):
                block = blocks[i]
                start = block[0]
                end = block[1]
                # Also remove leading whitespace on the same line
                while start > 0 and html[start - 1] in ' \t':
                    start -= 1
                html = html[:start] + html[end:]

    return html, changes


# ---- Issue 3: Add Big Picture callout where missing ----

MODULES_MISSING_BIG_PICTURE = [0, 1, 2, 3, 4, 5, 6, 36, 37, 38]

BIG_PICTURE_PLACEHOLDER = """<div class="callout big-picture">
    <div class="callout-title">Big Picture</div>
    <p><strong>TODO:</strong> Add big picture overview for this chapter.</p>
</div>
"""


def check_and_add_big_picture(html, path, fix_mode):
    changes = []
    mod_num = extract_module_num(path)

    # Check if big-picture already exists
    bp_block = find_block_by_class(html, 'callout big-picture')
    if bp_block is not None:
        return html, changes

    if mod_num not in MODULES_MISSING_BIG_PICTURE:
        # Report unexpected missing big picture
        changes.append(f"  INFO: Missing Big Picture callout (not in expected list)")
        return html, changes

    changes.append(f"  ADD: Big Picture placeholder callout")

    if fix_mode:
        # Insert after the overview div
        overview_block = find_block_by_class(html, 'overview')
        if overview_block:
            insert_pos = overview_block[1]
            html = html[:insert_pos] + '\n' + BIG_PICTURE_PLACEHOLDER + '\n' + html[insert_pos:]
        else:
            changes.append(f"  WARNING: No overview block found, cannot insert Big Picture")

    return html, changes


# ---- Issue 4: Add Learning Objectives where missing ----

MODULES_MISSING_OBJECTIVES = [36, 37, 38]

OBJECTIVES_PLACEHOLDER = """<div class="learning-objectives">
    <h3>What You Will Learn</h3>
    <ul>
        <li><strong>TODO:</strong> Add learning objectives for this chapter.</li>
    </ul>
</div>
"""


def check_and_add_objectives(html, path, fix_mode):
    changes = []
    mod_num = extract_module_num(path)

    # Check if objectives/learning-objectives/outcomes already exists
    obj_block = find_block_by_class(html, 'objectives')
    lo_block = find_block_by_class(html, 'learning-objectives')
    out_block = find_block_by_class(html, 'outcomes')

    if obj_block or lo_block or out_block:
        return html, changes

    if mod_num not in MODULES_MISSING_OBJECTIVES:
        changes.append(f"  INFO: Missing Learning Objectives (not in expected list)")
        return html, changes

    changes.append(f"  ADD: Learning Objectives placeholder")

    if fix_mode:
        # Insert after prereqs (which should exist)
        prereq_block = find_block_by_class(html, 'prereqs')
        if prereq_block is None:
            prereq_block = find_block_by_class(html, 'prerequisites')

        if prereq_block:
            # After the swap, objectives should come before prereqs,
            # but if there are no objectives yet we insert after prereqs
            # and the order fix will handle it on a subsequent pass
            insert_pos = prereq_block[1]
            html = html[:insert_pos] + '\n' + OBJECTIVES_PLACEHOLDER + '\n' + html[insert_pos:]
        else:
            # Insert after big picture or overview
            bp_block = find_block_by_class(html, 'callout big-picture')
            if bp_block:
                insert_pos = bp_block[1]
            else:
                overview_block = find_block_by_class(html, 'overview')
                if overview_block:
                    insert_pos = overview_block[1]
                else:
                    changes.append(f"  WARNING: No suitable insertion point found")
                    return html, changes
            html = html[:insert_pos] + '\n' + OBJECTIVES_PLACEHOLDER + '\n' + html[insert_pos:]

    return html, changes


def process_file(path, fix_mode):
    with open(path, 'r', encoding='utf-8') as f:
        original = f.read()

    html = original
    all_changes = []

    # Run all fixes (order matters: remove callouts first, then add missing, then fix order)
    html, changes = check_and_remove_callouts(html, path, fix_mode)
    all_changes.extend(changes)

    html, changes = check_and_add_big_picture(html, path, fix_mode)
    all_changes.extend(changes)

    html, changes = check_and_add_objectives(html, path, fix_mode)
    all_changes.extend(changes)

    # Run ordering fix last (after inserts) and run it twice to handle edge cases
    html, changes = check_and_fix_order(html, path, fix_mode)
    all_changes.extend(changes)

    if fix_mode and html != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)

    return all_changes, html != original


def main():
    fix_mode = '--fix' in sys.argv
    mode_label = "FIX MODE" if fix_mode else "DRY RUN"

    print(f"=== Chapter Index Structure Fix ({mode_label}) ===\n")

    files = find_chapter_indexes()
    print(f"Found {len(files)} chapter index.html files\n")

    total_changes = 0
    files_changed = 0

    for path in files:
        rel = os.path.relpath(path, BASE)
        changes, modified = process_file(path, fix_mode)
        if changes:
            print(f"{rel}:")
            for c in changes:
                print(c)
            print()
            total_changes += len(changes)
            if modified:
                files_changed += 1

    print(f"--- Summary ---")
    print(f"Files scanned: {len(files)}")
    print(f"Issues found: {total_changes}")
    if fix_mode:
        print(f"Files modified: {files_changed}")
    else:
        print(f"Run with --fix to apply changes")


if __name__ == '__main__':
    main()
