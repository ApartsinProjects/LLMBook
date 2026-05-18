"""Wave 94: Wrap bare <pre><code class="pygments-highlighted lang-X"> blocks
in <div class="code-block-wrapper">.

Many sections have code blocks without the canonical wrapper, which causes
non-standard margins / caption alignment / collapsibility behavior. This
wave finds bare blocks and wraps them, also pulling in adjacent
<div class="code-output"> and <div class="code-caption"> elements.

Conservative: only acts on Pygments-highlighted real code (lang-python,
lang-javascript, etc.), NOT on lang-text (which is typically pseudocode
inside algorithm callouts).
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", "node_modules", "KDP", "build", "source_fix_backups",
        "pagefind", ".book-update", "vendor", ".claude", "_archive",
        "agents", "templates", "docs", "scripts"}

# Match bare <pre><code class="pygments-highlighted lang-X">...</code></pre>
# where lang-X is NOT lang-text (which is pseudocode inside algorithm).
# Captures the WHOLE <pre>...</pre> block including code-output and
# code-caption that immediately follow.
BARE_BLOCK_RE = re.compile(
    r'(?P<pre><pre\b[^>]*>\s*<code\b[^>]*class="[^"]*pygments-highlighted[^"]*lang-(?!text\b)(\w+)[^"]*"[^>]*>'
    r'.*?</code>\s*</pre>)'
    r'(?P<after>(?:\s*<div\s+class="code-output"[^>]*>.*?</div>)?'
    r'\s*(?:<div\s+class="code-caption"[^>]*>.*?</div>)?)',
    re.IGNORECASE | re.DOTALL,
)


def is_already_wrapped(html: str, pos: int) -> bool:
    """Return True if pos is already inside a code-block-wrapper or
    other allowed container."""
    # Search backward for the nearest opening div tag with code-block-wrapper
    # OR the nearest callout algorithm opening.
    before = html[max(0, pos - 600):pos]
    # Count opens/closes of the wrapper
    wrap_opens = list(re.finditer(r'<div\s+class="code-block-wrapper"', before, re.IGNORECASE))
    if wrap_opens:
        last_open = wrap_opens[-1].start()
        # Count </div> between last_open and end
        depth_after = before[last_open:].count('</div>') - before[last_open:].count('<div')
        # If wrapper still open, we're inside it
        if depth_after < 0:
            return True
    # Check algorithm callout
    algo_opens = list(re.finditer(r'<div\s+class="callout algorithm"', before, re.IGNORECASE))
    if algo_opens:
        last_open = algo_opens[-1].start()
        depth_after = before[last_open:].count('</div>') - before[last_open:].count('<div')
        if depth_after < 0:
            return True
    # Inside a collapsible details
    det_opens = list(re.finditer(r'<details\b', before, re.IGNORECASE))
    det_closes = list(re.finditer(r'</details>', before, re.IGNORECASE))
    if len(det_opens) > len(det_closes):
        return True
    return False


def fix_file(p: Path) -> int:
    text = p.read_text(encoding="utf-8")
    if 'pygments-highlighted' not in text:
        return 0
    out = []
    pos = 0
    n = 0
    for m in BARE_BLOCK_RE.finditer(text):
        if is_already_wrapped(text, m.start()):
            continue
        # Build new block
        pre = m.group("pre")
        after = m.group("after")
        new_block = f'<div class="code-block-wrapper">\n{pre}{after}\n</div>'
        out.append(text[pos:m.start()])
        out.append(new_block)
        pos = m.end()
        n += 1
    if n == 0:
        return 0
    out.append(text[pos:])
    new = "".join(out)
    p.write_text(new, encoding="utf-8")
    return n


def main():
    n_files = 0
    n_total = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP:
            continue
        if not (p.name.startswith("section-") or p.name == "index.html"):
            continue
        n = fix_file(p)
        if n:
            n_files += 1
            n_total += n
            print(f"  + {p.relative_to(ROOT)}: {n} block(s) wrapped")
    print(f"\nFiles touched: {n_files}, blocks wrapped: {n_total}")


if __name__ == "__main__":
    main()
