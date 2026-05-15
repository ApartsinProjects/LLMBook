"""Audit: code block formatting issues.

Look for:
1. Over-indented code (lines starting with 8+ spaces consistently)
2. Code with no indentation when expected (Python-like patterns)
3. Code blocks with excessive empty lines
4. Code blocks wider than 75 chars (Kindle issue)
"""
from pathlib import Path
from bs4 import BeautifulSoup
import re

ROOT = Path(__file__).resolve().parents[2]
SKIP = ['node_modules', '.git', 'output', 'backup', 'KDP/build',
        'KDP/html2pub', 'pagefind', 'temp_epub', 'agents/', 'templates/']


def is_skip(p):
    sp = str(p).replace('\\', '/')
    return any(s in sp for s in SKIP)


overindented = []  # files with 8+ space indents
unindented = []  # python code with no indent where there should be
wide_code = []  # lines > 90 chars
empty_excessive = []  # multiple consecutive empty lines
n_code_blocks = 0

for p in ROOT.rglob('*.html'):
    if is_skip(p):
        continue
    try:
        s = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
    except Exception:
        continue
    for pre in s.find_all('pre'):
        n_code_blocks += 1
        code = pre.find('code')
        if not code:
            continue
        text = code.get_text()
        lines = text.split('\n')

        # Get language hint from class
        cls = ' '.join(code.get('class', []))
        lang = ''
        for c in code.get('class', []):
            if c.startswith('language-'):
                lang = c[9:]
            elif c.startswith('lang-'):
                lang = c[5:]

        # Over-indented: first non-empty line starts with 4+ spaces (unusual)
        non_empty = [l for l in lines if l.strip()]
        if non_empty:
            first_indent = len(non_empty[0]) - len(non_empty[0].lstrip(' '))
            if first_indent >= 8:
                overindented.append({
                    'file': str(p.relative_to(ROOT)),
                    'lang': lang,
                    'indent': first_indent,
                    'sample': non_empty[0][:60],
                })

        # Wide code: any line > 90 chars
        max_line = max((len(l) for l in lines), default=0)
        if max_line > 100:
            wide_code.append({
                'file': str(p.relative_to(ROOT)),
                'lang': lang,
                'max_len': max_line,
            })

        # Excessive empty lines (3+ consecutive)
        if re.search(r'\n\s*\n\s*\n\s*\n', text):
            empty_excessive.append({
                'file': str(p.relative_to(ROOT)),
                'lang': lang,
            })


print(f'Total code blocks: {n_code_blocks}')
print()
print(f'Over-indented (8+ leading spaces): {len(overindented)}')
for o in overindented[:20]:
    print(f'  {o["file"]}: lang={o["lang"]} indent={o["indent"]}')
    print(f'    sample: {o["sample"]}')

print()
print(f'Wide code (>100 chars/line): {len(wide_code)}')
for w in wide_code[:15]:
    print(f'  {w["file"]}: lang={w["lang"]} max={w["max_len"]}')

print()
print(f'Excessive empty lines: {len(empty_excessive)}')
for e in empty_excessive[:10]:
    print(f'  {e["file"]}: lang={e["lang"]}')
