"""8th edition Wave 23 / D-pass cleanup: v694 over-aggressively retagged
some `lang-text` Pygments blocks to `lang-python` based on the presence
of Python-keyword spans. But those blocks were tagged `lang-text`
originally because their extracted text isn't valid Python (e.g., lost
indentation, intentionally-elided snippets). The v661 AST validator then
fails on them.

Pragmatic fix: scan all `lang-python` blocks; if the extracted plain
text fails `ast.parse`, revert that block's tag to `lang-text`. The
visual coloring is preserved either way because Pygments span CSS is
scoped on `.pygments-highlighted`, not on the lang-X marker.

Idempotent.
"""
from __future__ import annotations
import ast
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/')

BLOCK_RE = re.compile(
    r'(<pre[^>]*>\s*<code\s+class="pygments-highlighted\s+)lang-python(">)'
    r'([\s\S]*?)(</code>\s*</pre>)',
    re.IGNORECASE)
SPAN_RE = re.compile(r'<span[^>]*>|</span>')


def extract_python(html_block: str) -> str:
    return html.unescape(SPAN_RE.sub('', html_block))


def is_parseable(code: str) -> bool:
    s = code.strip()
    if not s or s.startswith('...') or s.startswith('# ...'):
        return True
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False


def main() -> int:
    fix = '--fix' in sys.argv
    n_files = 0
    n_reverts = 0
    files_touched: list[str] = []
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        if 'lang-python' not in text:
            continue
        local = 0

        def repl(m: re.Match) -> str:
            nonlocal local
            head, tail, body, end = m.group(1), m.group(2), m.group(3), m.group(4)
            code = extract_python(body)
            if is_parseable(code):
                return m.group(0)
            local += 1
            return f'{head}lang-text{tail}{body}{end}'

        new = BLOCK_RE.sub(repl, text)
        if local:
            n_files += 1
            n_reverts += local
            files_touched.append(str(p.relative_to(ROOT)))
            if fix and new != text:
                p.write_text(new, encoding='utf-8')

    print(f'Files affected: {n_files}')
    print(f'Blocks reverted lang-python -> lang-text: {n_reverts}')
    if not fix:
        for f in files_touched[:20]:
            print(' ', f)
        if len(files_touched) > 20:
            print(f'  ... and {len(files_touched)-20} more')
        print('\nRe-run with --fix to apply.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
