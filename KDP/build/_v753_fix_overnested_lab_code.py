"""Fix the "over-nested post-return code" bug detected by v752.

Pattern (broken):
    def func(args):
        ...
        return X
        # comment              <-- inside function (unreachable)
        for x in items:        <-- inside function, but logically top-level
            X, y = [], []      <-- progressively deeper
            for y in others:
                ...

Fix algorithm:
  1. For each lang-python code block, find every `def NAME(...):` at
     indent N.
  2. Walk forward to find the function's `return` (or top of the next
     def, or end of block). The function body ends at the LAST line
     at indent > N.
  3. Examine all subsequent non-blank lines. If they all have indent
     >= body_indent (def_indent + 4) AND the indent never returns to
     def_indent within the block, AND the deepest indent grows beyond
     body_indent + 4, this is the over-nest signature.
  4. Dedent every post-function line by `body_indent` (the over-indent
     amount) so what was at body_indent goes to col 0 (top-level),
     body_indent+4 -> col 4, etc.

Safety:
  - Only apply when the deepest indent in the suspect region is
    body_indent + 8 or more. Shallow follow-on code that legitimately
    stays inside the function is left alone.
  - Skip if the function contains a NESTED def or class at body_indent.
  - Skip blocks where the suspect region contains another top-level
    statement (line at exactly def_indent), since the function scope
    has clearly already ended.
  - Operates on the plain-text view (spans stripped) to compute
    indent, then RE-TOKENIZES through Pygments to rebuild colored
    HTML. This avoids the complexity of stripping/re-adding spans
    line-by-line.
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
    r'(<pre[^>]*>\s*<code\s+class="[^"]*lang-python[^"]*">)([\s\S]*?)(</code>\s*</pre>)',
    re.IGNORECASE)
SPAN_RE = re.compile(r'<span[^>]*>|</span>')

LEXER = PythonLexer()
FORMATTER = HtmlFormatter(nowrap=True, classprefix='')


def extract_code(body: str) -> str:
    return html.unescape(SPAN_RE.sub('', body))


def fix_overnested(code: str) -> tuple[str, bool]:
    """Return (fixed_code, changed). Only fix obvious over-nest cases."""
    lines = code.split('\n')
    n = len(lines)
    changed = False
    # Find every def at the outermost indent in the block (likely col 0).
    out_lines: list[str] = []
    i = 0
    while i < n:
        line = lines[i]
        m = re.match(r'^(\s*)def\s+\w+', line)
        if not m:
            out_lines.append(line)
            i += 1
            continue
        def_indent = len(m.group(1))
        body_indent = def_indent + 4
        # Find end of function body: first non-blank line at indent <= def_indent
        # after at least one body line. Track deepest indent we see in body.
        j = i + 1
        last_body = i
        return_line: int | None = None
        deepest_in_body = body_indent
        found_nested_def_or_class = False
        while j < n:
            ln = lines[j]
            stripped = ln.strip()
            if not stripped:
                j += 1
                continue
            ln_indent = len(ln) - len(ln.lstrip())
            if ln_indent <= def_indent:
                # Function scope ended naturally
                break
            if ln_indent == body_indent and re.match(r'\s*(def|class)\s+\w+', ln):
                found_nested_def_or_class = True
            if ln_indent > deepest_in_body:
                deepest_in_body = ln_indent
            if return_line is None and re.match(r'\s+return(\s|$)', ln):
                return_line = j
            last_body = j
            j += 1
        if found_nested_def_or_class or return_line is None:
            # Skip: too complex to safely dedent
            for k in range(i, j):
                out_lines.append(lines[k])
            i = j
            continue
        # Now decide: are lines AFTER the return strongly over-nested?
        # Heuristic: if the deepest indent after the return is
        # >= body_indent + 8 AND no line after return drops to body_indent
        # without staying there (i.e., function body is "all the way down"),
        # apply the dedent.
        post_return = lines[return_line + 1 : last_body + 1]
        non_blank_post = [
            (k, ln) for k, ln in enumerate(post_return) if ln.strip()
        ]
        if not non_blank_post:
            for k in range(i, j):
                out_lines.append(lines[k])
            i = j
            continue
        # Compute the FIRST non-blank post-return line's indent. If it
        # equals body_indent (4) AND the deepest in the post-return is
        # >= body_indent + 8, this is over-nest.
        first_post_indent = len(post_return[non_blank_post[0][0]]) - len(post_return[non_blank_post[0][0]].lstrip())
        deepest_post = max(
            len(post_return[k]) - len(post_return[k].lstrip())
            for k, _ in non_blank_post
        )
        if first_post_indent < body_indent or deepest_post < body_indent + 8:
            # Not a clear over-nest; skip
            for k in range(i, j):
                out_lines.append(lines[k])
            i = j
            continue
        # SAFETY: require a TODO marker OR a "for X in Y" loop at the
        # FIRST non-blank post-return line that references a variable
        # not used in the function body. The TODO marker is the
        # strongest signal: it means the post-return is example code
        # that was meant to be top-level. Otherwise be conservative.
        first_post_ln = post_return[non_blank_post[0][0]]
        first_post_text = first_post_ln.strip()
        has_todo_marker = (
            first_post_text.startswith('#')
            and any(k in first_post_text.upper() for k in ('TODO', 'EXAMPLE', 'USAGE', 'DEMO'))
        )
        if not has_todo_marker:
            for k in range(i, j):
                out_lines.append(lines[k])
            i = j
            continue
        # Dedent post-return by first_post_indent (so col first_post_indent
        # -> col 0, col first_post_indent+4 -> col 4, etc.)
        dedent = first_post_indent
        # Output function body (i..return_line) unchanged
        for k in range(i, return_line + 1):
            out_lines.append(lines[k])
        # Blank line for visual separation
        out_lines.append('')
        # Dedented post-return code
        for ln in post_return:
            if not ln.strip():
                out_lines.append('')
            else:
                ln_indent = len(ln) - len(ln.lstrip())
                new_indent = max(0, ln_indent - dedent)
                out_lines.append(' ' * new_indent + ln.lstrip())
        changed = True
        i = last_body + 1
    return '\n'.join(out_lines), changed


def colorize(plain: str) -> str:
    leading = '\n' if plain.startswith('\n') else ''
    if leading:
        plain = plain[1:]
    trailing = '\n' if plain.endswith('\n') else ''
    if trailing:
        plain = plain[:-1]
    colored = highlight(plain, LEXER, FORMATTER).rstrip('\n')
    return f'{leading}{colored}{trailing}'


def main() -> int:
    fix = '--fix' in sys.argv
    files_touched = 0
    blocks_fixed = 0
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
        local_fixed = 0

        def repl(m: re.Match) -> str:
            nonlocal local_fixed
            head, body, tail = m.group(1), m.group(2), m.group(3)
            plain = extract_code(body)
            new_plain, changed = fix_overnested(plain)
            if not changed:
                return m.group(0)
            local_fixed += 1
            # Re-tokenize through Pygments to rebuild colored HTML
            try:
                colored = colorize(new_plain)
            except Exception:
                return m.group(0)
            return f'{head}{colored}{tail}'

        new = BLOCK_RE.sub(repl, text)
        if local_fixed:
            files_touched += 1
            blocks_fixed += local_fixed
            if fix:
                p.write_text(new, encoding='utf-8')

    mode = 'APPLIED' if fix else 'DRY-RUN'
    print(f'[{mode}] Files touched: {files_touched}')
    print(f'        Blocks fixed:  {blocks_fixed}')
    if not fix:
        print('\nRe-run with --fix to apply.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
