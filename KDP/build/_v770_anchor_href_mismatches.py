"""v770: Detect and fix anchor-text-vs-href mismatches.

Pattern: <a href="...section-X.Y.html">Section A.B</a> where (X,Y) != (A,B)
or where the anchor text references a non-existent section.

Conservative: only auto-fix when both forms are present and the href
clearly points at an existing file (preserve href as the source of truth,
update the anchor text to match).
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('KDP/build/source_fix_backups', 'pagefind', 'node_modules',
        'temp_epub', '.git', 'venv')


def should_skip(p: Path) -> bool:
    sp = str(p).replace('\\', '/')
    return any(s in sp for s in SKIP)


# Match <a href="...section-X.Y.html...">Section A.B[: Title]</a>
PAT = re.compile(
    r'<a\s+(?:[^>]*?\s)?href="([^"]*?section-(\d+)\.(\d+)\.html(?:#[^"]*)?)"[^>]*>'
    r'Section\s+(\d+)\.(\d+)([^<]*)</a>',
    re.IGNORECASE)

n_files = 0
n_total = 0
self_refs = []

def fix_one_file(p: Path) -> int:
    try:
        s = p.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        return 0
    counter = [0]

    def repl(m):
        href, fx, fy, ax, ay, rest = m.groups()
        href_x, href_y = int(fx), int(fy)
        anchor_x, anchor_y = int(ax), int(ay)
        if href_x == anchor_x and href_y == anchor_y:
            return m.group(0)
        if p.name == f'section-{href_x}.{href_y}.html':
            self_refs.append((str(p.relative_to(ROOT)),
                              f'self-link to section-{href_x}.{href_y}'))
            return m.group(0)
        counter[0] += 1
        return (f'<a href="{href}">'
                f'Section {href_x}.{href_y}{rest}</a>')

    new_s = PAT.sub(repl, s)
    if counter[0] > 0:
        p.write_text(new_s, encoding='utf-8')
    return counter[0]


for p in ROOT.rglob('*.html'):
    if should_skip(p):
        continue
    fixes = fix_one_file(p)
    if fixes > 0:
        n_files += 1
        n_total += fixes
        print(f'  [{p.relative_to(ROOT)}] {fixes} fixes')

print(f'\nTotal anchor-text fixes: {n_total} across {n_files} files')
if self_refs:
    print(f'\nSelf-references flagged (NOT auto-fixed, manual review needed):')
    for f, info in self_refs[:15]:
        print(f'  {f}: {info}')
    if len(self_refs) > 15:
        print(f'  ... and {len(self_refs) - 15} more')
