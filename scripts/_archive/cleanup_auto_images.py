"""
Remove auto-inserted figure blocks from the orphan-linking script.
These have: <figure> with style="max-width: 100%; height: auto; border-radius: 8px..."
"""

import re
from pathlib import Path

ROOT = Path(r"E:\Projects\LLMCourse")
SKIP_DIRS = {"vendor", "node_modules", ".git", "__pycache__", "scripts", "_lab_fragments"}

# Match figure blocks with the distinctive inline style from link_orphaned_images.py
FIGURE_PATTERN = re.compile(
    r'\n?\s*<figure>\s*\n'
    r'\s*<img src="[^"]*" alt="[^"]*" style="max-width: 100%; height: auto; border-radius: 8px; margin: 1rem auto; display: block;">\s*\n'
    r'\s*<figcaption class="diagram-caption">[^<]*</figcaption>\s*\n'
    r'\s*</figure>\s*\n?',
    re.MULTILINE
)


def main():
    removed = 0
    files_fixed = 0

    for fpath in sorted(ROOT.rglob("section-*.html")):
        rel = fpath.relative_to(ROOT)
        parts = rel.parts
        if any(p in SKIP_DIRS for p in parts):
            continue

        text = fpath.read_text(encoding="utf-8", errors="ignore")
        matches = list(FIGURE_PATTERN.finditer(text))

        if matches:
            new_text = FIGURE_PATTERN.sub('\n', text)
            fpath.write_text(new_text, encoding="utf-8")
            files_fixed += 1
            removed += len(matches)
            print(f"  {rel}: removed {len(matches)} auto-inserted figure(s)")

    print(f"\nDone: removed {removed} auto-inserted figures from {files_fixed} files.")


if __name__ == "__main__":
    main()
