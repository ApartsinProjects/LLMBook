"""v808: Fix mislabeled `lang-text` code blocks that are actually
Python. The 0.3.1.3 broadcasting example uses `import torch`,
`torch.ones`, etc. — clearly Python but classed as lang-text.

HEURISTIC
=========
A `<pre><code class="... lang-text ...">` block is likely Python if
its content contains 2+ Python idioms:
  - `import ` at line start
  - `from ` ... `import `
  - `def ` ... `:`
  - `torch.`, `nn.`, `np.`
  - `print(` or `assert `
  - `for ` ... `in ` ... `:`

For each such block, change `lang-text` → `lang-python`. The
pygments hook at build time will then color it correctly.

Skip blocks that are CLI output (start with `$`, `>>>`, `$ `, etc.).
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
SKIP = ['node_modules', '.git', 'output', 'backup', 'agents/', 'templates/',
        'KDP/build', 'KDP/html2epub', 'pagefind']


def is_skip(p):
    sp = str(p).replace('\\', '/')
    return any(s in sp for s in SKIP)


def looks_like_python(code: str) -> bool:
    """Return True if the code block content looks like Python."""
    text = code.lower()
    indicators = 0
    if re.search(r'\bimport\s+\w', code):
        indicators += 1
    if re.search(r'\bfrom\s+\w+\s+import\b', code):
        indicators += 1
    if re.search(r'\bdef\s+\w+\(.*\):', code):
        indicators += 1
    if re.search(r'\btorch\.\w+|\bnn\.\w+|\bnp\.\w+', code):
        indicators += 1
    if re.search(r'\bprint\s*\(', code):
        indicators += 1
    if re.search(r'\bfor\s+\w+\s+in\s+.*:', code):
        indicators += 1
    if re.search(r'\bassert\s+\w', code):
        indicators += 1
    if re.search(r'^\s*#\s', code, re.MULTILINE):  # Python comment
        indicators += 1
    # Disqualify if starts with shell prompt
    if re.match(r'^\s*[\$>][ ]', code):
        return False
    return indicators >= 2


n_files = 0
n_blocks = 0

CODE_BLOCK_RE = re.compile(
    r'<pre><code\s+class="([^"]*)\blang-text\b([^"]*)">([^<]+)</code></pre>',
    re.DOTALL
)


def replace(m):
    global n_blocks
    classes_before = m.group(1).strip()
    classes_after = m.group(2).strip()
    code = m.group(3)
    if not looks_like_python(code):
        return m.group(0)
    # Build new class string
    parts = [c for c in classes_before.split() if c] + ['lang-python'] + \
            [c for c in classes_after.split() if c]
    new_classes = ' '.join(dict.fromkeys(parts))  # dedupe but preserve order
    n_blocks += 1
    return f'<pre><code class="{new_classes}">{code}</code></pre>'


for p in ROOT.rglob('*.html'):
    if is_skip(p):
        continue
    try:
        s = p.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue
    orig = s
    s = CODE_BLOCK_RE.sub(replace, s)
    if s != orig:
        p.write_text(s, encoding='utf-8')
        n_files += 1

print(f'Relabeled {n_blocks} lang-text -> lang-python blocks across {n_files} files.')
