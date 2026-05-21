"""Remove all inline PagefindUI initializer <script> blocks across the book.

After moving the canonical PagefindUI initializer to scripts/book.js (with
the breadcrumb processResult), the duplicate inline blocks on individual
pages cause TWO PagefindUI instances to attach to the same #search element.

This script finds each <script>...new PagefindUI({...});...</script> block
and removes it. Idempotent — safe to re-run.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent

SKIP_DIRS = {
    '_archive', 'node_modules', '.git', 'pagefind', 'KDP',
    'build', 'vendor', '.claude', '__pycache__', '.book-update',
}

# Match a <script>...</script> block that contains "new PagefindUI(" in its
# body. Non-greedy so it stops at the first </script>.
SCRIPT_RE = re.compile(
    r'<script>\s*window\.addEventListener\(\s*["\']DOMContentLoaded["\'][^<]*new PagefindUI\([^<]*?\}\s*\);\s*\}\s*\}\s*\);\s*</script>\s*',
    re.DOTALL,
)


def fix_file(path: Path, apply: bool) -> int:
    text = path.read_text(encoding='utf-8')
    new_text, n = SCRIPT_RE.subn('', text)
    if n and apply:
        path.write_text(new_text, encoding='utf-8')
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    total = 0
    for path in ROOT.rglob('*.html'):
        if any(skip in path.parts for skip in SKIP_DIRS):
            continue
        n = fix_file(path, args.apply)
        if n:
            total += n
            if args.apply:
                print(f"  stripped {n} from {path.relative_to(ROOT)}")
    print(f"\nTotal: {total} inline PagefindUI initializer block(s) {'stripped' if args.apply else 'would be stripped (dry run)'}")
    if not args.apply:
        print("(pass --apply to write)")


if __name__ == '__main__':
    main()
