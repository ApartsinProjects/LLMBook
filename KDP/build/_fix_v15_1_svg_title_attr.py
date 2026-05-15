"""Strip 'title' attribute from <a> elements inside SVG.

The ACC-011 fix added aria-label to glossary-links inside SVG, but the
links still had their HTML 'title="Glossary: X"' attribute. SVG <a> does
not accept the title attribute (SVG uses a <title> child element
instead). epubcheck flags this with RSC-025.

The aria-label we added already provides the accessible name; the title
is redundant inside SVG context. Strip it.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import sys

ROOT = Path(__file__).resolve().parents[2]
SKIP = {"KDP", "node_modules", ".git", "pagefind", "scripts", "styles"}


def main():
    apply = "--apply" in sys.argv
    fixed_files = 0
    fixed_attrs = 0
    for p in ROOT.rglob("*.html"):
        if any(part in SKIP for part in p.parts):
            continue
        txt = p.read_text(encoding="utf-8")
        if "<svg" not in txt:
            continue
        s = BeautifulSoup(txt, "html.parser")
        changed = False
        for svg in s.find_all("svg"):
            for a in svg.find_all("a"):
                if a.has_attr("title"):
                    if apply:
                        del a.attrs["title"]
                    fixed_attrs += 1
                    changed = True
        if changed:
            fixed_files += 1
            if apply:
                p.write_text(str(s), encoding="utf-8")
    print(f"SVG <a> title attrs found: {fixed_attrs}")
    print(f"Files: {fixed_files} {'(APPLIED)' if apply else '(DRY RUN; use --apply)'}")


if __name__ == "__main__":
    main()
