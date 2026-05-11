"""One-shot source-HTML fixer: rename `viewbox=` to `viewBox=` on all
<svg> elements.

Root cause: SVG spec defines `viewBox` (camelCase). Browsers parsing
HTML5 lenient-mode accept lowercase, but XHTML parsers (used by EPUB)
and Kindle's strict renderer ignore the misnamed attribute and fall
back to the SVG intrinsic size, causing diagrams to clip or render at
wrong dimensions.

Idempotent. Run from project root:
    /c/Python314/python KDP/build/_fix_svg_viewbox.py
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE_DIRS = {"_archive", "KDP", "node_modules", "vendor", "scripts"}

# Match <svg ... viewbox="..." ...> and rename the attribute, preserving
# everything else around it. Restrict to opening svg tags.
SVG_TAG = re.compile(r"(<svg\b[^>]*?\b)viewbox(=)", re.IGNORECASE)


def main() -> int:
    n_files = 0
    n_svgs = 0
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE_DIRS):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        if "viewbox" not in text.lower():
            continue
        new_text, count = SVG_TAG.subn(r"\1viewBox\2", text)
        if count > 0 and new_text != text:
            p.write_text(new_text, encoding="utf-8")
            n_files += 1
            n_svgs += count
            print(f"  {count:>3}x  {p.relative_to(ROOT).as_posix()}")
    # Also fix raw .svg files
    for p in ROOT.rglob("*.svg"):
        if any(part in p.parts for part in EXCLUDE_DIRS):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        new_text, count = SVG_TAG.subn(r"\1viewBox\2", text)
        if count > 0 and new_text != text:
            p.write_text(new_text, encoding="utf-8")
            n_files += 1
            n_svgs += count
            print(f"  {count:>3}x  {p.relative_to(ROOT).as_posix()}")
    print(f"\nFixed {n_svgs} SVG viewBox attributes across {n_files} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
