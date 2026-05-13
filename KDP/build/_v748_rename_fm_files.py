"""Rename FM section files to descriptive, number-free names.

Background: the old filenames (section-fm.1a.html, section-fm.0c-...,
etc.) encode the OLD FM numbering. After the Tier B renumber the
user-visible FM.N labels shifted, leaving filenames misleading
(section-fm.1a.html is now displayed as FM.3 in the index).

Fix: rename to descriptive filenames that do not encode position, so
future renumbers do not require another rename.

Old -> New filename map:
  section-fm.1a.html              -> fm-what-this-book-covers.html
  section-fm.1b.html              -> fm-who-should-read.html
  section-fm.8.html               -> fm-problem-solution-key.html
  section-fm.4.html               -> fm-how-to-use.html
  section-fm.0-conceptual-map.html-> fm-conceptual-map.html
  section-fm.0a-reference-tables.html -> fm-reference-tables.html
  section-fm.0b-freshness-2026.html   -> fm-freshness-2026.html
  section-fm.0c-production-patterns.html -> fm-production-patterns.html
  section-fm.0d-pedagogy-kit.html -> fm-pedagogy-kit.html
  section-fm.0e-what-2026-settled.html -> fm-what-2026-settled.html

Steps:
1. For each (old, new) pair, locate the file under front-matter/.
2. Rename it (git mv preserved separately; here just os.rename).
3. Sweep all *.html and *.json files book-wide for the old filename
   string and replace with the new one. The grep is intentionally
   substring-based so URLs in any nesting level are updated.

Idempotent: skips renames where the old file does not exist (already
renamed) or where the new file already exists.

Run with: --fix to apply. Without --fix is a dry-run report.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
FM_DIR = ROOT / 'front-matter'
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/')

RENAMES = [
    ('section-fm.1a.html',                 'fm-what-this-book-covers.html'),
    ('section-fm.1b.html',                 'fm-who-should-read.html'),
    ('section-fm.8.html',                  'fm-problem-solution-key.html'),
    ('section-fm.4.html',                  'fm-how-to-use.html'),
    ('section-fm.0-conceptual-map.html',   'fm-conceptual-map.html'),
    ('section-fm.0a-reference-tables.html','fm-reference-tables.html'),
    ('section-fm.0b-freshness-2026.html',  'fm-freshness-2026.html'),
    ('section-fm.0c-production-patterns.html','fm-production-patterns.html'),
    ('section-fm.0d-pedagogy-kit.html',    'fm-pedagogy-kit.html'),
    ('section-fm.0e-what-2026-settled.html','fm-what-2026-settled.html'),
]


def main() -> int:
    fix = '--fix' in sys.argv
    moves: list[tuple[Path, Path]] = []
    for old, new in RENAMES:
        op = FM_DIR / old
        np = FM_DIR / new
        if not op.exists() and np.exists():
            print(f'  = already renamed: {old} -> {new}')
            continue
        if not op.exists():
            print(f'  ! missing: {old}')
            continue
        if np.exists():
            print(f'  ! collision: {new} already exists')
            continue
        moves.append((op, np))
        print(f'  + rename {old} -> {new}')

    if not moves:
        print('\nNothing to rename.')
    elif not fix:
        print(f'\n{len(moves)} files would be renamed. Re-run with --fix.')
        return 0
    else:
        for op, np in moves:
            op.rename(np)
        print(f'\nRenamed {len(moves)} files. Now sweeping references...')

    # Reference sweep: for both rename pairs and ALREADY-renamed pairs.
    # Old strings to find -> new strings to substitute.
    sub_map = dict(RENAMES)
    files_touched = 0
    total_subs = 0
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        new_text = text
        for old, new in sub_map.items():
            if old in new_text:
                new_text = new_text.replace(old, new)
        if new_text != text:
            files_touched += 1
            n = sum(text.count(o) for o in sub_map)
            total_subs += n
            if fix:
                p.write_text(new_text, encoding='utf-8')
    # Same for JSON (spine manifest etc.)
    for p in sorted(ROOT.rglob('*.json')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        new_text = text
        for old, new in sub_map.items():
            if old in new_text:
                new_text = new_text.replace(old, new)
        if new_text != text:
            files_touched += 1
            n = sum(text.count(o) for o in sub_map)
            total_subs += n
            if fix:
                p.write_text(new_text, encoding='utf-8')

    mode = 'APPLIED' if fix else 'DRY-RUN'
    print(f'[{mode}] Reference sweep: {files_touched} files, {total_subs} substitutions')
    return 0


if __name__ == '__main__':
    sys.exit(main())
