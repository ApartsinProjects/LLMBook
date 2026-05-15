"""v15: apply appendix redesign per APPENDIX_REDESIGN_PLAN.md.

Renumber appendices to close gaps:
  R (Experiment Tracking)       -> M
  S (Inference Serving)         -> N
  T (Distributed ML)            -> O
  U (Docker Containers)         -> P
  V (Tooling Ecosystem)         -> Q   (keep as 3-section appendix; demotion deferred)
  AD (Master Reference Tables)  -> R
  AE (Production Patterns)      -> S
  AF (Pedagogy Kit)             -> T
  AG (Problem-Solution Key)     -> U
  AI (2026 Freshness Index)     -> V

Move to front-matter:
  AJ (Reading Pathways)         -> front-matter/fm-reading-pathways.html
  AK (Course Syllabi)           -> front-matter/fm-course-syllabi.html

Updates:
  - Filesystem moves (shutil.move directories or files)
  - Per-file content updates:
    - Header label "Appendix R" -> "Appendix M"
    - Section IDs "R.1" -> "M.1" (in h1, internal anchors, link text)
    - Subsection numbers in headings (e.g., "R.2.3" -> "M.2.3")
    - <title> tags
    - description meta
  - Book-wide href updates:
    - href="appendix-r-..." -> href="appendix-m-..."
    - href="appendix-ad-..." -> href="appendix-r-..."  (etc.)
  - toc.html short + detailed views
  - appendices/index.html chapter cards
  - For AJ/AK: paths now go up one level (from appendices/appendix-aj-...
    to front-matter/fm-...)
"""
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
import os
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
SKIP = ['node_modules', '.git', 'KDP/output', 'KDP/build', 'KDP/html2pub',
        'pagefind', 'temp_epub', 'source_fix_backups']


def skip(p):
    sp = str(p).replace('\\', '/')
    return any(s in sp for s in SKIP)


# Renumbering map: (old_dirname, new_dirname, old_letter, new_letter,
#                    section_letter_old, section_letter_new)
RENUMBER = [
    ('appendix-r-experiment-tracking',     'appendix-m-experiment-tracking',     'R',  'M'),
    ('appendix-s-inference-serving',       'appendix-n-inference-serving',       'S',  'N'),
    ('appendix-t-distributed-ml',          'appendix-o-distributed-ml',          'T',  'O'),
    ('appendix-u-docker-containers',       'appendix-p-docker-containers',       'U',  'P'),
    ('appendix-v-tooling-ecosystem',       'appendix-q-tooling-ecosystem',       'V',  'Q'),
    ('appendix-ad-master-reference-tables', 'appendix-r-master-reference-tables', 'AD', 'R'),
    ('appendix-ae-production-patterns',    'appendix-s-production-patterns',     'AE', 'S'),
    ('appendix-af-pedagogy-kit',           'appendix-t-pedagogy-kit',            'AF', 'T'),
    ('appendix-ag-problem-solution-key',   'appendix-u-problem-solution-key',    'AG', 'U'),
    ('appendix-ai-freshness-2026',         'appendix-v-freshness-2026',          'AI', 'V'),
]

# Moves to front-matter
MOVES = [
    ('appendices/appendix-aj-reading-pathways/index.html',
     'front-matter/fm-reading-pathways.html', 'AJ', 'Reading Pathways'),
    ('appendices/appendix-ak-course-syllabi/index.html',
     'front-matter/fm-course-syllabi.html', 'AK', 'Course Syllabi'),
]


def step(label):
    print(f'\n>>> {label}')


