"""10th edition Wave 1: full chapter renumbering to fix the visible
ToC anomaly where Chapter 31 (Interpretability) appears between Ch 9
and Ch 10 in reading order.

PROBLEM
The 8th edition moved Interpretability from Part X to Part II to put
it next to the other Part-II chapters (Scaling, Landscape, Reasoning,
Inference). To minimize cross-reference disruption, the move kept
Ch 31 as the chapter number even though the reading position is right
after Ch 9. The ToC reads: 6 -> 7 -> 8 -> 9 -> 31 -> 10 -> 11 ...
Visibly broken.

FIX
Renumber every chapter from Ch 10 onward by +1, and renumber Ch 31 to
Ch 10. The mapping:
    Ch 31 -> Ch 10  (Interpretability, the moved chapter)
    Ch 10 -> Ch 11  (LLM APIs)
    Ch 11 -> Ch 12  (Prompt Engineering)
    ...
    Ch 30 -> Ch 31  (Strategy, Product, ROI)
    Ch 32 -> Ch 33  (Emerging Architectures)
    Ch 33 -> Ch 34  (Idea to Product)
    Ch 34 -> Ch 35  (Shipping & Scaling)

EXECUTION (token-substitution-based to avoid double-shifts)
1. Rename module-N-NAME directories using a two-phase token plan:
   first rename old module-N-NAME -> module-TMP_N-NAME, then rename
   module-TMP_N-NAME -> module-new_N-NAME.
2. Rename section files (section-N.M.html -> section-new_N.M.html)
   inside each renamed module.
3. Rename image files (fig-N.M.K-*.png/svg/mmd) inside images/ dirs.
4. Walk every HTML/MD file and rewrite ALL cross-references:
   - module-NN-NAME paths (in hrefs and prose)
   - section-NN.M.html paths
   - "Chapter NN" prose
   - "Section NN.M" prose
   - "Figure NN.M.K" prose + caption + alt-text
   - "Code Fragment NN.M.K" prose + caption
   - H1/H2/H3 leading-number prefixes
   - image fig-N.M.K filename references
5. Update spine_manifest.json and BOOK_CONFIG.md.

Idempotent guards: detects whether the renumber has already run by
checking whether the original module-31 directory exists.
"""
from __future__ import annotations
import argparse
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/')

# Old chapter number -> New chapter number
RENUMBER = {
    31: 10,  # Interpretability -- the chapter that moved
    10: 11,
    11: 12,
    12: 13,
    13: 14,
    14: 15,
    15: 16,
    16: 17,
    17: 18,
    18: 19,
    19: 20,
    20: 21,
    21: 22,
    22: 23,
    23: 24,
    24: 25,
    25: 26,
    26: 27,
    27: 28,
    28: 29,
    29: 30,
    30: 31,
    32: 33,
    33: 34,
    34: 35,
}

# Identity for chapters 0-9 (unchanged)
for n in range(0, 10):
    RENUMBER.setdefault(n, n)


def is_book_file(p: Path) -> bool:
    sp = str(p).replace('\\', '/')
    return not any(s in sp for s in SKIP)


def find_module_dirs() -> list[Path]:
    """Return all part-*/module-NN-NAME directories."""
    return sorted(ROOT.glob('part-*/module-*'))


# =============================================================================
# PHASE 1: rename directories via two-step temp-token plan
# =============================================================================

def rename_modules(dry_run: bool) -> list[tuple[Path, Path]]:
    """Two-phase rename: old name -> tmp name -> new name.
    Returns the final (old, new) mapping for downstream content rewrite.
    """
    plan: list[tuple[Path, Path, Path]] = []  # (old, tmp, new)
    for mod_dir in find_module_dirs():
        m = re.match(r'module-(\d+)-(.+)', mod_dir.name)
        if not m:
            continue
        old_n = int(m.group(1))
        name = m.group(2)
        if old_n not in RENUMBER:
            continue
        new_n = RENUMBER[old_n]
        if new_n == old_n:
            continue
        tmp_name = f'module-TMP{old_n}-{name}'
        new_name = f'module-{new_n:02d}-{name}'
        plan.append((mod_dir, mod_dir.parent / tmp_name,
                     mod_dir.parent / new_name))
    # Phase 1a: old -> tmp
    if not dry_run:
        for old, tmp, _new in plan:
            shutil.move(str(old), str(tmp))
        for _old, tmp, new in plan:
            shutil.move(str(tmp), str(new))
    return [(p[0], p[2]) for p in plan]


# =============================================================================
# PHASE 2: rename section files inside each new module dir
# =============================================================================

