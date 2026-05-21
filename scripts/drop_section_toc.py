"""Remove the per-section "What's in this section" mini-TOC.

It is markup of the form <aside class="section-internal-toc">...</aside> (a
single-section internal table of contents). Drop it from every section HTML.
Surrounding whitespace is collapsed so no blank gap is left behind.

Run:  py -3 scripts/drop_section_toc.py            # dry-run
      py -3 scripts/drop_section_toc.py --apply
"""
from __future__ import annotations
import argparse, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
SKIP = {"_archive", "node_modules", ".git", "pagefind", "KDP", "build", "vendor",
        ".claude", "__pycache__", ".book-update", ".tools", "temp_epub"}

ASIDE = re.compile(r"[ \t]*<aside class=\"section-internal-toc\">.*?</aside>[ \t]*\n?",
                   re.S | re.I)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    files = 0
    removed = 0
    for p in ROOT.rglob("*.html"):
        if any(s in p.parts for s in SKIP):
            continue
        html = p.read_text(encoding="utf-8", errors="ignore")
        n = len(ASIDE.findall(html))
        if not n:
            continue
        new = ASIDE.sub("", html)
        files += 1
        removed += n
        print(f"  {n}  {p.relative_to(ROOT)}")
        if args.apply:
            p.write_text(new, encoding="utf-8")
    print(f"\n{removed} aside(s) in {files} files {'removed' if args.apply else '(dry-run)'}")
    if not args.apply:
        print("(pass --apply to write)")


if __name__ == "__main__":
    main()
