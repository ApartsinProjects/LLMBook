"""Post-optimizer pass: recompress JPEGs via MozJPEG and PNGs via OxiPNG.

Lossless or near-lossless additional savings on top of epub-optimizer:
  - MozJPEG: ~25-30% smaller than libjpeg at the same visual quality
  - OxiPNG:  ~10-25% smaller than oxipng-default (lossless)

v14.1: hash-keyed CACHE so unchanged images skip recompression.
  Cache lives at: ~/Tools/img-tools/cache/recompress/
  Key: SHA-256(image_bytes) + tool-args-hash. Value: optimized image bytes.
  Safe: content-addressed, immune to filename changes. If input changes,
  hash differs, cache miss, tool runs. If tool args change (e.g., quality),
  hash differs, cache miss, tool re-runs.

Usage:
  python _recompress_images.py path/to/book.epub [output.epub]

If output not given, recompresses in place.
"""
from __future__ import annotations
import hashlib
import os, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path

def _find_tool(*candidates: str) -> Path | None:
    """Resolve binary by trying candidate paths + which()."""
    for c in candidates:
        p = Path(c)
        if p.exists():
            return p
    return None

_TOOLS_ROOT = Path.home() / "Tools/img-tools/node_modules"
MOZJPEG = _find_tool(
    str(_TOOLS_ROOT / "mozjpeg/vendor/cjpeg.exe"),
    "C:/Users/apart/Tools/img-tools/node_modules/mozjpeg/vendor/cjpeg.exe",
)
OXIPNG = _find_tool(
    str(_TOOLS_ROOT / "oxipng-bin/vendor/win/oxipng.exe"),
    str(_TOOLS_ROOT / "oxipng-bin/vendor/oxipng.exe"),
    "C:/Users/apart/Tools/img-tools/node_modules/oxipng-bin/vendor/win/oxipng.exe",
)
if not MOZJPEG or not OXIPNG:
    print(f"[WARN] tools missing: mozjpeg={MOZJPEG}, oxipng={OXIPNG}")

# MozJPEG: BASELINE (-baseline) — Kindle's KFX renderer cannot reliably
# decode progressive JPEGs and silently fails KDP ingestion with the
# "processing failed" symptom after a 15-30 min delay. epub-optimizer
# (sharp + mozjpeg) also emits progressive by default; this step runs
# AFTER it and overwrites with baseline, fixing both layers at once.
# q=68: undercuts epub-optimizer's q=65 floor only when trellis-quant
# wins; otherwise epub-optimizer's bytes survive (already baseline-safe
# because fix_cover_image_kdp.py runs after as belt-and-suspenders).
MOZJPEG_ARGS = ["-quality", "68", "-baseline"]

# Phase 1 size-reduction (Edition 16+): downsample content JPEGs whose
# long edge exceeds MAX_CONTENT_JPEG_PX. Kindle's reading area is at most
# ~1600 px on the Scribe; 1000 px gives ~140 ppi at full image width,
# which matches paperback print quality and stays sharp on e-ink.
# Cover is explicitly exempt (KDP wants the canonical 1600x2560 ideal).
MAX_CONTENT_JPEG_PX = 1000
COVER_EXEMPT_NAMES = {"cover.jpg", "cover.jpeg"}

# OxiPNG: -o 4 (most aggressive non-zopfli), --strip safe (drop ancillary
# chunks like EXIF, color profiles, gamma — keep only safe-to-display data).
OXIPNG_ARGS = ["-o", "4", "--strip", "safe", "--quiet"]


# ----------------------------------------------------------------------
# v14.1: content-addressed cache for recompressed images
# ----------------------------------------------------------------------
CACHE_ROOT = Path.home() / "Tools" / "img-tools" / "cache" / "recompress"
CACHE_ROOT.mkdir(parents=True, exist_ok=True)

# Encode tool-args into cache key namespace so an args change invalidates.
# Also include the resize cap so changes to MAX_CONTENT_JPEG_PX invalidate.
_ARGS_FINGERPRINT_JPG = hashlib.sha256(
    ("mozjpeg|" + "|".join(MOZJPEG_ARGS) + f"|maxpx={MAX_CONTENT_JPEG_PX}").encode()
).hexdigest()[:8]
_ARGS_FINGERPRINT_PNG = hashlib.sha256(
    ("oxipng|" + "|".join(OXIPNG_ARGS)).encode()
).hexdigest()[:8]


def _cache_key(input_bytes: bytes, fmt: str) -> str:
    """Compute cache key from input bytes + tool-args fingerprint."""
    h = hashlib.sha256(input_bytes).hexdigest()
    suffix = _ARGS_FINGERPRINT_JPG if fmt == 'jpg' else _ARGS_FINGERPRINT_PNG
    return f'{h}.{suffix}.{fmt}'


def _cache_lookup(input_bytes: bytes, fmt: str) -> bytes | None:
    """Return cached optimized bytes or None."""
    key = _cache_key(input_bytes, fmt)
    path = CACHE_ROOT / key
    if path.exists():
        try:
            return path.read_bytes()
        except Exception:
            return None
    return None


def _cache_store(input_bytes: bytes, output_bytes: bytes, fmt: str) -> None:
    """Cache the optimized bytes keyed by input hash."""
    key = _cache_key(input_bytes, fmt)
    path = CACHE_ROOT / key
    try:
        path.write_bytes(output_bytes)
    except Exception:
        pass  # cache write is best-effort


# Stats for cache effectiveness reporting
_CACHE_STATS = {"jpg_hits": 0, "jpg_miss": 0, "png_hits": 0, "png_miss": 0}


