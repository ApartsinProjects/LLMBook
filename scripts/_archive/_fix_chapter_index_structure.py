"""
Fix all chapter index.html files to use consistent structure matching section files.

Changes:
- <header> -> <header class="chapter-header">
- <div class="container"> -> <div class="content">
- Remove <footer> elements (not used in section files)
- Ensure content wrapper closes AFTER all content
"""

import glob
import re
import os

def fix_chapter_index(filepath):
    """Fix a single chapter index.html to use standard structure."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changes = []

    # 1. Fix <header> to <header class="chapter-header">
    # Match <header> that does NOT already have class="chapter-header"
    if '<header>' in content and '<header class="chapter-header">' not in content:
        content = content.replace('<header>', '<header class="chapter-header">', 1)
        changes.append('Added class="chapter-header" to <header>')

    # Also fix closing tag consistency (should still be </header>)
    # No change needed for closing tag

    # 2. Fix <div class="container"> to <div class="content">
    if '<div class="container">' in content:
        content = content.replace('<div class="container">', '<div class="content">', 1)
        changes.append('Changed div.container to div.content')

    # 3. Remove <footer> elements
    # Match footer block (may span multiple lines)
    footer_pattern = re.compile(r'\n*<footer>.*?</footer>\n*', re.DOTALL)
    if '<footer>' in content:
        content = footer_pattern.sub('\n', content)
        changes.append('Removed <footer> element')

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return changes
    return []


def main():
    base = os.path.dirname(os.path.abspath(__file__))

    # Find all module-*/index.html files
    pattern = os.path.join(base, 'part-*', 'module-*', 'index.html')
    files = sorted(glob.glob(pattern))

    print(f"Found {len(files)} chapter index files\n")

    fixed_count = 0
    already_ok = 0

    for filepath in files:
        relpath = os.path.relpath(filepath, base)
        changes = fix_chapter_index(filepath)

        if changes:
            fixed_count += 1
            print(f"FIXED: {relpath}")
            for c in changes:
                print(f"  - {c}")
        else:
            already_ok += 1
            print(f"  OK: {relpath}")

    print(f"\nSummary: {fixed_count} files fixed, {already_ok} already correct, {len(files)} total")


if __name__ == '__main__':
    main()
