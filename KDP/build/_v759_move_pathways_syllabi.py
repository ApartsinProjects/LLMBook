"""v759: Move pathways and syllabi from FM to appendices; renumber FM.

Per user direction:
  - Pathways are reference material consulted once; move to Appendix AJ.
  - Syllabi are reference material for instructors; move to Appendix AK.
  - FM keeps a brief overview + link in fm-who-should-read.
  - FM renumbers: drop FM.5 (pathways) and FM.6 (syllabi); FM.7 -> FM.5
    (How to Use), FM.8 -> FM.6 (Authors), FM.9 -> FM.7 (Copyright).

This script:
  1. Creates appendix-aj-reading-pathways/ and appendix-ak-course-syllabi/
  2. Copies the pathway/syllabi index.html into the new locations,
     rewriting relative paths so they resolve from appendices/.
  3. Updates the new files' titles to reference Appendix AJ/AK.
  4. Deletes the old front-matter/pathways/ and front-matter/syllabi/.
  5. Updates spine_manifest.json (remove old paths; appendices are
     auto-discovered).
  6. Cross-reference rewrites are handled in v760 (separate script).
"""
from __future__ import annotations
import re
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SRC_PATHWAYS = ROOT / 'front-matter' / 'pathways' / 'index.html'
SRC_SYLLABI = ROOT / 'front-matter' / 'syllabi' / 'index.html'
DST_PATHWAYS_DIR = ROOT / 'appendices' / 'appendix-aj-reading-pathways'
DST_SYLLABI_DIR = ROOT / 'appendices' / 'appendix-ak-course-syllabi'

assert SRC_PATHWAYS.exists(), f'missing {SRC_PATHWAYS}'
assert SRC_SYLLABI.exists(), f'missing {SRC_SYLLABI}'


def rewrite_paths_for_appendix_move(html: str) -> str:
    """Adjust relative URLs because the file moved from front-matter/X/
    to appendices/appendix-X/ (same depth, different parent)."""
    # Internal FM siblings: ../fm-foo.html -> ../../front-matter/fm-foo.html
    # Also ../index.html (the FM landing) -> ../../front-matter/index.html
    # And ../syllabi/ ../pathways/ -> appendix-aj... or appendix-ak...
    out = html

    # ../index.html (FM landing) -> point back to FM landing
    out = re.sub(r'href="\.\./index\.html"',
                 'href="../../front-matter/index.html"', out)

    # ../syllabi/index.html -> ../appendix-ak-course-syllabi/index.html
    out = re.sub(r'href="\.\./syllabi/index\.html"',
                 'href="../appendix-ak-course-syllabi/index.html"', out)
    out = re.sub(r'href="\.\./pathways/index\.html"',
                 'href="../appendix-aj-reading-pathways/index.html"', out)

    # ../fm-*.html -> ../../front-matter/fm-*.html
    out = re.sub(r'href="\.\./(fm-[a-z0-9-]+\.html)"',
                 r'href="../../front-matter/\1"', out)
    # ../foreword.html, ../about-authors.html, ../copyright.html, ../look-inside-preview.html
    for sib in ['foreword.html', 'about-authors.html', 'copyright.html',
                'look-inside-preview.html']:
        out = out.replace(f'href="../{sib}"',
                          f'href="../../front-matter/{sib}"')

    # The cross-appendix references (../../appendices/appendix-X/...) become
    # sibling references (../appendix-X/...). Keep ../../ for the rest.
    out = re.sub(r'href="\.\./\.\./appendices/(appendix-[a-z0-9-]+)/',
                 r'href="../\1/', out)

    return out


