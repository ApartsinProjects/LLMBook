"""11th edition Wave 0a: Sweep stale display-text section numbers in
toc.html and front-matter/section-fm.8.html (Problem-Solution Key).

The v727 chapter renumber (8th->9th edition) updated URLs and headings
but missed link DISPLAY TEXT in two large index/lookup files. Result:
hundreds of lines look like:

    <a href=".../section-10.1.html">31.1 Attention Analysis</a>

where the URL points to the new location (10.1) but the visible
display text still uses the old chapter number (31.1). Confusing.

Strategy:
- For each <a href="...section-X.Y[.Z].html">DISPLAY</a>:
  if DISPLAY starts with N.Y[.Z] where N != X, replace the leading
  number with X. Preserve the rest of the title verbatim.
- Idempotent: only rewrites when the prefix actually mismatches.
- Reports number of fixes per file.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# Files to sweep
TARGETS = [
    ROOT / 'toc.html',
    ROOT / 'front-matter' / 'section-fm.8.html',
]

# Match: <a href="...section-X.Y(.Z)?.html">N.Y(.Z)? title</a>
# Captures:
#   url_chapter (X), url_sub (Y), url_subsub (Z optional)
#   display_chapter (N), display_sub, display_subsub
#   rest of title
LINK_RE = re.compile(
    r'(<a\s+[^>]*href="[^"]*?section-(\d+)\.(\d+)(?:\.(\d+))?\.html"[^>]*>)'
    r'(\d+)\.(\d+)(?:\.(\d+))?'
    r'([^<]*</a>)',
    re.IGNORECASE
)


def fix_file(path: Path) -> tuple[int, int]:
    """Return (fixed, total_links_examined)."""
    if not path.exists():
        return 0, 0
    html = path.read_text(encoding='utf-8')
    fixed = 0
    examined = 0

    def repl(m: re.Match) -> str:
        nonlocal fixed, examined
        examined += 1
        anchor_open = m.group(1)
        url_ch, url_sub, url_subsub = m.group(2), m.group(3), m.group(4)
        disp_ch, disp_sub, disp_subsub = m.group(5), m.group(6), m.group(7)
        rest = m.group(8)

        # If the URL chapter and display chapter agree, leave alone.
        if url_ch == disp_ch and url_sub == disp_sub and (url_subsub or '') == (disp_subsub or ''):
            return m.group(0)

        # Build corrected display number using URL
        new_disp = f'{int(url_ch)}.{int(url_sub)}'
        if url_subsub is not None:
            new_disp += f'.{int(url_subsub)}'
        fixed += 1
        return f'{anchor_open}{new_disp}{rest}'

    new_html = LINK_RE.sub(repl, html)
    if fixed:
        path.write_text(new_html, encoding='utf-8')
    return fixed, examined


def main():
    total_fixed = 0
    total_examined = 0
    for path in TARGETS:
        rel = path.relative_to(ROOT)
        fixed, examined = fix_file(path)
        total_fixed += fixed
        total_examined += examined
        print(f'  {rel}: examined {examined} link(s), fixed {fixed}')
    print(f'\nTotal: {total_fixed} display-text fixes across {len(TARGETS)} files')
    return 0


if __name__ == '__main__':
    sys.exit(main())
