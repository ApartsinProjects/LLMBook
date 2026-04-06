"""
Batch fix: Remove inline styles that are now handled by book.css.
1. Replace inline-styled <nav> with <nav class="nav-footer">
2. Strip inline style= from .part-label and .chapter-label <a> tags
"""
import re
import glob
import os

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changes = []

    # 1. Fix inline-styled nav footers
    # Match <nav style="..."> and replace with <nav class="nav-footer">
    nav_pattern = r'<nav\s+style="[^"]*display:\s*flex[^"]*">'
    nav_matches = re.findall(nav_pattern, content)
    if nav_matches:
        content = re.sub(nav_pattern, '<nav class="nav-footer">', content)
        # Also strip style= from links inside nav-footer
        # Match <a href="..." style="..."> inside nav context
        # Only strip nav-link inline styles (the ones with text-decoration, color, font-weight)
        changes.append(f"  nav: {len(nav_matches)} inline-styled <nav> -> <nav class='nav-footer'>")

    # 2. Strip inline style from .part-label a and .chapter-label a
    # Pattern: <a href="..." style="color: rgba(255,255,255,0.85); text-decoration: none;">
    part_label_pattern = r'(<div class="part-label"><a href="[^"]*")\s+style="[^"]*">'
    part_matches = re.findall(part_label_pattern, content)
    if part_matches:
        content = re.sub(part_label_pattern, r'\1>', content)
        changes.append(f"  part-label: {len(part_matches)} inline styles stripped")

    # Pattern: <a href="..." style="color: rgba(255,255,255,0.7); text-decoration: none;">
    # or with class="chapter-num"
    chapter_label_pattern = r'(<div class="chapter-label"><a href="[^"]*"(?:\s+class="[^"]*")?)\s+style="[^"]*">'
    chapter_matches = re.findall(chapter_label_pattern, content)
    if chapter_matches:
        content = re.sub(chapter_label_pattern, r'\1>', content)
        changes.append(f"  chapter-label: {len(chapter_matches)} inline styles stripped")

    # Also handle the variant where style comes before class
    chapter_label_pattern2 = r'(<div class="chapter-label"><a href="[^"]*")\s+style="[^"]*"\s+(class="[^"]*")>'
    chapter_matches2 = re.findall(chapter_label_pattern2, content)
    if chapter_matches2:
        content = re.sub(chapter_label_pattern2, r'\1 \2>', content)
        changes.append(f"  chapter-label (variant): {len(chapter_matches2)} inline styles stripped")

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return changes
    return None

# Find all HTML files
html_files = sorted(glob.glob('E:/Projects/LLMCourse/part-*/module-*/*.html'))
html_files += sorted(glob.glob('E:/Projects/LLMCourse/part-*/module-*/section-*.html'))
# Deduplicate
html_files = sorted(set(html_files))

total_fixed = 0
nav_fixed = 0
header_fixed = 0

for f in html_files:
    changes = fix_file(f)
    if changes:
        total_fixed += 1
        basename = os.path.relpath(f, 'E:/Projects/LLMCourse')
        print(f"Fixed: {basename}")
        for c in changes:
            print(c)
            if 'nav:' in c:
                nav_fixed += 1
            if 'label:' in c:
                header_fixed += 1

print(f"\n=== Summary ===")
print(f"Files modified: {total_fixed}")
print(f"Nav footers fixed: {nav_fixed}")
print(f"Header link styles stripped: {header_fixed}")