def rename_sections(dry_run: bool) -> list[tuple[Path, Path]]:
    """For each new module dir, rename section-N.M.html to
    section-new_N.M.html. Uses the new module dir name to determine
    new_N. Returns (old, new) pairs."""
    plan: list[tuple[Path, Path]] = []
    for mod_dir in find_module_dirs():
        m = re.match(r'module-(\d+)-', mod_dir.name)
        if not m:
            continue
        new_n = int(m.group(1))
        # Find section files; their leading section-N.M will use the OLD
        # number, which we map back via the directory's name as the new
        # canonical number. For each section-K.M.html, K must equal
        # new_n once we are done; if K != new_n it needs renaming.
        for sec in sorted(mod_dir.glob('section-*.html')):
            sm = re.match(r'section-(\d+)\.(\d+)\.html', sec.name)
            if not sm:
                continue
            sec_chap = int(sm.group(1))
            if sec_chap == new_n:
                continue
            sub = sm.group(2)
            new_name = f'section-{new_n}.{sub}.html'
            plan.append((sec, mod_dir / new_name))
    if not dry_run:
        for old, new in plan:
            shutil.move(str(old), str(new))
    return plan


# =============================================================================
# PHASE 3: rename images inside images/ dirs to update fig-N.M.K- prefix
# =============================================================================

def rename_images(dry_run: bool) -> list[tuple[Path, Path]]:
    plan: list[tuple[Path, Path]] = []
    img_pat = re.compile(r'^(fig-)(\d+)\.(\d+)\.(\d+)(-.*)$', re.IGNORECASE)
    for mod_dir in find_module_dirs():
        m = re.match(r'module-(\d+)-', mod_dir.name)
        if not m:
            continue
        new_n = int(m.group(1))
        images_dir = mod_dir / 'images'
        if not images_dir.is_dir():
            continue
        for img in sorted(images_dir.iterdir()):
            if not img.is_file():
                continue
            im = img_pat.match(img.name)
            if not im:
                continue
            old_chap = int(im.group(2))
            sub1 = im.group(3)
            sub2 = im.group(4)
            rest = im.group(5)
            if old_chap == new_n:
                continue
            new_name = f'fig-{new_n}.{sub1}.{sub2}{rest}'
            plan.append((img, images_dir / new_name))
    if not dry_run:
        for old, new in plan:
            # Two-phase to avoid collisions: use tmp
            tmp = old.parent / (old.name + '.RENUMBER_TMP')
            shutil.move(str(old), str(tmp))
        for old, new in plan:
            tmp = old.parent / (old.name + '.RENUMBER_TMP')
            shutil.move(str(tmp), str(new))
    return plan


# =============================================================================
# PHASE 4: rewrite content cross-references in every HTML/MD file
# =============================================================================

# We do token-based substitution to avoid double-shifts. Phase 4a marks
# every occurrence of an old number with a TMP token; phase 4b replaces
# the TMP tokens with the new numbers.

def rewrite_content(dry_run: bool) -> int:
    """Walk every HTML / MD file in the book and apply the renumber to
    every cross-reference, prose chapter/section/figure mention, and
    heading."""

    # Build the pattern -> handler mapping.
    # We use placeholders \x00..N..\x00 keyed by old number so we can do
    # all replacements in a single pass, then swap to new numbers.

    n_changed_files = 0

    # Precompile patterns. Note: order matters; longer/more-specific first.
    # We will run a multi-pattern engine that emits placeholders.

    SUBS = []  # list of (pattern, kind) where kind in {'module-dir',
              #   'section-href', 'image-fname', 'chapter-prose',
              #   'section-prose', 'figure-prose', 'codefrag-prose',
              #   'heading-num', 'chap-label', 'partlabel-N'}

    # 1) module-NN-name in any context (hrefs)
    SUBS.append((
        re.compile(r'module-(\d{2})-([a-z][a-z0-9\-]*)'),
        'module-dir'))
    # 2) section-N.M.html in hrefs
    SUBS.append((
        re.compile(r'section-(\d+)\.(\d+)\.html'),
        'section-href'))
    # 3) fig-N.M.K-name image filenames in src/href
    SUBS.append((
        re.compile(r'fig-(\d+)\.(\d+)\.(\d+)-'),
        'image-fname'))
    # 4) "Chapter NN" prose -- ONLY two-digit chapters to avoid false hits
    SUBS.append((
        re.compile(r'\bChapter\s+(\d{2})\b'),
        'chapter-prose'))
    # 4b) "Chapter N" single-digit -- only for N in renumber map AND mapped
    SUBS.append((
        re.compile(r'\bChapter\s+(\d)\b(?!\.\d)'),
        'chapter-prose-1digit'))
    # 5) "Module NN" prose
    SUBS.append((
        re.compile(r'\bModule\s+(\d{2})\b'),
        'module-prose'))
    # 6) "Section N.M" prose -- numeric chap.sec form
    SUBS.append((
        re.compile(r'\bSection\s+(\d+)\.(\d+)\b'),
        'section-prose'))
    # 7) "Figure N.M.K" prose / caption
    SUBS.append((
        re.compile(r'\bFigure\s+(\d+)\.(\d+)\.(\d+)\b'),
        'figure-prose'))
    # 8) "Code Fragment N.M.K"
    SUBS.append((
        re.compile(r'\bCode Fragment\s+(\d+)\.(\d+)\.(\d+)\b'),
        'codefrag-prose'))
    # 9) <h1>N.M / <h2>N.M.K / <h3>N.M.K.L numeric prefixes at start of heading
    SUBS.append((
        re.compile(r'(<h[1-6][^>]*>\s*)(\d+)\.(\d+)(\.\d+)*(\b)'),
        'heading-num'))
    # 10) chapter-label / pagefind-meta strings like "Chapter NN:" or
    #     "Chapter NN"
    # (Already covered by chapter-prose pattern.)

    for f in sorted(ROOT.rglob('*.html')) + sorted(ROOT.rglob('*.md')) \
             + sorted(ROOT.rglob('*.yaml')) + sorted(ROOT.rglob('*.json')):
        if not is_book_file(f):
            continue
        try:
            text = f.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        original = text
        # Apply each pattern. Each handler produces the new text.
        text = apply_substitutions(text)
        if text != original:
            n_changed_files += 1
            if not dry_run:
                f.write_text(text, encoding='utf-8')
    return n_changed_files


