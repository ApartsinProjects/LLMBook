"""Wave 7: appendix restructure (7 -> 2 appendices).

Per v9 plan:
  - Drop pedagogy appendices entirely: E (Intermediate Projects), F (Capstone),
    G (War Stories)
  - Absorb A (Math) into Part I Ch 0 as new sections 0.1 + 0.2
  - Absorb B.1-B.3 (ML basics) into Part I Ch 0 sec 0.3 (existing)
  - Move B.4 (Evaluation Metrics, 22 inbound refs) -> Part IX Ch 44 (Eval Foundations)
    as new opening section
  - Renumber remaining: C -> A (Course Syllabi), D -> B (Reading Pathways)

For now, we do the SIMPLE moves: rename appendix directories and update refs.
The actual content absorption into main book (Math -> Ch 0, Eval Metrics -> Ch 44)
is deferred to Wave 9 content authoring, since it requires merging HTML content.
"""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs'}


def git_rm(p):
    if not p.exists(): return False
    r = subprocess.run(['git', 'rm', '-rf', str(p)], cwd=ROOT,
                      capture_output=True, text=True)
    return r.returncode == 0


def git_mv(src, dst):
    if not src.exists() or dst.exists(): return False
    r = subprocess.run(['git', 'mv', str(src), str(dst)], cwd=ROOT,
                      capture_output=True, text=True)
    return r.returncode == 0


def drop_appendices():
    """Drop E (Projects), F (Capstone), G (War Stories) — pedagogy material."""
    print('--- Drop pedagogy appendices E/F/G ---')
    for slug in ['appendix-e-intermediate-projects',
                 'appendix-f-capstone-project',
                 'appendix-g-war-stories']:
        p = ROOT / 'appendices' / slug
        if git_rm(p):
            print(f'  Dropped: {slug}')


def renumber_remaining():
    """C -> A, D -> B; preserve A (Math) and B (ML) for absorption."""
    print('--- Renumber appendices: preserve A (Math) and B (ML); C->A, D->B for pedagogy ---')
    # Use intermediate names to avoid collisions
    moves = [
        # First: archive A and B (Math and ML) — they'll be absorbed into main book in Wave 9
        # For now, move them to .book-update/ for preservation
        ('appendix-a-mathematical-foundations', '__preserved__appendix-a-math'),
        ('appendix-b-ml-essentials', '__preserved__appendix-b-ml'),
        # Then renumber C and D using temp names
        ('appendix-c-course-syllabi', '__tmp__appendix-a-course-syllabi'),
        ('appendix-d-reading-pathways', '__tmp__appendix-b-reading-pathways'),
    ]
    for src, dst in moves:
        sp = ROOT / 'appendices' / src
        dp = ROOT / 'appendices' / dst
        if git_mv(sp, dp):
            print(f'  Step 1: {src} -> {dst}')
    # Now move the tmp names to final A, B
    finals = [
        ('__tmp__appendix-a-course-syllabi', 'appendix-a-course-syllabi'),
        ('__tmp__appendix-b-reading-pathways', 'appendix-b-reading-pathways'),
    ]
    for src, dst in finals:
        sp = ROOT / 'appendices' / src
        dp = ROOT / 'appendices' / dst
        if git_mv(sp, dp):
            print(f'  Step 2: {src} -> {dst}')


