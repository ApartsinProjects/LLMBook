"""v6.5: Fix toc.html chapter placement + move Pseudocode captions
into algorithm callouts.

USER REPORTS

A. "there is no section 18 in the ToC"
   Audit found 4 errors in the compact view of toc.html:
     - Part II listed Ch 18 (Interpretability) which actually lives in Part X
     - Part IV listed phantom Ch 16 (merged into Ch 15 PEFT in v3.x)
     - Part VIII listed phantom Ch 30 (merged into Ch 29 in v3.x)
     - Part X listed phantom Ch 35 (merged into Ch 32 + 17.5 in v3.x) and
       was MISSING Ch 18

B. "Pseudocode 29.2.1: is orphan, find root cause, should it be inside
    algorithm box, fix everywhere in the book"
   Audit found 22 Pseudocode captions across the book, ALL in the same
   awkward pattern:

     <div class="code-caption"><strong>Pseudocode N.M.K:</strong> desc</div>
     <div class="callout algorithm">
       <div class="callout-title">Algorithm</div>
       <pre>...</pre>
     </div>

   The caption sits OUTSIDE the algorithm callout, then a generic
   "Algorithm" title appears INSIDE. Fix: collapse them — promote the
   pseudocode caption to BECOME the callout's title.

   After:
     <div class="callout algorithm">
       <div class="callout-title">Pseudocode N.M.K: desc</div>
       <pre>...</pre>
     </div>

   Eliminates the orphan and gives each algorithm box a meaningful title.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = {'agents', 'KDP', 'node_modules', 'scripts', '.git',
        'chapter_review', 'downloads', '_archive', '_lab_fragments',
        'templates'}


# ============ A. ToC compact-view fixes ============

def fix_toc() -> int:
    p = ROOT / 'toc.html'
    text = p.read_text(encoding='utf-8')
    original = text
    edits = 0

    # A.1. Remove Ch 18 row from Part II compact view
    p_ch18_in_partII = re.compile(
        r'\s*<div class="dense-chapter"><span class="dense-ch-num">Ch 18</span>'
        r' <a href="part-10-frontiers/module-18-interpretability/index\.html">'
        r'Interpretability[^<]*</a></div>',
    )
    # Only remove the FIRST occurrence (in Part II compact view); preserve
    # the one in Part X.
    # We need to be specific: find the one INSIDE the Part II section.
    # Strategy: locate Part II compact header, then the closing of its <div class="stoc-group">.
    # Within that span, remove the Ch 18 row.
    part_ii_start = text.find('<a href="part-2-understanding-llms/index.html">Part II:')
    if part_ii_start > 0:
        # find next </div></div> closing the stoc-group
        end_marker = text.find('</div>\n        </div>', part_ii_start)
        if end_marker > 0:
            segment = text[part_ii_start:end_marker]
            new_segment, n = p_ch18_in_partII.subn('', segment, count=1)
            if n:
                text = text[:part_ii_start] + new_segment + text[end_marker:]
                edits += 1
                print('  A.1 removed Ch 18 row from Part II compact view')

    # A.2. Remove phantom Ch 16 from Part IV compact view
    p_ch16 = re.compile(
        r'\s*<div class="dense-chapter"><span class="dense-ch-num">Ch 16</span>'
        r'[^<]*<a[^>]*>[^<]*</a></div>',
    )
    new_text, n = p_ch16.subn('', text)
    if n:
        text = new_text
        edits += n
        print(f'  A.2 removed {n} phantom Ch 16 row(s)')

    # A.3. Remove phantom Ch 30 from Part VIII compact view
    p_ch30 = re.compile(
        r'\s*<div class="dense-chapter"><span class="dense-ch-num">Ch 30</span>'
        r'[^<]*<a[^>]*>[^<]*</a></div>',
    )
    new_text, n = p_ch30.subn('', text)
    if n:
        text = new_text
        edits += n
        print(f'  A.3 removed {n} phantom Ch 30 row(s)')

    # A.4. Remove phantom Ch 35 from Part X compact view
    p_ch35 = re.compile(
        r'\s*<div class="dense-chapter"><span class="dense-ch-num">Ch 35</span>'
        r'[^<]*<a[^>]*>[^<]*</a></div>',
    )
    new_text, n = p_ch35.subn('', text)
    if n:
        text = new_text
        edits += n
        print(f'  A.4 removed {n} phantom Ch 35 row(s)')

    # A.5. Ensure Part X compact view has Ch 18 before Ch 34
    # Find the Part X compact-view block; check if Ch 18 is already there;
    # if not, insert before Ch 34.
    part_x_start = text.find('<a href="part-10-frontiers/index.html">Part X:')
    if part_x_start > 0:
        # find the stoc-group close
        end_marker = text.find('</div>\n        </div>', part_x_start)
        if end_marker > 0:
            segment = text[part_x_start:end_marker]
            if 'Ch 18' not in segment:
                # Insert Ch 18 row before Ch 34
                CH18_ROW = (
                    '                <div class="dense-chapter">'
                    '<span class="dense-ch-num">Ch 18</span> '
                    '<a href="part-10-frontiers/module-18-interpretability/index.html">'
                    'Interpretability &amp; Mechanistic Understanding</a></div>\n'
                )
                new_segment = re.sub(
                    r'(<div class="dense-chapter"><span class="dense-ch-num">Ch 34</span>)',
                    CH18_ROW + r'                \1',
                    segment, count=1,
                )
                if new_segment != segment:
                    text = text[:part_x_start] + new_segment + text[end_marker:]
                    edits += 1
                    print('  A.5 added Ch 18 row to Part X compact view (before Ch 34)')

    if text != original:
        p.write_text(text, encoding='utf-8')
    return edits


# ============ B. Move Pseudocode captions into algorithm callouts ============

# Pattern:
#   <div class="code-caption"><strong>Pseudocode {N.M.K}:</strong> {DESC}</div>
#   <div class="callout algorithm">
#     <div class="callout-title">{OLD_TITLE}</div>
#
# Replace with:
#   <div class="callout algorithm">
#     <div class="callout-title">Pseudocode {N.M.K}: {DESC}</div>

PSEUDO_PAT = re.compile(
    r'<div class="code-caption">\s*<strong>(Pseudocode [\d\.]+)\s*:</strong>\s*'
    r'(?P<desc>[^<]+)\s*</div>\s*'
    r'<div class="callout algorithm">\s*'
    r'<div class="callout-title">[^<]*</div>',
    re.IGNORECASE | re.DOTALL,
)


def fix_pseudocode(p: Path) -> int:
    text = p.read_text(encoding='utf-8', errors='replace')
    def repl(m):
        cap = m.group(1)
        desc = m.group('desc').strip()
        return (
            f'<div class="callout algorithm">\n'
            f'<div class="callout-title">{cap}: {desc}</div>'
        )
    new_text, n = PSEUDO_PAT.subn(repl, text)
    if n:
        p.write_text(new_text, encoding='utf-8')
    return n


def main() -> int:
    print('A. ToC compact-view fixes')
    n_a = fix_toc()
    print(f'   total ToC edits: {n_a}')

    print('\nB. Move Pseudocode captions inside algorithm callouts')
    total = 0
    files = 0
    for p in sorted(ROOT.rglob('*.html')):
        rel = p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP:
            continue
        n = fix_pseudocode(p)
        if n:
            files += 1
            total += n
            print(f'   + {n}  {rel}')
    print(f'   total Pseudocode merges: {total} across {files} files')
    return 0


if __name__ == '__main__':
    sys.exit(main())
