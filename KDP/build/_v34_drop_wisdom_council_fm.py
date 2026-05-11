"""v3.4: Drop wisdom-council.html and section-fm.7.html (the 42-Agent
Writing Team) from front matter.

Why: ~3500 words of meta about the production process; readers buying a
technical book about LLMs don't need a profile of every AI agent that
helped write it. The epigraphs throughout the book ALREADY carry agent
attributions, which we keep.

Mechanics:
  - Remove `<a href="...wisdom-council.html#xxx">Agent Name</a>` wrappers
    in epigraphs, leaving just the text and avatar
  - Remove `<a href="...section-fm.7.html...">...</a>` wrappers (any text)
  - Delete the two front-matter HTML files
  - Spine auto-regenerates without them

Preserves:
  - The epigraph (`<blockquote class="epigraph">`)
  - Agent attribution text (e.g., "Attn")
  - Agent avatar image
  - Agent description ("Gradient-Starved AI Agent")
  - Per-chapter Wisdom Council card panels (different from front matter
    page; already slimmed to 8 agents in the EPUB).

Run from project root:
    /c/Python314/python KDP/build/_v34_drop_wisdom_council_fm.py
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE = {"_archive", "KDP", "node_modules", "vendor", "scripts"}

DELETE_FILES = [
    "front-matter/wisdom-council.html",
    "front-matter/section-fm.7.html",
]

# Match <a href="...wisdom-council.html..." ...>TEXT</a> -> TEXT
# Greedy enough to handle href anywhere in attrs, including ../../front-matter/...
ANCHOR_RE = re.compile(
    r'<a\s+[^>]*href\s*=\s*"[^"]*(?:wisdom-council\.html|section-fm\.7\.html)[^"]*"[^>]*>(.*?)</a>',
    flags=re.IGNORECASE | re.DOTALL,
)


def main() -> int:
    n_files = 0
    n_anchors = 0
    delete_paths = {(ROOT / d).resolve() for d in DELETE_FILES}

    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE):
            continue
        if p.resolve() in delete_paths:
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        if "wisdom-council.html" not in text and "section-fm.7.html" not in text:
            continue
        new_text, count = ANCHOR_RE.subn(r"\1", text)
        if count > 0 and new_text != text:
            p.write_text(new_text, encoding="utf-8")
            n_files += 1
            n_anchors += count

    print(f"Unwrapped {n_anchors} anchors across {n_files} files")

    # Delete the front-matter pages
    print("\nDeleting front matter pages:")
    for rel in DELETE_FILES:
        f = ROOT / rel
        if f.exists():
            words = len(re.sub(r"<[^>]+>", " ",
                f.read_text(encoding="utf-8", errors="replace")).split())
            f.unlink()
            print(f"  rm {rel}  ({words:,} words)")
        else:
            print(f"  (gone) {rel}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
