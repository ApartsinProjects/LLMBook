"""v760 (rev2): Renumber FM after pathways/syllabi move + fix em-dashes + xrefs.

After v759 moved pathways and syllabi to Appendix AJ/AK, FM is now:

  FM.1 Foreword
  FM.2 What's Inside (look-inside-preview.html)
  FM.3 What This Book Covers
  FM.4 Who Should Read This Book
  FM.5 How to Use This Book      (was FM.7)
  FM.6 About the Authors          (was FM.8)
  FM.7 Copyright & Legal          (was FM.9)

CRITICAL: rules MUST require the noun phrase to avoid bleed. Otherwise
"FM.8 About the Authors" -> "FM.6 About the Authors" gets re-matched by
"FM.6 -> Appendix AK Course Syllabi". To prevent this:

  - All renumber rules require the SPECIFIC noun phrase that follows.
  - The "FM.5 Reading Pathways -> Appendix AJ" rule REQUIRES the words
    "Reading Pathways" to follow.
  - Same for "FM.6 Course Syllabi".

Path rewrites are pure string replacements; no risk of bleed.

Idempotent.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# Each rule: (pattern, replacement). All require explicit noun phrases.
XREF_REPLACE = [
    # FM.7 How to Use -> FM.5 How to Use (label may use ":" or " ")
    (re.compile(r'\bFM\.7([:\s]+How to Use This Book)\b'),
     r'FM.5\1'),
    (re.compile(r'\bFM\.7\s+How to Use\b'),
     'FM.5 How to Use'),
    # FM.8 About the Authors -> FM.6 About the Authors
    (re.compile(r'\bFM\.8([:\s]+About the Authors)\b'),
     r'FM.6\1'),
    # FM.9 Copyright -> FM.7 Copyright
    (re.compile(r'\bFM\.9([:\s]+Copyright)'),
     r'FM.7\1'),
    # FM.5 Reading Pathways -> Appendix AJ: Reading Pathways  (REQUIRES noun)
    (re.compile(r'\bFM\.5\s+Reading Pathways\b'),
     'Appendix AJ: Reading Pathways'),
    (re.compile(r'\bFM\.5:\s+Reading Pathways\b'),
     'Appendix AJ: Reading Pathways'),
    # FM.6 Course Syllabi -> Appendix AK: Course Syllabi  (REQUIRES noun)
    (re.compile(r'\bFM\.6\s+Course Syllabi\b'),
     'Appendix AK: Course Syllabi'),
    (re.compile(r'\bFM\.6:\s+Course Syllabi\b'),
     'Appendix AK: Course Syllabi'),
]

# Pure path rewrites (substring; safe because URLs are unique strings)
HREF_PATTERNS = [
    ('href="pathways/index.html"',
     'href="../appendices/appendix-aj-reading-pathways/index.html"'),
    ('href="syllabi/index.html"',
     'href="../appendices/appendix-ak-course-syllabi/index.html"'),
    ('href="../pathways/index.html"',
     'href="../../appendices/appendix-aj-reading-pathways/index.html"'),
    ('href="../syllabi/index.html"',
     'href="../../appendices/appendix-ak-course-syllabi/index.html"'),
    ('front-matter/pathways/index.html',
     'appendices/appendix-aj-reading-pathways/index.html'),
    ('front-matter/syllabi/index.html',
     'appendices/appendix-ak-course-syllabi/index.html'),
]

# Em-dash rules (FM ONLY). Conservative.
EM_DASH_RULES = [
    # "</strong></a> &mdash; description" -> ": "
    (re.compile(r'(</strong></a>)\s*&mdash;\s*'), r'\1: '),
    (re.compile(r'(</a>)\s*&mdash;\s*'), r'\1: '),
    # "or by any means &mdash; X &mdash; without"
    (re.compile(r'(by any means)\s*&mdash;\s*([^&]+?)\s*&mdash;\s*'),
     r'\1 (\2) '),
    # Generic remaining &mdash; surrounded by space
    (re.compile(r'\s+&mdash;\s+'), ', '),
    (re.compile(r'\s+—\s+'), ', '),
    (re.compile(r'\s+&#8212;\s+'), ', '),
]


def fix_em_dashes(html: str) -> tuple[str, int]:
    n = 0
    for pat, rep in EM_DASH_RULES:
        html, c = pat.subn(rep, html)
        n += c
    return html, n


def apply_xref_rewrites(html: str) -> tuple[str, int]:
    n = 0
    for pat, rep in XREF_REPLACE:
        html, c = pat.subn(rep, html)
        n += c
    for old, new_v in HREF_PATTERNS:
        c = html.count(old)
        if c:
            html = html.replace(old, new_v)
            n += c
    return html, n


SKIP_DIRS = ('KDP/build/source_fix_backups', 'pagefind', 'node_modules',
             'temp_epub', '.git', 'venv')


def should_skip(p: Path) -> bool:
    sp = str(p).replace('\\', '/')
    return any(s in sp for s in SKIP_DIRS)


def main() -> int:
    n_files_xref = 0
    n_files_em = 0
    total_xref = 0
    total_em = 0
    for p in ROOT.rglob('*.html'):
        if should_skip(p):
            continue
        try:
            src = p.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue
        new = src
        new, c1 = apply_xref_rewrites(new)
        is_fm = '/front-matter/' in str(p).replace('\\', '/') + '/'
        c2 = 0
        if is_fm:
            new, c2 = fix_em_dashes(new)
        if new != src:
            p.write_text(new, encoding='utf-8')
            if c1:
                n_files_xref += 1
                total_xref += c1
            if c2:
                n_files_em += 1
                total_em += c2
            print(f'  [{p.relative_to(ROOT)}] xref={c1} em={c2}')
    print(f'\nxref rewrites: {total_xref} across {n_files_xref} files')
    print(f'em-dash fixes (FM only): {total_em} across {n_files_em} files')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
