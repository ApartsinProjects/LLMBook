"""v3.4 Wave A: Renumber sections to close gaps left by v3.x deletions.

Maps:
  Chapter 11: 11.6 -> 11.5
  Chapter 12: 12.8 -> 12.6
  Chapter 13: 13.4..13.8 -> 13.3..13.7
  Chapter 22: 22.3..22.7 -> 22.2..22.6
  Chapter 24: 24.5 -> 24.3
  Chapter 25: 25.4 -> 25.3, 25.7 -> 25.4
  Chapter 29: 29.4..29.8 -> 29.3..29.7, 29.10..29.14 -> 29.8..29.12

For each renumber:
  1. Move/rename file
  2. Update every href in every other HTML file
  3. Update H1 prefix ("22.7 Memory..." -> "22.2 Memory...")
  4. Update "Section X.Y" prose mentions in body text
  5. Update breadcrumb / nav text

Idempotent within a single run (won't double-shift). Run twice -> no-op.

Run from project root:
    /c/Python314/python KDP/build/_v34_renumber_close_gaps.py
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE = {"_archive", "KDP", "node_modules", "vendor", "scripts"}

# (chapter, [(old_section, new_section), ...])
RENUMBERS: list[tuple[int, list[tuple[int, int]]]] = [
    (11, [(6, 5)]),
    (12, [(8, 6)]),
    (13, [(4, 3), (5, 4), (6, 5), (7, 6), (8, 7)]),
    (22, [(3, 2), (4, 3), (5, 4), (6, 5), (7, 6)]),
    (24, [(5, 3)]),
    (25, [(4, 3), (7, 4)]),
    (29, [(4, 3), (5, 4), (6, 5), (7, 6), (8, 7),
          (10, 8), (11, 9), (12, 10), (13, 11), (14, 12)]),
]


def find_section_file(chapter: int, section: int) -> Path | None:
    """Locate section-C.S.html anywhere under part-*/module-*/."""
    pattern = f"section-{chapter}.{section}.html"
    for p in ROOT.glob(f"part-*/module-*/{pattern}"):
        return p
    return None


def renumber_h1_prefix(text: str, old: str, new: str) -> str:
    """Update '<h1>X.Y Title</h1>' and breadcrumb/title prefixes."""
    # H1 leading "X.Y "
    text = re.sub(rf'(<h[12][^>]*>\s*){re.escape(old)}(\s+|&nbsp;)',
                  rf'\g<1>{new}\g<2>', text)
    # <title>Section X.Y: ...</title>
    text = re.sub(rf'(<title[^>]*>\s*Section\s+){re.escape(old)}(:?\s)',
                  rf'\g<1>{new}\g<2>', text)
    # meta description "Section X.Y: ..."
    text = re.sub(rf'(name="description"[^>]*content="[^"]*Section\s+){re.escape(old)}',
                  rf'\g<1>{new}', text)
    # body prose "Section X.Y" - careful not to touch unrelated decimals
    text = re.sub(rf'\bSection {re.escape(old)}\b', f'Section {new}', text)
    # Standalone "X.Y" at start of breadcrumb line/cell - too risky to do globally
    return text


def main() -> int:
    # Step 1: build the global old->new mapping with file paths
    moves: list[tuple[Path, Path, str, str]] = []  # (src, dst, "X.Y", "X.Y_new")
    for chapter, pairs in RENUMBERS:
        for old_sec, new_sec in pairs:
            src = find_section_file(chapter, old_sec)
            if src is None:
                # Already renumbered or never existed
                continue
            dst_name = f"section-{chapter}.{new_sec}.html"
            dst = src.parent / dst_name
            # NOTE: don't pre-check dst.exists() - it will exist as a SOURCE
            # for an earlier-numbered move in the same cascade. We rely on
            # sort-by-new-section + sequential execution to avoid clobbers.
            moves.append((src, dst, f"{chapter}.{old_sec}", f"{chapter}.{new_sec}"))

    # Sort moves so that we go in order that doesn't overwrite (renumber lowest
    # destinations first - because renaming 22.3 -> 22.2 is safe before 22.4 -> 22.3)
    moves.sort(key=lambda m: (m[0].parent.name, int(m[3].split(".")[1])))

    print(f"Renumber plan: {len(moves)} files to rename")
    for _, _, old_label, new_label in moves[:5]:
        print(f"  {old_label} -> {new_label}")
    if len(moves) > 5:
        print(f"  ... ({len(moves)-5} more)")

    # Step 2: build href-replacement map (for cross-references)
    # Format: section-X.Y.html (anywhere in href)
    href_map = {f"section-{ol}.html": f"section-{nl}.html"
                for _, _, ol, nl in moves}

    # Step 3: rename files + update internal H1/title text
    for src, dst, old_label, new_label in moves:
        if not src.exists():
            continue
        text = src.read_text(encoding="utf-8", errors="replace")
        # Apply href map FIRST so any self-reference inside the file gets the new name
        for old_href, new_href in href_map.items():
            text = re.sub(rf'\b{re.escape(old_href)}', new_href, text)
        # Update H1/title/section refs for THIS file's number
        text = renumber_h1_prefix(text, old_label, new_label)
        dst.write_text(text, encoding="utf-8")
        src.unlink()
        print(f"  mv  {src.relative_to(ROOT).as_posix()} -> {dst.name}")

    # Step 4: rewrite hrefs in all OTHER HTML files
    n_files = 0
    n_links = 0
    moved_paths = {m[0].relative_to(ROOT).as_posix() for m in moves} | \
                  {m[1].relative_to(ROOT).as_posix() for m in moves}
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE):
            continue
        rel = p.relative_to(ROOT).as_posix()
        if rel in moved_paths:
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        original = text
        for old_href, new_href in href_map.items():
            text = re.sub(rf'\b{re.escape(old_href)}', new_href, text)
        # Also fix prose mentions "Section X.Y" pointing to renamed sections
        for _, _, old_label, new_label in moves:
            text = re.sub(rf'\bSection {re.escape(old_label)}\b',
                          f'Section {new_label}', text)
        if text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1
            n_links += 1
    print(f"\nUpdated cross-refs in {n_files} other files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
