"""Re-render Python code blocks with collapsed nested-dict indent.

Root cause: some Python code in section files (e.g., section-13.2 OpenAI
tools schema, section-43.2 coding agent tools list) has all nested-dict
keys at the same 4-space indent. The structure is technically valid
Python (the dicts parse) but visually flat: nested levels indistinguishable
from siblings. Probably introduced by a stripper that collapsed leading
whitespace, or by a deserializer that re-emitted without indent_level.

Generalized fix: detect Python blocks where AST nesting depth >= 3 but
visual max-indent <= 1 level past function-body. Re-format via `black`
to canonical 4-space-per-level. Re-render through Pygments to refresh
the span markup. Substitute back into HTML.

Idempotent: blocks already properly nested produce zero diff via black.
"""
from __future__ import annotations
import argparse
import ast
import html as html_lib
import re
import sys
from pathlib import Path

import black
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude", ".book-update", "vendor", "scripts", "docs",
              "styles"}

LEXER = PythonLexer()
FORMATTER = HtmlFormatter(nowrap=True, noclasses=False)
BLACK_MODE = black.Mode(line_length=88, string_normalization=True)

# Match <pre>...<code class="...pygments-highlighted...lang-python...">BODY</code>...</pre>
CODE_PAT = re.compile(
    r'(<pre[^>]*>\s*)'
    r'(<code class="[^"]*pygments-highlighted[^"]*lang-python[^"]*">)'
    r'((?:(?!</code>).)*?)'
    r'(</code>\s*</pre>)',
    re.DOTALL,
)


def extract_raw_python(body_html: str) -> str:
    """Strip Pygments spans, unescape entities -> raw Python source."""
    no_spans = re.sub(r'</?span[^>]*>', '', body_html)
    return html_lib.unescape(no_spans)


def detect_collapsed_indent(src: str) -> bool:
    """Heuristic: source is collapsed if it contains a nested-dict pattern
    (multiple `"key":` lines indented identically) where the AST shows
    nesting depth >= 3."""
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return False
    # Count max dict nesting depth
    max_depth = 0
    def walk(node, depth=0):
        nonlocal max_depth
        if isinstance(node, ast.Dict):
            max_depth = max(max_depth, depth)
            for v in node.values:
                walk(v, depth + 1)
        elif isinstance(node, ast.List):
            for v in node.elts:
                walk(v, depth)
        elif isinstance(node, ast.Assign):
            walk(node.value, depth + 1)
        else:
            for child in ast.iter_child_nodes(node):
                walk(child, depth)
    walk(tree)
    if max_depth < 3:
        return False
    # Check actual visual indent of "name":-style lines
    lines = src.split('\n')
    indents = [len(l) - len(l.lstrip(' ')) for l in lines
               if l.strip().startswith('"') and ':' in l]
    if len(indents) < 3:
        return False
    # If max indent is <= 8 spaces for a 3+-deep dict, indent is collapsed
    return max(indents) <= 8 and len(set(indents)) <= 2


def reformat_block(raw: str) -> str | None:
    """Format with black. Return None if formatting fails."""
    try:
        formatted = black.format_str(raw, mode=BLACK_MODE)
        return formatted
    except Exception:
        return None


def fix(p: Path, dry_run: bool) -> int:
    text = p.read_text(encoding="utf-8")
    orig = text
    count = 0
    edits: list[tuple[int, int, str]] = []
    for m in CODE_PAT.finditer(text):
        pre_open = m.group(1)
        code_open = m.group(2)
        body = m.group(3)
        close = m.group(4)
        raw = extract_raw_python(body)
        if not detect_collapsed_indent(raw):
            continue
        formatted = reformat_block(raw)
        if formatted is None:
            continue
        if formatted.strip() == raw.strip():
            continue  # No change from black
        # Re-render with Pygments
        highlighted = highlight(formatted, LEXER, FORMATTER).rstrip("\n")
        replacement = pre_open + code_open + highlighted + close
        edits.append((m.start(), m.end(), replacement))
        count += 1
    for start, end, repl in reversed(edits):
        text = text[:start] + repl + text[end:]
    if text != orig and not dry_run:
        p.write_text(text, encoding="utf-8")
    return count


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply
    files_edited = 0
    total = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        n = fix(p, dry_run)
        if n > 0:
            files_edited += 1
            total += n
    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"=== {mode} ===")
    print(f"Files edited:    {files_edited}")
    print(f"Blocks reformatted: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
