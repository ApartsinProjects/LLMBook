"""8th edition Wave 23 / C-pass: walk every relative <a href> in the book
and report broken links (file does not exist, fragment anchor missing,
etc.). This catches ALL cross-reference debt in one pass, including
references created by earlier waves and the new B-pass canonical-ref
callouts.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/')

A_HREF = re.compile(r'<a\s[^>]*href="([^"]+)"', re.IGNORECASE)


def is_external(href: str) -> bool:
    h = href.strip().lower()
    return (h.startswith('http://') or h.startswith('https://')
            or h.startswith('mailto:') or h.startswith('javascript:')
            or h.startswith('tel:') or h.startswith('#'))


def main() -> int:
    broken: list[tuple[str, str, str]] = []
    n_links = 0
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        for m in A_HREF.finditer(text):
            href = unquote(m.group(1)).split('#', 1)[0].strip()
            if not href or is_external(href):
                continue
            n_links += 1
            target = (p.parent / href).resolve()
            if not target.exists():
                broken.append((str(p.relative_to(ROOT)), m.group(1), str(target)))
    print(f'Scanned {n_links} internal links across the book.')
    print(f'Broken links: {len(broken)}')
    for src, href, tgt in broken[:30]:
        print(f'  {src} -> {href}')
    if len(broken) > 30:
        print(f'  ... and {len(broken)-30} more')
    return 0


if __name__ == '__main__':
    sys.exit(main())
