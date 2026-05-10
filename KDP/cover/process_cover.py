"""
Process the source book cover into a KDP-compliant JPEG.

KDP cover requirements (as of 2026):
  - Recommended dimensions: 1600 x 2560 px (1:1.6 aspect ratio).
  - Minimum: 1000 px on the longest side.
  - Format: JPEG (.jpg) or TIFF (.tif).
  - Color space: sRGB.
  - Max file size: 50 MB.

Source asset:
  - images/book-cover.png at 896 x 1200 px, RGB.
  - Below KDP's 1000 px longest-side minimum.
  - Aspect ratio is 0.747 (~3:4), KDP wants 0.625 (~5:8).

Strategy:
  1. Upscale source proportionally so longest side = 2560 px (Lanczos).
  2. Pad with average edge color to 1600 x 2560 to match KDP aspect ratio.
  3. Save as sRGB JPEG, quality 92.

Notes:
  Upscaling a 1200-px source 2.13x is a placeholder. For production,
  re-render the cover natively at 1600 x 2560.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from PIL import Image, ImageCms

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "images" / "book-cover.png"
OUT_DIR = ROOT / "KDP" / "cover"
OUT_SRC_COPY = OUT_DIR / "cover_source.png"
OUT_KDP = OUT_DIR / "cover_kdp.jpg"

KDP_W, KDP_H = 1600, 2560


def average_edge_color(im: Image.Image) -> tuple[int, int, int]:
    """Sample the four edges to pick a sensible padding color."""
    w, h = im.size
    samples = []
    for x in range(0, w, max(1, w // 50)):
        samples.append(im.getpixel((x, 0)))
        samples.append(im.getpixel((x, h - 1)))
    for y in range(0, h, max(1, h // 50)):
        samples.append(im.getpixel((0, y)))
        samples.append(im.getpixel((w - 1, y)))
    r = sum(s[0] for s in samples) // len(samples)
    g = sum(s[1] for s in samples) // len(samples)
    b = sum(s[2] for s in samples) // len(samples)
    return (r, g, b)


def main() -> int:
    if not SRC.exists():
        print(f"ERROR: source cover not found at {SRC}", file=sys.stderr)
        return 1

    print(f"Loading source: {SRC}")
    im = Image.open(SRC).convert("RGB")
    sw, sh = im.size
    print(f"  source size: {sw} x {sh}")

    OUT_SRC_COPY.write_bytes(SRC.read_bytes())
    print(f"  copied source -> {OUT_SRC_COPY.name}")

    src_aspect = sw / sh
    dst_aspect = KDP_W / KDP_H

    if src_aspect > dst_aspect:
        new_w = KDP_W
        new_h = round(KDP_W / src_aspect)
    else:
        new_h = KDP_H
        new_w = round(KDP_H * src_aspect)

    print(f"  scaling source to {new_w} x {new_h} (Lanczos)")
    scaled = im.resize((new_w, new_h), Image.Resampling.LANCZOS)

    pad = average_edge_color(scaled)
    print(f"  padding color (sampled from edges): rgb{pad}")

    canvas = Image.new("RGB", (KDP_W, KDP_H), pad)
    off_x = (KDP_W - new_w) // 2
    off_y = (KDP_H - new_h) // 2
    canvas.paste(scaled, (off_x, off_y))
    print(f"  composed canvas: {KDP_W} x {KDP_H}, source offset ({off_x}, {off_y})")

    try:
        srgb_profile = ImageCms.createProfile("sRGB")
        canvas.save(
            OUT_KDP,
            format="JPEG",
            quality=92,
            optimize=True,
            progressive=False,
            icc_profile=ImageCms.ImageCmsProfile(srgb_profile).tobytes(),
        )
    except Exception as e:
        print(f"  (could not embed sRGB ICC profile: {e}; saving without)")
        canvas.save(OUT_KDP, format="JPEG", quality=92, optimize=True, progressive=False)

    out_size = OUT_KDP.stat().st_size
    print(f"  wrote {OUT_KDP.name} ({out_size / 1024:.1f} KB)")

    if out_size > 50 * 1024 * 1024:
        print("  WARNING: file > 50 MB, exceeds KDP limit")
    else:
        print(f"  OK: file size {out_size / 1024:.1f} KB is well under 50 MB limit")

    print("\nDone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
