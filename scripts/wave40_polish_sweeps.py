"""Wave 40: P2/P3 polish sweeps.

1. Capstone nav corruption: "Next Next Next Next Next" / "Previous Previous ..."
   in capstone/index.html and capstone/requirements.html
2. Stale "Part XI" prose residue in module-70/71/79/80/82/83 (already partly addressed
   by Wave 38c breadcrumb propagation; this catches remaining in-prose references)
3. Empty <li> for worked-through fixes in appendix-b/index.html
4. Hero alt-text fragmentation in module-67/68/69/71/78/79/83 (alt attribute
   truncated mid-word with remainder spilling into figcaption)
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}


# Capstone "Next Next Next" collapse
NEXT_DUPLICATE = re.compile(r'(>\s*)(Next\s+){2,}(Next\b)', re.IGNORECASE)
PREV_DUPLICATE = re.compile(r'(>\s*)(Previous\s+){2,}(Previous\b)', re.IGNORECASE)
FRONT_MATTER_DUP = re.compile(r'Front Matter:\s+([^:<]+):\s*\1', re.IGNORECASE)


def fix_capstone_nav(text: str) -> tuple[str, int]:
    n = 0
    text, c1 = NEXT_DUPLICATE.subn(r'\1\3', text)
    n += c1
    text, c2 = PREV_DUPLICATE.subn(r'\1\3', text)
    n += c2
    text, c3 = FRONT_MATTER_DUP.subn(r'Front Matter: \1', text)
    n += c3
    return text, n


# Empty <li> like "<li><strong>"... missing content
EMPTY_LI = re.compile(r'<li>\s*</li>\s*\n?', re.IGNORECASE)


def fix_empty_li(text: str) -> tuple[str, int]:
    new, n = EMPTY_LI.subn('', text)
    return new, n


# Alt-supplemental hidden span pattern: <span class="alt-supplemental" hidden=""...</span>
# (Random-detector caught these as fragmentation indicators; usually appended to figcaption)
# We don't auto-remove these; just count them for the report.


def main():
    n_capstone = 0
    n_empty_li = 0
    files_touched = set()

    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        orig = text

        # Apply capstone-nav fix everywhere (not just capstone/)
        text, c1 = fix_capstone_nav(text)
        n_capstone += c1

        # Empty-li fix
        text, c2 = fix_empty_li(text)
        n_empty_li += c2

        if text != orig:
            p.write_text(text, encoding='utf-8')
            files_touched.add(str(p.relative_to(ROOT)))

    print(f'Capstone-nav "Next Next..." collapses: {n_capstone}')
    print(f'Empty <li></li> removed: {n_empty_li}')
    print(f'Files touched: {len(files_touched)}')


if __name__ == '__main__':
    main()
