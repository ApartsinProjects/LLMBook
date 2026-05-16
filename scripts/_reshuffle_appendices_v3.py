"""Third appendix reshuffle: move Env Setup from Dev Setup -> Production Infra
(group dissolves), keep Python in Foundations, shift Framework Guides up,
rename Pedagogical Kit -> For Instructors. Final 5-group structure.

Mapping (current_letter -> new_letter):
  A -> A   Math                         (Foundations)
  B -> B   ML Essentials                (Foundations)
  C -> C   Python                       (Foundations)  -- promoted
  D -> G   Env Setup                    (Production Infra) -- moved
  E -> D   HuggingFace                  (Framework Guides) -- shift up
  F -> E   LangChain                    (Framework Guides) -- shift up
  G -> F   Tooling Ecosystem            (Framework Guides) -- shift up
  H -> H   Git/DVC                      (Production Infra) -- no change
  I -> I   Experiments                  (Production Infra) -- regrouped
  J -> J   Inference                    (Production Infra) -- no change
  K -> K   Distributed                  (Production Infra) -- no change
  L -> L   Docker                       (Production Infra) -- no change
  M -> M   Master Tables                (Cross-Cutting Reference) -- no change
  N -> N   Problem-Solution Key         (Cross-Cutting Reference) -- no change
  O -> O   Pedagogy Kit                 (For Instructors) -- regrouped
  P -> P   Freshness 2026               (For Instructors) -- regrouped

Only structural renames: D->G, E->D, F->E, G->F (4 swaps via temp prefix).
"""
from __future__ import annotations
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPS = ROOT / "appendices"
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude"}

RENAMES = [
    ("D", "G", "environment-setup"),
    ("E", "D", "huggingface-ecosystem"),
    ("F", "E", "langchain"),
    ("G", "F", "tooling-ecosystem"),
]


def git_mv(src: Path, dst: Path, dry_run: bool) -> str:
    if not src.exists():
        return f"  SKIP: {src.name} missing"
    if dst.exists():
        return f"  SKIP: {dst.name} exists"
    if dry_run:
        return f"  WOULD git mv {src.name} -> {dst.name}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "mv", str(src), str(dst)], cwd=ROOT, check=False)
    return f"  git mv {src.name} -> {dst.name}"


def step1_renames(dry_run: bool) -> list[str]:
    msgs: list[str] = []
    for old, new, slug in RENAMES:
        src = APPS / f"appendix-{old.lower()}-{slug}"
        dst = APPS / f"_tmp-{new.lower()}-{slug}"
        msgs.append(git_mv(src, dst, dry_run))
    for old, new, slug in RENAMES:
        src = APPS / f"_tmp-{new.lower()}-{slug}"
        dst = APPS / f"appendix-{new.lower()}-{slug}"
        msgs.append(git_mv(src, dst, dry_run))
    if not dry_run:
        for old, new, slug in RENAMES:
            d = APPS / f"appendix-{new.lower()}-{slug}"
            if not d.exists():
                continue
            for sec in sorted(d.glob(f"section-{old.lower()}.*.html")):
                new_name = sec.name.replace(
                    f"section-{old.lower()}.", f"section-{new.lower()}.")
                new_path = sec.parent / new_name
                if new_path == sec or new_path.exists():
                    continue
                subprocess.run(["git", "mv", str(sec), str(new_path)],
                                cwd=ROOT, check=False)
                msgs.append(f"  section {sec.name} -> {new_name}")
    return msgs


def step2_book_wide(dry_run: bool) -> int:
    forward = {old: new for old, new, _ in RENAMES}
    n_files = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        text = p.read_text(encoding="utf-8")
        orig = text
        for old, new in forward.items():
            text = re.sub(rf"\bAppendix\s+{old}\b",
                           f"Appendix §{old}§", text)
            for kind in ("Code Fragment", "Figure", "Table", "Pseudocode"):
                text = re.sub(rf"\b{kind}\s+{old}\.(\d+(?:\.\d+)?)\b",
                               rf"{kind} §{old}§.\1", text)
            text = re.sub(rf"\bSection\s+{old}\.(\d+(?:\.\d+)?)\b",
                           rf"Section §{old}§.\1", text)
            text = re.sub(rf"appendix-{old.lower()}-",
                           f"appendix-§{old}§-", text)
            text = re.sub(rf"section-{old.lower()}\.(\d+(?:\.\d+)?)\.html",
                           rf"section-§{old}§.\1.html", text)
        for old, new in forward.items():
            text = text.replace(f"§{old}§", new)
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
    print(f"=== {mode}: Renames (D-G-E-F swap) ===")
    for m in step1_renames(dry_run):
        print(m)
    print(f"\n=== {mode}: Book-wide rewrite ===")
    print(f"  {step2_book_wide(dry_run)} files updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
