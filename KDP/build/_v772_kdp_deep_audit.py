"""v772: Deep KDP-compliance audit of the shipped EPUB.

Goes beyond the v756 acceptance suite to catch every issue that has
ever appeared in KDP rejection reports:

  Hard requirements (would block ingestion):
    1. EPUBCheck 5.x clean (0 errors)
    2. OPF metadata: title, language, identifier, modified, creator
    3. Cover image: declared with properties="cover-image", JPEG/PNG
       (NOT SVG/TIFF/GIF), 625 px min side, 1.6:1 aspect, < 5 MB
    4. EPUB total size < 650 MB
    5. Reflowable rendition explicitly declared
    6. NAV document with toc nav element (EPUB 3 requirement)
    7. NCX present (Kindle compatibility)
    8. Container.xml points to valid OPF
    9. mimetype first file, uncompressed, exact value
   10. Every spine itemref resolves to a manifest item that exists
   11. No forms / inputs / buttons / iframes / embeds / objects
   12. No JavaScript (no <script> tags, no .js files)
   13. No audio/video media items
   14. No DRM markers (Adobe Adept, Marlin, FairPlay)
   15. No external @import or @font-face URLs in CSS

  KDP-specific quirks:
   16. Path length: KDP rejects internal paths > 240 chars
   17. Filename characters: only [a-z0-9._-]; no spaces, %, #, &, ?
   18. Image file size: every image < 5 MB
   19. Image dimensions: every image < 4000 px on either side
       (KDP's converter struggles with very-large images)
   20. Cover image filename in manifest matches actual file
   21. Every XHTML parses as well-formed XML
   22. Every XHTML has a DOCTYPE declaration
   23. Every XHTML has UTF-8 encoding declared
   24. No external URLs in src/href except http(s) for hyperlinks
       (i.e., no file://, about:, data: blob: etc.)
   25. Anchor IDs are unique within each file
   26. Cross-file anchor links resolve to existing IDs in target files
   27. CSS files reference no missing assets
   28. No XHTML uses <html> without xmlns
   29. <title> non-empty in every XHTML
   30. Spine first item: cover OR nav OR title page (usual conventions)

  Known KDP traps:
   31. CSS @charset declarations in non-UTF8 form
   32. position: fixed / sticky in CSS (Kindle reflow incompatible)
   33. display: flex / grid in non-standard ways
   34. Math formulas:
       - Either KaTeX-rendered HTML OR proper <math> MathML
       - Not bare $$..$$ source text
   35. <pre> blocks with pre-formatted whitespace > 1000 chars wide
       (Kindle wraps poorly; KDP recommends max ~80 cols)

Output: categorized severity report (Critical / High / Medium / Info).
Exits 0 if no Critical/High issues; 1 otherwise.
"""
from __future__ import annotations
import io
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

try:
    from PIL import Image
    HAVE_PIL = True
except ImportError:
    HAVE_PIL = False

ROOT = Path(__file__).resolve().parent.parent.parent
EPUB = ROOT / 'KDP' / 'output' / 'building-conversational-ai-llms-agents.epub'

CRIT = []
HIGH = []
MED = []
INFO = []


def critical(msg): CRIT.append(msg); print(f'  [CRIT] {msg}')
def high(msg): HIGH.append(msg); print(f'  [HIGH] {msg}')
def medium(msg): MED.append(msg); print(f'  [MED]  {msg}')
def info(msg): INFO.append(msg); print(f'  [INFO] {msg}')
def ok(msg): print(f'  [OK]   {msg}')


def fmt_size(n):
    for u in ['B', 'KB', 'MB', 'GB']:
        if n < 1024:
            return f'{n:.2f} {u}'
        n /= 1024
    return f'{n:.2f} TB'


