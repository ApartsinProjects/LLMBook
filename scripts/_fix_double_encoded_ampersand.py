"""Fix double-encoded `&amp;amp;` -> `&amp;` book-wide.

Root cause: somewhere in the chrome-regeneration pipeline (prev/next
section labels, breadcrumbs, page-current titles), a section title
like "3D Asset Generation & Neural Scenes" was HTML-escaped to
"3D Asset Generation &amp; Neural Scenes" once during source authoring,
then re-escaped again to "&amp;amp;" during a later automated rewrite.
Result: browser renders the literal text `&amp;` in nav labels.

Generalized fix: book-wide text replace `&amp;amp;` -> `&amp;`. Safe
because the only way `&amp;amp;` should appear in HTML output is via
double-encoding accident.

Idempotent: re-runs find no `&amp;amp;` and do nothing.
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude", ".book-update", "vendor"}

OLD = "&amp;amp;"
NEW = "&amp;"


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
        text = p.read_text(encoding="utf-8")
        if OLD not in text:
            continue
        n = text.count(OLD)
        new_text = text.replace(OLD, NEW)
        files_edited += 1
        total += n
        if not dry_run:
            p.write_text(new_text, encoding="utf-8")
    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"=== {mode} ===")
    print(f"Files edited:  {files_edited}")
    print(f"Replacements:  {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
