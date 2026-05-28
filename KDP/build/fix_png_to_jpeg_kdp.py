"""Phase 2 size-reduction: convert opaque PNGs to JPEG when smaller.

CONSERVATIVE RULES (Kindle dark-mode safe):
  1. Only convert PNGs that are FULLY OPAQUE (no alpha channel and no
     palette `transparency` index). Dark-mode Kindle renders JPEG-with-
     fake-white-background as a bright white box on a dark page, which
     is an accessibility regression. PNG with transparency renders
     correctly in both light and dark mode.
  2. Only convert PNGs > 50 KB (smaller ones don't move the needle and
     JPEG header overhead can make them worse).
  3. Only commit the swap if the JPEG version is at least 25% smaller
     (otherwise keep PNG; PNG handles flat regions better at small sizes).
  4. Cover.jpg is never touched (already JPEG, exempt by ext).

After successful swap:
  - Rename file in EPUB from foo.png -> foo.jpg
  - Update OPF manifest media-type image/png -> image/jpeg AND href ext
  - Update every <img src="...foo.png"> across all XHTML to foo.jpg

Run AFTER MozJPEG/OxiPNG step (so PNGs are already optimized; only the
truly compression-resistant opaque PNGs get swapped). Run BEFORE the
three KDP post-build patches.
"""
from __future__ import annotations
import argparse
import io
import os
import re
import sys
import tempfile
import zipfile
from pathlib import Path
from PIL import Image


MIN_PNG_SIZE_BYTES = 50_000
MIN_SAVINGS_FRAC = 0.25  # JPEG must be >= 25% smaller
JPEG_QUALITY = 88        # Slightly higher than content (78) because PNG -> JPEG
                          # for diagrams needs to preserve text edges


def is_fully_opaque(img_bytes: bytes) -> bool:
    """True iff PIL detects no alpha and no palette-transparency-index."""
    try:
        with Image.open(io.BytesIO(img_bytes)) as im:
            im.load()
            if im.mode in ('RGBA', 'LA'):
                # Check actual alpha channel: if all pixels are 255, treat opaque
                alpha = im.getchannel('A')
                extrema = alpha.getextrema()
                return extrema[0] == 255 and extrema[1] == 255
            if im.mode == 'P':
                if 'transparency' in im.info:
                    return False
                return True
            if im.mode in ('RGB', 'L', '1'):
                return True
            # Other modes (e.g. CMYK, I, F) - skip conservatively
            return False
    except Exception:
        return False


def png_bytes_to_jpeg(png_bytes: bytes, quality: int = JPEG_QUALITY) -> bytes:
    with Image.open(io.BytesIO(png_bytes)) as im:
        im.load()
        if im.mode != 'RGB':
            im = im.convert('RGB')
        out = io.BytesIO()
        im.save(out, format='JPEG', quality=quality,
                progressive=False, optimize=True, subsampling=0)  # 4:4:4 chroma
        return out.getvalue()


