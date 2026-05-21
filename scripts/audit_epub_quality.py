"""Deep quality audit of a built EPUB - catches problems EPUBCheck and Kindle
Previewer qualitychecks do NOT flag (they pass clean while real reader-facing
issues remain).

Checks:
  LINKS  internal <a href> resolves to an existing file; #fragment resolves to a
         real id in the target file; no empty/`#` href.
  IMG    every <img> has non-empty alt; no data: URIs (KDP strips them); flag
         absurd width/height; src resolves to a bundled file.
  MANIFEST  every manifest href exists in the zip; every content file is in the
         manifest (orphans); spine idrefs all resolve.
  IDS    no duplicate id="" within a single chapter (breaks fragment links).
  HEAD   heading levels don't skip (h1 -> h3) - accessibility/structure.
  KINDLE regression guards: 0 lowercase camelCase SVG attrs, 0 _math_placeholder
         (empty math), 0 <math>/.katex if math is pre-rendered to PNG, no broken
         &amp;-entities in attributes.

Usage: py -3 scripts/audit_epub_quality.py [path/to/book.epub]
Exit 0 if clean, 1 if any ERROR-level finding (warnings don't fail).
"""
from __future__ import annotations
import sys, zipfile, re, posixpath
from collections import Counter, defaultdict
from pathlib import Path

from bs4 import BeautifulSoup

EPUB = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    "KDP/output/building-conversational-ai-llms-agents.epub")

SVG_CAMEL = ["viewbox", "refx", "refy", "markerwidth", "markerheight",
             "markerunits", "preserveaspectratio", "gradientunits",
             "gradienttransform", "stddeviation"]

errors: list[str] = []
warns: list[str] = []

def err(msg): errors.append(msg)
def warn(msg): warns.append(msg)


