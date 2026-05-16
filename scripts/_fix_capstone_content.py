"""Recover Capstone Project content from old Pedagogy Kit index.

The v8 reshuffle's part-matcher missed 'Part 1: Capstone Rubric' because
the actual h2 is 'Part 1: Capstone Rubric (3 tracks + 5-dimension scoring)'.
This script grabs that content from git history and replaces the TODO
placeholder in appendix-t-capstone-project/index.html.

One-shot fix. Run once.
"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: pip install beautifulsoup4", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    # Recover old pedagogy index
    res = subprocess.run(
        ["git", "show", "617de141:appendices/appendix-p-pedagogy-kit/index.html"],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    if res.returncode != 0:
        print(f"ERROR: git show failed: {res.stderr}", file=sys.stderr)
        return 1
    old_html = res.stdout

    soup = BeautifulSoup(old_html, "html.parser")
    main_el = soup.find("main") or soup
    h2s = main_el.find_all("h2")

    capstone_chunks: list[str] = []
    capture = False
    for h2 in h2s:
        title = h2.get_text(strip=True)
        if title.startswith("Part 1:"):
            capture = True
            capstone_chunks.append(str(h2))
            for sib in h2.find_next_siblings():
                if sib.name == "h2" and sib.get_text(strip=True).startswith("Part "):
                    break
                if sib.name == "hr":
                    break
                capstone_chunks.append(str(sib))
            break

    if not capstone_chunks:
        print("ERROR: Could not find Part 1 in old pedagogy index", file=sys.stderr)
        return 1

    capstone_body = "\n".join(capstone_chunks)
    print(f"Extracted {len(capstone_body)} chars of Capstone content")

    # Read current appendix-t-capstone-project/index.html
    target = ROOT / "appendices" / "appendix-t-capstone-project" / "index.html"
    target_html = target.read_text(encoding="utf-8")

    todo_marker = (
        '<p><em>TODO: migrate content from old '
        'Pedagogy Kit index Part: Part 1: Capstone Rubric</em></p>'
    )
    if todo_marker not in target_html:
        print(f"WARNING: TODO marker not found in {target.name}; aborting")
        return 1

    new_html = target_html.replace(todo_marker, capstone_body)
    target.write_text(new_html, encoding="utf-8")
    print(f"Replaced TODO with Capstone content in {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
