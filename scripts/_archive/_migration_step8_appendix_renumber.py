"""Migration step 8: Renumber appendices per the target yaml.

Drops G (Model Cards), H (Prompt Templates), I (Datasets/Benchmarks).
Regroups remaining 18 into 4 thematic groups and relabels A through R.

Renumber map (from target yaml):
  A -> A (Mathematical Foundations)
  B -> B (Machine Learning Essentials)
  C -> C (Python Libraries)
  D -> D (Dev Environment)
  E -> E (Git/DVC)
  J -> F (HuggingFace)
  K -> G (LangChain)
  P -> H (LLM Tooling Ecosystem)
  F -> I (GPU Hardware)
  L -> J (Experiment Tracking)
  M -> K (Inference Serving)
  N -> L (Distributed ML)
  O -> M (Docker)
  Q -> N (Master Reference Tables)
  R -> O (Production Patterns)
  S -> P (Pedagogy Kit + Capstone)
  T -> Q (Problem-Solution Key)
  U -> R (Freshness 2026)

Dropped: G, H, I (Model Cards, Prompt Templates, Datasets/Benchmarks)

Procedure:
  1. Drop the three doomed appendix dirs (G, H, I).
  2. Rename remaining appendix dirs using temp prefix to avoid collisions.
  3. Rename section files inside each (section-x.N.html -> section-y.N.html).
  4. Update internal references (caption letters, breadcrumbs, hrefs).
  5. Book-wide cross-ref rewrite for any "Appendix X" / "X.N" reference.
"""
from __future__ import annotations
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPS = ROOT / "appendices"

# (old_letter, new_letter, slug)
RENAMES = [
    ("J", "F", "huggingface-ecosystem"),
    ("K", "G", "langchain"),
    ("P", "H", "tooling-ecosystem"),
    ("F", "I", "hardware-compute"),
    ("L", "J", "experiment-tracking"),
    ("M", "K", "inference-serving"),
    ("N", "L", "distributed-ml"),
    ("O", "M", "docker-containers"),
    ("Q", "N", "master-reference-tables"),
    ("R", "O", "production-patterns"),
    ("S", "P", "pedagogy-kit"),
    ("T", "Q", "problem-solution-key"),
    ("U", "R", "freshness-2026"),
]

DROPS = [
    ("G", "model-cards"),
    ("H", "prompt-templates"),
    ("I", "datasets-benchmarks"),
]


def rename_appendix(old_letter: str, new_letter: str, slug: str,
                     dry_run: bool, temp: bool) -> int:
    """Rename one appendix dir + its section files. Returns n_changes."""
    old_letter_lower = old_letter.lower()
    new_letter_lower = new_letter.lower()
    if temp:
        old_name = f"appendix-{old_letter_lower}-{slug}"
        new_name = f"_tmp-{new_letter_lower}-{slug}"
    else:
        old_name = f"_tmp-{new_letter_lower}-{slug}"
        new_name = f"appendix-{new_letter_lower}-{slug}"

    old_dir = APPS / old_name
    new_dir = APPS / new_name
    if not old_dir.exists():
        return 0
    if new_dir.exists():
        print(f"  SKIP rename: target {new_name} exists")
        return 0
    if dry_run:
        print(f"  WOULD git mv appendices/{old_name} -> appendices/{new_name}")
        return 1
    subprocess.run(["git", "mv", str(old_dir), str(new_dir)],
                    cwd=ROOT, check=False)

    # Rename section files inside (after the final rename, not during temp)
    if not temp:
        for sec_file in sorted(new_dir.glob(f"section-{old_letter_lower}.*.html")):
            new_sec = sec_file.parent / sec_file.name.replace(
                f"section-{old_letter_lower}.", f"section-{new_letter_lower}.")
            if new_sec == sec_file:
                continue
            subprocess.run(["git", "mv", str(sec_file), str(new_sec)],
                            cwd=ROOT, check=False)
    return 1


def drop_appendix(letter: str, slug: str, dry_run: bool) -> int:
    """git rm the doomed appendix dir."""
    d = APPS / f"appendix-{letter.lower()}-{slug}"
    if not d.exists():
        return 0
    print(f"  WOULD git rm -r appendices/{d.name}" if dry_run else
          f"  git rm -r appendices/{d.name}")
    if not dry_run:
        subprocess.run(["git", "rm", "-r", str(d)],
                        cwd=ROOT, check=False)
    return 1


def update_internal_refs(dry_run: bool) -> int:
    """Inside each renamed appendix, update caption letters + breadcrumb +
    self-references. Use temp tokens for the swap to avoid collisions."""
    # Build forward map and apply in 2 passes
    forward = {old: new for old, new, _ in RENAMES}
    n_files = 0
    SKIP = {"node_modules", ".git", "KDP", "build", "temp_ebook", "temp_epub",
            "source_fix_backups", "pagefind", "templates", ".claude"}
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding="utf-8")
        orig = text
        # Pass 1: encode every old letter ref as temp token
        for old, new in forward.items():
            # Appendix <letter> followed by word boundary
            text = re.sub(rf"\bAppendix\s+{old}\b",
                           f"Appendix §{old}§", text)
            # Captions: Code Fragment X.Y.Z / Figure / Table / Pseudocode
            for kind in ("Code Fragment", "Figure", "Table", "Pseudocode"):
                text = re.sub(rf"\b{kind}\s+{old}\.(\d+(?:\.\d+)?)\b",
                               rf"{kind} §{old}§.\1", text)
            # Section X.Y
            text = re.sub(rf"\bSection\s+{old}\.(\d+(?:\.\d+)?)\b",
                           rf"Section §{old}§.\1", text)
            # href paths: appendix-x-slug/
            text = re.sub(rf"appendix-{old.lower()}-",
                           f"appendix-§{old}§-", text)
            # section-x.Y.html
            text = re.sub(rf"section-{old.lower()}\.(\d+(?:\.\d+)?)\.html",
                           rf"section-§{old}§.\1.html", text)
        # Pass 2: temp -> new
        for old, new in forward.items():
            text = text.replace(f"§{old}§", new)
            text = text.replace(f"§{old}§-", f"{new.lower()}-")
            # Lower-case the temp token for paths
            text = text.replace(f"appendix-{new}-", f"appendix-{new.lower()}-")
            text = text.replace(f"section-{new}.", f"section-{new.lower()}.")
        if text != orig:
            n_files += 1
            if not dry_run:
                p.write_text(text, encoding="utf-8")
    return n_files


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply

    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"=== {mode}: Drop appendices G, H, I ===")
    for letter, slug in DROPS:
        drop_appendix(letter, slug, dry_run)

    print(f"\n=== {mode}: Rename remaining 13 appendices (temp -> final) ===")
    # Phase A: old -> temp
    for old, new, slug in RENAMES:
        rename_appendix(old, new, slug, dry_run, temp=True)
    # Phase B: temp -> final
    for old, new, slug in RENAMES:
        rename_appendix(old, new, slug, dry_run, temp=False)

    print(f"\n=== {mode}: Book-wide appendix-ref rewrite ===")
    n = update_internal_refs(dry_run)
    print(f"  {n} files updated")

    return 0


if __name__ == "__main__":
    sys.exit(main())
