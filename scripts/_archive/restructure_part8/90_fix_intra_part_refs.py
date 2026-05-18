"""Phase 9: fix intra-part `../module-OLD/section-X.Y.html` refs that
Phase 5 missed because its regex required the full book-relative path.

Builds module + section pair maps from migration-map.json, then walks
every HTML file book-wide. For each href of the form:
  href="(?:\\.\\./)+module-OLD-slug/section-X.Y.html"
  href="(?:\\.\\./)+module-OLD-slug/index.html"

rewrites to the new module slug and section num. Also handles paths to
deleted modules (module-35-production-engineering, module-49-post-launch-monitoring)
by routing to the cross-part destination.

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

SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude", ".book-update", "vendor", "docs",
              "_scratch_part8_new_sections"}


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

    # Build old_module_slug -> new_module_slug
    old_to_new_mod: dict[str, str] = {}
    for src, dst in data["module_renames"].items():
        old_to_new_mod[src.split("/")[-1]] = dst.split("/")[-1]
    deleted_modules = {m.split("/")[-1] for m in data["modules_to_delete"]}

    # Build (old_X, old_Y) -> (new_X, new_Y) for section renumbers
    sec_pairs: dict[tuple[int, int], tuple[int, int]] = {}
    for entry in data["section_moves"]:
        src_sec = parse_section_num(entry["from"].split("/")[-1])
        dst_sec = parse_section_num(entry["to"].split("/")[-1])
        if src_sec and dst_sec and src_sec != dst_sec:
            sec_pairs[src_sec] = dst_sec
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
            if new_sec and new_sec[0] == new_ch:
                sec_pairs[(old_ch, new_sec[1])] = new_sec

    # Build cross-part destination map for deleted-module sections
    cross_part_route: dict[tuple[int, int], str] = {}
    for entry in data["section_moves"]:
        if "cross-part" in entry.get("action", ""):
            src_sec = parse_section_num(entry["from"].split("/")[-1])
            if src_sec:
                cross_part_route[src_sec] = entry["to"]

    files_edited = 0
    total = 0

    # Build a single regex for matching old module slugs (renamed OR deleted)
    all_old = list(old_to_new_mod.keys()) + list(deleted_modules)
    if not all_old:
        return 0
    pat = re.compile(
        r'href="((?:\.\./)+)('
        + "|".join(re.escape(s) for s in all_old)
        + r')/(section-(\d+)\.(\d+)\.html|index\.html)"'
    )

    def repl_for_file(p: Path):
        def repl(m: re.Match) -> str:
            nonlocal total
            prefix = m.group(1)
            old_mod = m.group(2)
            file_part = m.group(3)
            # Determine src part and old_mod part
            old_mod_part = None
            for src_full in data["module_renames"]:
                if src_full.endswith("/" + old_mod):
                    old_mod_part = src_full.split("/")[0]
                    break
            for src_full in data["modules_to_delete"]:
                if src_full.endswith("/" + old_mod):
                    old_mod_part = src_full.split("/")[0]
                    break
            if not old_mod_part:
                return m.group(0)
            src_file_part = p.relative_to(ROOT).parts[0] if p.is_relative_to(ROOT) else None
            if file_part == "index.html":
                if old_mod in deleted_modules:
                    return m.group(0)  # Don't auto-rewrite; deleted module index
                new_mod = old_to_new_mod[old_mod]
                # Adjust prefix only if part changed (which doesn't happen on rename of slug only)
                total += 1
                return f'href="{prefix}{new_mod}/index.html"'
            # It's section-X.Y.html
            sec_X = int(m.group(4))
            sec_Y = int(m.group(5))
            new_x, new_y = sec_pairs.get((sec_X, sec_Y), (sec_X, sec_Y))
            if old_mod in deleted_modules:
                full_dst = cross_part_route.get((sec_X, sec_Y))
                if not full_dst:
                    return m.group(0)
                # Determine new prefix: source file is at depth determined by ../ count.
                # The original prefix counts the depth from src file UP to book root.
                depth = prefix.count("../")
                # The destination path is full book-relative. Need to go up `depth-1` from
                # src file's container to reach book root, then append dst.
                # If src is at part-X/module-Y/file.html, depth=2 (../ ../). To reach book root from src dir = 2.
                # We assume same depth structure: src has /part/module/file -> ../ from module brings to part, ../../ from module brings to root.
                # The original href had `(../)*` going up from src dir. To get to a sibling part path: same `(../)*` + new dst.
                total += 1
                return f'href="{prefix}{full_dst}"'
            new_mod = old_to_new_mod[old_mod]
            total += 1
            return f'href="{prefix}{new_mod}/section-{new_x}.{new_y}.html"'
        return repl

    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        text = p.read_text(encoding="utf-8")
        orig = text
        text = pat.sub(repl_for_file(p), text)
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
