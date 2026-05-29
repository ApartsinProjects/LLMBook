"""Post-build EPUB patch: strip ALL rendition-vocabulary signals from OPF.

DEEP-HUNT finding (2026-05-29): KDP's fixed-format classifier is rejecting
the EPUB despite cover.xhtml looking reflowable AND OPF declaring
rendition:layout=reflowable. The remaining suspects are metadata-level
"fixed-layout heritage" signals:

  1. <package prefix="rendition: http://www.idpf.org/vocab/rendition/#">
     Only FXL EPUBs typically declare this prefix.
  2. <meta property="rendition:orientation">auto</meta>
  3. <meta property="rendition:spread">auto</meta>
     These two are only meaningful for fixed-layout (where orientation
     and spread actually matter). For reflowable they're noise that
     KDP's classifier MAY weight as "this book cares about layout =
     fixed-layout-leaning".
  4. <meta name="cover" content="cover-img"/> (legacy EPUB 2 style)
     Already redundant with <item properties="cover-image"/>; removing
     reduces "mixed-format heritage" appearance.

We also REGENERATE the dc:identifier UUID so KDP doesn't match this
upload to a cached failed previous one (if such caching exists).

What this patch does:
  - Remove prefix="rendition:..." from <package>
  - Remove <meta property="rendition:orientation">...</meta>
  - Remove <meta property="rendition:spread">...</meta>
  - KEEP <meta property="rendition:layout">reflowable</meta> (still useful as positive signal)
  - Remove <meta name="cover" content="..."/>
  - Replace UUID with a fresh one

Run AFTER fix_cover_kdp_heuristic.py and the other patches, AS THE LAST
post-build step before EPUBCheck.
"""
from __future__ import annotations
import argparse
import os
import re
import sys
import uuid
import zipfile
from pathlib import Path


def patch(epub_path: Path, regen_uuid: bool = True) -> dict:
    stats = {
        'removed_package_prefix': False,
        'removed_rendition_orientation': False,
        'removed_rendition_spread': False,
        'kept_rendition_layout': False,
        'removed_legacy_meta_cover': False,
        'old_uuid': '',
        'new_uuid': '',
        'ncx_uuid_synced': False,
    }

    with zipfile.ZipFile(epub_path) as z:
        container = z.read('META-INF/container.xml').decode()
        opf_path = re.search(r'full-path="([^"]+)"', container).group(1)
        opf = z.read(opf_path).decode()

    new_opf = opf

    # 1. Strip rendition prefix from package element
    new_opf2, n = re.subn(
        r'\s+prefix="rendition:\s*http://www\.idpf\.org/vocab/rendition/#"',
        '', new_opf)
    if n:
        stats['removed_package_prefix'] = True
        new_opf = new_opf2

    # 2. Remove rendition:orientation meta
    new_opf2, n = re.subn(
        r'\s*<meta property="rendition:orientation">[^<]*</meta>\s*',
        '\n    ', new_opf)
    if n:
        stats['removed_rendition_orientation'] = True
        new_opf = new_opf2

    # 3. Remove rendition:spread meta
    new_opf2, n = re.subn(
        r'\s*<meta property="rendition:spread">[^<]*</meta>\s*',
        '\n    ', new_opf)
    if n:
        stats['removed_rendition_spread'] = True
        new_opf = new_opf2

    # 4. Verify rendition:layout is kept (we want it as positive signal)
    if re.search(r'<meta property="rendition:layout">reflowable</meta>', new_opf):
        stats['kept_rendition_layout'] = True

    # 5. Remove legacy <meta name="cover" content="..."/>
    new_opf2, n = re.subn(
        r'\s*<meta name="cover" content="[^"]+"\s*/>\s*',
        '\n    ', new_opf)
    if n:
        stats['removed_legacy_meta_cover'] = True
        new_opf = new_opf2

    # 6. Regenerate UUID
    if regen_uuid:
        m = re.search(
            r'(<dc:identifier[^>]*>)(urn:uuid:[^<]+|[^<]+)(</dc:identifier>)',
            new_opf)
        if m:
            stats['old_uuid'] = m.group(2)
            new_uuid = f'urn:uuid:{uuid.uuid4()}'
            stats['new_uuid'] = new_uuid
            new_opf = new_opf[:m.start()] + m.group(1) + new_uuid + m.group(3) + new_opf[m.end():]

    # Repack
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
            # Also update NCX dtb:uid to match the new OPF UUID
            # EPUBCheck NCX-001 enforces this match.
            elif regen_uuid and stats['new_uuid'] and \
                    info.filename.lower().endswith('.ncx'):
                ncx = data.decode('utf-8', errors='ignore')
                # Match either attribute order: name="dtb:uid" content=... OR content=... name="dtb:uid"
                new_ncx, n_ncx = re.subn(
                    r'(<meta\b[^>]*\bname="dtb:uid"[^>]*\bcontent=")[^"]+(")',
                    rf'\g<1>{stats["new_uuid"]}\g<2>',
                    ncx,
                )
                if n_ncx == 0:
                    new_ncx, n_ncx = re.subn(
                        r'(<meta\b[^>]*\bcontent=")[^"]+("[^>]*\bname="dtb:uid")',
                        rf'\g<1>{stats["new_uuid"]}\g<2>',
                        ncx,
                    )
                if n_ncx:
                    data = new_ncx.encode('utf-8')
                    stats['ncx_uuid_synced'] = True
            zout.writestr(info.filename, data, compress_type=zipfile.ZIP_DEFLATED)
    os.replace(tmp_out, epub_path)
    return stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('epub', type=Path)
    ap.add_argument('--keep-uuid', action='store_true',
                    help='Do not regenerate the UUID (default: regenerate)')
    args = ap.parse_args()
    if not args.epub.exists():
        sys.exit(f'EPUB not found: {args.epub}')
    print(f'Patching {args.epub}')
    s = patch(args.epub, regen_uuid=not args.keep_uuid)
    print(f'  removed package prefix:           {s["removed_package_prefix"]}')
    print(f'  removed rendition:orientation:    {s["removed_rendition_orientation"]}')
    print(f'  removed rendition:spread:         {s["removed_rendition_spread"]}')
    print(f'  kept rendition:layout=reflowable: {s["kept_rendition_layout"]}')
    print(f'  removed legacy meta name=cover:   {s["removed_legacy_meta_cover"]}')
    if s['new_uuid']:
        print(f'  UUID: {s["old_uuid"]}')
        print(f'        -> {s["new_uuid"]}')
    print('DONE.')


if __name__ == '__main__':
    main()
