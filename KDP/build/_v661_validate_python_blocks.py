"""Wave 15: validate every Python <pre><code> block parses with ast.parse.

Root cause for D4/D41: an early "Pygments highlighter wrapper" stage
inserted progressive over-indentation around method bodies, making the
class definitions unparseable as Python. Several flagship "from-scratch"
examples in the production chapters (CircuitBreaker, TokenBucket,
PromptRegistry, ABExperiment, FastAPI streaming endpoint, Secure-
AgentExecutor) ship as broken Python.

This script extracts every <pre><code class="lang-python"> or
<pre><code class="pygments-highlighted lang-python"> block, strips
Pygments span tags + decodes HTML entities, and feeds the result to
ast.parse(). Reports every parse error with file:line context.
Idempotent. Exit 1 on any failure.
"""
from __future__ import annotations
import ast
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/')

# Match a python code block (with or without Pygments)
BLOCK_RE = re.compile(
    r'<pre[^>]*>\s*<code[^>]*\b(?:lang|language)-python\b[^>]*>([\s\S]*?)</code>\s*</pre>',
    re.IGNORECASE,
)
SPAN_RE = re.compile(r'<span[^>]*>|</span>')


def extract_python(html_block: str) -> str:
    """Strip Pygments span tags + decode HTML entities to recover plain Python."""
    no_spans = SPAN_RE.sub('', html_block)
    return html.unescape(no_spans)


def line_of(text: str, idx: int) -> int:
    return text.count('\n', 0, idx) + 1


def main() -> int:
    n_blocks = 0
    n_errors = 0
    n_files_with_err = 0

    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue

        local = []
        for m in BLOCK_RE.finditer(text):
            n_blocks += 1
            block_html = m.group(1)
            code = extract_python(block_html)
            # Skip blocks that are clearly snippets (no statements / partial)
            stripped = code.strip()
            if not stripped or stripped.startswith('...') or stripped.startswith('# ...'):
                continue
            try:
                ast.parse(code)
            except SyntaxError as e:
                line = line_of(text, m.start()) + (e.lineno or 1) - 1
                msg = f'{type(e).__name__}: {e.msg} (offending line {e.lineno})'
                local.append((line, msg, code.split('\n')[(e.lineno or 1) - 1][:80] if e.lineno else ''))

        if local:
            n_files_with_err += 1
            n_errors += len(local)
            rel = p.relative_to(ROOT)
            for line, msg, snip in sorted(local):
                print(f'{rel}:{line}  {msg}')
                if snip:
                    safe = ''.join(c if 32 <= ord(c) < 127 else '?' for c in snip)
                    print(f'    line text: {safe!r}')

    print()
    print(f'Validated {n_blocks} Python blocks. Errors: {n_errors} across {n_files_with_err} file(s).')
    return 1 if n_errors else 0


if __name__ == '__main__':
    sys.exit(main())
