"""v6.34: Audit code formatting inside library-shortcut callouts."""
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
issues = []
total = 0

for p in sorted(ROOT.glob('part-*/module-*/section-*.html')):
    text = p.read_text(encoding='utf-8', errors='replace')
    for m in re.finditer(
        r'<div class="callout library-shortcut">(.*?)</div>\s*</div>',
        text, re.DOTALL,
    ):
        block = m.group(1)
        for cm in re.finditer(r'<pre><code[^>]*>(.+?)</code></pre>', block, re.DOTALL):
            total += 1
            code = re.sub(r'<[^>]+>', '', cm.group(1))
            code = (code.replace('&lt;', '<').replace('&gt;', '>')
                        .replace('&amp;', '&').replace('&quot;', '"'))
            lines = code.split('\n')
            n = len(lines)
            has_comment = any(l.lstrip().startswith('#') for l in lines)
            long_lines = [l for l in lines if len(l) > 120]
            non_blank = [l for l in lines if l.strip()]
            no_breathing = n > 6 and len(non_blank) == n
            mixed_indent = any('\t' in l for l in lines) and any(
                l.startswith(' ') for l in lines)
            problems = []
            if not has_comment and n > 4:
                problems.append('no-comments')
            if long_lines:
                problems.append(f'{len(long_lines)}-long-lines')
            if no_breathing:
                problems.append('no-blank-lines')
            if mixed_indent:
                problems.append('mixed-tabs-spaces')
            if problems:
                rel = str(p.relative_to(ROOT)).replace('\\', '/')
                issues.append((rel, problems, code[:200]))

print(f'Total library-shortcut code blocks: {total}')
print(f'Blocks with formatting issues:      {len(issues)}\n')

all_issues = Counter()
for _, ps, _ in issues:
    for prob in ps:
        all_issues[prob.split('-', 1)[0] if prob[0].isdigit() else prob] += 1
for k, v in all_issues.most_common():
    print(f'  {k}: {v}')

print('\nFirst 10 examples:')
for rel, problems, snip in issues[:10]:
    print(f'  {rel}  [{",".join(problems)}]')
    print(f'    {snip[:150].replace(chr(10), " | ")}')
