"""Produce a smaller, upload-friendly copy of the built EPUB by re-encoding its
JPEGs at a lower quality. Everything else (XHTML, PNGs incl. math, SVG, fonts,
CSS, OPF) is copied byte-for-byte, and the original EPUB is left untouched.

Only the JPEG bytes change, so the OPF media-types stay valid (jpeg stays jpeg)
and structure/validation are unaffected. mimetype is written first + stored so
the result is a valid EPUB.

JPEGs here are Gemini artwork/comics/hero images (not text diagrams - those are
SVG/vector + math PNGs, left untouched), so they downscale safely. The big size
lever is pixel dimensions, not quality (the JPEGs are already MozJPEG-optimized).

Usage: py -3 scripts/make_light_epub.py [quality] [maxdim]   (default 62 720)
Writes: KDP/output/building-conversational-ai-llms-agents-light.epub
"""
import io, os, sys, zipfile
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "KDP/output/building-conversational-ai-llms-agents.epub"
DST = ROOT / "KDP/output/building-conversational-ai-llms-agents-light.epub"
Q = int(sys.argv[1]) if len(sys.argv) > 1 else 62
MAXDIM = int(sys.argv[2]) if len(sys.argv) > 2 else 720

zin = zipfile.ZipFile(SRC)
infos = zin.infolist()
if DST.exists():
    DST.unlink()

n_jpg = 0
saved = 0
with zipfile.ZipFile(DST, "w") as zout:
    # mimetype MUST be first and uncompressed for a valid EPUB
    zout.writestr("mimetype", zin.read("mimetype"), compress_type=zipfile.ZIP_STORED)
    for info in infos:
        name = info.filename
        if name == "mimetype":
            continue
        data = zin.read(name)
        if name.lower().endswith((".jpg", ".jpeg")):
            try:
                im = Image.open(io.BytesIO(data))
                im = im.convert("RGB")  # drop alpha/CMYK/ICC quirks
                w, h = im.size
                if max(w, h) > MAXDIM:  # downscale artwork (real size lever)
                    scale = MAXDIM / max(w, h)
                    im = im.resize((max(1, round(w * scale)), max(1, round(h * scale))),
                                   Image.LANCZOS)
                buf = io.BytesIO()
                im.save(buf, format="JPEG", quality=Q, optimize=True, progressive=True)
                new = buf.getvalue()
                if len(new) < len(data):  # keep original if re-encode didn't help
                    saved += len(data) - len(new)
                    data = new
                    n_jpg += 1
            except Exception as e:
                print("  [keep original]", name.split("/")[-1], str(e)[:50])
        zout.writestr(name, data, compress_type=zipfile.ZIP_DEFLATED)

print(f"quality={Q}  recompressed {n_jpg} JPEGs, saved {saved/1024/1024:.1f} MB")
print(f"original: {SRC.stat().st_size/1024/1024:.1f} MB")
print(f"light:    {DST.stat().st_size/1024/1024:.1f} MB   -> {DST}")
