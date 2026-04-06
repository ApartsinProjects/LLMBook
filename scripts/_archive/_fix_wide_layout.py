"""Fix wide-layout bug: move elements inside the content wrapper."""
import glob
import re
import os

BASE = r"E:\Projects\LLMCourse"
files = glob.glob(os.path.join(BASE, "**", "section-*.html"), recursive=True)

# The elements that should be inside the content wrapper, in order
ELEMENT_PATTERNS = [
    r'<div class="callout research-frontier">',
    r'<div class="whats-next">',
    r'<section class="bibliography">',
    r'<nav class="chapter-nav">',
]

fixed_files = []
already_ok = []
errors = []

for fpath in sorted(files):
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Determine wrapper type
    if '<main class="content">' in content:
        open_tag = '<main class="content">'
        close_tag = '</main>'
    elif '<div class="content">' in content:
        open_tag = '<div class="content">'
        # For div, we need to find the matching closing </div>
        # This is trickier; we'll handle it below
        close_tag = '</div>'
    else:
        errors.append((fpath, "No content wrapper found"))
        continue

    # Find where the content wrapper opens
    open_pos = content.find(open_tag)
    if open_pos == -1:
        errors.append((fpath, "Could not find opening tag"))
        continue

    # For <main>, find </main>
    # For <div class="content">, we need to be smarter about finding the right </div>
    if open_tag == '<main class="content">':
        close_pos = content.find('</main>', open_pos)
        if close_pos == -1:
            # No </main> at all; we need to add one before </body>
            body_close = content.rfind('</body>')
            if body_close == -1:
                errors.append((fpath, "No </body> found"))
                continue
            # Insert </main> right before </body>
            new_content = content[:body_close] + '\n</main>\n' + content[body_close:]
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_content)
            fixed_files.append((fpath, "Added missing </main> before </body>"))
            continue

        close_end = close_pos + len('</main>')
    else:
        # For <div class="content">, find the matching </div>
        # Count nested divs from open_pos
        search_start = open_pos + len(open_tag)
        depth = 1
        pos = search_start
        close_pos = -1
        while pos < len(content) and depth > 0:
            next_open = content.find('<div', pos)
            next_close = content.find('</div>', pos)
            if next_close == -1:
                break
            if next_open != -1 and next_open < next_close:
                depth += 1
                pos = next_open + 4
            else:
                depth -= 1
                if depth == 0:
                    close_pos = next_close
                pos = next_close + 6

        if close_pos == -1:
            errors.append((fpath, "Could not find matching </div> for content wrapper"))
            continue
        close_end = close_pos + len('</div>')
        close_tag = '</div>'

    # Now check: is there any target element AFTER the close tag?
    after_close = content[close_end:]

    # Check what target elements exist after the closing tag but before </body>
    body_close_in_after = after_close.find('</body>')
    if body_close_in_after == -1:
        errors.append((fpath, "No </body> after wrapper close"))
        continue

    between = after_close[:body_close_in_after]

    has_outside_elements = False
    for pat in ELEMENT_PATTERNS:
        if pat in between:
            has_outside_elements = True
            break

    if not has_outside_elements:
        already_ok.append(fpath)
        continue

    # We need to move the closing tag to after these elements.
    # Strategy: remove the current closing tag, find the right place to insert it.
    #
    # The content after close_pos through </body> contains elements that should be
    # inside the wrapper. We need to:
    # 1. Remove the closing tag at its current position
    # 2. Insert it right before </body>

    # But we need to be careful: there might be a </body></html> at the end.
    # We want the closing wrapper tag right before </body>.

    # Remove the current closing tag
    if open_tag == '<main class="content">':
        actual_close_tag = '</main>'
    else:
        actual_close_tag = '</div>'

    # Remove the closing tag at close_pos
    before_close = content[:close_pos]
    after_close_tag = content[close_end:]

    # Now find </body> in after_close_tag
    body_pos = after_close_tag.rfind('</body>')
    if body_pos == -1:
        errors.append((fpath, "No </body> found after removing close tag"))
        continue

    # Insert the closing wrapper tag before </body>
    # Make sure there's a newline
    insert_point = body_pos
    new_after = after_close_tag[:insert_point].rstrip() + '\n' + actual_close_tag + '\n' + after_close_tag[insert_point:]

    new_content = before_close + new_after

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(new_content)

    fixed_files.append((fpath, "Moved closing wrapper tag after outside elements"))

print(f"\n=== Wide Layout Fix Report ===")
print(f"Total section files scanned: {len(files)}")
print(f"Files fixed: {len(fixed_files)}")
print(f"Files already OK: {len(already_ok)}")
print(f"Errors: {len(errors)}")

if fixed_files:
    print(f"\n--- Fixed Files ({len(fixed_files)}) ---")
    for fpath, reason in fixed_files:
        rel = os.path.relpath(fpath, BASE)
        print(f"  {rel}: {reason}")

if errors:
    print(f"\n--- Errors ({len(errors)}) ---")
    for fpath, reason in errors:
        rel = os.path.relpath(fpath, BASE)
        print(f"  {rel}: {reason}")
