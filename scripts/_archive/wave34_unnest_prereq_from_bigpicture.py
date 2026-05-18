"""Wave 34d: Fix swap-script corruption — prereq nested inside big-picture.

The earlier swap script's regex was non-greedy and matched only up to
the first `</div>` (which closed `<div class="callout-title">`), so the
prerequisites block ended up INSIDE the big-picture callout div.

Bad structure:
    <div class="callout big-picture">
    <div class="callout-title">Big Picture</div>
    <div class="prerequisites">...</div>      <- WRONG: nested inside big-picture
    <p>...</p>
    </div>

Fix to:
    <div class="callout big-picture">
    <div class="callout-title">Big Picture</div>
    <p>...</p>
    </div>
    <div class="prerequisites">...</div>      <- OUTSIDE big-picture, after it
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups', 'pagefind',
        '.book-update', 'vendor', '.claude', '_archive', 'agents', 'templates',
        'docs', 'scripts'}

# Detect the corrupt pattern:
#   <div class="callout big-picture">
#     <div class="callout-title">...</div>
#     <div class="prerequisites">...</div>     <-- this block
#     <p>...</p>                                 <-- big-picture body
#   </div>
#
# Capture groups:
#   1. opening big-picture div + callout-title div
#   2. the nested prereq div block (complete with its </div>)
#   3. the rest of big-picture body up to closing </div>
CORRUPT_RE = re.compile(
    r'(<div\s+class="callout\s+big-picture"[^>]*>\s*'
    r'<div\s+class="callout-title"[^>]*>[^<]*</div>\s*)'
    r'(<div\s+class="prerequisites"[^>]*>[\s\S]*?</div>\s*)'
    r'([\s\S]*?</div>\s*)'
    r'(?=<div|<h[1-6]|<nav|<details|<section|<figure|<p\b)',
    re.IGNORECASE,
)


def fix(text: str) -> tuple[str, int]:
    def repl(m: re.Match) -> str:
        prefix = m.group(1)
        prereq_block = m.group(2)
        body_and_close = m.group(3)
        return prefix + body_and_close + prereq_block
    return CORRUPT_RE.subn(repl, text)


def main():
    n_files = 0
    n_total = 0
    for p in sorted(ROOT.rglob('section-*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        # Cheap pre-filter: must contain the bad pattern
        if '<div class="callout big-picture">' not in text:
            continue
        if 'class="prerequisites"' not in text:
            continue
        new, n = fix(text)
        if n > 0 and new != text:
            p.write_text(new, encoding='utf-8')
            n_files += 1
            n_total += n
            print(f'  {p.relative_to(ROOT)}: unnested')
    print(f'\nUn-nested {n_total} prereq blocks from big-picture in {n_files} files')


if __name__ == '__main__':
    main()