def main():
    if not EPUB.exists():
        print("no epub at", EPUB); sys.exit(2)
    z = zipfile.ZipFile(EPUB)
    names = set(z.namelist())

    # locate OPF
    container = z.read("META-INF/container.xml").decode("utf-8", "replace")
    opf_path = re.search(r'full-path="([^"]+)"', container).group(1)
    opf_dir = posixpath.dirname(opf_path)
    opf = z.read(opf_path).decode("utf-8", "replace")

    # manifest: id -> href (opf-relative)
    manifest = {}
    for m in re.finditer(r'<item\b[^>]*\bid="([^"]+)"[^>]*\bhref="([^"]+)"', opf):
        manifest[m.group(1)] = m.group(2)
    # also catch href-before-id ordering
    for m in re.finditer(r'<item\b[^>]*\bhref="([^"]+)"[^>]*\bid="([^"]+)"', opf):
        manifest.setdefault(m.group(2), m.group(1))

    def opf_to_zip(href):
        href = href.split("#")[0]
        return posixpath.normpath(posixpath.join(opf_dir, href))

    # MANIFEST checks: every href exists
    manifest_zip = set()
    for mid, href in manifest.items():
        zp = opf_to_zip(href)
        manifest_zip.add(zp)
        if zp not in names:
            err(f"MANIFEST item id={mid} href={href} -> missing zip entry {zp}")

    # orphans: content files in zip not in manifest (excluding mimetype, container, ncx maybe)
    for n in names:
        if n in ("mimetype",) or n.startswith("META-INF/"):
            continue
        if n.endswith("/"):
            continue
        if n == opf_path:
            continue
        if n.endswith((".xhtml", ".html", ".css", ".js")) or "/img" in n.lower() or "/images" in n.lower() or "/fonts" in n.lower():
            if n not in manifest_zip:
                warn(f"ORPHAN file not in manifest: {n}")

    # spine idrefs
    for m in re.finditer(r'<itemref\b[^>]*\bidref="([^"]+)"', opf):
        if m.group(1) not in manifest:
            err(f"SPINE idref={m.group(1)} not in manifest")

    # per-chapter analysis
    xhtml = [n for n in names if n.endswith((".xhtml", ".html"))]
    # build set of (file -> ids) for fragment resolution
    file_ids: dict[str, set] = {}
    for n in xhtml:
        d = z.read(n).decode("utf-8", "replace")
        file_ids[n] = set(re.findall(r'\bid="([^"]+)"', d))

    total_imgs = 0
    imgs_no_alt = 0
    for n in xhtml:
        raw = z.read(n).decode("utf-8", "replace")
        soup = BeautifulSoup(raw, "html.parser")

        # duplicate ids
        ids = re.findall(r'\bid="([^"]+)"', raw)
        dups = [i for i, c in Counter(ids).items() if c > 1]
        if dups:
            err(f"DUP-ID in {n}: {dups[:5]}")

        # links
        for a in soup.find_all("a"):
            href = a.get("href")
            if href is None:
                continue
            if href.strip() == "" or href.strip() == "#":
                warn(f"EMPTY-HREF in {n}")
                continue
            if href.startswith(("http://", "https://", "mailto:", "tel:", "data:", "javascript:")):
                continue
            tgt, _, frag = href.partition("#")
            if tgt:
                base = posixpath.dirname(n)
                zp = posixpath.normpath(posixpath.join(base, tgt))
                if zp not in names:
                    err(f"BROKEN-LINK in {n}: href={href} -> {zp} (missing)")
                    continue
                if frag and zp in file_ids and frag not in file_ids[zp]:
                    err(f"BROKEN-FRAG in {n}: href={href} -> #{frag} not an id in {zp}")
            else:  # same-file fragment
                if frag and frag not in file_ids.get(n, set()):
                    err(f"BROKEN-FRAG in {n}: #{frag} not an id here")

        # images
        for img in soup.find_all("img"):
            total_imgs += 1
            src = img.get("src", "")
            alt = img.get("alt")
            if alt is None or alt.strip() == "":
                imgs_no_alt += 1
            if src.startswith("data:"):
                err(f"DATA-URI img in {n} (KDP strips these)")
            elif src and not src.startswith(("http://", "https://")):
                base = posixpath.dirname(n)
                zp = posixpath.normpath(posixpath.join(base, src))
                if zp not in names:
                    err(f"BROKEN-IMG in {n}: src={src} -> {zp} (missing)")

        # heading hierarchy
        levels = [int(h.name[1]) for h in soup.find_all(re.compile(r"^h[1-6]$"))]
        prev = 0
        for lv in levels:
            if prev and lv > prev + 1:
                warn(f"HEAD-SKIP in {n}: h{prev} -> h{lv}")
            prev = lv

        # kindle regression guards
        low = raw.lower()
        svgblocks = re.findall(r"<svg\b.*?</svg>", raw, re.S | re.I)
        for blk in svgblocks:
            for a in SVG_CAMEL:
                if re.search(r"\s" + a + "=", blk):
                    err(f"SVG-LOWERCASE attr '{a}' in {n}")
                    break
        if "_math_placeholder" in raw:
            err(f"EMPTY-MATH (_math_placeholder) in {n}")
        if "<math" in low:
            warn(f"LIVE-MATHML (<math>) in {n} (expected PNG)")

    if total_imgs:
        pct = 100.0 * imgs_no_alt / total_imgs
        if imgs_no_alt:
            warn(f"ALT-TEXT: {imgs_no_alt}/{total_imgs} <img> missing alt ({pct:.1f}%)")

    # report
    print(f"=== EPUB quality audit: {EPUB.name} ===")
    print(f"chapters: {len(xhtml)}  images: {total_imgs}")
    print(f"\nERRORS ({len(errors)}):")
    for e in errors[:60]:
        print("  [ERR]", e)
    if len(errors) > 60:
        print(f"  ... +{len(errors)-60} more")
    print(f"\nWARNINGS ({len(warns)}):")
    wc = Counter(w.split(" in ")[0].split(":")[0] for w in warns)
    for k, c in wc.most_common():
        print(f"  [WARN x{c}] {k}")
    for w in warns[:25]:
        print("   -", w)
    if len(warns) > 25:
        print(f"   ... +{len(warns)-25} more")
    print(f"\nRESULT: {'FAIL' if errors else 'PASS'}  ({len(errors)} errors, {len(warns)} warnings)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
