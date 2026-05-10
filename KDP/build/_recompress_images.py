"""Post-optimizer pass: recompress JPEGs via MozJPEG and PNGs via OxiPNG.

Lossless or near-lossless additional savings on top of epub-optimizer:
  - MozJPEG: ~25-30% smaller than libjpeg at the same visual quality
  - OxiPNG:  ~10-25% smaller than oxipng-default (lossless)

Usage:
  python _recompress_images.py path/to/book.epub [output.epub]

If output not given, recompresses in place.
"""
from __future__ import annotations
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


def _recompress_jpeg(p: Path) -> int:
    """Returns bytes saved (negative if larger)."""
    orig = p.stat().st_size
    tmp = p.with_suffix(p.suffix + ".tmp")
    try:
        with open(tmp, "wb") as out_fh:
            subprocess.run(
                [str(MOZJPEG), *MOZJPEG_ARGS, str(p)],
                stdout=out_fh,
                stderr=subprocess.DEVNULL,
                check=True,
            )
        new = tmp.stat().st_size
        if new < orig and new > 100:
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
    orig = p.stat().st_size
    try:
        subprocess.run(
            [str(OXIPNG), *OXIPNG_ARGS, str(p)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        new = p.stat().st_size
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
