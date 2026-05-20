"""Fix chapter index pages: align <span class="section-num"> with the new href.

After the a/b renumber, chapter index.html files have correct hrefs (e.g.,
section-5.2.html) but stale labels (e.g., <span class="section-num">5.2a</span>).

This script reads each index.html and for each section-card block, parses the
href to derive the section number, then rewrites the section-num span text.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent


# Match a section-card block, captures the href filename and the existing
# section-num text.
CARD_RE = re.compile(
    r'(<a[^>]*class="section-card"[^>]*href="section-(\d+)\.(\d+)\.html"[^>]*>\s*'
    r'<span class="section-num">)([^<]+)(</span>)',
    re.MULTILINE,
)


def fix_file(path: Path, apply: bool) -> int:
    """Returns the number of section-num spans rewritten."""
    text = path.read_text(encoding='utf-8')
    fixes = 0

    def repl(m):
        nonlocal fixes
        before = m.group(1)
        chap = m.group(2)
        sec = m.group(3)
        old_label = m.group(4)
        after = m.group(5)
        new_label = f'{chap}.{sec}'
        if old_label.strip() != new_label:
            fixes += 1
            return f'{before}{new_label}{after}'
        return m.group(0)
    new_text = CARD_RE.sub(repl, text)
    if fixes and apply:
        path.write_text(new_text, encoding='utf-8')
    return fixes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    total = 0
    for idx in ROOT.glob('part-*/module-*/index.html'):
        if '_archive' in idx.parts:
            continue
        n = fix_file(idx, args.apply)
        if n:
            print(f"  {idx.relative_to(ROOT)}: {n} fix(es)")
            total += n
    print(f"\nTotal: {total} section-num span(s) {'fixed' if args.apply else 'would be fixed (dry run)'}")
    if not args.apply:
        print("(pass --apply to write)")


if __name__ == '__main__':
    main()
