"""Audit: code block formatting issues that mar Kindle rendering.

Look for:
  1. LEADING_BLANK: <pre><code> starts with blank line(s) -> visible
     whitespace at top of code panel.
  2. TRAILING_BLANK: trailing blank lines (>= 2).
  3. OVER_INDENT_ALL: every non-empty line indented >= 8 spaces.
  4. PYTHON_NO_INDENT_BODY: Python code with def/class/if/...: but the
     following line is at the SAME indent (no body indent).
  5. TAB_AND_SPACES: mixed tab/space indent.
  6. WIDE: longest line > 100 characters (overflows Kindle column).

Usage:
    python audit_code_indent.py --root <book-root>
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup


DEFAULT_SKIP = [
    'node_modules', '.git', 'output', 'backup', 'pagefind',
    'temp_epub', 'agents/', 'templates/', 'KDP/build', 'KDP/html2pub',
]


def is_skip(p: Path, skip: list[str]) -> bool:
    sp = str(p).replace('\\', '/')
    return any(s in sp for s in skip)


def analyze_code(text: str, lang: str) -> list[str]:
    if not text:
        return []
    lines = text.split('\n')
    non_empty = [l for l in lines if l.strip()]
    if not non_empty:
        return []

    issues = []

    # LEADING_BLANK
    if lines and not lines[0].strip():
        cnt = 0
        for l in lines:
            if not l.strip():
                cnt += 1
            else:
                break
        if cnt >= 1:
            issues.append(f'LEADING_BLANK ({cnt})')

    # TRAILING_BLANK
    if len(lines) > 1 and not lines[-1].strip():
        cnt = 0
        for l in reversed(lines):
            if not l.strip():
                cnt += 1
            else:
                break
        if cnt >= 2:
            issues.append(f'TRAILING_BLANK ({cnt})')

    # Indents
    indents = []
    has_tab = False
    has_space_indent = False
    for l in non_empty:
        if l.startswith('\t'):
            has_tab = True
        ws = 0
        for ch in l:
            if ch == ' ':
                ws += 1
            elif ch == '\t':
                ws += 4
                has_tab = True
            else:
                break
        if ws > 0 and l[0] == ' ':
            has_space_indent = True
        indents.append(ws)

    min_indent = min(indents) if indents else 0
    if min_indent >= 8 and len(non_empty) >= 3:
        issues.append(f'OVER_INDENT_ALL ({min_indent} sp)')

    if has_tab and has_space_indent:
        issues.append('TAB_AND_SPACES_MIX')

    if lang in ('python', 'py'):
        body_needed = False
        for i, l in enumerate(non_empty):
            if (re.match(r'^(def |class |if |elif |else:|for |while |'
                         r'try:|except|with |finally:)', l)
                    and l.rstrip().endswith(':')):
                this_indent = indents[i]
                if i + 1 < len(non_empty):
                    next_indent = indents[i + 1]
                    if next_indent <= this_indent:
                        body_needed = True
                        break
        if body_needed:
            issues.append('PYTHON_NO_INDENT_BODY')

    # Wide
    max_line = max((len(l) for l in lines), default=0)
    if max_line > 100:
        issues.append(f'WIDE ({max_line} chars)')

    return issues


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, required=True)
    ap.add_argument('--skip', nargs='*', default=DEFAULT_SKIP)
    args = ap.parse_args(argv)

    root: Path = args.root.resolve()
    if not root.exists():
        print(f'ERROR: root does not exist: {root}', file=sys.stderr)
        return 2

    results = []
    counts = {}
    n_blocks = 0
    for p in root.rglob('*.html'):
        if is_skip(p, args.skip):
            continue
        try:
            s = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
        except Exception:
            continue
        for pre in s.find_all('pre'):
            n_blocks += 1
            code = pre.find('code')
            if not code:
                continue
            text = code.get_text()
            lang = ''
            for c in code.get('class', []):
                if c.startswith('language-'):
                    lang = c[9:]
                    break
                if c.startswith('lang-'):
                    lang = c[5:]
                    break

            issues = analyze_code(text, lang)
            if issues:
                results.append({
                    'file': str(p.relative_to(root)),
                    'lang': lang,
                    'issues': issues,
                    'first_line': text.split('\n')[0][:60] if text else '',
                    'n_lines': len(text.split('\n')),
                })
                for issue in issues:
                    key = issue.split(' ')[0]
                    counts[key] = counts.get(key, 0) + 1

    print('=== CODE INDENT ISSUE SUMMARY ===')
    for k, v in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f'  {k}: {v}')
    print()
    print(f'Total code blocks scanned: {n_blocks}')
    print(f'Total problematic blocks:  {len(results)}')

    for cat in ('LEADING_BLANK', 'TRAILING_BLANK', 'OVER_INDENT_ALL',
                'PYTHON_NO_INDENT_BODY', 'TAB_AND_SPACES_MIX', 'WIDE'):
        cases = [r for r in results
                 if any(i.startswith(cat) for i in r['issues'])]
        if cases:
            print(f'\n=== Sample {cat} cases ===')
            for r in cases[:10]:
                print(f'  {r["file"]} ({r["lang"]}, {r["n_lines"]} lines):'
                      f' {r["issues"]}')
                if r['first_line'].strip():
                    print(f'    first line: {r["first_line"][:80]}')

    return 0 if len(results) == 0 else 1


if __name__ == '__main__':
    raise SystemExit(main())
