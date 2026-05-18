"""Apply bibliographies from bib_data.BIBLIOGRAPHIES to the corresponding section files."""
import sys
import os

# Make the scripts dir importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bib_data import BIBLIOGRAPHIES


def insert_bibliography(file_path: str, bib_html: str) -> str:
    """Insert bib_html right before <nav class="chapter-nav">.

    Returns one of: 'inserted', 'already_has_bib', 'no_nav', 'file_missing'.
    """
    if not os.path.exists(file_path):
        return 'file_missing'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if '<details class="bibliography-collapsible"' in content:
        return 'already_has_bib'
    nav_pattern = '<nav class="chapter-nav">'
    if nav_pattern not in content:
        return 'no_nav'
    new_content = content.replace(nav_pattern, bib_html.rstrip() + '\n' + nav_pattern, 1)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return 'inserted'


def main():
    counts = {'inserted': 0, 'already_has_bib': 0, 'no_nav': 0, 'file_missing': 0}
    for rel_path, bib_html in BIBLIOGRAPHIES.items():
        result = insert_bibliography(rel_path, bib_html)
        counts[result] += 1
        if result != 'inserted':
            print(f"{result}: {rel_path}")
    print()
    print("=== Summary ===")
    for k, v in counts.items():
        print(f"  {k}: {v}")
    print(f"  total: {len(BIBLIOGRAPHIES)}")


if __name__ == '__main__':
    main()
