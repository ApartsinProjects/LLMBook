#!/usr/bin/env python3
"""Reclassify 'When to Use This Appendix' callouts from practical-example to note.

These callouts in appendix index pages use <div class="callout practical-example">
but contain guidance text, not real-world scenarios. This script changes them to
<div class="callout note"> and strips any "Real-World Scenario:" prefix from the title.

Usage:
    python fix_appendix_when_to_use.py          # dry run (default)
    python fix_appendix_when_to_use.py --fix    # apply changes
"""

import argparse
import re
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")
APPENDICES_DIR = BOOK_ROOT / "appendices"


def fix_file(path: Path, apply: bool) -> list[str]:
    """Return list of actions taken (or that would be taken) for one file."""
    text = path.read_text(encoding="utf-8")
    actions: list[str] = []

    # Pattern: a practical-example callout whose title contains "When to Use"
    pattern = re.compile(
        r'(<div\s+class="callout\s+)practical-example(">\s*'
        r'<div\s+class="callout-title">)'
        r'((?:Real-World Scenario:\s*)?When to Use[^<]*)'
        r'(</div>)',
        re.DOTALL,
    )

    def replacer(m: re.Match) -> str:
        prefix_open = m.group(1)   # '<div class="callout '
        mid = m.group(2)           # '"><div class="callout-title">'
        raw_title = m.group(3)     # title text (may have RWS prefix)
        close = m.group(4)         # '</div>'

        # Strip "Real-World Scenario: " prefix if present
        clean_title = re.sub(r'^Real-World Scenario:\s*', '', raw_title).strip()

        actions.append(f"  {path.relative_to(BOOK_ROOT)}: "
                       f"practical-example -> note | title: \"{clean_title}\"")
        return f'{prefix_open}note{mid}{clean_title}{close}'

    new_text = pattern.sub(replacer, text)

    if actions and apply:
        path.write_text(new_text, encoding="utf-8")

    return actions


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fix", action="store_true",
                        help="Apply changes (default is dry run)")
    args = parser.parse_args()

    index_files = sorted(APPENDICES_DIR.glob("*/index.html"))
    total = 0

    mode = "APPLYING" if args.fix else "DRY RUN"
    print(f"[{mode}] Scanning {len(index_files)} appendix index pages...\n")

    for path in index_files:
        actions = fix_file(path, apply=args.fix)
        for a in actions:
            print(a)
        total += len(actions)

    print(f"\n{'Fixed' if args.fix else 'Would fix'} {total} callout(s).")


if __name__ == "__main__":
    main()
