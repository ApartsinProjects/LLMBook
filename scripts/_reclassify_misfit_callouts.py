"""Reclassify cross-ref / looking-back callouts whose titles are
insight-form ("X is Y") rather than reference-pointer labels.

Root cause: authors used `cross-ref` and `looking-back` as catch-all
"connect this idea to another section" wrappers, but the visual style
of those classes is subtle (light gray bg, low-contrast border) — meant
for actual pointers like "Canonical reference" or "Looking Back". When
the title is a sentence-form key insight ("Multi-view cross-attention
is long-document attention with cameras"), the reader sees a bordered
text-box that doesn't read as a callout at all.

Generalization: cross-ref / looking-back callouts with non-standard
titles get reclassified to `key-insight` (already a standard type in
the palette, with a visually distinctive style).

Standard reference titles that stay as cross-ref / looking-back:
  Looking Back, Looking back, Canonical reference, Cross-References,
  Cross-reference, Cross-references, See also, Scope

Idempotent: only reclassifies callouts whose title is NOT in the
standard set.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude", ".book-update", "styles", "vendor", "scripts",
              "docs"}

# Titles that should KEEP their cross-ref / looking-back classification.
KEEP_AS_CROSSREF = {
    "Canonical reference",
    "Cross-References",
    "Cross-reference",
    "Cross-references",
    "See also",
    "Scope",
}
KEEP_AS_LOOKING_BACK = {
    "Looking Back",
    "Looking back",
}


def fix(p: Path, dry_run: bool) -> int:
    text = p.read_text(encoding="utf-8")
    orig = text
    count = 0

    # Build a list of (start, end, new_class) substitutions.
    pat = re.compile(
        r'<div class="callout (cross-ref|looking-back)">\s*<div class="callout-title">([^<]+)</div>'
    )
    edits: list[tuple[int, int, str]] = []
    for m in pat.finditer(text):
        cls = m.group(1)
        title = m.group(2).strip()
        # Standard-label titles stay
        if cls == "cross-ref" and title in KEEP_AS_CROSSREF:
            continue
        if cls == "looking-back":
            # Allow "Looking Back: ..." (subtitled looking-backs)
            if title in KEEP_AS_LOOKING_BACK or title.startswith("Looking Back:") or title.startswith("Looking back:"):
                continue
        # Else: reclassify to key-insight
        # Replace the class attribute
        old = f'<div class="callout {cls}">'
        new = '<div class="callout key-insight">'
        edits.append((m.start(), m.start() + len(old), new))
        count += 1

    # Apply edits right-to-left to preserve offsets
    for start, end, new in reversed(edits):
        text = text[:start] + new + text[end:]

    if text != orig and not dry_run:
        p.write_text(text, encoding="utf-8")
    return count


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
        n = fix(p, dry_run)
        if n > 0:
            files_edited += 1
            total += n
    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"=== {mode} ===")
    print(f"Files edited:    {files_edited}")
    print(f"Reclassified:    {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
