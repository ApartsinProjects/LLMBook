"""Rewrite <img src="...svg-rasterized/X.svg"> to use the PNG version.

Counterpart to rasterize_svgs_to_png.js. Walks all section-*.html and
index.html (outside SKIP dirs) and rewrites every reference to a
standalone SVG (in images/svg-rasterized/) to point at the rasterized
PNG (images/svg-rasterized/png/X.png).

The PNG is bundled in the EPUB instead of the SVG, so KFX never sees
an SVG it can preprocess + inline + complain about. PNG is a binary
image format that goes through KFX's image pipeline (raster passthrough).

Idempotent.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = {"KDP", "node_modules", ".git", "_archive", "source_fix_backups"}

# Pattern: any <img src="...svg_<hash>.svg" ...>
SVG_REF_RE = re.compile(
    r'(<img[^>]*\bsrc=")([^"]*svg-rasterized/)([^"/]+\.svg)("[^>]*?)(/?>)',
    re.IGNORECASE,
)


def patch_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8", errors="replace")
    n = 0
    def repl(m: re.Match) -> str:
        nonlocal n
        n += 1
        svg_name = m.group(3)
        png_name = svg_name.replace(".svg", ".png")
        # Insert /png/ into the path
        return f'{m.group(1)}{m.group(2)}png/{png_name}{m.group(4)}{m.group(5)}'
    new_text = SVG_REF_RE.sub(repl, text)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return n
    return 0


def main() -> int:
    total_files = 0
    total_modified = 0
    total_refs = 0
    for path in ROOT.rglob("*.html"):
        rel = path.relative_to(ROOT)
        if any(p in SKIP for p in rel.parts):
            continue
        total_files += 1
        try:
            n = patch_file(path)
        except Exception as e:
            print(f"ERR {rel}: {e}", file=sys.stderr)
            continue
        if n:
            total_modified += 1
            total_refs += n
    print(f"Files scanned:  {total_files}")
    print(f"Files modified: {total_modified}")
    print(f"Total <img src> refs rewritten: {total_refs}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
