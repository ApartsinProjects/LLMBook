#!/usr/bin/env python3
"""
Audit Python code fragments embedded in section-*.html files for syntax /
indentation bugs.

Scans every section-*.html and index.html under the repo (skipping KDP,
node_modules, .git, _archive, source_fix_backups, conv_temp). For each
<pre><code class="pygments-highlighted lang-python">...</code></pre> block:
  1. Extract the plain Python source (strip <span> tags, unescape entities).
  2. Try compile(code, '<frag>', 'exec'); record SyntaxError/IndentationError.
  3. Heuristically flag "progressive nesting" pattern: a def/class indented
     deeper than the first def/class in the block, without an obvious enclosing
     if/for/while/with/try block.

Outputs a single structured report to stdout, grouped by SYNTAX_ERROR,
PROBABLE_INDENT_BUG, SUMMARY.

Run with: C:/Python314/python KDP/build/audit_python_fragments.py
"""
from __future__ import annotations

import html
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {"KDP", "node_modules", ".git", "_archive",
             "source_fix_backups", "conv_temp", "__pycache__",
             "temp_epub", "_concept-figs"}

BLOCK_RE = re.compile(
    r'<pre[^>]*>\s*<code[^>]*class="[^"]*\bpygments-highlighted\b[^"]*\blang-python\b[^"]*"[^>]*>'
    r'(.*?)</code>\s*</pre>',
    re.DOTALL | re.IGNORECASE,
)
TAG_RE = re.compile(r'<[^>]+>')
CAPTION_RE = re.compile(
    r'(?:Code\s+Fragment|Listing|Code)\s+([0-9A-Za-z.]+)',
    re.IGNORECASE,
)


def find_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # prune
        rel = Path(dirpath).relative_to(ROOT)
        parts = rel.parts
        if parts and parts[0] in SKIP_DIRS:
            dirnames[:] = []
            continue
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn == "index.html" or (fn.startswith("section-") and fn.endswith(".html")):
                yield Path(dirpath) / fn


def extract_code(raw_html: str) -> str:
    no_tags = TAG_RE.sub('', raw_html)
    return html.unescape(no_tags)


def line_of_offset(text: str, offset: int) -> int:
    return text.count('\n', 0, offset) + 1


def find_caption(text_before: str) -> str | None:
    """Search a window before the <pre> tag for a fragment caption."""
    window = text_before[-1500:]
    matches = CAPTION_RE.findall(window)
    if matches:
        return matches[-1]
    return None


INDENT_RE = re.compile(r'^( *)(def |class |async def )', re.MULTILINE)
ENCLOSING_RE = re.compile(
    r'^( *)(if |for |while |with |try:|elif |else:|except|finally|@|async for |async with )',
    re.MULTILINE,
)


def check_progressive_nesting(code: str) -> tuple[int, str] | None:
    """Return (line_no, source_line) if pattern detected, else None.

    Pattern: a def/class at indent > the first def/class indent, with no
    enclosing if/for/while/with/try/decorator preceding it at a compatible
    indent in the same block.
    """
    matches = list(INDENT_RE.finditer(code))
    if len(matches) < 2:
        return None
    first_indent = len(matches[0].group(1))
    for m in matches[1:]:
        ind = len(m.group(1))
        if ind <= first_indent:
            continue
        # check that something plausible encloses this nested def/class
        # by walking upward through previous lines for a less-indented enclosing
        # construct (if/for/while/with/try/decorator/class/def)
        start = m.start()
        prev_text = code[:start]
        prev_lines = prev_text.splitlines()
        enclosed = False
        for prev_line in reversed(prev_lines):
            stripped = prev_line.lstrip()
            if not stripped or stripped.startswith('#'):
                continue
            prev_indent = len(prev_line) - len(stripped)
            if prev_indent >= ind:
                continue
            # found the parent line
            if (stripped.startswith(('if ', 'for ', 'while ', 'with ',
                                     'try:', 'elif ', 'else:', 'except',
                                     'finally', '@', 'async for ',
                                     'async with ', 'def ', 'class ',
                                     'async def '))):
                enclosed = True
            break
        if not enclosed:
            line_no = code.count('\n', 0, start) + 1
            src_line = code.splitlines()[line_no - 1] if line_no - 1 < len(code.splitlines()) else ''
            return (line_no, src_line.rstrip())
    return None


def main() -> int:
    total_frags = 0
    syntax_errors: list[dict] = []
    indent_bugs: list[dict] = []

    for path in find_files():
        try:
            text = path.read_text(encoding='utf-8', errors='replace')
        except Exception as e:
            print(f"# READ_ERROR {path}: {e}", file=sys.stderr)
            continue
        for m in BLOCK_RE.finditer(text):
            total_frags += 1
            block_html = m.group(1)
            code = extract_code(block_html)
            pre_line = line_of_offset(text, m.start())
            caption = find_caption(text[:m.start()])
            rel_path = path.relative_to(ROOT).as_posix()

            try:
                compile(code, '<frag>', 'exec')
            except (SyntaxError, IndentationError) as e:
                syntax_errors.append({
                    'file': rel_path,
                    'pre_line': pre_line,
                    'caption': caption,
                    'err': f'{type(e).__name__}: {e.msg}',
                    'err_line': e.lineno,
                    'err_offset': e.offset,
                    'src_line': (e.text or '').rstrip() if e.text else '',
                })
                continue
            except Exception as e:
                syntax_errors.append({
                    'file': rel_path,
                    'pre_line': pre_line,
                    'caption': caption,
                    'err': f'{type(e).__name__}: {e}',
                    'err_line': None,
                    'err_offset': None,
                    'src_line': '',
                })
                continue

            # heuristic indent check
            res = check_progressive_nesting(code)
            if res is not None:
                line_no, src_line = res
                indent_bugs.append({
                    'file': rel_path,
                    'pre_line': pre_line,
                    'caption': caption,
                    'nested_line': line_no,
                    'src_line': src_line,
                })

    print("=" * 78)
    print("SYNTAX_ERROR")
    print("=" * 78)
    if not syntax_errors:
        print("(none)")
    for r in syntax_errors:
        cap = f"Frag {r['caption']}" if r['caption'] else "?"
        loc = f"line {r['err_line']}" if r['err_line'] else ""
        print(f"  {r['file']}:{r['pre_line']}  [{cap}]  {r['err']}  {loc}")
        if r['src_line']:
            print(f"      > {r['src_line']}")

    print()
    print("=" * 78)
    print("PROBABLE_INDENT_BUG")
    print("=" * 78)
    if not indent_bugs:
        print("(none)")
    for r in indent_bugs:
        cap = f"Frag {r['caption']}" if r['caption'] else "?"
        print(f"  {r['file']}:{r['pre_line']}  [{cap}]  line {r['nested_line']}: {r['src_line']}")

    print()
    print("=" * 78)
    print("SUMMARY")
    print("=" * 78)
    print(f"  total fragments scanned: {total_frags}")
    print(f"  total syntax errors:     {len(syntax_errors)}")
    print(f"  probable indent bugs:    {len(indent_bugs)}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
