"""Auto-fix the safe-to-regex bug classes senior-editor R2 flagged:

1. "Why: Why <claim>" -> "Why: <claim>" (drop one Why)
2. <h3 ...>...</h4> -> <h3 ...>...</h3> (close with matching tag)
3. <h4 ...>...</h3> -> <h4 ...>...</h4> (same)
4. Duplicate "What Comes Next" h2 above a whats-next div: remove the h2

Does NOT touch code-fragment labels (intentional cross-chapter refs).
Does NOT touch cross-reference rot (needs LLM judgement).
Does NOT touch table-prefix rot (rare; needs case-by-case).
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent

WHY_WHY = re.compile(r'\bWhy:\s+Why\b')
H3_OPEN_H4_CLOSE = re.compile(r'(<h3\b[^>]*>[^<]*)</h4>')
H4_OPEN_H3_CLOSE = re.compile(r'(<h4\b[^>]*>[^<]*)</h3>')
# Manual h2 "What Comes Next" or similar immediately followed by a whats-next div
DUP_WHATS_NEXT = re.compile(
    r'<h2\b[^>]*>\s*What\s+Comes?\s+Next[^<]*</h2>\s*(?=<div\s+class="[^"]*whats-next)',
    re.IGNORECASE
)


def fix_file(filepath):
    text = filepath.read_text(encoding='utf-8')
    orig = text
    fixes = []

    new_text, n = WHY_WHY.subn('Why:', text)
    if n:
        text = new_text
        fixes.append(f'{n} Why-Why')

    new_text, n = H3_OPEN_H4_CLOSE.subn(r'\1</h3>', text)
    if n:
        text = new_text
        fixes.append(f'{n} h3/h4-mismatch')

    new_text, n = H4_OPEN_H3_CLOSE.subn(r'\1</h4>', text)
    if n:
        text = new_text
        fixes.append(f'{n} h4/h3-mismatch')

    new_text, n = DUP_WHATS_NEXT.subn('', text)
    if n:
        text = new_text
        fixes.append(f'{n} dup-whatsnext')

    if text != orig:
        filepath.write_text(text, encoding='utf-8')
        return fixes
    return []


def main():
    html_files = []
    for part_dir in ROOT.glob('part-*'):
        if not part_dir.is_dir():
            continue
        for module_dir in part_dir.glob('module-*'):
            if not module_dir.is_dir():
                continue
            html_files.extend(module_dir.glob('section-*.html'))
            html_files.extend(module_dir.glob('index.html'))

    total_files = 0
    total_fixes = {'why_why': 0, 'h3h4': 0, 'h4h3': 0, 'dup_whatsnext': 0}
    for f in html_files:
        fixes = fix_file(f)
        if fixes:
            total_files += 1
            print(f"  {f.relative_to(ROOT)}: {', '.join(fixes)}")
            for fix in fixes:
                if 'Why-Why' in fix: total_fixes['why_why'] += int(fix.split()[0])
                elif 'h3/h4' in fix: total_fixes['h3h4'] += int(fix.split()[0])
                elif 'h4/h3' in fix: total_fixes['h4h3'] += int(fix.split()[0])
                elif 'dup-whats' in fix: total_fixes['dup_whatsnext'] += int(fix.split()[0])

    print(f"\n{'='*60}")
    print(f"Total: {total_files} files modified")
    for k, v in total_fixes.items():
        print(f"  {k}: {v}")


if __name__ == '__main__':
    main()
