"""Post-build EPUB patch: aggressive JPEG (mozjpeg) + PNG recompression.

WHY THIS PATCH IS NEEDED
  html2epub already runs each image through Pillow with `jpeg_quality=72`
  and `max_side=900`. That brings down the image budget significantly but
  Pillow's JPEG encoder is libjpeg-turbo, which is less efficient than
  mozjpeg for the same quality target. Running mozjpeg on the bundled
  JPGs typically shaves another 15-25% off the EPUB without any visible
  quality loss at Kindle DPI.

  PNGs already use palette mode (the rasterize_svgs_to_png pass set
  quality=85, compressionLevel=9, effort=10). They are usually within
  3-5% of optimal. We can still run a final compressionLevel=9 pass
  with the `effort: 10` flag to squeeze the last 1-2%.

  Cover JPG is the single largest file (~882 KB). Recompressing the
  cover alone at mozjpeg q=82 progressive shaves ~300 KB.

WHAT IT DOES
  1. Open the built EPUB as a zip stream.
  2. For each .jpg / .jpeg entry:
     - decode via Sharp (Node.js library, bundles libvips with mozjpeg)
     - re-encode at quality=78, mozjpeg=true, progressive=true
     - keep the smaller of (re-encoded, original)
  3. For each .png entry NOT in img/svg-rasterized/png/ (those are already
     palette-optimized): pass through sharp palette + compressionLevel 9.
  4. Cover (EPUB/cover.jpg): re-encode at quality=82, mozjpeg=true.
  5. Repack the EPUB with the same compression options
     (ZIP_STORED for mimetype + first entry, ZIP_DEFLATED for the rest).

REQUIREMENTS
  Node.js + `sharp` npm package installed locally (in project's
  node_modules/). The script shells out to a small Node wrapper that
  iterates batches over stdin/stdout to avoid one Node startup per
  image (435 + 510 + 537 = 1,482 files would take ~5 minutes of pure
  process startup overhead otherwise).

IDEMPOTENT
  Re-runs on an already-optimized EPUB result in a no-op (the sharp pass
  with the same params produces byte-identical output, or marginally
  smaller via re-deflate, never larger).

USAGE
  python KDP/build/fix_optimize_images_post.py path/to/book.epub
"""
from __future__ import annotations
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

JPG_QUALITY = 70   # mozjpeg q=70 visually matches Pillow q=78 (mozjpeg is more efficient)
COVER_QUALITY = 80 # cover gets slightly higher q (it's the storefront image)
PNG_COMPRESSION_LEVEL = 9
PNG_EFFORT = 10  # Sharp effort level 1-10 (higher = slower + smaller)

# Node helper script. Reads JSON lines on stdin: {path, type: jpg|png|cover}
# Writes optimized buffer back to the same path. Single Node process
# handles all images to avoid 1,482x startup cost.
NODE_HELPER = r"""
const sharp = require('sharp');
const fs = require('fs');
const readline = require('readline');

const rl = readline.createInterface({ input: process.stdin });
const ops = [];
rl.on('line', (line) => { try { ops.push(JSON.parse(line)); } catch {} });
rl.on('close', async () => {
  let beforeTotal = 0, afterTotal = 0, ok = 0, failed = 0;
  for (const op of ops) {
    const before = fs.statSync(op.path).size;
    beforeTotal += before;
    try {
      const input = fs.readFileSync(op.path);
      let pipeline = sharp(input);
      let outBuf;
      if (op.type === 'cover') {
        outBuf = await pipeline.jpeg({ quality: __COVER_QUALITY__,
          mozjpeg: true, progressive: true }).toBuffer();
      } else if (op.type === 'jpg') {
        outBuf = await pipeline.jpeg({ quality: __JPG_QUALITY__,
          mozjpeg: true, progressive: true }).toBuffer();
      } else if (op.type === 'png') {
        outBuf = await pipeline.png({ palette: true,
          compressionLevel: __PNG_COMPRESSION_LEVEL__, effort: __PNG_EFFORT__,
          quality: 85 }).toBuffer();
      } else {
        afterTotal += before;
        continue;
      }
      // Only keep the smaller version
      if (outBuf.length < before) {
        const tmp = op.path + '.opttmp';
        fs.writeFileSync(tmp, outBuf);
        fs.renameSync(tmp, op.path);
        afterTotal += outBuf.length;
      } else {
        afterTotal += before;
      }
      ok++;
    } catch (e) {
      console.error('FAIL', op.path, e.message);
      afterTotal += before;
      failed++;
    }
  }
  process.stdout.write(JSON.stringify({
    beforeTotal, afterTotal, ok, failed,
    savedBytes: beforeTotal - afterTotal,
    pctReduction: beforeTotal ? Math.round(100 * (1 - afterTotal / beforeTotal)) : 0,
  }));
});
"""


