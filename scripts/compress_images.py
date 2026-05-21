"""Near-lossless image compression pass for the book's raster assets.

PNG -> pngquant (quality 82-98, palette + strip): big wins on diagrams/illustrations,
       refuses to write if it cannot stay above quality 82, so quality is bounded.
JPG -> Pillow re-encode at quality 85, optimize + progressive, EXIF stripped.

Safety:
  - Only replaces a file if the new version is SMALLER and re-opens cleanly.
  - Skips tiny files (< 8 KB) and SVGs (vector).
  - --sample writes original+compressed copies side by side for visual QA;
    nothing in the book is touched until you run --apply.

Run:  py -3 scripts/compress_images.py                 # dry-run (projected savings)
      py -3 scripts/compress_images.py --sample 4      # QA copies -> .tools/_pilot
      py -3 scripts/compress_images.py --apply
"""
from __future__ import annotations
import argparse, subprocess, sys
from pathlib import Path
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / ".tools"
PNGQUANT = TOOLS / "pngquant" / "pngquant.exe"
SKIP = {"_archive", "node_modules", ".git", "vendor", ".claude", "__pycache__",
        ".book-update", ".tools", "KDP", "pagefind", "temp_epub"}
MINBYTES = 8 * 1024


def iter_images():
    for p in ROOT.rglob("*"):
        if p.is_dir() or any(s in p.parts for s in SKIP):
            continue
        if p.suffix.lower() in (".png", ".jpg", ".jpeg"):
            yield p


def compress_png(src: Path, dst: Path) -> bool:
    r = subprocess.run(
        [str(PNGQUANT), "--quality=82-98", "--strip", "--force",
         "--output", str(dst), str(src)],
        capture_output=True)
    return dst.exists()  # pngquant writes only if it met the quality floor


def compress_jpg(src: Path, dst: Path) -> bool:
    try:
        im = Image.open(src)
        if im.mode not in ("RGB", "L"):
            im = im.convert("RGB")
        im.save(dst, "JPEG", quality=85, optimize=True, progressive=True)
        return dst.exists()
    except Exception:
        return False


def make_compressed(p: Path, dst: Path) -> bool:
    return compress_png(p, dst) if p.suffix.lower() == ".png" else compress_jpg(p, dst)


def process(p: Path, apply: bool, tmp: Path):
    old = p.stat().st_size
    if old < MINBYTES:
        return old, old, "tiny"
    t = tmp / (p.stem + "__c" + p.suffix)
    if not make_compressed(p, t):
        return old, old, "fail"
    new = t.stat().st_size
    if new >= old:
        t.unlink(missing_ok=True)
        return old, old, "no-gain"
    try:
        Image.open(t).verify()
    except Exception:
        t.unlink(missing_ok=True)
        return old, old, "corrupt"
    if apply:
        t.replace(p)
    else:
        t.unlink(missing_ok=True)
    return old, new, "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--sample", type=int, default=0,
                    help="write N largest images as orig+compressed QA copies")
    args = ap.parse_args()
    tmp = TOOLS / "_cmp_tmp"
    tmp.mkdir(parents=True, exist_ok=True)

    if args.sample:
        qa = TOOLS / "_pilot" / "cmp_qa"
        qa.mkdir(parents=True, exist_ok=True)
        imgs = sorted(iter_images(), key=lambda p: -p.stat().st_size)[:args.sample]
        rows = []
        for p in imgs:
            c = qa / (p.stem + "__comp" + p.suffix)
            if make_compressed(p, c):
                o, n = p.stat().st_size, c.stat().st_size
                # also copy original for side-by-side
                orig = qa / (p.stem + "__orig" + p.suffix)
                orig.write_bytes(p.read_bytes())
                rows.append((p.name, o, n, orig, c))
                print(f"  {p.name}: {o/1e6:.2f}->{n/1e6:.2f} MB ({100*(o-n)/o:.0f}% off)")
        print(f"\nQA copies in {qa}")
        return

    old_t = new_t = 0
    n_ok = n_skip = 0
    by = {}
    for p in iter_images():
        o, n, status = process(p, args.apply, tmp)
        old_t += o
        new_t += n
        by[status] = by.get(status, 0) + 1
        if status == "ok":
            n_ok += 1
        else:
            n_skip += 1
    print(f"compressed(ok)={n_ok}  unchanged={n_skip}  detail={by}")
    print(f"total: {old_t/1e6:.1f} MB -> {new_t/1e6:.1f} MB "
          f"({100*(old_t-new_t)/old_t:.1f}% smaller, saves {(old_t-new_t)/1e6:.1f} MB) "
          f"{'[APPLIED]' if args.apply else '(dry-run)'}")


if __name__ == "__main__":
    main()
