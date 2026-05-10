"""Per-file deduplication of Code Fragment numbers.

After fix_code_fragment_numbering.py applied hierarchical X.Y.N numbering,
some files still have duplicates because the author copy-pasted (or hand-counted
incorrectly). Within ONE file, the same Code Fragment number appears 2+ times.

This script walks each file in order, tracks the count of each number, and
suffixes duplicates with `a`, `b`, `c`, etc. (Code Fragment 29.14.2,
Code Fragment 29.14.2a, Code Fragment 29.14.2b).

Idempotent: skip if any of N already ends in a letter suffix.
"""
from __future__ import annotations
import re
import shutil
import sys
import time
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Match `<strong>Code Fragment 29.14.2:</strong>` etc. Capture number.
CF_RE = re.compile(r"(<strong>Code Fragment\s+)([\d.]+)([a-z]?)(:\s*</strong>)", re.IGNORECASE)

LETTER_SUFFIXES = "abcdefghijklmnopqrstuvwxyz"


def dedup_in_file(content: str) -> tuple[str, int]:
    """Walk file in order, suffix duplicate numbers."""
    counts: dict[str, int] = defaultdict(int)
    n_changed = 0

    def replace(m: re.Match) -> str:
        nonlocal n_changed
        prefix = m.group(1)
        num = m.group(2).rstrip(".")
        existing_suffix = m.group(3)
        suffix_html = m.group(4)
        # If author already manually suffixed (a, b, c), trust it
        if existing_suffix:
            counts[num + existing_suffix] += 1
            return m.group(0)
        counts[num] += 1
        if counts[num] == 1:
            return m.group(0)
        # Duplicate: suffix with a, b, c
        idx = counts[num] - 2  # 2nd occurrence -> 'a' (index 0)
        if idx < len(LETTER_SUFFIXES):
            suffix_letter = LETTER_SUFFIXES[idx]
            n_changed += 1
            return f"{prefix}{num}{suffix_letter}{suffix_html}"
        return m.group(0)

    new_content = CF_RE.sub(replace, content)
    return new_content, n_changed


def main() -> int:
    files_modified: list[tuple[str, int]] = []
    backup_dir = PROJECT_ROOT / "KDP/build/source_fix_backups" / time.strftime("dedup_cf_%Y%m%d_%H%M%S")

    for path in PROJECT_ROOT.rglob("*.html"):
        if any(part in path.parts for part in ("KDP", "vendor", "scripts", "templates", "md", "node_modules")):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if "Code Fragment" not in text:
            continue
        new_text, n = dedup_in_file(text)
        if n > 0 and new_text != text:
            backup_dir.mkdir(parents=True, exist_ok=True)
            rel = path.relative_to(PROJECT_ROOT)
            backup = backup_dir / rel
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, backup)
            path.write_text(new_text, encoding="utf-8")
            files_modified.append((str(rel).replace("\\", "/"), n))

    total = sum(n for _, n in files_modified)
    print(f"Suffixed {total} duplicate Code Fragment numbers in {len(files_modified)} files")
    if files_modified:
        print(f"Backups: {backup_dir.relative_to(PROJECT_ROOT)}")
        for rel, n in files_modified:
            print(f"  {n}x  {rel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
