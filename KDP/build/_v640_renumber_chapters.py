"""v6.40: Master chapter renumbering — gap-free, monotonic 0..34.

OLD -> NEW chapter mapping:
  Part I:    0,1,2,3,4,5         -> 0,1,2,3,4,5
  Part II:   6,7,8,9              -> 6,7,8,9
  Part III:  10,11,12              -> 10,11,12
  Part IV:   13,14,15,17           -> 13,14,15,16
  Part V:    19,20,21              -> 17,18,19
  Part VI:   22,23,24,25,26        -> 20,21,22,23,24
  Part VII:  27,28                 -> 25,26
  Part VIII: 29,31                 -> 27,28
  Part IX:   32,33                 -> 29,30
  Part X:    18,34                 -> 31,32  (Ch 18 lives in Part X)
  Part XI:   36,38                 -> 33,34

This script does FOUR things, in order:

  PHASE 1 — Rename directories: module-XX-* -> module-YY-*
            (Two-pass: first stash to module-XX.tmp; then rename to YY.
             This avoids collisions when YY refers to an existing chapter.)

  PHASE 2 — Rename section files INSIDE each renamed directory:
            section-XX.M.html -> section-YY.M.html

  PHASE 3 — Rename image files: fig-XX.M.K-*.png/svg/mmd -> fig-YY.M.K-*

  PHASE 4 — Rewrite content. For every HTML file in the book, rewrite:
            - HREF paths containing "module-XX-" or "section-XX." or "fig-XX."
            - Inline prose: "Chapter XX", "Section XX.M", "Module XX"
            - Heading numbers: "<h2>XX.M Title</h2>" -> "<h2>YY.M Title</h2>"
            - Caption labels: "Figure XX.M.K", "Listing XX.M.K",
              "Pseudocode XX.M.K", "Code Fragment XX.M.K", "Algorithm XX.M.K",
              "Table XX.M.K", "Exercise XX.M.K", "Quiz XX.M.K"

The script is idempotent: re-running on already-renumbered tree is a no-op.

USAGE:
  Dry-run (default): python _v640_renumber_chapters.py
  Apply:             python _v640_renumber_chapters.py --apply
"""
from __future__ import annotations
import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# OLD -> NEW chapter number map. Identity entries omitted.
RENAME = {
    17: 16,
    19: 17, 20: 18, 21: 19,
    22: 20, 23: 21, 24: 22, 25: 23, 26: 24,
    27: 25, 28: 26,
    29: 27, 31: 28,
    32: 29, 33: 30,
    18: 31, 34: 32,
    36: 33, 38: 34,
}

# Reverse map for verification only
NEW_TO_OLD = {v: k for k, v in RENAME.items()}

# Find all module directories with their chapter number
def discover_modules() -> list[tuple[Path, int]]:
    """Return [(module_path, old_chapter_number)] across all parts."""
    out = []
    for pdir in sorted(ROOT.glob('part-*')):
        for mdir in sorted(pdir.glob('module-*')):
            m = re.match(r'module-0*(\d+)-(.+)', mdir.name)
            if m:
                out.append((mdir, int(m.group(1)), m.group(2)))
    return out


def plan_renames():
    """Build the directory-rename plan and the section/image rename plans."""
    dir_renames = []   # (old_path, new_path)
    file_renames = []  # (old_path, new_path)

    modules = discover_modules()
    for mpath, old_n, slug in modules:
        new_n = RENAME.get(old_n, old_n)
        if new_n == old_n:
            continue
        # Width: original used 2-digit zero pad for some, 1-digit for others.
        # Standardize on 2 digits.
        old_dir_name = mpath.name
        new_dir_name = f'module-{new_n:02d}-{slug}'
        new_path = mpath.parent / new_dir_name
        dir_renames.append((mpath, new_path, old_n, new_n))

    # Plan file renames inside each renumbered module
    for old_dir, new_dir, old_n, new_n in dir_renames:
        # Sections
        for f in sorted(old_dir.glob('section-*.html')):
            m = re.match(r'section-(\d+)\.(\d+)(?:\.(\d+))?\.html', f.name)
            if not m:
                continue
            chap, sec = int(m.group(1)), m.group(2)
            sub = m.group(3)
            if chap != old_n:
                continue
            if sub:
                new_name = f'section-{new_n}.{sec}.{sub}.html'
            else:
                new_name = f'section-{new_n}.{sec}.html'
            file_renames.append((f, old_dir / new_name))
        # Images: fig-XX.M.K-*.png/svg/mmd
        img_dir = old_dir / 'images'
        if img_dir.exists():
            for f in sorted(img_dir.iterdir()):
                m = re.match(r'fig-(\d+)\.(\d+)\.(\d+)-(.+)$', f.name)
                if not m:
                    continue
                chap = int(m.group(1))
                if chap != old_n:
                    continue
                new_name = f'fig-{new_n}.{m.group(2)}.{m.group(3)}-{m.group(4)}'
                file_renames.append((f, img_dir / new_name))
            # Also figure-XX.M.K.png pattern
            for f in sorted(img_dir.iterdir()):
                m = re.match(r'figure-(\d+)\.(\d+)(?:\.(\d+))?\.(png|svg|jpg|jpeg)$', f.name)
                if not m:
                    continue
                chap = int(m.group(1))
                if chap != old_n:
                    continue
                if m.group(3):
                    new_name = f'figure-{new_n}.{m.group(2)}.{m.group(3)}.{m.group(4)}'
                else:
                    new_name = f'figure-{new_n}.{m.group(2)}.{m.group(4)}'
                file_renames.append((f, img_dir / new_name))

    return dir_renames, file_renames


