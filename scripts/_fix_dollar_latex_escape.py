r"""Strip the LaTeX escape '\$' from rendered HTML.

`\$` is LaTeX syntax for "literal dollar sign in math mode". It leaked
into the rendered HTML during a build step (probably KaTeX or pandoc
passed it through unchanged). On every page that mentions currency or
prices, the reader sees `\$67,800` instead of `$67,800`, and inline
SVG diagrams with `\$` overflow their bounding rectangles because the
backslash widens the text width.

Replaces `\$` -> `$` book-wide except in:
- HTML pages under KDP / .claude / scripts / pagefind / templates / backups
- Math fragments where `\$` may be intentional (we don't bother carving
  these out because the book uses MathML/HTML math, not LaTeX in body)

Idempotent.
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude"}


def should_skip(p: Path) -> bool:
    return bool(set(p.parts) & SKIP_PARTS)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    files_changed = 0
    total = 0
    for p in ROOT.rglob("*.html"):
        if should_skip(p):
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        n = text.count(r"\$")
        if n == 0:
            continue
        # Replace `\$` with `$`. Only do so in HTML body text; SVG diagrams
        # share the same syntax escape problem so the same replacement applies.
        new_text = text.replace(r"\$", "$")
        if new_text != text:
            files_changed += 1
            total += n
            if not args.dry_run:
                p.write_text(new_text, encoding="utf-8")
    print(f"TOTAL: {total} `\\$` -> `$` replacements across {files_changed} files")
    if args.dry_run:
        print("(dry run; nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
