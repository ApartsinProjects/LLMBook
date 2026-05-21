"""Wave 33d: Fix `</strong>:</strong>` double-close bug across all captions.

Random detector found 13+ pages with this pattern; full scan finds 245
occurrences book-wide. Pattern is always at the end of a Figure/Table/Code-Fragment
caption marker:

  bad:  <strong>Code Fragment 0.1.1</strong>:</strong> caption text
  good: <strong>Code Fragment 0.1.1</strong>: caption text

Likely a regression of Wave 17c double-wrapping followed by Wave 28 partial
collapse; some captions had `</strong>:` followed by another `</strong>` that
never got collapsed because they weren't immediately adjacent.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups', 'pagefind',
        '.book-update', 'vendor', '.claude', '_archive', 'agents', 'templates',
        'docs', 'scripts'}

BAD = re.compile(r'</strong>:\s*</strong>')


def main():
    n_files = 0
    n_total = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        new, n = BAD.subn('</strong>:', text)
        if n > 0:
            p.write_text(new, encoding='utf-8')
            n_files += 1
            n_total += n
    print(f'Fixed {n_total} </strong>:</strong> patterns in {n_files} files')


if __name__ == '__main__':
    main()
