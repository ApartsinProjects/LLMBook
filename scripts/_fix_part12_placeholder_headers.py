"""Fix Part 12 chapter landings whose section headings render as loose text
with a placeholder character: `^.1 Title`, `_.1 Title`, etc.

The placeholder character (`^`, `_`, `*`, etc.) should be the chapter number
(36, 37, 38, ...) and the line should be wrapped in `<h2>`. Also fixes the
`data-pagefind-meta="part:Appendices"` typo on these pages to point to
Part XII.

Idempotent.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PART_12 = ROOT / "part-12-llm-applications-across-industries"
PART_TITLE = "Part XII: LLM Applications Across Industries"

# Match any chapter-section line: <ph>.<N> <Title>
# <ph> is one of: ^ _ * ~ %
# <N> is a digit run (1, 12, etc.)
# <Title> is text up to the end of line (one line only)
LINE_RE = re.compile(
    r"^[ \t]*([\^_\*~%])\.(\d+)\s+([^\n<]+?)[ \t]*$",
    re.M,
)


def fix_file(p: Path, dry_run: bool) -> tuple[int, list[str]]:
    text = p.read_text(encoding="utf-8")
    orig = text
    messages: list[str] = []

    # Derive chapter number from the directory name: module-NN-slug
    m = re.match(r"module-(\d+)-", p.parent.name)
    if not m:
        return 0, []
    chapter_num = int(m.group(1))

    def sub(match: re.Match) -> str:
        ph, n, title = match.group(1), match.group(2), match.group(3).strip()
        messages.append(f"  {ph}.{n} {title!r} → <h2>{chapter_num}.{n} {title}</h2>")
        return f"<h2>{chapter_num}.{n} {title}</h2>"

    text = LINE_RE.sub(sub, text)

    # Fix the pagefind-meta typo
    if 'data-pagefind-meta="part:Appendices"' in text:
        text = text.replace(
            'data-pagefind-meta="part:Appendices"',
            f'data-pagefind-meta="part:{PART_TITLE}"',
        )
        messages.append("  fixed pagefind-meta part:Appendices → part:Part XII")

    if text == orig:
        return 0, []
    if not dry_run:
        p.write_text(text, encoding="utf-8")
    return len(messages), messages


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    total_changes = 0
    files_changed = 0
    for p in sorted(PART_12.glob("module-*/index.html")):
        n, msgs = fix_file(p, args.dry_run)
        if n:
            files_changed += 1
            total_changes += n
            print(f"{p.relative_to(ROOT)}:")
            for m in msgs:
                print(m)
    print(f"\nTOTAL: {total_changes} edits across {files_changed} files")
    if args.dry_run:
        print("(dry run; nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
