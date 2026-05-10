"""
Structural EPUB validator (Python-only, no Java/epubcheck required).

Performs the checks that catch the vast majority of EPUB defects KDP would flag.
This is NOT a substitute for the official IDPF epubcheck (which validates
schema-level XHTML and OPF semantics), but covers:

  - Valid ZIP archive
  - mimetype is first entry and uncompressed (EPUB spec mandate)
  - META-INF/container.xml present and points to valid OPF
  - OPF parses; all required Dublin Core fields present
  - Every manifest item file exists in the zip
  - Every spine itemref references a valid manifest item
  - Cover declared and image present
  - Nav document present
  - For each XHTML in the manifest:
      * parses as XML
      * every <img src> resolves to a file in the zip
      * every internal <a href> (non-external) resolves to a manifest item
  - Image dimensions / sizes summary (KDP rejects 0-dimension or oversized)
  - File-size summary (KDP limits + delivery-fee estimate)

Outputs a human-readable report to stdout AND to `structural_report.txt`.

Exit code: 0 if no errors, 1 if any errors detected.
Warnings (suspicious but not blocking) do not change the exit code.
"""
from __future__ import annotations

import io
import json
import re
import sys
import zipfile
from collections import defaultdict
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET

from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parents[2]
EPUB_PATH = PROJECT_ROOT / "KDP" / "output" / "building-conversational-ai-llms-agents.epub"
REPORT_PATH = Path(__file__).resolve().parent / "structural_report.txt"

NS = {
    "ocf": "urn:oasis:names:tc:opendocument:xmlns:container",
    "opf": "http://www.idpf.org/2007/opf",
    "dc": "http://purl.org/dc/elements/1.1/",
    "xhtml": "http://www.w3.org/1999/xhtml",
    "epub": "http://www.idpf.org/2007/ops",
}

errors: list[str] = []
warnings: list[str] = []
info: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def note(msg: str) -> None:
    info.append(msg)


def check_zip_structure(zf: zipfile.ZipFile) -> None:
    names = zf.namelist()
    if not names:
        err("EPUB zip is empty")
        return
    note(f"ZIP entries: {len(names)}")

    # mimetype must be first AND uncompressed
    first = zf.infolist()[0]
    if first.filename != "mimetype":
        err(f"first zip entry must be 'mimetype', got '{first.filename}'")
    elif first.compress_type != zipfile.ZIP_STORED:
        err("'mimetype' must be uncompressed (ZIP_STORED), got compressed")
    else:
        content = zf.read("mimetype").decode("ascii", errors="replace").strip()
        if content != "application/epub+zip":
            err(f"mimetype content must be 'application/epub+zip', got '{content}'")
        else:
            note("mimetype: OK (first, uncompressed, correct value)")


def find_opf_path(zf: zipfile.ZipFile) -> str | None:
    if "META-INF/container.xml" not in zf.namelist():
        err("missing META-INF/container.xml")
        return None
    try:
        root = ET.fromstring(zf.read("META-INF/container.xml"))
    except ET.ParseError as e:
        err(f"META-INF/container.xml does not parse: {e}")
        return None
    rootfile = root.find(".//ocf:rootfile", NS)
    if rootfile is None:
        err("container.xml has no <rootfile>")
        return None
    full_path = rootfile.get("full-path")
    if not full_path:
        err("container.xml <rootfile> has no full-path attribute")
        return None
    if full_path not in zf.namelist():
        err(f"OPF file '{full_path}' declared in container.xml is not in the zip")
        return None
    note(f"OPF path: {full_path}")
    return full_path


