"""v5.8: Heuristic re-indenter for broken Python code blocks.

Audit: 864 of 1371 Python <pre><code class="lang-python"> blocks fail
ast.parse(). Inspection of CF 10.1.2 shows the source code itself was
flat (zero leading whitespace), so Pygments produced no `<span class="w">`
indentation tokens. The break happened upstream — likely a "normalize
whitespace" pass that stripped leading spaces.

This module attempts to RECOVER indentation from a flat Python source
using a simple state machine. It is NOT a parser; it makes per-line
decisions based on:

  STATE        SOURCE OF +1 / -1 INDENT
  ────────     ─────────────────────────────────────────────
  paren_depth  unclosed (, [, { from prior lines (continuation)
  block_depth  number of `:`-ending control statements opened

Indent rules:
  - If paren_depth > 0 entering line:  indent = block_depth + 1 (continuation)
  - Otherwise:                          indent = block_depth
  - After a line ending with `:` (and NOT inside a paren):  block_depth += 1
  - On a `dedent keyword` (return/break/continue/raise/pass) at last line of
    a block:                            no change to block_depth on this line,
                                        but the NEXT line should de-dent if it
                                        starts with elif/else/except/finally/...

Limitations:
  - Cannot recover NESTED block boundaries: e.g. given
        for x in xs:
        for y in ys:
        process(x, y)
    we will indent both `for y` and `process` under the outer `for x`,
    producing a single nested loop instead of doubly-nested. Heuristics
    for "expected number of statements per block" are unreliable.
  - We re-verify each repaired block with ast.parse(). Failed repairs
    are LEFT UNTOUCHED so we never make things worse.

The fixer:
  1. Walks every Python <pre><code class="lang-python"> block in book HTML
  2. Strips Pygments span tags to recover the raw source
  3. Re-indents using the state machine
  4. Verifies with ast.parse
  5. If success AND the original failed, RE-EMITS the corrected source as
     plain code (Pygments will re-highlight on next build)
  6. Otherwise leaves block unchanged
"""
from __future__ import annotations
import ast
import html
import io
import re
import sys
import tokenize
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = {'agents', 'KDP', 'node_modules', 'scripts', '.git',
        'chapter_review', 'downloads', '_archive', '_lab_fragments',
        'templates'}

# Match <pre><code class="...lang-python...">{body}</code></pre>
PYBLOCK = re.compile(
    r'(?P<open><pre><code class="[^"]*lang-python[^"]*">)'
    r'(?P<body>(?:.|\n)*?)'
    r'(?P<close></code></pre>)',
    re.IGNORECASE,
)


def strip_html(s: str) -> str:
    """Remove Pygments span markup and decode entities."""
    s = re.sub(r'<span[^>]*>', '', s)
    s = s.replace('</span>', '')
    return html.unescape(s)


# Lines that, when starting the next logical line, mean we DEDENT
DEDENT_STARTERS = ('elif', 'else', 'except', 'finally')

# Compound-statement keywords that introduce a new block
BLOCK_KEYWORDS = ('def', 'class', 'if', 'elif', 'else', 'for', 'while',
                  'try', 'except', 'finally', 'with', 'async')

INDENT = '    '


def reindent(source: str) -> str:
    """Best-effort re-indenter."""
    lines = source.splitlines()
    out = []
    block_depth = 0
    paren_depth = 0
    prev_logical_was_colon = False  # last non-empty line ended with `:`

    for raw in lines:
        line = raw.lstrip()  # treat all input as flat
        stripped = line.rstrip()

        if not stripped:
            out.append('')
            continue

        # If this line begins with a closing bracket, decrement paren_depth FIRST
        leading_close = 0
        for ch in stripped:
            if ch in ')]}':
                leading_close += 1
            else:
                break

        # If previous line ended with `:`, we open a new block for THIS line
        if prev_logical_was_colon and paren_depth == 0:
            block_depth += 1
            prev_logical_was_colon = False

        # Determine effective indent
        # Start with block_depth; if continuing a paren, add one extra level
        effective_depth = block_depth
        if paren_depth > 0:
            effective_depth += 1
        # Dedent for "elif/else/except/finally" at the same level as their parent
        first_word = stripped.split(maxsplit=1)[0].rstrip(':')
        if first_word in DEDENT_STARTERS and block_depth > 0:
            effective_depth = max(0, block_depth - 1)
            # And ensure the "block_depth" reflects this dedent for the
            # body that follows the colon
            block_depth = effective_depth

        # Reconstruct the line with proper indent
        out.append(INDENT * effective_depth + stripped)

        # Now update paren_depth based on chars in this line
        # Don't count brackets inside strings/comments. Use tokenize for accuracy
        # but fall back to a simple counter for malformed lines.
        try:
            paren_delta = _safe_paren_delta(stripped)
        except Exception:
            paren_delta = sum(stripped.count(c) for c in '([{') - sum(stripped.count(c) for c in ')]}')
        paren_depth += paren_delta
        if paren_depth < 0:
            paren_depth = 0

        # Track if this line ended logical line with `:` (for next iteration)
        if paren_depth == 0:
            prev_logical_was_colon = stripped.endswith(':')

    return '\n'.join(out)


