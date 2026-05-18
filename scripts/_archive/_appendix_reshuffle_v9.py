"""V9 reshuffle: drop Cross-Cutting References group + Glossary.

Drops:
  - Appendix N (Master Reference Tables) -- content can live in chapters
  - Appendix P (2026 Freshness Index)    -- date-sensitive, redundant
  - Glossary (5 sections + index)        -- search replaces lookup;
    all <a class="glossary-link"> wrappers are stripped book-wide

Moves:
  - O (Problem-Solution Key) -> G (joins Framework Guides)

Letter shifts after drops + O->G:
  G Python      -> H
  H Env Setup   -> I
  I Git/DVC     -> J
  J Experiments -> K
  K Inference   -> L
  L Distributed -> M
  M Docker      -> N
  Q Syllabi     -> O
  R Pathways    -> P
  S Projects    -> Q
  T Capstone    -> R
  U War Stories -> S

Final 19-appendix structure A-S in 5 groups:
  Foundations               A Math, B ML
  Framework Guides          C HF, D LangChain, E Orchestration,
                            F Agents, G Problem-Solution Key
  R&D Infrastructure        H Python, I Env Setup, J Git/DVC, K Experiments
  Production Infrastructure L Inference, M Distributed, N Docker
  For Instructors           O Syllabi, P Pathways, Q Projects,
                            R Capstone, S War Stories

Idempotent. Run once with --apply.
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

# Renames (old letter -> new letter, slug)
# O->G done FIRST (since G is being vacated by Python -> H below)
RENAMES = [
    ("O", "G", "problem-solution-key"),
    ("G", "H", "python-for-llm"),
    ("H", "I", "environment-setup"),
    ("I", "J", "git-collaboration"),
    ("J", "K", "experiment-tracking"),
    ("K", "L", "inference-serving"),
    ("L", "M", "distributed-ml"),
    ("M", "N", "docker-containers"),
    ("Q", "O", "course-syllabi"),
    ("R", "P", "reading-pathways"),
    ("S", "Q", "intermediate-projects"),
    ("T", "R", "capstone-project"),
    ("U", "S", "war-stories"),
]

DROP_DIRS = [
    "appendix-n-master-reference-tables",
    "appendix-p-freshness-2026",
    "glossary",
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


def step1_drop(dry_run: bool) -> list[str]:
    msgs: list[str] = []
    for d in DROP_DIRS:
        p = APPS / d
        if not p.exists():
            msgs.append(f"  SKIP: {d} missing")
            continue
        if dry_run:
            msgs.append(f"  WOULD git rm -r {d}")
        else:
            subprocess.run(["git", "rm", "-rf", str(p)],
                            cwd=ROOT, check=False, capture_output=True)
            msgs.append(f"  git rm -r {d}")
    return msgs


def step2_renames(dry_run: bool) -> list[str]:
    msgs: list[str] = []
    # Pass A: move all to temp prefix
    for old, new, slug in RENAMES:
        src = APPS / f"appendix-{old.lower()}-{slug}"
        dst = APPS / f"_tmp9-{new.lower()}-{slug}"
        msgs.append(git_mv(src, dst, dry_run))
    # Pass B: move temp -> final
    for old, new, slug in RENAMES:
        src = APPS / f"_tmp9-{new.lower()}-{slug}"
        dst = APPS / f"appendix-{new.lower()}-{slug}"
        msgs.append(git_mv(src, dst, dry_run))
    # Rename section files inside each appendix
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


def step3_strip_glossary_links_and_rewrite_refs(dry_run: bool) -> int:
    """One book-wide pass:
    1. Strip <a class="glossary-link" ...>TEXT</a> -> TEXT
    2. Rewrite Appendix letter refs via § markers
    3. Drop dead links to appendix-n-master-reference-tables /
       appendix-p-freshness-2026 / glossary/ (replace with plain text)
    """
    forward = {old: new for old, new, _ in RENAMES}
    n_files = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        text = p.read_text(encoding="utf-8")
        orig = text

        # 1. Strip glossary-link <a> wrappers (preserve inner text)
        text = re.sub(
            r'<a\s+class="glossary-link"[^>]*>([^<]*)</a>',
            r'\1',
            text,
        )

        # 2. Rewrite dead appendix links (Master Tables, Freshness, Glossary)
        #    -> point to appendices index for now; author can re-route
        for dead in ("appendix-n-master-reference-tables",
                      "appendix-p-freshness-2026"):
            # In-page hrefs to dead appendices: drop the <a> wrapper
            text = re.sub(
                rf'<a\s+[^>]*href="[^"]*{re.escape(dead)}[^"]*"[^>]*>'
                rf'([^<]*)</a>',
                r'\1',
                text,
            )
        # Glossary refs already stripped via class="glossary-link"; catch
        # any remaining via href pattern
        text = re.sub(
            r'<a\s+[^>]*href="[^"]*glossary/[^"]*"[^>]*>([^<]*)</a>',
            r'\1',
            text,
        )

        # 3. Letter renames via § markers (avoid double substitution)
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

    print(f"=== {mode}: Step 1 - Drop N, P, Glossary ===")
    for m in step1_drop(dry_run):
        print(m)

    print(f"\n=== {mode}: Step 2 - Letter renames ===")
    for m in step2_renames(dry_run):
        print(m)

    print(f"\n=== {mode}: Step 3 - Strip glossary links + rewrite refs ===")
    n = step3_strip_glossary_links_and_rewrite_refs(dry_run)
    print(f"  {n} files updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
