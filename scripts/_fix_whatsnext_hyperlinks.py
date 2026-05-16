"""Hyperlink every chapter/section/part/appendix reference inside
`<div class="whats-next">` callouts and other "looking ahead" callouts.

Patterns to link:
  - "Chapter N" / "chapter N"
  - "Section X.Y" / "section X.Y"
  - "Part X" (Roman numeral) / "part X"
  - "Appendix X" (single letter A-V) / "appendix X"
  - "Appendix X.N" / "appendix X.N"

Skip references that are already inside an <a> tag.

Idempotent.
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

ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7,
         "VIII": 8, "IX": 9, "X": 10, "XI": 11, "XII": 12}


def build_indexes():
    """Return (chapter_to_path, part_to_path, appendix_to_path) mappings."""
    chapter_to_path: dict[int, Path] = {}
    part_to_path: dict[int, Path] = {}
    appendix_to_path: dict[str, Path] = {}
    for d in ROOT.glob("part-*-*"):
        m = re.match(r"part-(\d+)-", d.name)
        if m:
            part_to_path[int(m.group(1))] = d / "index.html"
        for cd in d.glob("module-*-*"):
            cm = re.match(r"module-(\d+)-", cd.name)
            if cm:
                chapter_to_path[int(cm.group(1))] = cd / "index.html"
    for d in (ROOT / "appendices").glob("appendix-*-*"):
        m = re.match(r"appendix-([a-z])-", d.name)
        if m:
            appendix_to_path[m.group(1).upper()] = d / "index.html"
    return chapter_to_path, part_to_path, appendix_to_path


def relpath(target: Path, source: Path) -> str:
    """POSIX-style relative path from source file to target file."""
    import os
    rel = os.path.relpath(target, source.parent)
    return rel.replace("\\", "/")


WHATSNEXT_RE = re.compile(
    r'(<(?:div|section)[^>]*class="[^"]*(?:whats-next|looking-ahead|looking-back)[^"]*"[^>]*>)(.*?)(</(?:div|section)>)',
    re.S,
)


def link_refs_in_block(block: str, source: Path,
                        chapters: dict, parts: dict, appendices: dict) -> str:
    """Add hyperlinks to chapter/section/part/appendix refs inside the block,
    avoiding refs already inside <a> tags."""
    # Walk text, track when we're inside an <a>
    out = []
    i = 0
    a_depth = 0
    n = len(block)
    while i < n:
        # Detect <a> opening
        if block.startswith("<a ", i) or block.startswith("<a>", i):
            close = block.find(">", i)
            if close == -1:
                out.append(block[i:])
                break
            out.append(block[i:close + 1])
            i = close + 1
            a_depth += 1
            continue
        # Detect </a>
        if block.startswith("</a>", i):
            out.append("</a>")
            i += 4
            a_depth = max(0, a_depth - 1)
            continue
        if a_depth > 0:
            out.append(block[i])
            i += 1
            continue
        # Try to match reference patterns at position i
        # Section X.Y first (more specific)
        m = re.match(r"(Section)\s+(\d+\.\d+)", block[i:], re.I)
        if m:
            sec_num = m.group(2)
            chap_num = int(sec_num.split(".")[0])
            chap_dir = chapters.get(chap_num)
            if chap_dir is not None:
                target = chap_dir.parent / f"section-{sec_num}.html"
                if target.exists():
                    href = relpath(target, source)
                    out.append(f'<a href="{href}">{m.group(0)}</a>')
                    i += len(m.group(0))
                    continue
        # Chapter N
        m = re.match(r"(Chapter)\s+(\d+)", block[i:], re.I)
        if m:
            chap_num = int(m.group(2))
            chap_path = chapters.get(chap_num)
            if chap_path is not None and chap_path.exists():
                href = relpath(chap_path, source)
                out.append(f'<a href="{href}">{m.group(0)}</a>')
                i += len(m.group(0))
                continue
        # Part X (Roman)
        m = re.match(r"(Part)\s+([IVXLCDM]+)\b", block[i:], re.I)
        if m:
            roman = m.group(2).upper()
            part_num = ROMAN.get(roman)
            if part_num is not None:
                part_path = parts.get(part_num)
                if part_path is not None and part_path.exists():
                    href = relpath(part_path, source)
                    out.append(f'<a href="{href}">{m.group(0)}</a>')
                    i += len(m.group(0))
                    continue
        # Appendix X.N (section)
        m = re.match(r"(Appendix)\s+([A-Z])\.(\d+(?:\.\d+)?)", block[i:], re.I)
        if m:
            letter = m.group(2).upper()
            sec_num = m.group(3)
            app_dir = appendices.get(letter)
            if app_dir is not None:
                target = app_dir.parent / f"section-{letter.lower()}.{sec_num}.html"
                if target.exists():
                    href = relpath(target, source)
                    out.append(f'<a href="{href}">{m.group(0)}</a>')
                    i += len(m.group(0))
                    continue
        # Appendix X (landing)
        m = re.match(r"(Appendix)\s+([A-Z])\b", block[i:], re.I)
        if m:
            letter = m.group(2).upper()
            app_path = appendices.get(letter)
            if app_path is not None and app_path.exists():
                href = relpath(app_path, source)
                out.append(f'<a href="{href}">{m.group(0)}</a>')
                i += len(m.group(0))
                continue
        # No match — copy 1 char
        out.append(block[i])
        i += 1
    return "".join(out)


def process_file(p: Path, dry_run: bool, idx) -> tuple[int, str]:
    text = p.read_text(encoding="utf-8")
    chapters, parts, appendices = idx
    total_added = 0

    def repl(m: re.Match) -> str:
        nonlocal total_added
        open_tag, body, close_tag = m.group(1), m.group(2), m.group(3)
        before = body.count("<a ")
        new_body = link_refs_in_block(body, p, chapters, parts, appendices)
        after = new_body.count("<a ")
        total_added += (after - before)
        return open_tag + new_body + close_tag

    new = WHATSNEXT_RE.sub(repl, text)
    if new == text:
        return 0, ""
    if not dry_run:
        p.write_text(new, encoding="utf-8")
    return total_added, ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    idx = build_indexes()
    total = 0
    files = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        n, _ = process_file(p, args.dry_run, idx)
        if n:
            files += 1
            total += n
            print(f"  {p.relative_to(ROOT)}: +{n} hyperlinks")
    print(f"\nTOTAL: {total} hyperlinks added across {files} What's Next/Looking-Ahead blocks")
    if args.dry_run:
        print("(dry run; nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
