"""Phase 6: inject the authored scratch sections into their target modules.

Reads migration-map.json's `sections_from_scratch` list. For each entry,
copies _scratch_part8_new_sections/section-X.Y.html -> the destination
module's section-X.Y.html. Skips entries whose source doesn't exist
(stub-only entries).

DRY-RUN by default; --apply to execute.
"""
from __future__ import annotations
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MAP = HERE / "migration-map.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply
    data = json.loads(MAP.read_text(encoding="utf-8"))

    print(f"=== Phase 6: inject scratch sections ===")
    if dry_run:
        print("(DRY-RUN; pass --apply to execute)")
    print()
    injected = 0
    skipped = 0
    for entry in data["sections_from_scratch"]:
        src = ROOT / entry["from"]
        dst = ROOT / entry["to"]
        if not src.exists():
            print(f"  SKIP (scratch not authored): {entry['from']}")
            skipped += 1
            continue
        if dst.exists():
            print(f"  SKIP (dst exists already): {entry['to']}")
            skipped += 1
            continue
        print(f"  INJECT: {entry['from']} -> {entry['to']}")
        if not dry_run:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            # Stage with git
            subprocess.run(["git", "add", str(dst)], cwd=ROOT)
        injected += 1
    print()
    print(f"=== Summary ===")
    print(f"Injected: {injected}")
    print(f"Skipped:  {skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
