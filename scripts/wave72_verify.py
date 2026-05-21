"""Run the p2_callout_order audit on all section files and report
CALLOUT_ORDER hits."""
import sys
from pathlib import Path

ROOT = Path('E:/Projects/BookBlogsHome/LLMBook')
sys.path.insert(0, str(ROOT / 'agents' / 'book-skills' / 'scripts' / 'audit' / 'checks'))
import p2_callout_order

# Find all section files (not in tools-of-the-trade/appendices/KDP/build).
SKIP_HINTS = ('/tools-of-the-trade/', '/appendices/', '/appendix-',
              '/kdp/', '/build/')

def should_skip(p: Path) -> bool:
    s = str(p).lower().replace('\\', '/')
    if not p.name.startswith('section-'):
        return True
    return any(x in s for x in SKIP_HINTS)


files = [f for f in ROOT.rglob('section-*.html') if not should_skip(f)]
print(f'Sections scanned: {len(files)}')

all_issues = []
for fp in files:
    try:
        html = fp.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        continue
    issues = p2_callout_order.run(fp, html, {})
    all_issues.extend(issues)

print(f'CALLOUT_ORDER issues remaining: {len(all_issues)}')

# Pattern breakdown.
from collections import Counter
import re
patterns = Counter()
for i in all_issues:
    m = re.match(r'CALLOUT_ORDER: "(.+?)" appears after "(.+?)"', i.message)
    if m:
        patterns[(m.group(1), m.group(2))] += 1

if patterns:
    print()
    print('Remaining patterns:')
    for (a, b), c in patterns.most_common():
        print(f'  {c}x {a} after {b}')

# File-level list.
files_with_issues = {str(i.filepath) for i in all_issues}
print()
print(f'Unique files with remaining issues: {len(files_with_issues)}')
for f in sorted(files_with_issues):
    rel = f.replace(str(ROOT), '').lstrip('\\').lstrip('/')
    print(f'  {rel}')
