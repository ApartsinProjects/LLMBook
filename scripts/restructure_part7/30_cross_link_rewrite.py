"""Phase 3: book-wide cross-link rewrite for Part 9 + Part 10 cascade.

Walks every HTML file. For each href matching a moved/renamed path,
rewrite to the new home.
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

SKIP = {"node_modules", ".git", "KDP", "build", "temp_ebook",
        "temp_epub", "source_fix_backups", "pagefind", "templates",
        ".claude", ".book-update", "vendor", "docs"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply
    data = json.loads(MAP.read_text(encoding="utf-8"))

    # Build path-to-path map
    mapping = {}

    # Module renames (with chapter num changes)
    for src_mod, dst_mod in data["module_renames"].items():
        m_old = re.search(r"module-(\d+)-", src_mod)
        m_new = re.search(r"module-(\d+)-", dst_mod)
        if not (m_old and m_new):
            mapping[src_mod] = dst_mod
            continue
        old_n = int(m_old.group(1))
        new_n = int(m_new.group(1))
        mapping[f"{src_mod}/index.html"] = f"{dst_mod}/index.html"
        dst_p = ROOT / dst_mod
        if dst_p.exists():
            for sec in dst_p.glob("section-*.html"):
                sm = re.match(r"section-(\d+)\.(\d+)\.html", sec.name)
                if sm and int(sm.group(1)) == new_n:
                    new_y = int(sm.group(2))
                    mapping[f"{src_mod}/section-{old_n}.{new_y}.html"] = f"{dst_mod}/section-{new_n}.{new_y}.html"

    # Part 7 has no wholesale_section_moves in this phase (deferred)

    files_edited = 0
    total = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding="utf-8")
        orig = text
        for old_path, new_path in mapping.items():
            pat = re.compile(rf'(href="((?:\.\./)*){re.escape(old_path)}")')
            text, n = pat.subn(lambda m: f'href="{m.group(2)}{new_path}"', text)
            total += n
        if text != orig:
            files_edited += 1
            if not dry_run:
                p.write_text(text, encoding="utf-8")
    print(f"Files edited: {files_edited}, hrefs rewritten: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
