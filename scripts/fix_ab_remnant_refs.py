"""Clean up lingering X.OLD_Y.Z references inside renamed b-half files.

After the a/b renumber, b-half files were renamed (e.g., section-31.1b ->
section-31.2). Inside those files, the H2 subsection K values were renumbered
via sub_map. But Code Fragment / Figure / Algorithm / Table / Exercise labels
that happened to have K values OUTSIDE the H2 sub_map (e.g., Code Fragment
31.1.8 when sub_map only covered K 3-7) were left untouched.

This script rewrites any remaining "X.OLD_Y.Z" label inside a renamed b-half
file to "X.NEW_Y.Z" (preserving Z). Affects:
  - Code Fragment X.OLD_Y.Z -> Code Fragment X.NEW_Y.Z
  - Figure X.OLD_Y.Z -> Figure X.NEW_Y.Z
  - Algorithm X.OLD_Y.Z -> Algorithm X.NEW_Y.Z
  - Table X.OLD_Y.Z -> Table X.NEW_Y.Z
  - Exercise X.OLD_Y.Z -> Exercise X.NEW_Y.Z
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent

# Manual map of (renamed_file_path) -> (old_chap, old_sec) for files that
# were renamed via the a/b renumber. We can recover this by tracking the
# git rename data, but for now we hardcode the mapping using the plan from
# the renumber script.

# Re-derive map from current state by reading git log? Easier: hardcode the
# 50 ab renames here based on the renumber script's plan output.

# Map: (chap, new_sec) -> (chap, old_sec, letter)
AB_RENAMES = [
    # (chap, old_sec, letter, new_sec)
    (0, 3, 'a', 3),
    (0, 3, 'b', 4),
    (1, 7, 'a', 7),
    (1, 7, 'b', 8),
    (2, 3, 'a', 3),
    (2, 3, 'b', 4),
    (3, 1, 'a', 1),
    (3, 1, 'b', 2),
    (3, 2, 'a', 3),
    (3, 2, 'b', 4),
    (5, 2, 'a', 2),
    (5, 2, 'b', 3),
    (7, 1, 'a', 1),
    (7, 1, 'b', 2),
    (9, 1, 'a', 1),
    (9, 1, 'b', 2),
    (9, 4, 'a', 5),
    (9, 4, 'b', 6),
    (10, 4, 'b', 5),  # orphan
    (10, 6, 'a', 7),
    (10, 6, 'b', 8),
    (13, 5, 'a', 5),
    (13, 5, 'b', 6),
    (17, 5, 'a', 5),
    (17, 5, 'b', 6),
    (18, 1, 'a', 1),
    (18, 1, 'b', 2),
    (18, 2, 'a', 3),
    (18, 2, 'b', 4),
    (19, 3, 'a', 3),
    (19, 3, 'b', 4),
    (30, 2, 'a', 2),
    (30, 2, 'b', 3),
    (31, 1, 'a', 1),
    (31, 1, 'b', 2),
    (31, 2, 'a', 3),
    (31, 2, 'b', 4),
    (31, 4, 'b', 7),  # orphan
    (32, 1, 'a', 1),
    (32, 1, 'b', 2),
    (35, 1, 'a', 1),
    (35, 1, 'b', 2),
    (35, 5, 'a', 6),
    (35, 5, 'b', 7),
    (37, 5, 'a', 5),
    (37, 5, 'b', 6),
    (40, 6, 'a', 6),
    (40, 6, 'b', 7),
    (47, 1, 'a', 1),
    (47, 1, 'b', 2),
]


PARTS = sorted([p for p in ROOT.iterdir()
                if p.is_dir() and p.name.startswith('part-')])


def find_renamed_section(chap, new_sec):
    """Locate section-{chap}.{new_sec}.html on disk."""
    for part in PARTS:
        for mod in part.iterdir():
            if not mod.is_dir():
                continue
            f = mod / f'section-{chap}.{new_sec}.html'
            if f.exists():
                return f
    return None


# Asset label keywords. We rewrite "X.OLD_Y.Z" prefixed by any of these.
ASSET_KEYWORDS = [
    'Code Fragment', 'Code fragment',
    'Figure', 'Fig\\.', 'Fig',
    'Algorithm',
    'Table',
    'Exercise',
    'Lab',
    'Listing',
    'fig-',  # image filename prefix
]


def fix_file(path: Path, chap, old_sec, new_sec, apply: bool):
    text = path.read_text(encoding='utf-8')
    fixes = 0

    # For each asset keyword, rewrite "X.OLD_Y.Z" -> "X.NEW_Y.Z" (preserve Z)
    for kw in ASSET_KEYWORDS:
        if kw == 'fig-':
            # image filenames: src="images/fig-X.OLD_Y.Z-..." -> ...fig-X.NEW_Y.Z-...
            pat = re.compile(rf'(\bfig-){chap}\.{old_sec}\.(\d+)')
            def img_repl(m, lo=chap, no=old_sec, ns=new_sec):
                nonlocal fixes
                fixes += 1
                return f'{m.group(1)}{lo}.{ns}.{m.group(2)}'
            text = pat.sub(img_repl, text)
            continue
        # prose label
        pat = re.compile(rf'(\b{kw}\s+){chap}\.{old_sec}\.(\d+(?:\.\d+)?)')
        def kw_repl(m, lo=chap, no=old_sec, ns=new_sec):
            nonlocal fixes
            fixes += 1
            return f'{m.group(1)}{lo}.{ns}.{m.group(2)}'
        text = pat.sub(kw_repl, text)

    # ALSO rewrite "X.OLD_Y.Z" appearing in alt text or aria-label
    # Pattern: ' X.OLD_Y.Z ' or '>X.OLD_Y.Z<'  (preserve K)
    # This is broader — we restrict to inside alt= and aria-label= attributes.
    def attr_repl(m, lo=chap, no=old_sec, ns=new_sec):
        nonlocal fixes
        fixes += 1
        before = m.group(1)
        rest = m.group(2)
        # rest is the K(.W?) part
        return f'{before}{lo}.{ns}.{rest}'
    text = re.sub(
        rf'((?:alt|aria-label)="[^"]*?\b){chap}\.{old_sec}\.(\d+(?:\.\d+)?)',
        attr_repl,
        text,
    )

    if fixes and apply:
        path.write_text(text, encoding='utf-8')
    return fixes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    total = 0
    per_file = []
    for (chap, old_sec, letter, new_sec) in AB_RENAMES:
        # Skip a-half files where new_sec == old_sec (no shift, no remnants)
        if letter == 'a' and old_sec == new_sec:
            continue
        # For b-half OR a-half-shifted: find the file
        f = find_renamed_section(chap, new_sec)
        if f is None:
            print(f"  ! section-{chap}.{new_sec}.html not found")
            continue
        n = fix_file(f, chap, old_sec, new_sec, args.apply)
        if n:
            per_file.append((f.relative_to(ROOT), chap, old_sec, new_sec, n))
            total += n
    for relp, c, oy, ny, n in per_file:
        print(f"  {relp}: {n} fix(es) ({c}.{oy} -> {c}.{ny})")
    print(f"\nTotal: {total} remnant-ref fixes {'applied' if args.apply else 'would apply (dry run)'}")
    if not args.apply:
        print("(pass --apply to write)")


if __name__ == '__main__':
    main()
