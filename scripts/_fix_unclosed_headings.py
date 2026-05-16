"""Fix unclosed heading tags book-wide.

The bug pattern: an <hN> opener is never followed by </hN>. The next block
element (a <p>, <div>, <ul>, <figure>, ...) opens INSIDE the still-open
heading, so the heading absorbs that block (and everything after it,
until the parser recovers). Result on the rendered page: a heading that
goes on for hundreds of pixels in bold/centered styling, callouts that
look empty because they're tucked inside the heading, missing line
breaks, the whole page looking corrupted.

Anchor case: section-30.1.html had 12 such unclosed <h3> tags. The
audit also looked for the same pattern across all content pages.

Fix shape: for each <hN id="..." ...>text-only content followed
immediately by a block-level child, insert the missing </hN> right
before the block opener.

Run from project root:
    python scripts/_fix_unclosed_headings.py [--dry-run]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude"}


def should_skip(p: Path) -> bool:
    return bool(set(p.parts) & SKIP_PARTS)


# Match an opening <hN ...> followed by text containing no tags, then
# directly a block-level child (p, div, ul, ol, figure, table, hN, blockquote)
# without an intervening </hN>. Capture the heading attributes and inner text.
UNCLOSED_RE = re.compile(
    r'(<h([1-6])\b[^>]*>)'           # group 1 = full opening tag, group 2 = level
    r'([^<]*?)'                       # group 3 = text content (no tags)
    r'(?=\s*<(?:p|div|ul|ol|figure|table|h[1-6]|blockquote)\b)',
    flags=re.IGNORECASE,
)


def fix_text(text: str) -> tuple[str, int]:
    """Return (new_text, count_fixed)."""
    fixed = 0

    def repl(m):
        nonlocal fixed
        # Check this isn't already followed by </hN> within the captured text
        # (the regex prevents that, but be defensive).
        level = m.group(2)
        # Look ahead in the original text to see if a </hN> already exists.
        # We rely on the regex anchor: the next non-whitespace MUST be a block
        # opener, so there's no </hN> between.
        fixed += 1
        return f'{m.group(1)}{m.group(3)}</h{level}>'

    new_text = UNCLOSED_RE.sub(repl, text)
    return new_text, fixed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    files_changed = 0
    total_fixed = 0
    per_file = []

    for p in ROOT.rglob("*.html"):
        if should_skip(p):
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        new_text, n = fix_text(text)
        if n > 0:
            rel = p.relative_to(ROOT)
            per_file.append((rel, n))
            if not args.dry_run:
                p.write_text(new_text, encoding="utf-8")
            files_changed += 1
            total_fixed += n

    for rel, n in per_file:
        print(f"  {rel}: {n} unclosed heading(s) fixed")
    print()
    print(f"TOTAL: {total_fixed} heading(s) closed across {files_changed} file(s)")
    if args.dry_run:
        print("(dry run; nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
