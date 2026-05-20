"""Remove empty `<div class="takeaways"></div>` containers.

Several sections have stray empty `<div class="takeaways">` blocks left over
from earlier authoring drafts. They render as empty boxes with takeaways
styling (a visual artifact). Since they have no content, the safe fix is to
remove the whole div block.
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

# Match an empty <div class="takeaways">...whitespace...</div>, including the
# surrounding blank lines.
EMPTY_DIV_RE = re.compile(
    r'\n?<div class="takeaways">\s*</div>\n?',
)


def fix_file(path: Path, apply: bool) -> int:
    text = path.read_text(encoding='utf-8')
    new_text, n = EMPTY_DIV_RE.subn('\n', text)
    if n and apply:
        path.write_text(new_text, encoding='utf-8')
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    total = 0
    for p in ROOT.rglob('*.html'):
        if any(s in p.parts for s in SKIP_DIRS):
            continue
        n = fix_file(p, args.apply)
        if n:
            print(f"  {p.relative_to(ROOT)}: {n} removed")
            total += n
    print(f"\nTotal: {total} empty takeaways divs {'removed' if args.apply else 'would be removed (dry run)'}")
    if not args.apply:
        print("(pass --apply to write)")


if __name__ == '__main__':
    main()
