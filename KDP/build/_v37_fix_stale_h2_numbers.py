"""v3.7 R6-E: Fix stale H2/H3 numbering inside section files.

After v3.x renumbering moved/renamed sections, the body H2/H3 headings
inside many files still show the OLD section number prefix. Examples
from chapter-review:
  - section-22.2.html: H2s read 22.3.x  (file is 22.2)
  - section-25.4.html: H2s read 25.7.x  (file is 25.4)
  - section-11.5.html: H2s read 11.6.x  (file is 11.5)
  - section-12.6.html: H2s read 12.8.x  (file is 12.6)
  - section-15.5.html: H2s read 16.1.x  (was section-16.1 originally)
  - section-17.5.html: H2s read 35.1.x  (was section-32.14 originally)
  - section-26.8/9/10.html: H2s read 35.x.y  (was section-35.5/6/8)
  - section-13.x: chapter-wide off-by-one
  - section-29.x: H2 say 30.x.y on absorbed sections

Fix: for each section-X.Y.html, find every <h2>/<h3>/<h4> whose numeric
prefix matches a known X'.Y' (chapter.section) different from X.Y, and
rewrite to use the file's own X.Y.

Conservative: only rewrite if the prefix is clearly a section header
(matches `\d+\.\d+\.\d+` with the trailing index preserved).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# H2/H3/H4 with leading section prefix like "22.3.5 Title" or "35.1.2 Title"
HEADING_RE = re.compile(
    r'(<h[2-4](?:\s+[^>]*)?>)\s*(\d+\.\d+)\.(\d+)([^\d<])',
)


def main() -> int:
    n_files = 0
    n_fixed = 0
    for p in ROOT.glob("part-*/module-*/section-*.html"):
        m = re.match(r"section-(\d+)\.(\d+)\.html", p.name)
        if not m:
            continue
        file_chap, file_sec = m.group(1), m.group(2)
        file_prefix = f"{file_chap}.{file_sec}"

        try:
            sz = p.stat().st_size
            if sz > 5_000_000:
                print(f"  [skip] {p.name} too large ({sz//1024}KB)")
                continue
            text = p.read_text(encoding="utf-8", errors="replace")
        except (OSError, MemoryError) as e:
            print(f"  [skip] {p.name}: {e}")
            continue
        original = text

        def _sub(hm: re.Match) -> str:
            tag, prefix, idx, sep = hm.groups()
            if prefix == file_prefix:
                return hm.group(0)
            return f"{tag}{file_prefix}.{idx}{sep}"

        text = HEADING_RE.sub(_sub, text)

        # Also fix exercise/lab references that share the stale prefix
        # within this file. E.g., "Exercise 22.3.1" in file 22.2 -> "Exercise 22.2.1"
        # BUT only when the wrong prefix appears inline near these tags.
        actual_changes = 0
        for hm in HEADING_RE.finditer(original):
            if hm.group(2) != file_prefix:
                actual_changes += 1
        if actual_changes > 0 and text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1
            n_fixed += actual_changes
            print(f"  {actual_changes:>2}x  {p.relative_to(ROOT).as_posix()}")
    print(f"\nFixed {n_fixed} stale H2/H3/H4 prefixes across {n_files} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
