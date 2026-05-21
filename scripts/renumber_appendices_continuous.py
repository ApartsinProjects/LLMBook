"""Renumber appendices for continuous labels after C-N and O deletions.

Current:  A, B, P, Q, R, S, T  (gap B -> P)
Target:   A, B, C, D, E, F, G  (continuous)

Renames:
  appendix-p-course-syllabi        ->  appendix-c-course-syllabi        (Appendix P -> C)
  appendix-q-reading-pathways      ->  appendix-d-reading-pathways      (Appendix Q -> D)
  appendix-r-intermediate-projects ->  appendix-e-intermediate-projects (Appendix R -> E)
  appendix-s-capstone-project      ->  appendix-f-capstone-project      (Appendix S -> F)
  appendix-t-war-stories           ->  appendix-g-war-stories           (Appendix T -> G)

Per-file rewrites inside each renamed appendix:
  - Filenames: section-{old_letter}.X.html -> section-{new_letter}.X.html
  - Title, meta description: "Appendix P:" -> "Appendix C:", "Section P.X" -> "Section C.X"
  - page-current, page-breadcrumb spans
  - Anchor IDs: id="p-X-Y-..." -> id="c-X-Y-..."  (id and href anchors)
  - Body text mentions: "Appendix P" -> "Appendix C", "P.1" -> "C.1", etc.

Cross-references everywhere else in the book:
  - href="...appendices/appendix-{old}-.../..." -> href="...appendices/appendix-{new}-.../..."
  - Body text references "Appendix P" -> "Appendix C" (in href text)
"""
from __future__ import annotations
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# (old_letter, old_slug, new_letter, new_slug)
RENAMES = [
    ('p', 'appendix-p-course-syllabi',        'c', 'appendix-c-course-syllabi'),
    ('q', 'appendix-q-reading-pathways',      'd', 'appendix-d-reading-pathways'),
    ('r', 'appendix-r-intermediate-projects', 'e', 'appendix-e-intermediate-projects'),
    ('s', 'appendix-s-capstone-project',      'f', 'appendix-f-capstone-project'),
    ('t', 'appendix-t-war-stories',           'g', 'appendix-g-war-stories'),
]

SKIP_DIRS = {"node_modules", ".git", "KDP", "build", "temp_ebook", "temp_epub",
             "source_fix_backups", "pagefind", "templates", ".claude",
             ".book-update", "vendor", "docs"}