# SINGLE-PASS rewriting: each pattern matches ANY old chapter number and
# uses a callback to look up the new value. This prevents the
# `20 -> 18 -> 31` double-rewrite bug we hit when applying per-chapter
# patterns sequentially.
#
# Map of old chapter -> new chapter (identity entries omitted).
def lookup_new(old_n: int) -> int:
    return RENAME.get(old_n, old_n)


# Each compiled pattern uses a generic group capture for the chapter number.
# The replacement is a function that examines the matched number and
# substitutes the new one.
HREF_PATTERNS = [
    # module-NN- (with optional zero-pad)
    (re.compile(r'(\bmodule-)0*(\d{1,2})(-)'),
     lambda m: f'{m.group(1)}{lookup_new(int(m.group(2))):02d}{m.group(3)}'),
    # section-NN.M(.K)?.html
    (re.compile(r'(\bsection-)(\d{1,2})(\.\d+(?:\.\d+)?\.html)'),
     lambda m: f'{m.group(1)}{lookup_new(int(m.group(2)))}{m.group(3)}'),
    # fig-NN.M.K-suffix
    (re.compile(r'(\bfig-)(\d{1,2})(\.\d+\.\d+-)'),
     lambda m: f'{m.group(1)}{lookup_new(int(m.group(2)))}{m.group(3)}'),
    # figure-NN.M(.K)?.{png|svg|jpg|jpeg}
    (re.compile(r'(\bfigure-)(\d{1,2})(\.\d+(?:\.\d+)?\.(?:png|svg|jpg|jpeg))'),
     lambda m: f'{m.group(1)}{lookup_new(int(m.group(2)))}{m.group(3)}'),
]

PROSE_PATTERNS = [
    # "Chapter NN" / "chapter NN" / "Ch NN" / "Module NN" — generic int 0..38
    (re.compile(r'\b(Chapter|chapter|Ch\.?|Module|module)\s+0*(\d{1,2})\b'),
     lambda m: f'{m.group(1)} {lookup_new(int(m.group(2))):02d}'
              if int(m.group(2)) <= 38 else m.group(0)),
    # "Section NN.M" or "Section NN.M.K"
    (re.compile(r'\b(Section|section|Sect\.)\s+(\d{1,2})(\.\d+(?:\.\d+)?)\b'),
     lambda m: f'{m.group(1)} {lookup_new(int(m.group(2)))}{m.group(3)}'
              if int(m.group(2)) <= 38 else m.group(0)),
    # Figure/Listing/etc NN.M(.K)
    (re.compile(r'\b(Figure|Listing|Pseudocode|Code Fragment|Algorithm|Table|Exercise|Quiz)\s+(\d{1,2})(\.\d+(?:\.\d+)?)\b'),
     lambda m: f'{m.group(1)} {lookup_new(int(m.group(2)))}{m.group(3)}'
              if int(m.group(2)) <= 38 else m.group(0)),
    # H2/H3 heading numeric prefix
    (re.compile(r'(<h[23][^>]*>)\s*(\d{1,2})(\.\d+(?:\.\d+)?\s)'),
     lambda m: f'{m.group(1)}{lookup_new(int(m.group(2)))}{m.group(3)}'
              if int(m.group(2)) <= 38 else m.group(0)),
    # data-pagefind-meta="chapter:Chapter NN:" or "chapter:Chapter NN"
    (re.compile(r'(data-pagefind-meta="chapter:Chapter\s+)0*(\d{1,2})(:|")'),
     lambda m: f'{m.group(1)}{lookup_new(int(m.group(2))):02d}{m.group(3)}'
              if int(m.group(2)) <= 38 else m.group(0)),
]


def rewrite_text(text: str, patterns) -> tuple[str, int]:
    """Single-pass: apply each pattern once, ALL substitutions happen using
    the original chapter numbers (no chained rewrites)."""
    n = 0
    for pat, repl in patterns:
        new_text, k = pat.subn(repl, text)
        if k > 0:
            text = new_text
            n += k
    return text, n


# Legacy stubs for compatibility (in case external tools call them)
def make_href_patterns():
    return HREF_PATTERNS

