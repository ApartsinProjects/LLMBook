"""
Fix image-caption misalignment in <div class="diagram-container"> blocks.

For each diagram-container in source HTML:
  1. Extract the figure number from the caption ("Figure N.M.K")
  2. Look for an image file `fig-N.M.K*.png` (or .svg/.jpg) in the chapter's images/ folder
  3. If found AND different from current src, replace the src
  4. Log the change

Safe by design: only updates the src URL, doesn't rename files, doesn't
renumber captions, doesn't move blocks. If the matching image doesn't
exist, leave the diagram alone (will need manual attention).

Usage:
    python KDP/build/fix_diagram_image_pairs.py            # dry-run, prints would-be changes
    python KDP/build/fix_diagram_image_pairs.py --apply    # write changes
"""
from __future__ import annotations

import argparse
import re
import shutil
from collections import defaultdict
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKUP_ROOT = PROJECT_ROOT / "KDP" / "build" / "source_fix_backups"

# Match: <div class="diagram-container">...<img src="X" ...>...<div class="diagram-caption"><strong>Figure N.M.K</strong>:...
DIAG_BLOCK_RE = re.compile(
    r'(<div class="diagram-container">\s*<img\b[^>]*?src=")([^"]+)("[^>]*?>\s*<div class="diagram-caption">\s*<strong>Figure ([\d.]+[a-z]?)</strong>)',
    re.DOTALL,
)


def find_image_for_figure(figure_num: str, images_dir: Path) -> Path | None:
    """Return the image file in images_dir whose name starts with `fig-{figure_num}-...`."""
    if not images_dir.exists():
        return None
    # Try exact prefix match
    candidates = []
    for ext in (".png", ".svg", ".jpg", ".jpeg"):
        for p in images_dir.glob(f"fig-{figure_num}-*{ext}"):
            candidates.append(p)
        for p in images_dir.glob(f"fig-{figure_num}{ext}"):
            candidates.append(p)
    if candidates:
        # Prefer .png, then .svg, then jpg
        candidates.sort(key=lambda p: ("png", "svg", "jpg", "jpeg").index(p.suffix.lstrip(".").lower()))
        return candidates[0]
    return None


def process_file(file: Path, dry_run: bool, run_dir: Path) -> dict:
    """Returns dict with stats."""
    text = file.read_text(encoding="utf-8")
    if "diagram-container" not in text:
        return {"checked": 0, "fixed": 0, "missing": 0}

    images_dir = file.parent / "images"
    n_checked = 0
    n_fixed = 0
    n_missing = 0
    fixes: list[tuple] = []  # (old_src, new_src, figure_num)

    def replace(m):
        nonlocal n_checked, n_fixed, n_missing
        prefix, current_src, suffix_caption_num = m.group(1), m.group(2), m.group(3)
        figure_num = m.group(4)
        n_checked += 1
        # Look up the right image for this figure number
        target = find_image_for_figure(figure_num, images_dir)
        if target is None:
            n_missing += 1
            return m.group(0)  # unchanged
        # Build the relative src to use
        new_src = f"images/{target.name}"
        if new_src == current_src or current_src.endswith(target.name):
            return m.group(0)  # already correct
        fixes.append((current_src, new_src, figure_num))
        n_fixed += 1
        return f"{prefix}{new_src}{suffix_caption_num}"

    new_text = DIAG_BLOCK_RE.sub(replace, text)

    if n_fixed > 0 and not dry_run:
        rel = file.relative_to(PROJECT_ROOT)
        backup_target = run_dir / rel.with_suffix(rel.suffix + ".bak")
        backup_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file, backup_target)
        file.write_text(new_text, encoding="utf-8")

    if n_fixed > 0 or n_missing > 0:
        print(f"  {file.relative_to(PROJECT_ROOT)} - {n_checked} checked, {n_fixed} fixed, {n_missing} missing image")
        for old, new, num in fixes:
            old_short = old.rsplit("/", 1)[-1]
            new_short = new.rsplit("/", 1)[-1]
            print(f"    Figure {num}: {old_short}  ->  {new_short}")

    return {"checked": n_checked, "fixed": n_fixed, "missing": n_missing, "file": str(file.relative_to(PROJECT_ROOT))}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[1])
    p.add_argument("--apply", action="store_true", help="Apply changes (default is dry-run)")
    p.add_argument("--only", default=None, help="Only process files matching this glob pattern (e.g. 'part-1*/section-4.1.html')")
    args = p.parse_args()

    files: list[Path] = []
    for p2 in PROJECT_ROOT.rglob("*.html"):
        rel = p2.relative_to(PROJECT_ROOT)
        if rel.parts[0] in {"KDP", "scripts", "vendor", "templates", "md"}:
            continue
        if args.only and not p2.match(args.only):
            continue
        files.append(p2)

    print(f"Source HTML files in scope: {len(files)}")
    print(f"Mode: {'APPLY' if args.apply else 'DRY-RUN'}")

    run_dir = BACKUP_ROOT / datetime.now().strftime("diag_image_pair_%Y%m%d-%H%M%S")
    if args.apply:
        run_dir.mkdir(parents=True, exist_ok=True)
        print(f"Backup dir: {run_dir.relative_to(PROJECT_ROOT)}")

    totals = defaultdict(int)
    for file in files:
        stats = process_file(file, dry_run=not args.apply, run_dir=run_dir)
        for k in ("checked", "fixed", "missing"):
            totals[k] += stats[k]

    print()
    print("=" * 60)
    print(f"SUMMARY: {totals['checked']} diagram blocks checked")
    print(f"  {totals['fixed']} src updated to match caption figure number")
    print(f"  {totals['missing']} diagrams have no matching image file (need manual generation)")
    if not args.apply and totals["fixed"]:
        print()
        print("To apply: python KDP/build/fix_diagram_image_pairs.py --apply")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
