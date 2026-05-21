"""Wave 107: Move self-check callout to before the exercises h2/block.

Canonical order: ... key-takeaway -> self-check -> exercises -> ...

For sections where self-check ended up AFTER the exercises block,
this script identifies the self-check callout's block, removes it from
its current position, and inserts it BEFORE the first `<h2 id="exercises">`
heading (or `<section class="exercises">` opener) in the file.

Targets: section-1.4, section-6.3 (and any future cases the audit
surfaces). Idempotent: if self-check is already before exercises, no
change.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", "node_modules", "KDP", "build", "source_fix_backups",
        "pagefind", ".book-update", "vendor", ".claude", "_archive",
        "agents", "templates", "docs", "scripts"}

SELFCHECK_OPEN_RE = re.compile(
    r'<div\s+class="callout\s+self-check"[^>]*>',
    re.IGNORECASE,
)
EXERCISES_RE = re.compile(
    r'<h2\b[^>]*id="exercises"[^>]*>|<section\s+class="exercises"',
    re.IGNORECASE,
)


def _matching_div_end(text: str, after_open: int) -> int:
    """Return position AFTER the matching </div>."""
    open_re = re.compile(r'<div\b', re.IGNORECASE)
    close_re = re.compile(r'</div>', re.IGNORECASE)
    depth = 1
    pos = after_open
    while depth > 0 and pos < len(text):
        no = open_re.search(text, pos)
        nc = close_re.search(text, pos)
        if not nc:
            return -1
        if no and no.start() < nc.start():
            depth += 1
            pos = no.end()
        else:
            depth -= 1
            pos = nc.end()
    return pos if depth == 0 else -1


def fix(p: Path) -> int:
    text = p.read_text(encoding="utf-8")
    ex_m = EXERCISES_RE.search(text)
    if not ex_m:
        return 0
    ex_start = ex_m.start()
    # Find self-check AFTER the exercises position
    sc_m = SELFCHECK_OPEN_RE.search(text, ex_start)
    if not sc_m:
        return 0
    sc_block_start = sc_m.start()
    sc_block_end = _matching_div_end(text, sc_m.end())
    if sc_block_end < 0:
        return 0
    # Include trailing newline
    if sc_block_end < len(text) and text[sc_block_end] == "\n":
        sc_block_end += 1

    block = text[sc_block_start:sc_block_end]
    # Strip leading whitespace from the gap left behind
    new_text = (
        text[:ex_start]
        + block
        + "\n"
        + text[ex_start:sc_block_start].rstrip()
        + "\n"
        + text[sc_block_end:]
    )
    p.write_text(new_text, encoding="utf-8")
    return 1


def main():
    n = 0
    for p in sorted(ROOT.rglob("section-*.html")):
        if set(p.parts) & SKIP:
            continue
        if fix(p):
            n += 1
            print(f"  + {p.relative_to(ROOT)}")
    print(f"\nFiles touched: {n}")


if __name__ == "__main__":
    main()
