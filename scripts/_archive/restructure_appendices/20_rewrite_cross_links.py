"""Phase 20: rewrite book-wide cross-links to moved appendix sections.

Reads section_moves from migration-map.json and rewrites every href to
an old appendix path. Handles 4 prefix variants:
  href="appendices/appendix-X-.../section-X.Y.html"
  href="../appendices/appendix-X-.../section-X.Y.html"
  href="../../appendices/appendix-X-.../section-X.Y.html"
  href="../../../appendices/..." (deeper - rare)

For each found ref, rewrites the path to the new home and adjusts the
relative-prefix depth based on the source file's location.

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
              ".claude", ".book-update", "vendor", "docs"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply
    data = json.loads(MAP.read_text(encoding="utf-8"))

    # Build path-to-path map. Each old appendix path -> new path.
    path_map: dict[str, str] = {}
    for entry in data["section_moves"]:
        path_map[entry["from"]] = entry["to"]
    # Also add appendix index pages -> redirect stubs (which still exist at old path)
    # so refs to appendix-X/index.html keep working via the stub.

    files_edited = 0
    total_rewrites = 0

    # Regex matches href with optional ../ prefix to old path
    # Need to handle 3 depth levels of source file: deeper paths use more ../
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        text = p.read_text(encoding="utf-8")
        orig = text

        for old_path, new_path in path_map.items():
            # Match `href="(prefix)?old_path"` where prefix is 0..N "../"
            pattern = re.compile(
                rf'(href="((?:\.\./)*){re.escape(old_path)}")'
            )
            def repl(m: re.Match) -> str:
                nonlocal total_rewrites
                old_prefix = m.group(2)  # "../" * N
                # The number of "../" in old_prefix tells us the source file's depth
                # from the book root. Same depth applies for new path.
                total_rewrites += 1
                return f'href="{old_prefix}{new_path}"'
            text = pattern.sub(repl, text)

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
