"""Generate audit-only thumbnails for any PNG over 2000px in either dim.

Why: visual-inspection sub-agents hit a per-image dimension limit (2000px)
when many images are loaded in one session. By pre-shrinking the
oversized ones to a max dim of 1800px, sub-agents can do exhaustive
visual review without tripping the limit.

The thumbnails are NOT shipped to readers; they live in KDP/build/
audit_thumbs/ with the original directory structure preserved.

Usage: python thumbnail_audit_pngs.py
"""
from __future__ import annotations
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent.parent
OUT_ROOT = ROOT / "KDP" / "build" / "audit_thumbs"
MAX_DIM = 1800


def main() -> int:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    n_resized = 0
    n_copied = 0
    for src in ROOT.glob("part-*/module-*/images/*.png"):
        try:
            img = Image.open(src)
            w, h = img.size
        except Exception:
            continue

        rel = src.relative_to(ROOT)
        dst = OUT_ROOT / rel
        dst.parent.mkdir(parents=True, exist_ok=True)

        if max(w, h) <= MAX_DIM:
            # Small enough: skip (sub-agent can read original directly)
            continue

        # Shrink keeping aspect ratio
        img.thumbnail((MAX_DIM, MAX_DIM), Image.LANCZOS)
        img.save(dst, format="PNG", optimize=True)
        n_resized += 1

    print(f"Resized: {n_resized} oversized PNGs into {OUT_ROOT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
