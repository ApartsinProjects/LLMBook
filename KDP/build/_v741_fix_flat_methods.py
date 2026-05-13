"""Fix Bug A: class methods at column 0 that should be indented inside
the class scope.

Pattern (broken):
    class FeedForward(nn.Module):
        \"\"\"docstring\"\"\"
    def __init__(self, config):       <-- BUG: should be indented
        self.fc = ...

Fix:
    class FeedForward(nn.Module):
        \"\"\"docstring\"\"\"
        def __init__(self, config):   <-- 4-space indent added
            self.fc = ...             <-- 4-space indent added to body too

Algorithm:
1. Find every <pre><code class="...lang-python..."> block.
2. Extract the plain Python (strip <span> tags).
3. Walk lines; when inside a "class X:" scope (tracked by class line at
   col 0 + indented body), find any line at col 0 starting with `def `
   or `@` (decorator) or `async def `: those are buggy.
4. For each bug stretch (the def and its body until next col-0 def or
   end of class scope), add 4-space prefix to every line.
5. Re-emit the block. If the block was originally <span>-styled, we
   would need to re-tokenize through Pygments. To avoid that complexity,
   only operate on blocks where the body has NO <span> tags (i.e., the
   block is already plain text inside a pygments wrapper, Bug C
   territory) OR where the block has the bug AND is small enough that
   we can identify it by examining the rendered text and rewriting
   verbatim.

For safety in this first pass: only fix blocks WITHOUT <span> tags
(plain text inside pygments wrapper, ~668 blocks total, of which 147
have flat methods). Spans-styled blocks would need re-tokenization
which is risky.

Idempotent: only acts when the bug is present.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/')

BLOCK_RE = re.compile(
    r'(<pre[^>]*>\s*<code\s+class="[^"]*lang-python[^"]*">)([\s\S]*?)(</code>\s*</pre>)',
    re.IGNORECASE)


def has_spans(body: str) -> bool:
    return '<span' in body


def fix_flat_methods(code: str) -> tuple[str, int]:
    """Return (fixed_code, number_of_def_lines_indented)."""
    lines = code.split('\n')
    out: list[str] = []
    n_fixed = 0
    in_class = False
    fixing_method = False
    for line in lines:
        stripped = line.rstrip('\n')
        # Track class scope
        if re.match(r'^class\s+\w+', stripped):
            in_class = True
            fixing_method = False
            out.append(stripped)
            continue

        # Lines starting at col 0 with letter or @ but not "class" end the class scope
        # UNLESS they're a "def" inside a class that we're about to fix.
        if in_class and re.match(r'^(def\s+\w+|async\s+def\s+\w+|@\w+)', stripped):
            # BUG: method def at col 0 inside class scope
            fixing_method = True
            n_fixed += 1
            out.append('    ' + stripped)
            continue

        # If we're mid-fixing a method body, indent its lines too
        if fixing_method:
            if stripped == '':
                out.append('')
                continue
            # Body line: if at col 0, fix doesn't apply (could be next top-level)
            # If at col 4+, this is already-indented body, add 4 more spaces.
            if re.match(r'^[ \t]', stripped):
                out.append('    ' + stripped)
                continue
            # Hit a col-0 line that's not a def/decorator: class scope ended
            fixing_method = False
            in_class = False
            out.append(stripped)
            continue

        # Outside class or inside class body line not needing fix
        if in_class:
            # Check if this line is at col 0 and not a comment/decorator: ends class
            if re.match(r'^[a-zA-Z]', stripped) and not re.match(r'^(class|def|async|@)', stripped):
                in_class = False
            out.append(stripped)
        else:
            out.append(stripped)

    return '\n'.join(out), n_fixed


def main() -> int:
    fix = '--fix' in sys.argv
    files_touched = 0
    blocks_fixed = 0
    methods_indented = 0
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

        local_fixed_blocks = 0
        local_methods = 0

        def repl(m: re.Match) -> str:
            nonlocal local_fixed_blocks, local_methods
            head, body, tail = m.group(1), m.group(2), m.group(3)
            if has_spans(body):
                return m.group(0)  # skip span-styled blocks
            new_body, n = fix_flat_methods(body)
            if n > 0:
                local_fixed_blocks += 1
                local_methods += n
                return f'{head}{new_body}{tail}'
            return m.group(0)

        new = BLOCK_RE.sub(repl, text)
        if local_fixed_blocks > 0:
            files_touched += 1
            blocks_fixed += local_fixed_blocks
            methods_indented += local_methods
            if fix and new != text:
                p.write_text(new, encoding='utf-8')

    mode = 'APPLIED' if fix else 'DRY-RUN'
    print(f'[{mode}] Files touched: {files_touched}')
    print(f'        Blocks fixed:  {blocks_fixed}')
    print(f'        Methods indented (def/@ lines + bodies): {methods_indented}')
    if not fix:
        print('\nRe-run with --fix to apply.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