def parse_opf(zf: zipfile.ZipFile, opf_path: str) -> dict:
    """Return a dict with metadata, manifest, spine, and OPF base directory."""
    try:
        opf = ET.fromstring(zf.read(opf_path))
    except ET.ParseError as e:
        err(f"OPF '{opf_path}' does not parse: {e}")
        return {}

    base_dir = ""
    if "/" in opf_path:
        base_dir = opf_path.rsplit("/", 1)[0] + "/"

    meta = opf.find("opf:metadata", NS)
    if meta is None:
        err("OPF has no <metadata>")
        return {}

    md: dict = {}
    md["title"] = [t.text for t in meta.findall("dc:title", NS) if t.text]
    md["creator"] = [c.text for c in meta.findall("dc:creator", NS) if c.text]
    md["language"] = [l.text for l in meta.findall("dc:language", NS) if l.text]
    md["identifier"] = [i.text for i in meta.findall("dc:identifier", NS) if i.text]
    md["description"] = [d.text for d in meta.findall("dc:description", NS) if d.text]
    md["publisher"] = [p.text for p in meta.findall("dc:publisher", NS) if p.text]
    md["date"] = [d.text for d in meta.findall("dc:date", NS) if d.text]
    md["subject"] = [s.text for s in meta.findall("dc:subject", NS) if s.text]
    md["rights"] = [r.text for r in meta.findall("dc:rights", NS) if r.text]

    # Manifest
    manifest_el = opf.find("opf:manifest", NS)
    if manifest_el is None:
        err("OPF has no <manifest>")
        return {}
    manifest: dict[str, dict] = {}
    cover_image_id = None
    nav_id = None
    for item in manifest_el.findall("opf:item", NS):
        iid = item.get("id")
        href = item.get("href")
        media_type = item.get("media-type")
        properties = (item.get("properties") or "").split()
        if not iid or not href or not media_type:
            err(f"manifest item missing id/href/media-type: {item.attrib}")
            continue
        full_zip_path = base_dir + href
        manifest[iid] = {
            "href": href,
            "full": full_zip_path,
            "media_type": media_type,
            "properties": properties,
        }
        if "cover-image" in properties:
            cover_image_id = iid
        if "nav" in properties:
            nav_id = iid

    # Spine
    spine_el = opf.find("opf:spine", NS)
    if spine_el is None:
        err("OPF has no <spine>")
        return {}
    spine_refs = [it.get("idref") for it in spine_el.findall("opf:itemref", NS)]

    return {
        "base_dir": base_dir,
        "metadata": md,
        "manifest": manifest,
        "spine_refs": spine_refs,
        "cover_image_id": cover_image_id,
        "nav_id": nav_id,
    }


def check_metadata(md: dict) -> None:
    required = {
        "title": "dc:title",
        "creator": "dc:creator (author)",
        "language": "dc:language",
        "identifier": "dc:identifier",
    }
    for key, label in required.items():
        if not md.get(key):
            err(f"missing required metadata: {label}")
    if md.get("title"):
        note(f"title: {md['title'][0]!r}")
    if md.get("creator"):
        note(f"authors ({len(md['creator'])}): {', '.join(md['creator'])}")
    if md.get("language"):
        note(f"language: {md['language'][0]!r}")
    if md.get("identifier"):
        note(f"identifier: {md['identifier'][0]!r}")
    if md.get("description"):
        d = md["description"][0]
        note(f"description: {len(d)} chars (preview: {d[:100]!r})")
        if len(d) > 4000:
            warn(f"description is {len(d)} chars; KDP web form caps at 4000")
    else:
        warn("missing dc:description (KDP will require this on the web form anyway)")
    if not md.get("subject"):
        warn("no dc:subject (keywords) in OPF; KDP form will require keywords too")
    else:
        note(f"keywords ({len(md['subject'])}): {', '.join(md['subject'])}")


def check_manifest_files(zf: zipfile.ZipFile, info: dict) -> dict[str, int]:
    names = set(zf.namelist())
    missing = []
    sizes: dict[str, int] = {}
    for iid, item in info["manifest"].items():
        if item["full"] not in names:
            err(f"manifest item '{iid}' file not in zip: {item['full']}")
            missing.append(iid)
        else:
            sizes[item["full"]] = zf.getinfo(item["full"]).file_size
    note(f"manifest items: {len(info['manifest'])} (missing files: {len(missing)})")
    return sizes


