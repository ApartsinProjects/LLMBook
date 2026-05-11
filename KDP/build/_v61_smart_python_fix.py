"""v6.1: Smarter Python code-block reconstructor.

After v5.8's heuristic re-indenter, 164 blocks remain broken. Triage:

  -  13 SHELL blocks (pip / conda / nvcc / docker) mis-tagged as
     `lang-python` -> retag as `lang-bash`
  -  13 AMBIGUOUS blocks (Jupyter !magic, %magic, pseudocode, YAML
     spilling into config) -> retag as `lang-text`
  - 138 TRULY BROKEN python blocks -> apply the v5.8 heuristic plus
     a NEW post-pass that lifts sibling `def`/`class` definitions back
     to the correct nesting depth (the v5.8 heuristic monotonically
     increased block_depth and never de-indented when a new method
     appeared inside a class)

The smarter re-indenter uses a SCOPE STACK:
  - Each entry: (keyword, body_indent)
  - When a `class X:` or `def Y:` is seen, push (keyword, current+1)
  - When a NEW `def` or `class` is encountered, check the scope stack:
    if there is an enclosing `class` with body_indent <= current_depth,
    LIFT this def to that body_indent (i.e., it's a sibling method)

After re-indenting, ast.parse() validates. Failures leave block as-is.
"""
from __future__ import annotations
import ast
import html
import io
import re
import sys
import tokenize
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = {'agents', 'KDP', 'node_modules', 'scripts', '.git',
        'chapter_review', 'downloads', '_archive', '_lab_fragments',
        'templates'}

PYBLOCK = re.compile(
    r'(?P<open><pre><code class=")(?P<cls>[^"]*lang-python[^"]*)(?P<mid>")>'
    r'(?P<body>(?:.|\n)*?)(?P<close></code></pre>)',
    re.IGNORECASE,
)

INDENT = '    '
DEDENT_STARTERS = ('elif', 'else', 'except', 'finally')
SHELL_FIRST_TOK = {'pip', 'conda', 'python', 'apt', 'apt-get', 'brew',
                   'nvidia-smi', 'nvcc', 'docker', 'cd', 'export', 'source',
                   'mkdir', 'curl', 'wget', 'git', 'uv', 'poetry', 'mv',
                   'cp', 'rm', 'ls', 'echo', 'mamba', 'micromamba', 'sh',
                   'bash', 'sudo', 'yum', 'dnf', 'tar', 'unzip', 'rsync',
                   'ssh', 'scp', 'kubectl', 'helm', 'terraform'}


def strip_html(s: str) -> str:
    s = re.sub(r'<span[^>]*>', '', s)
    s = s.replace('</span>', '')
    return html.unescape(s).strip('\n')


def looks_like_shell(src: str) -> bool:
    for ln in src.splitlines():
        t = ln.strip()
        if not t or t.startswith('#'):
            continue
        first = t.split()[0] if t.split() else ''
        if first in SHELL_FIRST_TOK or first in ('$', '>'):
            return True
        return False
    return False


def looks_like_pseudo(src: str) -> bool:
    for ln in src.splitlines():
        t = ln.strip()
        if not t or t.startswith('#'):
            continue
        # First non-comment line
        if t.startswith(('Input:', 'Output:', 'Algorithm:', 'Procedure:',
                         '!pip', '!nvidia', '%pip', '%magic', '## ')):
            return True
        return False
    return False


def _safe_paren_delta(line: str) -> int:
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
        delta = sum(line.count(c) for c in '([{') - sum(line.count(c) for c in ')]}')
    return delta


def _first_word(line: str) -> str:
    s = line.lstrip()
    if not s:
        return ''
    # Take first identifier-like token, strip trailing :
    m = re.match(r'(\w+)', s)
    return m.group(1) if m else ''


