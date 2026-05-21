"""Phase 8.5: targeted fix for Part 8 + Part 10 index.html hrefs.

The part-index pages use same-folder-relative hrefs like
  href="module-34-evaluation-observability/section-34.1.html"
which phase 5 missed because its regex required a `../` prefix.

This script handles bare module-slug paths.

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

    # Build a map of old-module-slug -> new-module-slug (last segment)
    old_to_new_mod: dict[str, str] = {}
    for src, dst in data["module_renames"].items():
        old_to_new_mod[src.split("/")[-1]] = dst.split("/")[-1]
    for m in data["modules_to_delete"]:
        old_to_new_mod[m.split("/")[-1]] = ""  # deleted

    # Build (old_chapter, old_secnum) -> (new_chapter, new_secnum) map
    sec_pairs: dict[tuple[int, int], tuple[int, int]] = {}
    for entry in data["section_moves"]:
        src_path = entry["from"]
        dst_path = entry["to"]
        src_sec = parse_section_num(src_path.split("/")[-1])
        dst_sec = parse_section_num(dst_path.split("/")[-1])
        if src_sec and dst_sec and src_sec != dst_sec:
            sec_pairs[src_sec] = dst_sec

    # Map for module_rename + section file rename (chapter num change)
    for src_mod, dst_mod in data["module_renames"].items():
        m_old = re.search(r"module-(\d+)-", src_mod)
        m_new = re.search(r"module-(\d+)-", dst_mod)
        if not (m_old and m_new):
            continue
        old_ch = int(m_old.group(1))
        new_ch = int(m_new.group(1))
        if old_ch == new_ch:
            continue
        dst_p = ROOT / dst_mod
        if not dst_p.exists():
            continue
        for sec_file in dst_p.glob("section-*.html"):
            new_sec = parse_section_num(sec_file.name)
            if not new_sec or new_sec[0] != new_ch:
                continue
            sec_pairs[(old_ch, new_sec[1])] = new_sec

    # For each section_move entry, also build a "where did section X.Y go to which part?" map
    # for the cross-part deletions (so module-49 section refs can route correctly).
    cross_part_route: dict[tuple[int, int], str] = {}  # (X, Y) -> new full path
    for entry in data["section_moves"]:
        if "cross-part" in entry.get("action", ""):
            src_sec = parse_section_num(entry["from"].split("/")[-1])
            if src_sec:
                cross_part_route[src_sec] = entry["to"]

    print(f"Module rename map: {len(old_to_new_mod)}")
    print(f"Section pair map:  {len(sec_pairs)}")
    print(f"Cross-part routes: {len(cross_part_route)}")
    print()

    files_edited = 0
    total = 0
    targets = [
        ROOT / "part-8-evaluation-production/index.html",
        ROOT / "part-9-safety-security-ethics/index.html",
        ROOT / "part-10-idea-to-product/index.html",
    ]
    for p in targets:
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        orig = text

        def repl(m: re.Match) -> str:
            nonlocal total
            mod_slug = m.group(1)
            sec_X = int(m.group(2))
            sec_Y = int(m.group(3))
            new_mod = old_to_new_mod.get(mod_slug)
            if new_mod is None:
                # Module not in rename map; keep
                return m.group(0)
            # Compute new section nums
            new_x, new_y = sec_pairs.get((sec_X, sec_Y), (sec_X, sec_Y))
            if new_mod == "":  # deleted module — route via cross_part_route
                full_dst = cross_part_route.get((sec_X, sec_Y))
                if full_dst:
                    # The destination is in a DIFFERENT part. We need ../-prefix.
                    # For a file at part-10-idea-to-product/index.html linking to
                    # part-8-evaluation-production/module-37-.../section-37.4.html,
                    # the relative path is ../part-8-evaluation-production/module-37-.../section-37.4.html
                    total += 1
                    src_part = p.parent.name  # part-10-...
                    dst_part = full_dst.split("/")[0]  # part-8-...
                    if src_part == dst_part:
                        # Same part — same-folder
                        rest = "/".join(full_dst.split("/")[1:])
                        return f'href="{rest}"'
                    else:
                        return f'href="../{full_dst}"'
                return m.group(0)
            total += 1
            return f'href="{new_mod}/section-{new_x}.{new_y}.html"'

        text = re.sub(
            r'href="(module-[\w\-]+)/section-(\d+)\.(\d+)\.html"',
            repl, text,
        )

        # Also handle bare module index.html refs
        def repl_idx(m: re.Match) -> str:
            nonlocal total
            mod_slug = m.group(1)
            new_mod = old_to_new_mod.get(mod_slug)
            if new_mod is None:
                return m.group(0)
            if new_mod == "":
                return m.group(0)  # deleted - leave for manual
            total += 1
            return f'href="{new_mod}/index.html"'

        text = re.sub(
            r'href="(module-[\w\-]+)/index\.html"',
            repl_idx, text,
        )

        if text != orig:
            files_edited += 1
            if not dry_run:
                p.write_text(text, encoding="utf-8")

    print(f"=== Summary ===")
    print(f"Files edited:    {files_edited}")
    print(f"Hrefs rewritten: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