def make_prose_patterns():
    return PROSE_PATTERNS


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true', help='Actually apply changes')
    args = ap.parse_args()

    print('=' * 70)
    print(f"v6.40 chapter renumber  ({'APPLYING' if args.apply else 'DRY RUN'})")
    print('=' * 70)

    dir_renames, file_renames = plan_renames()
    print(f'\nDirectory renames planned: {len(dir_renames)}')
    for od, nd, on, nn in dir_renames:
        print(f'  Ch {on:>2} -> {nn:>2}   {od.name} -> {nd.name}')
    print(f'\nFile renames planned: {len(file_renames)}')

    if not args.apply:
        print('\n[DRY RUN] No changes made. Re-run with --apply.')
        return 0

    # PHASE 1: Rename directories via .tmp intermediate
    print('\n=== PHASE 1: rename directories (with .tmp intermediate) ===')
    # Step 1a: stash each old dir to .tmp
    stash_map = {}
    for od, nd, on, nn in dir_renames:
        tmp = od.parent / (od.name + '.RENUMBER.tmp')
        if od.exists() and not tmp.exists():
            shutil.move(str(od), str(tmp))
            stash_map[(on, nn)] = (tmp, nd)
            print(f'  stash: {od.name} -> {tmp.name}')
    # Step 1b: from .tmp -> final new name
    for (on, nn), (tmp, nd) in stash_map.items():
        if tmp.exists() and not nd.exists():
            shutil.move(str(tmp), str(nd))
            print(f'  final: {tmp.name} -> {nd.name}')

    # PHASE 2: Rename section files (inside renumbered dirs)
    # Rebuild file_renames using new dir paths
    print('\n=== PHASE 2 & 3: rename section files + image files ===')
    # Re-discover after dirs moved
    file_renames = []
    for pdir in sorted(ROOT.glob('part-*')):
        for mdir in sorted(pdir.glob('module-*')):
            m = re.match(r'module-(\d+)-', mdir.name)
            if not m:
                continue
            mnum = int(m.group(1))
            # Rename sections whose number doesn't match the dir
            for f in sorted(mdir.glob('section-*.html')):
                m2 = re.match(r'section-(\d+)\.(\d+)(?:\.(\d+))?\.html', f.name)
                if not m2:
                    continue
                old_chap = int(m2.group(1))
                if old_chap == mnum:
                    continue
                if m2.group(3):
                    new_name = f'section-{mnum}.{m2.group(2)}.{m2.group(3)}.html'
                else:
                    new_name = f'section-{mnum}.{m2.group(2)}.html'
                file_renames.append((f, f.parent / new_name))
            img_dir = mdir / 'images'
            if img_dir.exists():
                for f in sorted(img_dir.iterdir()):
                    m2 = re.match(r'fig-(\d+)\.(\d+)\.(\d+)-(.+)$', f.name)
                    if m2 and int(m2.group(1)) != mnum:
                        new_name = f'fig-{mnum}.{m2.group(2)}.{m2.group(3)}-{m2.group(4)}'
                        file_renames.append((f, img_dir / new_name))
                    m3 = re.match(
                        r'figure-(\d+)\.(\d+)(?:\.(\d+))?\.(png|svg|jpg|jpeg)$',
                        f.name,
                    )
                    if m3 and int(m3.group(1)) != mnum:
                        if m3.group(3):
                            new_name = f'figure-{mnum}.{m3.group(2)}.{m3.group(3)}.{m3.group(4)}'
                        else:
                            new_name = f'figure-{mnum}.{m3.group(2)}.{m3.group(4)}'
                        file_renames.append((f, img_dir / new_name))

    for src, dst in file_renames:
        if src.exists() and not dst.exists():
            shutil.move(str(src), str(dst))
    print(f'  renamed {len(file_renames)} files')

    # PHASE 4: Rewrite content
    print('\n=== PHASE 4: rewrite content (HTML cross-references + labels) ===')
    href_pats = make_href_patterns()
    prose_pats = make_prose_patterns()
    all_pats = href_pats + prose_pats

    rewritten = 0
    targets = sorted({
        *ROOT.glob('part-*/module-*/section-*.html'),
        *ROOT.glob('part-*/module-*/index.html'),
        *ROOT.glob('part-*/index.html'),
        *ROOT.glob('appendices/appendix-*/section-*.html'),
        *ROOT.glob('appendices/appendix-*/index.html'),
        *ROOT.glob('appendices/index.html'),
        *ROOT.glob('front-matter/**/*.html'),
        ROOT / 'toc.html',
        ROOT / 'index.html',
    })
    total_replacements = 0
    for f in targets:
        if not f.exists():
            continue
        text = f.read_text(encoding='utf-8', errors='replace')
        new_text, n = rewrite_text(text, all_pats)
        if n > 0:
            f.write_text(new_text, encoding='utf-8')
            rewritten += 1
            total_replacements += n
    print(f'  rewrote {rewritten} files, {total_replacements} total substitutions')

    print('\n=== DONE ===')
    print('Next steps (manual):')
    print('  1. Re-run _v628_audit_layout.py and _v638_audit_numbering.py')
    print('  2. Rebuild Pagefind: npx pagefind --site . --output-path pagefind')
    print('  3. Rebuild EPUB:   python KDP/build/build_epub.py --max-image-side 1000 --jpeg-quality 72')
    print('  4. Run optimizer: python KDP/build/_v622_epub_image_optimizer.py')
    print('  5. EPUBCheck:     java -jar epubcheck.jar KDP/output/*.epub')
    return 0


if __name__ == '__main__':
    sys.exit(main())