def patch(epub_path: Path) -> dict:
    stats = {
        'png_scanned': 0,
        'png_skipped_small': 0,
        'png_skipped_transparent': 0,
        'png_skipped_jpeg_larger': 0,
        'png_converted': 0,
        'bytes_saved': 0,
        'opf_refs_rewritten': 0,
        'xhtml_files_modified': 0,
        'xhtml_refs_rewritten': 0,
    }
    rename_map = {}   # old_full_path -> new_full_path (e.g. 'EPUB/img/x.png' -> 'EPUB/img/x.jpg')
    new_bytes = {}    # new_full_path -> JPEG bytes
    delete_paths = set()

    # Pass 1: scan PNGs, decide conversions
    with zipfile.ZipFile(epub_path, 'r') as zin:
        for info in zin.infolist():
            name = info.filename
            if not name.lower().endswith('.png'):
                continue
            stats['png_scanned'] += 1
            if info.file_size < MIN_PNG_SIZE_BYTES:
                stats['png_skipped_small'] += 1
                continue
            data = zin.read(name)
            if not is_fully_opaque(data):
                stats['png_skipped_transparent'] += 1
                continue
            try:
                jpeg_bytes = png_bytes_to_jpeg(data)
            except Exception:
                stats['png_skipped_transparent'] += 1
                continue
            if len(jpeg_bytes) >= info.file_size * (1 - MIN_SAVINGS_FRAC):
                stats['png_skipped_jpeg_larger'] += 1
                continue
            new_name = name[:-4] + '.jpg'  # strip .png, add .jpg
            rename_map[name] = new_name
            new_bytes[new_name] = jpeg_bytes
            delete_paths.add(name)
            stats['png_converted'] += 1
            stats['bytes_saved'] += info.file_size - len(jpeg_bytes)

    if not rename_map:
        print('  no PNG conversions')
        return stats

    # Build basename rename map for href rewrites (basenames are unique by hash prefix)
    basename_rename = {
        old.split('/')[-1]: new.split('/')[-1]
        for old, new in rename_map.items()
    }

    # Pass 2: rewrite EPUB
    tmp_out = epub_path.with_suffix(epub_path.suffix + '.tmp')
    with zipfile.ZipFile(epub_path, 'r') as zin, \
         zipfile.ZipFile(tmp_out, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zout:
        # mimetype first uncompressed
        for info in zin.infolist():
            if info.filename == 'mimetype':
                zout.writestr(info, zin.read(info.filename),
                              compress_type=zipfile.ZIP_STORED)
                break

        for info in zin.infolist():
            if info.filename == 'mimetype':
                continue
            name = info.filename
            data = zin.read(name)

            # If this is a PNG we're swapping, skip writing it; we write the JPEG instead
            if name in delete_paths:
                # Write the new JPEG with same metadata except name
                new_name = rename_map[name]
                new_data = new_bytes[new_name]
                zout.writestr(new_name, new_data, compress_type=zipfile.ZIP_DEFLATED)
                continue

            # OPF: rewrite manifest item href and media-type
            if name.lower().endswith('.opf'):
                text = data.decode('utf-8', errors='ignore')
                orig = text
                for old_bn, new_bn in basename_rename.items():
                    # rewrite href="...old_bn" and media-type="image/png" on same item line
                    # be conservative: rewrite href first then verify same item has png media-type
                    def _rewrite_item(m, _old=old_bn, _new=new_bn):
                        item = m.group(0)
                        if _old in item:
                            item = item.replace(_old, _new)
                            item = item.replace('media-type="image/png"',
                                                'media-type="image/jpeg"')
                        return item
                    text = re.sub(r'<item\b[^/>]*?/?>', _rewrite_item, text)
                if text != orig:
                    stats['opf_refs_rewritten'] += len(basename_rename)
                data = text.encode('utf-8')

            # XHTML/HTML: rewrite <img src> references
            elif name.lower().endswith(('.xhtml', '.html')):
                text = data.decode('utf-8', errors='ignore')
                orig = text
                local_n = 0
                for old_bn, new_bn in basename_rename.items():
                    if old_bn in text:
                        # Only rewrite when in src= or href= contexts to avoid
                        # touching incidental strings in body text
                        new_text, n1 = re.subn(
                            r'(\bsrc=")([^"]*?)(' + re.escape(old_bn) + r')(")',
                            lambda m: m.group(1) + m.group(2) + new_bn + m.group(4),
                            text,
                        )
                        text = new_text
                        local_n += n1
                if text != orig:
                    stats['xhtml_files_modified'] += 1
                    stats['xhtml_refs_rewritten'] += local_n
                    data = text.encode('utf-8')

            zout.writestr(name, data, compress_type=zipfile.ZIP_DEFLATED)

    os.replace(tmp_out, epub_path)
    return stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('epub', type=Path)
    args = ap.parse_args()
    if not args.epub.exists():
        sys.exit(f'EPUB not found: {args.epub}')
    print(f'Patching {args.epub}')
    s = patch(args.epub)
    print(f'  PNGs scanned:              {s["png_scanned"]}')
    print(f'  PNGs converted to JPEG:    {s["png_converted"]}')
    print(f'  bytes saved:               {s["bytes_saved"]/1024:.0f} KB '
          f'({s["bytes_saved"]/1024/1024:.2f} MB)')
    print(f'  skipped (too small):       {s["png_skipped_small"]}')
    print(f'  skipped (has transparency): {s["png_skipped_transparent"]}')
    print(f'  skipped (jpeg not smaller): {s["png_skipped_jpeg_larger"]}')
    print(f'  OPF item refs rewritten:   {s["opf_refs_rewritten"]}')
    print(f'  XHTML files modified:      {s["xhtml_files_modified"]}')
    print(f'  XHTML <img src> rewrites:  {s["xhtml_refs_rewritten"]}')
    print('DONE.')


if __name__ == '__main__':
    main()
