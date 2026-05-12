"""v6.44a: Audit every Python code block in the book.

For each <pre><code class="lang-python">...</code></pre>:
  1. Strip Pygments spans + decode HTML entities to recover source.
  2. Try ast.parse(). If it parses, the block is structurally OK.
  3. If it fails, classify the error (IndentationError vs SyntaxError vs other).

The goal is to identify how many blocks have the "methods nested in __init__"
bug (which manifests as IndentationError or as code that parses but has
the methods unreachable). This is the diagnostic pass before fix.

Output: KDP/validation/python_structure_audit.csv
"""
from __future__ import annotations
import ast
import csv
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = ROOT / 'KDP' / 'validation' / 'python_structure_audit.csv'


def strip_html(s: str) -> str:
    s = re.sub(r'<[^>]+>', '', s)
    s = html.unescape(s)
    return s


def detect_bug_pattern(code: str) -> str | None:
    """Look for the 'def nested inside def-body' pattern that this bug produces.
    Returns a short description if detected, else None."""
    lines = code.split('\n')
    # Track the indent level of the most recent `def`/`class` declaration
    # at each depth. Bug pattern: a `def`/`class` appears at an indent that's
    # exactly 4 deeper than its expected scope opener.
    prev_def_indent = None
    for i, line in enumerate(lines):
        s = line.lstrip()
        if not s or s.startswith('#'):
            continue
        indent = len(line) - len(s)
        m = re.match(r'(?:async\s+)?(def|class)\s+(\w+)', s)
        if m:
            if prev_def_indent is not None and indent > prev_def_indent:
                # This decl is nested inside the previous one -- could be
                # legitimate (closure / inner class) OR the bug.
                # Check: is the previous decl's BODY at indent prev_def_indent+4?
                # If yes, and this new decl is ALSO at prev_def_indent+4, that's
                # the bug pattern (the new decl appears as a sibling of body
                # statements rather than as a sibling of the previous def).
                if indent == prev_def_indent + 4:
                    # Look for body lines BETWEEN prev_def and this one at
                    # the same indent (prev+4). If there are several, this
                    # def is mis-placed.
                    body_count = 0
                    for j in range(i):
                        ll = lines[j].lstrip()
                        if not ll or ll.startswith('#'):
                            continue
                        ind_j = len(lines[j]) - len(ll)
                        if ind_j == indent and not re.match(
                            r'(?:async\s+)?(def|class)\s+', ll
                        ):
                            body_count += 1
                    if body_count >= 2:
                        return f'over-nested {m.group(1)} {m.group(2)} at line {i + 1}'
            prev_def_indent = indent
    return None


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    total = parse_ok = parse_err = bug_detected = 0
    for p in sorted(ROOT.glob('part-*/module-*/section-*.html')):
        text = p.read_text(encoding='utf-8', errors='replace')
        for m in re.finditer(
            r'<pre>\s*<code[^>]*lang-python[^>]*>(.+?)</code>\s*</pre>',
            text, re.DOTALL,
        ):
            total += 1
            code = strip_html(m.group(1))
            # Skip very short blocks
            if len(code.strip()) < 30:
                continue
            err_kind = ''
            try:
                ast.parse(code)
                parse_ok += 1
            except IndentationError as e:
                parse_err += 1
                err_kind = f'IndentationError: {e.msg} (line {e.lineno})'
            except SyntaxError as e:
                parse_err += 1
                err_kind = f'SyntaxError: {e.msg} (line {e.lineno})'
            except Exception as e:
                err_kind = f'{type(e).__name__}: {e}'
            bug = detect_bug_pattern(code)
            if bug:
                bug_detected += 1
            rows.append({
                'file': str(p.relative_to(ROOT)).replace('\\', '/'),
                'block_offset': m.start(),
                'parse_error': err_kind,
                'bug_pattern': bug or '',
                'preview': code.strip().split('\n')[0][:80],
            })

    with OUT.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else
                           ['file', 'block_offset', 'parse_error', 'bug_pattern', 'preview'])
        w.writeheader()
        w.writerows(rows)

    print(f'Total Python blocks: {total}')
    print(f'  Parse OK:           {parse_ok}')
    print(f'  Parse error:        {parse_err}')
    print(f'  Bug pattern found:  {bug_detected}')
    print(f'\nReport: {OUT}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
