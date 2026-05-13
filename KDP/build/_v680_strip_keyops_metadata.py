"""Strip auto-generated '# Key operations: ...' comments from code blocks.

The comments were inserted by an early auto-summary pipeline and produce
nonsensical metadata like 'Key operations: attention mechanism, results
display, prompt construction' inside a Modal deployment example. They
add no information and look amateurish in a production-engineering
chapter.

Also strip the leading '# Define X; implement Y, Z' meta-comments that
appear directly above the 'Key operations' line for the same reason.

Idempotent.
"""
from __future__ import annotations
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/')

# Match a Pygments-highlighted comment line containing 'Key operations:'
# Pattern: '<span class="c1"># Key operations: ...</span>' (anywhere on a line)
PYG_KEYOPS = re.compile(
    r'<span class="c1">#\s*Key operations:[^<]*</span>\s*\n?',
)
# Plain (non-Pygments) variant: '<pre>...# Key operations: ...\n'
PLAIN_KEYOPS = re.compile(
    r'^\s*#\s*Key operations:[^\n]*\n',
    re.MULTILINE,
)
# Same with the partner 'Define X; implement Y' line directly above the
# 'Key operations' line. Only strip the Define line when paired (since
# stand-alone 'Define X' might be legitimate code commentary).
PYG_DEFINE_PAIR = re.compile(
    r'<span class="c1">#\s*Define\s[^<]*</span>\s*\n'
    r'(?=<span class="c1">#\s*Key operations:)',
)
PLAIN_DEFINE_PAIR = re.compile(
    r'^\s*#\s*Define\s[^\n]*\n'
    r'(?=\s*#\s*Key operations:)',
    re.MULTILINE,
)


def main() -> int:
    n_files = 0
    n_keyops = 0
    n_defines = 0
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        original = text
        # Strip define-then-keyops pair first
        n1 = len(PYG_DEFINE_PAIR.findall(text))
        text = PYG_DEFINE_PAIR.sub('', text)
        n2 = len(PLAIN_DEFINE_PAIR.findall(text))
        text = PLAIN_DEFINE_PAIR.sub('', text)
        # Then strip standalone keyops lines
        n3 = len(PYG_KEYOPS.findall(text))
        text = PYG_KEYOPS.sub('', text)
        n4 = len(PLAIN_KEYOPS.findall(text))
        text = PLAIN_KEYOPS.sub('', text)
        if text != original:
            p.write_text(text, encoding='utf-8')
            n_files += 1
            n_keyops += n3 + n4
            n_defines += n1 + n2
            print(f'  cleaned: {p.relative_to(ROOT)}  '
                  f'(define lines: {n1+n2}, keyops lines: {n3+n4})')
    print(f'\nStripped {n_keyops} Key-operations + {n_defines} paired Define lines '
          f'across {n_files} files.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
