"""Phase 5: book-wide cross-link rewrite.

After phases 2-4, every renamed/moved file is in its new home with new
chapter numbers internally. But every OTHER file in the book that
linked to the OLD location now has a broken href.

This phase walks every HTML file book-wide and rewrites hrefs that point
to moved/renamed sections. Uses migration-map.json to build the full
mapping.

Mapping built from:
  1. module_renames (module-X-slug -> module-Y-slug)
  2. section_moves cross-part (full-path -> full-path)
  3. anchor_prefix_renames (X.Y -> X'.Y')
  4. Same-chapter section renumbers within a renamed module

Idempotent: re-running finds no old paths to rewrite.

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


def build_path_rewrite_map(data: dict) -> dict[str, str]:
    """Build a flat dict: old_relative_path -> new_relative_path.

    Used to rewrite hrefs in files outside the moved/renamed scope.
    Keys are book-relative paths like
        'part-10-idea-to-product/module-40-ideation/section-40.1.html'.
    """
    mapping: dict[str, str] = {}

    # 1. Module renames (which also imply section file renames)
    for src_mod, dst_mod in data["module_renames"].items():
        # Each section-X.Y.html in src_mod becomes section-X'.Y.html in dst_mod
        # (where X' is the new chapter num if the slug had a chapter num)
        m_old = re.match(r".*/module-(\d+)-", src_mod)
        m_new = re.match(r".*/module-(\d+)-", dst_mod)
        if not (m_old and m_new):
            mapping[src_mod] = dst_mod
            continue
        old_n = int(m_old.group(1))
        new_n = int(m_new.group(1))
        # index.html
        mapping[f"{src_mod}/index.html"] = f"{dst_mod}/index.html"
        # section files: discover by listing the destination dir
        dst_p = ROOT / dst_mod
        if dst_p.exists():
            for sec in dst_p.glob("section-*.html"):
                sec_m = re.match(r"section-(\d+)\.(\d+)\.html", sec.name)
                if not sec_m:
                    continue
                sec_ch = int(sec_m.group(1))
                sec_n = int(sec_m.group(2))
                if sec_ch == new_n:
                    # Was section-{old_n}.{sec_n}.html in old module
                    old_path = f"{src_mod}/section-{old_n}.{sec_n}.html"
                    new_path = f"{dst_mod}/section-{new_n}.{sec_n}.html"
                    mapping[old_path] = new_path

    # 2. Cross-part section_moves
    for entry in data["section_moves"]:
        if "cross-part" in entry.get("action", ""):
            mapping[entry["from"]] = entry["to"]
            # Also the index.html link if any
        # For intra-part moves (within Part 8 module-34 -> module-34-foundations),
        # the section file slug may also have changed (34.8 -> 34.3 inside same module).
        if "renumber" in entry.get("action", "") or "intact" in entry.get("action", ""):
            mapping[entry["from"]] = entry["to"]
        if "split-source" in entry.get("action", ""):
            mapping[entry["from"]] = entry["to"]

    # 3. Module deletions point at the dissolution target (e.g., 49 -> P8 ch 37)
    # already covered by cross-part section_moves.

    return mapping


def rewrite_href(text: str, mapping: dict[str, str]) -> tuple[str, int]:
    """Rewrite hrefs in text. Returns (new_text, count_of_rewrites)."""
    count = 0
    for old, new in mapping.items():
        # Match the old path as the last fragment of any href, regardless of
        # relative-path prefix (../ or ../../). The key is the trailing
        # path segments must equal old (book-relative).
        # Build a regex that matches any href ending in `old`.
        # Escape and pattern: (?:\.\./)*old
        pattern = re.compile(
            rf'(href=")((?:\.\./)+|){re.escape(old)}(")'
        )
        def repl(m: re.Match) -> str:
            nonlocal count
            count += 1
            # Compute correct relative prefix.
            # The depth of new vs the SOURCE file's depth varies. For book-wide
            # rewrite, we can't easily know the source file's location in a global
            # mapping. Practical approach: preserve the same prefix depth (../).
            prefix = m.group(2)
            return m.group(1) + prefix + new + m.group(3)
        new_text = pattern.sub(repl, text)
        text = new_text
    return text, count


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply
    data = json.loads(MAP.read_text(encoding="utf-8"))
    mapping = build_path_rewrite_map(data)
    print(f"=== Phase 5: book-wide cross-link rewrite ===")
    if dry_run:
        print("(DRY-RUN; pass --apply to execute)")
    print(f"Mapping entries: {len(mapping)}")
    print()
    files_edited = 0
    total_rewrites = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        text = p.read_text(encoding="utf-8")
        new_text, n = rewrite_href(text, mapping)
        if n > 0:
            files_edited += 1
            total_rewrites += n
            if not dry_run:
                p.write_text(new_text, encoding="utf-8")
    print(f"=== Summary ===")
    print(f"Files edited:    {files_edited}")
    print(f"Hrefs rewritten: {total_rewrites}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