def _safe_paren_delta(line: str) -> int:
    """Count net paren depth change on a single line, ignoring strings/comments."""
    src = io.StringIO(line + '\n')
    delta = 0
    try:
        for tok in tokenize.generate_tokens(src.readline):
            if tok.type == tokenize.OP:
                if tok.string in '([{':
                    delta += 1
                elif tok.string in ')]}':
                    delta -= 1
    except (tokenize.TokenError, IndentationError):
        # malformed line — fall back to char counting
        delta = sum(line.count(c) for c in '([{') - sum(line.count(c) for c in ')]}')
    return delta


def fix_block(body_html: str) -> tuple[str, bool, bool]:
    """Return (new_body_html, was_broken, was_fixed)."""
    src = strip_html(body_html).strip('\n')
    if not src.strip():
        return body_html, False, False

    # Was it already valid?
    try:
        ast.parse(src)
        return body_html, False, False  # nothing to do
    except (SyntaxError, IndentationError, TabError):
        pass

    # Try re-indent
    new_src = reindent(src)
    try:
        ast.parse(new_src)
    except (SyntaxError, IndentationError, TabError):
        return body_html, True, False  # gave up

    # Re-emit as plain text (escape HTML entities). Pygments will re-highlight
    # on next build. We DO want to escape <, >, & to be safe inside <pre><code>.
    escaped = (new_src
               .replace('&', '&amp;')
               .replace('<', '&lt;')
               .replace('>', '&gt;'))
    # Preserve the surrounding newline structure
    return escaped, True, True


def fix_file(p: Path) -> tuple[int, int, int]:
    """Return (n_blocks, n_broken, n_fixed) for this file."""
    text = p.read_text(encoding='utf-8', errors='replace')
    n_blocks = n_broken = n_fixed = 0
    edits = []  # (start, end, new_body)
    for m in PYBLOCK.finditer(text):
        n_blocks += 1
        body = m.group('body')
        new_body, broken, fixed = fix_block(body)
        if broken:
            n_broken += 1
        if fixed:
            n_fixed += 1
            edits.append((m.start('body'), m.end('body'), new_body))

    if edits:
        # Apply in reverse order
        edits.sort(reverse=True)
        for s, e, new_body in edits:
            text = text[:s] + new_body + text[e:]
        p.write_text(text, encoding='utf-8')

    return n_blocks, n_broken, n_fixed


def main() -> int:
    total_blocks = total_broken = total_fixed = 0
    fixed_per_file = Counter()
    broken_remain = Counter()
    for p in sorted(ROOT.rglob('*.html')):
        rel = p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP:
            continue
        nb, nbk, nfx = fix_file(p)
        total_blocks += nb
        total_broken += nbk
        total_fixed += nfx
        if nfx:
            fixed_per_file[str(rel)] = nfx
        if nbk - nfx:
            broken_remain[str(rel)] = nbk - nfx

    print(f'Total Python blocks scanned: {total_blocks}')
    print(f'Broken (failed ast.parse) before fix: {total_broken}')
    print(f'Successfully re-indented: {total_fixed}')
    print(f'Still broken after re-indent: {total_broken - total_fixed}')
    print(f'\nTop fixed files:')
    for f, n in fixed_per_file.most_common(10):
        print(f'  {n:>3}x  {f}')
    print(f'\nFiles with blocks STILL broken (top 10):')
    for f, n in broken_remain.most_common(10):
        print(f'  {n:>3}x  {f}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
