"""v6.20: Strip dead FM.7 / FM.8 / FM.9 ToC entries.

USER REPORT
"FM7-FM9 in TOC do not exist"

ROOT CAUSE
toc.html lists three plain-text entries (no <a>) under the front-matter
section:
  FM.7  How This Book Was Created
  FM.8  The Wisdom Council
  FM.9  The 42-Agent Writing Team
These were process pages dropped during v3.4 restructuring (see
_v34_drop_wisdom_council_fm.py and _v34_consolidate_frontmatter.py),
but the ToC labels were never removed. They appear twice each (once in
the "compact" overview and once in the "expanded" dense ToC).

FIX
Remove every `<div class="dense-chapter">` whose dense-ch-num is FM.7,
FM.8, or FM.9. Whitespace artifacts collapse afterwards.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
TOC = ROOT / 'toc.html'

DEAD_LABELS = ['FM.7', 'FM.8', 'FM.9']


def main() -> int:
    text = TOC.read_text(encoding='utf-8')
    original = text
    removed = 0
    for label in DEAD_LABELS:
        # Match the full <div class="dense-chapter">...</div> with this label
        pat = re.compile(
            r'\s*<div class="dense-chapter">\s*'
            r'<span class="dense-ch-num">' + re.escape(label) + r'</span>'
            r'[^<]*</div>',
            re.DOTALL,
        )
        text, n = pat.subn('', text)
        removed += n
        print(f'  {label}: removed {n} entries')

    if text == original:
        print('No changes (already clean).')
        return 0

    # Collapse multiple consecutive blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    TOC.write_text(text, encoding='utf-8')
    print(f'\nTotal entries removed: {removed}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
