"""Strip leading ': ' from `alt=": <text>"` attributes (batch-generation artifact).

Many figures were generated via a template like `alt="{prefix}: {caption}"`
where `{prefix}` was sometimes empty, producing `alt=": ..."`. Screen
readers announce a literal colon. This sweep strips the leading `": "`.

Idempotent. Reports counts.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/')

# Match alt=": some text" with the leading ": "
PAT = re.compile(r'alt="(:\s+)([^"]+)"')


def main() -> int:
    files_changed = 0
    total_fixed = 0
    for p in ROOT.rglob('*.html'):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        original = text
        # Replace alt=": text" → alt="text"
        new_text, n = PAT.subn(r'alt="\2"', text)
        if n > 0:
            p.write_text(new_text, encoding='utf-8')
            files_changed += 1
            total_fixed += n
            print(f'  {p.relative_to(ROOT)}  ({n} fixed)')
    print(f'\nFixed {total_fixed} alt attributes across {files_changed} files.')
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