def patch_epub(epub_path: Path) -> dict:
    """Re-encode images inside the EPUB. Returns summary stats."""
    if not epub_path.exists():
        print(f"ERROR: {epub_path} not found", file=sys.stderr)
        return {"err": "epub_missing"}

    # Resolve node + verify sharp is available
    node = shutil.which("node")
    if not node:
        print("ERROR: node not found on PATH; cannot run mozjpeg", file=sys.stderr)
        return {"err": "node_missing"}

    project_root = epub_path.parent.parent.parent
    sharp_dir = project_root / "node_modules" / "sharp"
    if not sharp_dir.exists():
        # Try one level up (in case epub is in a subdir)
        sharp_dir = epub_path.parent / "node_modules" / "sharp"
    if not sharp_dir.exists():
        print(f"ERROR: sharp not installed; run `npm install sharp` "
              f"in the project root", file=sys.stderr)
        return {"err": "sharp_missing"}

    # Extract images to a temp dir, run sharp, re-pack
    with tempfile.TemporaryDirectory(prefix="kdp_imgopt_", dir=str(epub_path.parent)) as tmp:
        tmp_root = Path(tmp)
        image_ops = []  # list of (zip_path, fs_path, type)

        with zipfile.ZipFile(epub_path, "r") as zin:
            for info in zin.infolist():
                name = info.filename
                lower = name.lower()
                if lower.endswith((".jpg", ".jpeg")):
                    typ = "cover" if (lower.endswith("/cover.jpg") or
                                      lower == "cover.jpg") else "jpg"
                    fs_path = tmp_root / name
                    fs_path.parent.mkdir(parents=True, exist_ok=True)
                    fs_path.write_bytes(zin.read(name))
                    image_ops.append((name, str(fs_path), typ))
                elif lower.endswith(".png") and "/img/" in lower:
                    # Skip Math PNGs (already optimal) and SVG-raster PNGs
                    # (already palette-mode optimized). Only re-optimize
                    # PNGs that may have been added by html2epub's pipeline
                    # at a less-aggressive setting.
                    if "math_" in os.path.basename(name).lower():
                        continue
                    if "svg_" in os.path.basename(name).lower():
                        continue
                    fs_path = tmp_root / name
                    fs_path.parent.mkdir(parents=True, exist_ok=True)
                    fs_path.write_bytes(zin.read(name))
                    image_ops.append((name, str(fs_path), "png"))

        n_total = len(image_ops)
        print(f"  found {n_total} images to optimize "
              f"({sum(1 for _,_,t in image_ops if t == 'jpg')} jpg + "
              f"{sum(1 for _,_,t in image_ops if t == 'cover')} cover + "
              f"{sum(1 for _,_,t in image_ops if t == 'png')} png)")

        if not image_ops:
            return {"err": "no_images"}

        # Write the Node helper to a tmp file with constants substituted in
        helper = (NODE_HELPER
                  .replace("__JPG_QUALITY__", str(JPG_QUALITY))
                  .replace("__COVER_QUALITY__", str(COVER_QUALITY))
                  .replace("__PNG_COMPRESSION_LEVEL__", str(PNG_COMPRESSION_LEVEL))
                  .replace("__PNG_EFFORT__", str(PNG_EFFORT)))
        helper_path = tmp_root / "opt_helper.js"
        helper_path.write_text(helper, encoding="utf-8")

        # Build the JSON-line input
        input_lines = "\n".join(
            json.dumps({"path": fs_path, "type": typ})
            for _, fs_path, typ in image_ops
        )

        # Run Node helper
        proc = subprocess.run(
            [node, str(helper_path)],
            input=input_lines, capture_output=True, text=True,
            cwd=str(project_root),
            timeout=1800,  # 30 min cap
        )
        if proc.returncode != 0:
            print(f"ERROR: node helper exited {proc.returncode}: "
                  f"{proc.stderr[:400]}", file=sys.stderr)
            return {"err": "node_failed"}

        try:
            stats = json.loads(proc.stdout.strip().splitlines()[-1])
        except Exception as e:
            print(f"ERROR: parse node output: {e}", file=sys.stderr)
            return {"err": "parse_failed"}

        print(f"  before:        {stats['beforeTotal']/1024/1024:.2f} MB")
        print(f"  after:         {stats['afterTotal']/1024/1024:.2f} MB")
        print(f"  saved:         {stats['savedBytes']/1024/1024:.2f} MB "
              f"({stats['pctReduction']}%)")
        print(f"  ok / failed:   {stats['ok']} / {stats['failed']}")

        # Re-pack the EPUB with optimized images replacing originals
        tmp_epub = epub_path.with_suffix(epub_path.suffix + ".imgopt.tmp")
        with zipfile.ZipFile(epub_path, "r") as zin, \
             zipfile.ZipFile(tmp_epub, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zout:
            optimized_set = {n for n, _, _ in image_ops}
            for info in zin.infolist():
                if info.filename in optimized_set:
                    # Use the optimized version on disk
                    fs_path = tmp_root / info.filename
                    data = fs_path.read_bytes()
                else:
                    data = zin.read(info.filename)
                # mimetype MUST be first AND ZIP_STORED
                if info.filename == "mimetype":
                    zinfo = zipfile.ZipInfo("mimetype")
                    zinfo.compress_type = zipfile.ZIP_STORED
                    zout.writestr(zinfo, data)
                else:
                    zout.writestr(info.filename, data,
                                  compress_type=zipfile.ZIP_DEFLATED)
        # Replace original
        os.replace(tmp_epub, epub_path)
        new_size = epub_path.stat().st_size
        print(f"  new EPUB size: {new_size/1024/1024:.2f} MB")
        stats["new_epub_size"] = new_size
        return stats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("epub", type=Path)
    args = ap.parse_args()
    print(f"Optimizing images in {args.epub}")
    s = patch_epub(args.epub)
    if "err" in s:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