def _maybe_downsample_jpeg(p: Path) -> bool:
    """Phase 1: downsample content JPEGs whose long edge exceeds threshold.
    Cover is exempt. Writes back to p as baseline JPEG q=92 (MozJPEG re-encodes
    at the final quality). Returns True if downsample happened.
    """
    if p.name.lower() in COVER_EXEMPT_NAMES:
        return False
    try:
        from PIL import Image
        with Image.open(p) as im:
            im.load()
            w, h = im.size
            if max(w, h) <= MAX_CONTENT_JPEG_PX:
                return False
            scale = MAX_CONTENT_JPEG_PX / max(w, h)
            new_w = max(1, int(round(w * scale)))
            new_h = max(1, int(round(h * scale)))
            if im.mode != 'RGB':
                im = im.convert('RGB')
            im_resized = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
            # Write back as baseline JPEG q=92; MozJPEG step will re-encode at q=78
            im_resized.save(p, format='JPEG', quality=92,
                            progressive=False, optimize=False)
        return True
    except Exception:
        return False


def _recompress_jpeg(p: Path) -> int:
    """Returns bytes saved (negative if larger). Uses content-addressed cache.

    Phase 1: if image is content (not cover) and long edge > MAX_CONTENT_JPEG_PX,
    downsample BEFORE MozJPEG. Cache key uses post-downsample bytes so cache
    hits remain valid across rebuilds.
    """
    orig = p.stat().st_size

    # Phase 1: downsample (cover-exempt) before cache lookup so cache key
    # represents the actually-encoded image, not the source.
    _maybe_downsample_jpeg(p)

    input_bytes = p.read_bytes()

    # Cache lookup first
    cached = _cache_lookup(input_bytes, 'jpg')
    if cached is not None and len(cached) < orig and len(cached) > 100:
        p.write_bytes(cached)
        _CACHE_STATS["jpg_hits"] += 1
        return orig - len(cached)
    _CACHE_STATS["jpg_miss"] += 1

    tmp = p.with_suffix(p.suffix + ".tmp")
    try:
        with open(tmp, "wb") as out_fh:
            subprocess.run(
                [str(MOZJPEG), *MOZJPEG_ARGS, str(p)],
                stdout=out_fh,
                stderr=subprocess.DEVNULL,
                check=True,
            )
        new_bytes = tmp.read_bytes()
        new = len(new_bytes)
        if new < orig and new > 100:
            # Save to cache before moving
            _cache_store(input_bytes, new_bytes, 'jpg')
            tmp.replace(p)
            return orig - new
        tmp.unlink(missing_ok=True)
        return 0
    except Exception:
        if tmp.exists():
            try:
                tmp.unlink()
            except Exception:
                pass
        return 0


def _recompress_png(p: Path) -> int:
    """Returns bytes saved. Uses content-addressed cache."""
    orig = p.stat().st_size
    input_bytes = p.read_bytes()

    # Cache lookup first
    cached = _cache_lookup(input_bytes, 'png')
    if cached is not None and len(cached) < orig:
        p.write_bytes(cached)
        _CACHE_STATS["png_hits"] += 1
        return orig - len(cached)
    _CACHE_STATS["png_miss"] += 1

    try:
        subprocess.run(
            [str(OXIPNG), *OXIPNG_ARGS, str(p)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        new = p.stat().st_size
        if new < orig:
            # Save optimized bytes to cache (keyed by original input)
            _cache_store(input_bytes, p.read_bytes(), 'png')
        return orig - new
    except Exception:
        return 0


def recompress_epub(in_path: Path, out_path: Path) -> dict:
    work = in_path.parent / "_recompress_temp"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()

    with zipfile.ZipFile(in_path) as z:
        z.extractall(work)

    stats = {"jpg_files": 0, "jpg_saved": 0, "png_files": 0, "png_saved": 0}

    for p in work.rglob("*"):
        if not p.is_file():
            continue
        ext = p.suffix.lower()
        if ext in (".jpg", ".jpeg"):
            saved = _recompress_jpeg(p)
            if saved > 0:
                stats["jpg_files"] += 1
                stats["jpg_saved"] += saved
        elif ext == ".png":
            saved = _recompress_png(p)
            if saved > 0:
                stats["png_files"] += 1
                stats["png_saved"] += saved

    if out_path.exists():
        out_path.unlink()
    mimetype = work / "mimetype"
    with zipfile.ZipFile(out_path, "w") as zout:
        if mimetype.exists():
            zout.write(mimetype, "mimetype", compress_type=zipfile.ZIP_STORED)
        for p in sorted(work.rglob("*")):
            if not p.is_file() or p == mimetype:
                continue
            arc = str(p.relative_to(work)).replace("\\", "/")
            zout.write(p, arc, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    shutil.rmtree(work)
    # Append cache stats to result for visibility
    stats.update({
        "cache_jpg_hits": _CACHE_STATS["jpg_hits"],
        "cache_jpg_miss": _CACHE_STATS["jpg_miss"],
        "cache_png_hits": _CACHE_STATS["png_hits"],
        "cache_png_miss": _CACHE_STATS["png_miss"],
    })
    return stats


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    in_p = Path(sys.argv[1])
    out_p = Path(sys.argv[2]) if len(sys.argv) > 2 else in_p
    before = in_p.stat().st_size
    s = recompress_epub(in_p, out_p)
    after = out_p.stat().st_size
    print(f"  MozJPEG: {s['jpg_files']} files, saved {s['jpg_saved']/1024:.0f} KB")
    print(f"  OxiPNG:  {s['png_files']} files, saved {s['png_saved']/1024:.0f} KB")
    print(f"  EPUB:    {before/1024/1024:.2f} MB -> {after/1024/1024:.2f} MB "
          f"({(after-before)/1024:.0f} KB delta, {after/before*100:.1f}% of input)")
