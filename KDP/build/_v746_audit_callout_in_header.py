"""QA detector: <aside class="callout..."> or <div class="callout...">
trapped INSIDE <header class="chapter-header"> instead of placed after
the header in <main>.

Symptom: callout's note/tip/warning styling clashes with the header's
chrome (dark background, sticky positioning), and the callout pushes
the page title into an awkward layout.

Read-only audit. Reports each file with line numbers.

Run with: python _v746_audit_callout_in_header.py
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/')

HEADER_BLOCK = re.compile(
    r'<header\s+class="chapter-header"[^>]*>([\s\S]*?)</header>',
    re.IGNORECASE)
# Look for callout-class asides/divs inside header (strict match on
# closing </aside> to avoid the v744 regex bug).
CALLOUT_IN_HEADER = re.compile(
    r'<aside\s+class="callout[^"]*"[^>]*>[\s\S]*?</aside>',
    re.IGNORECASE)


def main() -> int:
    n_bad_files = 0
    n_bad_callouts = 0
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        if 'chapter-header' not in text or 'callout' not in text:
            continue
        m = HEADER_BLOCK.search(text)
        if not m:
            continue
        inner = m.group(1)
        callouts = CALLOUT_IN_HEADER.findall(inner)
        if callouts:
            n_bad_files += 1
            n_bad_callouts += len(callouts)
            line = text[:m.start()].count('\n') + 1
            print(f'  {p.relative_to(ROOT)} : {len(callouts)} callout(s) '
                  f'inside <header> (header starts L{line})')
    if n_bad_files:
        print(f'\nFound {n_bad_callouts} callout(s) trapped inside '
              f'<header> across {n_bad_files} file(s).')
        return 1  # fail QA
    print('No callouts trapped inside <header>. OK.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
