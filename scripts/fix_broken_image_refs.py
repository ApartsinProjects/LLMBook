"""Rename image files to match the post-renumber `fig-X.Y.Z` src references.

The a/b renumber rewrote `<img src="...fig-9.1.3-foo.png"` to `fig-9.2.3-foo.png`
inside renamed section files. But the actual PNG/MMD/SVG files on disk were
NOT renamed. This script:

1. Scans section files for any `src="...fig-X.Y.Z-suffix.png"` reference.
2. For each, checks whether the file exists. If not, searches the same
   `images/` folder for `fig-*-suffix.*` files (matching the descriptive
   suffix) at any X.Y.Z numbering, and renames them to match the src.

This is a one-shot fix-up; it's safe because the descriptive suffix is
extremely specific (typically 5+ words from the figure caption).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent

SKIP_DIRS = {
    '_archive', 'node_modules', '.git', 'pagefind', 'KDP',
    'build', 'vendor', '.claude', '__pycache__', '.book-update',
}

# Match `fig-X.Y.Z-descriptive-suffix.ext` inside src=, alt=, etc.
FIG_REF_RE = re.compile(
    r'(?P<prefix>src=")(?P<path>[^"]*?fig-(?P<num>\d+\.\d+\.\d+(?:\.\d+)?)-(?P<desc>[a-z0-9-]+?)\.(?P<ext>png|svg|jpg|jpeg|mmd))(?P<suffix>")',
    re.IGNORECASE,
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    renames = []  # (old_path, new_path)
    seen_targets = set()

    for html_file in ROOT.rglob('section-*.html'):
        if any(s in html_file.parts for s in SKIP_DIRS):
            continue
        text = html_file.read_text(encoding='utf-8')
        for m in FIG_REF_RE.finditer(text):
            ref_path = m.group('path')
            num = m.group('num')
            desc = m.group('desc')
            ext = m.group('ext')
            # Compute the absolute path to where the image SHOULD be.
            # ref_path is relative to the html_file's directory.
            target = (html_file.parent / ref_path).resolve()
            if target.exists():
                continue  # already correctly named
            # Search the target's parent folder for files matching
            # `fig-*-{desc}.{ext}` at any X.Y.Z number.
            images_dir = target.parent
            if not images_dir.exists():
                continue
            candidates = list(images_dir.glob(f'fig-*-{desc}.{ext}'))
            # Also check for sibling extensions (rename them together too)
            if not candidates:
                continue
            # Pick the one with the OLD number; usually only one match exists
            old_file = candidates[0]
            new_file = target
            if new_file in seen_targets:
                continue
            seen_targets.add(new_file)
            renames.append((old_file, new_file))
            # Also rename sibling extensions (mmd, svg) if they exist with
            # the same OLD number stem.
            old_stem = old_file.stem  # without ext
            for ext2 in ('png', 'svg', 'mmd', 'jpg', 'jpeg'):
                sibling = old_file.parent / f'{old_stem}.{ext2}'
                if sibling.exists() and sibling != old_file:
                    new_sibling = new_file.parent / f'{new_file.stem}.{ext2}'
                    renames.append((sibling, new_sibling))

    # Deduplicate
    seen = set()
    deduped = []
    for old_p, new_p in renames:
        key = (old_p, new_p)
        if key in seen:
            continue
        seen.add(key)
        deduped.append((old_p, new_p))
    renames = deduped

    print(f"Found {len(renames)} image file renames needed")
    for old_p, new_p in renames[:20]:
        print(f"  {old_p.name}  ->  {new_p.name}")
    if len(renames) > 20:
        print(f"  ... and {len(renames) - 20} more")

    if args.apply:
        for old_p, new_p in renames:
            if not old_p.exists():
                continue
            if new_p.exists():
                continue  # don't overwrite
            old_p.rename(new_p)
        print(f"\nRenamed {len(renames)} files")
    else:
        print("\n(dry-run; pass --apply to rename)")


if __name__ == '__main__':
    main()
