"""Fix the appendix prefix-letter regression.

Each appendix directory `appendices/appendix-X-name/` should reference its
own section files as `section-X.N.html`. The bug pattern: index.html and
section files contain `section-Y.N.html` self-references where Y is some
adjacent appendix's letter (typically a one- or two-letter lag from when
the glossary was promoted out of the appendix tree and the labels drifted).

Self-refs to be rewritten:
    href="section-Y.N.html"           ->   href="section-X.N.html"
    href="section-Y.N.html#anchor"    ->   href="section-X.N.html#anchor"

Cross-refs to be left alone:
    href="../glossary/section-f.2.html"
    href="../appendix-m-inference-serving/section-m.3.html"

The distinction: any href starting with `section-` (no slash before) is a
self-reference. Any href containing a slash before `section-` points to a
different directory and is presumed correct.

Usage:
    python scripts/_fix_appendix_letters.py [--dry-run]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Appendices where the regression appears (G through P per the audit).
# The script auto-detects affected directories by scanning, but this is a
# safety net.
EXPECTED_DIRS = [
    "appendix-g-model-cards",
    "appendix-h-prompt-templates",
    "appendix-i-datasets-benchmarks",
    "appendix-j-huggingface-ecosystem",
    "appendix-k-langchain",
    "appendix-l-experiment-tracking",
    "appendix-m-inference-serving",
    "appendix-n-distributed-ml",
    "appendix-o-docker-containers",
    "appendix-p-tooling-ecosystem",
]

# Match a self-ref href to a section file in the same directory.
# The (?<!/) lookbehind rules out cross-dir refs like ../X/section-Y.N.html.
SELF_REF_RE = re.compile(r'(?<![/.])section-([a-z])\.(\d+)\.html')


def fix_file(path: Path, correct_letter: str, dry_run: bool) -> tuple[int, list[str]]:
    """Rewrite self-ref section letters in one file. Return (count, samples)."""
    text = path.read_text(encoding="utf-8")
    changes = []
    new_text, n = SELF_REF_RE.subn(
        lambda m: (
            f"section-{correct_letter}.{m.group(2)}.html"
            if m.group(1) != correct_letter
            else m.group(0)
        ),
        text,
    )
    # SELF_REF_RE.subn replaces every match unconditionally inside the lambda's
    # closure; count actual *changed* substitutions by diffing
    if n == 0:
        return 0, []
    # Refind to verify which were changed
    changed = 0
    for m in SELF_REF_RE.finditer(text):
        if m.group(1) != correct_letter:
            changed += 1
            if len(changes) < 3:
                changes.append(f"section-{m.group(1)}.{m.group(2)}.html -> section-{correct_letter}.{m.group(2)}.html")
    if changed == 0:
        return 0, []
    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return changed, changes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="Report changes without writing files")
    ap.add_argument("--root", default=".",
                    help="Project root (default: cwd)")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    appendices_dir = root / "appendices"
    if not appendices_dir.exists():
        print(f"error: not found: {appendices_dir}", file=sys.stderr)
        return 1

    total_files_changed = 0
    total_refs_changed = 0
    grand_samples = []

    for appendix_name in EXPECTED_DIRS:
        ap_dir = appendices_dir / appendix_name
        if not ap_dir.is_dir():
            print(f"skip (missing): {appendix_name}")
            continue

        # Extract the canonical letter from the dir name: "appendix-g-..." -> "g"
        parts = appendix_name.split("-")
        if len(parts) < 2 or len(parts[1]) != 1:
            print(f"skip (cannot parse letter): {appendix_name}")
            continue
        letter = parts[1]

        files = sorted(ap_dir.glob("*.html"))
        ap_files_changed = 0
        ap_refs_changed = 0
        for f in files:
            n, samples = fix_file(f, letter, args.dry_run)
            if n > 0:
                ap_files_changed += 1
                ap_refs_changed += n
                rel = f.relative_to(root)
                print(f"  {rel}: {n} ref(s) fixed -> letter '{letter}'")
                for s in samples:
                    print(f"      {s}")
                    grand_samples.append(f"{rel}: {s}")
        if ap_files_changed:
            print(f"  ----- {appendix_name}: {ap_files_changed} files, "
                  f"{ap_refs_changed} refs -----")
        else:
            print(f"  {appendix_name}: no self-ref letter mismatches found")
        total_files_changed += ap_files_changed
        total_refs_changed += ap_refs_changed

    print()
    print(f"TOTAL: {total_refs_changed} refs across {total_files_changed} files")
    if args.dry_run:
        print("(dry run; nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
