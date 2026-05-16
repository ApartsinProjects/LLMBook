"""Fix glossary-link breakage from Wave 4 appendix renumber.

The Wave 4 renumber treated `section-f.*.html` paths as belonging to old
Appendix F (GPU Hardware -> new Appendix I), so it rewrote ALL
`section-f.N.html` references book-wide to `section-i.N.html`. The glossary
internally uses `section-f.N.html` filenames (legacy numbering for the 5
glossary sections F.1 through F.5) and was NOT supposed to be renamed.

Result: ~3,820 broken links of the form `appendices/glossary/section-i.*.html`
across 60+ files.

This script rewrites those specific links back to the correct path:
  glossary/section-i.<N>.html -> glossary/section-f.<N>.html

ONLY inside `appendices/glossary/...` paths. Other appendix-i references
(GPU Hardware) are unaffected.

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


def fix_file(p: Path, dry_run: bool) -> int:
    """Return number of replacements."""
    text = p.read_text(encoding="utf-8")
    orig = text
    # Match the wrong path: glossary/section-i.<N>.html (with optional fragment)
    text = re.sub(
        r"(/glossary/section-)i(\.\d+(?:\.\d+)?\.html)",
        r"\1f\2",
        text,
    )
    # Also handle the appendix-i match inside text that explicitly says
    # "Appendix F" but was rewritten to "Appendix I" by mistake:
    # the only case is the glossary, but Wave 4 renumber rewrote Appendix F
    # captions correctly. We don't touch "Appendix I" body text generally.
    if text == orig:
        return 0
    if not dry_run:
        p.write_text(text, encoding="utf-8")
    return text.count("glossary/section-f.") - orig.count("glossary/section-f.")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply
    total_files = 0
    total_changes = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        n = fix_file(p, dry_run)
        if n:
            total_files += 1
            total_changes += n
    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"{mode}: fixed glossary-link drift in {total_files} files "
          f"({total_changes} replacements)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
