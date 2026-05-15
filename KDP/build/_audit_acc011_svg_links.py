"""Find SVG <a> elements that lack an accessible name (ACC-011).

EPUB accessibility rules require every SVG link to have either an
aria-label attribute or a <title> child element. epubcheck flagged 50
such cases in v15.0. This script locates them in the source.

Usage:
  python _audit_acc011_svg_links.py            # report
  python _audit_acc011_svg_links.py --fix      # add aria-label from href
"""
from pathlib import Path
from bs4 import BeautifulSoup
import sys

ROOT = Path(__file__).resolve().parents[2]
SKIP_PARTS = {"KDP", "node_modules", "scripts", "styles", ".git", "pagefind"}


def file_iter():
    for p in ROOT.rglob("*.html"):
        rel = p.relative_to(ROOT)
        if any(part in SKIP_PARTS for part in rel.parts):
            continue
        yield p


def derive_label(a) -> str:
    """Build a label from href, fall back to anchor text, then a generic."""
    href = a.get("href", "") or a.get("xlink:href", "")
    text = a.get_text(strip=True)
    if text and len(text) <= 60:
        return text
    if href:
        # Strip hash, query, and path; keep meaningful tail
        tail = href.rsplit("/", 1)[-1].split("#", 1)[0].split("?", 1)[0]
        if tail:
            return f"Link: {tail}"
    return "SVG hyperlink"


def main():
    fix = "--fix" in sys.argv
    issues = []
    fixed = 0
    for p in file_iter():
        txt = p.read_text(encoding="utf-8")
        if "<svg" not in txt or "<a" not in txt:
            continue
        s = BeautifulSoup(txt, "html.parser")
        changed = False
        for svg in s.find_all("svg"):
            for a in svg.find_all("a"):
                if a.get("aria-label") or a.find("title"):
                    continue
                issues.append((str(p), str(a)[:120]))
                if fix:
                    a["aria-label"] = derive_label(a)
                    changed = True
        if fix and changed:
            p.write_text(str(s), encoding="utf-8")
            fixed += 1

    print(f"SVG <a> without accessible name: {len(issues)}")
    print(f"Files affected: {len({i[0] for i in issues})}")
    if not fix and issues:
        print("\nFirst 10 occurrences:")
        for path, html in issues[:10]:
            print(f"  {Path(path).name}")
            print(f"    {html}")
    if fix:
        print(f"\nFixed: {fixed} files updated with aria-label")


if __name__ == "__main__":
    main()
