"""Phase 2: rewrite chapter prefixes inside renamed/moved Part 9 + Part 10 files.

After phase 1, Part 10 modules 42-52 got renumbered to 51-61. Inside
those files, breadcrumbs, page-current, h2/h3 prefixes, anchor IDs, and
caption labels still hold OLD chapter numbers. Two-pass placeholder
rewrite.

Also handles Part 9 module-39 (renamed -safety-ethics-regulation ->
-adversarial-security-red-team).

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


def build_renumber_map(data):
    out = {}
    for src, dst in data["module_renames"].items():
        old_m = re.search(r"module-(\d+)-", src)
        new_m = re.search(r"module-(\d+)-", dst)
        if old_m and new_m:
            old_n = int(old_m.group(1))
            new_n = int(new_m.group(1))
            if old_n != new_n:
                out[old_n] = new_n
    return out


def rewrite_file(path, full_renumber, dry_run):
    text = path.read_text(encoding="utf-8")
    orig = text
    pairs_to_apply = sorted(full_renumber.items(), key=lambda x: -x[0])
    # Two-pass rewrite (placeholder -> target)
    for old_n in [old for old, _ in pairs_to_apply]:
        text = re.sub(rf"\bChapter {old_n}\b", f"__CH_{old_n}__", text)
        text = re.sub(rf"\bSection {old_n}\.", f"__S_{old_n}_DOT__", text)
        text = re.sub(rf"\bsection-{old_n}\.", f"__SF_{old_n}_DOT__", text)
        text = re.sub(rf"\bsection-{old_n}-", f"__SF_{old_n}_DASH__", text)
        text = re.sub(rf"\bmodule-{old_n}-", f"__M_{old_n}_DASH__", text)
        text = re.sub(rf"\bCode Fragment {old_n}\.", f"__CF_{old_n}_DOT__", text)
        text = re.sub(rf"\bFigure {old_n}\.", f"__FIG_{old_n}_DOT__", text)
        text = re.sub(rf"\bTable {old_n}\.", f"__TBL_{old_n}_DOT__", text)
        text = re.sub(rf"\bListing {old_n}\.", f"__LST_{old_n}_DOT__", text)
        text = re.sub(rf"(<h[234][^>]*>){old_n}\.", rf"\g<1>__H_{old_n}_DOT__", text)
        text = re.sub(rf"(<h[234][^>]*>){old_n}\s", rf"\g<1>__H_{old_n}_SPACE__", text)
    for old_n, new_n in pairs_to_apply:
        text = text.replace(f"__CH_{old_n}__", f"Chapter {new_n}")
        text = text.replace(f"__S_{old_n}_DOT__", f"Section {new_n}.")
        text = text.replace(f"__SF_{old_n}_DOT__", f"section-{new_n}.")
        text = text.replace(f"__SF_{old_n}_DASH__", f"section-{new_n}-")
        text = text.replace(f"__M_{old_n}_DASH__", f"module-{new_n}-")
        text = text.replace(f"__CF_{old_n}_DOT__", f"Code Fragment {new_n}.")
        text = text.replace(f"__FIG_{old_n}_DOT__", f"Figure {new_n}.")
        text = text.replace(f"__TBL_{old_n}_DOT__", f"Table {new_n}.")
        text = text.replace(f"__LST_{old_n}_DOT__", f"Listing {new_n}.")
        text = text.replace(f"__H_{old_n}_DOT__", f"{new_n}.")
        text = text.replace(f"__H_{old_n}_SPACE__", f"{new_n} ")
    if text != orig:
        if not dry_run:
            path.write_text(text, encoding="utf-8")
        return 1
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply
    data = json.loads(MAP.read_text(encoding="utf-8"))
    renumber = build_renumber_map(data)
    print(f"Renumber map: {dict(sorted(renumber.items()))}")
    print()

    SKIP = {"node_modules", ".git", "KDP", "build", "temp_ebook",
            "temp_epub", "source_fix_backups", "pagefind", "templates",
            ".claude", ".book-update", "vendor", "docs"}
    inv = {v: k for k, v in renumber.items()}
    edited = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP:
            continue
        rel = p.relative_to(ROOT).as_posix()
        in_renamed = any(rel.startswith(dst + "/") for dst in data["module_renames"].values())
        if not in_renamed:
            continue
        m = re.search(r"module-(\d+)-", rel)
        if not m: continue
        cur_ch = int(m.group(1))
        old_ch = inv.get(cur_ch)
        if old_ch is None:
            continue
        n = rewrite_file(p, renumber, dry_run)
        if n: edited += 1

    print(f"Files edited: {edited}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
