"""8th edition: detect HTML files that USE Pygments-highlighted code blocks
(class="pygments-highlighted") but DO NOT link the pygments.css stylesheet.
Result: code blocks render uncolored / unformatted.

Root cause: when sections were added in later waves, the page template
linked book.css + prism-theme.css but omitted styles/pygments.css. The
Pygments span markup (.k, .n, .nf, .c1, ...) is present in the HTML but
unstyled.

Fix mode (--fix): inject
  <link rel="stylesheet" href="<rel>/styles/pygments.css">
right after the existing book.css link, where <rel> is the relative
path back to the project root (computed per file).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/')


def rel_root(p: Path) -> str:
    """Compute relative path from p's parent up to ROOT, e.g. '../../'."""
    rel = p.parent.relative_to(ROOT)
    depth = len(rel.parts)
    if depth == 0:
        return ''
    return '../' * depth


def main() -> int:
    fix = '--fix' in sys.argv
    needs = []
    missing = []
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        if 'pygments-highlighted' not in text:
            continue
        needs.append(p)
        if 'pygments.css' in text:
            continue
        missing.append(p)
    print(f'Files using pygments-highlighted: {len(needs)}')
    print(f'  - Linking pygments.css : {len(needs) - len(missing)}')
    print(f'  - MISSING pygments.css : {len(missing)}')

    if not fix:
        print('\nFirst 20 missing-css files:')
        for p in missing[:20]:
            print(' ', p.relative_to(ROOT))
        if len(missing) > 20:
            print(f'  ... and {len(missing)-20} more')
        if missing:
            print('\nRe-run with --fix to inject the stylesheet link.')
        return 0

    n_fixed = 0
    for p in missing:
        text = p.read_text(encoding='utf-8', errors='replace')
        rel = rel_root(p)
        new_link = f'<link rel="stylesheet" href="{rel}styles/pygments.css">'
        # Insert right after the existing book.css link
        bookcss_pat = re.compile(
            r'(<link\s+rel="stylesheet"\s+href="[^"]*styles/book\.css"\s*/?>)',
            re.IGNORECASE)
        m = bookcss_pat.search(text)
        if not m:
            print(f'  SKIP (no book.css link found): {p.relative_to(ROOT)}')
            continue
        new_text = text[:m.end()] + '\n' + new_link + text[m.end():]
        p.write_text(new_text, encoding='utf-8')
        n_fixed += 1
    print(f'\nInjected pygments.css link into {n_fixed} files.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
