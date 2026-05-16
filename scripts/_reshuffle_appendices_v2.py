"""Second appendix reshuffle: drop Production Patterns Reference, move Git
to MLOps, move Master Tables + Problem-Solution Key to Cross-Cutting
Reference. Resulting structure has 16 appendices A-P organized into 6
thematic groups.

Mapping (old_letter -> new_letter):
    A -> A   (Math)              [no change]
    B -> B   (ML)                [no change]
    C -> C   (Python)            [no change]
    D -> D   (Env Setup)         [no change]
    E -> H   (Git/DVC)           [Development Setup -> MLOps]
    F -> E   (HuggingFace)       [shift up]
    G -> F   (LangChain)         [shift up]
    H -> G   (Tooling Ecosystem) [shift up]
    I -> I   (Experiments)       [no change in letter, group shift]
    J -> J   (Inference)         [no change]
    K -> K   (Distributed)       [no change]
    L -> L   (Docker)            [no change]
    M -> M   (Master Tables)     [no change in letter, group: Cross-Cutting Ref]
    N        (Production Patterns Reference) -- DROPPED
    O -> O   (Pedagogy Kit)      [no change]
    P -> N   (Problem-Solution Key) [shift up, group: Cross-Cutting Ref]
    Q -> P   (Freshness 2026)    [shift up]

Cross-cutting renames require temp-prefix swap to avoid collisions
(E -> H requires H to be free first, etc.).
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

# (old_letter, new_letter, slug)
RENAMES = [
    ("E", "H", "git-collaboration"),
    ("F", "E", "huggingface-ecosystem"),
    ("G", "F", "langchain"),
    ("H", "G", "tooling-ecosystem"),
    ("P", "N", "problem-solution-key"),
    ("Q", "P", "freshness-2026"),
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


def step1_drop_production_patterns(dry_run: bool) -> str:
    d = APPS / "appendix-n-production-patterns"
    if not d.exists():
        return f"  SKIP: {d.name} missing"
    if dry_run:
        return f"  WOULD git rm -r {d.name}"
    subprocess.run(["git", "rm", "-r", str(d)], cwd=ROOT, check=False)
    return f"  git rm -r {d.name}"


def step2_rename_dirs(dry_run: bool) -> list[str]:
    msgs: list[str] = []
    # Phase A: appendix-<old> -> _tmp-<new>
    for old, new, slug in RENAMES:
        src = APPS / f"appendix-{old.lower()}-{slug}"
        dst = APPS / f"_tmp-{new.lower()}-{slug}"
        msgs.append(git_mv(src, dst, dry_run))
    # Phase B: _tmp-<new> -> appendix-<new>
    for old, new, slug in RENAMES:
        src = APPS / f"_tmp-{new.lower()}-{slug}"
        dst = APPS / f"appendix-{new.lower()}-{slug}"
        msgs.append(git_mv(src, dst, dry_run))
    # Phase C: rename section files inside
    if not dry_run:
        for old, new, slug in RENAMES:
            d = APPS / f"appendix-{new.lower()}-{slug}"
            if not d.exists():
                continue
            for sec_file in sorted(d.glob(f"section-{old.lower()}.*.html")):
                new_name = sec_file.name.replace(
                    f"section-{old.lower()}.", f"section-{new.lower()}.")
                new_path = sec_file.parent / new_name
                if new_path == sec_file or new_path.exists():
                    continue
                subprocess.run(["git", "mv", str(sec_file), str(new_path)],
                                cwd=ROOT, check=False)
                msgs.append(f"  section {sec_file.name} -> {new_name}")
    return msgs


def step3_rewrite_book_wide(dry_run: bool) -> int:
    """Rewrite all references using two-pass temp tokens to avoid cascading."""
    forward = {old: new for old, new, _ in RENAMES}
    n_files = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        text = p.read_text(encoding="utf-8")
        orig = text

        # Pass 1: tokenize old letters as TMP markers
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

        # Pass 2: TMP tokens -> final new letters
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
    print(f"=== {mode}: Drop Production Patterns Reference ===")
    print(step1_drop_production_patterns(dry_run))

    print(f"\n=== {mode}: Renames (temp-swap) ===")
    for m in step2_rename_dirs(dry_run):
        print(m)

    print(f"\n=== {mode}: Book-wide cross-ref rewrite ===")
    n = step3_rewrite_book_wide(dry_run)
    print(f"  {n} files updated")

    return 0


if __name__ == "__main__":
    sys.exit(main())
