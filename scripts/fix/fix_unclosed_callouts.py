#!/usr/bin/env python3
"""Find and fix callout divs that are missing closing </div> tags.

Detects when a structural div (takeaways, whats-next, prerequisites, etc.)
or another callout appears inside an unclosed callout div, and inserts the
missing </div> before it.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP_DIRS = {".git", "node_modules", "__pycache__", "_archive", "agents", "vendor"}

CALLOUT_OPEN = re.compile(r'^\s*<div class="callout [^"]*">')
STRUCTURAL_OPEN = re.compile(r'^\s*<div class="(takeaways|whats-next|prerequisites|objectives|callout )">')


def fix_file(filepath):
    lines = filepath.read_text(encoding="utf-8").split('\n')
    inserts = []  # (line_index, indent) where we need to insert </div>

    in_callout = False
    callout_start = 0
    callout_depth = 0

    for i, line in enumerate(lines):
        is_callout_open = CALLOUT_OPEN.search(line)
        is_structural_open = STRUCTURAL_OPEN.search(line)

        if is_callout_open and in_callout:
            # Nested callout = unclosed outer
            indent = len(line) - len(line.lstrip())
            inserts.append((i, ' ' * indent + '</div>\n'))
            # Reset: new callout starts
            callout_start = i
            callout_depth = 0

        elif is_callout_open:
            in_callout = True
            callout_start = i
            callout_depth = 0

        if is_structural_open and in_callout and not is_callout_open:
            indent = len(line) - len(line.lstrip())
            inserts.append((i, ' ' * indent + '</div>\n'))
            in_callout = False
            callout_depth = 0

        if in_callout:
            callout_depth += line.count('<div')
            callout_depth -= line.count('</div')
            if callout_depth <= 0:
                in_callout = False

    if not inserts:
        return 0

    # Insert in reverse order to preserve line numbers
    for idx, closing_tag in reversed(inserts):
        lines.insert(idx, closing_tag.rstrip('\n'))

    filepath.write_text('\n'.join(lines), encoding="utf-8")
    return len(inserts)


def main():
    total_fixes = 0
    for html_file in sorted(ROOT.rglob("*.html")):
        if any(s in html_file.parts for s in SKIP_DIRS):
            continue
        try:
            count = fix_file(html_file)
        except Exception as e:
            print(f"ERROR: {html_file.relative_to(ROOT)}: {e}")
            continue
        if count > 0:
            print(f"Fixed: {html_file.relative_to(ROOT)} ({count} missing </div> inserted)")
            total_fixes += count

    print(f"\nInserted {total_fixes} missing </div> tags")


if __name__ == "__main__":
    main()
