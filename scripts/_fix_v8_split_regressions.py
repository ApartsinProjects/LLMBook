"""Fix two v8 reshuffle regressions in newly-split For-Instructors appendices.

1. Course Syllabi (Q): the book-wide cross-ref rewrite saw 'Appendix Q'
   in the freshly-created file and rewrote it to 'Appendix P' (because
   the old Q->P rename applied). Restore 'Appendix Q' inside this file.

2. Intermediate Projects (S), Capstone (T), War Stories (U): my
   _wrap_as_appendix_index helper wrote h1 as 'Appendix X: Title' with
   prefix, while the rest of the book uses just 'Title' for appendix
   index h1s. Strip the prefix.

Idempotent. Run once.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPS = ROOT / "appendices"


def fix_q_appendix_p_to_q() -> int:
    p = APPS / "appendix-q-course-syllabi" / "index.html"
    if not p.exists():
        print(f"SKIP: {p.name} missing")
        return 0
    text = p.read_text(encoding="utf-8")
    orig = text
    # Replace 'Appendix P' -> 'Appendix Q' but only inside this file
    text = re.sub(r"\bAppendix\s+P\b", "Appendix Q", text)
    if text != orig:
        p.write_text(text, encoding="utf-8")
        print(f"  Fixed {p.parent.name}/{p.name}: Appendix P -> Appendix Q")
        return 1
    return 0


def strip_h1_prefix() -> int:
    n = 0
    for letter, slug in [("S", "intermediate-projects"),
                          ("T", "capstone-project"),
                          ("U", "war-stories")]:
        p = APPS / f"appendix-{letter.lower()}-{slug}" / "index.html"
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        orig = text
        # Strip 'Appendix X: ' from h1
        text = re.sub(
            rf"<h1>Appendix {letter}: ([^<]+)</h1>",
            r"<h1>\1</h1>",
            text,
        )
        if text != orig:
            p.write_text(text, encoding="utf-8")
            print(f"  Stripped 'Appendix {letter}: ' prefix from h1 in "
                   f"{p.parent.name}/{p.name}")
            n += 1
    return n


def main() -> int:
    print("=== Fix v8 split regressions ===")
    n_q = fix_q_appendix_p_to_q()
    n_stripped = strip_h1_prefix()
    print(f"Q (Course Syllabi) Appendix P -> Q: {n_q} file")
    print(f"S/T/U h1 prefix stripped:          {n_stripped} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
