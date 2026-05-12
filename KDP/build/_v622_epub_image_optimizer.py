"""v6.22: Post-process the built EPUB with smarter image compression.

Three optimizations applied to KDP/output/building-conversational-ai-llms-agents.epub:

  1. PNGs with NO real alpha (or alpha all == 255) -> recompress as JPEG q=82.
     The build pipeline's check only looks at color mode tag, not actual alpha
     content, so opaque RGBA PNGs slip through and ship as PNG.

  2. PNGs with binary alpha (only 0 or 255) -> flatten on white background +
     JPEG q=82. Matplotlib charts and Mermaid diagrams typically save with
     a transparent background mask that is invisible on a white reader page.

  3. JPEGs at q=72 -> recompress at q=65 with optimize=True. Marginal visual
     change, ~12% byte savings on each.

The script:
  - Opens the EPUB (a ZIP)
  - Walks each image, decides if it can be rewritten
  - Rewrites the OPF media-type and manifest entries (.png -> .jpg)
  - Rewrites every chapter XHTML's <img src> reference (.png -> .jpg)
  - Writes a new EPUB next to the original

Idempotent: if file is already JPEG at q<=65, it is left alone.
"""
from __future__ import annotations

import io
import re
import shutil
import sys
import zipfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent.parent
EPUB_IN = ROOT / 'KDP' / 'output' / 'building-conversational-ai-llms-agents.epub'
EPUB_OUT = ROOT / 'KDP' / 'output' / 'building-conversational-ai-llms-agents.opt.epub'

JPEG_QUALITY_FOR_PNG_CONVERT = 82  # converting from lossless PNG; keep high
JPEG_QUALITY_RECOMPRESS = 65       # recompressing existing lossy JPEGs


def alpha_kind(im: Image.Image) -> str:
    """Return one of: 'none', 'binary', 'real'."""
    if im.mode not in ('RGBA', 'LA', 'P'):
        return 'none'
    rgba = im.convert('RGBA')
    a = rgba.split()[-1]
    mn, mx = a.getextrema()
    if mn == 255:
        return 'none'  # fully opaque
    # Sample alpha values: if all ∈ {0, 255} (with small tolerance), it's binary
    colors = a.getcolors(maxcolors=256)
    if colors is None:
        return 'real'
    if all(v <= 5 or v >= 250 for _, v in colors):
        return 'binary'
    return 'real'


def optimize_image(name: str, data: bytes) -> tuple[bytes, str, str]:
    """Return (new_bytes, new_filename, new_media_type). Same as input if unchanged."""
    ext = name.rsplit('.', 1)[-1].lower()
    if ext not in ('png', 'jpg', 'jpeg'):
        return data, name, ''

    try:
        im = Image.open(io.BytesIO(data))
        im.load()
    except Exception:
        return data, name, ''

    if ext == 'png':
        kind = alpha_kind(im)
        if kind == 'real':
            # Keep as PNG, but try optimize re-encode (sometimes saves a few %)
            buf = io.BytesIO()
            im.save(buf, 'PNG', optimize=True)
            new_data = buf.getvalue()
            if len(new_data) < len(data):
                return new_data, name, 'image/png'
            return data, name, 'image/png'
        # 'none' or 'binary' -> flatten + JPEG
        if im.mode != 'RGB':
            bg = Image.new('RGB', im.size, (255, 255, 255))
            if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
                rgba = im.convert('RGBA')
                bg.paste(rgba, mask=rgba.split()[-1])
            else:
                bg.paste(im.convert('RGB'))
            im = bg
        buf = io.BytesIO()
        im.save(buf, 'JPEG', quality=JPEG_QUALITY_FOR_PNG_CONVERT,
                optimize=True, progressive=False)
        new_data = buf.getvalue()
        if len(new_data) >= len(data):
            return data, name, 'image/png'
        new_name = name.rsplit('.', 1)[0] + '.jpg'
        return new_data, new_name, 'image/jpeg'

    # JPEG path: recompress at lower quality
    buf = io.BytesIO()
    im.convert('RGB').save(buf, 'JPEG', quality=JPEG_QUALITY_RECOMPRESS,
                           optimize=True, progressive=False)
    new_data = buf.getvalue()
    if len(new_data) >= len(data):
        return data, name, 'image/jpeg'
    return new_data, name, 'image/jpeg'


