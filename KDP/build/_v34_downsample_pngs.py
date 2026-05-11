"""v3.4 Wave B: Downsample oversized source PNGs to 1500 px max long side.

Why: source PNGs sit at 3-4 MB each (full print resolution). Web display
maxes out at ~1200 px wide; print-bound 300 dpi sources are pure waste on
disk and slow git operations. EPUB pipeline already resizes these
independently to max_side=1000, so this script only affects:
  - source repo size
  - web image bandwidth
  - clone/checkout speed

Targets: PNGs > 500 KB. Resizes to max(width, height) = 1500 px while
preserving aspect ratio. Uses PIL with LANCZOS for high quality.
Skips PNGs whose larger dimension is already <= 1500 px.

Run from project root:
    /c/Python314/python KDP/build/_v34_downsample_pngs.py
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE = {"_archive", "KDP", "node_modules", "vendor", "scripts", ".git"}
TARGET = 1500
MIN_FILE_SIZE = 500_000


def main() -> int:
    try:
        from PIL import Image
    except ImportError:
        print("[error] Pillow not installed (pip install pillow)")
        return 1

    n_resized = 0
    saved_bytes = 0
    for p in ROOT.rglob("*.png"):
        if any(part in p.parts for part in EXCLUDE):
            continue
        size = p.stat().st_size
        if size < MIN_FILE_SIZE:
            continue
        try:
            img = Image.open(p)
        except Exception as e:
            print(f"  [skip] {p.name}: {e}")
            continue
        w, h = img.size
        long_side = max(w, h)
        if long_side <= TARGET:
            continue
        scale = TARGET / long_side
        new_size = (int(w * scale), int(h * scale))
        try:
            img2 = img.resize(new_size, Image.LANCZOS)
            # Preserve mode (RGBA stays RGBA) and metadata
            img2.save(p, format="PNG", optimize=True)
            new_size_bytes = p.stat().st_size
            saved = size - new_size_bytes
            saved_bytes += saved
            n_resized += 1
            print(f"  {w}x{h} -> {new_size[0]}x{new_size[1]}  "
                  f"({size//1024}KB -> {new_size_bytes//1024}KB)  "
                  f"{p.relative_to(ROOT).as_posix()}")
        except Exception as e:
            print(f"  [error] {p.name}: {e}")
            continue

    print(f"\nResized {n_resized} PNGs, saved {saved_bytes/1024/1024:.1f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
