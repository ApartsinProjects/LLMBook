"""Fix deterministic header-drift patterns from header-style-audit.md.

Patterns fixed:
  1. PAGEFIND_WRONG_CHAPTER (131 files): chapter:Chapter N value stale.
     For each section/chapter file under part-N/module-MM/, look up the
     real chapter number from the directory name and the real chapter
     title from the chapter's index.html <h1>. Rewrite the
     pagefind-meta-injected chapter span.

  2. PAGEFIND_WRONG_PART (14 files): part:Part X value stale.
     Look up real part from the part-N-slug directory and rewrite the
     part: pagefind-meta-injected span.

  3. HEADER_MISSING_BOOK_LINK (57 files): book title rendered as plain
     text inside <nav class="header-nav">. Replace with the linked form.

  4. BOOK_LINK_HREF (2 files): book-title-link href has wrong relative
     depth for the file's location. Fix based on path depth.

  5. UNEXPECTED_SUBTITLE (15 files): section pages with
     <p class="chapter-subtitle"> in the header. Remove (sections should
     not have a chapter-subtitle).

Read-only with no flag; --apply to write.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude"}

PART_RE = re.compile(r"part-(\d+)-")
MODULE_RE = re.compile(r"module-(\d+)-")
SECTION_RE = re.compile(r"section-(\d+)\.(\d+)\.html")


def _read_h1(p: Path) -> str | None:
    if not p.exists():
        return None
    text = p.read_text(encoding="utf-8")
    m = re.search(r"<h1[^>]*>([^<]+)</h1>", text)
    if m:
        return m.group(1).strip()
    return None


_PART_ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI",
               7: "VII", 8: "VIII", 9: "IX", 10: "X", 11: "XI", 12: "XII"}


def _build_lookup() -> tuple[dict, dict]:
    """Build {part_num -> part_title}, {(part_num, chapter_num) -> title}."""
    part_titles: dict[int, str] = {}
    chapter_titles: dict[tuple[int, int], str] = {}
    for part_dir in ROOT.iterdir():
        if not part_dir.is_dir():
            continue
        pm = PART_RE.match(part_dir.name)
        if not pm:
            continue
        pnum = int(pm.group(1))
        # Part title from part-N-slug/index.html <h1>
        ptitle = _read_h1(part_dir / "index.html") or f"Part {pnum}"
        part_titles[pnum] = ptitle
        # Chapters
        for mod_dir in part_dir.iterdir():
            if not mod_dir.is_dir():
                continue
            mm = MODULE_RE.match(mod_dir.name)
            if not mm:
                continue
            cnum = int(mm.group(1))
            ctitle = _read_h1(mod_dir / "index.html") or f"Chapter {cnum}"
            chapter_titles[(pnum, cnum)] = ctitle
    return part_titles, chapter_titles


def _fix_pagefind_meta(text: str, part_num: int, part_title: str,
                        chapter_num: int | None,
                        chapter_title: str | None) -> tuple[str, int]:
    """Update pagefind-meta-injected part: and chapter: spans."""
    changes = 0
    # Build expected values
    roman = _PART_ROMAN.get(part_num, str(part_num))
    # Normalize the part title (strip leading "Part X: ")
    if part_title.startswith(f"Part {roman}:"):
        part_title_clean = part_title[len(f"Part {roman}:"):].strip()
    else:
        part_title_clean = part_title
    expected_part = f"Part {roman}: {part_title_clean}"

    if chapter_num is not None and chapter_title is not None:
        # Normalize chapter title (strip leading "Chapter N:")
        ct_clean = chapter_title
        m = re.match(r"^Chapter\s+\d+:\s*(.+)$", chapter_title)
        if m:
            ct_clean = m.group(1).strip()
        expected_chapter = f"Chapter {chapter_num}: {ct_clean}"
    else:
        expected_chapter = None

    # Update part:
    def repl_part(m: re.Match) -> str:
        nonlocal changes
        current = m.group(1)
        if current != expected_part:
            changes += 1
            return m.group(0).replace(f'part:{current}', f'part:{expected_part}')
        return m.group(0)
    text = re.sub(
        r'<span[^>]*data-pagefind-meta="part:([^"]+)"[^>]*></span>',
        repl_part, text)

    # Update chapter:
    if expected_chapter:
        def repl_ch(m: re.Match) -> str:
            nonlocal changes
            current = m.group(1)
            if current != expected_chapter:
                changes += 1
                return m.group(0).replace(
                    f'chapter:{current}', f'chapter:{expected_chapter}')
            return m.group(0)
        text = re.sub(
            r'<span[^>]*data-pagefind-meta="chapter:([^"]+)"[^>]*></span>',
            repl_ch, text)
    return text, changes


# Standard header-nav template (matches the working chapter-header style)
_LINKED_BOOK_TITLE = (
    '<a class="book-title-link" href="{href}">'
    'Building Conversational AI with LLMs and Agents</a>'
)


def _fix_book_link(text: str, depth: int) -> tuple[str, int]:
    """Replace plain text 'Building Conversational AI...' inside header-nav
    with the linked form. depth is number of '../' segments needed to
    reach book root from the file."""
    # Pattern: <nav class="header-nav"> ... Building Conversational AI ... </nav>
    # We look for either plain text or a wrong link in that block.
    href = "../" * depth + "index.html"

    # Case 1: plain text inside header-nav
    nav_pattern = re.compile(
        r'(<nav class="header-nav">)([\s\S]*?)(</nav>)',
        re.IGNORECASE,
    )
    n = 0
    def repl(m: re.Match) -> str:
        nonlocal n
        nav_open, inner, nav_close = m.group(1), m.group(2), m.group(3)
        if '<a class="book-title-link"' in inner:
            # Maybe wrong href? Check.
            new_inner = re.sub(
                r'<a class="book-title-link"[^>]*>'
                r'Building Conversational AI with LLMs and Agents</a>',
                _LINKED_BOOK_TITLE.format(href=href),
                inner,
            )
            if new_inner != inner:
                n += 1
                return nav_open + new_inner + nav_close
            return m.group(0)
        # No book-title-link anchor. Replace plain text mention.
        new_inner = inner
        new_inner = re.sub(
            r'(\s*)Building Conversational AI with LLMs and Agents(\s*)',
            r'\1' + _LINKED_BOOK_TITLE.format(href=href) + r'\2',
            new_inner,
            count=1,
        )
        if new_inner != inner:
            n += 1
            return nav_open + new_inner + nav_close
        return m.group(0)
    text = nav_pattern.sub(repl, text)
    return text, n


def _strip_unexpected_subtitle(text: str) -> tuple[str, int]:
    """Remove <p class="chapter-subtitle">...</p> from section files
    (sections should not have a chapter-subtitle; only chapter indexes)."""
    new_text, n = re.subn(
        r'<p\s+class="chapter-subtitle"[^>]*>[^<]*</p>\s*',
        '',
        text,
    )
    return new_text, n


def _depth_from_root(p: Path) -> int:
    """Return number of '../' segments needed from file to ROOT."""
    rel = p.relative_to(ROOT)
    # Each path component except the file name is a directory level
    return len(rel.parents) - 1  # exclude '.'


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply

    part_titles, chapter_titles = _build_lookup()
    print(f"Loaded {len(part_titles)} parts, {len(chapter_titles)} chapters")

    n_pagefind = 0
    n_booklink = 0
    n_subtitle = 0
    n_files_edited = 0

    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        # Identify part / chapter context from path
        part_num = None
        chapter_num = None
        for parent in p.parts:
            pm = PART_RE.match(parent)
            if pm:
                part_num = int(pm.group(1))
            mm = MODULE_RE.match(parent)
            if mm:
                chapter_num = int(mm.group(1))

        if part_num is None:
            # Not in a part directory (could be appendix, front-matter, etc.).
            # Still apply book-link fix.
            text = p.read_text(encoding="utf-8")
            orig = text
            depth = _depth_from_root(p)
            text, dn = _fix_book_link(text, depth)
            if dn:
                n_booklink += dn
            # Strip unexpected subtitle from appendix/section files
            if SECTION_RE.match(p.name) and "appendix" in str(p.parent):
                text, sn = _strip_unexpected_subtitle(text)
                n_subtitle += sn
            if text != orig:
                n_files_edited += 1
                if not dry_run:
                    p.write_text(text, encoding="utf-8")
            continue

        text = p.read_text(encoding="utf-8")
        orig = text

        # 1. Pagefind meta
        ptitle = part_titles.get(part_num, f"Part {part_num}")
        ctitle = (chapter_titles.get((part_num, chapter_num))
                   if chapter_num else None)
        text, pn = _fix_pagefind_meta(text, part_num, ptitle, chapter_num, ctitle)
        n_pagefind += pn

        # 2. Book-link inside header-nav
        depth = _depth_from_root(p)
        text, bn = _fix_book_link(text, depth)
        n_booklink += bn

        # 3. Unexpected subtitle on section pages
        if SECTION_RE.match(p.name):
            text, sn = _strip_unexpected_subtitle(text)
            n_subtitle += sn

        if text != orig:
            n_files_edited += 1
            if not dry_run:
                p.write_text(text, encoding="utf-8")

    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"=== {mode} ===")
    print(f"Pagefind meta updates:    {n_pagefind}")
    print(f"Book-link fixes:          {n_booklink}")
    print(f"Subtitle strips:          {n_subtitle}")
    print(f"Files edited:             {n_files_edited}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
