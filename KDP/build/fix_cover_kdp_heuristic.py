"""Post-build EPUB patch: normalize cover.xhtml to the KDP-canonical
image-only pattern (matches May 22 ACCEPTED EPUB structure).

History (cancellation of two prior diagnoses):
  - Original LESSONS #54 said: image-only cover causes KDP fixed-format
    misdetection. FALSE. KDP wants image-only cover.
  - 2026-05-29 rewrite added <h1>+description+authors visible text and
    set spine linear="yes" because we thought that defeated the
    "fixed-format" classifier. FALSE. That triggered the rejection.

Comparison with the on-disk May 22 -reflowable.epub (presumed accepted
by KDP) revealed the canonical reflowable cover pattern is:

  <html ...><head><title>Cover</title></head>
   <body><img src="cover.jpg" alt="Cover"/></body></html>

That's it. No body styles. No CSS in head. No text. Just <img>.
The spine itemref has linear="yes".

This patch:
  1. Replaces cover.xhtml with the minimal image-only template
  2. Sets spine itemref linear="yes"
Idempotent.
"""
from __future__ import annotations
import argparse, os, re, sys, zipfile
from pathlib import Path

# EXACT bytes the May 22 accepted EPUB has at EPUB/cover.xhtml
MINIMAL_COVER_TEMPLATE = (
    "<?xml version='1.0' encoding='utf-8'?> "
    '<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml" '
    'xmlns:epub="http://www.idpf.org/2007/ops" '
    'epub:prefix="z3998: http://www.daisy.org/z3998/2012/vocab/structure/#" '
    'lang="en" xml:lang="en"><head><title>Cover</title></head>'
    '<body><img src="{cover_src}" alt="{cover_alt}"/></body></html>'
)


def patch_epub(epub_path: Path, *_, **__) -> dict:
    stats = {'cover_xhtml_normalized': False, 'spine_linear_yes': False}
    with zipfile.ZipFile(epub_path) as z:
        container = z.read('META-INF/container.xml').decode()
        opf_path = re.search(r'full-path="([^"]+)"', container).group(1)
        opf = z.read(opf_path).decode()
        cov_item = re.search(r'<item[^>]+href="([^"]*cover[^"]*\.xhtml)"', opf)
        if not cov_item:
            return stats
        cover_href = cov_item.group(1)
        cover_path = f'EPUB/{cover_href}'
        cur = z.read(cover_path).decode()
        img_m = re.search(r'<img[^>]+src="([^"]+)"[^>]*alt="([^"]*)"', cur)
        cover_src = img_m.group(1) if img_m else 'cover.jpg'
        cover_alt = img_m.group(2) if img_m else 'Cover'

    new_cover = MINIMAL_COVER_TEMPLATE.format(cover_src=cover_src, cover_alt=cover_alt)
    new_opf = re.sub(
        r'<itemref idref="cover"(?:\s+linear="[^"]+")?\s*/>',
        '<itemref idref="cover" linear="yes"/>', opf)

    tmp_out = epub_path.with_suffix(epub_path.suffix + '.tmp')
    with zipfile.ZipFile(epub_path, 'r') as zin, \
         zipfile.ZipFile(tmp_out, 'w', zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            if info.filename == 'mimetype':
                zout.writestr(info, zin.read(info.filename),
                              compress_type=zipfile.ZIP_STORED); break
        for info in zin.infolist():
            if info.filename == 'mimetype': continue
            data = zin.read(info.filename)
            if info.filename == opf_path:
                if new_opf != opf:
                    stats['spine_linear_yes'] = True
                data = new_opf.encode('utf-8')
            elif info.filename == cover_path:
                if new_cover != cur:
                    stats['cover_xhtml_normalized'] = True
                data = new_cover.encode('utf-8')
            zout.writestr(info.filename, data, compress_type=zipfile.ZIP_DEFLATED)
    os.replace(tmp_out, epub_path)
    return stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('epub', type=Path)
    args = ap.parse_args()
    if not args.epub.exists(): sys.exit(f'EPUB not found: {args.epub}')
    print(f'Patching {args.epub}')
    s = patch_epub(args.epub)
    print(f'  cover.xhtml normalized to image-only:  {s["cover_xhtml_normalized"]}')
    print(f'  spine cover linear="yes":              {s["spine_linear_yes"]}')
    print('DONE.')


if __name__ == '__main__':
    main()
