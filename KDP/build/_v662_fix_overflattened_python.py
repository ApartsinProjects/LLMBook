"""Wave 15: auto-fix Python <pre><code> blocks where compound statement
bodies were flattened to the parent's indent level.

For each block that fails ast.parse, walk through and find lines starting
with a compound-statement keyword (def/class/for/if/while/with/try/elif/
else/except/finally) whose immediately following lines are at the SAME or
LESS indent than itself. Indent each such "body" line +4 spaces until the
indent level exceeds the parent. Iterate until ast.parse succeeds (or
heuristic gives up).

If the auto-fix produces parseable code, replaces the original block with
a clean `<pre><code class="lang-python">{corrected}</code></pre>` (no
Pygments markup, since re-running Pygments here is overkill and the
existing Pygments was the source of the bug). Else leaves the block
alone and reports.

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
        'templates/', '_archive/', 'temp_epub/')

BLOCK_RE = re.compile(
    r'(<pre[^>]*>\s*<code[^>]*\b(?:lang|language)-python\b[^>]*>)([\s\S]*?)(</code>\s*</pre>)',
    re.IGNORECASE,
)
SPAN_RE = re.compile(r'<span[^>]*>|</span>')

COMPOUND_KEYWORDS = ('def ', 'async def ', 'class ', 'for ', 'async for ',
                     'while ', 'if ', 'elif ', 'else:', 'try:', 'except',
                     'finally:', 'with ', 'async with ')


def extract_python(html_block: str) -> str:
    no_spans = SPAN_RE.sub('', html_block)
    return html.unescape(no_spans)


def indent_of(line: str) -> int:
    return len(line) - len(line.lstrip(' '))


def is_compound_header(stripped: str) -> bool:
    return any(stripped.startswith(kw) for kw in COMPOUND_KEYWORDS) and stripped.rstrip().endswith(':')


def try_fix(code: str, max_passes: int = 8) -> str | None:
    """Try to indent the bodies of compound statements that lost their indent.
    Returns the fixed code if ast.parse succeeds, else None."""
    for _pass in range(max_passes):
        try:
            ast.parse(code)
            return code
        except (SyntaxError, IndentationError):
            pass
        lines = code.split('\n')
        out = list(lines)
        changed = False
        for i, line in enumerate(lines):
            stripped = line.lstrip(' ')
            if not stripped or stripped.startswith('#'):
                continue
            if not is_compound_header(stripped):
                continue
            parent_indent = indent_of(line)
            # Find next non-blank/non-comment line
            j = i + 1
            while j < len(lines) and (not lines[j].strip() or lines[j].lstrip(' ').startswith('#')):
                j += 1
            if j >= len(lines):
                continue
            child = lines[j]
            child_indent = indent_of(child)
            if child_indent > parent_indent:
                continue  # already correctly indented
            # Body lost indent. Indent every line from j until indent drops below
            # parent_indent (or we hit EOF).
            target_indent = parent_indent + 4
            extra = target_indent - child_indent
            if extra <= 0:
                continue
            k = j
            while k < len(lines):
                kline = lines[k]
                kstripped = kline.strip()
                if not kstripped:
                    k += 1
                    continue
                kindent = indent_of(kline)
                # Stop when we see a sibling-or-shallower statement
                # (after the body started)
                if kindent < child_indent:
                    break
                # If this line starts with a compound keyword AT child_indent,
                # it's a sibling within the body, treat as part of body.
                out[k] = ' ' * extra + kline
                k += 1
            changed = True
            code = '\n'.join(out)
            break  # restart loop; one fix per pass
        if not changed:
            return None
    # Final attempt
    try:
        ast.parse(code)
        return code
    except Exception:
        return None


def main() -> int:
    n_fixed = 0
    n_unfixable = 0
    n_files_changed = 0
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        new_chunks = []
        last = 0
        local_fixes = 0
        local_unfix = []
        for m in BLOCK_RE.finditer(text):
            block_html = m.group(2)
            code = extract_python(block_html)
            stripped = code.strip()
            if not stripped or stripped.startswith('...') or stripped.startswith('# ...'):
                continue
            try:
                ast.parse(code)
                continue  # already parses
            except (SyntaxError, IndentationError):
                pass
            fixed = try_fix(code)
            if fixed is None:
                local_unfix.append((m.start(), code[:60]))
                continue
            # Replace the block with a clean <pre><code> using the fixed code
            new_block = (f'<pre><code class="language-python">'
                         f'{html.escape(fixed.rstrip())}'
                         f'</code></pre>')
            new_chunks.append(text[last:m.start()])
            new_chunks.append(new_block)
            last = m.end()
            local_fixes += 1
        new_chunks.append(text[last:])
        if local_fixes > 0:
            new_text = ''.join(new_chunks)
            p.write_text(new_text, encoding='utf-8')
            n_files_changed += 1
            n_fixed += local_fixes
            print(f'  fixed {local_fixes} block(s): {p.relative_to(ROOT)}')
        for offset, snip in local_unfix:
            n_unfixable += 1
            line = text[:offset].count('\n') + 1
            print(f'  UNFIX {p.relative_to(ROOT)}:{line}  starts: {snip!r}')
    print(f'\nFixed {n_fixed} blocks across {n_files_changed} files; {n_unfixable} unfixable.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
