"""8th edition cleanup: detect <nav class="chapter-nav"> blocks containing
orphan text not wrapped in <a class="prev|up|next"> anchors. Such navs
render as junk text at the bottom of the page (e.g., the appendix-r
case where the prev link's anchor text leaked out as bare text).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/')

NAV_RE = re.compile(r'<nav\s+class="chapter-nav"[^>]*>(.*?)</nav>', re.DOTALL)
A_TAG = re.compile(r'<a\s[^>]*>.*?</a>', re.DOTALL)
# Empty placeholder spans for "no next page" / "no prev page" are legit.
EMPTY_SPAN = re.compile(
    r'<span\s+class="(?:prev|up|next)"\s*>\s*</span>', re.IGNORECASE)


def main() -> int:
    n_bad = 0
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        text = p.read_text(encoding='utf-8', errors='replace')
        for m in NAV_RE.finditer(text):
            inner = m.group(1)
            # Strip all <a>...</a> blocks and empty <span class="prev|up|next">
            # placeholders; what remains should be only whitespace.
            residue = EMPTY_SPAN.sub('', A_TAG.sub('', inner)).strip()
            if residue:
                n_bad += 1
                snippet = ' / '.join(line.strip() for line in residue.splitlines()
                                     if line.strip())[:120]
                print(f'  {p.relative_to(ROOT)} : "{snippet}"')
    print(f'\nFiles with junk text in chapter-nav: {n_bad}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
