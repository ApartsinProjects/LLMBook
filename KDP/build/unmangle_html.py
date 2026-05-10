"""
Best-effort reversal of BeautifulSoup re-serialization changes.

When the previous BS-based source-fix run wrote files via str(soup),
BeautifulSoup applied its own normalization rules:
  - meta/link/img made self-closing  (<meta charset="UTF-8"> -> <meta charset="utf-8"/>)
  - charset value lowercased
  - attributes alphabetically reordered
  - empty boolean attributes given empty values  (defer -> defer="")
  - indentation collapsed
  - some entity rewrites

This script reverses the most visible patterns to bring file formatting
closer to the original convention used elsewhere in the project. It does
NOT change semantics - just the cosmetic appearance.

Usage:
    python KDP/build/unmangle_html.py             # apply
    python KDP/build/unmangle_html.py --dry-run

Backups go to KDP/build/source_fix_backups/<TS>/.
"""
from __future__ import annotations

import argparse
import re
import shutil
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKUP_ROOT = PROJECT_ROOT / "KDP" / "build" / "source_fix_backups"


# Common BS-output patterns and their pristine equivalents.
# Each is a (regex, replacement) pair applied in order.
TRANSFORMS = [
    # <meta charset="utf-8"/> -> <meta charset="UTF-8">
    (re.compile(r'<meta charset="utf-8"\s*/?>', re.IGNORECASE),
     '<meta charset="UTF-8">'),
    # <meta content="X" name="Y"/> -> <meta name="Y" content="X">
    (re.compile(r'<meta content="([^"]*)" name="([^"]*)"\s*/?>', re.IGNORECASE),
     r'<meta name="\2" content="\1">'),
    # <link href="X" rel="Y"/> -> <link rel="Y" href="X">
    (re.compile(r'<link href="([^"]*)" rel="([^"]*)"\s*/?>', re.IGNORECASE),
     r'<link rel="\2" href="\1">'),
    # <link href="X" rel="Y" type="Z"/> -> <link rel="Y" type="Z" href="X">
    (re.compile(r'<link href="([^"]*)" rel="([^"]*)" type="([^"]*)"\s*/?>', re.IGNORECASE),
     r'<link rel="\2" type="\3" href="\1">'),
    # <script defer="" src="X"></script> -> <script defer src="X"></script>
    (re.compile(r'<script defer="" '),
     '<script defer '),
    # <img alt="X" src="Y"/> common BS reorder for img with no other attrs
    (re.compile(r'<img alt="([^"]*)" src="([^"]*)"\s*/?>', re.IGNORECASE),
     r'<img src="\2" alt="\1">'),
    # <img alt="X" class="Y" src="Z"/> -> <img class="Y" src="Z" alt="X">
    (re.compile(r'<img alt="([^"]*)" class="([^"]*)" src="([^"]*)"\s*/?>', re.IGNORECASE),
     r'<img class="\2" src="\3" alt="\1">'),
    # <img alt="X" height="N" src="Y" width="M"/> -> <img src="Y" alt="X" width="M" height="N">
    (re.compile(r'<img alt="([^"]*)" height="(\d+)" src="([^"]*)" width="(\d+)"\s*/?>', re.IGNORECASE),
     r'<img src="\3" alt="\1" width="\4" height="\2">'),
    # <img alt="X" class="Y" height="N" src="Z" width="M"/>
    (re.compile(r'<img alt="([^"]*)" class="([^"]*)" height="(\d+)" src="([^"]*)" width="(\d+)"\s*/?>', re.IGNORECASE),
     r'<img class="\2" src="\4" alt="\1" width="\5" height="\3">'),
]


def is_bs_mangled(text: str) -> bool:
    """Heuristic: detect BS-mangled formatting."""
    return '<meta charset="utf-8"/>' in text


def unmangle(text: str) -> tuple[str, int]:
    """Apply all unmangling transforms; return (new_text, n_changes)."""
    n = 0
    for pat, replacement in TRANSFORMS:
        new_text, count = pat.subn(replacement, text)
        if count > 0:
            text = new_text
            n += count
    return text, n


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[1])
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    run_dir = BACKUP_ROOT / datetime.now().strftime("%Y%m%d-%H%M%S")
    if not args.dry_run:
        run_dir.mkdir(parents=True, exist_ok=True)
        print(f"Backup dir: {run_dir.relative_to(PROJECT_ROOT)}")

    files: list[Path] = []
    for p2 in PROJECT_ROOT.rglob("*.html"):
        rel = p2.relative_to(PROJECT_ROOT)
        if rel.parts and rel.parts[0] in {"KDP", "scripts", "vendor", "templates", "md"}:
            continue
        files.append(p2)

    print(f"Source HTML files in scope: {len(files)}")

    n_files = 0
    n_changes = 0

    for file in files:
        text = file.read_text(encoding="utf-8")
        if not is_bs_mangled(text):
            continue
        new_text, count = unmangle(text)
        if count > 0:
            n_files += 1
            n_changes += count
            if not args.dry_run:
                rel = file.relative_to(PROJECT_ROOT)
                target = run_dir / rel.with_suffix(rel.suffix + ".bak")
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file, target)
                file.write_text(new_text, encoding="utf-8")

    print(f"\nUnmangled {n_files} files, {n_changes} pattern matches")
    if not args.dry_run and n_files:
        print(f"Backups in: {run_dir.relative_to(PROJECT_ROOT)}")

    # Show remaining mangled count
    remaining = sum(1 for p2 in files if is_bs_mangled(p2.read_text(encoding="utf-8", errors="replace")))
    print(f"Files still showing meta-charset BS-mangling: {remaining}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
