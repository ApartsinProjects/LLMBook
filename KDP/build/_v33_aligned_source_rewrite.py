"""v3.3: Source-level rewrite of multi-line display math.

Wraps any `$$ ... \\\\ ... $$` block in `\begin{aligned} ... \end{aligned}`
so that web KaTeX (auto-render) and EPUB KaTeX both produce stacked lines
instead of one wide line that overflows narrow screens.

Idempotent: blocks already wrapped in aligned/align/gathered/cases/etc.
are left alone.

Run from project root:
    /c/Python314/python KDP/build/_v33_aligned_source_rewrite.py
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE = {"_archive", "KDP", "node_modules", "vendor", "scripts"}

DISPLAY_MATH = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)
HAS_LINE_BREAK = re.compile(r"\\\\")
HAS_ENV = re.compile(
    r"\\begin\{(?:aligned|align\*?|gathered|cases|matrix|array|bmatrix|"
    r"pmatrix|vmatrix|smallmatrix|split|multline)\}"
)
EQ_PER_LINE = re.compile(r"^([^=&\n]*)=", re.MULTILINE)


def rewrite_block(match: re.Match) -> str:
    body = match.group(1)
    if not HAS_LINE_BREAK.search(body):
        return match.group(0)
    if HAS_ENV.search(body):
        return match.group(0)
    # Insert `&` before first `=` per line for column alignment
    aligned_body = EQ_PER_LINE.sub(r"\1&=", body)
    return r"$$\begin{aligned}" + aligned_body + r"\end{aligned}$$"


def main() -> int:
    n_files = 0
    n_blocks = 0
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        if "$$" not in text or "\\\\" not in text:
            continue
        new_text, count = DISPLAY_MATH.subn(rewrite_block, text)
        # Count actual rewrites (subn counts every match, even no-ops)
        actual_changes = sum(
            1 for m in DISPLAY_MATH.finditer(text)
            if HAS_LINE_BREAK.search(m.group(1)) and not HAS_ENV.search(m.group(1))
        )
        if actual_changes > 0 and new_text != text:
            p.write_text(new_text, encoding="utf-8")
            n_files += 1
            n_blocks += actual_changes
            print(f"  {actual_changes:>2}x  {p.relative_to(ROOT).as_posix()}")
    print(f"\nWrapped {n_blocks} multi-line display-math blocks in {n_files} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
