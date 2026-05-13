"""8th edition: detect <code class="pygments-highlighted lang-text"> blocks
whose CONTENT is actually highlighted Python (contains Pygments span markup
like <span class="k">def</span>, <span class="kn">import</span>, etc.).

Symptom: even after pygments.css is linked, lang-text blocks may inherit
generic styling that suppresses color (some themes scope color rules to
specific languages or use lang-text as a "deliberately plain" marker).

Even where the colors do render, lang-text is semantically wrong: a
screen reader or future tooling that filters by language would miss the
block. Re-tagging to lang-python is the right fix.

Heuristic for "this is really Python": the code body contains at least
two distinct Pygments span classes that are characteristic of Python
parsing (e.g., span class="k">, <span class="kn">, <span class="nf">,
<span class="bp">, <span class="fm">, <span class="nd">). Plain text
through the Pygments text lexer would have only .w (whitespace) and .err.

Fix mode (--fix): replace `lang-text` with `lang-python` ONLY in those
matching <pre><code> blocks (leave true plain-text blocks alone).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/')

# Distinctive Python Pygments span classes
PY_CLASSES = ('class="k"', 'class="kn"', 'class="nf"', 'class="bp"',
              'class="fm"', 'class="nd"', 'class="nc"', 'class="kc"',
              'class="ow"', 'class="se"', 'class="s2"', 'class="s1"',
              'class="sd"', 'class="kt"', 'class="kr"')

BLOCK_PAT = re.compile(
    r'(<code\s+class="pygments-highlighted\s+)lang-text(">)(.*?)(</code>)',
    re.DOTALL)


def is_python_body(body: str) -> bool:
    distinct = sum(1 for c in PY_CLASSES if c in body)
    return distinct >= 2


def main() -> int:
    fix = '--fix' in sys.argv
    n_blocks_total = 0
    n_blocks_python = 0
    n_files_changed = 0
    changed_paths: list[str] = []
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        if 'lang-text' not in text:
            continue
        local_blocks = 0
        local_python = 0

        def repl(m: re.Match) -> str:
            nonlocal local_blocks, local_python
            local_blocks += 1
            head, tail, body, end = m.group(1), m.group(2), m.group(3), m.group(4)
            if is_python_body(body):
                local_python += 1
                return f'{head}lang-python{tail}{body}{end}'
            return m.group(0)

        new = BLOCK_PAT.sub(repl, text)
        n_blocks_total += local_blocks
        n_blocks_python += local_python
        if fix and new != text:
            p.write_text(new, encoding='utf-8')
            n_files_changed += 1
            changed_paths.append(str(p.relative_to(ROOT)))
        elif not fix and local_python:
            print(f'  {local_python}/{local_blocks} blocks: {p.relative_to(ROOT)}')

    print(f'\nTotal lang-text blocks scanned: {n_blocks_total}')
    print(f'Identified as Python (would re-tag): {n_blocks_python}')
    if fix:
        print(f'Files re-tagged: {n_files_changed}')
    else:
        print('Re-run with --fix to apply.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
