"""Audit code blocks for known indentation/highlighting bugs.

A) Flat methods: class def at col 0 followed by another def at col 0 in
   the same code block (should be 4-space indent inside class).
B) Missing pygments class: lang-python WITHOUT pygments-highlighted but
   the code parses cleanly.
C) Empty highlighting: pygments-highlighted lang-python but no <span>
   tags inside.
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

# Find <pre><code class="...lang-python..."> blocks
BLOCK_RE = re.compile(
    r'<pre[^>]*>\s*<code\s+class="([^"]*lang-python[^"]*)">([\s\S]*?)</code>\s*</pre>',
    re.IGNORECASE)
SPAN_RE = re.compile(r'<span[^>]*>|</span>')


def extract_code(html_block: str) -> str:
    return html.unescape(SPAN_RE.sub('', html_block))


def check_flat_methods(code: str) -> bool:
    """True if code has `class X:` at col 0 followed by `def Y` at col 0."""
    lines = code.split('\n')
    in_class = False
    saw_class_body = False
    for line in lines:
        if re.match(r'^class\s+\w+', line):
            in_class = True
            saw_class_body = False
            continue
        if not in_class:
            continue
        if re.match(r'^def\s+\w+', line):
            # def at col 0 INSIDE a class scope = bug
            return True
        if re.match(r'^[a-zA-Z]', line) and not line.startswith('class'):
            # a non-indented statement = class scope ended naturally
            in_class = False
    return False


def main() -> int:
    bug_a: list[str] = []
    bug_b: list[str] = []
    bug_c: list[str] = []
    count = 0
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
        rel = str(p.relative_to(ROOT))
        for m in BLOCK_RE.finditer(text):
            count += 1
            classes = m.group(1)
            body = m.group(2)
            code = extract_code(body)
            has_pygments_cls = 'pygments-highlighted' in classes
            has_spans = '<span' in body

            # Bug A: flat methods (any block, but most common in pygments blocks)
            if check_flat_methods(code):
                bug_a.append(rel)

            # Bug B: lang-python WITHOUT pygments class, code parses
            if not has_pygments_cls:
                try:
                    ast.parse(code)
                    bug_b.append(rel)
                except SyntaxError:
                    pass

            # Bug C: pygments class but no spans (plain text inside)
            if has_pygments_cls and not has_spans and code.strip():
                bug_c.append(rel)

    print(f'Total lang-python blocks scanned: {count}')
    print(f'Bug A (flat methods inside class): {len(bug_a)} blocks across {len(set(bug_a))} files')
    print(f'Bug B (missing pygments class):    {len(bug_b)} blocks across {len(set(bug_b))} files')
    print(f'Bug C (pygments class no spans):   {len(bug_c)} blocks across {len(set(bug_c))} files')

    print('\nTop 20 files with Bug A:')
    from collections import Counter
    for f, n in Counter(bug_a).most_common(20):
        print(f'  {n:3d}  {f}')
    print('\nTop 20 files with Bug B:')
    for f, n in Counter(bug_b).most_common(20):
        print(f'  {n:3d}  {f}')
    print('\nTop 20 files with Bug C:')
    for f, n in Counter(bug_c).most_common(20):
        print(f'  {n:3d}  {f}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
