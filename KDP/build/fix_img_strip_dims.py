"""Post-build EPUB patch: strip explicit width/height pixel attrs from <img> tags.

DEEP-HUNT finding (2026-05-29): 551 of 607 XHTML pages have <img> tags with
explicit `width="N"` and `height="N"` pixel attributes (e.g. width="1200"
height="669"). This is the classic FIXED-LAYOUT convention: every image
declares precise pixel dimensions because fixed-layout EPUBs need them for
exact positioning. Reflowable EPUBs typically rely on CSS (max-width:100%)
and OMIT width/height attrs.

KDP's fixed-format classifier may well weight this pattern as "every image
is precisely sized => looks like a scanned-page comic/manga/PDF" and override
the OPF rendition:layout=reflowable declaration.

What this patch does:
  - For every <img> in every XHTML, remove width="..." and height="..." attrs
  - Preserve all OTHER attrs (src, alt, class, id, style, etc.)
  - Add style="max-width:100%;height:auto" if no inline style exists
  - Idempotent: re-running has no further effect

The image files themselves are untouched; only the markup changes.
Kindle will scale images naturally via CSS, which is the correct reflowable
behavior anyway. EPUBCheck accepts both with-attrs and without-attrs forms.
"""
from __future__ import annotations
import argparse
import os
import re
import sys
import zipfile
from pathlib import Path


# Match an <img> tag and capture its attribute payload (everything between < and />)
IMG_TAG_RE = re.compile(r'<img\b([^>]*?)/?>', re.IGNORECASE)
# Match width="N" or height="N" with optional px suffix
DIM_ATTR_RE = re.compile(r'\s+(?:width|height)\s*=\s*"\d+(?:px)?"', re.IGNORECASE)
INLINE_STYLE_RE = re.compile(r'\sstyle\s*=\s*"([^"]*)"', re.IGNORECASE)


def strip_img_dims(html: str) -> tuple[str, int, int]:
    """Returns (new_html, n_imgs_modified, n_attrs_removed)."""
    n_imgs = 0
    n_attrs = 0

    def repl(m):
        nonlocal n_imgs, n_attrs
        full = m.group(0)
        attrs = m.group(1)
        # Count dim attrs to be removed
        dim_matches = DIM_ATTR_RE.findall(attrs)
        if not dim_matches:
            return full
        n_imgs += 1
        n_attrs += len(dim_matches)
        # Remove width/height attrs
        new_attrs = DIM_ATTR_RE.sub('', attrs)
        # Ensure there's a style with max-width:100% so the image still scales
        style_m = INLINE_STYLE_RE.search(new_attrs)
        if style_m:
            existing = style_m.group(1).rstrip(';').strip()
            if 'max-width' not in existing.lower():
                new_style = f'{existing};max-width:100%;height:auto' if existing else 'max-width:100%;height:auto'
                new_attrs = INLINE_STYLE_RE.sub(f' style="{new_style}"', new_attrs)
        else:
            new_attrs = new_attrs.rstrip() + ' style="max-width:100%;height:auto"'
        # Reconstruct
        # Preserve self-closing vs open tag form (img is always void in xhtml)
        return f'<img{new_attrs}/>'

    new_html = IMG_TAG_RE.sub(repl, html)
    return new_html, n_imgs, n_attrs


def patch(epub_path: Path) -> dict:
    stats = {'files_scanned': 0, 'files_modified': 0,
             'imgs_modified': 0, 'dim_attrs_removed': 0}
    tmp_out = epub_path.with_suffix(epub_path.suffix + '.tmp')
    with zipfile.ZipFile(epub_path, 'r') as zin, \
         zipfile.ZipFile(tmp_out, 'w', zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            if info.filename == 'mimetype':
                zout.writestr(info, zin.read(info.filename),
                              compress_type=zipfile.ZIP_STORED)
                break
        for info in zin.infolist():
            if info.filename == 'mimetype':
                continue
            data = zin.read(info.filename)
            if info.filename.lower().endswith(('.xhtml', '.html')):
                stats['files_scanned'] += 1
                html = data.decode('utf-8', errors='ignore')
                new_html, n_imgs, n_attrs = strip_img_dims(html)
                if n_imgs:
                    stats['files_modified'] += 1
                    stats['imgs_modified'] += n_imgs
                    stats['dim_attrs_removed'] += n_attrs
                    data = new_html.encode('utf-8')
            zout.writestr(info.filename, data, compress_type=zipfile.ZIP_DEFLATED)
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
    print(f'  XHTML files scanned:    {s["files_scanned"]}')
    print(f'  files modified:         {s["files_modified"]}')
    print(f'  <img> tags modified:    {s["imgs_modified"]}')
    print(f'  width/height attrs removed: {s["dim_attrs_removed"]}')
    print('DONE.')


if __name__ == '__main__':
    main()
