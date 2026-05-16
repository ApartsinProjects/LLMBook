"""Fix caption-prefix drift in sections moved by the Module 25/27/31 dissolution.

After Wave 3 moved sections from dissolved modules to new chapters, the
captions inside those sections kept their OLD chapter prefix. E.g.,
section-41.2.html (moved from old 31.2 Product Management) still has
captions like "Code Fragment 31.2.1" when they should be "Code Fragment 41.2.1".

This script walks each moved file and rewrites caption chapter prefixes.

Moves (target_path, old_chap, new_chap):
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# (file_path, old_chap, new_chap) — based on the dissolution mapping
MOVES = [
    # Module 25 dissolution
    ("part-9-safety-security-ethics/module-38-agent-safety-security/section-38.1.html", 25, 38),
    ("part-9-safety-security-ethics/module-38-agent-safety-security/section-38.2.html", 25, 38),
    ("part-9-safety-security-ethics/module-38-agent-safety-security/section-38.3.html", 25, 38),
    ("part-9-safety-security-ethics/module-38-agent-safety-security/section-38.4.html", 25, 38),
    ("part-10-idea-to-product/module-48-shipping-deploying/section-48.5.html", 25, 48),
    ("part-10-idea-to-product/module-48-shipping-deploying/section-48.6.html", 25, 48),
    ("part-6-agentic-ai/module-28-multi-agent-systems/section-28.6.html", 25, 28),
    # Module 27 dissolution
    ("part-10-idea-to-product/module-43-vibe-coding/section-43.2.html", 27, 43),
    ("part-11-applications-across-industries/module-52-finance-llms/section-52.7.html", 27, 52),
    ("part-11-applications-across-industries/module-53-healthcare-llms/section-53.7.html", 27, 53),
    ("part-11-applications-across-industries/module-59-recommendation-search/section-59.2.html", 27, 59),
    ("part-11-applications-across-industries/module-55-cybersecurity-llms/section-55.7.html", 27, 55),
    ("part-11-applications-across-industries/module-58-creative-industries/section-58.2.html", 27, 58),
    ("part-7-multimodal-generation/module-32-embodied-world-models/section-32.8.html", 27, 32),
    # Module 31 dissolution
    ("part-10-idea-to-product/module-42-strategy-prioritization/section-42.3.html", 31, 42),
    ("part-10-idea-to-product/module-42-strategy-prioritization/section-42.4.html", 31, 42),
    ("part-10-idea-to-product/module-41-product-management/section-41.2.html", 31, 41),
    ("part-10-idea-to-product/module-47-scaling-economics/section-47.3.html", 31, 47),
    ("part-10-idea-to-product/module-47-scaling-economics/section-47.4.html", 31, 47),
    ("part-10-idea-to-product/module-46-compute-planning/section-46.3.html", 31, 46),
    ("part-10-idea-to-product/module-46-compute-planning/section-46.4.html", 31, 46),
    # Module 33 split
    ("part-12-frontiers/module-61-frontier-architectures/section-61.1.html", 33, 61),
    ("part-12-frontiers/module-61-frontier-architectures/section-61.2.html", 33, 61),
    ("part-12-frontiers/module-61-frontier-architectures/section-61.3.html", 33, 61),
    ("part-12-frontiers/module-61-frontier-architectures/section-61.4.html", 33, 61),
    ("part-12-frontiers/module-62-frontier-theory/section-62.1.html", 33, 62),
    ("part-12-frontiers/module-62-frontier-theory/section-62.2.html", 33, 62),
    ("part-12-frontiers/module-62-frontier-theory/section-62.3.html", 33, 62),
    ("part-12-frontiers/module-62-frontier-theory/section-62.4.html", 33, 62),
    ("part-7-multimodal-generation/module-32-embodied-world-models/section-32.4.html", 33, 32),
    ("part-6-agentic-ai/module-27-tool-use-protocols/section-27.6.html", 33, 27),
    ("part-12-frontiers/module-64-agi-trajectories/section-64.5.html", 33, 64),
]


def fix_file(rel: str, old_chap: int, new_chap: int, dry_run: bool) -> int:
    p = ROOT / rel
    if not p.exists():
        return -1
    text = p.read_text(encoding="utf-8")
    orig = text
    # Rewrite captions: Code Fragment <old>.X.Y, Figure, Table, Pseudocode
    for kind in ("Code Fragment", "Figure", "Table", "Pseudocode"):
        text = re.sub(
            rf"\b{kind}\s+{old_chap}\.(\d+(?:\.\d+)?)\b",
            rf"{kind} {new_chap}.\1", text,
        )
    # Rewrite body "Section <old>.X" -> "Section <new>.X" for self-references
    text = re.sub(
        rf"\bSection\s+{old_chap}\.(\d+(?:\.\d+)?)\b",
        rf"Section {new_chap}.\1", text,
    )
    # Rewrite intro phrases like "In Chapter <old>, ..." that point at the
    # section's own former chapter
    text = re.sub(rf"\bChapter\s+{old_chap}\b",
                   f"Chapter {new_chap}", text)
    if text == orig:
        return 0
    if not dry_run:
        p.write_text(text, encoding="utf-8")
    return 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply

    n_fixed = 0
    n_missing = 0
    for rel, old, new in MOVES:
        r = fix_file(rel, old, new, dry_run)
        if r == -1:
            n_missing += 1
            print(f"  MISSING {rel}")
        elif r > 0:
            n_fixed += 1

    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"\n{mode}: fixed caption drift in {n_fixed} moved sections "
          f"({n_missing} missing).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
