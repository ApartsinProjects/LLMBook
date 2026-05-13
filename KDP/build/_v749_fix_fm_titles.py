"""Fix stale FM.X: title prefixes in renamed FM files.

The <title> tags still carry the old FM numbering (e.g. "FM.1: What
This Book Covers" inside what is now FM.3). Sync each to the new
display label.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
FM = ROOT / 'front-matter'

# (filename, new title prefix, new <h1>)
TITLES = [
    ('foreword.html',                       'FM.1 Foreword',                    'Foreword'),
    ('look-inside-preview.html',            'FM.2 What\'s Inside',              'What\'s Inside'),
    ('fm-what-this-book-covers.html',       'FM.3 What This Book Covers',       'What This Book Covers'),
    ('fm-who-should-read.html',             'FM.4 Who Should Read This Book',   'Who Should Read This Book'),
    ('pathways/index.html',                 'FM.5 Reading Pathways',            'Reading Pathways: Goal-Based Routes with Timing'),
    ('syllabi/index.html',                  'FM.6 Course Syllabi',              'Course Syllabi'),
    ('fm-problem-solution-key.html',        'FM.7 Problem-Solution Key',        'Problem-Solution Key'),
    ('fm-how-to-use.html',                  'FM.8 How to Use This Book',        'How to Use This Book: Conventions, Callouts & Labs'),
    ('fm-conceptual-map.html',              'FM.9 Conceptual Map of This Book', 'Conceptual Map of This Book'),
    ('fm-reference-tables.html',            'FM.10 Master Reference Tables',    'Master Reference Tables'),
    ('fm-freshness-2026.html',              'FM.11 2026 Freshness Index',       '2026 Freshness Index'),
    ('fm-production-patterns.html',         'FM.12 Production Patterns Reference', 'Production Patterns Reference'),
    ('fm-pedagogy-kit.html',                'FM.13 Pedagogy Kit',               'Pedagogy Kit: Capstone Rubric, Intermediate Projects, War Stories'),
    ('fm-what-2026-settled.html',           'FM.14 What 2026 Settled',          'What 2026 Settled'),
    ('about-authors.html',                  'FM.15 About the Authors',          'About the Authors'),
    ('copyright.html',                      'FM.16 Copyright & Legal',          'Copyright'),
]


def fix_title(html: str, new_prefix: str) -> str:
    """Replace whatever is before ' | Building Conversational' or
    ' | LLM' or just at the start of the <title> with new_prefix."""
    # Pattern: <title>OLD | Building Conversational AI...</title>
    suffix = ' | Building Conversational AI with LLMs and Agents'
    # Generic title replacement: always set to new_prefix + suffix
    return re.sub(
        r'<title>[^<]*</title>',
        f'<title>{new_prefix}{suffix}</title>',
        html,
        count=1,
        flags=re.IGNORECASE)


def main() -> int:
    fix = '--fix' in sys.argv
    files_touched = 0
    for rel, new_prefix, _h1 in TITLES:
        path = FM / rel
        if not path.exists():
            print(f'  ! missing: {rel}')
            continue
        text = path.read_text(encoding='utf-8')
        new = fix_title(text, new_prefix)
        if new != text:
            files_touched += 1
            print(f'  + {rel} -> "{new_prefix}"')
            if fix:
                path.write_text(new, encoding='utf-8')
        else:
            print(f'  = {rel} (already)')
    mode = 'APPLIED' if fix else 'DRY-RUN'
    print(f'\n[{mode}] {files_touched} title(s) updated')
    if not fix:
        print('Re-run with --fix to apply.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
