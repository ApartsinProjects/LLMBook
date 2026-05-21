"""Scan source HTML for literal '<' inside LaTeX math ($...$, $$...$$).

A literal '<' immediately followed by a letter (e.g. x_{<t}, \\sum_{j<k}) is
parsed by the HTML/XHTML parser as the start of a tag, corrupting the math and
sometimes producing an "invalid token" XML error in the built EPUB. Such '<'
must be written as &lt; (KaTeX decodes the entity back to '<' when rendering).
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = ("_archive/", "KDP/", "node_modules/", "pagefind/", "temp_epub/",
        "templates/", ".git/", "scripts/")


def skip(p: Path) -> bool:
    s = str(p).replace("\\", "/") + "/"
    return any(k in s for k in SKIP)


INLINE = re.compile(r'(?<!\$)\$(?!\$)([^\$\n]{1,400}?)\$(?!\$)')
DISPLAY = re.compile(r'\$\$(.+?)\$\$', re.S)
DANGER = re.compile(r'<[a-zA-Z]')
CMD = re.compile(r'\\[a-zA-Z]+')


def is_real_latex(f: str) -> bool:
    # Exclude HTML-attribute / currency / code-span false positives.
    for bad in ('class=', '=""', 'href=', '&#36;', '</span>', '<span', '<code',
                '<strong', '<em>', '<sub>', '<sup>'):
        if bad in f:
            return False
    return len(CMD.findall(f)) >= 1


def main() -> None:
    hits = []
    for p in ROOT.rglob("*.html"):
        if skip(p):
            continue
        try:
            t = p.read_text(encoding="utf-8")
        except Exception:
            continue
        spans = [("$$", m.group(1), m.start()) for m in DISPLAY.finditer(t)]
        t2 = DISPLAY.sub(lambda m: " " * len(m.group(0)), t)
        spans += [("$", m.group(1), m.start()) for m in INLINE.finditer(t2)]
        for kind, frag, pos in spans:
            if DANGER.search(frag) and is_real_latex(frag):
                ln = t.count("\n", 0, pos) + 1
                rel = str(p.relative_to(ROOT)).replace("\\", "/")
                hits.append((rel, ln, kind, frag.strip()[:140]))
    print(f"GENUINE literal-< in LaTeX math: {len(hits)}")
    for f, ln, kind, frag in sorted(hits):
        print(f"  {f}:{ln} [{kind}] {frag!r}")


if __name__ == "__main__":
    main()
