"""Re-sequence figure numbers within a section so captions appear in ascending
document order (fixes FIGURE_SEQUENCE after inserting a figure mid-document).

Within each given section file, collects <figcaption><strong>Figure X.Y.Z</strong>
in document order, reassigns Z = 1,2,3..., and atomically remaps every
"Figure X.Y.Z" mention (captions AND prose references) for that section's X.Y
prefix. References to other sections' figures (different X.Y) are untouched.

Usage: py -3 scripts/resequence_figures.py <section.html> [<section.html> ...]
"""
from __future__ import annotations
import re, sys
from collections import OrderedDict
from pathlib import Path

CAP = re.compile(r'<figcaption><strong>Figure (\d+\.\d+\.\d+)</strong>')


def resequence(path: str) -> int:
    p = Path(path)
    t = p.read_text(encoding="utf-8")
    caps = CAP.findall(t)
    if not caps:
        return 0
    by_xy: "OrderedDict[str, list]" = OrderedDict()
    for full in caps:
        xy = full.rsplit(".", 1)[0]
        by_xy.setdefault(xy, []).append(full)
    mapping = {}
    for xy, fulls in by_xy.items():
        for i, full in enumerate(fulls, 1):
            mapping[full] = f"{xy}.{i}"
    changed = [(o, n) for o, n in mapping.items() if o != n]
    if not changed:
        return 0
    new = t
    for i, (old, _) in enumerate(changed):
        new = re.sub(r"Figure " + re.escape(old) + r"\b", f"\x00F{i}\x00", new)
    for i, (_, newnum) in enumerate(changed):
        new = new.replace(f"\x00F{i}\x00", f"Figure {newnum}")
    p.write_text(new, encoding="utf-8")
    return len(changed)


def main():
    total = 0
    for path in sys.argv[1:]:
        n = resequence(path)
        if n:
            print(f"  {n} figure number(s) remapped: {path}")
        total += n
    print(f"{total} figure number(s) remapped across {len(sys.argv)-1} file(s)")


if __name__ == "__main__":
    main()
