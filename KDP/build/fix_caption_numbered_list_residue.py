"""Strip numbered-list residue from comparison-table-title captions.

ROOT CAUSE
  Some comparison-table-title captions were generated from a markdown
  numbered list. When the list item heading was lifted into a caption,
  the "N. " ordinal stayed. Example:
    <div class="comparison-table-title">
      <strong>Table 6.1.1f:</strong>
      <em>5. The Model Comparison Landscape (as of 2026).</em>
    </div>
  The "5. " in the body is meaningless inside a caption; it confuses
  the reader (table looks like it has a sub-number).

FIX
  For every <em>N. Rest of caption...</em> inside a *-caption block,
  strip the leading "N. " (1-2 digits, dot, single space).
  Idempotent. Safe (the pattern is specific enough not to false-positive
  on real sentences starting with digits).

Run:
  python KDP/build/fix_caption_numbered_list_residue.py
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# Caption containers we touch
CAPTION_CLASSES = (
    "comparison-table-title",
    "code-caption",
    "diagram-caption",
    "figure-caption",
)

# Match a caption div/p, then inside it an <em>N. ...</em> with leading digits
# Pattern is split into two passes so we only modify the FIRST <em> inside
# a caption block.
CAPTION_BLOCK_RE = re.compile(
    r'(<(?:div|p)[^>]*class="[^"]*(?:'
    + "|".join(CAPTION_CLASSES) + r')[^"]*"[^>]*>'
    r'(?:[^<]|<(?!em>))*?)'
    r'(<em>)\s*(\d{1,2})\.\s+',
    re.IGNORECASE,
)


def patch(text: str) -> tuple[str, int]:
    n = 0
    def repl(m: re.Match) -> str:
        nonlocal n
        n += 1
        return m.group(1) + m.group(2)
    new_text = CAPTION_BLOCK_RE.sub(repl, text)
    return new_text, n


def main() -> int:
    total_files = 0
    total_files_modified = 0
    total_fixes = 0
    skip_dirs = {"KDP", "node_modules", ".git", "source_fix_backups"}

    for path in ROOT.rglob("*.html"):
        # Skip build output, KDP build dirs, backups
        rel_parts = path.relative_to(ROOT).parts
        if any(p in skip_dirs for p in rel_parts):
            continue
        # Skip pure index files (no captions there typically)
        total_files += 1
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            print(f"WARN: cannot read {path}: {e}", file=sys.stderr)
            continue
        new_text, n = patch(text)
        if n:
            path.write_text(new_text, encoding="utf-8")
            total_files_modified += 1
            total_fixes += n
            print(f"  {n:3d}  {path.relative_to(ROOT)}")

    print()
    print(f"Files scanned:  {total_files}")
    print(f"Files modified: {total_files_modified}")
    print(f"Total fixes:    {total_fixes}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
