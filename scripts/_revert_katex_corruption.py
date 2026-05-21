"""Revert \\text{right} corruption inside KaTeX delimiter config script blocks.

The fix_math_bare_text.py script accidentally matched between the two
'$$' string literals inside the KaTeX auto-render config, wrapping `right`
in \\text{}. This script reverses that targeted corruption.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent

SKIP_DIRS = {
    '_archive', 'node_modules', '.git', 'pagefind',
    'build', 'vendor', '__pycache__', '.book-update',
}

# The exact corrupted line we need to revert:
CORRUPTED = "{left: '$$', \\text{right}: '$$', display: true},"
ORIGINAL  = "{left: '$$', right: '$$', display: true},"


def main():
    apply = '--apply' in sys.argv
    total = 0
    for path in ROOT.rglob('*.html'):
        if any(s in path.parts for s in SKIP_DIRS):
            continue
        text = path.read_text(encoding='utf-8')
        if CORRUPTED not in text:
            continue
        new_text = text.replace(CORRUPTED, ORIGINAL)
        if apply:
            path.write_text(new_text, encoding='utf-8')
        total += 1
        print(f"  {path.relative_to(ROOT)}")
    print(f"\nTotal: {total} files {'reverted' if apply else 'would be reverted (dry run)'}")
    if not apply:
        print("(pass --apply to write)")


if __name__ == '__main__':
    main()
