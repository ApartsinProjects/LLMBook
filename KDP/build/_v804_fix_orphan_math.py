"""v804: Convert 3 orphan inline math spans (alone on a line)
to display math blocks. Author wrote them as <span class="math">
but they were standalone between paragraphs, so reader rendered
them inline + left-aligned. Wrap in <div class="math-block"> with
$$...$$ delimiters so they become display math (centered).
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]

ORPHANS = [
    'part-1-foundations/module-00-ml-pytorch-foundations/section-0.2.html',
    'part-1-foundations/module-00-ml-pytorch-foundations/section-0.4.html',
    'part-1-foundations/module-03-sequence-models-attention/section-3.3.html',
]

n_fixed = 0
for rel in ORPHANS:
    fp = ROOT / rel
    if not fp.exists():
        print(f'  MISSING: {rel}')
        continue
    s = fp.read_text(encoding='utf-8')
    # Convert <span class="math">$...$</span> alone on a line to
    # <div class="math-block">$$...$$</div>
    def repl(m):
        indent = m.group(1)
        tex = m.group(2)  # includes the $...$
        # Strip outer dollars and re-wrap with $$
        inner = tex.strip()
        if inner.startswith('$') and inner.endswith('$') and not inner.startswith('$$'):
            inner = inner[1:-1]  # strip $...$
        return f'{indent}<div class="math-block">$${inner}$$</div>'
    new_s, n = re.subn(
        r'^(\s*)<span class="math">(\$[^<]+\$)</span>\s*$',
        repl,
        s, flags=re.MULTILINE
    )
    if new_s != s:
        fp.write_text(new_s, encoding='utf-8')
        n_fixed += n
        print(f'  CONVERTED in {rel}  ({n} occurrences)')

print(f'\nTotal orphan math spans converted to display math: {n_fixed}')
