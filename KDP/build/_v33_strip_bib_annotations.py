"""v3.3 Tier 2: Strip <div class="bib-annotation"> blocks from bibliographies.

Each section's bibliography has ~5-10 entries, each with a 50-80 word
"annotation" that tends to repeat what the chapter prose already said.
Across 200 sections this is ~40-50K words of footer noise.

Citations (bib-ref) and category headers (bib-category) and meta tags
(bib-meta) are KEPT - just the editorial annotations are removed.

Run from project root:
    /c/Python314/python KDP/build/_v33_strip_bib_annotations.py
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE = {"_archive", "KDP", "node_modules", "vendor", "scripts"}

# Match <div class="bib-annotation">...</div> (single-line or multi-line).
# Use non-greedy to stop at first closing </div>. Annotations are flat divs
# with no nested divs in our codebase.
ANNOTATION_RE = re.compile(
    r'\s*<div\s+class="bib-annotation"[^>]*>.*?</div>\s*',
    re.DOTALL,
)


def main() -> int:
    n_files = 0
    n_annotations = 0
    n_words_saved = 0
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        if "bib-annotation" not in text:
            continue
        # Count words inside annotations before strip
        for m in ANNOTATION_RE.finditer(text):
            n_words_saved += len(re.sub(r"<[^>]+>", " ", m.group(0)).split())
        new_text, count = ANNOTATION_RE.subn("\n", text)
        if count > 0 and new_text != text:
            p.write_text(new_text, encoding="utf-8")
            n_files += 1
            n_annotations += count
            print(f"  {count:>3}x  {p.relative_to(ROOT).as_posix()}")
    print(f"\nStripped {n_annotations} bib annotations across {n_files} files")
    print(f"Words removed: ~{n_words_saved:,}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
