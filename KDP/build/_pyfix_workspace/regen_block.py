"""Replace the pygmentized python block at given line in HTML file
with a freshly pygmentized version generated from the source file given.

Usage:
    python regen_block.py <html_file> <line_number> <source_py_file>

Requires `pygments`. Reads the python source, re-highlights via PythonLexer,
and replaces the matching <pre><code ...>...</code></pre> block.
"""
from __future__ import annotations
import sys
import re
from pathlib import Path

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter


def find_block(text: str, line_number: int) -> tuple[int, int]:
    line_starts = [0]
    for i, c in enumerate(text):
        if c == "\n":
            line_starts.append(i + 1)
    target_offset = line_starts[line_number - 1]
    pat = re.compile(
        r'<pre><code class="pygments-highlighted lang-python">(.*?)</code></pre>',
        re.DOTALL,
    )
    nearest = None
    for m in pat.finditer(text):
        s, e = m.span()
        if s <= target_offset <= e:
            return s, e
        d = min(abs(target_offset - s), abs(target_offset - e))
        if nearest is None or d < nearest[2]:
            nearest = (s, e, d)
    if nearest is not None:
        return nearest[0], nearest[1]
    raise SystemExit("no pygments block found")


def regen(src: str) -> str:
    formatter = HtmlFormatter(cssclass="pygments-highlighted", nowrap=False)
    out = highlight(src, PythonLexer(), formatter)
    # pygments wraps in <div class="..."><pre>...</pre></div>; we want
    # <pre><code class="pygments-highlighted lang-python">SPANS</code></pre>
    m = re.search(r"<pre>(.*?)</pre>", out, re.DOTALL)
    if not m:
        raise SystemExit("pygments output unexpected")
    inner = m.group(1)
    # pygments wraps inside <span></span>; strip outer wrapper if present
    # but inner content is already span'd. The default formatter wraps in
    # <pre><span></span>...</pre>. Strip the leading empty span if present.
    inner = re.sub(r"^<span></span>", "", inner)
    # Trim trailing newline that ends the pygments output
    inner = inner.rstrip("\n")
    return f'<pre><code class="pygments-highlighted lang-python">{inner}</code></pre>'


def main() -> None:
    html_path = Path(sys.argv[1])
    line_number = int(sys.argv[2])
    src_path = Path(sys.argv[3])
    text = html_path.read_text(encoding="utf-8")
    s, e = find_block(text, line_number)
    src = src_path.read_text(encoding="utf-8")
    # Sanity: source must parse
    import ast
    try:
        ast.parse(src)
    except SyntaxError as ex:
        raise SystemExit(f"source does not parse: {ex}")
    new_block = regen(src)
    new_text = text[:s] + new_block + text[e:]
    html_path.write_text(new_text, encoding="utf-8")
    print(f"OK replaced {e - s} bytes -> {len(new_block)} bytes in {html_path.name}")


if __name__ == "__main__":
    main()
