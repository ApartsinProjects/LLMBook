"""v14.4: Auto-format Python code blocks with black, then re-emit
with Pygments syntax highlighting.

Targets the 216 PYTHON_NO_BODY_INDENT + 123 INCONSISTENT_INDENT cases
from AUDIT_code_indent.json (where Python `def`/`class`/`if`/`for`
bodies are at the same or shallower indent than the opener).

Approach:
  1. Read AUDIT_code_indent.json -> list of files with the issue
  2. For each unique file:
     a. Parse HTML with BeautifulSoup
     b. For each <pre><code class="...python..."> block:
        - Extract plain text (strip pygments spans)
        - Try black.format_str() with mode=Mode()
        - If black fails (syntax error), leave block as-is
        - If black succeeds, re-tokenize with pygments and rebuild the
          <code> with new pygments-highlighted spans
  3. Write modified files back

Safety:
  - If black raises any error -> skip (no change)
  - If pygments raises any error -> use plain <code> text without highlighting
  - Black-formatted source must be syntactically valid Python (black
    refuses on invalid input)
"""
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
import json
import sys
import re

ROOT = Path(__file__).resolve().parents[2]
AUDIT_JSON = ROOT / 'KDP' / 'build' / 'AUDIT_code_indent.json'


def get_target_files():
    """Files with PYTHON_NO_BODY_INDENT or INCONSISTENT_INDENT issues."""
    data = json.load(open(AUDIT_JSON))
    files = set()
    for issue in data['issues']:
        if issue['type'] in ('PYTHON_NO_BODY_INDENT', 'INCONSISTENT_INDENT'):
            if issue.get('lang', '').lower() in ('python', 'py'):
                files.add(issue['file'])
    return sorted(files)


def format_with_black(code: str) -> str | None:
    """Run black on a Python source string. Returns formatted code or None."""
    try:
        import black
        mode = black.Mode(
            target_versions={black.TargetVersion.PY311},
            line_length=88,
            string_normalization=True,
        )
        formatted = black.format_str(code, mode=mode)
        return formatted
    except Exception:
        return None


def reformat_with_pygments(code: str, lang: str) -> str | None:
    """Re-tokenize formatted code with pygments. Returns HTML."""
    try:
        from pygments import highlight
        from pygments.lexers import get_lexer_by_name
        from pygments.formatters import HtmlFormatter
        lexer = get_lexer_by_name(lang.lower() if lang else 'python')
        formatter = HtmlFormatter(
            nowrap=True,  # don't wrap in <div class="highlight">
            cssclass='highlight',
        )
        return highlight(code, lexer, formatter)
    except Exception:
        return None


def fix_html_file(path: Path, dry: bool) -> tuple[int, int]:
    """Returns (blocks_examined, blocks_fixed)."""
    soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
    n_examined = 0
    n_fixed = 0
    for code in soup.find_all('code'):
        cls = ' '.join(code.get('class', []))
        # Match Python code blocks
        lang = None
        for c in code.get('class', []):
            if c.startswith('language-'):
                lang = c[9:]
            elif c.startswith('lang-'):
                lang = c[5:]
        if not lang or lang.lower() not in ('python', 'py'):
            continue
        n_examined += 1
        # Extract plain text (strip pygments spans)
        original_text = code.get_text()
        # Skip if too short or trivial
        if len(original_text.strip()) < 20:
            continue
        # Conservative: only reformat if the code FAILS to parse as Python.
        # Already-valid code is left alone (don't impose style changes).
        import ast
        try:
            ast.parse(original_text)
            continue  # parses OK, no indent fix needed
        except SyntaxError:
            pass  # broken — try to fix
        except Exception:
            continue
        # Try to format with black
        formatted = format_with_black(original_text)
        if formatted is None or formatted == original_text:
            continue  # black failed or no-op
        # Sanity: formatted code must also parse
        try:
            ast.parse(formatted)
        except Exception:
            continue  # black produced unparseable code, skip

        # Pygments re-highlight
        new_html = reformat_with_pygments(formatted, lang)
        if new_html is None:
            # Fall back to plain text
            code.clear()
            code.string = formatted
        else:
            # Parse the pygments HTML and replace code contents
            new_soup = BeautifulSoup(new_html, 'html.parser')
            code.clear()
            for child in list(new_soup.children):
                code.append(child.extract() if hasattr(child, 'extract') else child)

        # Restore the language class
        cls_list = code.get('class', [])
        if 'pygments-highlighted' not in cls_list:
            code['class'] = cls_list + ['pygments-highlighted']

        n_fixed += 1

    if n_fixed > 0 and not dry:
        path.write_text(str(soup), encoding='utf-8')
    return n_examined, n_fixed


def main():
    dry = '--apply' not in sys.argv
    print('DRY RUN. Pass --apply.' if dry else 'APPLY mode.')
    print()
    files = get_target_files()
    print(f'Target files: {len(files)}')

    total_examined = 0
    total_fixed = 0
    n_files_modified = 0
    for rel in files:
        p = ROOT / rel
        if not p.exists():
            continue
        examined, fixed = fix_html_file(p, dry)
        if fixed > 0:
            n_files_modified += 1
            print(f'  {rel}: {fixed}/{examined} Python blocks reformatted')
        total_examined += examined
        total_fixed += fixed

    print()
    print(f'Files modified:   {n_files_modified}')
    print(f'Blocks examined:  {total_examined}')
    print(f'Blocks reformatted: {total_fixed}')


if __name__ == '__main__':
    main()