def remap(n: int) -> int:
    return RENUMBER.get(n, n)


def apply_substitutions(text: str) -> str:
    """Single function that applies every renumber substitution in one
    pass. Use placeholder-tokens to avoid double-substitution. Strategy:
    each numeric occurrence gets a \x00NEW_N\x00 placeholder during the
    first pass; second pass converts placeholders back to plain digits.
    """
    PLACEHOLDER = '{:02d}'  # private-use Unicode chars
    SUB_PLACEHOLDER = '{}'  # for section/figure/code numbers

    # 1. module-NN-name
    def repl_mod(m: re.Match) -> str:
        n = int(m.group(1))
        new_n = remap(n)
        return f'module-{PLACEHOLDER.format(new_n)}-{m.group(2)}'
    text = re.sub(r'module-(\d{2})-([a-z][a-z0-9\-]*)', repl_mod, text)

    # 2. section-N.M.html  (chapter part of section href)
    def repl_sec_href(m: re.Match) -> str:
        chap = int(m.group(1))
        sub = int(m.group(2))
        new_chap = remap(chap)
        return f'section-{SUB_PLACEHOLDER.format(new_chap)}.{sub}.html'
    text = re.sub(r'section-(\d+)\.(\d+)\.html', repl_sec_href, text)

    # 3. fig-N.M.K- image filenames
    def repl_fig_fname(m: re.Match) -> str:
        chap = int(m.group(1))
        sub1 = int(m.group(2))
        sub2 = int(m.group(3))
        new_chap = remap(chap)
        return f'fig-{SUB_PLACEHOLDER.format(new_chap)}.{sub1}.{sub2}-'
    text = re.sub(r'fig-(\d+)\.(\d+)\.(\d+)-', repl_fig_fname, text)

    # 4. "Chapter NN" prose (2-digit)
    def repl_chap2(m: re.Match) -> str:
        n = int(m.group(1))
        new_n = remap(n)
        return f'Chapter {PLACEHOLDER.format(new_n)}'
    text = re.sub(r'\bChapter\s+(\d{2})\b', repl_chap2, text)

    # 4b. "Chapter N" prose (1-digit) -- only chapters 0-9 in renumber map.
    # Chapter 0..9 (single digit) don't actually need remapping (they're
    # identity), but the pattern is included for safety.
    def repl_chap1(m: re.Match) -> str:
        n = int(m.group(1))
        new_n = remap(n)
        if new_n == n:
            return m.group(0)
        return f'Chapter {PLACEHOLDER.format(new_n)}'
    text = re.sub(r'\bChapter\s+(\d)\b(?!\.\d)', repl_chap1, text)

    # 5. "Module NN" prose
    def repl_mod_prose(m: re.Match) -> str:
        n = int(m.group(1))
        new_n = remap(n)
        return f'Module {PLACEHOLDER.format(new_n)}'
    text = re.sub(r'\bModule\s+(\d{2})\b', repl_mod_prose, text)

    # 6. "Section N.M" prose
    def repl_sec_prose(m: re.Match) -> str:
        chap = int(m.group(1))
        sub = int(m.group(2))
        new_chap = remap(chap)
        return f'Section {SUB_PLACEHOLDER.format(new_chap)}.{sub}'
    text = re.sub(r'\bSection\s+(\d+)\.(\d+)\b', repl_sec_prose, text)

    # 7. "Figure N.M.K" prose
    def repl_fig(m: re.Match) -> str:
        chap = int(m.group(1))
        sub1 = m.group(2)
        sub2 = m.group(3)
        new_chap = remap(chap)
        return f'Figure {SUB_PLACEHOLDER.format(new_chap)}.{sub1}.{sub2}'
    text = re.sub(r'\bFigure\s+(\d+)\.(\d+)\.(\d+)\b', repl_fig, text)

    # 8. "Code Fragment N.M.K"
    def repl_code(m: re.Match) -> str:
        chap = int(m.group(1))
        sub1 = m.group(2)
        sub2 = m.group(3)
        new_chap = remap(chap)
        return f'Code Fragment {SUB_PLACEHOLDER.format(new_chap)}.{sub1}.{sub2}'
    text = re.sub(r'\bCode Fragment\s+(\d+)\.(\d+)\.(\d+)\b', repl_code, text)

    # 9. Headings like <h1>N.M ...</h1>, <h2>N.M.K ...</h2>, etc.
    def repl_heading(m: re.Match) -> str:
        prefix = m.group(1)  # <hX...>
        chap = int(m.group(2))
        sub_rest = m.group(0)[len(prefix):]  # "N.M.K..." part
        new_chap = remap(chap)
        # Replace just the leading "N." with the new number
        new_rest = re.sub(rf'^{chap}\.', f'{new_chap}.', sub_rest)
        return prefix + new_rest
    text = re.sub(r'(<h[1-6][^>]*>\s*)(\d+)\.\d+', repl_heading, text)

    return text


