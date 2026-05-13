"""9th edition follow-up: detect chapter-opener figures placed INSIDE
<header class="chapter-header"> instead of after it. The visual symptom:
the chapter image lives next to the page title rather than flowing
into the content with the epigraph + Looking Back recap.

Pattern: <figure ...> (any class) appearing between <header> and </header>.

Read-only audit. Reports each file with line numbers.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/')

HEADER_BLOCK = re.compile(
    r'<header\s+class="chapter-header"[^>]*>(.*?)</header>',
    re.IGNORECASE | re.DOTALL)
FIGURE_IN = re.compile(r'<figure\b', re.IGNORECASE)
IMG_DIRECT = re.compile(r'<img\b', re.IGNORECASE)


def main() -> int:
    n_bad = 0
    bad_files: list[str] = []
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        m = HEADER_BLOCK.search(text)
        if not m:
            continue
        inner = m.group(1)
        # Filter out the avatar-style inline images inside agent-desc spans
        # by stripping <span class="agent-avatar-inline">...</span> blocks.
        inner_clean = re.sub(
            r'<span\s+class="agent-avatar-inline[^"]*"[^>]*>.*?</span>',
            ' ', inner, flags=re.DOTALL | re.IGNORECASE)
        if FIGURE_IN.search(inner_clean) or (
                IMG_DIRECT.search(inner_clean)
                and 'toc-icon' not in inner_clean.split('<img', 1)[1][:50]):
            # Avoid false positives on header search/toc icon
            n_bad += 1
            bad_files.append(sp)
            line = text[:m.start()].count('\n') + 1
            print(f'  {p.relative_to(ROOT)} : <figure>/<img> inside header (header starts L{line})')
    print(f'\nFiles with chapter opener inside <header>: {n_bad}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
