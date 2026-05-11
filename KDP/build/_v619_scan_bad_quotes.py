"""Find HTML files with unescaped " inside attribute values."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
problems = []
for p in ROOT.rglob('*.html'):
    sp = str(p).replace('\\', '/')
    if any(x in sp for x in ['node_modules', '.git/', 'pagefind/', 'KDP/build/']):
        continue
    try:
        text = p.read_text(encoding='utf-8', errors='replace')
    except Exception:
        continue
    # Find tag spanning one line; require an attribute pattern like  ="X""..."
    # where the second " starts a stray word/phrase, then more " and more attrs.
    for m in re.finditer(r'<[a-zA-Z]+\s+[^<>]*?/?>', text):
        tag = m.group(0)
        # Look for: ="prefix"WORD"suffix" — three quote pairs surrounding loose word
        if re.search(r'="[^"]*"\s*[A-Za-z][A-Za-z0-9 /,;:.\-]+"[^"]*"', tag):
            line = text[:m.start()].count('\n') + 1
            problems.append((sp, line, tag[:200]))

print(f'Found {len(problems)} potentially-malformed tags:')
for sp, line, tag in problems[:50]:
    print(f'  {sp}:{line}')
    print(f'    {tag}')
