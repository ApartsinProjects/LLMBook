"""8th edition Wave 23 / D-pass: renumber Figure N.M.K labels sequentially
within each section, and update prose cross-references to match.

Different from code fragments: each figure typically appears TWICE in
the file (once in <img alt="Figure N.M.K: ..."> and once in
<div class="diagram-caption"><strong>Figure N.M.K:</strong> ...</div>).
Both occurrences must map to the SAME new K.

Algorithm per section file:
1. Walk all `Figure N.M.K` matches in document order.
2. For each distinct (N, M, old_K), the FIRST time we see it gets the
   next available new_K within that (N, M) group.
3. Apply the same mapping to all occurrences (alt-text, caption,
   and any prose cross-reference).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/')

FIG_PAT = re.compile(r'(Figure\s+)(\d+)\.(\d+)\.(\d+)')


def main() -> int:
    fix = '--fix' in sys.argv
    n_files = 0
    n_changes = 0
    for p in sorted(ROOT.rglob('section-*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        text = p.read_text(encoding='utf-8', errors='replace')
        matches = list(FIG_PAT.finditer(text))
        if not matches:
            continue
        # Build mapping: (N, M, old_K) -> new_K based on first-seen order
        first_seen: dict[tuple[int, int, int], int] = {}
        running: dict[tuple[int, int], int] = defaultdict(int)
        for m in matches:
            n, mm, k = int(m.group(2)), int(m.group(3)), int(m.group(4))
            key = (n, mm, k)
            if key not in first_seen:
                running[(n, mm)] += 1
                first_seen[key] = running[(n, mm)]

        # Skip if mapping is identity for all keys
        if all(new == old for (_n, _mm, old), new in first_seen.items()):
            continue

        def repl(match: re.Match) -> str:
            n = int(match.group(2)); mm = int(match.group(3)); old = int(match.group(4))
            new = first_seen[(n, mm, old)]
            return f'{match.group(1)}{n}.{mm}.{new}'

        new_text = FIG_PAT.sub(repl, text)
        if new_text != text:
            n_files += 1
            n_changes += sum(1 for (_n, _mm, old), new in first_seen.items() if new != old)
            print(f'  {p.relative_to(ROOT)}: '
                  + ', '.join(f'{n}.{m}.{o}->{n}.{m}.{nw}'
                              for (n, m, o), nw in first_seen.items() if o != nw))
            if fix:
                p.write_text(new_text, encoding='utf-8')

    print(f'\nFiles needing change: {n_files}')
    print(f'Distinct figure relabels: {n_changes}')
    if not fix:
        print('Re-run with --fix to apply.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
