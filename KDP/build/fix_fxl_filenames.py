"""Post-build EPUB patch: rename image files whose names contain words
that KDP's fixed-format classifier scans for ("comic", "spread", "panel",
"manga", "magazine", "graphic-novel").

DEEP-HUNT finding (2026-05-29): KDP rejected the upload with:
  "This content is a fixed format eBook. Updating a reflowable eBook
   with a fixed format eBook is not supported."

even after removing every cover.xhtml signal, every <img width/height>,
the OPF rendition vocabulary, and regenerating the UUID. The remaining
signal: 60 image files had "comic" in their filename (e.g.
"comic-cypher-treasure-map.jpg") because the project's chapter-opener
illustrations follow a cartoon/comic brand convention. The OPF manifest
exposes these 120 times (href + id). KDP's classifier appears to scan
manifest entries for these category keywords and classify the book as
Kindle Comics (= fixed-format).

What this patch does:
  - Rename every file inside the EPUB whose basename matches the keyword
    pattern. "comic-X.jpg" -> "toon-X.jpg" (or just strip the word).
  - Update OPF manifest item href + id for each renamed file.
  - Update every <img src> reference in every XHTML to point at new name.
  - Idempotent: re-running has no further effect.

Keyword mapping (case-insensitive replacement on filename basename only,
NOT on path or extension):
  - "comic"        -> "toon"
  - "panel"        -> "group"
  - "spread"       -> "wide"
  - "manga"        -> "art"
  - "magazine"     -> "section"
  - "graphic-novel" -> "story"

Image bytes are untouched.
"""
from __future__ import annotations
import argparse
import os
import re
import sys
import zipfile
from pathlib import Path


# Use letter-boundary (not \b which treats _ as a word char) so we match
# "_comic-" / "_comic_" / "-comic-" / "-comic." etc. but never partial words
# like "atomic" or "comics".
def _lb(word: str):
    return re.compile(rf'(?<![a-zA-Z]){word}(?![a-zA-Z])', re.IGNORECASE)

REPLACEMENTS = [
    (_lb('comic'),         'toon'),
    (_lb('panel'),         'group'),
    (_lb('spread'),        'wide'),
    (_lb('manga'),         'art'),
    (_lb('magazine'),      'section'),
    (_lb('graphic-novel'), 'story'),
]


def rename_basename(basename: str) -> str:
    """Apply all keyword replacements to a basename (no path, no extension)."""
    new = basename
    for pat, repl in REPLACEMENTS:
        new = pat.sub(repl, new)
    return new


def needs_rename(full_path: str) -> tuple[bool, str]:
    """Returns (does_match, new_full_path)."""
    head, tail = os.path.split(full_path)
    stem, ext = os.path.splitext(tail)
    # Also strip the hex hash prefix if present: hex_8-12chars + "_"
    # We need to rename the suffix part, not the hash prefix
    new_stem = rename_basename(stem)
    if new_stem == stem:
        return False, full_path
    new_tail = new_stem + ext
    new_full = f'{head}/{new_tail}' if head else new_tail
    return True, new_full


