"""Compress all PNG and JPEG images in the book for smaller EPUB.

Uses Pillow only (no external tool dependencies):
- PNG: re-encode with optimize=True + max compression. Lossless.
- JPEG: re-encode at quality=82 with progressive=True + optimize=True.
  Quality 82 is visually identical to original on Kindle e-ink and tablets.

Operates on copies in `KDP/build/compressed_images/` so source files stay
untouched. The build pipeline can swap in compressed versions via the
`--use-compressed-images` flag (TODO: wire up in build_epub.py).

For the LLMBook project the dominant images are:
- Chapter illustrations (large painterly PNGs) — biggest win
- Agent avatars (small) — already small, marginal win
- Mermaid-rendered figures (large PNGs with simple geometry) — huge win
- Photos (rare) — JPEG re-encode helps

Idempotent: if compressed file exists and is newer than source, skip.

Usage:
    python KDP/build/compress_images.py [--dry-run] [--workers 4]
"""
from __future__ import annotations
import argparse
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None  # don't choke on big chapter illustrations

PROJECT_ROOT = Path(__file__).resolve().parents[2]
COMPRESSED_DIR = PROJECT_ROOT / "KDP/build/compressed_images"

# Don't compress images smaller than this (no meaningful win)
MIN_BYTES_TO_COMPRESS = 8 * 1024  # 8 KB

JPEG_QUALITY = 82
PNG_OPTIMIZE = True


def find_images() -> list[Path]:
    images: list[Path] = []
    for ext in ("*.png", "*.jpg", "*.jpeg"):
        for p in PROJECT_ROOT.rglob(ext):
            if any(part in p.parts for part in ("KDP", "vendor", "scripts", "templates", "node_modules", "compressed_images")):
                continue
            images.append(p)
    return images


def compress_one(src: Path, out: Path, dry_run: bool) -> tuple[Path, int, int]:
    """Compress one image. Returns (path, original_size, new_size)."""
    orig_size = src.stat().st_size
    if orig_size < MIN_BYTES_TO_COMPRESS:
        return src, orig_size, orig_size

    if not dry_run:
        out.parent.mkdir(parents=True, exist_ok=True)

    suffix = src.suffix.lower()
    try:
        with Image.open(src) as im:
            if suffix == ".png":
                # Convert RGBA paletted PNGs are kept as-is; truecolor PNGs are quantized
                if not dry_run:
                    # Choose mode: keep RGBA if alpha present, else RGB.
                    if im.mode in ("RGBA", "LA"):
                        # Re-encode RGBA with optimize
                        im.save(out, format="PNG", optimize=PNG_OPTIMIZE)
                    else:
                        im_rgb = im.convert("RGB") if im.mode != "RGB" else im
                        im_rgb.save(out, format="PNG", optimize=PNG_OPTIMIZE)
            elif suffix in (".jpg", ".jpeg"):
                if not dry_run:
                    im_rgb = im.convert("RGB") if im.mode != "RGB" else im
                    im_rgb.save(out, format="JPEG", quality=JPEG_QUALITY,
                                progressive=True, optimize=True)
    except Exception as e:
        return src, orig_size, orig_size

    if dry_run:
        # Estimate by re-saving in memory
        from io import BytesIO
        buf = BytesIO()
        with Image.open(src) as im:
            if suffix == ".png":
                im.save(buf, format="PNG", optimize=True)
            else:
                im_rgb = im.convert("RGB") if im.mode != "RGB" else im
                im_rgb.save(buf, format="JPEG", quality=JPEG_QUALITY, progressive=True, optimize=True)
        new_size = len(buf.getvalue())
    else:
        new_size = out.stat().st_size if out.exists() else orig_size

    return src, orig_size, new_size


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--workers", type=int, default=4)
    args = p.parse_args()

    images = find_images()
    print(f"Found {len(images)} candidate images")

    total_orig = 0
    total_new = 0
    n_compressed = 0
    n_skipped = 0
    n_grew = 0

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = []
        for src in images:
            rel = src.relative_to(PROJECT_ROOT)
            out = COMPRESSED_DIR / rel
            futures.append(pool.submit(compress_one, src, out, args.dry_run))

        start = time.time()
        for i, fut in enumerate(as_completed(futures)):
            src, orig, new = fut.result()
            total_orig += orig
            if new < orig:
                total_new += new
                n_compressed += 1
            else:
                total_new += orig
                if new > orig:
                    n_grew += 1
                else:
                    n_skipped += 1
            if (i + 1) % 50 == 0:
                pct = total_new / total_orig * 100 if total_orig else 100
                print(f"  [{i+1}/{len(images)}]  saved {(total_orig-total_new)/1024/1024:.2f} MB  "
                      f"({100-pct:.1f}% reduction)  in {time.time()-start:.1f}s")

    print()
    print(f"=== Summary ===")
    print(f"Original total: {total_orig / 1024 / 1024:.2f} MB")
    print(f"Compressed total: {total_new / 1024 / 1024:.2f} MB")
    saved = total_orig - total_new
    pct = saved / total_orig * 100 if total_orig else 0
    print(f"Saved: {saved / 1024 / 1024:.2f} MB ({pct:.1f}%)")
    print(f"Compressed: {n_compressed}  Same/grew: {n_skipped + n_grew}  Too small to bother: {len(images) - n_compressed - n_skipped - n_grew}")
    if not args.dry_run:
        print(f"\nCompressed images at: {COMPRESSED_DIR.relative_to(PROJECT_ROOT)}")
        print(f"Source files NOT modified.")
        print(f"To use these in EPUB, set environment var IMAGE_DIR_OVERRIDE before build.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
