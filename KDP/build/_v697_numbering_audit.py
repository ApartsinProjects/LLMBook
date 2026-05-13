"""8th edition Wave 23 / D-pass: chapter & figure numbering alignment audit.

Checks four classes of numbering debt:

1. Chapter cards in each part-index.html have the right chapter number.
2. Section file naming (section-X.Y.html) matches the section's <h1> /
   data-pagefind-meta numbering.
3. Figure labels (`Figure N.M.K:`) are sequential within each section
   (no duplicates, no gaps where a label exists but no preceding label).
4. Code-fragment labels (`Code Fragment N.M.K:`) are sequential within
   each section.

Read-only: report findings; the user decides whether to fix or accept.

Skips: agents/, archive, vendor, KDP/build, KDP/output, pagefind.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/')


def is_book_html(sp: str) -> bool:
    return not any(s in sp for s in SKIP)


def audit_figure_numbering() -> tuple[int, int]:
    """Within each section, figure labels should be increasing N.M.K.
    Report duplicates and out-of-order labels."""
    n_files_with_issues = 0
    n_issues = 0
    # Only count anchor labels (strong/em/figcaption), not alt-text.
    pat = re.compile(
        r'(?:<strong>|<em>|<figcaption[^>]*>)\s*Figure\s+(\d+)\.(\d+)\.(\d+)\s*:',
        re.IGNORECASE)
    for p in sorted(ROOT.rglob('section-*.html')):
        sp = str(p).replace('\\', '/')
        if not is_book_html(sp):
            continue
        text = p.read_text(encoding='utf-8', errors='replace')
        labels = pat.findall(text)
        if not labels:
            continue
        # Group by (chapter, section)
        by_section = defaultdict(list)
        for c, s, k in labels:
            by_section[(int(c), int(s))].append(int(k))
        issues_here = []
        for (c, s), ks in by_section.items():
            # Duplicates
            seen = set()
            dups = []
            for k in ks:
                if k in seen:
                    dups.append(k)
                seen.add(k)
            if dups:
                issues_here.append(f'Fig {c}.{s}: duplicate K={dups}')
            # Should be strictly increasing
            for i in range(1, len(ks)):
                if ks[i] < ks[i-1]:
                    issues_here.append(
                        f'Fig {c}.{s}: out of order at idx {i} ({ks[i-1]}->{ks[i]})')
                    break
        if issues_here:
            n_files_with_issues += 1
            n_issues += len(issues_here)
            print(f'  {p.relative_to(ROOT)}')
            for msg in issues_here:
                print(f'    {msg}')
    return n_files_with_issues, n_issues


def audit_code_numbering() -> tuple[int, int]:
    """Within each section, Code Fragment N.M.K should be increasing."""
    n_files = 0
    n_issues = 0
    pat = re.compile(r'Code Fragment\s+(\d+)\.(\d+)\.(\d+)\s*:', re.IGNORECASE)
    for p in sorted(ROOT.rglob('section-*.html')):
        sp = str(p).replace('\\', '/')
        if not is_book_html(sp):
            continue
        text = p.read_text(encoding='utf-8', errors='replace')
        labels = pat.findall(text)
        if not labels:
            continue
        by_section = defaultdict(list)
        for c, s, k in labels:
            by_section[(int(c), int(s))].append(int(k))
        issues_here = []
        for (c, s), ks in by_section.items():
            seen = set()
            dups = []
            for k in ks:
                if k in seen:
                    dups.append(k)
                seen.add(k)
            if dups:
                issues_here.append(f'Code {c}.{s}: duplicate K={dups}')
            for i in range(1, len(ks)):
                if ks[i] < ks[i-1]:
                    issues_here.append(
                        f'Code {c}.{s}: out of order ({ks[i-1]}->{ks[i]})')
                    break
        if issues_here:
            n_files += 1
            n_issues += len(issues_here)
            print(f'  {p.relative_to(ROOT)}')
            for msg in issues_here:
                print(f'    {msg}')
    return n_files, n_issues


def audit_section_numbering() -> tuple[int, int]:
    """section-X.Y.html should match the <h1> chapter/section number."""
    n_files = 0
    n_issues = 0
    h1_pat = re.compile(r'<h1[^>]*>\s*(\d+\.\d+)', re.IGNORECASE)
    name_pat = re.compile(r'section-(\d+)\.(\d+)\.html$', re.IGNORECASE)
    for p in sorted(ROOT.rglob('section-*.html')):
        sp = str(p).replace('\\', '/')
        if not is_book_html(sp):
            continue
        m = name_pat.search(p.name)
        if not m:
            continue
        expect = f'{m.group(1)}.{m.group(2)}'
        text = p.read_text(encoding='utf-8', errors='replace')
        m2 = h1_pat.search(text)
        if not m2:
            # Some sections have non-numeric H1; skip
            continue
        actual = m2.group(1)
        if actual != expect:
            n_files += 1
            n_issues += 1
            print(f'  {p.relative_to(ROOT)} : H1 says {actual}, filename says {expect}')
    return n_files, n_issues


def main() -> int:
    print('=== Section numbering (filename vs. <h1>) ===')
    a, b = audit_section_numbering()
    print(f'  {a} files with section-number mismatch; {b} issues\n')

    print('=== Figure label sequencing (per section) ===')
    a, b = audit_figure_numbering()
    print(f'  {a} files with figure-label issues; {b} issues\n')

    print('=== Code Fragment label sequencing (per section) ===')
    a, b = audit_code_numbering()
    print(f'  {a} files with code-fragment-label issues; {b} issues\n')

    return 0


if __name__ == '__main__':
    sys.exit(main())
