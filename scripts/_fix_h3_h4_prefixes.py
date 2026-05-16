"""Fix stale H3/H4 numeric prefixes book-wide.

Root cause: when chapters are renumbered or sections are moved, the H2
prefixes get fixed by `_fix_section_audits.py` but H3/H4 sub-section
prefixes get left behind. Example: `section-9.5.html` has h3 starting
with "8.5.4.2 When the Reasoning Tax..." instead of "9.5.4.2 ...".

Generalized fix: for each `section-N.M.html` file, find every h3/h4
with a numeric prefix (A.B[.C[.D]]) that doesn't match `N.M`. Audit
revealed every affected file has exactly ONE wrong A.B prefix
throughout the file, so we can safely do a text-substitution from
`<h3>A.B.` -> `<h3>N.M.` (and same for h4).

Idempotent: only edits where the file's prefix doesn't already match.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude", ".book-update", "styles", "vendor", "scripts",
              "docs"}


def fix(p: Path, dry_run: bool) -> int:
    fn = p.name
    m = re.match(r'section-(\d+)\.(\d+)\.html', fn)
    if not m:
        return 0
    chapter, section = m.group(1), m.group(2)
    expected = f'{chapter}.{section}'
    text = p.read_text(encoding="utf-8")

    # Find all h3/h4 prefixes (A.B portion only)
    prefixes = Counter()
    for hm in re.finditer(r'<h([34])>(\d+\.\d+)(?:\.\d+){0,2}(?:\s|<)', text):
        prefixes[hm.group(2)] += 1
    wrong = [(ab, n) for ab, n in prefixes.items() if ab != expected]
    if not wrong:
        return 0
    if len(wrong) > 1:
        print(f'  WARNING mixed prefixes in {p.relative_to(ROOT)}: {dict(prefixes)}')
        return 0

    wrong_prefix = wrong[0][0]
    # Replace <h3>A.B. -> <h3>N.M. and <h4>A.B. -> <h4>N.M.
    # Also handle <h3>A.B<space/>...</h3> (3-segment exact match: "A.B Title")
    # but only when A.B is the wrong prefix.
    count = 0
    new_text = text
    for tag in ('h3', 'h4'):
        # <hN>A.B. -> <hN>N.M.
        old = f'<{tag}>{wrong_prefix}.'
        new = f'<{tag}>{expected}.'
        n = new_text.count(old)
        new_text = new_text.replace(old, new)
        count += n
        # <hN>A.B<space> -> <hN>N.M<space>  (2-segment heading like "8.5 Section")
        old2 = f'<{tag}>{wrong_prefix} '
        new2 = f'<{tag}>{expected} '
        n2 = new_text.count(old2)
        new_text = new_text.replace(old2, new2)
        count += n2

    if count > 0 and not dry_run:
        p.write_text(new_text, encoding="utf-8")
    return count


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply
    files_edited = 0
    total = 0
    for p in sorted(ROOT.rglob("section-*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        n = fix(p, dry_run)
        if n > 0:
            files_edited += 1
            total += n
    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"=== {mode} ===")
    print(f"Files edited:  {files_edited}")
    print(f"Prefix fixes:  {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
