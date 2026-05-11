"""v3.5 R4#1: Renumber stale Code Fragment / Figure captions to match the
filename prefix.

After v3.x renumbering moved sections (e.g. section-37.1 -> section-36.5),
the captions inside still read 'Code Fragment 37.1.X' / 'Figure 37.1.X'.
The filename's chapter.section is ground truth; rewrite the caption prefix
to match it.

Mechanics: per file, extract (chapter, section) from filename. For every
'Code Fragment N.M.x' / 'Figure N.M.x' pattern where (N, M) != (chapter,
section), rewrite the prefix while PRESERVING the trailing index x.

Idempotent. Run from project root:
    /c/Python314/python KDP/build/_v35_renumber_captions.py
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE = {"_archive", "KDP", "node_modules", "vendor", "scripts"}

# Match 'Code Fragment X.Y.Z' or 'Figure X.Y.Z'
CAPTION_RE = re.compile(r"\b(Code Fragment|Figure) (\d+)\.(\d+)\.(\d+)\b")


def main() -> int:
    n_files = 0
    n_caps = 0
    for p in ROOT.glob("part-*/module-*/section-*.html"):
        m = re.match(r"section-(\d+)\.(\d+)\.html", p.name)
        if not m:
            continue
        file_chap, file_sec = m.group(1), m.group(2)
        text = p.read_text(encoding="utf-8", errors="replace")
        original = text

        def _sub(cap_m: re.Match) -> str:
            kind, c, s, idx = cap_m.groups()
            if c == file_chap and s == file_sec:
                return cap_m.group(0)  # already correct
            return f"{kind} {file_chap}.{file_sec}.{idx}"

        text, n = CAPTION_RE.subn(_sub, text)
        # Count actual rewrites (subn includes no-ops)
        actual = sum(
            1 for cm in CAPTION_RE.finditer(original)
            if cm.group(2) != file_chap or cm.group(3) != file_sec
        )
        if actual > 0 and text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1
            n_caps += actual
            print(f"  {actual:>3}x  {p.relative_to(ROOT).as_posix()}")

    print(f"\nFixed {n_caps} stale caption prefixes across {n_files} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
