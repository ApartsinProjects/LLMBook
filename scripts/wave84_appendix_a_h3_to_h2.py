"""Wave 84: Promote h3 -> h2 in appendix-A sections a.1-a.4.

These 4 sections have h1 -> h3 x4 with NO h2 between them, triggering
HEADING_HIERARCHY violations. The h3s ARE top-level subsections of the
section, so promoting to h2 is the right fix.

Sections a.5 and a.6 already have correct h2/h3 nesting and are skipped.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
APPENDIX_DIR = ROOT / "appendices" / "appendix-a-mathematical-foundations"
TARGETS = ["section-a.1.html", "section-a.2.html",
           "section-a.3.html", "section-a.4.html"]

H3_OPEN_RE = re.compile(r'<h3(\s[^>]*)?>', re.IGNORECASE)
H3_CLOSE_RE = re.compile(r'</h3>', re.IGNORECASE)


def fix_file(p: Path) -> int:
    html = p.read_text(encoding="utf-8")
    new_html, n_open = H3_OPEN_RE.subn(
        lambda m: f'<h2{m.group(1) or ""}>', html
    )
    new_html, n_close = H3_CLOSE_RE.subn('</h2>', new_html)
    if n_open != n_close:
        print(f"  ! {p.name}: open/close count mismatch ({n_open}/{n_close})")
        return 0
    if new_html == html:
        return 0
    p.write_text(new_html, encoding="utf-8")
    return n_open


def main():
    total = 0
    for name in TARGETS:
        p = APPENDIX_DIR / name
        if not p.exists():
            print(f"  ! missing: {p}")
            continue
        n = fix_file(p)
        total += n
        print(f"  + {p.name}: {n} h3 -> h2")
    print(f"\nTotal headings promoted: {total}")


if __name__ == "__main__":
    main()