def rename_dirs(dry):
    """Rename appendix directories per RENUMBER table.

    IMPORTANT: must be done in 2-phase to avoid collisions when
    target letter collides with another rename source.
    """
    base = ROOT / 'appendices'

    # Phase 1: rename old→temp (so target letters can't collide)
    for old_dir, new_dir, _, _ in RENUMBER:
        src = base / old_dir
        tmp = base / (old_dir + '.__rename_tmp')
        if src.exists():
            if not dry:
                src.rename(tmp)
            print(f'  phase1: {old_dir} -> .__rename_tmp')

    # Phase 2: rename temp→new
    for old_dir, new_dir, _, _ in RENUMBER:
        tmp = base / (old_dir + '.__rename_tmp')
        dst = base / new_dir
        if tmp.exists():
            if not dry:
                tmp.rename(dst)
            print(f'  phase2: .__rename_tmp -> {new_dir}')


def rename_section_files(dry):
    """Rename section-X.N.html -> section-Y.N.html inside renumbered dirs."""
    base = ROOT / 'appendices'
    for _old_dir, new_dir, old_letter, new_letter in RENUMBER:
        d = base / new_dir
        if not d.exists():
            continue
        old_pat = old_letter.lower()
        new_pat = new_letter.lower()
        for sec in list(d.glob(f'section-{old_pat}.*.html')):
            new_name = sec.name.replace(f'section-{old_pat}.', f'section-{new_pat}.')
            new_path = sec.parent / new_name
            if not dry:
                sec.rename(new_path)
            print(f'  rename: {sec.name} -> {new_name}')


def update_internal_markup(dry):
    """For each renumbered file, update internal text references:
        - 'Appendix R' -> 'Appendix M'
        - Section heading "R.2 ..." -> "M.2 ..."
        - Subsection IDs like #r-2 -> #m-2
        - <title>, meta description
    """
    base = ROOT / 'appendices'
    for _old_dir, new_dir, old_letter, new_letter in RENUMBER:
        d = base / new_dir
        if not d.exists():
            continue
        for f in d.glob('*.html'):
            t = f.read_text(encoding='utf-8')
            orig = t

            # 1. "Appendix R" -> "Appendix M" (whole-word, preserve case)
            t = re.sub(rf'\bAppendix\s+{re.escape(old_letter)}\b',
                       f'Appendix {new_letter}', t)
            t = re.sub(rf'\bappendix\s+{re.escape(old_letter)}\b',
                       f'appendix {new_letter}', t)

            # 2. Section labels in headings: "R.2 Title" -> "M.2 Title"
            # Match: optional non-letter boundary + Letter + dot + digit
            t = re.sub(
                rf'(<h[234][^>]*>(?:<[^>]+>)?){re.escape(old_letter)}\.(\d+)',
                rf'\g<1>{new_letter}.\2',
                t
            )

            # 3. Internal anchors and IDs: r-2-3 patterns
            old_id = old_letter.lower()
            new_id = new_letter.lower()
            t = re.sub(
                rf'(id|href)="#{old_id}-(\d+)',
                lambda m: f'{m.group(1)}="#{new_id}-{m.group(2)}',
                t
            )
            t = re.sub(rf'id="{old_id}-(\d+)', lambda m: f'id="{new_id}-{m.group(1)}', t)

            # 4. Section.X.Y plain-text refs (cross-section within same appendix)
            t = re.sub(rf'\b{re.escape(old_letter)}\.(\d+)\b',
                       lambda m: f'{new_letter}.{m.group(1)}', t)

            # 5. section-X.N.html -> section-Y.N.html in href attributes
            t = re.sub(
                rf'(href="[^"]*section-){old_id}\.(\d+)\.html',
                rf'\g<1>{new_id}.\2.html',
                t
            )

            # 6. Path to own directory: appendix-r-experiment-tracking
            # (when self-referenced via long form)
            for o, n, _, _ in RENUMBER:
                t = t.replace(o, n)

            if t != orig and not dry:
                f.write_text(t, encoding='utf-8')

        print(f'  updated internal markup: {new_dir}/')


