"""Compress oversized PNGs across the book to bring the EPUB under the
KDP 50 MB file-size budget.

Strategy per image:
  1. If the image is already <= max bytes, skip.
  2. If width > 1200 px, resize keeping aspect ratio so width == 1200 px.
     Most figures are 1500 x 1120 px, larger than any reflowable Kindle
     screen renders at 1x; 1200 px keeps retina-class crispness with ~36%
     fewer pixels.
  3. Save as PNG with optimize=True and reduced color palette where the
     image has <= 256 distinct colors (`P` mode via adaptive quantization),
     otherwise re-save as RGB optimized.
  4. If the result is still > target_bytes AND the image is non-photographic
     (diagram-like: few colors, lots of solid fills), convert to palette
     mode with 128-color adaptive palette.

Backups: original bytes are saved to .png.orig (skipped if .orig already
exists). Re-running won't overwrite the .orig.

Run from project root:
    python scripts/_compress_book_images.py [--dry-run] [--max-width N]
                                            [--target-kb N]
"""
from __future__ import annotations
import argparse
import shutil
import sys
from io import BytesIO
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude"}


def should_skip(p: Path) -> bool:
    return bool(set(p.parts) & SKIP_PARTS)


def compress_one(path: Path, max_width: int, target_bytes: int) -> tuple[int, int]:
    """Compress in-place. Returns (orig_size, new_size). Skips if already small."""
    orig_size = path.stat().st_size
    if orig_size <= target_bytes:
        return orig_size, orig_size  # already small enough

    # Backup if not already backed up
    backup = path.with_suffix(path.suffix + ".orig")
    if not backup.exists():
        shutil.copyfile(path, backup)

    img = Image.open(path)
    orig_mode = img.mode

    # Resize down if too wide
    if img.width > max_width:
        new_h = round(img.height * max_width / img.width)
        img = img.resize((max_width, new_h), Image.Resampling.LANCZOS)

    # Round 1: just optimize
    buf = BytesIO()
    save_kwargs = {"format": "PNG", "optimize": True}
    img.save(buf, **save_kwargs)
    candidate_bytes = buf.getvalue()
    candidate_size = len(candidate_bytes)

    # Round 2: if still too big, quantize to palette
    if candidate_size > target_bytes:
        if orig_mode != "P":
            # Adaptive 256-color palette
            quant = img.convert("RGB").quantize(colors=256, method=Image.Quantize.MEDIANCUT)
            buf = BytesIO()
            quant.save(buf, format="PNG", optimize=True)
            if len(buf.getvalue()) < candidate_size:
                candidate_bytes = buf.getvalue()
                candidate_size = len(candidate_bytes)

    # Round 3: if STILL too big, try 128-color palette
    if candidate_size > target_bytes:
        quant = img.convert("RGB").quantize(colors=128, method=Image.Quantize.MEDIANCUT)
        buf = BytesIO()
        quant.save(buf, format="PNG", optimize=True)
        if len(buf.getvalue()) < candidate_size:
            candidate_bytes = buf.getvalue()
            candidate_size = len(candidate_bytes)

    # Only write if we actually reduced size
    if candidate_size < orig_size:
        path.write_bytes(candidate_bytes)
        return orig_size, candidate_size
    # No improvement; restore backup and report no change
    return orig_size, orig_size


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--max-width", type=int, default=1200,
                    help="Resize wider images down to this width (px). Default 1200.")
    ap.add_argument("--target-kb", type=int, default=400,
                    help="Target max bytes per image (KB). Default 400.")
    args = ap.parse_args()

    target_bytes = args.target_kb * 1024
    total_orig = 0
    total_new = 0
    files_processed = 0
    files_compressed = 0

    candidates = []
    for p in ROOT.rglob("*.png"):
        if should_skip(p):
            continue
        if p.suffix == ".orig":
            continue
        if p.stat().st_size > target_bytes:
            candidates.append(p)

    print(f"Found {len(candidates)} PNGs over {args.target_kb} KB. Target: {args.max_width}px / {args.target_kb} KB")
    if args.dry_run:
        sample = sorted(candidates, key=lambda x: -x.stat().st_size)[:10]
        for p in sample:
            sz_kb = p.stat().st_size / 1024
            print(f"  {p.relative_to(ROOT)}: {sz_kb:,.0f} KB")
        return 0

    for p in candidates:
        try:
            orig, new = compress_one(p, args.max_width, target_bytes)
        except Exception as e:
            print(f"  ERR {p.relative_to(ROOT)}: {e}")
            continue
        files_processed += 1
        total_orig += orig
        total_new += new
        if new < orig:
            files_compressed += 1
            ratio = (1 - new / orig) * 100
            print(f"  {p.relative_to(ROOT)}: {orig//1024} KB -> {new//1024} KB ({ratio:.0f}%)")
        if files_processed % 50 == 0:
            print(f"    ... {files_processed}/{len(candidates)} processed, "
                  f"{(total_orig-total_new)/1024/1024:.1f} MB saved so far")

    saved_mb = (total_orig - total_new) / 1024 / 1024
    print()
    print(f"TOTAL: {files_compressed}/{files_processed} images compressed; "
          f"{saved_mb:.1f} MB saved "
          f"({total_orig/1024/1024:.1f} MB -> {total_new/1024/1024:.1f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
