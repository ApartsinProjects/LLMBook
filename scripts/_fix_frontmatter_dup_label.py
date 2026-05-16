"""Front-matter pages had part-label="Front Matter" AND chapter-label="Front
Matter" — pure duplicate breadcrumb. Previously masked by a global CSS rule
`.part-label ~ .chapter-label { display: none }`, which broke every other
page once part+chapter were distinct text.

This script removes the redundant chapter-label from front-matter pages where
its text matches the part-label text. Idempotent.
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]


def fix_one(p: Path, dry_run: bool) -> bool:
    text = p.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")
    header = soup.find("header")
    if header is None:
        return False
    part = header.find("div", class_="part-label")
    chap = header.find("div", class_="chapter-label")
    if part is None or chap is None:
        return False
    part_text = part.get_text(strip=True)
    chap_text = chap.get_text(strip=True)
    if part_text != chap_text:
        return False
    chap.decompose()
    new_text = str(soup)
    if new_text == text:
        return False
    if not dry_run:
        p.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    n = 0
    fm_dir = ROOT / "front-matter"
    for p in fm_dir.glob("*.html"):
        if fix_one(p, args.dry_run):
            n += 1
            print(f"  {p.relative_to(ROOT)}")
    print(f"\nTOTAL: {n} front-matter pages deduped")
    if args.dry_run:
        print("(dry run; nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
