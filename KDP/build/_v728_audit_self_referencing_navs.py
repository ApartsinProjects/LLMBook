"""Audit for self-referencing chapter-nav links book-wide.

Symptom: section-35.4.html has `<a class="next" href="section-35.4.html">`
which points to itself. Root cause is likely the v727 renumber rewriting
chapter numbers in the href but leaving anchor text that mentioned a
DIFFERENT page (e.g., the next chapter's first section).

This audit walks every chapter-nav and reports any prev/up/next that
points to the page itself.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/')

NAV_BLOCK = re.compile(
    r'<nav\s+class="chapter-nav"[^>]*>([\s\S]*?)</nav>', re.IGNORECASE)
A_TAG = re.compile(
    r'<a\s+class="(prev|up|next)"\s+href="([^"]+)"[^>]*>([^<]+)</a>',
    re.IGNORECASE)


def main() -> int:
    n_bad = 0
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        for nm in NAV_BLOCK.finditer(text):
            inner = nm.group(1)
            for am in A_TAG.finditer(inner):
                role = am.group(1)
                href = am.group(2).strip()
                anchor = am.group(3).strip()
                href_clean = href.split('#', 1)[0].strip()
                # Self-reference only if the resolved href is the same
                # absolute path as the source file.
                target = (p.parent / href_clean).resolve()
                if target == p.resolve():
                    print(f'  {p.relative_to(ROOT)}:')
                    print(f'    {role} -> "{href}" (self-reference)')
                    print(f'    anchor text: "{anchor}"')
                    n_bad += 1
    print(f'\nSelf-referencing nav links: {n_bad}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
