"""Post-build EPUB patch: replace cover.jpg with a KDP-ideal baseline JPEG
and convert any progressive JPEG inside the book to baseline.

Why:
  The publish.py pipeline downsamples the canonical 1600x2560 cover to
  1000x1600 AND re-encodes it as a PROGRESSIVE JPEG. Both are independently
  risky for KDP's KFX renderer:

    * Progressive JPEGs are documented to trigger silent ingestion failures
      that surface as "processing failed" after a long delay.
    * 1600 px long edge is at KDP's floor (1000 minimum); ideal is 2560
      to match storefront thumbnails without resampling.

  The canonical source at KDP/cover/cover_kdp.jpg is already RGB, 1600x2560,
  baseline, no ICC, no EXIF. We swap it into the built EPUB verbatim, and
  also re-encode any other progressive JPEG in the book to baseline.

  All work is in-memory + atomic temp-file replace to avoid Windows file
  locks from extracted files being held by Explorer thumbnailers etc.

Run AFTER fix_cover_kdp_heuristic.py.
"""
from __future__ import annotations
import argparse
import io
import os
import sys
import tempfile
import zipfile
from pathlib import Path
from PIL import Image


def reencode_baseline(jpeg_bytes: bytes) -> bytes:
    img = Image.open(io.BytesIO(jpeg_bytes))
    if img.mode != 'RGB':
        img = img.convert('RGB')
    out = io.BytesIO()
    img.save(out, format='JPEG', quality=92, progressive=False, optimize=True)
    return out.getvalue()


def is_progressive(jpeg_bytes: bytes) -> bool:
    try:
        img = Image.open(io.BytesIO(jpeg_bytes))
        return bool(img.info.get('progressive') or img.info.get('progression'))
    except Exception:
        return False


def patch(epub_path: Path, canonical_cover: Path) -> dict:
    stats = {'cover_replaced': False, 'cover_before': 0, 'cover_after': 0,
             'progressive_reencoded': 0, 'total_jpegs': 0}
    if not canonical_cover.exists():
        raise SystemExit(f'Canonical cover not found: {canonical_cover}')
    new_cover = canonical_cover.read_bytes()

    # Build new EPUB in a sibling temp file, then atomically replace
    tmp_out = epub_path.with_suffix(epub_path.suffix + '.tmp')
    with zipfile.ZipFile(epub_path, 'r') as zin, \
         zipfile.ZipFile(tmp_out, 'w', zipfile.ZIP_DEFLATED) as zout:
        # mimetype FIRST, uncompressed
        for info in zin.infolist():
            if info.filename == 'mimetype':
                zout.writestr(info, zin.read(info.filename),
                              compress_type=zipfile.ZIP_STORED)
                break
        # everything else
        for info in zin.infolist():
            if info.filename == 'mimetype':
                continue
            data = zin.read(info.filename)
            name_lower = info.filename.lower()

            if info.filename == 'EPUB/cover.jpg' or name_lower.endswith('/cover.jpg'):
                stats['cover_before'] += info.file_size
                data = new_cover
                stats['cover_after'] += len(data)
                stats['cover_replaced'] = True
            elif name_lower.endswith(('.jpg', '.jpeg')):
                stats['total_jpegs'] += 1
                if is_progressive(data):
                    data = reencode_baseline(data)
                    stats['progressive_reencoded'] += 1

            zout.writestr(info.filename, data,
                          compress_type=zipfile.ZIP_DEFLATED)

    # Atomic replace
    os.replace(tmp_out, epub_path)
    return stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('epub', type=Path)
    ap.add_argument('--cover', type=Path,
                    default=Path('KDP/cover/cover_kdp.jpg'),
                    help='Canonical baseline-JPEG cover (1600x2560 RGB)')
    args = ap.parse_args()
    if not args.epub.exists():
        sys.exit(f'EPUB not found: {args.epub}')
    print(f'Patching {args.epub}')
    print(f'  canonical cover: {args.cover}')
    s = patch(args.epub, args.cover)
    print(f'  cover replaced:           {s["cover_replaced"]}')
    print(f'  cover bytes:              {s["cover_before"]:,} -> {s["cover_after"]:,}')
    print(f'  total non-cover JPEGs:    {s["total_jpegs"]}')
    print(f'  progressive JPEGs fixed:  {s["progressive_reencoded"]}')
    print('DONE.')


if __name__ == '__main__':
    main()