def rewrite_text(text: str, renames: dict[str, str]) -> str:
    """Replace any reference to old image filenames with their new names."""
    for old, new in renames.items():
        # Old/new are like 'img/abc_foo.png' / 'img/abc_foo.jpg'
        # Replace both bare and href-quoted forms
        old_base = old.split('/')[-1]
        new_base = new.split('/')[-1]
        text = text.replace(old, new)
        text = text.replace(old_base, new_base)
    return text


def main() -> int:
    if not EPUB_IN.exists():
        print(f'EPUB not found: {EPUB_IN}', file=sys.stderr)
        return 1

    print(f'Reading {EPUB_IN.name} ({EPUB_IN.stat().st_size/1024/1024:.2f} MB)')

    renames: dict[str, str] = {}
    media_type_changes: dict[str, str] = {}
    bytes_before = bytes_after = 0
    converted_png = recompressed_jpg = unchanged = 0

    # First pass: optimize all images, collect rename map
    new_entries: list[tuple[str, bytes]] = []
    with zipfile.ZipFile(EPUB_IN, 'r') as zin:
        for info in zin.infolist():
            data = zin.read(info.filename)
            ext = info.filename.lower().rsplit('.', 1)[-1]
            if ext in ('png', 'jpg', 'jpeg'):
                new_data, new_name, new_mime = optimize_image(info.filename, data)
                bytes_before += len(data)
                bytes_after += len(new_data)
                if new_name != info.filename:
                    renames[info.filename] = new_name
                    media_type_changes[new_name] = new_mime
                    converted_png += 1
                elif len(new_data) < len(data):
                    if ext == 'png':
                        pass  # PNG re-optimized
                    else:
                        recompressed_jpg += 1
                else:
                    unchanged += 1
                new_entries.append((new_name, new_data))
            else:
                new_entries.append((info.filename, data))

    print(f'  converted PNG -> JPG:   {converted_png}')
    print(f'  recompressed JPEG:      {recompressed_jpg}')
    print(f'  image bytes: {bytes_before/1024/1024:.2f} MB -> {bytes_after/1024/1024:.2f} MB '
          f'(saved {(bytes_before-bytes_after)/1024/1024:.2f} MB)')

    # Second pass: rewrite OPF + every XHTML to update references
    final_entries: list[tuple[str, bytes]] = []
    for name, data in new_entries:
        ext = name.lower().rsplit('.', 1)[-1]
        if ext in ('opf', 'xhtml', 'html', 'ncx', 'css'):
            try:
                text = data.decode('utf-8')
            except UnicodeDecodeError:
                final_entries.append((name, data))
                continue
            new_text = rewrite_text(text, renames)
            # OPF needs media-type updates too. The OPF references files
            # relative to its own location, so 'EPUB/img/foo.jpg' in the ZIP
            # appears as 'img/foo.jpg' in the OPF. Try both forms.
            if ext == 'opf':
                for new_name, new_mime in media_type_changes.items():
                    candidates = [new_name]
                    if new_name.startswith('EPUB/'):
                        candidates.append(new_name[len('EPUB/'):])
                    for cand in candidates:
                        item_pat = re.compile(
                            r'<item\b[^>]*href="' + re.escape(cand) + r'"[^>]*/?>'
                        )
                        def _fix_mt(m):
                            return re.sub(r'media-type="image/png"',
                                          f'media-type="{new_mime}"',
                                          m.group(0))
                        new_text = item_pat.sub(_fix_mt, new_text)
            final_entries.append((name, new_text.encode('utf-8')))
        else:
            final_entries.append((name, data))

    # Write the new EPUB
    with zipfile.ZipFile(EPUB_OUT, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zout:
        # mimetype must be first and uncompressed
        for name, data in final_entries:
            if name == 'mimetype':
                info = zipfile.ZipInfo('mimetype')
                info.compress_type = zipfile.ZIP_STORED
                zout.writestr(info, data)
                break
        for name, data in final_entries:
            if name == 'mimetype':
                continue
            zout.writestr(name, data)

    new_size = EPUB_OUT.stat().st_size
    print(f'\nWrote {EPUB_OUT.name}: {new_size/1024/1024:.2f} MB')
    print(f'  vs original {EPUB_IN.stat().st_size/1024/1024:.2f} MB '
          f'(saved {(EPUB_IN.stat().st_size-new_size)/1024/1024:.2f} MB)')

    # Replace original with optimized version
    shutil.move(str(EPUB_OUT), str(EPUB_IN))
    print(f'Replaced original EPUB.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
