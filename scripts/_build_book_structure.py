#!/usr/bin/env python
"""
Build the CURRENT-STATE inventory of the LLMBook as a single YAML file.

Walks the file system in the order:
    Part I -> XII, Appendix A -> U, Glossary, Front-matter

For each artifact extracts:
    - title    (h1, with "Part X:" / "Chapter N:" / "Section N.M:" prefix stripped)
    - subtitle (p.chapter-subtitle text, if present)
    - opener_image (path of any <img> with src that points to an opener illustration, if present)

Writes the YAML to E:/Projects/BookBlogsHome/LLMBook/book_structure.yaml
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml
from bs4 import BeautifulSoup

BOOK_ROOT = Path("E:/Projects/BookBlogsHome/LLMBook")
OUT_PATH = BOOK_ROOT / "book_structure.yaml"

ROMAN = {
    1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI",
    7: "VII", 8: "VIII", 9: "IX", 10: "X", 11: "XI", 12: "XII",
}

FAILED_H1: list[str] = []


# --------------------------------------------------------------------------
# HTML helpers
# --------------------------------------------------------------------------

def parse(path: Path) -> BeautifulSoup | None:
    if not path.is_file():
        return None
    try:
        return BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    except Exception as exc:
        print(f"  ! parse error {path}: {exc}", file=sys.stderr)
        return None


def get_h1_text(soup: BeautifulSoup | None, rel_path: str) -> str:
    if soup is None:
        FAILED_H1.append(rel_path)
        return ""
    # Look for the first <h1> within the header (chapter-header) or the body.
    h1 = soup.find("h1")
    if h1 is None:
        FAILED_H1.append(rel_path)
        return ""
    # Strip nested page-current spans etc. - get_text gives plain text.
    text = h1.get_text(" ", strip=True)
    return text


def strip_prefix(text: str, pattern: str) -> str:
    """Strip prefixes such as 'Part I:', 'Chapter 0:', 'Section 0.1:', 'A.1', 'Glossary 1:'."""
    m = re.match(pattern, text)
    if m:
        return text[m.end():].strip(" :")
    return text.strip()


def get_subtitle(soup: BeautifulSoup | None) -> str | None:
    if soup is None:
        return None
    p = soup.find("p", class_="chapter-subtitle")
    if p is None:
        return None
    return p.get_text(" ", strip=True) or None


def get_opener_image(soup: BeautifulSoup | None) -> str | None:
    """Return src of the first illustration <img> in <figure class='illustration'>
    inside <main>, or None if not found."""
    if soup is None:
        return None
    main = soup.find("main")
    if main is None:
        return None
    fig = main.find("figure", class_="illustration")
    if fig is None:
        return None
    img = fig.find("img")
    if img is None:
        return None
    src = img.get("src")
    return src or None


# --------------------------------------------------------------------------
# Section helpers
# --------------------------------------------------------------------------

def section_entry(section_path: Path, sec_num: str, rel_for_log: str) -> dict[str, Any]:
    soup = parse(section_path)
    h1 = get_h1_text(soup, rel_for_log)
    # Strip patterns like 'Section 0.1:' OR 'A.1 ' OR 'Glossary 1:'
    title = h1
    # Section N.M: ...
    title = strip_prefix(title, r"^Section\s+[\dA-Za-z]+\.[\dA-Za-z]+\s*:\s*")
    # Appendix-style: "A.1 Linear Algebra Essentials"
    title = strip_prefix(title, r"^[A-Z]\.\d+\s+")
    # Glossary-style: "Glossary 1: Libraries, ..."
    title = strip_prefix(title, r"^Glossary\s+\d+\s*:\s*")
    return {
        "num": sec_num,
        "slug": section_path.stem,  # e.g. "section-0.1"
        "title": title,
    }


# --------------------------------------------------------------------------
# Chapter helpers
# --------------------------------------------------------------------------

CH_DIR_RE = re.compile(r"^module-(\d+)-(.+)$")
SEC_FILE_RE = re.compile(r"^section-([\dA-Za-z]+(?:\.[\dA-Za-z]+)?)\.html$")


def chapter_entry(chapter_dir: Path) -> dict[str, Any]:
    m = CH_DIR_RE.match(chapter_dir.name)
    assert m, f"unexpected chapter dir: {chapter_dir.name}"
    ch_num = int(m.group(1))
    slug = m.group(2)

    idx = chapter_dir / "index.html"
    rel = str(idx.relative_to(BOOK_ROOT)).replace("\\", "/")
    soup = parse(idx)
    h1 = get_h1_text(soup, rel)
    title = strip_prefix(h1, r"^Chapter\s+\d+\s*:\s*")
    subtitle = get_subtitle(soup)
    opener = get_opener_image(soup)

    # Sections in order section-N.1, N.2, ...
    sections: list[dict[str, Any]] = []
    for sf in sorted(chapter_dir.glob("section-*.html"), key=lambda p: _section_sort_key(p.name)):
        ms = SEC_FILE_RE.match(sf.name)
        if not ms:
            continue
        sec_num = ms.group(1)
        rel_s = str(sf.relative_to(BOOK_ROOT)).replace("\\", "/")
        sections.append(section_entry(sf, sec_num, rel_s))

    return {
        "num": ch_num,
        "slug": slug,
        "title": title,
        "subtitle": subtitle,
        "opener_image": opener,
        "sections": sections,
    }


def _section_sort_key(name: str) -> tuple:
    """Sort section-0.10.html after section-0.2.html naturally."""
    m = SEC_FILE_RE.match(name)
    if not m:
        return (999, name)
    parts = m.group(1).split(".")
    # numeric where possible
    key = []
    for p in parts:
        if p.isdigit():
            key.append((0, int(p)))
        else:
            key.append((1, p))
    return tuple(key)


# --------------------------------------------------------------------------
# Part helpers
# --------------------------------------------------------------------------

PART_DIR_RE = re.compile(r"^part-(\d+)-(.+)$")


def part_entry(part_dir: Path) -> dict[str, Any]:
    m = PART_DIR_RE.match(part_dir.name)
    assert m, f"unexpected part dir: {part_dir.name}"
    pnum = int(m.group(1))
    slug = m.group(2)

    idx = part_dir / "index.html"
    rel = str(idx.relative_to(BOOK_ROOT)).replace("\\", "/")
    soup = parse(idx)
    h1 = get_h1_text(soup, rel)
    # strip "Part X:" prefix (where X is roman)
    title = strip_prefix(h1, r"^Part\s+[IVXLCDM]+\s*:\s*")
    subtitle = get_subtitle(soup)
    opener = get_opener_image(soup)

    chapters: list[dict[str, Any]] = []
    for ch_dir in sorted(part_dir.iterdir(), key=lambda p: p.name):
        if not ch_dir.is_dir():
            continue
        if not CH_DIR_RE.match(ch_dir.name):
            continue
        chapters.append(chapter_entry(ch_dir))
    chapters.sort(key=lambda c: c["num"])

    return {
        "num": pnum,
        "roman": ROMAN.get(pnum, str(pnum)),
        "slug": slug,
        "title": title,
        "subtitle": subtitle,
        "opener_image": opener,
        "chapters": chapters,
    }


# --------------------------------------------------------------------------
# Appendix helpers
# --------------------------------------------------------------------------

APP_DIR_RE = re.compile(r"^appendix-([a-z])-(.+)$")
APP_SEC_RE = re.compile(r"^section-([a-z])\.(\d+)\.html$", re.IGNORECASE)


def appendix_entry(app_dir: Path) -> dict[str, Any]:
    m = APP_DIR_RE.match(app_dir.name)
    assert m, f"unexpected appendix dir: {app_dir.name}"
    letter = m.group(1).upper()
    slug = m.group(2)

    idx = app_dir / "index.html"
    rel = str(idx.relative_to(BOOK_ROOT)).replace("\\", "/")
    soup = parse(idx)
    h1 = get_h1_text(soup, rel)
    title = strip_prefix(h1, r"^Appendix\s+[A-Z]\s*:\s*")
    subtitle = get_subtitle(soup)
    opener = get_opener_image(soup)

    sections: list[dict[str, Any]] = []
    for sf in sorted(app_dir.glob("section-*.html"), key=lambda p: _appendix_section_sort_key(p.name)):
        ms = APP_SEC_RE.match(sf.name)
        if not ms:
            continue
        sec_num = f"{ms.group(1).upper()}.{ms.group(2)}"
        rel_s = str(sf.relative_to(BOOK_ROOT)).replace("\\", "/")
        sections.append(section_entry(sf, sec_num, rel_s))

    return {
        "letter": letter,
        "slug": slug,
        "title": title,
        "subtitle": subtitle,
        "opener_image": opener,
        "sections": sections,
    }


def _appendix_section_sort_key(name: str) -> tuple:
    m = APP_SEC_RE.match(name)
    if not m:
        return (999, name)
    return (m.group(1).lower(), int(m.group(2)))


# --------------------------------------------------------------------------
# Glossary helpers
# --------------------------------------------------------------------------

def glossary_entry() -> dict[str, Any]:
    gdir = BOOK_ROOT / "appendices" / "glossary"
    idx = gdir / "index.html"
    rel = str(idx.relative_to(BOOK_ROOT)).replace("\\", "/")
    soup = parse(idx)
    h1 = get_h1_text(soup, rel)
    title = h1.strip() or "Glossary"
    subtitle = get_subtitle(soup)
    opener = get_opener_image(soup)

    sections: list[dict[str, Any]] = []
    for sf in sorted(gdir.glob("section-*.html"), key=lambda p: _appendix_section_sort_key(p.name)):
        ms = APP_SEC_RE.match(sf.name)
        if not ms:
            continue
        sec_num = f"{ms.group(1).upper()}.{ms.group(2)}"
        rel_s = str(sf.relative_to(BOOK_ROOT)).replace("\\", "/")
        sections.append(section_entry(sf, sec_num, rel_s))

    return {
        "title": title,
        "subtitle": subtitle,
        "opener_image": opener,
        "sections": sections,
    }


# --------------------------------------------------------------------------
# Front-matter helpers
# --------------------------------------------------------------------------

def front_matter_entries() -> list[dict[str, Any]]:
    fm_dir = BOOK_ROOT / "front-matter"
    entries: list[dict[str, Any]] = []
    for f in sorted(fm_dir.glob("*.html")):
        if f.name == "index.html":
            continue
        rel = str(f.relative_to(BOOK_ROOT)).replace("\\", "/")
        soup = parse(f)
        h1 = get_h1_text(soup, rel)
        entries.append({
            "slug": f.stem,
            "title": h1.strip(),
        })
    return entries


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main() -> int:
    print(f"Building structure for {BOOK_ROOT}", file=sys.stderr)

    # 1. Parts in numeric order 1..12
    parts: list[dict[str, Any]] = []
    part_dirs = sorted(
        [p for p in BOOK_ROOT.iterdir() if p.is_dir() and PART_DIR_RE.match(p.name)],
        key=lambda p: int(PART_DIR_RE.match(p.name).group(1)),
    )
    for pd in part_dirs:
        parts.append(part_entry(pd))

    # 2. Appendices A..U
    app_root = BOOK_ROOT / "appendices"
    appendices: list[dict[str, Any]] = []
    app_dirs = sorted(
        [p for p in app_root.iterdir() if p.is_dir() and APP_DIR_RE.match(p.name)],
        key=lambda p: APP_DIR_RE.match(p.name).group(1),  # letter
    )
    for ad in app_dirs:
        appendices.append(appendix_entry(ad))

    # 3. Glossary
    glossary = glossary_entry()

    # 4. Front-matter
    fm = front_matter_entries()

    book = {
        "book": {
            "title": "Building Conversational AI with LLMs and Agents",
            "edition": "Fifteenth Edition",
            "year": 2026,
        },
        "parts": parts,
        "appendices": appendices,
        "glossary": glossary,
        "front_matter": fm,
    }

    OUT_PATH.write_text(
        yaml.safe_dump(book, sort_keys=False, allow_unicode=True, width=120),
        encoding="utf-8",
    )

    # ---- Report --------------------------------------------------
    n_parts = len(parts)
    n_chapters = sum(len(p["chapters"]) for p in parts)
    n_sections = sum(len(c["sections"]) for p in parts for c in p["chapters"])
    n_app = len(appendices)
    n_app_sections = sum(len(a["sections"]) for a in appendices)
    n_gloss = len(glossary["sections"])
    n_fm = len(fm)

    print(f"\nWrote {OUT_PATH}")
    print(f"  parts                 : {n_parts}")
    print(f"  chapters              : {n_chapters}")
    print(f"  sections              : {n_sections}")
    print(f"  appendices            : {n_app}")
    print(f"  appendix sections     : {n_app_sections}")
    print(f"  glossary sections     : {n_gloss}")
    print(f"  front-matter entries  : {n_fm}")

    if FAILED_H1:
        print(f"\nH1 extraction FAILED for {len(FAILED_H1)} page(s):")
        for p in FAILED_H1:
            print(f"  - {p}")
    else:
        print("\nH1 extraction: no failures.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
