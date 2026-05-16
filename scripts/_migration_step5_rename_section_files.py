"""Migration step 5: rename section files inside renumbered chapter dirs.

After step 3 renamed module dirs (e.g. module-21-ai-agents -> module-26-ai-agents),
the section files inside still have their OLD chapter prefix in the filename
(section-21.1.html, section-21.2.html, etc.). Step 4 rewrote the body text and
href references, so now we need to rename the actual files on disk.

Rules:
- Inside module-NN-slug/, find every section-X.Y.html.
- If X != NN, rename to section-NN.Y.html.

Idempotent. Skips files that already have the correct prefix.
"""
from __future__ import annotations
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply

    renamed = 0
    for mod_dir in sorted(ROOT.glob("part-*/module-*")):
        if not mod_dir.is_dir():
            continue
        m = re.match(r"module-(\d+)-", mod_dir.name)
        if not m:
            continue
        chap_num = int(m.group(1))
        for sec_file in sorted(mod_dir.glob("section-*.html")):
            sm = re.match(r"section-(\d+)\.(\d+(?:\.\d+)?)\.html", sec_file.name)
            if not sm:
                continue
            old_chap = int(sm.group(1))
            rest = sm.group(2)
            if old_chap == chap_num:
                continue  # already correct
            new_name = f"section-{chap_num}.{rest}.html"
            new_path = sec_file.parent / new_name
            if new_path.exists():
                print(f"  SKIP {sec_file.name} -> {new_name}: target exists")
                continue
            print(f"  git mv {mod_dir.name}/{sec_file.name} -> {new_name}")
            if not dry_run:
                subprocess.run(["git", "mv", str(sec_file), str(new_path)],
                                cwd=ROOT, check=False)
                renamed += 1

    # Same logic for appendices (skip for now — handled in a later step)

    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"\n{mode}: renamed {renamed} section files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
