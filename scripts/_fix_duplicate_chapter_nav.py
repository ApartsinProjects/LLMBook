"""Remove duplicate <nav class="chapter-nav"> blocks from section files.

5 Tools-of-the-Trade sections shipped with two adjacent chapter-nav
blocks: the first with correct sibling-section prev/next, the second
with all three links pointing at index.html (stale fallback inserted
during an earlier author pass that didn't notice the prior block).

Keep the first; drop subsequent.

Idempotent. Run with --apply.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude", ".book-update"}

NAV_RE = re.compile(
    r'<nav\s+class="chapter-nav">.*?</nav>',
    re.DOTALL,
)


def fix(p: Path, dry_run: bool) -> int:
    text = p.read_text(encoding="utf-8")
    matches = list(NAV_RE.finditer(text))
    if len(matches) < 2:
        return 0
    # Keep the first, remove the rest. Walk in reverse to preserve indices.
    new_text = text
    for m in reversed(matches[1:]):
        # Also strip the immediately-trailing whitespace/newline so the
        # output stays tidy.
        end = m.end()
        while end < len(new_text) and new_text[end] in (' ', '\t', '\r', '\n'):
            end += 1
        new_text = new_text[:m.start()] + new_text[end:]
    if new_text == text:
        return 0
    if not dry_run:
        p.write_text(new_text, encoding="utf-8")
    return len(matches) - 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply

    total_files = 0
    total_navs_removed = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        n = fix(p, dry_run)
        if n:
            total_files += 1
            total_navs_removed += n
            print(f"  {p.relative_to(ROOT)} -> removed {n} duplicate nav block(s)")

    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"\n=== {mode} ===")
    print(f"Files affected:           {total_files}")
    print(f"Duplicate navs removed:   {total_navs_removed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
