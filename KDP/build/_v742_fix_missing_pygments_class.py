"""Fix Bug B: <code class="lang-python"> blocks that should have the
pygments-highlighted class. Adds it as a prefix.

Cosmetic but consistent: ensures all lang-python blocks share the
.pygments-highlighted wrapper styling (padding, border, etc.) even if
the actual <span> coloring is missing inside.

Idempotent.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/')

# Match <code class="lang-python"> (no pygments-highlighted prefix)
RE = re.compile(
    r'(<code\s+class=")(lang-python)(")',
    re.IGNORECASE)


def main() -> int:
    fix = '--fix' in sys.argv
    files_touched = 0
    total_subs = 0
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        if 'lang-python' not in text:
            continue
        new, n = RE.subn(r'\1pygments-highlighted \2\3', text)
        if n > 0:
            files_touched += 1
            total_subs += n
            if fix and new != text:
                p.write_text(new, encoding='utf-8')

    mode = 'APPLIED' if fix else 'DRY-RUN'
    print(f'[{mode}] Files touched: {files_touched}')
    print(f'        Class fixes: {total_subs}')
    if not fix:
        print('\nRe-run with --fix to apply.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
