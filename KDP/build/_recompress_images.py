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

# MozJPEG: progressive (-prog), trellis quant on, q=82 (visually similar to
# libjpeg q=88 but smaller). --strip removes EXIF/iCC profile metadata.
MOZJPEG_ARGS = ["-quality", "82", "-progressive"]

# OxiPNG: -o 4 (most aggressive non-zopfli), --strip safe (drop ancillary
# chunks like EXIF, color profiles, gamma — keep only safe-to-display data).
OXIPNG_ARGS = ["-o", "4", "--strip", "safe", "--quiet"]


# ----------------------------------------------------------------------
# v14.1: content-addressed cache for recompressed images
# ----------------------------------------------------------------------
CACHE_ROOT = Path.home() / "Tools" / "img-tools" / "cache" / "recompress"
CACHE_ROOT.mkdir(parents=True, exist_ok=True)

# Encode tool-args into cache key namespace so an args change invalidates.
_ARGS_FINGERPRINT_JPG = hashlib.sha256(
    ("mozjpeg|" + "|".join(MOZJPEG_ARGS)).encode()
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


def _recompress_jpeg(p: Path) -> int:
    """Returns bytes saved (negative if larger). Uses content-addressed cache."""
    orig = p.stat().st_size
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
