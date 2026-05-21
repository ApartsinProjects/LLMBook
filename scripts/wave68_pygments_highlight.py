"""Wave 68: Run Pygments over code blocks that have the `pygments-highlighted
lang-X` class but lack the <span class="..."> tokens (i.e., the class was set
but the code text never went through the highlighter).

Strategy:
  1. Find <pre><code class="pygments-highlighted lang-LANG">CODE</code></pre>
     where CODE contains no <span class= tags.
  2. Decode HTML entities in CODE back to raw text (Python strings, etc.).
  3. Run Pygments with the matching lexer.
  4. Splice the highlighted output back in.

Handles common languages: python, bash, sh, yaml, json, javascript, text.
"""
import html
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

from pygments import highlight
from pygments.lexers import (
    PythonLexer, BashLexer, YamlLexer, JsonLexer, JavascriptLexer, TextLexer,
)
from pygments.formatters import HtmlFormatter

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

LEXERS = {
    'python': PythonLexer(),
    'py': PythonLexer(),
    'bash': BashLexer(),
    'sh': BashLexer(),
    'shell': BashLexer(),
    'yaml': YamlLexer(),
    'yml': YamlLexer(),
    'json': JsonLexer(),
    'javascript': JavascriptLexer(),
    'js': JavascriptLexer(),
}

# Match <pre><code class="pygments-highlighted lang-LANG"...>CODE</code></pre>
# where CODE contains no <span class= tag.
PRE_CODE_RE = re.compile(
    r'(<pre[^>]*><code\s+class="pygments-highlighted\s+lang-(\w+)"[^>]*>)'
    r'([\s\S]*?)'
    r'(</code></pre>)',
    re.IGNORECASE,
)

# HtmlFormatter without wrapping in a <div class="highlight"><pre>...
FORMATTER = HtmlFormatter(nowrap=True, classprefix='')


def fix_file(p: Path) -> int:
    text = p.read_text(encoding='utf-8')
    orig = text
    n = 0

    def repl(m: re.Match) -> str:
        nonlocal n
        prefix = m.group(1)
        lang = m.group(2).lower()
        code = m.group(3)
        suffix = m.group(4)

        # Already highlighted (has spans)? skip
        if '<span class=' in code:
            return m.group()

        lexer = LEXERS.get(lang)
        if not lexer:
            return m.group()  # unknown lang, leave alone

        # Decode HTML entities to raw code text
        raw = html.unescape(code)
        # Strip leading/trailing newlines (Pygments adds its own)
        raw = raw.strip('\n')
        if not raw:
            return m.group()

        try:
            highlighted = highlight(raw, lexer, FORMATTER)
        except Exception:
            return m.group()

        # Pygments wraps in newlines; trim once
        highlighted = highlighted.rstrip('\n')
        n += 1
        return prefix + highlighted + suffix

    new_text = PRE_CODE_RE.sub(repl, text)
    if new_text != orig:
        p.write_text(new_text, encoding='utf-8')
    return n


def main():
    n_total = 0
    files_touched = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        n = fix_file(p)
        if n > 0:
            n_total += n
            files_touched += 1
    print(f'Pygments-highlighted: {n_total} code blocks across {files_touched} files')


if __name__ == '__main__':
    main()
