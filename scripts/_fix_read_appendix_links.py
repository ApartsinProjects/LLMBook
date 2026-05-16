"""Fix every `<a href="appendix-X-slug/...">Read Appendix Y →</a>` where Y != X.
The earlier `_fix_appendix_nav_labels.py` matched only `&rarr;` (HTML entity)
but the actual files use the literal Unicode arrow `→`. This script handles
both forms book-wide.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude"}

# Match: <a href="appendix-y-slug/...">Read Appendix X (&rarr;|→|->)</a>
PAT = re.compile(
    r'(<a href="appendix-([a-z])-[^"/]+/[^"]+">Read Appendix\s+)([A-Z]+)(\s*(?:&rarr;|→|-&gt;|->)?\s*</a>)',
    re.I,
)


def fix_file(p: Path, dry_run: bool) -> tuple[int, list[str]]:
    text = p.read_text(encoding="utf-8")
    msgs: list[str] = []

    def repl(m: re.Match) -> str:
        prefix, dir_letter, label_letter, suffix = (
            m.group(1), m.group(2).upper(), m.group(3), m.group(4)
        )
        if label_letter == dir_letter:
            return m.group(0)
        msgs.append(f"  'Read Appendix {label_letter}' -> 'Read Appendix {dir_letter}'")
        return f"{prefix}{dir_letter}{suffix}"

    new = PAT.sub(repl, text)
    if new == text:
        return 0, []
    if not dry_run:
        p.write_text(new, encoding="utf-8")
    return len(msgs), msgs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    total = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        n, msgs = fix_file(p, args.dry_run)
        if n:
            total += n
            print(f"{p.relative_to(ROOT)}:")
            for m in msgs:
                print(m)
    print(f"\nTOTAL: {total} 'Read Appendix' link fixes")
    if args.dry_run:
        print("(dry run; nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
