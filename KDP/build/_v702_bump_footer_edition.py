"""8th edition cleanup: rewrite all footer edition strings to
"Eighth Edition" across the book. Audit shows 408 Fifth + 1 Fourth +
1 Seventh, all of which should now read Eighth.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/')

PAT = re.compile(
    r'(First|Second|Third|Fourth|Fifth|Sixth|Seventh|Ninth)\s+Edition')


def main() -> int:
    fix = '--fix' in sys.argv
    n_files = 0
    n_subs = 0
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        text = p.read_text(encoding='utf-8', errors='replace')
        new, n = PAT.subn('Eighth Edition', text)
        if n:
            n_files += 1
            n_subs += n
            if fix:
                p.write_text(new, encoding='utf-8')
    print(f'Files touched: {n_files}; substitutions: {n_subs}')
    if not fix:
        print('Re-run with --fix to apply.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