def move_one(src_file: Path, dst_dir: Path, new_label: str,
             new_title: str, new_h1: str, new_chap_label: str) -> None:
    print(f'\nMoving {src_file.relative_to(ROOT)} -> '
          f'{dst_dir.relative_to(ROOT)}/index.html')
    dst_dir.mkdir(parents=True, exist_ok=True)
    src = src_file.read_text(encoding='utf-8')
    new = rewrite_paths_for_appendix_move(src)

    # Update <title>
    new = re.sub(r'<title>[^<]*</title>',
                 f'<title>{new_title} | Building Conversational AI '
                 'with LLMs and Agents</title>', new, count=1)

    # Update part-label and chapter-label (these were "Front Matter")
    new = re.sub(
        r'<div class="part-label" data-pagefind-meta="part">[^<]*</div>',
        '<div class="part-label" data-pagefind-meta="part">'
        '<a href="../index.html">Appendices</a></div>', new, count=1)
    new = re.sub(
        r'<div class="chapter-label" data-pagefind-meta="chapter">[^<]*</div>',
        f'<div class="chapter-label" data-pagefind-meta="chapter">'
        f'<a href="index.html">{new_chap_label}</a></div>', new, count=1)

    # Update pagefind meta injected
    new = re.sub(
        r'data-pagefind-meta="part:[^"]+"',
        'data-pagefind-meta="part:Appendices"', new)
    new = re.sub(
        r'data-pagefind-meta="chapter:[^"]+"',
        f'data-pagefind-meta="chapter:{new_chap_label}"', new)

    # Update the h1 to reflect appendix labelling (light touch: keep
    # original h1 text but allow it to remain reader-friendly)
    new = re.sub(r'<h1>[^<]*</h1>', f'<h1>{new_h1}</h1>', new, count=1)

    # Update chapter-nav prev/next: appendix-aj prev=appendix-ai-..., next=ak
    # appendix-ak: prev=aj, next=appendix index? (use existing nearby letters)
    # We rewrite the whole chapter-nav block at the end of main:
    nav_block = (
        '<nav class="chapter-nav">\n'
        f'{new_label["prev_html"]}\n'
        '<a class="up" href="../index.html">Appendices</a>\n'
        f'{new_label["next_html"]}\n'
        '</nav>'
    )
    new = re.sub(r'<nav class="chapter-nav">.*?</nav>', nav_block, new,
                 count=1, flags=re.DOTALL)

    (dst_dir / 'index.html').write_text(new, encoding='utf-8')


# Appendix order:
# AI Freshness Index | AJ Reading Pathways | AK Course Syllabi |
# (no further appendix beyond AK; AK is last)
move_one(
    SRC_PATHWAYS, DST_PATHWAYS_DIR,
    new_label={
        'prev_html': '<a class="prev" href="../appendix-ai-freshness-2026/'
                     'index.html">&larr; Appendix AI: 2026 Freshness Index'
                     '</a>',
        'next_html': '<a class="next" href="../appendix-ak-course-syllabi/'
                     'index.html">Appendix AK: Course Syllabi &rarr;</a>',
    },
    new_title='Appendix AJ: Reading Pathways',
    new_h1='Appendix AJ: Reading Pathways',
    new_chap_label='Appendix AJ: Reading Pathways',
)
move_one(
    SRC_SYLLABI, DST_SYLLABI_DIR,
    new_label={
        'prev_html': '<a class="prev" href="../appendix-aj-reading-pathways/'
                     'index.html">&larr; Appendix AJ: Reading Pathways</a>',
        'next_html': '<a class="next" href="../index.html">Appendices Home '
                     '&rarr;</a>',
    },
    new_title='Appendix AK: Course Syllabi',
    new_h1='Appendix AK: Course Syllabi',
    new_chap_label='Appendix AK: Course Syllabi',
)

# Delete the old FM directories
for d in (ROOT / 'front-matter' / 'pathways',
          ROOT / 'front-matter' / 'syllabi'):
    if d.exists():
        shutil.rmtree(d)
        print(f'  removed {d.relative_to(ROOT)}')

# Update spine_manifest.json: drop the two old entries; appendices are
# auto-discovered when the build walks appendices/.
sp_path = ROOT / 'KDP' / 'build' / 'spine_manifest.json'
sp = json.loads(sp_path.read_text(encoding='utf-8'))
before = len(sp)
sp = [e for e in sp if e.get('path') not in (
    'front-matter/pathways/index.html',
    'front-matter/syllabi/index.html')]
after = len(sp)
sp_path.write_text(json.dumps(sp, indent=2), encoding='utf-8')
print(f'\nspine_manifest entries: {before} -> {after}')
print('done.')
