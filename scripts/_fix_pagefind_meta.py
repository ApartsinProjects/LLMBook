"""Audit B: Ensure every section HTML file has the two required pagefind-meta spans.

Required (one of each):
    <span class="pagefind-meta-injected" data-pagefind-meta="part:..." hidden=""></span>
    <span class="pagefind-meta-injected" data-pagefind-meta="chapter:..." hidden=""></span>

The "part:" value and "chapter:" value are derived from the section's parent
directories:
    section file:   <part-dir>/<module-dir>/section-X.Y.html
    chapter index:  <part-dir>/<module-dir>/index.html
    part index:     <part-dir>/index.html

We read the chapter title from the chapter's index.html (preferring its
existing data-pagefind-meta="chapter:..." value, else its <h1>), and the part
title likewise from the part's index.html (preferring data-pagefind-meta="part:...",
else its <h1>).

For appendices the part value is "Building Conversational AI with LLMs and Agents"
(matches the existing house style in appendices/*/section-*.html) and the chapter
value is "Appendix <Letter>: <Title>".

For capstone the part value is "Capstone Project" and the chapter value is "Capstone".

Idempotent: if both spans are already present, skip.

Usage:
    python scripts/_fix_pagefind_meta.py            # dry-run
    python scripts/_fix_pagefind_meta.py --apply    # write
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

ROOT = Path(r"E:/Projects/BookBlogsHome/LLMBook")

EXCLUDE_DIR_NAMES = {
    "node_modules", ".git", "KDP", "build", "temp_ebook", "temp_epub",
    "source_fix_backups", "pagefind", "templates", ".claude", ".book-update",
    "vendor", "scripts", "docs", "styles", ".html2pub_cache", "agents",
    "images", "_concept-figs", "downloads", ".github",
}


def is_excluded(name: str) -> bool:
    if name in EXCLUDE_DIR_NAMES:
        return True
    if name.startswith("temp_"):
        return True
    if "backups" in name:
        return True
    return False


def iter_section_files() -> list[Path]:
    out: list[Path] = []
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if not is_excluded(d)]
        for fn in fns:
            if fn.startswith("section-") and fn.endswith(".html"):
                out.append(Path(dp) / fn)
    return sorted(out)


def has_meta(text: str, key: str) -> bool:
    return bool(re.search(rf'data-pagefind-meta="{re.escape(key)}:', text))


def extract_meta(text: str, key: str) -> str | None:
    m = re.search(rf'data-pagefind-meta="{re.escape(key)}:([^"]+)"', text)
    return m.group(1) if m else None


def extract_h1(text: str) -> str | None:
    # Capture first <h1>...</h1> text content (strip inner tags).
    m = re.search(r"<h1\b[^>]*>(.*?)</h1>", text, re.DOTALL | re.IGNORECASE)
    if not m:
        return None
    return re.sub(r"<[^>]+>", "", m.group(1)).strip()


def part_chapter_for(section_path: Path) -> tuple[str | None, str | None]:
    """Determine the part: and chapter: meta values for the given section file."""
    chapter_dir = section_path.parent
    part_dir = chapter_dir.parent

    rel_part = part_dir.name
    rel_chap = chapter_dir.name

    # CAPSTONE
    if rel_part == "capstone" or rel_chap == "capstone":
        return ("Capstone Project", "Capstone")

    # APPENDICES: appendices/appendix-a-... or appendices/appendix-a-mathematical-foundations/section-a.6.html
    # The structure is appendices/<appendix-x-slug>/section-x.y.html
    # so chapter_dir.name starts with "appendix-" and part_dir.name == "appendices"
    if part_dir.name == "appendices":
        chap_idx = chapter_dir / "index.html"
        # Prefer composing "Appendix X: <Title>" because the chapter index's
        # pagefind-meta sometimes contains just "Appendix X". We use the h1 as
        # the title and the directory name for the letter.
        letter = None
        m = re.match(r"appendix-([a-z])-(.+)", chapter_dir.name)
        if m:
            letter = m.group(1).upper()
        chap_meta = None
        h1_title = None
        existing_meta = None
        if chap_idx.exists():
            ct = chap_idx.read_text(encoding="utf-8")
            h1_title = extract_h1(ct)
            existing_meta = extract_meta(ct, "chapter")
        if letter and h1_title and not h1_title.lower().startswith("appendix"):
            chap_meta = f"Appendix {letter}: {h1_title}"
        elif existing_meta:
            # If the index's meta already has "Appendix X: ...", use it. If it
            # is just "Appendix X", append the h1.
            if re.fullmatch(r"Appendix\s+[A-Z]", existing_meta.strip()) and h1_title:
                chap_meta = f"{existing_meta.strip()}: {h1_title}"
            else:
                chap_meta = existing_meta
        elif h1_title:
            chap_meta = h1_title
        if not chap_meta and letter and m:
            slug = m.group(2)
            title = slug.replace("-", " ").title()
            chap_meta = f"Appendix {letter}: {title}"
        # House-style: appendices use the book title as the "part" value.
        return ("Building Conversational AI with LLMs and Agents", chap_meta)

    # NORMAL PARTS: part-N-slug/module-MM-slug/section-X.Y.html
    chap_idx = chapter_dir / "index.html"
    part_idx = part_dir / "index.html"

    chap_meta = None
    if chap_idx.exists():
        ct = chap_idx.read_text(encoding="utf-8")
        chap_meta = extract_meta(ct, "chapter") or extract_h1(ct)

    part_meta = None
    if part_idx.exists():
        pt = part_idx.read_text(encoding="utf-8")
        part_meta = extract_meta(pt, "part") or extract_h1(pt)

    return (part_meta, chap_meta)


def inject_meta_spans(text: str, missing_part: str | None, missing_chapter: str | None) -> str:
    """Inject the missing meta spans just inside <main class="content">.

    The convention is to place them as the very first children of <main>:
        <main class="content"><span ...></span><span ...></span>
    """
    new_spans = []
    if missing_part:
        new_spans.append(
            f'<span class="pagefind-meta-injected" data-pagefind-meta="part:{missing_part}" hidden=""></span>'
        )
    if missing_chapter:
        new_spans.append(
            f'<span class="pagefind-meta-injected" data-pagefind-meta="chapter:{missing_chapter}" hidden=""></span>'
        )
    if not new_spans:
        return text
    injection = "".join(new_spans)

    # Inject after the opening <main ...> tag.
    pattern = re.compile(r"(<main\b[^>]*>)", re.IGNORECASE)
    def repl(m: re.Match) -> str:
        return m.group(1) + injection
    new_text, n = pattern.subn(repl, text, count=1)
    if n == 0:
        # Fallback: place before </body>.
        new_text = text.replace("</body>", injection + "</body>", 1)
    return new_text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Write changes (default: dry-run)")
    args = parser.parse_args()

    files = iter_section_files()
    total = 0
    part_added = 0
    chap_added = 0
    files_changed = 0
    unresolved: list[tuple[str, str]] = []  # (path, key)

    for f in files:
        total += 1
        text = f.read_text(encoding="utf-8")
        has_part = has_meta(text, "part")
        has_chap = has_meta(text, "chapter")
        if has_part and has_chap:
            continue
        part_value, chap_value = part_chapter_for(f)
        missing_part = None if has_part else part_value
        missing_chap = None if has_chap else chap_value
        if not has_part and not part_value:
            unresolved.append((f.relative_to(ROOT).as_posix(), "part"))
        if not has_chap and not chap_value:
            unresolved.append((f.relative_to(ROOT).as_posix(), "chapter"))
        if missing_part:
            part_added += 1
        if missing_chap:
            chap_added += 1
        if (missing_part or missing_chap):
            files_changed += 1
            if args.apply:
                new_text = inject_meta_spans(text, missing_part, missing_chap)
                f.write_text(new_text, encoding="utf-8")

    mode = "APPLIED" if args.apply else "DRY-RUN"
    print(f"[{mode}] Audit B: pagefind meta spans")
    print(f"  Sections scanned:        {total}")
    print(f"  Files changed:           {files_changed}")
    print(f"  Missing-part injected:   {part_added}")
    print(f"  Missing-chapter injected:{chap_added}")
    if unresolved:
        print(f"  Unresolved (no source title found): {len(unresolved)}")
        for path, key in unresolved[:20]:
            print(f"    {path}: missing {key}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