def smart_reindent(source: str) -> str:
    """Two-pass:
       Pass 1: monotonic-depth heuristic (v5.8 logic)
       Pass 2: lift sibling def/class to enclosing class body depth
    """
    lines = source.splitlines()
    out = []
    block_depth = 0
    paren_depth = 0
    prev_was_colon = False
    # Scope stack: list of (kind, body_depth) for open class/def
    scope_stack = []

    for raw in lines:
        line = raw.lstrip()
        stripped = line.rstrip()

        if not stripped:
            out.append('')
            continue

        first_word = _first_word(stripped)

        # Open new block from previous `:`
        if prev_was_colon and paren_depth == 0:
            block_depth += 1
            prev_was_colon = False

        # Smart sibling lift: if this line starts with `def`/`class` AND the
        # enclosing scope has an open `class` with body_depth <= block_depth,
        # this is a sibling method — lift to body_depth.
        if first_word in ('def', 'class', 'async'):
            for kind, body_d in reversed(scope_stack):
                if kind == 'class' and body_d <= block_depth:
                    # Lift this def/class to body_d
                    block_depth = body_d
                    # Pop any deeper scopes that this lift dropped out of
                    while scope_stack and scope_stack[-1][1] > body_d:
                        scope_stack.pop()
                    break

        # Dedent for elif/else/except/finally
        effective_depth = block_depth
        if paren_depth > 0:
            effective_depth += 1
        if first_word in DEDENT_STARTERS and block_depth > 0:
            effective_depth = max(0, block_depth - 1)
            block_depth = effective_depth

        # Decorators stay at same depth as the def they decorate
        # (no special handling: they naturally sit at block_depth, and the
        # following `def` inherits the same depth via the sibling-lift above)

        out.append(INDENT * effective_depth + stripped)

        # Update paren depth
        try:
            delta = _safe_paren_delta(stripped)
        except Exception:
            delta = sum(stripped.count(c) for c in '([{') - sum(stripped.count(c) for c in ')]}')
        paren_depth = max(0, paren_depth + delta)

        # Update scope stack on `:` ending lines
        if paren_depth == 0 and stripped.endswith(':'):
            prev_was_colon = True
            if first_word == 'class':
                scope_stack.append(('class', effective_depth + 1))
            elif first_word in ('def', 'async'):
                scope_stack.append(('def', effective_depth + 1))

    return '\n'.join(out)


def fix_block(body_html: str, cls: str) -> tuple[str, str, str]:
    """Return (new_body_html, new_cls, action) where action ∈
    {'noop', 'parsed', 'reindented', 'retag-bash', 'retag-text', 'gave-up'}."""
    src = strip_html(body_html)
    if not src.strip():
        return body_html, cls, 'noop'

    # Already valid?
    try:
        ast.parse(src)
        return body_html, cls, 'noop'
    except (SyntaxError, IndentationError, TabError):
        pass

    # SHELL?
    if looks_like_shell(src):
        new_cls = re.sub(r'lang-python', 'lang-bash', cls)
        return body_html, new_cls, 'retag-bash'

    # PSEUDO / magic / config?
    if looks_like_pseudo(src):
        new_cls = re.sub(r'lang-python', 'lang-text', cls)
        return body_html, new_cls, 'retag-text'

    # Try smart re-indent
    new_src = smart_reindent(src)
    try:
        ast.parse(new_src)
    except (SyntaxError, IndentationError, TabError):
        return body_html, cls, 'gave-up'

    # Re-emit as plain text
    escaped = (new_src
               .replace('&', '&amp;')
               .replace('<', '&lt;')
               .replace('>', '&gt;'))
    return escaped, cls, 'reindented'


def fix_file(p: Path) -> Counter:
    text = p.read_text(encoding='utf-8', errors='replace')
    edits = []
    actions = Counter()
    for m in PYBLOCK.finditer(text):
        new_body, new_cls, action = fix_block(m.group('body'), m.group('cls'))
        actions[action] += 1
        if action == 'noop':
            continue
        # Need to replace the whole match
        new_open = m.group('open') + new_cls + m.group('mid') + '>'
        new_match = new_open + new_body + m.group('close')
        edits.append((m.start(), m.end(), new_match))

    if edits:
        edits.sort(reverse=True)
        for s, e, repl in edits:
            text = text[:s] + repl + text[e:]
        p.write_text(text, encoding='utf-8')

    return actions


def main() -> int:
    grand = Counter()
    files_changed = 0
    for p in sorted(ROOT.rglob('*.html')):
        rel = p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP:
            continue
        actions = fix_file(p)
        grand.update(actions)
        if any(k != 'noop' for k in actions):
            files_changed += 1

    print('Action breakdown:')
    for k, v in grand.items():
        print(f'  {v:>5}  {k}')
    print(f'\nFiles changed: {files_changed}')

    # Final audit
    print('\nFinal audit (any python blocks still failing ast.parse):')
    still_broken = 0
    for p in sorted(ROOT.rglob('*.html')):
        rel = p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP:
            continue
        text = p.read_text(encoding='utf-8', errors='replace')
        for m in PYBLOCK.finditer(text):
            src = strip_html(m.group('body')).strip()
            if not src:
                continue
            try:
                ast.parse(src)
            except (SyntaxError, IndentationError, TabError):
                still_broken += 1
    print(f'  Python blocks still broken: {still_broken}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
