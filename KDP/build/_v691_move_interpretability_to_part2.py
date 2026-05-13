"""8th edition Wave 23 / A.1: move Interpretability (Ch 31) from Part X
(Frontiers) to Part II (Understanding LLMs).

Strategy: physical move WITHOUT renumbering the chapter. The chapter
stays 'Chapter 31' to preserve every cross-reference's number. Only
the directory location moves: part-10-frontiers/module-31-
interpretability -> part-2-understanding-llms/module-31-interpretability.

Steps:
1. Move the directory tree.
2. Rewrite every absolute-from-project-root path
   'part-10-frontiers/module-31-interpretability/' ->
   'part-2-understanding-llms/module-31-interpretability/' in every
   HTML file book-wide (39 inbound references identified).
3. Section files inside the moved chapter use relative paths like
   '../../part-N/module-X/...'. Since both Part X and Part II are at
   the same depth (root/part-PART/module-MODULE/), these RELATIVE paths
   already resolve correctly without changes. No edits needed inside
   the moved chapter for inbound part-2 / part-3 / ... links.
4. The part-label in chapter index + section metadata gets set to
   'Part II: Understanding LLMs' (was 'Part X: Frontiers' or
   inconsistent). Use _v660's mapping or update directly.

Idempotent: if the source directory has already moved, the script
just runs the rewrite step and reports zero changes.
"""
from __future__ import annotations
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/')

SRC = ROOT / 'part-10-frontiers' / 'module-31-interpretability'
DST = ROOT / 'part-2-understanding-llms' / 'module-31-interpretability'

OLD_PATH = 'part-10-frontiers/module-31-interpretability'
NEW_PATH = 'part-2-understanding-llms/module-31-interpretability'

OLD_PART_LABEL = 'Part X: Frontiers'
NEW_PART_LABEL = 'Part II: Understanding LLMs'


def main() -> int:
    # Step 1: Move directory if not already moved
    if SRC.exists():
        if DST.exists():
            print(f'ERROR: both source and destination exist; aborting')
            return 1
        print(f'Moving {SRC.relative_to(ROOT)} -> {DST.relative_to(ROOT)}')
        shutil.move(str(SRC), str(DST))
    elif DST.exists():
        print(f'Source already moved (idempotent path).')
    else:
        print(f'ERROR: source {SRC} not found and destination not present')
        return 1

    # Step 2: Rewrite all path references and part-label strings
    n_files = 0
    n_path_replacements = 0
    n_label_replacements = 0
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        original = text
        # Path rewrite (only does anything where the old path is still mentioned)
        old_count = text.count(OLD_PATH)
        text = text.replace(OLD_PATH, NEW_PATH)
        n_path_replacements += old_count

        # Update part-label inside the moved chapter only
        # (other chapters' part-labels remain whatever they should be)
        if 'module-31-interpretability' in sp.replace('\\', '/'):
            old_label_count = text.count(OLD_PART_LABEL)
            text = text.replace(OLD_PART_LABEL, NEW_PART_LABEL)
            n_label_replacements += old_label_count

        if text != original:
            p.write_text(text, encoding='utf-8')
            n_files += 1
    print(f'Rewrote {n_path_replacements} path references + {n_label_replacements} '
          f'part-label strings across {n_files} files.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
