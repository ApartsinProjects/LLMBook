"""Phase 5.5: rewrite same-folder section-X.Y.html refs inside moved files.

Scoped fix: only rewrite hrefs inside files that were moved by cross-part
section_moves OR that are inside newly-created modules. For these files,
bare same-folder refs point at OLD sibling names that no longer exist.

For files that stayed in their original location (only their PARENT module
got renamed), the bare same-folder refs are STILL VALID — those siblings
also got renamed in lockstep by phase 2. Don't rewrite those.

The earlier "naive" phase 5.5 broke this by rewriting bare refs in EVERY
file. Skipping files that haven't moved keeps the right links intact.

DRY-RUN by default.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MAP = HERE / "migration-map.json"


def parse_section_num(filename: str) -> tuple[int, int] | None:
    m = re.match(r"section-(\d+)\.(\d+)\.html", filename)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply
    data = json.loads(MAP.read_text(encoding="utf-8"))

    # Set of files (destinations) that received a cross-part move
    cross_part_destinations: set[str] = set()
    for entry in data["section_moves"]:
        if "cross-part" in entry.get("action", ""):
            cross_part_destinations.add(entry["to"])

    # Also include the 7 injected scratch sections (they reference siblings
    # that may not yet exist in their new module, but those siblings will
    # arrive in future phases or are intentional unresolved refs).
    for entry in data["sections_from_scratch"]:
        cross_part_destinations.add(entry["to"])

    # Build (old_chapter, old_secnum) -> (new_chapter, new_secnum) only for
    # cross-part moves AND specific Part 8 within-part moves (34.X intact
    # vs 34.8 -> 34.3 renumbers within the same module).
    sec_pairs: dict[tuple[int, int], tuple[int, int]] = {}
    for entry in data["section_moves"]:
        src_path = entry["from"]
        dst_path = entry["to"]
        src_sec = parse_section_num(src_path.split("/")[-1])
        dst_sec = parse_section_num(dst_path.split("/")[-1])
        if src_sec and dst_sec and src_sec != dst_sec:
            sec_pairs[src_sec] = dst_sec

    print(f"Files in scope: {len(cross_part_destinations)}")
    print(f"Section pair map: {len(sec_pairs)} entries")
    print()

    files_edited = 0
    total_rewrites = 0
    for rel in sorted(cross_part_destinations):
        p = ROOT / rel
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        orig = text
        # Bare same-folder: href="section-X.Y.html"
        def repl_bare(m: re.Match) -> str:
            nonlocal total_rewrites
            X = int(m.group(1))
            Y = int(m.group(2))
            if (X, Y) in sec_pairs:
                nX, nY = sec_pairs[(X, Y)]
                total_rewrites += 1
                return f'href="section-{nX}.{nY}.html"'
            return m.group(0)
        text = re.sub(r'href="section-(\d+)\.(\d+)\.html"', repl_bare, text)
        if text != orig:
            files_edited += 1
            if not dry_run:
                p.write_text(text, encoding="utf-8")

    print(f"=== Summary ===")
    print(f"Files edited:    {files_edited}")
    print(f"Hrefs rewritten: {total_rewrites}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
