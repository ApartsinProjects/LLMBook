"""KPV smoke test: convert a small EPUB subset to flush out blockers.

Why: full KPV conversion of a large book can take 10+ minutes. Iterating
the build -> KPV -> qualitychecks loop is slow if you must convert the
entire book to discover a single E21018 in chapter 4. This script builds
a SUBSET EPUB (first N spine entries) by rewriting the OPF + nav, then
runs KPV on the subset. If the subset passes, run the full convert.

Strategy:
  1. Unzip the EPUB into a temp directory.
  2. Read content.opf, take the first N <itemref> entries from <spine>.
  3. Drop everything else from <spine> and from <manifest> (except for
     items the kept entries link to — CSS, images, fonts).
  4. Optionally trim nav.xhtml to match.
  5. Repack as a new EPUB.
  6. Hand off to kpv_convert.py for the actual conversion.

Usage:
    python kpv_smoke_test.py --epub <input.epub>
    python kpv_smoke_test.py --epub <input.epub> --n 20
    python kpv_smoke_test.py --epub <input.epub> --n 10 --output <subset.epub>

Default N=20 spine entries.
"""
from __future__ import annotations
import argparse
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

# Register XML namespaces used in OPF / NAV
NS = {
    'opf': 'http://www.idpf.org/2007/opf',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'xhtml': 'http://www.w3.org/1999/xhtml',
}
for prefix, uri in NS.items():
    ET.register_namespace('' if prefix == 'opf' else prefix, uri)


def find_opf(extract_dir: Path) -> Path:
    container = extract_dir / 'META-INF' / 'container.xml'
    if not container.exists():
        raise RuntimeError('META-INF/container.xml not found in EPUB')
    root = ET.fromstring(container.read_text(encoding='utf-8'))
    rootfile = root.find('.//{urn:oasis:names:tc:opendocument:xmlns:container}'
                          'rootfile')
    if rootfile is None:
        raise RuntimeError('No rootfile in container.xml')
    opf_rel = rootfile.get('full-path')
    return extract_dir / opf_rel


def trim_epub(in_epub: Path, out_epub: Path, n: int) -> int:
    """Trim in_epub down to first n spine entries; write to out_epub."""
    with tempfile.TemporaryDirectory(prefix='kpv_smoke_') as tdir:
        ex = Path(tdir)
        with zipfile.ZipFile(in_epub) as z:
            z.extractall(ex)

        opf_path = find_opf(ex)
        opf_root = ET.parse(opf_path).getroot()

        # Get spine itemrefs
        spine = opf_root.find('opf:spine', NS) or opf_root.find('{*}spine')
        if spine is None:
            raise RuntimeError('No <spine> in OPF')
        itemrefs = list(spine)
        keep_itemrefs = itemrefs[:n]
        keep_idrefs = set(it.get('idref') for it in keep_itemrefs)

        # Build idref -> href map from manifest
        manifest = opf_root.find('opf:manifest', NS) or opf_root.find(
            '{*}manifest')
        if manifest is None:
            raise RuntimeError('No <manifest> in OPF')
        id_to_item = {it.get('id'): it for it in manifest}

        # Determine which files to keep (kept chapters + ALL non-chapter
        # items: CSS, images, fonts, nav, cover). Drop only un-kept
        # chapters from the manifest.
        chapter_idrefs = set(it.get('idref') for it in itemrefs)
        keep_ids = set(keep_idrefs)
        for item_id, item in id_to_item.items():
            mtype = item.get('media-type', '')
            if not mtype.startswith('application/xhtml'):
                keep_ids.add(item_id)
            elif item_id in keep_idrefs:
                keep_ids.add(item_id)
            elif item.get('properties') and 'nav' in item.get('properties'):
                keep_ids.add(item_id)
        drop_ids = set(id_to_item.keys()) - keep_ids

        # Determine HREFs to delete from ZIP for dropped items
        opf_dir = opf_path.parent
        drop_files = set()
        for did in drop_ids:
            item = id_to_item[did]
            href = item.get('href')
            if not href:
                continue
            f = (opf_dir / href).resolve()
            try:
                drop_files.add(str(f.relative_to(ex)).replace('\\', '/'))
            except ValueError:
                pass

        # Strip <itemref> entries not in keep
        for it in list(spine):
            if it.get('idref') not in keep_idrefs:
                spine.remove(it)
        # Strip <item> entries not in keep
        for it in list(manifest):
            if it.get('id') in drop_ids:
                manifest.remove(it)

        # Write OPF
        opf_path.write_text(ET.tostring(opf_root, encoding='unicode',
                                          xml_declaration=True),
                             encoding='utf-8')

        # Repack
        if out_epub.exists():
            out_epub.unlink()
        with zipfile.ZipFile(out_epub, 'w') as zout:
            # mimetype first, stored
            mimetype = ex / 'mimetype'
            if mimetype.exists():
                info = zipfile.ZipInfo('mimetype')
                info.compress_type = zipfile.ZIP_STORED
                zout.writestr(info, mimetype.read_bytes())
            for p in sorted(ex.rglob('*')):
                if not p.is_file() or p == mimetype:
                    continue
                arc = str(p.relative_to(ex)).replace('\\', '/')
                if arc in drop_files:
                    continue
                zout.write(p, arc, compress_type=zipfile.ZIP_DEFLATED,
                            compresslevel=6)

        return len(keep_itemrefs)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--epub', type=Path, required=True,
                    help='Input EPUB (the full book)')
    ap.add_argument('--n', type=int, default=20,
                    help='Number of spine entries to keep (default 20)')
    ap.add_argument('--output', type=Path, default=None,
                    help='Output subset EPUB path')
    ap.add_argument('--skip-convert', action='store_true',
                    help='Build subset but skip KPV convert')
    args = ap.parse_args(argv)

    if not args.epub.exists():
        print(f'ERROR: EPUB not found: {args.epub}', file=sys.stderr)
        return 2

    out = args.output or args.epub.with_name(
        args.epub.stem + f'-smoke{args.n}.epub')
    print(f'Trimming {args.epub} to first {args.n} spine entries -> {out}')
    n_kept = trim_epub(args.epub, out, args.n)
    print(f'Kept {n_kept} spine entries; output size:'
          f' {out.stat().st_size / 1024 / 1024:.2f} MB')

    if args.skip_convert:
        return 0

    # Hand off to kpv_convert.py
    here = Path(__file__).resolve().parent
    cmd = [sys.executable, str(here / 'kpv_convert.py'),
           '--epub', str(out)]
    print(f'\nRunning: {" ".join(cmd)}')
    rc = subprocess.call(cmd)
    return rc


if __name__ == '__main__':
    raise SystemExit(main())
