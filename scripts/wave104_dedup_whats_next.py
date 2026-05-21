"""Wave 104: Remove duplicate whats-next callouts.

Six sections in module-21 and module-22 have TWO consecutive whats-next
callouts. The first is the substantive one (with a descriptive title
like "What's Next: VLMs Redefine the Cost-Accuracy Frontier"); the
second is a generic boilerplate pointing to the next section. Removing
the second keeps the more informative one.

This script deletes any whats-next callout that is the SECOND of two
in the same section, preserving the first (which is canonical per the
SECTION_ORDER plugin: whats-next should precede bibliography).
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", "node_modules", "KDP", "build", "source_fix_backups",
        "pagefind", ".book-update", "vendor", ".claude", "_archive",
        "agents", "templates", "docs", "scripts"}

WHATS_NEXT_OPEN_RE = re.compile(
    r'<div\s+class="callout\s+whats-next"[^>]*>',
    re.IGNORECASE,
)


def _matching_div_end(text: str, after_open: int) -> int:
    """Return position AFTER matching </div>."""
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


def fix_file(p: Path) -> int:
    text = p.read_text(encoding="utf-8")
    opens = list(WHATS_NEXT_OPEN_RE.finditer(text))
    if len(opens) <= 1:
        return 0
    # Find the SECOND whats-next and delete it (and trailing whitespace)
    second = opens[1]
    end = _matching_div_end(text, second.end())
    if end < 0:
        return 0
    # Strip leading whitespace before the second block too
    block_start = second.start()
    while block_start > 0 and text[block_start - 1] in ' \t':
        block_start -= 1
    # Include trailing newline if any
    block_end = end
    while block_end < len(text) and text[block_end] in '\n':
        block_end += 1
    new_text = text[:block_start].rstrip(' \t\n') + '\n' + text[block_end:]
    p.write_text(new_text, encoding="utf-8")
    return 1


def main():
    n_files = 0
    for p in sorted(ROOT.rglob("section-*.html")):
        if set(p.parts) & SKIP:
            continue
        n = fix_file(p)
        if n:
            n_files += 1
            print(f"  - {p.relative_to(ROOT)}: removed duplicate whats-next")
    print(f"\nFiles touched: {n_files}")


if __name__ == "__main__":
    main()
