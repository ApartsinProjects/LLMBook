"""Insert a bibliography-collapsible block before <nav class="chapter-nav"> in a section HTML file.

Usage: python bib_insert.py <file_path> <bib_file>
The bib_file should contain the full <details class="bibliography-collapsible">...</details> block.
"""
import sys
import os
import re


def insert_bibliography(file_path: str, bib_html: str) -> bool:
    """Insert bib_html right before <nav class="chapter-nav">.

    Returns True if inserted, False if not (already has bib or no chapter-nav).
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if '<details class="bibliography-collapsible"' in content:
        print(f"SKIP (already has bib): {file_path}")
        return False
    nav_pattern = '<nav class="chapter-nav">'
    if nav_pattern not in content:
        print(f"SKIP (no chapter-nav): {file_path}")
        return False
    new_content = content.replace(nav_pattern, bib_html.rstrip() + '\n' + nav_pattern, 1)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"INSERTED: {file_path}")
    return True


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: bib_insert.py <file_path> <bib_file>")
        sys.exit(1)
    file_path = sys.argv[1]
    bib_file = sys.argv[2]
    with open(bib_file, 'r', encoding='utf-8') as f:
        bib_html = f.read()
    insert_bibliography(file_path, bib_html)
