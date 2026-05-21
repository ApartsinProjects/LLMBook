"""Audit: stale section references in prose text.

Builds a catalog of valid Section X.Y identifiers from existing files
under the book root, then scans every HTML page for inline references
like "Section AB.6", "see X.4", "Appendix B.3" where X.Y has no
corresponding file.

Also scans internal subsection labels: a <strong>32.1.1</strong> inside
section-30.1.html indicates the file was renumbered but internal labels
were not updated.

Usage:
    python audit_stale_refs.py --root <book-root>

Layout assumed:
    <root>/
        appendices/appendix-X/section-X.Y.html
        part-N/module-M/section-M.K.html

If your tree differs, pass --section-pattern to control the regex.
"""
from __future__ import annotations
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup


DEFAULT_SKIP = [
    'node_modules', '.git', 'output', 'backup', 'pagefind',
    'temp_epub', 'agents/', 'templates/', 'KDP/build', 'KDP/html2pub',
]


def is_skip(p: Path, skip: list[str]) -> bool:
    sp = str(p).replace('\\', '/')
    return any(s in sp for s in skip)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, required=True)
    ap.add_argument('--skip', nargs='*', default=DEFAULT_SKIP)
    args = ap.parse_args(argv)

    root: Path = args.root.resolve()
    if not root.exists():
        print(f'ERROR: root does not exist: {root}', file=sys.stderr)
        return 2

    # Build catalog of valid Section X.Y identifiers
    catalog = {}
    appendix_re = re.compile(r'section-([a-z]+)\.(\d+)\.html', re.I)
    numeric_re = re.compile(r'section-(\d+)\.(\d+)\.html')
    for f in root.rglob('section-*.html'):
        if is_skip(f, args.skip):
            continue
        m = numeric_re.match(f.name)
        if m:
            catalog[f'{m.group(1)}.{m.group(2)}'] = f
            continue
        m = appendix_re.match(f.name)
        if m:
            catalog[f'{m.group(1).upper()}.{m.group(2)}'] = f
    print(f'Catalog: {len(catalog)} section files found')
    valid = set(catalog.keys())

    # In-prose ref pattern: Section X.Y, Appendix X.Y, Chapter X.Y, see X.Y
    ref_pattern = re.compile(
        r'\b(Section|Chapter|Appendix|see)\s+([A-Z]{1,3}|\d{1,2})\.(\d+)\b',
        re.IGNORECASE
    )

    stale = []
    for p in root.rglob('*.html'):
        if is_skip(p, args.skip):
            continue
        try:
            s = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
        except Exception:
            continue
        text = s.get_text(' ', strip=True)

        for m in ref_pattern.finditer(text):
            ref = f'{m.group(2).upper()}.{m.group(3)}'
            if ref not in valid:
                ctx = text[max(0, m.start() - 30):m.end() + 30]
                # Skip false positives
                if any(w in ctx.lower() for w in ['figure', 'fig.', 'eq.',
                                                    'equation', 'algorithm',
                                                    'table', 'code fragment']):
                    continue
                stale.append({
                    'file': str(p.relative_to(root)),
                    'ref': ref,
                    'full': m.group(0),
                    'context': ctx[:100],
                })

    by_ref = Counter(s['ref'] for s in stale)
    print(f'\nStale references found: {len(stale)}')
    print('\nTop stale refs:')
    for ref, n in by_ref.most_common(20):
        print(f'  {ref}: {n} mentions')

    print('\nSample stale references:')
    for s in stale[:30]:
        print(f'  {s["file"]}')
        print(f'    "{s["full"]}"  ctx: ...{s["context"]}...')

    # Stale internal section-number labels
    print()
    print('=== STALE INTERNAL SECTION NUMBERS ===')
    stale_internal = []
    for p in root.rglob('section-*.html'):
        if is_skip(p, args.skip):
            continue
        m = numeric_re.match(p.name)
        if not m:
            continue
        expected_major = m.group(1)
        try:
            soup = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
        except Exception:
            continue
        seen_majors = Counter()
        for b in soup.find_all('strong'):
            txt = b.get_text(strip=True)
            mm = re.match(r'^(\d+)\.(\d+)\.(\d+)$', txt)
            if mm:
                seen_majors[mm.group(1)] += 1
        if seen_majors:
            dom = seen_majors.most_common(1)[0][0]
            if str(dom) != str(expected_major):
                stale_internal.append({
                    'file': str(p.relative_to(root)),
                    'expected': expected_major,
                    'found': dom,
                    'count': seen_majors[dom],
                })
    print(f'Files with stale internal labels: {len(stale_internal)}')
    for issue in stale_internal[:20]:
        print(f'  {issue["file"]}')
        print(f'    filename says {issue["expected"]}.x but content shows '
              f'{issue["found"]}.x.y ({issue["count"]} times)')

    return 0 if (not stale and not stale_internal) else 1


if __name__ == '__main__':
    raise SystemExit(main())
