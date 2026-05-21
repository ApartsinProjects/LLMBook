"""V11: Drop Appendix G (Problem-Solution Key). Cascade H-U up to G-T.

Final 20-appendix structure A-T in 5 groups (was 21 A-U in v10):
  Foundations               A Math, B ML
  Framework Guides          C HF, D LangChain, E Orchestration, F Agents
                            (was 5; now 4 after G drop)
  R&D Infrastructure        G Python, H Env Setup, I Git/DVC, J Experiments
                            (was H-K; cascaded down 1)
  Production Infrastructure K Inference, L Data Eng, M Distributed ML,
                            N MLOps, O Docker
                            (was L-P; cascaded down 1)
  For Instructors           P Syllabi, Q Pathways, R Projects,
                            S Capstone, T War Stories
                            (was Q-U; cascaded down 1)

Letter cascade (current -> new):
  H Python      -> G
  I Env Setup   -> H
  J Git/DVC     -> I
  K Experiments -> J
  L Inference   -> K
  M Data Eng    -> L
  N Distributed -> M
  O MLOps       -> N
  P Docker      -> O
  Q Syllabi     -> P
  R Pathways    -> Q
  S Projects    -> R
  T Capstone    -> S
  U War Stories -> T

Idempotent. Run with --apply.
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
              ".claude", ".book-update"}

# Cascade (old letter -> new letter, slug)
RENAMES = [
    ("H", "G", "python-for-llm"),
    ("I", "H", "environment-setup"),
    ("J", "I", "git-collaboration"),
    ("K", "J", "experiment-tracking"),
    ("L", "K", "inference-serving"),
    ("M", "L", "data-engineering"),
    ("N", "M", "distributed-ml"),
    ("O", "N", "mlops"),
    ("P", "O", "docker-containers"),
    ("Q", "P", "course-syllabi"),
    ("R", "Q", "reading-pathways"),
    ("S", "R", "intermediate-projects"),
    ("T", "S", "capstone-project"),
    ("U", "T", "war-stories"),
]

DROP_DIR = "appendix-g-problem-solution-key"


def git_op(args: list[str], dry_run: bool) -> tuple[int, str]:
    if dry_run:
        return 0, ""
    res = subprocess.run(["git"] + args, cwd=ROOT, capture_output=True, text=True)
    return res.returncode, res.stdout + res.stderr


def step1_drop_g(dry_run: bool) -> str:
    p = APPS / DROP_DIR
    if not p.exists():
        return f"  SKIP: {DROP_DIR} missing"
    if dry_run:
        return f"  WOULD git rm -r {DROP_DIR}"
    rc, out = git_op(["rm", "-rf", str(p)], dry_run)
    return f"  git rm -r {DROP_DIR}" if rc == 0 else f"  FAIL: {out.strip()}"


def step2_renames(dry_run: bool) -> list[str]:
    msgs: list[str] = []
    # Pass A: rename to temp
    for old, new, slug in RENAMES:
        src = APPS / f"appendix-{old.lower()}-{slug}"
        dst = APPS / f"_tmp11-{new.lower()}-{slug}"
        if not src.exists():
            msgs.append(f"  SKIP: {src.name} missing")
            continue
        if dry_run:
            msgs.append(f"  WOULD git mv {src.name} -> {dst.name}")
        else:
            git_op(["mv", str(src), str(dst)], dry_run)
            msgs.append(f"  git mv {src.name} -> {dst.name}")
    # Pass B: temp -> final
    for old, new, slug in RENAMES:
        src = APPS / f"_tmp11-{new.lower()}-{slug}"
        dst = APPS / f"appendix-{new.lower()}-{slug}"
        if not src.exists():
            continue
        if dry_run:
            msgs.append(f"  WOULD git mv {src.name} -> {dst.name}")
        else:
            git_op(["mv", str(src), str(dst)], dry_run)
            msgs.append(f"  git mv {src.name} -> {dst.name}")
    # Rename section files inside each renamed appendix
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


def step3_strip_g_refs_and_rewrite(dry_run: bool) -> int:
    """Strip all <a> wrappers pointing to dropped appendix-g-problem-solution-key
    (keep inner text), then rewrite Appendix letter refs via § markers."""
    forward = {old: new for old, new, _ in RENAMES}

    n_files = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        text = p.read_text(encoding="utf-8")
        orig = text

        # 1. Strip <a> wrappers pointing to dropped appendix-g
        text = re.sub(
            r'<a\s+[^>]*href="[^"]*appendix-g-problem-solution-key[^"]*"[^>]*>'
            r'([^<]*)</a>',
            r'\1',
            text,
        )

        # 2. Letter cascade via § markers
        for old in forward:
            text = re.sub(rf"\bAppendix\s+{old}\b",
                           f"Appendix §{old}§", text)
            for kind in ("Code Fragment", "Figure", "Table", "Pseudocode",
                          "Listing"):
                text = re.sub(rf"\b{kind}\s+{old}\.(\d+(?:\.\d+)?)\b",
                               rf"{kind} §{old}§.\1", text)
            text = re.sub(rf"\bSection\s+{old}\.(\d+(?:\.\d+)?)\b",
                           rf"Section §{old}§.\1", text)
            text = re.sub(rf"appendix-{old.lower()}-",
                           f"appendix-§{old}§-", text)
            text = re.sub(rf"section-{old.lower()}\.(\d+(?:\.\d+)?)\.html",
                           rf"section-§{old}§.\1.html", text)
            text = re.sub(rf"section-{old.lower()}\.(\d+(?:\.\d+)?)#",
                           rf"section-§{old}§.\1#", text)
        for old, new in forward.items():
            text = text.replace(f"§{old}§", new)
        for old, new in forward.items():
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

    print(f"=== {mode}: Step 1 - Drop Appendix G ===")
    print(step1_drop_g(dry_run))
    print(f"\n=== {mode}: Step 2 - Cascade H-U -> G-T ===")
    for m in step2_renames(dry_run):
        print(m)
    print(f"\n=== {mode}: Step 3 - Book-wide cross-ref rewrite ===")
    n = step3_strip_g_refs_and_rewrite(dry_run)
    print(f"  {n} files updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