def check_spine(info: dict) -> None:
    bad = [r for r in info["spine_refs"] if r not in info["manifest"]]
    if bad:
        err(f"spine references {len(bad)} unknown idref(s): {bad[:5]}...")
    note(f"spine: {len(info['spine_refs'])} entries")


def check_cover(info: dict) -> None:
    if not info.get("cover_image_id"):
        err("no manifest item has properties='cover-image' (KDP/Kindle uses this)")
    else:
        cover_item = info["manifest"][info["cover_image_id"]]
        note(f"cover image: {cover_item['href']} ({cover_item['media_type']})")


def check_nav(info: dict) -> None:
    if not info.get("nav_id"):
        err("no manifest item has properties='nav' (EPUB 3 requires a nav doc)")
    else:
        nav_item = info["manifest"][info["nav_id"]]
        note(f"nav doc: {nav_item['href']}")


def check_xhtml_internals(zf: zipfile.ZipFile, info: dict) -> None:
    """For each XHTML in the manifest, verify img/href targets resolve."""
    base_dir = info["base_dir"]
    manifest_files = {item["full"]: item for item in info["manifest"].values()}
    href_lookup = {item["full"] for item in info["manifest"].values()}

    n_xhtml = 0
    n_imgs_total = 0
    n_imgs_missing = 0
    n_links_total = 0
    n_links_broken = 0
    parse_errors = 0

    for iid, item in info["manifest"].items():
        if item["media_type"] not in ("application/xhtml+xml", "text/html"):
            continue
        n_xhtml += 1
        try:
            data = zf.read(item["full"])
        except KeyError:
            continue
        try:
            root = ET.fromstring(data)
        except ET.ParseError as e:
            parse_errors += 1
            err(f"XHTML parse error in {item['href']}: {e}")
            continue

        chapter_dir = item["full"].rsplit("/", 1)[0] if "/" in item["full"] else ""

        for img in root.iter("{http://www.w3.org/1999/xhtml}img"):
            src = img.get("src", "")
            if not src or src.startswith(("http:", "https:", "data:")):
                continue
            n_imgs_total += 1
            target = resolve_relative_zip(chapter_dir, src)
            if target not in href_lookup and target not in zf.namelist():
                n_imgs_missing += 1
                if n_imgs_missing <= 5:
                    err(f"broken image in {item['href']}: {src} (resolved {target})")

        for a in root.iter("{http://www.w3.org/1999/xhtml}a"):
            href = a.get("href", "")
            if not href or href.startswith(("http:", "https:", "mailto:", "javascript:", "tel:", "#")):
                continue
            n_links_total += 1
            href_no_frag = href.split("#", 1)[0]
            target = resolve_relative_zip(chapter_dir, href_no_frag)
            if target and target not in href_lookup and target not in zf.namelist():
                n_links_broken += 1
                if n_links_broken <= 5:
                    warn(f"broken link in {item['href']}: {href} (resolved {target})")

    note(f"XHTML files: {n_xhtml} (parse errors: {parse_errors})")
    note(f"images checked: {n_imgs_total} (missing: {n_imgs_missing})")
    note(f"internal links checked: {n_links_total} (broken: {n_links_broken})")


def resolve_relative_zip(base_dir: str, href: str) -> str:
    """Resolve a relative href against a directory inside the zip."""
    if not href:
        return ""
    if href.startswith("/"):
        return href.lstrip("/")
    parts = (base_dir + "/" if base_dir else "").split("/")
    # Strip empty trailing
    parts = [p for p in parts if p]
    for piece in href.split("/"):
        if piece == "..":
            if parts:
                parts.pop()
        elif piece in ("", "."):
            continue
        else:
            parts.append(piece)
    return "/".join(parts)


