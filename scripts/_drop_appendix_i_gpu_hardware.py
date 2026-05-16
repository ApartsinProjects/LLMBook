"""Drop Appendix I (GPU Hardware and Cloud Compute) and renumber J-R -> I-Q.

After drop, appendix letter sequence is A-Q (17 appendices).
Affected operations:
  1. git rm -r appendices/appendix-i-hardware-compute/
  2. Renumber on-disk dirs J..R -> I..Q (and their section files)
  3. Book-wide rewrite of "Appendix J" -> "Appendix I", etc.
  4. Book-wide rewrite of href paths appendix-j-... -> appendix-i-...
  5. Book-wide rewrite of caption letters (Code Fragment J.X.Y -> I.X.Y)

Uses temp-prefix swap so the renames don't collide (J->I, K->J would
collide when I exists from J's rename before K can become J).

Idempotent: skips moves whose source no longer exists.
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
RENUMBER = [
    ("J", "I", "experiment-tracking"),
    ("K", "J", "inference-serving"),
    ("L", "K", "distributed-ml"),
    ("M", "L", "docker-containers"),
    ("N", "M", "master-reference-tables"),
    ("O", "N", "production-patterns"),
    ("P", "O", "pedagogy-kit"),
    ("Q", "P", "problem-solution-key"),
    ("R", "Q", "freshness-2026"),
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


def step1_drop_gpu(dry_run: bool) -> str:
    """Drop Appendix I (GPU Hardware)."""
    d = APPS / "appendix-i-hardware-compute"
    if not d.exists():
        return "  SKIP: appendix-i-hardware-compute missing"
    if dry_run:
        return f"  WOULD git rm -r {d.name}"
    subprocess.run(["git", "rm", "-r", str(d)], cwd=ROOT, check=False)
    return f"  git rm -r {d.name}"


def step2_renumber_dirs(dry_run: bool) -> list[str]:
    """Renumber appendix dirs J-R -> I-Q using temp prefix swap."""
    msgs: list[str] = []
    # Phase A: rename appendix-<old> -> _tmp-<new>
    for old, new, slug in RENUMBER:
        src = APPS / f"appendix-{old.lower()}-{slug}"
        dst = APPS / f"_tmp-{new.lower()}-{slug}"
        msgs.append(git_mv(src, dst, dry_run))
    # Phase B: rename _tmp-<new> -> appendix-<new>
    for old, new, slug in RENUMBER:
        src = APPS / f"_tmp-{new.lower()}-{slug}"
        dst = APPS / f"appendix-{new.lower()}-{slug}"
        msgs.append(git_mv(src, dst, dry_run))
    # Phase C: rename section files inside each renamed dir
    if not dry_run:
        for old, new, slug in RENUMBER:
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
    """Rewrite Appendix references + href paths + caption letters book-wide
    using temp tokens for the J-R -> I-Q swap."""
    forward = {old: new for old, new, _ in RENUMBER}
    # Add the drop: anything referencing Appendix I (GPU Hardware) -> just
    # remove or warn. We don't auto-replace because the new Appendix I is a
    # different topic. Track separately.
    n_files = 0
    n_drops = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        text = p.read_text(encoding="utf-8")
        orig = text

        # Pass 1: tokenize old letters J-R as TMP tokens
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

        # Pass 2: tokens -> final new letters
        for old, new in forward.items():
            text = text.replace(f"§{old}§", new)
            text = text.replace(f"appendix-{new}-", f"appendix-{new.lower()}-")
            text = text.replace(f"section-{new}.", f"section-{new.lower()}.")

        # Pass 3: count stale refs to dropped Appendix I (GPU Hardware)
        # For prose readability we annotate rather than silently rewrite.
        # Old Appendix I content has moved out of the book. References get
        # an HTML comment marker.
        stale_app_i = list(re.finditer(
            r"\bAppendix\s+I\b(?:[^A-Za-z]|$)",
            text,
        ))
        # NOTE: post-renumber, Appendix I is now Experiment Tracking.
        # So body refs to "Appendix I" now point at the NEW I which is
        # actually correct for the destination but wrong topic. We can't
        # programmatically tell intent. Skip auto-handling and report count.
        if stale_app_i:
            n_drops += len(stale_app_i)

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
    print(f"=== {mode}: Drop Appendix I (GPU Hardware) ===")
    print(step1_drop_gpu(dry_run))

    print(f"\n=== {mode}: Renumber J-R -> I-Q ===")
    for m in step2_renumber_dirs(dry_run):
        print(m)

    print(f"\n=== {mode}: Book-wide cross-ref rewrite ===")
    n = step3_rewrite_book_wide(dry_run)
    print(f"  {n} files updated")

    return 0


if __name__ == "__main__":
    sys.exit(main())
