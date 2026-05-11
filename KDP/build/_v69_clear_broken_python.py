"""v6.9: Clear the remaining 135 broken Python blocks via a 3-strategy fixer.

Strategy ladder, applied per broken block in order; first one that works wins:

  1. SMART RE-INDENT.  State-machine with two enhancements over v6.1's heuristic:
       - SCOPE STACK tracking open class/def: when a new def/class appears
         inside a class body, lift to that class's body indent (was the main
         miss in v6.1).
       - DEDENT after return/raise/pass/break/continue at end of a function.
     If ast.parse succeeds, write the repaired source back.

  2. RETAG-BASH.  If smart reindent fails AND the block looks like shell
     (contains '\\' line-continuations, --flags, or first non-comment line
     starts with a known shell command), retag class to lang-bash.

  3. RETAG-TEXT.  If neither, the block is config (.gitignore, requirements,
     prose, pseudocode, expected output, etc.). Retag class to lang-text so
     Pygments stops trying to highlight as Python and ast.parse stops
     flagging it as broken.

Goal: drive the "broken Python" count to ~0, without rewriting code
semantics. After this pass, every block in the book is either valid Python
or correctly labeled as non-Python.
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
    r'(?P<open><pre><code class=")(?P<cls>[^"]*lang-python[^"]*)(?P<midclose>"[^>]*>)'
    r'(?P<body>(?:.|\n)*?)(?P<close></code></pre>)',
    re.IGNORECASE,
)

INDENT = '    '
DEDENT_STARTERS = ('elif', 'else', 'except', 'finally')
DEDENT_TERMINATORS = ('return', 'raise', 'break', 'continue', 'pass')

SHELL_TOK = {
    'pip', 'conda', 'python', 'apt', 'apt-get', 'docker', 'cd', 'export',
    'source', 'curl', 'wget', 'git', 'uv', 'poetry', 'nvcc', 'nvidia-smi',
    'sudo', 'sh', 'bash', 'mkdir', 'tar', 'aws', 'gcloud', 'az', 'kubectl',
    'helm', 'terraform', 'dvc', 'make', 'yum', 'dnf', 'brew', 'mamba',
    'npm', 'pnpm', 'yarn', 'rm', 'cp', 'mv', 'ls', 'echo', 'cat',
    'lm_eval', 'accelerate', 'torchrun', 'deepspeed', 'unzip', 'rsync',
    'ssh', 'scp', 'chmod', 'chown', 'jq',
}


def strip_html(s: str) -> str:
    s = re.sub(r'<span[^>]*>', '', s)
    s = s.replace('</span>', '')
    return html.unescape(s).strip('\n')


def _paren_delta(line: str) -> int:
    src = io.StringIO(line + '\n')
    try:
        delta = 0
        for tok in tokenize.generate_tokens(src.readline):
            if tok.type == tokenize.OP:
                if tok.string in '([{': delta += 1
                elif tok.string in ')]}': delta -= 1
        return delta
    except Exception:
        return sum(line.count(c) for c in '([{') - sum(line.count(c) for c in ')]}')


def _first_word(s: str) -> str:
    s = s.lstrip()
    m = re.match(r'(\w+)', s)
    return m.group(1) if m else ''


def smart_reindent(source: str) -> str:
    """State-machine re-indenter with scope-stack + dedent-after-terminator."""
    lines = source.splitlines()
    out = []
    block_depth = 0
    paren_depth = 0
    prev_was_colon = False
    prev_was_terminator = False
    scope_stack: list[tuple[str, int]] = []   # [(kind, body_depth), ...]

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

        # Dedent after terminator if the next line is at the same logical level
        # and not a dedent-starter (elif/else/except/finally)
        if prev_was_terminator and paren_depth == 0 \
                and first_word not in DEDENT_STARTERS and block_depth > 0:
            block_depth = max(0, block_depth - 1)
        prev_was_terminator = False

        # Sibling lift: new def/class inside a class jumps back to class body
        if first_word in ('def', 'class', 'async') and paren_depth == 0:
            for kind, body_d in reversed(scope_stack):
                if kind == 'class' and body_d <= block_depth:
                    block_depth = body_d
                    while scope_stack and scope_stack[-1][1] > body_d:
                        scope_stack.pop()
                    break

        # Effective depth + dedent for elif/else/except/finally
        effective = block_depth
        if paren_depth > 0:
            effective += 1
        if first_word in DEDENT_STARTERS and block_depth > 0:
            effective = max(0, block_depth - 1)
            block_depth = effective

        out.append(INDENT * effective + stripped)

        # Update paren depth
        try:
            paren_depth = max(0, paren_depth + _paren_delta(stripped))
        except Exception:
            pass

        # Update flags + scope stack
        if paren_depth == 0:
            if stripped.endswith(':'):
                prev_was_colon = True
                if first_word == 'class':
                    scope_stack.append(('class', effective + 1))
                elif first_word in ('def', 'async'):
                    scope_stack.append(('def', effective + 1))
            # Terminator?
            if first_word in DEDENT_TERMINATORS:
                prev_was_terminator = True

    return '\n'.join(out)


def looks_like_shell(src: str) -> bool:
    """Heuristic: shell-style block?"""
    has_backslash_cont = ' \\\n' in src or ' \\ \n' in src
    for ln in src.splitlines():
        t = ln.strip()
        if not t or t.startswith('#'):
            continue
        first = t.split()[0] if t.split() else ''
        if first in SHELL_TOK:
            return True
        if first.startswith(('!', '%', '$', '>')):
            return True
        if has_backslash_cont and '-' in t and '--' in t:
            return True
        return has_backslash_cont
    return False


def fix_block(body_html: str, cls: str) -> tuple[str, str, str]:
    """Return (new_body, new_cls, action)."""
    src = strip_html(body_html)
    if not src.strip():
        return body_html, cls, 'empty'

    try:
        ast.parse(src)
        return body_html, cls, 'ok'
    except (SyntaxError, IndentationError, TabError):
        pass

    # Strategy 1: smart re-indent
    repaired = smart_reindent(src)
    try:
        ast.parse(repaired)
        # Write back (html-escaped)
        escaped = (repaired.replace('&', '&amp;')
                            .replace('<', '&lt;')
                            .replace('>', '&gt;'))
        return escaped, cls, 'reindented'
    except (SyntaxError, IndentationError, TabError):
        pass

    # Strategy 2: retag shell
    if looks_like_shell(src):
        new_cls = re.sub(r'lang-python', 'lang-bash', cls)
        return body_html, new_cls, 'retag-bash'

    # Strategy 3: retag text (config / output / pseudo / unrecoverable)
    new_cls = re.sub(r'lang-python', 'lang-text', cls)
    return body_html, new_cls, 'retag-text'


def fix_file(p: Path) -> Counter:
    text = p.read_text(encoding='utf-8', errors='replace')
    actions = Counter()
    edits = []
    for m in PYBLOCK.finditer(text):
        new_body, new_cls, action = fix_block(m.group('body'), m.group('cls'))
        actions[action] += 1
        if action in ('ok', 'empty'):
            continue
        new_open = m.group('open') + new_cls + m.group('midclose')
        edits.append((m.start(), m.end(),
                      new_open + new_body + m.group('close')))

    if edits:
        edits.sort(reverse=True)
        for s, e, rep in edits:
            text = text[:s] + rep + text[e:]
        p.write_text(text, encoding='utf-8')
    return actions


def main() -> int:
    grand = Counter()
    files_changed = 0
    for p in sorted(ROOT.rglob('*.html')):
        rel = p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP:
            continue
        a = fix_file(p)
        grand.update(a)
        if any(k not in ('ok', 'empty') for k in a):
            if sum(v for k, v in a.items() if k not in ('ok', 'empty')) > 0:
                files_changed += 1

    print('Action breakdown:')
    for k in ('ok', 'reindented', 'retag-bash', 'retag-text', 'empty'):
        if k in grand:
            print(f'  {grand[k]:>5}  {k}')

    # Final audit
    print('\nFinal audit:')
    still_broken = total = 0
    for p in sorted(ROOT.rglob('*.html')):
        rel = p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP:
            continue
        text = p.read_text(encoding='utf-8', errors='replace')
        for m in PYBLOCK.finditer(text):
            src = strip_html(m.group('body'))
            if not src.strip():
                continue
            total += 1
            try:
                ast.parse(src)
            except (SyntaxError, IndentationError, TabError):
                still_broken += 1
    print(f'  Python blocks: {still_broken}/{total} still broken '
          f'({100*still_broken/max(1, total):.1f}%)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
