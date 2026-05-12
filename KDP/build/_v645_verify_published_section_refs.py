"""Verify the v6.41 'Section X.Y' bare-text fix held across the published book.

Looks for any 'Section N.M' appearing as bare prose (outside <a> tags) in a
context that suggests broken substitution, with broader pattern matching
than v641b."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/validation/')

# Words that legitimately precede "Section N.M" as a cross-reference
LEGIT = {
    'see', 'in', 'from', 'where', 'when', 'while', 'and', 'or', 'is', 'as',
    'before', 'after', 'covered', 'shown', 'cited', 'introduced', 'discussed',
    'reference', 'review', 'recall', 'revisit', 'subsection', 'chapter',
    'section', 'sub', 'per', 'via', 'inspired', 'detailed', 'explained',
    'mentioned', 'returned', 'returns', 'across', 'beyond', 'until', 'than',
    'discussed', 'described', 'follows', 'follow', 'figure', 'table', 'recap',
    'check', 'verify', 'compare', 'pair', 'paired', 'previously', 'recall',
    'review', 'reviewing', 'overview', 'using', 'similar', 'unlike', 'like',
    'between', 'against', 'further', 'building', 'extends', 'extending',
    'parallel', 'now', 'see', 'visit', 'returns', 'returned', 'reviewing',
}

hits = []
for p in ROOT.rglob('*.html'):
    sp = str(p).replace('\\', '/')
    if any(s in sp for s in SKIP):
        continue
    try:
        text = p.read_text(encoding='utf-8', errors='replace')
    except Exception:
        continue
    stripped = re.sub(r'<a\b[^>]*>.*?</a>', '', text, flags=re.DOTALL)
    for m in re.finditer(r'\b(\w+)\s+Section\s+(\d+)\.(\d+)\b', stripped):
        prev = m.group(1).lower()
        if prev in LEGIT:
            continue
        ctx_start = max(0, m.start() - 40)
        ctx_end = min(len(stripped), m.end() + 50)
        ctx = stripped[ctx_start:ctx_end].replace('\n', ' ')
        hits.append((sp, ctx))

print(f'Potentially broken bare Section refs: {len(hits)}')
for f, c in hits[:15]:
    print(f'  {f}')
    print(f'    ...{c}...')
