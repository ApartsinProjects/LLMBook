"""Rewrite stale 'Appendix AJ/AK' prose references after v15 redesign.

The v15.0 redesign moved appendix-aj-reading-pathways to
front-matter/fm-reading-pathways.html and appendix-ak-course-syllabi to
front-matter/fm-course-syllabi.html, but prose still says "Appendix AJ:
Reading Pathways" and "Appendix AK: Course Syllabi".

These appear in:
  - appendices/appendix-v-freshness-2026/index.html
  - appendices/index.html
  - front-matter/{fm-course-syllabi,fm-reading-pathways,fm-who-should-read,
                  foreword,look-inside-preview}.html

Replace with plain "Reading Pathways" / "Course Syllabi".
"""
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
SKIP = {"KDP", "node_modules", ".git", "pagefind", "scripts", "styles"}


def fix_text(t: str) -> str:
    out = t
    # Common phrasings to clean up
    out = re.sub(r'\bAppendix\s+AJ:?\s*Reading Pathways', 'Reading Pathways', out)
    out = re.sub(r'\bAppendix\s+AK:?\s*Course Syllabi', 'Course Syllabi', out)
    # Bare "Appendix AJ" / "Appendix AK" without trailing title - drop
    out = re.sub(r'\bAppendix\s+AJ\b', 'Reading Pathways', out)
    out = re.sub(r'\bAppendix\s+AK\b', 'Course Syllabi', out)
    return out


def main():
    apply = "--apply" in sys.argv
    files_touched = 0
    total = 0
    for p in ROOT.rglob("*.html"):
        if any(part in SKIP for part in p.parts):
            continue
        s = p.read_text(encoding="utf-8")
        if "Appendix AJ" not in s and "Appendix AK" not in s:
            continue
        soup = BeautifulSoup(s, "html.parser")
        changed = False
        n_local = 0
        for el in list(soup.find_all(string=True)):
            if el.parent and el.parent.name in ("code", "pre", "script", "style", "title"):
                continue
            t = str(el)
            new_t = fix_text(t)
            if new_t != t:
                el.replace_with(NavigableString(new_t))
                changed = True
                n_local += 1
        if changed:
            files_touched += 1
            total += n_local
            if apply:
                p.write_text(str(soup), encoding="utf-8")
            print(f"  {p.relative_to(ROOT)}: {n_local} text nodes")

    print()
    print(f"Total: {total} text nodes across {files_touched} files "
          f"{'(APPLIED)' if apply else '(DRY RUN; use --apply)'}")


if __name__ == "__main__":
    main()