def update_book_wide_hrefs(dry):
    """Update all hrefs across the book to point to new appendix paths.

    Done in 2-phase like dir rename to avoid collision:
    1. old paths -> temp marker
    2. temp marker -> new paths
    """
    # Build the mapping
    href_map = {}
    for o, n, _, _ in RENUMBER:
        href_map[o] = n

    n_files_modified = 0
    n_replacements = 0
    for p in ROOT.rglob('*.html'):
        if skip(p):
            continue
        try:
            t = p.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue
        orig = t
        # Phase 1: old -> __tmp__<idx>
        for i, (old, new) in enumerate(href_map.items()):
            t = t.replace(old, f'__TMP_APX_{i}__')
        # Phase 2: __tmp__<idx> -> new
        for i, (old, new) in enumerate(href_map.items()):
            t = t.replace(f'__TMP_APX_{i}__', new)
        # Also fix section-X.N.html across hrefs (since dirs renamed, paths inside change too)
        # Already covered by the directory rename portion of paths.
        # But section file letters change inside hrefs too:
        for _o, _n, ol, nl in RENUMBER:
            ol_lower = ol.lower()
            nl_lower = nl.lower()
            # appendix-X/section-x.N.html -> appendix-Y/section-y.N.html
            # The dir-portion is already mapped; just need section filename
            # Strategy: find href="...appendix-NEW/section-OLDLETTER.N.html"
            # But the OLD letter is in the path already because we just renamed.
            # Simpler: look for /section-OLDLETTER.<digit>.html inside the
            # context of the new dir.
            t = re.sub(
                rf'(appendix-{nl_lower}[^/]*?/section-){ol_lower}\.(\d+)\.html',
                rf'\g<1>{nl_lower}.\2.html',
                t
            )
        if t != orig:
            if not dry:
                p.write_text(t, encoding='utf-8')
            n_files_modified += 1
            # Count replacements (approximation)
            for o, n in href_map.items():
                n_replacements += orig.count(o)

    print(f'  href updates: {n_files_modified} files, {n_replacements} occurrences')


def move_aj_ak_to_frontmatter(dry):
    """Move appendix-aj and appendix-ak to front-matter."""
    for src_rel, dst_rel, old_letter, label in MOVES:
        src = ROOT / src_rel
        dst = ROOT / dst_rel
        if not src.exists():
            print(f'  SKIP: {src_rel} (not found)')
            continue
        if dst.exists():
            print(f'  SKIP: {dst_rel} already exists')
            continue
        # Read content, update paths (front-matter is 1 level deep, appendices
        # are 2 levels deep), then write
        t = src.read_text(encoding='utf-8')
        # Adjust relative paths: ../../X/ -> ../X/ (one fewer level up)
        # because front-matter is at depth 1 vs appendices/X/ at depth 2
        t = re.sub(r'\.\./\.\./(?!\.)', '../', t)
        # Adjust "Appendix AJ"/"Appendix AK" labels in headers
        t = re.sub(rf'\bAppendix\s+{old_letter}\b',
                   f'Front Matter: {label}', t)
        if not dry:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(t, encoding='utf-8')
            # Remove the source dir (whole directory since it's a single-page)
            shutil.rmtree(src.parent)
        print(f'  moved: {src_rel} -> {dst_rel}')


def update_aj_ak_inbound_refs(dry):
    """Update all hrefs in the book that point to appendix-aj/ak/."""
    aj_old_dir = 'appendices/appendix-aj-reading-pathways'
    ak_old_dir = 'appendices/appendix-ak-course-syllabi'
    aj_new = 'front-matter/fm-reading-pathways.html'
    ak_new = 'front-matter/fm-course-syllabi.html'

    n_files = 0
    for p in ROOT.rglob('*.html'):
        if skip(p):
            continue
        try:
            t = p.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue
        orig = t
        # Hrefs to old appendix-aj/ak with /index.html -> new front-matter path
        # Determine depth so we can write correct relative path
        rel_to_root = p.relative_to(ROOT)
        depth = len(rel_to_root.parts) - 1  # how many ../ to root
        prefix = '../' * depth

        # Replace the old path patterns
        t = re.sub(
            rf'(href=")(?:\.\./)*{re.escape(aj_old_dir)}/index\.html',
            rf'\1{prefix}{aj_new}',
            t
        )
        t = re.sub(
            rf'(href=")(?:\.\./)*{re.escape(ak_old_dir)}/index\.html',
            rf'\1{prefix}{ak_new}',
            t
        )
        # Also replace bare "Appendix AJ" / "Appendix AK" mentions in prose
        # — but keep the link text since these become front-matter entries
        # rather than appendices
        if t != orig:
            if not dry:
                p.write_text(t, encoding='utf-8')
            n_files += 1
    print(f'  AJ/AK inbound refs updated: {n_files} files')


