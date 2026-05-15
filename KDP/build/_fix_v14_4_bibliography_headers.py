"""v14.4: consolidate bibliography section headings.

User wants ONE heading per bibliography section: "Bibliography and
Further Reading". Audit found:
  - 213 sections use <h3>Further Reading</h3> as canonical
  - 8 module index pages ALSO have <h2>Bibliography & Further Reading</h2>
    (duplicate, structurally redundant)
  - Many sections have multiple <h3> children (category headings like
    "Foundational Papers", "Tools and Frameworks") which is FINE

Fix:
  1. Find every <section class="bibliography">
  2. Remove duplicate <h2>Bibliography...</h2> if present alongside h3
  3. Rename the FIRST <h3>Further Reading</h3> to
     <h3>Bibliography and Further Reading</h3>
     (keep at h3 for consistency with callout-title sizing)
  4. Category sub-headings stay as <h3> or get demoted to <h4> if they
     follow the renamed canonical heading.

Run with --apply to write changes.
"""
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
import sys

ROOT = Path(__file__).resolve().parents[2]
SKIP = ['node_modules', '.git', 'KDP/output', 'KDP/build', 'KDP/html2pub',
        'pagefind', 'temp_epub', 'backup', 'source_fix_backups', 'templates']


def skip(p):
    sp = str(p).replace('\\', '/')
    return any(s in sp for s in SKIP)


def fix_file(p: Path, dry: bool) -> tuple[int, int]:
    """Returns (sections_processed, modifications)."""
    s = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
    n_sections = 0
    n_modified = 0
    for sec in s.find_all('section', class_='bibliography'):
        n_sections += 1
        # 1. Remove duplicate <h2>Bibliography...</h2>
        for h2 in list(sec.find_all('h2')):
            txt = h2.get_text(strip=True).lower()
            if 'bibliography' in txt or 'further reading' in txt:
                h2.decompose()
                n_modified += 1

        # 2. Find first <h3>Further Reading</h3> and rename
        first_h3 = sec.find('h3')
        if first_h3:
            txt = first_h3.get_text(strip=True)
            if txt == 'Further Reading':
                first_h3.clear()
                first_h3.append(NavigableString('Bibliography and Further Reading'))
                n_modified += 1

        # 3. Demote subsequent <h3> category headings to <h4>
        # Skip the renamed canonical h3 (which is the first one)
        h3s = sec.find_all('h3')
        if len(h3s) > 1:
            for h3 in h3s[1:]:
                txt = h3.get_text(strip=True)
                # Skip if already canonical (renamed above)
                if 'Bibliography and Further Reading' in txt:
                    continue
                new_h4 = s.new_tag('h4', **h3.attrs)
                for child in list(h3.children):
                    new_h4.append(child.extract() if hasattr(child, 'extract') else child)
                h3.replace_with(new_h4)
                n_modified += 1

    if n_modified > 0 and not dry:
        p.write_text(str(s), encoding='utf-8')
    return n_sections, n_modified


def main():
    dry = '--apply' not in sys.argv
    print('DRY RUN. Pass --apply.' if dry else 'APPLY mode.')
    print()
    total_secs = 0
    total_mods = 0
    n_files = 0
    for p in ROOT.rglob('*.html'):
        if skip(p):
            continue
        secs, mods = fix_file(p, dry)
        total_secs += secs
        total_mods += mods
        if mods > 0:
            n_files += 1
            print(f'  {p.relative_to(ROOT)}: {mods} mods in {secs} bib section(s)')
    print()
    print(f'Sections processed: {total_secs}')
    print(f'Modifications:      {total_mods}')
    print(f'Files modified:     {n_files}')


if __name__ == '__main__':
    main()