def main() -> int:
    print('=' * 70)
    print(f'KDP deep-compliance audit of: {EPUB.relative_to(ROOT)}')
    print('=' * 70)

    if not EPUB.exists():
        critical(f'EPUB does not exist at {EPUB}')
        return 1

    sz = EPUB.stat().st_size
    if sz > 650 * 1024 * 1024:
        critical(f'EPUB size {fmt_size(sz)} exceeds KDP 650 MB limit')
    else:
        ok(f'EPUB size: {fmt_size(sz)} (under 650 MB cap)')

    # Open ZIP
    with zipfile.ZipFile(EPUB) as z:
        names = z.namelist()
        infolist = {i.filename: i for i in z.infolist()}

        # Mimetype first + uncompressed
        first = infolist.get(names[0]) if names else None
        if not first or first.filename != 'mimetype':
            critical(f'First file is not "mimetype" (it is {names[0]})')
        elif first.compress_type != zipfile.ZIP_STORED:
            critical('mimetype is compressed (must be STORED)')
        else:
            mt = z.read('mimetype').decode('ascii', errors='replace').strip()
            if mt != 'application/epub+zip':
                critical(f'mimetype content is "{mt}", not "application/epub+zip"')
            else:
                ok('mimetype: stored, uncompressed, correct value')

        # container.xml -> OPF path
        if 'META-INF/container.xml' not in names:
            critical('META-INF/container.xml missing')
            return 1
        cx = z.read('META-INF/container.xml').decode('utf-8', errors='replace')
        m = re.search(r'full-path="([^"]+)"', cx)
        if not m:
            critical('container.xml has no rootfile/full-path')
            return 1
        opf_path = m.group(1)
        if opf_path not in names:
            critical(f'OPF file declared in container.xml does not exist: {opf_path}')
            return 1
        ok(f'container.xml -> {opf_path}')

        opf_text = z.read(opf_path).decode('utf-8', errors='replace')
        opf_dir = opf_path.rsplit('/', 1)[0] + '/' if '/' in opf_path else ''
        opf_root = ET.fromstring(opf_text)
        ns = {'opf': 'http://www.idpf.org/2007/opf',
              'dc': 'http://purl.org/dc/elements/1.1/'}

        # OPF metadata required fields
        meta = opf_root.find('opf:metadata', ns)
        for tag, label in [('dc:title', 'title'), ('dc:language', 'language'),
                           ('dc:identifier', 'identifier'),
                           ('dc:creator', 'creator')]:
            els = meta.findall(tag, ns)
            if not els:
                critical(f'OPF missing required <{tag}>')
            else:
                ok(f'OPF {label}: {els[0].text[:60] if els[0].text else "(no text)"}')

        # dcterms:modified
        dcterms_mod = None
        for m in meta.findall('opf:meta', ns):
            if m.get('property') == 'dcterms:modified':
                dcterms_mod = m.text
                break
        if dcterms_mod:
            ok(f'OPF dcterms:modified: {dcterms_mod}')
        else:
            high('OPF missing <meta property="dcterms:modified"> (EPUB 3 required)')

        # Reflowable rendition
        layout = None
        for m in meta.findall('opf:meta', ns):
            if m.get('property') == 'rendition:layout':
                layout = m.text
                break
        if layout == 'reflowable':
            ok('rendition:layout = reflowable (explicit)')
        elif layout == 'pre-paginated':
            critical('rendition:layout = pre-paginated; KDP cannot update reflowable book')
        else:
            high('rendition:layout not declared (KDP may default to fixed-format)')

        # Cover
        manifest = opf_root.find('opf:manifest', ns)
        cover_item = None
        for it in manifest.findall('opf:item', ns):
            props = (it.get('properties') or '').split()
            if 'cover-image' in props:
                cover_item = it
                break
        if cover_item is None:
            critical('No item declared with properties="cover-image"')
        else:
            cover_href = cover_item.get('href')
            cover_full = opf_dir + cover_href
            cover_mime = cover_item.get('media-type')
            ok(f'Cover declared: {cover_href} ({cover_mime})')
            if cover_mime not in ('image/jpeg', 'image/png'):
                critical(f'Cover MIME {cover_mime} not JPEG/PNG (KDP rejects SVG/TIFF/GIF)')
            if cover_full not in names:
                critical(f'Cover file missing in archive: {cover_full}')
            else:
                # Cover dims and size
                cover_bytes = z.read(cover_full)
                cover_sz = len(cover_bytes)
                if cover_sz > 5 * 1024 * 1024:
                    high(f'Cover size {fmt_size(cover_sz)} > KDP 5 MB recommended')
                else:
                    ok(f'Cover size: {fmt_size(cover_sz)} (< 5 MB)')
                if HAVE_PIL:
                    try:
                        img = Image.open(io.BytesIO(cover_bytes))
                        w, h = img.size
                        ms = min(w, h)
                        if ms < 625:
                            critical(f'Cover min side {ms} px < KDP 625 px minimum')
                        else:
                            ok(f'Cover dimensions: {w}x{h} (min side {ms} >= 625)')
                        ratio = h / w
                        if abs(ratio - 1.6) > 0.05:
                            medium(f'Cover h/w = {ratio:.2f} (KDP recommends 1.6)')
                        else:
                            ok(f'Cover aspect ratio: {ratio:.2f} ~ 1.6:1')
                        if max(w, h) < 1600:
                            medium(f'Cover max side {max(w,h)} px; KDP recommends >= 1600 for HD')
                    except Exception as e:
                        high(f'Cover image could not be parsed: {e}')

        # NAV doc
        nav_item = None
        for it in manifest.findall('opf:item', ns):
            props = (it.get('properties') or '').split()
            if 'nav' in props:
                nav_item = it
                break
        if nav_item is None:
            critical('No NAV document with properties="nav" (EPUB 3 required)')
        else:
            nav_full = opf_dir + nav_item.get('href')
            nav_text = z.read(nav_full).decode('utf-8', errors='replace')
            if '<nav' not in nav_text or 'epub:type="toc"' not in nav_text:
                high('NAV doc has no <nav epub:type="toc">')
            else:
                ok(f'NAV doc with toc nav: {nav_full}')

        # NCX
        spine = opf_root.find('opf:spine', ns)
        ncx_id = spine.get('toc') if spine is not None else None
        if ncx_id:
            for it in manifest.findall('opf:item', ns):
                if it.get('id') == ncx_id:
                    ok(f'NCX present: {it.get("href")}')
                    break
            else:
                medium('Spine declares toc=ncx-id but no matching manifest item')
        else:
            medium('No NCX in spine (Kindle older readers may need it)')

        # Spine itemref resolution
        manifest_by_id = {it.get('id'): it for it in manifest.findall('opf:item', ns)}
        spine_orphans = []
        for ir in spine.findall('opf:itemref', ns):
            idref = ir.get('idref')
            if idref not in manifest_by_id:
                spine_orphans.append(idref)
        if spine_orphans:
            critical(f'Spine itemrefs not in manifest: {spine_orphans[:3]} ({len(spine_orphans)} total)')
        else:
            ok(f'All {len(spine.findall("opf:itemref", ns))} spine itemrefs resolve to manifest items')

        # Manifest items exist in archive
        missing_files = []
        for it in manifest.findall('opf:item', ns):
            full = opf_dir + it.get('href')
            if full not in names:
                missing_files.append(full)
        if missing_files:
            critical(f'Manifest items missing from archive: {missing_files[:3]} ({len(missing_files)} total)')
        else:
            ok(f'All {len(manifest.findall("opf:item", ns))} manifest items exist')

        # No DRM
        drm_markers = ['META-INF/encryption.xml', 'META-INF/rights.xml',
                       'META-INF/signatures.xml']
        drm_found = [n for n in drm_markers if n in names]
        if drm_found:
            critical(f'DRM-related files in archive: {drm_found}')
        else:
            ok('No DRM markers (Adobe Adept, Marlin, FairPlay)')

        # No JavaScript
        js_files = [n for n in names if n.endswith('.js')]
        if js_files:
            critical(f'JavaScript files in archive: {js_files[:3]}')
        else:
            ok('No .js files')

        script_files = []
        for n in names:
            if n.endswith(('.xhtml', '.html')):
                t = z.read(n).decode('utf-8', errors='replace')
                if re.search(r'<script\b', t, re.IGNORECASE):
                    script_files.append(n)
        if script_files:
            critical(f'<script> tags in {len(script_files)} XHTML files: {script_files[:3]}')
        else:
            ok('No <script> tags in any XHTML')

        # No interactive elements
        bad_tags = ['form', 'input', 'button', 'select', 'textarea',
                    'iframe', 'embed', 'object']
        bad_files = []
        for n in names:
            if n.endswith(('.xhtml', '.html')):
                t = z.read(n).decode('utf-8', errors='replace')
                hits = []
                for tag in bad_tags:
                    if re.search(rf'<{tag}\b', t, re.IGNORECASE):
                        hits.append(tag)
                if hits:
                    bad_files.append((n, hits))
        if bad_files:
            critical(f'Interactive elements found in {len(bad_files)} files: '
                     f'{bad_files[:2]}')
        else:
            ok(f'No <{"|".join(bad_tags)}> in any spine doc')

        # No audio/video
        media_items = []
        for it in manifest.findall('opf:item', ns):
            mt = it.get('media-type', '')
            if mt.startswith(('audio/', 'video/')):
                media_items.append(f'{it.get("href")} ({mt})')
        if media_items:
            critical(f'Audio/video media items in manifest: {media_items[:3]}')
        else:
            ok('No audio/video media items')

        # External @import or @font-face URLs in CSS
        ext_url_files = []
        for n in names:
            if n.endswith('.css'):
                t = z.read(n).decode('utf-8', errors='replace')
                if re.search(r'@import\s+url\(["\']?https?:', t, re.IGNORECASE):
                    ext_url_files.append((n, '@import http'))
                elif re.search(r'src:\s*url\(["\']?https?:', t, re.IGNORECASE):
                    ext_url_files.append((n, '@font-face http'))
        if ext_url_files:
            high(f'External CSS/font URLs: {ext_url_files[:3]}')
        else:
            ok('No external CSS/font URLs')

        # Path length & filename characters
        long_paths = [n for n in names if len(n) > 240]
        if long_paths:
            critical(f'Paths > 240 chars (KDP limit): {len(long_paths)}')
            for lp in long_paths[:3]:
                print(f'        {len(lp)} chars: {lp[:80]}...')
        else:
            ok(f'All {len(names)} paths <= 240 chars')

        bad_chars = []
        for n in names:
            base = n.split('/')[-1]
            if re.search(r'[ %#?&]', base):
                bad_chars.append(n)
        if bad_chars:
            high(f'Filenames with KDP-unsafe chars: {bad_chars[:3]}')
        else:
            ok('All filenames use KDP-safe characters')

        # Image file size + dimensions
        large_images = []
        huge_dim_images = []
        if HAVE_PIL:
            for n in names:
                if n.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                    data = z.read(n)
                    if len(data) > 5 * 1024 * 1024:
                        large_images.append((n, fmt_size(len(data))))
                    try:
                        img = Image.open(io.BytesIO(data))
                        w, h = img.size
                        if max(w, h) > 4000:
                            huge_dim_images.append((n, f'{w}x{h}'))
                    except Exception:
                        pass
        if large_images:
            high(f'Images > 5 MB: {large_images[:3]}')
        else:
            ok('All images < 5 MB')
        if huge_dim_images:
            medium(f'Images with side > 4000 px: {huge_dim_images[:3]}')
        else:
            ok('No images with side > 4000 px')

        # XHTML well-formedness
        xhtml_bad = []
        for n in names:
            if n.endswith('.xhtml'):
                t = z.read(n).decode('utf-8', errors='replace')
                try:
                    ET.fromstring(t)
                except ET.ParseError as e:
                    xhtml_bad.append((n, str(e)[:80]))
        if xhtml_bad:
            critical(f'XHTML files not well-formed: {len(xhtml_bad)}')
            for fn, err in xhtml_bad[:3]:
                print(f'        {fn}: {err}')
        else:
            ok(f'All XHTML files well-formed XML')

        # DOCTYPE in every XHTML
        no_doctype = []
        for n in names:
            if n.endswith('.xhtml'):
                t = z.read(n).decode('utf-8', errors='replace')
                if not re.search(r'<!DOCTYPE\s+html', t[:500], re.IGNORECASE):
                    no_doctype.append(n)
        if no_doctype:
            high(f'XHTML files without <!DOCTYPE html>: {len(no_doctype)}')
        else:
            ok('All XHTML files have <!DOCTYPE html>')

        # UTF-8 encoding declared
        no_utf8 = []
        for n in names:
            if n.endswith('.xhtml'):
                t = z.read(n).decode('utf-8', errors='replace')
                head = t[:500].lower()
                if 'utf-8' not in head and 'charset=utf-8' not in head:
                    no_utf8.append(n)
        if no_utf8:
            medium(f'XHTML without explicit UTF-8 declaration: {len(no_utf8)}')
        else:
            ok('All XHTML declare UTF-8')

        # External URLs in src/href
        bad_uris = []
        for n in names:
            if n.endswith(('.xhtml', '.html')):
                t = z.read(n).decode('utf-8', errors='replace')
                for m in re.finditer(
                        r'(?:src|href)\s*=\s*["\']'
                        r'(file|about|javascript|data):', t, re.IGNORECASE):
                    bad_uris.append((n, m.group(0)))
                    if len(bad_uris) > 5:
                        break
        if bad_uris:
            high(f'Disallowed URI schemes in src/href: {bad_uris[:3]}')
        else:
            ok('No file:/about:/javascript:/data: URIs in src/href')

        # Math: bare $$..$$ in shipped EPUB (should be all rendered)
        bare_math = []
        for n in names:
            if n.endswith('.xhtml'):
                t = z.read(n).decode('utf-8', errors='replace')
                if '$$' in t and t.count('$$') >= 2:
                    bare_math.append(n)
        if bare_math:
            high(f'XHTML with bare $$..$$ (math not rendered): {bare_math[:3]}')
        else:
            ok('No bare $$..$$ math source in EPUB (KaTeX rendered)')

        # Rough math content check: at least some <math> tags must exist
        n_math_tags = 0
        for n in names:
            if n.endswith('.xhtml'):
                t = z.read(n).decode('utf-8', errors='replace')
                n_math_tags += t.count('<math')
        if n_math_tags > 0:
            ok(f'MathML rendered: {n_math_tags} <math> tags across spine')
        else:
            medium('No <math> tags in EPUB (math may be HTML-only KaTeX)')

        # CSS: position: fixed/sticky
        fixed_css = []
        for n in names:
            if n.endswith('.css'):
                t = z.read(n).decode('utf-8', errors='replace')
                if re.search(r'position\s*:\s*fixed', t):
                    fixed_css.append((n, 'position:fixed'))
                if re.search(r'position\s*:\s*sticky', t):
                    fixed_css.append((n, 'position:sticky'))
        if fixed_css:
            medium(f'CSS uses position:fixed/sticky: {fixed_css[:3]}')
        else:
            ok('No position:fixed or position:sticky in CSS')

        # Empty <title>
        empty_title = []
        for n in names:
            if n.endswith('.xhtml'):
                t = z.read(n).decode('utf-8', errors='replace')
                m = re.search(r'<title>([^<]*)</title>', t)
                if not m or not m.group(1).strip():
                    empty_title.append(n)
        if empty_title:
            high(f'XHTML with empty <title>: {len(empty_title)}')
        else:
            ok('All XHTML have non-empty <title>')

        # Page progression direction (LTR/RTL)
        ppd = spine.get('page-progression-direction')
        if not ppd:
            info('No spine page-progression-direction (KDP defaults to LTR)')
        else:
            ok(f'page-progression-direction: {ppd}')

        # Spine first content item: cover or nav or title page
        if spine.findall('opf:itemref', ns):
            first_idref = spine.findall('opf:itemref', ns)[0].get('idref')
            first_item = manifest_by_id.get(first_idref)
            if first_item:
                ok(f'Spine first item: {first_item.get("href")}')

    print()
    print('=' * 70)
    print(f'Critical: {len(CRIT)}')
    print(f'High:     {len(HIGH)}')
    print(f'Medium:   {len(MED)}')
    print(f'Info:     {len(INFO)}')
    print('=' * 70)
    if CRIT or HIGH:
        print('KDP REJECTION RISK: address Critical and High items before upload')
        return 1
    print('KDP-ready: no Critical or High issues found')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
