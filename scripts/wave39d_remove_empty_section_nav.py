"""Wave 39d: Remove empty `<nav class="section-nav"></nav>` blocks.

These are leftover empty markers in 15 section files (Ch 59, Ch 61).
They serve no purpose and add minor visual noise.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

PATTERN = re.compile(r'<nav class="section-nav"></nav>\s*', re.IGNORECASE)


def main():
    n_files = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        new, n = PATTERN.subn('', text)
        if n > 0 and new != text:
            p.write_text(new, encoding='utf-8')
            n_files += 1
            print(f'  {p.relative_to(ROOT)}: removed {n}')
    print(f'\nRemoved empty section-nav from {n_files} files')


if __name__ == '__main__':
    main()
