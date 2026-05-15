"""v14.5: standardize appendix section + single-page numbering in h1 titles.

For section files (section-X.N.html): prefix h1 with "X.N "
  - "Linear Algebra Essentials" -> "A.1 Linear Algebra Essentials"

For single-page appendices (index.html only): prefix h1 with "Appendix X: "
  - "Master Reference Tables" -> "Appendix AD: Master Reference Tables"

Skip files where the prefix is already present.
"""
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
APPENDICES = ROOT / 'appendices'


def fix_section_files(dry):
    n = 0
    for app_dir in APPENDICES.iterdir():
        if not app_dir.is_dir():
            continue
        for sec in app_dir.glob('section-*.html'):
            m = re.match(r'section-([a-z]+)\.(\d+)\.html', sec.name)
            if not m:
                continue
            prefix_id = f'{m.group(1).upper()}.{m.group(2)}'
            s = BeautifulSoup(sec.read_text(encoding='utf-8'), 'html.parser')
            h1 = s.find('h1')
            if not h1:
                continue
            current = h1.get_text(strip=True)
            # Skip if prefix already present (e.g., "A.1 Linear..." or "A.1:" or "Section A.1")
            if (current.startswith(prefix_id) or
                current.startswith(f'Section {prefix_id}') or
                current.startswith(f'{prefix_id}:') or
                current.startswith(f'{prefix_id}.')):
                continue
            # Build new title: "A.1 Linear Algebra Essentials"
            new_title = f'{prefix_id} {current}'
            h1.clear()
            h1.append(NavigableString(new_title))
            if not dry:
                sec.write_text(str(s), encoding='utf-8')
            n += 1
            print(f'  {sec.relative_to(ROOT)}: "{current[:40]}..." -> "{new_title[:50]}..."')
    return n


def fix_single_page_appendices(dry):
    """Single-page appendices: their index.html h1 should be 'Appendix X: Title'."""
    # Map dir to appendix letter
    SINGLE_PAGE_LETTER = {
        'appendix-ad-master-reference-tables': 'AD',
        'appendix-ae-production-patterns':     'AE',
        'appendix-af-pedagogy-kit':            'AF',
        'appendix-ag-problem-solution-key':    'AG',
        'appendix-ai-freshness-2026':          'AI',
        'appendix-aj-reading-pathways':        'AJ',
        'appendix-ak-course-syllabi':          'AK',
    }
    n = 0
    for dir_name, letter in SINGLE_PAGE_LETTER.items():
        d = APPENDICES / dir_name
        idx = d / 'index.html'
        if not idx.exists():
            continue
        s = BeautifulSoup(idx.read_text(encoding='utf-8'), 'html.parser')
        h1 = s.find('h1')
        if not h1:
            continue
        current = h1.get_text(strip=True)
        if current.startswith(f'Appendix {letter}') or current.startswith(f'Appendix {letter}:'):
            continue
        new_title = f'Appendix {letter}: {current}'
        h1.clear()
        h1.append(NavigableString(new_title))
        if not dry:
            idx.write_text(str(s), encoding='utf-8')
        n += 1
        print(f'  {idx.relative_to(ROOT)}: -> "{new_title[:60]}"')
    return n


if __name__ == '__main__':
    dry = '--apply' not in sys.argv
    print('DRY RUN.' if dry else 'APPLY mode.')
    print()
    print('=== Section files (h1 prefix) ===')
    n1 = fix_section_files(dry)
    print(f'\n=== Single-page appendices (Appendix X: prefix) ===')
    n2 = fix_single_page_appendices(dry)
    print(f'\nTotal: {n1 + n2} files updated')
