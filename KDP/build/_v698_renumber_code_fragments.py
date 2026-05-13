"""8th edition Wave 23 / D-pass: renumber Code Fragment labels sequentially
within each section, and update prose cross-references to match.

Algorithm (per section file):
1. Find all `Code Fragment N.M.K:` LABELS (inside <div class="code-caption">).
2. In document order, assign new K = 1, 2, 3, ... for that (N, M) prefix.
3. Build a mapping (N, M, old_K) -> new_K.
4. Rewrite all `Code Fragment N.M.<old>` strings in the file (both labels
   and prose) to `Code Fragment N.M.<new>`.

Idempotent: if labels are already sequential, mapping is identity and
nothing changes.

Strategy for prose: every `Code Fragment N.M.K` reference in prose is
assumed to refer to a label in the SAME section file (the common case).
We do not chase cross-section references (rare in this book).

Caveat: the assignment loop processes labels strictly in document
order, so the natural reading order becomes 1, 2, 3, ...
"""
from __future__ import annotations
import re
import sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/')

LABEL_PAT = re.compile(
    r'(<div class="code-caption">\s*<strong>\s*Code Fragment\s+)'
    r'(\d+)\.(\d+)\.(\d+)(\s*:)',
    re.IGNORECASE)

# Used for prose references (not necessarily inside code-caption div).
ANY_PAT = re.compile(
    r'(Code Fragment\s+)(\d+)\.(\d+)\.(\d+)',
    re.IGNORECASE)


def main() -> int:
    fix = '--fix' in sys.argv
    n_files_changed = 0
    n_relabels = 0
    n_prose_updates = 0
    for p in sorted(ROOT.rglob('section-*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        text = p.read_text(encoding='utf-8', errors='replace')
        labels = list(LABEL_PAT.finditer(text))
        if not labels:
            continue

        # Group labels by (N, M); within each group, assign new sequential K.
        groups: dict[tuple[int, int], list[int]] = defaultdict(list)
        for m in labels:
            n, mm, k = int(m.group(2)), int(m.group(3)), int(m.group(4))
            groups[(n, mm)].append(k)

        # Build per-group occurrence -> new_K mapping in DOC ORDER.
        # Track, per (N,M), the running counter as labels are encountered.
        new_k_per_label: list[int] = []
        running: dict[tuple[int, int], int] = defaultdict(int)
        # First pass: assign in order of appearance
        for m in labels:
            n, mm = int(m.group(2)), int(m.group(3))
            running[(n, mm)] += 1
            new_k_per_label.append(running[(n, mm)])

        # Build mapping (N, M, old_K_in_order) -> new_K for prose updates.
        # But several labels may share old_K (duplicates); a prose reference
        # to that old K is ambiguous and we cannot reliably remap. Skip
        # prose rewrite if duplicates exist; flag the file.
        per_group_olds: dict[tuple[int, int], list[int]] = defaultdict(list)
        for m, new_k in zip(labels, new_k_per_label):
            n, mm, k = int(m.group(2)), int(m.group(3)), int(m.group(4))
            per_group_olds[(n, mm)].append(k)

        has_duplicates = any(
            len(set(olds)) != len(olds) for olds in per_group_olds.values()
        )

        # Build the new text: rewrite each label with new K (and remember
        # mapping for the no-duplicates groups).
        groupwise_mapping: dict[tuple[int, int, int], int] = {}
        if not has_duplicates:
            for (n, mm), olds in per_group_olds.items():
                # The order of olds matches doc order. new_k = 1..len(olds).
                for idx, old in enumerate(olds, 1):
                    groupwise_mapping[(n, mm, old)] = idx

        # First, rewrite labels.
        local_relabels = 0
        def label_repl(match: re.Match) -> str:
            nonlocal local_relabels
            n = int(match.group(2)); mm = int(match.group(3)); old_k = int(match.group(4))
            # Determine new k by consuming the next entry from the per-group queue.
            new_k = consume[(n, mm)]
            consume[(n, mm)] += 1
            if new_k != old_k:
                local_relabels += 1
            return f'{match.group(1)}{n}.{mm}.{new_k}{match.group(5)}'

        consume: dict[tuple[int, int], int] = defaultdict(lambda: 1)
        new_text = LABEL_PAT.sub(label_repl, text)

        # Second, rewrite prose references (only if no duplicates).
        local_prose = 0
        if not has_duplicates:
            def any_repl(match: re.Match) -> str:
                nonlocal local_prose
                n = int(match.group(2)); mm = int(match.group(3)); old_k = int(match.group(4))
                key = (n, mm, old_k)
                if key in groupwise_mapping:
                    new_k = groupwise_mapping[key]
                    if new_k != old_k:
                        local_prose += 1
                        return f'{match.group(1)}{n}.{mm}.{new_k}'
                return match.group(0)
            # ANY_PAT will also match the labels we just rewrote, but they
            # already have new_k, so the mapping `key` will lookup the new_k
            # (which maps to itself) and produce no change. Wait -- the
            # mapping uses OLD_K as the key. If a label has already been
            # rewritten to new_k, looking up (n, mm, new_k) might map to a
            # different label. To avoid this, run prose rewrite on the
            # ORIGINAL text (before label rewrite), then apply the label
            # rewrite to the result.
            new_text_for_prose = ANY_PAT.sub(any_repl, text)
            # Now also rewrite the labels in new_text_for_prose:
            consume = defaultdict(lambda: 1)
            new_text = LABEL_PAT.sub(label_repl, new_text_for_prose)

        if new_text != text:
            n_files_changed += 1
            n_relabels += local_relabels
            n_prose_updates += local_prose
            tag = '!! HAS DUPLICATES (prose not rewritten)' if has_duplicates else ''
            print(f'  {p.relative_to(ROOT)}: {local_relabels} label(s), '
                  f'{local_prose} prose update(s) {tag}')
            if fix:
                p.write_text(new_text, encoding='utf-8')

    print(f'\nFiles needing change: {n_files_changed}')
    print(f'  Label rewrites    : {n_relabels}')
    print(f'  Prose rewrites    : {n_prose_updates}')
    if not fix:
        print('\nRe-run with --fix to apply.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
