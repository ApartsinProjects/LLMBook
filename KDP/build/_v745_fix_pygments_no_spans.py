"""Fix Bug C: <pre><code class="pygments-highlighted lang-python"> blocks
that have the wrapper class but no <span> tokens inside. The content
is plain text; syntax coloring is missing.

Strategy:
- For each affected block, extract the plain Python text.
- Re-tokenize it through Pygments with the same HTMLFormatter
  configuration the rest of the book uses (nowrap=True, classprefix='').
- Substitute the colored HTML back into the <pre><code> block.

Idempotent: only acts on blocks that currently have NO <span> tags.
Skip blocks that already have spans (already correctly highlighted).

Encoding caveats:
- Pygments output uses HTML entities for &, <, >. Pre-existing
  &amp;, &lt;, &gt; in the block become &amp;amp; etc. after pygments
  if we naively pass them through. So we html.unescape first, then
  re-encode through Pygments. The result matches what the v60-era
  build pipeline produced.
"""
from __future__ import annotations
import html
import re
import sys
from pathlib import Path

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/')

BLOCK_RE = re.compile(
    r'(<pre[^>]*>\s*<code\s+class="pygments-highlighted\s+lang-python">)'
    r'([\s\S]*?)'
    r'(</code>\s*</pre>)',
    re.IGNORECASE)

LEXER = PythonLexer()
# nowrap=True: emit only the span tokens, no surrounding <div class="highlight">
FORMATTER = HtmlFormatter(nowrap=True, classprefix='')


def has_spans(body: str) -> bool:
    return '<span' in body


def colorize(plain: str) -> str:
    """Run Pygments on plain text; preserve leading/trailing newlines."""
    # Pygments strips trailing newline. Preserve.
    leading = ''
    if plain.startswith('\n'):
        leading = '\n'
        plain = plain[1:]
    trailing = ''
    if plain.endswith('\n'):
        trailing = '\n'
        plain = plain[:-1]
    colored = highlight(plain, LEXER, FORMATTER)
    # Pygments adds a trailing newline; collapse multiple trailing newlines
    colored = colored.rstrip('\n')
    return f'{leading}{colored}{trailing}'


def main() -> int:
    fix = '--fix' in sys.argv
    files_touched = 0
    blocks_recolored = 0
    skipped_unparseable = 0
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        if 'pygments-highlighted' not in text:
            continue

        local = 0
        local_skipped = 0

        def repl(m: re.Match) -> str:
            nonlocal local, local_skipped
            head, body, tail = m.group(1), m.group(2), m.group(3)
            if has_spans(body):
                return m.group(0)
            plain = html.unescape(body)
            if not plain.strip():
                return m.group(0)
            try:
                colored = colorize(plain)
            except Exception:
                local_skipped += 1
                return m.group(0)
            local += 1
            return f'{head}{colored}{tail}'

        new = BLOCK_RE.sub(repl, text)
        if local:
            files_touched += 1
            blocks_recolored += local
            if fix and new != text:
                p.write_text(new, encoding='utf-8')
        skipped_unparseable += local_skipped

    mode = 'APPLIED' if fix else 'DRY-RUN'
    print(f'[{mode}] Files touched: {files_touched}')
    print(f'        Blocks re-colored: {blocks_recolored}')
    if skipped_unparseable:
        print(f'        Blocks skipped (pygments error): {skipped_unparseable}')
    if not fix:
        print('\nRe-run with --fix to apply.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
