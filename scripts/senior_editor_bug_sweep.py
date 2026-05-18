"""Detect the 5 systemic bug classes that senior-editor R2 flagged.

1. "Why: Why <claim>" — duplicate Why prefix in callout titles
2. "Table X.Y.Z: A.B <title>" — stray old chapter prefix in table titles
3. "Code Fragment [A-Z]." — old-style code-fragment labels in sections
4. Mismatched h3/h4 tags — <h3>...</h4>
5. Duplicate "What Comes Next" (manual h2 + standard div)

Stale temporal framing (March 2027 in 2026 book) is also checked.

Runs across all section-*.html and index.html files under part-*/.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent

# Patterns
WHY_WHY = re.compile(r'Why:\s+Why\b', re.IGNORECASE)
TABLE_PREFIX = re.compile(r'<(?:strong|b)>Table\s+(\d+)\.(\d+)\.(\d+):\s+(\d+)\.(\d+)\s+', re.IGNORECASE)
CODE_FRAGMENT_OLD = re.compile(r'\bCode Fragment\s+[A-Z]\.\d+\b')
MISMATCH_H3_H4 = re.compile(r'<h3\b[^>]*>[^<]*</h4>')
MISMATCH_H4_H3 = re.compile(r'<h4\b[^>]*>[^<]*</h3>')
DUP_WHATS_NEXT = re.compile(r'<h2[^>]*>\s*What\s+Comes?\s+Next.*?</h2>.*?<div\s+class="[^"]*whats-next', re.DOTALL | re.IGNORECASE)
FUTURE_DATE = re.compile(r'\b(?:As of|by|in)\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+202(7|8|9|[1-9]\d)\b', re.IGNORECASE)


def find_bugs():
    findings = {
        'why_why': [],
        'table_prefix': [],
        'code_fragment_old': [],
        'mismatch_h3_h4': [],
        'mismatch_h4_h3': [],
        'dup_whats_next': [],
        'future_date': [],
    }

    html_files = []
    for part_dir in ROOT.glob('part-*'):
        if not part_dir.is_dir():
            continue
        for module_dir in part_dir.glob('module-*'):
            if not module_dir.is_dir():
                continue
            html_files.extend(module_dir.glob('section-*.html'))
            html_files.extend(module_dir.glob('index.html'))

    for f in html_files:
        try:
            text = f.read_text(encoding='utf-8')
        except Exception as e:
            continue
        rel = f.relative_to(ROOT)

        for m in WHY_WHY.finditer(text):
            line = text.count('\n', 0, m.start()) + 1
            findings['why_why'].append((str(rel), line, m.group(0)))

        for m in TABLE_PREFIX.finditer(text):
            line = text.count('\n', 0, m.start()) + 1
            findings['table_prefix'].append((str(rel), line, m.group(0)))

        for m in CODE_FRAGMENT_OLD.finditer(text):
            line = text.count('\n', 0, m.start()) + 1
            findings['code_fragment_old'].append((str(rel), line, m.group(0)))

        for m in MISMATCH_H3_H4.finditer(text):
            line = text.count('\n', 0, m.start()) + 1
            findings['mismatch_h3_h4'].append((str(rel), line, m.group(0)[:80]))

        for m in MISMATCH_H4_H3.finditer(text):
            line = text.count('\n', 0, m.start()) + 1
            findings['mismatch_h4_h3'].append((str(rel), line, m.group(0)[:80]))

        for m in DUP_WHATS_NEXT.finditer(text):
            line = text.count('\n', 0, m.start()) + 1
            findings['dup_whats_next'].append((str(rel), line, 'duplicate What Comes Next'))

        for m in FUTURE_DATE.finditer(text):
            line = text.count('\n', 0, m.start()) + 1
            findings['future_date'].append((str(rel), line, m.group(0)))

    return findings


def main():
    findings = find_bugs()
    total = sum(len(v) for v in findings.values())

    print(f"\n{'='*70}")
    print(f"Senior-Editor Bug Sweep: {total} total findings")
    print(f"{'='*70}\n")

    for cat, items in findings.items():
        if not items:
            continue
        print(f"\n## {cat} ({len(items)})")
        for rel, line, snippet in items[:50]:
            print(f"  {rel}:{line}  {snippet}")
        if len(items) > 50:
            print(f"  ... and {len(items)-50} more")

    return total


if __name__ == '__main__':
    main()
