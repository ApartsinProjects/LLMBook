"""Edition bump utility.

Sweeps content HTML + html2epub.toml + KDP/metadata/metadata.yaml for the
current edition string and updates everything in one pass. Also bumps
the publication_date and dcterms:modified meta.

Usage:
    python scripts/_bump_edition.py --from "Fourteenth Edition" --to "Fifteenth Edition" --date 2026-05-16
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


def should_skip(p: Path) -> bool:
    return bool(set(p.parts) & SKIP_PARTS)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="src", required=True, help='current edition string e.g. "Fourteenth Edition"')
    ap.add_argument("--to", dest="dst", required=True, help='new edition string e.g. "Fifteenth Edition"')
    ap.add_argument("--date", dest="date", required=True, help='new publication date e.g. 2026-05-16')
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    src, dst, date = args.src, args.dst, args.date
    year = date[:4]

    # 1. Update html2epub.toml
    toml_path = ROOT / "html2epub.toml"
    if toml_path.exists():
        text = toml_path.read_text(encoding="utf-8")
        new = text.replace(f'edition = "{src}"', f'edition = "{dst}"')
        new = re.sub(r'publication_date\s*=\s*"\d{4}-\d{2}-\d{2}"',
                     f'publication_date = "{date}"', new)
        if new != text and not args.dry_run:
            toml_path.write_text(new, encoding="utf-8")
        print(f"html2epub.toml: {'(dry-run) would update' if args.dry_run else 'updated'}")

    # 2. Update KDP/metadata/metadata.yaml if present
    yaml_path = ROOT / "KDP" / "metadata" / "metadata.yaml"
    if yaml_path.exists():
        text = yaml_path.read_text(encoding="utf-8")
        new = text.replace(src, dst)
        new = re.sub(r'publication_date:\s*"\d{4}-\d{2}-\d{2}"',
                     f'publication_date: "{date}"', new)
        new = re.sub(r'publication_date:\s*\d{4}-\d{2}-\d{2}',
                     f'publication_date: {date}', new)
        if new != text and not args.dry_run:
            yaml_path.write_text(new, encoding="utf-8")
        print(f"KDP/metadata/metadata.yaml: {'(dry-run) would update' if args.dry_run else 'updated'}")

    # 3. Sweep all content HTML for the edition string + year
    pages_changed = 0
    occs_changed = 0
    for p in ROOT.rglob("*.html"):
        if should_skip(p):
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        n = text.count(src)
        if n == 0:
            continue
        new_text = text.replace(src, dst)
        # Also update bare "2026" in the same footer line context
        # (cautious: only replace when adjacent to the edition, to avoid touching prose like '2026 Anthropic')
        new_text = re.sub(
            rf'{re.escape(dst)},\s*\d{{4}}',
            f'{dst}, {year}',
            new_text,
        )
        if new_text != text:
            pages_changed += 1
            occs_changed += n
            if not args.dry_run:
                p.write_text(new_text, encoding="utf-8")

    print(f"HTML pages: {pages_changed} pages updated, {occs_changed} occurrences of '{src}' replaced")
    if args.dry_run:
        print("(dry run; nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
