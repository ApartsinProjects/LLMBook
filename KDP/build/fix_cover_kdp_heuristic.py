"""Post-build EPUB patch: make cover.xhtml look unambiguously REFLOWABLE.

History:
  Previous version (LESSONS #54 misdiagnosis) added body{margin:0;padding:0}
  CSS + a hidden caption + set spine linear="no". KDP REJECTED the upload
  with "This content is a fixed format eBook. Updating a reflowable eBook
  with a fixed format eBook is not supported."

  Root cause: KDP's classifier treats body{margin:0;padding:0} + image-only-
  when-rendered body + cover spine linear="no" as a FIXED-LAYOUT signature.
  ebooklib's default cover.xhtml ALSO ships this same CSS by default. So
  both the ebooklib default AND our LESSONS #54 fix flag the book as
  fixed-layout.

What this patch now does (2026-05-29):
  1. Rewrite cover.xhtml with normal flowing body CSS (no margin:0)
  2. Add a visible byline/title text block AFTER the image so the body
     is provably not image-only when rendered
  3. Set spine itemref linear="yes" (was linear="no" in earlier patch)
  4. Keep the original cover.jpg href (don't touch the image itself)

The patched cover.xhtml looks like a normal title page (image + title
block), which is the pattern KDP's classifier accepts as reflowable.

Run AFTER html2pub builds the EPUB, BEFORE uploading.
"""
from __future__ import annotations
import argparse
import os
import re
import sys
import tempfile
import zipfile
from pathlib import Path


COVER_XHTML_TEMPLATE = '''<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en">
<head>
<title>Cover</title>
</head>
<body>
<div class="cover-page" style="text-align:center">
<img src="{cover_src}" alt="{cover_alt}" style="max-width:100%;height:auto"/>
<h1 style="text-align:center;font-size:1.4em;margin-top:1em">{book_title}</h1>
<p style="text-align:center;font-style:italic;margin-top:0.5em">{book_subtitle}</p>
<p style="text-align:center;margin-top:1em">{authors}</p>
</div>
</body></html>
'''


def patch_epub(epub_path: Path,
               book_title: str = 'Building Conversational AI with LLMs and Agents',
               book_subtitle: str = 'From the mathematics of attention to production agent systems',
               authors: str = 'Alexander Apartsin and Yehudit Aperstein') -> dict:
    """Rewrite cover.xhtml to look reflowable and set spine linear='yes'."""
    stats = {'spine_linear_yes': False, 'cover_xhtml_rewritten': False,
             'cover_xhtml_size_before': 0, 'cover_xhtml_size_after': 0,
             'body_has_text': False}

    with zipfile.ZipFile(epub_path) as z:
        container = z.read('META-INF/container.xml').decode()
        m = re.search(r'full-path="([^"]+)"', container)
        if not m:
            raise SystemExit('container.xml missing full-path')
        opf_path = m.group(1)
        opf_dir = os.path.dirname(opf_path)
        opf = z.read(opf_path).decode()

        cov_item = re.search(
            r'<item[^>]+href="([^"]*cover[^"]*\.xhtml)"[^>]*id="(cover[^"]*)"', opf)
        if not cov_item:
            print('No cover.xhtml manifest entry found; nothing to patch.')
            return stats
        cover_href = cov_item.group(1)
        cover_id = cov_item.group(2)
        cover_path = f'{opf_dir}/{cover_href}' if opf_dir else cover_href

        cur = z.read(cover_path).decode()
        stats['cover_xhtml_size_before'] = len(cur)

        # Extract current <img src> + alt from existing cover.xhtml
        img_match = re.search(r'<img[^>]+src="([^"]+)"[^>]*alt="([^"]*)"', cur)
        if img_match:
            cover_src = img_match.group(1)
            cur_alt = img_match.group(2) or 'Cover'
        else:
            cover_src = 'cover.jpg'
            cur_alt = 'Cover'

    new_cover = COVER_XHTML_TEMPLATE.format(
        cover_src=cover_src,
        cover_alt=cur_alt,
        book_title=book_title,
        book_subtitle=book_subtitle,
        authors=authors,
    )
    stats['cover_xhtml_size_after'] = len(new_cover)
    stats['cover_xhtml_rewritten'] = True
    stats['body_has_text'] = ('<h1' in new_cover and book_title in new_cover)

    # Patch OPF spine: ensure cover itemref has linear="yes"
    new_opf, n = re.subn(
        rf'<itemref idref="{re.escape(cover_id)}"(?:\s+linear="[^"]+")?\s*/>',
        f'<itemref idref="{cover_id}" linear="yes"/>',
        opf,
    )
    if n:
        stats['spine_linear_yes'] = True

    # Repack in-memory + atomic temp file replace
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
            if info.filename == opf_path:
                data = new_opf.encode('utf-8')
            elif info.filename == cover_path:
                data = new_cover.encode('utf-8')
            zout.writestr(info.filename, data, compress_type=zipfile.ZIP_DEFLATED)
    os.replace(tmp_out, epub_path)
    return stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('epub', type=Path)
    ap.add_argument('--title', default='Building Conversational AI with LLMs and Agents')
    ap.add_argument('--subtitle',
                    default='From the mathematics of attention to production agent systems')
    ap.add_argument('--authors', default='Alexander Apartsin and Yehudit Aperstein')
    args = ap.parse_args()
    if not args.epub.exists():
        sys.exit(f'EPUB not found: {args.epub}')
    print(f'Patching {args.epub}')
    stats = patch_epub(args.epub, args.title, args.subtitle, args.authors)
    print(f'  spine linear="yes":      {stats["spine_linear_yes"]}')
    print(f'  cover.xhtml rewritten:   {stats["cover_xhtml_rewritten"]}')
    print(f'  body has visible text:   {stats["body_has_text"]}')
    print(f'  cover.xhtml size:        {stats["cover_xhtml_size_before"]} -> {stats["cover_xhtml_size_after"]} bytes')
    print('DONE.')


if __name__ == '__main__':
    main()
