"""Add explicit width/height HTML attrs to math PNGs in the EPUB.

ROOT CAUSE
  The build pipeline generates math PNGs at MATH_PNG_SCALE = 3 (3x device
  pixels for crispness on retina screens). The `<img class="math-png-inline">`
  tags it inserts carry only `style="max-width:100%;height:auto"` and NO
  explicit HTML width/height attributes.

  Without width/height attrs, the EPUB reader displays the PNG at its
  NATURAL pixel size (3x intended), so inline math like `h_t = \\bar{A}h_{t-1}`
  renders 3x too large, breaking line flow.

  The CSS comment in epub_overrides.css already acknowledges this:
    "we deliberately do NOT set CSS height here so those attributes win
     (Kindle honors width/height attrs but ignores CSS max-height on <img>)"
  ...but the build never set those attrs. This patch sets them.

FIX
  For each <img class="math-png-{inline|display}"> in the EPUB:
    1. Locate the referenced PNG file (resolved relative to the xhtml location).
    2. Read its natural pixel width/height.
    3. Divide by MATH_PNG_SCALE (= 3) to get the LOGICAL CSS-pixel size.
    4. Add width="..." height="..." attributes to the img tag.

Idempotent: skips img tags that already have width and height attrs.

Usage:
  python KDP/build/fix_math_png_sizing.py path/to/book.epub
"""
from __future__ import annotations
import argparse
import os
import re
import struct
import sys
import zipfile
from pathlib import Path

# Must match html2epub/src/html2epub/math_render.py MATH_PNG_SCALE
MATH_PNG_SCALE = 3

# Match <img ...> tags with class math-png-{inline|display}, capturing the
# whole tag so we can rebuild with width/height attrs inserted.
IMG_RE = re.compile(
    r'<img\b([^>]*?\bclass="(?:math-png-inline|math-png-display)"[^>]*?)/?>',
    re.IGNORECASE,
)
SRC_RE = re.compile(r'\bsrc="([^"]+)"', re.IGNORECASE)
HAS_WIDTH_RE = re.compile(r'\bwidth="[^"]*"', re.IGNORECASE)
HAS_HEIGHT_RE = re.compile(r'\bheight="[^"]*"', re.IGNORECASE)


def png_dims(data: bytes) -> tuple[int, int] | None:
    """Extract PNG pixel width/height from header (no Pillow needed)."""
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    # IHDR chunk starts at offset 8, IHDR data at offset 16
    try:
        width, height = struct.unpack(">II", data[16:24])
        return width, height
    except struct.error:
        return None


def patch_xhtml(text: str, png_dim_lookup) -> tuple[str, int, int]:
    """Return (new_text, n_fixed, n_skipped)."""
    fixed = 0
    skipped = 0

    def repl(m: re.Match) -> str:
        nonlocal fixed, skipped
        attrs = m.group(1)
        if HAS_WIDTH_RE.search(attrs) and HAS_HEIGHT_RE.search(attrs):
            skipped += 1
            return m.group(0)  # Already has dims
        src_m = SRC_RE.search(attrs)
        if not src_m:
            skipped += 1
            return m.group(0)
        src = src_m.group(1)
        dims = png_dim_lookup(src)
        if dims is None:
            skipped += 1
            return m.group(0)
        nat_w, nat_h = dims
        css_w = max(1, round(nat_w / MATH_PNG_SCALE))
        css_h = max(1, round(nat_h / MATH_PNG_SCALE))
        # Insert width/height right after class="..."
        new_attrs = attrs + f' width="{css_w}" height="{css_h}"'
        fixed += 1
        return f"<img{new_attrs}/>"

    new_text = IMG_RE.sub(repl, text)
    return new_text, fixed, skipped


def build_png_index(z: zipfile.ZipFile) -> dict[str, tuple[int, int]]:
    """Map archive paths of PNGs -> (width, height)."""
    out: dict[str, tuple[int, int]] = {}
    for info in z.infolist():
        if not info.filename.lower().endswith(".png"):
            continue
        data = z.read(info.filename)
        d = png_dims(data)
        if d is not None:
            out[info.filename] = d
    return out


def patch_epub(epub_path: Path) -> dict:
    stats = {"files_scanned": 0, "files_modified": 0,
             "imgs_sized": 0, "imgs_skipped": 0}
    tmp = epub_path.with_suffix(epub_path.suffix + ".tmp")
    with zipfile.ZipFile(epub_path, "r") as zin:
        png_dim_map = build_png_index(zin)

        def lookup_for_xhtml(xhtml_archive_path: str):
            xhtml_dir = os.path.dirname(xhtml_archive_path)

            def resolver(src: str) -> tuple[int, int] | None:
                # Resolve src relative to the xhtml's archive directory
                full = os.path.normpath(os.path.join(xhtml_dir, src))
                full = full.replace(os.sep, "/")
                return png_dim_map.get(full)

            return resolver

        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
            for info in zin.infolist():
                data = zin.read(info.filename)
                if info.filename.lower().endswith((".xhtml", ".html")):
                    stats["files_scanned"] += 1
                    text = data.decode("utf-8", errors="replace")
                    resolver = lookup_for_xhtml(info.filename)
                    new_text, n_fixed, n_skipped = patch_xhtml(text, resolver)
                    stats["imgs_sized"] += n_fixed
                    stats["imgs_skipped"] += n_skipped
                    if new_text != text:
                        stats["files_modified"] += 1
                        data = new_text.encode("utf-8")
                comp = zipfile.ZIP_STORED if info.filename == "mimetype" else zipfile.ZIP_DEFLATED
                zout.writestr(info.filename, data, compress_type=comp)
    os.replace(tmp, epub_path)
    return stats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("epub", type=Path)
    args = ap.parse_args()
    if not args.epub.exists():
        print(f"ERROR: {args.epub} not found", file=sys.stderr)
        return 1
    print(f"Patching {args.epub}")
    s = patch_epub(args.epub)
    print(f"  Files scanned:    {s['files_scanned']}")
    print(f"  Files modified:   {s['files_modified']}")
    print(f"  <img> sized:      {s['imgs_sized']}")
    print(f"  <img> skipped:    {s['imgs_skipped']} (already-sized or src not found)")
    print("DONE.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