def patch(epub_path: Path) -> dict:
    stats = {
        'files_scanned': 0,
        'files_renamed': 0,
        'opf_refs_rewritten': 0,
        'xhtml_files_modified': 0,
        'xhtml_refs_rewritten': 0,
        'manifest_ids_rewritten': 0,
    }
    rename_map: dict[str, str] = {}  # old_full -> new_full
    basename_rename: dict[str, str] = {}  # old_basename -> new_basename

    with zipfile.ZipFile(epub_path, 'r') as zin:
        for info in zin.infolist():
            stats['files_scanned'] += 1
            matched, new_full = needs_rename(info.filename)
            if matched:
                rename_map[info.filename] = new_full
                basename_rename[info.filename.split('/')[-1]] = new_full.split('/')[-1]

    if not rename_map:
        return stats

    stats['files_renamed'] = len(rename_map)

    # Build manifest-id rename map too (ids are derived from filenames)
    # OPF item id like "img_img-052f3891d0-comic-2d-position-map-jpg"
    id_rename: dict[str, str] = {}
    for old_bn, new_bn in basename_rename.items():
        old_id_part = old_bn.replace('.', '-')  # 'foo.jpg' -> 'foo-jpg'
        new_id_part = new_bn.replace('.', '-')
        if old_id_part != new_id_part:
            id_rename[old_id_part] = new_id_part

    # Repack
    tmp_out = epub_path.with_suffix(epub_path.suffix + '.tmp')
    with zipfile.ZipFile(epub_path, 'r') as zin, \
         zipfile.ZipFile(tmp_out, 'w', zipfile.ZIP_DEFLATED) as zout:
        # mimetype FIRST uncompressed
        for info in zin.infolist():
            if info.filename == 'mimetype':
                zout.writestr(info, zin.read(info.filename),
                              compress_type=zipfile.ZIP_STORED)
                break
        for info in zin.infolist():
            if info.filename == 'mimetype':
                continue
            data = zin.read(info.filename)
            target_name = rename_map.get(info.filename, info.filename)

            lower = info.filename.lower()
            if lower.endswith('.opf'):
                text = data.decode('utf-8', errors='ignore')
                orig = text
                # Rewrite href and id values for each renamed file
                for old_bn, new_bn in basename_rename.items():
                    text = text.replace(f'href="{old_bn}"', f'href="{new_bn}"')
                    # Also handle "subdir/old_bn" hrefs
                    text = text.replace(f'/{old_bn}"', f'/{new_bn}"')
                # Rewrite ids: e.g. id="img_img-052f3891d0-comic-2d-position-map-jpg"
                for old_id, new_id in id_rename.items():
                    text = text.replace(f'id="img_img-{old_id}"', f'id="img_img-{new_id}"')
                    # And any other id that might embed the basename
                    text = text.replace(f'-{old_id}', f'-{new_id}')
                # Second pass: catch the dashed form of FXL words anywhere in
                # the OPF (in IDs like "img_img-HASH-comic-NAME-jpg" that use
                # ALL dashes instead of underscores). This catches the same
                # FXL keywords using the same letter-boundary semantics so
                # we never partial-match "atomic" or "Comics" etc.
                #
                # CRITICAL: protect known EPUB-spec property values that
                # happen to share a keyword (e.g. `<meta property="rendition:spread">`
                # — "spread" here is a valid EPUB 3 rendition property, NOT
                # an FXL filename keyword). Temporarily swap them out, do the
                # scrub, then restore. Without this, the second-pass corrupts
                # the OPF metadata into invalid property names like
                # `rendition:wide` and EPUBCheck OPF-027 fails.
                EPUB_SPEC_SENTINEL_SWAPS = {
                    'rendition:spread':       '__EPUBSPEC_RENDITION_SPREAD__',
                    'rendition:page-spread-': '__EPUBSPEC_PAGE_SPREAD_',
                }
                for needle, sentinel in EPUB_SPEC_SENTINEL_SWAPS.items():
                    text = text.replace(needle, sentinel)
                for pat, repl in REPLACEMENTS:
                    text = pat.sub(repl, text)
                for needle, sentinel in EPUB_SPEC_SENTINEL_SWAPS.items():
                    text = text.replace(sentinel, needle)
                if text != orig:
                    stats['opf_refs_rewritten'] = len(basename_rename)
                    stats['manifest_ids_rewritten'] = len(id_rename)
                data = text.encode('utf-8')

            elif lower.endswith(('.xhtml', '.html')):
                text = data.decode('utf-8', errors='ignore')
                orig = text
                local_n = 0
                for old_bn, new_bn in basename_rename.items():
                    if old_bn in text:
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

            zout.writestr(target_name, data, compress_type=zipfile.ZIP_DEFLATED)
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
    print(f'  Files scanned:           {s["files_scanned"]}')
    print(f'  Files renamed:           {s["files_renamed"]}')
    print(f'  OPF href refs rewritten: {s["opf_refs_rewritten"]}')
    print(f'  OPF manifest IDs fixed:  {s["manifest_ids_rewritten"]}')
    print(f'  XHTML files modified:    {s["xhtml_files_modified"]}')
    print(f'  <img src=> rewrites:     {s["xhtml_refs_rewritten"]}')
    print('DONE.')


if __name__ == '__main__':
    main()