def check_image_dimensions(zf: zipfile.ZipFile, info: dict) -> None:
    """Open every image and warn on suspicious dimensions or sizes."""
    n = 0
    biggest: tuple[int, str] | None = None
    big_count = 0
    for iid, item in info["manifest"].items():
        if not item["media_type"].startswith("image/"):
            continue
        n += 1
        try:
            data = zf.read(item["full"])
            size = len(data)
            if size > 1024 * 1024:
                big_count += 1
                if biggest is None or size > biggest[0]:
                    biggest = (size, item["href"])
            if item["media_type"] != "image/svg+xml":
                with Image.open(io.BytesIO(data)) as im:
                    if 0 in im.size:
                        err(f"image {item['href']} has zero dimension {im.size}")
        except Exception as e:
            warn(f"could not read image {item['href']}: {e}")

    note(f"images: {n} total, {big_count} > 1 MB"
         + (f", largest: {biggest[1]} ({biggest[0]/1024:.0f} KB)" if biggest else ""))


def check_kdp_size(zf: zipfile.ZipFile) -> None:
    epub_size = EPUB_PATH.stat().st_size
    mb = epub_size / 1024 / 1024
    note(f"EPUB file size: {mb:.2f} MB ({epub_size:,} bytes)")
    if mb > 650:
        err(f"EPUB exceeds KDP 650 MB upload limit")
    elif mb > 200:
        warn(f"EPUB is {mb:.0f} MB; large for Kindle. Delivery fee at 70% royalty: ${mb*0.15:.2f}/sale")
    elif mb > 50:
        note(f"EPUB is {mb:.0f} MB. Delivery fee at 70% royalty: ${mb*0.15:.2f}/sale; recommend 35% royalty plan.")
    else:
        note(f"EPUB size acceptable for either royalty plan.")


# --------------------------------------------------------------------- main

def main() -> int:
    if not EPUB_PATH.exists():
        print(f"ERROR: EPUB not found at {EPUB_PATH}", file=sys.stderr)
        return 2

    note(f"EPUB: {EPUB_PATH}")

    try:
        zf = zipfile.ZipFile(EPUB_PATH, "r")
    except zipfile.BadZipFile as e:
        err(f"EPUB is not a valid zip: {e}")
        return write_report()

    with zf:
        check_zip_structure(zf)
        opf_path = find_opf_path(zf)
        if opf_path:
            opf_info = parse_opf(zf, opf_path)
            if opf_info:
                check_metadata(opf_info["metadata"])
                check_manifest_files(zf, opf_info)
                check_spine(opf_info)
                check_cover(opf_info)
                check_nav(opf_info)
                check_xhtml_internals(zf, opf_info)
                check_image_dimensions(zf, opf_info)
        check_kdp_size(zf)

    return write_report()


def write_report() -> int:
    lines: list[str] = []
    lines.append("=" * 70)
    lines.append("EPUB STRUCTURAL VALIDATION REPORT")
    lines.append("=" * 70)
    lines.append("")
    lines.append("INFO")
    lines.append("-" * 70)
    for m in info:
        lines.append(f"  {m}")
    lines.append("")
    lines.append(f"WARNINGS ({len(warnings)})")
    lines.append("-" * 70)
    for m in warnings:
        lines.append(f"  WARN  {m}")
    if not warnings:
        lines.append("  (none)")
    lines.append("")
    lines.append(f"ERRORS ({len(errors)})")
    lines.append("-" * 70)
    for m in errors:
        lines.append(f"  ERROR {m}")
    if not errors:
        lines.append("  (none)")
    lines.append("")
    lines.append("=" * 70)
    if errors:
        lines.append(f"RESULT: FAIL ({len(errors)} errors)")
    elif warnings:
        lines.append(f"RESULT: PASS WITH WARNINGS ({len(warnings)} warnings)")
    else:
        lines.append("RESULT: PASS")
    lines.append("=" * 70)
    out = "\n".join(lines)
    print(out)
    REPORT_PATH.write_text(out, encoding="utf-8")
    print(f"\nReport saved to: {REPORT_PATH}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