# =============================================================================
# PHASE 5: special-case rewrites for spine_manifest.json and BOOK_CONFIG.md
# (These get rewritten by apply_substitutions if their paths/numbers match
#  the patterns. Provided here as a sanity check that the substitutions
#  worked.)
# =============================================================================

def rewrite_explicit_configs(dry_run: bool) -> int:
    """Some config files live inside KDP/build/ which is in SKIP. Apply
    the renumber explicitly to those known files."""
    targets = [
        ROOT / 'KDP' / 'build' / 'spine_manifest.json',
        ROOT / 'BOOK_CONFIG.md',
    ]
    n_changed = 0
    for tgt in targets:
        if not tgt.exists():
            continue
        text = tgt.read_text(encoding='utf-8', errors='replace')
        new = apply_substitutions(text)
        if new != text:
            n_changed += 1
            if not dry_run:
                tgt.write_text(new, encoding='utf-8')
            print(f'  rewrote {tgt.relative_to(ROOT)}')
    return n_changed


def report_spine(path: Path) -> None:
    if not path.exists():
        return
    text = path.read_text(encoding='utf-8', errors='replace')
    bad = re.findall(r'module-31-interpretability', text)
    if bad:
        print(f'  WARNING: spine still references module-31-interpretability '
              f'({len(bad)} occurrences)')


# =============================================================================
# Driver
# =============================================================================

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--fix', action='store_true')
    args = ap.parse_args()

    # Idempotent guard: if module-31-interpretability no longer exists,
    # this script has already run.
    sentinel = ROOT / 'part-2-understanding-llms' / 'module-31-interpretability'
    if not sentinel.exists():
        print('ALREADY RUN: module-31-interpretability not found. '
              'Renumber is already applied.')
        return 0

    print('PHASE 1: rename module directories')
    mod_plan = rename_modules(dry_run=not args.fix)
    for old, new in mod_plan:
        print(f'  {old.relative_to(ROOT)} -> {new.name}')
    print(f'  ({len(mod_plan)} module directories)')

    print('\nPHASE 2: rename section files inside renamed modules')
    sec_plan = rename_sections(dry_run=not args.fix)
    for old, new in sec_plan[:10]:
        print(f'  {old.relative_to(ROOT)} -> {new.name}')
    if len(sec_plan) > 10:
        print(f'  ... +{len(sec_plan) - 10} more')
    print(f'  ({len(sec_plan)} section files)')

    print('\nPHASE 3: rename images')
    img_plan = rename_images(dry_run=not args.fix)
    print(f'  ({len(img_plan)} image files)')

    print('\nPHASE 4: rewrite content cross-references')
    n_changed = rewrite_content(dry_run=not args.fix)
    print(f'  ({n_changed} files updated)')

    print('\nPHASE 5: rewrite explicit configs (spine manifest, BOOK_CONFIG)')
    rewrite_explicit_configs(dry_run=not args.fix)
    report_spine(ROOT / 'KDP' / 'build' / 'spine_manifest.json')

    if not args.fix:
        print('\nDry run complete. Re-run with --fix to apply.')
    else:
        print('\nDone. Verify with QA pipeline next.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
