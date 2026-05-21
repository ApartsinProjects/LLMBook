"""Wave 105: canonicalize `<div class="prereqs">` to `<div class="prerequisites">`.

The editing-leftover detector flagged 82 chapter index files using the
non-canonical class `prereqs` instead of the canonical `prerequisites`.
This script does the swap. Idempotent: only touches the exact class
string.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", "node_modules", "KDP", "build", "source_fix_backups",
        "pagefind", ".book-update", "vendor", ".claude", "_archive",
        "agents", "templates", "docs", "scripts"}

PREREQS_RE = re.compile(r'<div\s+class\s*=\s*"prereqs"')


def fix(p: Path) -> int:
    text = p.read_text(encoding="utf-8")
    new_text, n = PREREQS_RE.subn('<div class="prerequisites"', text)
    if n:
        p.write_text(new_text, encoding="utf-8")
    return n


def main():
    total = 0
    n_files = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP:
            continue
        n = fix(p)
        if n:
            n_files += 1
            total += n
            print(f"  + {p.relative_to(ROOT)}: {n} prereqs -> prerequisites")
    print(f"\nFiles touched: {n_files}, swaps: {total}")


if __name__ == "__main__":
    main()
