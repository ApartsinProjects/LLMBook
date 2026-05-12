"""v6.33: Audit trivial / placeholder / low-information code fragments.

A code block is "trivial" if any of:
  - 3 lines or fewer AND only assignments/imports
  - All lines are comments
  - Just `pass` or `# TODO`
  - Empty function/class definition with only `pass` or `...`
  - Single-line expression that's just a print() of a literal
  - Hello-world style: import, var = 1, print(var)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

trivial = []
for p in sorted(list(ROOT.glob('part-*/module-*/section-*.html')) +
                list(ROOT.glob('appendices/appendix-*/section-*.html'))):
    text = p.read_text(encoding='utf-8', errors='replace')
    rel = str(p.relative_to(ROOT)).replace('\\', '/')
    for i, m in enumerate(re.finditer(r'<pre>\s*<code[^>]*>(.+?)</code>\s*</pre>', text, re.DOTALL)):
        # strip Pygments spans
        code = re.sub(r'<[^>]+>', '', m.group(1))
        # decode entities
        code = (code.replace('&lt;', '<').replace('&gt;', '>')
                    .replace('&amp;', '&').replace('&quot;', '"'))
        lines = [l.rstrip() for l in code.split('\n') if l.strip()]
        n = len(lines)
        if n == 0:
            trivial.append((rel, i, 'empty', code[:80]))
            continue
        # All-comment block
        if all(l.lstrip().startswith('#') or l.lstrip().startswith('//') for l in lines):
            trivial.append((rel, i, 'all-comments', '\\n'.join(lines)[:80]))
            continue
        # Just `pass` or `...`
        if n <= 3 and all(re.match(r'\s*(pass|\.\.\.|return\s*$)', l) for l in lines):
            trivial.append((rel, i, 'pass-only', '\\n'.join(lines)[:80]))
            continue
        # Single trivial print
        if n == 1 and re.match(r'^\s*print\s*\(\s*[\'"][^\'"]*[\'"]\s*\)\s*$', lines[0]):
            trivial.append((rel, i, 'literal-print', lines[0][:80]))
            continue
        # Just imports
        if all(re.match(r'^\s*(import|from)\s+', l) for l in lines):
            trivial.append((rel, i, 'imports-only', '\\n'.join(lines)[:80]))
            continue
        # Hello-world: <=4 lines, all simple assignments + print
        if n <= 4 and all(re.match(r'^\s*(\w+\s*=\s*[\d\'\"]+|print\s*\(|import\s)', l)
                          for l in lines):
            trivial.append((rel, i, 'hello-world', '\\n'.join(lines)[:80]))

print(f'{len(trivial)} trivial code blocks:\n')
from collections import Counter
by_kind = Counter(t[2] for t in trivial)
for kind, n in by_kind.most_common():
    print(f'  {kind}: {n}')

print('\nExamples:')
for rel, i, kind, snip in trivial[:15]:
    print(f'  [{kind}] {rel} block #{i}')
    print(f'    {snip[:100]}')
