"""Scan every chapter index, module index, and section file for nav completeness.

Each page's <nav class="chapter-nav"> should have exactly 3 anchors with the
roles 'prev', 'up', and 'next'.

Reports each page that has fewer than 3 nav items, with which roles are missing.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

NAV_BLOCK_RE = re.compile(
    r'<nav\s+class="chapter-nav"[^>]*>(.*?)</nav>',
    re.DOTALL | re.IGNORECASE,
)
ANCHOR_RE = re.compile(
    r'<a\s+class="(prev|up|next)"[^>]*?href="([^"]+)"[^>]*>',
    re.IGNORECASE,
)

SKIP = {'_archive', 'node_modules', '.git', '.book-update', 'pagefind',
        'KDP', 'build', 'vendor', '.claude', '__pycache__'}


def walk():
    for path in ROOT.rglob('*.html'):
        if any(s in path.parts for s in SKIP):
            continue
        yield path


def main():
    missing = []   # list of (relpath, missing_roles, present_roles)
    total = 0
    no_nav = []
    for f in walk():
        text = f.read_text(encoding='utf-8', errors='replace')
        m = NAV_BLOCK_RE.search(text)
        if not m:
            # Files like toc.html, front-matter pages may not have chapter-nav
            # by design. Only flag those that have other navigation markers
            # suggesting they should.
            rel = str(f.relative_to(ROOT)).replace('\\', '/')
            # Skip top-level meta files
            if any(s in rel for s in ('toc.html', '/front-matter/', '/appendices/', 'index.html')):
                # Only flag if it's a section file or chapter index
                if not (f.name.startswith('section-') or (f.name == 'index.html' and 'module-' in rel)):
                    continue
                no_nav.append(rel)
            else:
                if f.name.startswith('section-') or (f.name == 'index.html' and ('module-' in rel or 'part-' in rel)):
                    no_nav.append(rel)
            continue
        total += 1
        roles = set(m_.group(1).lower() for m_ in ANCHOR_RE.finditer(m.group(1)))
        required = {'prev', 'up', 'next'}
        missing_roles = required - roles
        if missing_roles:
            missing.append((str(f.relative_to(ROOT)).replace('\\', '/'), sorted(missing_roles), sorted(roles)))

    print(f"Files with chapter-nav: {total}")
    print(f"Files MISSING one or more nav roles: {len(missing)}")
    print(f"Files with NO chapter-nav at all: {len(no_nav)}\n")
    if missing:
        print("=== Pages missing nav roles ===")
        for rel, miss, have in missing:
            print(f"  {rel}")
            print(f"      missing: {', '.join(miss):<25}  has: {', '.join(have)}")
    if no_nav:
        print("\n=== Pages with no chapter-nav block ===")
        for rel in no_nav[:40]:
            print(f"  {rel}")
        if len(no_nav) > 40:
            print(f"  ... and {len(no_nav)-40} more")


if __name__ == '__main__':
    main()