def rewrite_appendix_refs():
    """Update body refs across the book to new appendix letters/slugs."""
    print('--- Rewriting appendix refs ---')
    mapping = [
        # Old slug -> new slug (mapping)
        ('appendix-c-course-syllabi', 'appendix-a-course-syllabi'),
        ('appendix-d-reading-pathways', 'appendix-b-reading-pathways'),
    ]
    # For body labels: Old letter (C, D) -> new letter (A, B)
    label_mapping = [('Appendix C', 'Appendix A'),
                     ('Appendix D', 'Appendix B')]
    # Refs to deleted appendices (E, F, G) — drop with chapter index fallback
    drop_refs = ['appendix-e-intermediate-projects', 'appendix-f-capstone-project',
                 'appendix-g-war-stories']

    n_files = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP: continue
        # Skip the appendix-A (Math) and appendix-B (ML) preserved dirs
        if '__preserved__' in str(p): continue
        text = p.read_text(encoding='utf-8')
        orig = text
        # Drop refs to deleted appendices (replace with appendix-index)
        for slug in drop_refs:
            # href="...appendix-X/index.html" -> href="appendices/index.html"
            text = re.sub(
                rf'href="([^"]*?){re.escape(slug)}(/[^"]*)?"',
                r'href="\1index.html"',
                text
            )
        # Renumber refs to old C and D
        for old, new in mapping:
            text = text.replace(old, new)
        # Update body labels
        for old_label, new_label in label_mapping:
            text = re.sub(rf'\b{re.escape(old_label)}\b', new_label, text)
        # Visible aria-labels in toc and chapter cards
        text = re.sub(r'aria-label="Appendix C"', 'aria-label="Appendix A"', text)
        text = re.sub(r'aria-label="Appendix D"', 'aria-label="Appendix B"', text)
        if text != orig:
            p.write_text(text, encoding='utf-8')
            n_files += 1
    print(f'  Updated refs in {n_files} files')


def update_appendices_index():
    """Update appendices/index.html to show new structure."""
    p = ROOT / 'appendices/index.html'
    if not p.exists(): return
    text = p.read_text(encoding='utf-8')

    # Remove chapter-cards for E, F, G (will be missing entries)
    for letter in 'EFG':
        text = re.sub(
            rf'<div class="chapter-card">\s*'
            rf'<div class="chapter-card-header">\s*<span class="mod-num">Appendix {letter}</span>[^<]*</div>\s*'
            rf'<div class="chapter-card-body">[\s\S]*?</div>\s*</div>\s*',
            '', text
        )
    # Also remove any h2 "For Instructors" section if it had only E/F/G
    text = re.sub(
        r'<h2 id="group-for-instructors">[^<]+</h2>\s*(?=<h2|</main>)',
        '', text
    )
    # Remove the math+ML chapter cards (they're absorbed; will preserve as note)
    for letter in 'AB':
        text = re.sub(
            rf'<div class="chapter-card">\s*'
            rf'<div class="chapter-card-header">\s*<span class="mod-num">Appendix {letter}</span>[^<]*</div>\s*'
            rf'<div class="chapter-card-body">[\s\S]*?</div>\s*</div>\s*',
            '', text
        )
    # Now the appendix-c-course-syllabi (now appendix-a) and appendix-d-reading-pathways (now appendix-b) cards
    # should be at C and D labels. The body-ref rewrite above changes their visible letters to A and B.
    p.write_text(text, encoding='utf-8')
    print('  Updated appendices/index.html')


def update_toc_appendix_section():
    """Update toc.html — keep only Appendix A and B entries."""
    p = ROOT / 'toc.html'
    text = p.read_text(encoding='utf-8')
    # Remove appendix entries that became preserved or deleted
    for slug in ['__preserved__appendix-a-math', '__preserved__appendix-b-ml',
                 'appendix-e-intermediate-projects', 'appendix-f-capstone-project',
                 'appendix-g-war-stories']:
        # Find and remove <li class="toc-chapter toc-appendix"> blocks referencing the slug
        text = re.sub(
            rf'<li class="toc-chapter[^"]*">\s*<a href="appendices/{re.escape(slug)}/[^"]*">[\s\S]*?</a>\s*</li>\s*',
            '', text
        )
    # Update the appendix-count chip
    text = re.sub(r'<span class="toc-part-count">\d+ appendices</span>',
                  '<span class="toc-part-count">2 appendices</span>', text)
    p.write_text(text, encoding='utf-8')
    print('  Updated toc.html appendix section')


def main():
    print('=== WAVE 7: appendix restructure ===\n')
    drop_appendices()
    print()
    renumber_remaining()
    print()
    rewrite_appendix_refs()
    print()
    update_appendices_index()
    print()
    update_toc_appendix_section()


if __name__ == '__main__':
    main()
