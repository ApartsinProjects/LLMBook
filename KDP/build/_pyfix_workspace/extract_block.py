"""Extract the raw Python source text from a pygmentized HTML block.

Usage:
    python extract_block.py <html_file> <line_number>

Prints the raw Python (HTML-decoded, all <span> tags stripped) so we can
re-indent it and feed it back through regenerate_block.py.
"""
from __future__ import annotations
import sys
import re
import html as ihtml
from pathlib import Path


def find_block(text: str, line_number: int) -> tuple[int, int, str]:
    """Find the <pre><code class="pygments-highlighted lang-python">...</code></pre>
    block that overlaps the given 1-indexed line number.

    Returns (start_offset, end_offset, inner_html).
    """
    # Index every line start
    line_starts = [0]
    for i, c in enumerate(text):
        if c == "\n":
            line_starts.append(i + 1)
    if line_number <= 0 or line_number > len(line_starts):
        raise SystemExit(f"line {line_number} out of range")
    target_offset = line_starts[line_number - 1]

    pat = re.compile(
        r'<pre><code class="pygments-highlighted lang-python">(.*?)</code></pre>',
        re.DOTALL,
    )
    nearest = None
    for m in pat.finditer(text):
        s, e = m.span()
        if s <= target_offset <= e:
            return s, e, m.group(1)
        d = min(abs(target_offset - s), abs(target_offset - e))
        if nearest is None or d < nearest[2]:
            nearest = (s, e, d, m.group(1))
    if nearest is not None:
        s, e, _d, inner = nearest
        return s, e, inner
    raise SystemExit("no pygments block found")


def spans_to_text(html: str) -> str:
    """Strip <span ...> and </span> from a pygmentized block, decode entities."""
    no_span = re.sub(r"</?span[^>]*>", "", html)
    return ihtml.unescape(no_span)


def main() -> None:
    path = Path(sys.argv[1])
    line_number = int(sys.argv[2])
    text = path.read_text(encoding="utf-8")
    s, e, inner = find_block(text, line_number)
    raw = spans_to_text(inner)
    print(f"# OFFSETS: {s} {e}")
    print(f"# RAW START")
    print(raw)
    print(f"# RAW END")


if __name__ == "__main__":
    main()
