"""Audit: detailed code indentation issues.

Categorize all code blocks by their indentation pattern:
1. ALL_OVER_INDENT: every non-empty line starts with N+ spaces (uniform extra indent)
2. NO_INDENT_FOR_PYTHON: looks like Python (def, class, if, for) but has no indentation
3. MIXED_INDENT: some lines indented, others not (broken)
4. TAB_AND_SPACES: mixed tab/space (will look weird)
5. LEADING_BLANK: starts with blank lines
6. TRAILING_BLANK: ends with blank lines
"""
from pathlib import Path
from bs4 import BeautifulSoup
import re

ROOT = Path(__file__).resolve().parents[2]
SKIP = ['node_modules', '.git', 'output', 'backup', 'KDP/build',
        'KDP/html2pub', 'pagefind', 'temp_epub', 'agents/', 'templates/']


def is_skip(p):
    sp = str(p).replace('\\', '/')
    return any(s in sp for s in SKIP)


def analyze_code(text, lang):
    """Categorize indent pattern of a code block."""
    if not text:
        return None
    lines = text.split('\n')
    # Strip trailing newlines/blank lines but track
    non_empty = [l for l in lines if l.strip()]
    if not non_empty:
        return None

    issues = []

    # Check leading/trailing blanks
    if len(lines) > 0 and not lines[0].strip():
        # Lines that are pure whitespace at start
        cnt = 0
        for l in lines:
            if not l.strip():
                cnt += 1
            else:
                break
        if cnt >= 1:
            issues.append(f'LEADING_BLANK ({cnt})')
    if len(lines) > 1 and not lines[-1].strip():
        cnt = 0
        for l in reversed(lines):
            if not l.strip():
                cnt += 1
            else:
                break
        if cnt >= 2:  # 1 trailing newline is OK
            issues.append(f'TRAILING_BLANK ({cnt})')

    # Get leading whitespace counts (in spaces; tabs as 4)
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

    # Check for uniform extra indent (everyone indented >=N where N is "extra")
    min_indent = min(indents)
    if min_indent >= 4 and len(non_empty) >= 3:
        issues.append(f'OVER_INDENT_ALL ({min_indent} sp)')

    # Check tabs+spaces mix
    if has_tab and has_space_indent:
        issues.append('TAB_AND_SPACES_MIX')

    # Check Python-like content without indentation
    if lang in ('python', 'py'):
        # Has def/class/if/for/while/try at top level (no leading spaces)?
        has_def = any(re.match(r'^(def |class |if |for |while |try:|with )', l)
                      for l in non_empty)
        # Are there any lines that SHOULD be indented (body of def/class/if)?
        body_needed = False
        for i, l in enumerate(non_empty):
            if re.match(r'^(def |class |if |elif |else:|for |while |try:|except|with |finally:)', l) and l.rstrip().endswith(':'):
                # Next line should be indented relative to this one
                this_indent = indents[i]
                if i + 1 < len(non_empty):
                    next_indent = indents[i + 1]
                    if next_indent <= this_indent:
                        body_needed = True
                        break
        if body_needed:
            issues.append('PYTHON_NO_INDENT_BODY')

    # Check broken indent (e.g., one line at 4 spaces, next at 8, then 4 again)
    if len(set(indents)) > 4 and lang in ('python', 'py', 'javascript', 'js',
                                           'typescript', 'ts'):
        # Wide variation — likely OK for nested code, but check inconsistent
        pass

    return issues if issues else None


results = []
counts = {}
for p in ROOT.rglob('*.html'):
    if is_skip(p):
        continue
    try:
        s = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
    except Exception:
        continue
    for pre in s.find_all('pre'):
        code = pre.find('code')
        if not code:
            continue
        text = code.get_text()
        lang = ''
        for c in code.get('class', []):
            if c.startswith('language-'):
                lang = c[9:]
                break
            elif c.startswith('lang-'):
                lang = c[5:]
                break

        issues = analyze_code(text, lang)
        if issues:
            results.append({
                'file': str(p.relative_to(ROOT)),
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
print(f'Total problematic code blocks: {len(results)}')

print()
print('=== Sample OVER_INDENT_ALL cases ===')
over = [r for r in results if any('OVER_INDENT_ALL' in i for i in r['issues'])]
for r in over[:20]:
    print(f'  {r["file"]} ({r["lang"]}, {r["n_lines"]} lines): {r["issues"]}')
    print(f'    first line: {r["first_line"][:80]}')

print()
print('=== Sample PYTHON_NO_INDENT_BODY cases ===')
no_indent = [r for r in results if any('PYTHON_NO_INDENT_BODY' in i for i in r['issues'])]
for r in no_indent[:20]:
    print(f'  {r["file"]} ({r["lang"]}, {r["n_lines"]} lines): {r["issues"]}')
    print(f'    first line: {r["first_line"][:80]}')

print()
print('=== Sample LEADING_BLANK cases ===')
lead = [r for r in results if any('LEADING_BLANK' in i for i in r['issues'])]
for r in lead[:15]:
    print(f'  {r["file"]} ({r["lang"]}): {r["issues"]}')