def git_mv(src, dst):
    if not src.exists() or dst.exists():
        return False
    r = subprocess.run(['git', 'mv', str(src), str(dst)],
                       cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        print(f'  ERR git mv {src} -> {dst}: {r.stderr.strip()}')
        return False
    return True


def step1_rename_directories():
    """Use .__tmp__ intermediate to avoid collisions (none expected here,
    but consistent with other renumbering scripts)."""
    print('--- Step 1a: appendix dir -> .__tmp__ ---')
    n1 = 0
    for old_letter, old_slug, new_letter, new_slug in RENAMES:
        src = ROOT / 'appendices' / old_slug
        tmp = ROOT / 'appendices' / (new_slug + '.__tmp__')
        if git_mv(src, tmp):
            print(f'  {old_slug} -> .__tmp__')
            n1 += 1

    print('--- Step 1b: .__tmp__ -> final slug ---')
    n2 = 0
    for old_letter, old_slug, new_letter, new_slug in RENAMES:
        tmp = ROOT / 'appendices' / (new_slug + '.__tmp__')
        dst = ROOT / 'appendices' / new_slug
        if git_mv(tmp, dst):
            print(f'  {new_slug}.__tmp__ -> {new_slug}')
            n2 += 1
    return n2


def step2_rename_section_files():
    """Inside each renamed appendix dir, rename section-{old_letter}.X.html ->
    section-{new_letter}.X.html. Letters are unique so no .__tmp__ shuffle needed."""
    print('--- Step 2: section-X.html -> section-Y.html ---')
    n = 0
    for old_letter, old_slug, new_letter, new_slug in RENAMES:
        ap_dir = ROOT / 'appendices' / new_slug
        if not ap_dir.exists():
            continue
        for f in list(ap_dir.glob(f'section-{old_letter}.*.html')):
            m = re.match(rf'^section-{old_letter}\.(\d+)\.html$', f.name)
            if not m: continue
            dst = f.parent / f'section-{new_letter}.{m.group(1)}.html'
            if git_mv(f, dst):
                n += 1
        print(f'  {new_slug}: renamed sections section-{old_letter}.* -> section-{new_letter}.*')
    print(f'  Total section files renamed: {n}')


def step3_rewrite_inside_files():
    """For every file in a renamed appendix dir, rewrite letter-bound metadata."""
    print('--- Step 3: rewrite in-file content inside renamed appendices ---')
    n_files = 0
    for old_letter, old_slug, new_letter, new_slug in RENAMES:
        ap_dir = ROOT / 'appendices' / new_slug
        if not ap_dir.exists():
            continue
        upper_old = old_letter.upper()
        upper_new = new_letter.upper()
        for f in list(ap_dir.glob('*.html')):
            text = f.read_text(encoding='utf-8')
            orig = text
            # Title/meta/breadcrumb: "Appendix P:" -> "Appendix C:"
            text = re.sub(
                rf'\bAppendix {upper_old}\b',
                f'Appendix {upper_new}',
                text
            )
            # page-current / breadcrumb: "Section P.X" -> "Section C.X"
            text = re.sub(
                rf'\bSection {upper_old}\.(\d+)\b',
                rf'Section {upper_new}.\1',
                text
            )
            # Anchor IDs: id="p-X-Y-..." -> id="c-X-Y-..."
            text = re.sub(
                rf'\bid="{old_letter}-(\d+)-',
                rf'id="{new_letter}-\1-',
                text
            )
            text = re.sub(
                rf'\bhref="#{old_letter}-(\d+)-',
                rf'href="#{new_letter}-\1-',
                text
            )
            # Same-dir intra-file refs: href="section-{old_letter}.X.html"
            text = re.sub(
                rf'(href="(?:section-)?){old_letter}\.(\d+)(\.html)',
                rf'\g<1>{new_letter}.\2\3',
                text
            )
            text = re.sub(
                rf'(href="section-){old_letter}\.(\d+)(\.html)',
                rf'\g<1>{new_letter}.\2\3',
                text
            )
            # Body refs like "P.1" -> "C.1" only inside paragraphs (carefully, avoid letter-only matches)
            # Use word boundary on numeric and require uppercase letter dot digit
            text = re.sub(
                rf'\b{upper_old}\.(\d+)\b',
                rf'{upper_new}.\1',
                text
            )
            # aria-labels: aria-label="Appendix P"
            text = re.sub(
                rf'(aria-label="Appendix ){upper_old}(")',
                rf'\1{upper_new}\2',
                text
            )
            # Body text + chapter card content "Appendix P" remained handled above by \bAppendix X\b
            if text != orig:
                f.write_text(text, encoding='utf-8')
                n_files += 1
    print(f'  Updated in-file content for {n_files} files')


def step4_rewrite_external_refs():
    """Walk every HTML in the book. Rewrite all hrefs and body text that
    references the old appendix slugs/letters."""
    print('--- Step 4: rewrite external refs across the book ---')

    # Build dir-slug substitutions
    dir_sub = [(old, new) for _, old, _, new in RENAMES]
    # Letter substitutions in text mentioning "Appendix P"
    letter_sub = [(old.upper(), new.upper()) for old, _, new, _ in RENAMES]

    # First do dir-slug replacements with .__tmp__ to avoid the
    # 'overlap' issue (e.g. if a new slug equals an old slug). Here no
    # overlap exists (P/Q/R/S/T <-> C/D/E/F/G) so we can do straight subs.

    n_files = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP_DIRS: continue
        # skip the renamed appendix dirs themselves (handled in step 3)
        if p.parts[-2] in {n for _, _, _, n in RENAMES}: continue
        text = p.read_text(encoding='utf-8')
        orig = text
        # Replace dir slugs in hrefs
        for old, new in dir_sub:
            # in hrefs
            text = text.replace(f'/{old}/', f'/{new}/')
            text = text.replace(f'"{old}/', f'"{new}/')
            text = text.replace(f"'{old}/", f"'{new}/")
        # Replace body-text "Appendix P" -> "Appendix C", etc.
        for upper_old, upper_new in letter_sub:
            text = re.sub(rf'\bAppendix {upper_old}\b', f'Appendix {upper_new}',
                          text)
            # aria-label
            text = re.sub(rf'aria-label="Appendix {upper_old}"',
                          f'aria-label="Appendix {upper_new}"',
                          text)
            # Section X.Y refs that point INTO renamed appendices.
            # Only rewrite if the surrounding href targets the new appendix.
            # Safer: handled via specific href patterns above.

        # Update toc.html chapter-num span content if pointing at appendix slug
        # Already handled by letter_sub for aria-label

        if text != orig:
            p.write_text(text, encoding='utf-8')
            n_files += 1
    print(f'  Updated cross-refs in {n_files} files')


def step5_update_audit_script():
    """Update html_integrity_audit.py to expect the new letter assignments:
       C = Course Syllabi, D = Reading Pathways."""
    audit = ROOT / 'scripts' / 'html_integrity_audit.py'
    if not audit.exists(): return
    text = audit.read_text(encoding='utf-8')
    orig = text
    # Old patterns expected Appendix O/P/Q with Docker/Course/Pathways.
    # After Appendix O removal and P/Q/R/S/T -> C/D/E/F/G:
    #   C = Course Syllabi, D = Reading Pathways
    # Remove O check entirely.
    # Replace P check with C, Q check with D.
    text = re.sub(
        r'\(re\.compile\(r"\\\\bAppendix\\\\s\+O\\\\b[^)]+\), "\'Appendix O\' refers to non-Docker content"\),\s*\n\s*',
        '',
        text
    )
    text = re.sub(
        r'\(re\.compile\(r"\\\\bAppendix\\\\s\+P\\\\b\(\?\!\\\\s\*\(\?\:\[\\\\\.\\\\-:,\\\\\(\]\|\\\\s\|<\)\*\(\?:Course\|Syllab\)\)", re\.IGNORECASE\), "\'Appendix P\' refers to non-Course-Syllabi content"\),',
        '(re.compile(r"\\\\bAppendix\\\\s+C\\\\b(?!\\\\s*(?:[\\\\.\\\\-:,\\\\(]|\\\\s|<)*(?:Course|Syllab))", re.IGNORECASE), "\'Appendix C\' refers to non-Course-Syllabi content"),',
        text
    )
    text = re.sub(
        r'\(re\.compile\(r"\\\\bAppendix\\\\s\+Q\\\\b\(\?\!\\\\s\*\(\?\:\[\\\\\.\\\\-:,\\\\\(\]\|\\\\s\|<\)\*\(\?:Reading\|Pathways\)\)", re\.IGNORECASE\), "\'Appendix Q\' refers to non-Pathways content"\),',
        '(re.compile(r"\\\\bAppendix\\\\s+D\\\\b(?!\\\\s*(?:[\\\\.\\\\-:,\\\\(]|\\\\s|<)*(?:Reading|Pathways))", re.IGNORECASE), "\'Appendix D\' refers to non-Pathways content"),',
        text
    )
    if text != orig:
        audit.write_text(text, encoding='utf-8')
        print('  Updated html_integrity_audit.py letter expectations')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    if not args.apply:
        print('(DRY-RUN; pass --apply to execute)\n')

    if args.apply:
        step1_rename_directories()
        step2_rename_section_files()
        step3_rewrite_inside_files()
        step4_rewrite_external_refs()
        step5_update_audit_script()
    else:
        # Just print the planned renames
        print('Planned renames:')
        for ol, os_, nl, ns_ in RENAMES:
            print(f'  Appendix {ol.upper()} ({os_}) -> Appendix {nl.upper()} ({ns_})')


if __name__ == '__main__':
    sys.exit(main())
