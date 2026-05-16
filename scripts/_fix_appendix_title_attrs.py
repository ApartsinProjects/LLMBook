"""Fix stale `title="Appendix X: ..."` attributes on `<a>` tags that point
at appendix pages.

After the Wave 4 appendix renumber, hrefs were rewritten correctly
(appendix-j-* -> appendix-f-*) but the title= attribute on the same
anchor still said the OLD letter ("Appendix J: HuggingFace" -> should be
"Appendix F: HuggingFace").

This script: for every `<a href="...appendices/appendix-X-slug/..."
title="Appendix Y: ...">`, where X != Y, rewrite Y -> X.

Idempotent.
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

# Match: <a ... href="...appendix-X-slug/..." ... title="Appendix Y: ...">
# Captures the href letter (X) and title letter (Y).
PATTERN = re.compile(
    r'(<a[^>]*?\bhref="[^"]*?appendix-([a-z])-[^"]*?"[^>]*?\btitle=")Appendix\s+([A-Z]+)(:\s*[^"]*?")',
    re.S,
)


def rewrite_file(p: Path, dry_run: bool) -> int:
    text = p.read_text(encoding="utf-8")
    n = 0

    def repl(m: re.Match) -> str:
        nonlocal n
        href_letter = m.group(2).upper()
        title_letter = m.group(3)
        if href_letter == title_letter:
            return m.group(0)
        n += 1
        return f"{m.group(1)}Appendix {href_letter}{m.group(4)}"

    new = PATTERN.sub(repl, text)
    if n == 0:
        return 0
    if not dry_run:
        p.write_text(new, encoding="utf-8")
    return n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply
    total = 0
    files = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        n = rewrite_file(p, dry_run)
        if n:
            total += n
            files += 1
    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"{mode}: fixed {total} stale appendix title= attributes across {files} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
