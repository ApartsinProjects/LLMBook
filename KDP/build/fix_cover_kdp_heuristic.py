"""Post-build EPUB patch: avoid KDP's fixed-layout misdetection on the cover.

KDP's web upload runs an undocumented "fixed-layout detection" heuristic
that classifies the entire book as fixed-layout when the cover spine item
(cover.xhtml) contains ONLY <img> inside <body> AND is in the linear
spine. Once flagged, KDP rejects the upload with "processing failed".

Symptoms before fix:
  - EPUBCheck 0/0/0 PASS
  - KPV CLI Conversion Status: Success, Enhanced Typesetting: Supported,
    0 errors, 0 quality issues
  - KDP web upload: "processing failed" with no useful diagnostic

The KPV CLI does NOT run this check. Only KDP's web ingestion does.
The fix has two parts (Amazon support engineers have confirmed both
matter to their heuristic):

  1. Set <itemref idref="cover" linear="no"/> in the OPF spine so KDP
     does not analyze cover.xhtml as content.
  2. Make cover.xhtml's body contain text content (a hidden caption
     paragraph) in addition to the <img>, so even if KDP DOES analyze
     it the body is not image-only.

Reference: html2kpd LESSONS #54 (2026-05). Default html2pub does NOT
apply this fix; it must be added as a post-build hook for any book that
KDP rejects despite passing every other gate.

Run AFTER KDP/build/publish.py builds the EPUB, BEFORE uploading:
    python KDP/build/fix_cover_kdp_heuristic.py KDP/output/<name>.epub
"""
from __future__ import annotations
import argparse
import os
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path


COVER_XHTML_TEMPLATE = '''<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en">
<head><title>Cover</title>
<style>body{{margin:0;padding:0;text-align:center}}img{{max-width:100%;height:auto}}.cover-caption{{display:none}}</style>
</head>
<body>
<div class="cover-page">
<img src="{cover_src}" alt="{cover_alt}"/>
<p class="cover-caption">{cover_alt}</p>
</div>
</body></html>
'''


def patch_epub(epub_path: Path, alt_text: str | None = None) -> dict:
    """Apply the two-part KDP cover heuristic fix to an EPUB in place."""
    stats = {'spine_linear_no': False, 'cover_xhtml_text_added': False,
             'cover_xhtml_size_before': 0, 'cover_xhtml_size_after': 0}

    with zipfile.ZipFile(epub_path) as z:
        # Find OPF path via container.xml
        container = z.read('META-INF/container.xml').decode()
        m = re.search(r'full-path="([^"]+)"', container)
        if not m:
            raise SystemExit('container.xml missing full-path')
        opf_path = m.group(1)
        opf_dir = os.path.dirname(opf_path)
        opf = z.read(opf_path).decode()

        # Find cover.xhtml manifest entry
        cov_item = re.search(
            r'<item[^>]+href="([^"]*cover[^"]*\.xhtml)"[^>]*id="(cover[^"]*)"', opf)
        if not cov_item:
            print('No cover.xhtml manifest entry found; nothing to patch.')
            return stats
        cover_href = cov_item.group(1)
        cover_id = cov_item.group(2)
        cover_path = f'{opf_dir}/{cover_href}' if opf_dir else cover_href

        # Find current cover.xhtml
        cur = z.read(cover_path).decode()
        stats['cover_xhtml_size_before'] = len(cur)

        # Find cover image href (referenced from inside cover.xhtml's <img>)
        img_match = re.search(r'<img[^>]+src="([^"]+)"[^>]*alt="([^"]*)"', cur)
        if img_match:
            cover_src = img_match.group(1)
            cur_alt = img_match.group(2)
        else:
            cover_src = 'cover.jpg'
            cur_alt = ''

    # Build new cover.xhtml with body text + new OPF
    if alt_text is None:
        alt_text = cur_alt or 'Cover'
    new_cover = COVER_XHTML_TEMPLATE.format(cover_src=cover_src, cover_alt=alt_text)
    stats['cover_xhtml_size_after'] = len(new_cover)
    stats['cover_xhtml_text_added'] = '<p class="cover-caption">' in new_cover

    # Patch OPF: set linear='no' on cover spine ref
    new_opf, n = re.subn(
        rf'<itemref idref="{re.escape(cover_id)}"(?:\s+linear="[^"]+")?/>',
        f'<itemref idref="{cover_id}" linear="no"/>',
        opf,
    )
    if n:
        stats['spine_linear_no'] = True

    # Repack: extract, overwrite, rezip
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        with zipfile.ZipFile(epub_path) as z:
            z.extractall(tmp)
        (tmp / opf_path).write_text(new_opf, encoding='utf-8')
        (tmp / cover_path).write_text(new_cover, encoding='utf-8')
        epub_path.unlink()
        with zipfile.ZipFile(epub_path, 'w', zipfile.ZIP_DEFLATED) as z:
            # mimetype FIRST, uncompressed
            mime = tmp / 'mimetype'
            if mime.exists():
                z.write(mime, 'mimetype', compress_type=zipfile.ZIP_STORED)
            for root, dirs, files in os.walk(tmp):
                for f in files:
                    full = Path(root) / f
                    arc = str(full.relative_to(tmp)).replace(os.sep, '/')
                    if arc == 'mimetype':
                        continue
                    z.write(full, arc, compress_type=zipfile.ZIP_DEFLATED)
    return stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('epub', type=Path)
    ap.add_argument('--alt', default=None,
                    help='Custom alt text for the cover img (default: keep existing)')
    args = ap.parse_args()
    if not args.epub.exists():
        sys.exit(f'EPUB not found: {args.epub}')
    print(f'Patching {args.epub}')
    stats = patch_epub(args.epub, alt_text=args.alt)
    print(f'  spine linear="no":     {stats["spine_linear_no"]}')
    print(f'  cover.xhtml text added:  {stats["cover_xhtml_text_added"]}')
    print(f'  cover.xhtml size:        {stats["cover_xhtml_size_before"]} -> {stats["cover_xhtml_size_after"]} bytes')
    print('DONE.')


if __name__ == '__main__':
    main()