def update_toc_html(dry):
    """Rewrite toc.html appendix entries to use new letters + remove AJ/AK
    (they're in front-matter now)."""
    p = ROOT / 'toc.html'
    t = p.read_text(encoding='utf-8')

    # 1. Remove AJ and AK rows entirely (they're moving to front-matter)
    for letter in ('AJ', 'AK'):
        t = re.sub(
            rf'<div class="dense-chapter"><span class="dense-ch-num">App\s+{letter}</span>[^<]*<a[^>]*>[^<]*</a></div>\s*',
            '', t
        )
        t = re.sub(
            rf'<div class="dense-chapter"><span class="dense-ch-num">{letter}</span>[^<]*<a[^>]*>[^<]*</a></div>\s*',
            '', t
        )

    # 2. Insert front-matter rows for Reading Pathways and Course Syllabi
    # Find the FM block and append after copyright row (last FM entry).
    # Actually a cleaner approach: insert just before the Part I block.
    fm_entries = (
        '<div class="dense-chapter"><span class="dense-ch-num">FM.8</span> '
        '<a href="front-matter/fm-reading-pathways.html">Reading Pathways</a></div>\n'
        '<div class="dense-chapter"><span class="dense-ch-num">FM.9</span> '
        '<a href="front-matter/fm-course-syllabi.html">Course Syllabi</a></div>\n'
    )
    # Find ToC short view: insert after FM.7 (last FM entry)
    # Detail view also has FM.7. Insert in both.
    t = re.sub(
        r'(<div class="dense-chapter"><span class="dense-ch-num">FM\.7</span>[^<]*<a[^>]*>[^<]*</a></div>\s*)',
        rf'\1{fm_entries}',
        t
    )

    # 3. Renumber appendix labels: AD->R, AE->S, ..., AI->V; R->M, S->N, ..., V->Q
    # Use 2-phase to avoid collision
    label_map = {}
    for _o, _n, old_letter, new_letter in RENUMBER:
        label_map[old_letter] = new_letter

    # Phase 1: temp markers
    for i, (old, new) in enumerate(label_map.items()):
        for prefix in ['App ', '']:
            t = re.sub(
                rf'(<span class="dense-ch-num">){prefix}{re.escape(old)}(</span>)',
                rf'\1{prefix}__TMP_{i}__\2',
                t
            )
    # Phase 2: new letters
    for i, (old, new) in enumerate(label_map.items()):
        t = t.replace(f'__TMP_{i}__', new)

    if not dry:
        p.write_text(t, encoding='utf-8')
    print('  toc.html: updated appendix labels + added FM.8/FM.9 entries')


def main():
    dry = '--apply' not in sys.argv
    print('DRY RUN.' if dry else 'APPLY mode.')

    step('Phase 1: rename appendix directories (2-phase to avoid collision)')
    rename_dirs(dry)

    step('Phase 2: rename section-X.N.html files inside renumbered dirs')
    rename_section_files(dry)

    step('Phase 3: update internal markup in renumbered files')
    update_internal_markup(dry)

    step('Phase 4: update book-wide hrefs (2-phase)')
    update_book_wide_hrefs(dry)

    step('Phase 5: move AJ/AK to front-matter')
    move_aj_ak_to_frontmatter(dry)

    step('Phase 6: update AJ/AK inbound refs')
    update_aj_ak_inbound_refs(dry)

    step('Phase 7: update toc.html')
    update_toc_html(dry)

    print('\nDONE.')


if __name__ == '__main__':
    main()
