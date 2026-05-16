"""Split LLM Tooling Ecosystem (Appendix F) into individual library guides.

Current F:
  F.1 The LLM Tooling Landscape (intro/landscape)
  F.2 Orchestration Frameworks (LangChain, LlamaIndex, Haystack, DSPy)
  F.3 Agent Frameworks (LangGraph, CrewAI, AutoGen, Semantic Kernel, etc.)

Plan:
  - Drop the F.1 "Landscape" intro (it duplicates LangChain + HF prose);
    its content can be summarized in the new appendix indexes.
  - Promote F.2 to its own appendix:
      appendix-f-orchestration-frameworks/section-f.X.html
  - Promote F.3 to its own appendix:
      appendix-g-agent-frameworks/section-g.X.html
  - Shift everything from G onward up by 1 letter:
      G Env Setup -> H
      H Git/DVC -> I
      I Experiments -> J
      J Inference -> K
      K Distributed -> L
      L Docker -> M
      M Master Tables -> N
      N Problem-Solution Key -> O
      O Pedagogy Kit -> P
      P Freshness 2026 -> Q

Net: 17 appendices A-Q (was 16). Tooling Ecosystem (3 sections) becomes
2 separate appendices (Orchestration + Agent Frameworks), with the
Landscape intro folded into LangChain (E) or dropped.
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

# Phase 1: shift G-P -> H-Q (free up F + G for split)
SHIFTS = [
    ("G", "H", "environment-setup"),
    ("H", "I", "git-collaboration"),
    ("I", "J", "experiment-tracking"),
    ("J", "K", "inference-serving"),
    ("K", "L", "distributed-ml"),
    ("L", "M", "docker-containers"),
    ("M", "N", "master-reference-tables"),
    ("N", "O", "problem-solution-key"),
    ("O", "P", "pedagogy-kit"),
    ("P", "Q", "freshness-2026"),
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


def step1_shift_g_to_p(dry_run: bool) -> list[str]:
    """Shift G-P -> H-Q via temp prefix swap."""
    msgs: list[str] = []
    for old, new, slug in SHIFTS:
        src = APPS / f"appendix-{old.lower()}-{slug}"
        dst = APPS / f"_tmp-{new.lower()}-{slug}"
        msgs.append(git_mv(src, dst, dry_run))
    for old, new, slug in SHIFTS:
        src = APPS / f"_tmp-{new.lower()}-{slug}"
        dst = APPS / f"appendix-{new.lower()}-{slug}"
        msgs.append(git_mv(src, dst, dry_run))
    if not dry_run:
        for old, new, slug in SHIFTS:
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


def step2_split_tooling(dry_run: bool) -> list[str]:
    """Split appendix-f-tooling-ecosystem into F (Orchestration) and G
    (Agent Frameworks). Drop F.1 (Landscape) by deleting; the content
    is repeated in the index pages of D (HF) and E (LangChain)."""
    msgs: list[str] = []
    src_dir = APPS / "appendix-f-tooling-ecosystem"
    if not src_dir.exists():
        return ["  SKIP: appendix-f-tooling-ecosystem missing"]

    # Create new dirs
    new_f = APPS / "appendix-f-orchestration-frameworks"
    new_g = APPS / "appendix-g-agent-frameworks"

    if not dry_run:
        new_f.mkdir(exist_ok=True)
        (new_f / "images").mkdir(exist_ok=True)
        new_g.mkdir(exist_ok=True)
        (new_g / "images").mkdir(exist_ok=True)

    # Move F.2 -> new F.1
    src_f2 = src_dir / "section-f.2.html"
    dst_f1 = new_f / "section-f.1.html"
    msgs.append(git_mv(src_f2, dst_f1, dry_run))

    # Move F.3 -> new G.1
    src_f3 = src_dir / "section-f.3.html"
    dst_g1 = new_g / "section-g.1.html"
    msgs.append(git_mv(src_f3, dst_g1, dry_run))

    # Drop F.1 Landscape (content duplicates LangChain/HF intros)
    src_f1 = src_dir / "section-f.1.html"
    if src_f1.exists():
        if dry_run:
            msgs.append(f"  WOULD git rm {src_f1.name}")
        else:
            subprocess.run(["git", "rm", str(src_f1)], cwd=ROOT, check=False)
            msgs.append(f"  git rm {src_f1.name}")

    # Move old index.html to new F (Orchestration) — author can tune later
    src_idx = src_dir / "index.html"
    new_f_idx = new_f / "index.html"
    if src_idx.exists() and not new_f_idx.exists():
        if dry_run:
            msgs.append(f"  WOULD git mv {src_dir.name}/index.html -> {new_f.name}/index.html")
        else:
            subprocess.run(["git", "mv", str(src_idx), str(new_f_idx)],
                            cwd=ROOT, check=False)
            # Update title in new index
            text = new_f_idx.read_text(encoding="utf-8")
            text = re.sub(r"<title>[^<]+</title>",
                           "<title>Appendix F: Orchestration Frameworks | Building Conversational AI with LLMs and Agents</title>",
                           text, count=1)
            text = re.sub(r"<h1[^>]*>[^<]+</h1>",
                           "<h1>Orchestration Frameworks</h1>",
                           text, count=1)
            new_f_idx.write_text(text, encoding="utf-8")
            msgs.append(f"  moved index.html + retitled to 'Orchestration Frameworks'")

    # Create minimal index.html for new G (Agent Frameworks)
    if not dry_run:
        new_g_idx = new_g / "index.html"
        if not new_g_idx.exists():
            new_g_idx.write_text(
                '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
                '<meta charset="utf-8"/>\n'
                '<title>Appendix G: Agent Frameworks | Building Conversational AI with LLMs and Agents</title>\n'
                '<link href="../../styles/book.css" rel="stylesheet"/>\n'
                '</head>\n<body>\n'
                '<header class="chapter-header">\n'
                '<nav class="header-nav">\n'
                '<a class="book-title-link" href="../../index.html">Building Conversational AI with LLMs and Agents</a>\n'
                '<a class="toc-link" href="../../toc.html">Contents</a></nav>\n'
                '<div class="header-search"><div id="search"></div></div>\n'
                '<div class="page-breadcrumb" data-pagefind-meta="chapter">'
                '<a href="../index.html">Appendices</a>'
                '<span class="bc-sep">›</span>'
                '<span class="bc-current">Appendix G</span></div>\n'
                '<h1>Agent Frameworks</h1>\n'
                '<p class="chapter-subtitle">LangGraph, CrewAI, AutoGen, OpenAI Agents SDK, Semantic Kernel, smolagents, PydanticAI.</p>\n'
                '</header>\n<main class="content">\n'
                '<p>This appendix surveys the major agent-orchestration frameworks of 2026, with installation, basic agent loop, tool integration, and a short comparative perspective for each.</p>\n'
                '</main></body></html>',
                encoding="utf-8")
            msgs.append(f"  created {new_g.name}/index.html")

        # Remove empty old tooling-ecosystem dir
        try:
            for leftover in src_dir.iterdir():
                lo_dst = new_f / leftover.name
                if not lo_dst.exists():
                    subprocess.run(["git", "mv", str(leftover), str(lo_dst)],
                                    cwd=ROOT, check=False)
            src_dir.rmdir()
            msgs.append(f"  Removed empty {src_dir.name}")
        except OSError:
            pass

    return msgs


def step3_book_wide(dry_run: bool) -> int:
    """Rewrite cross-refs G-P -> H-Q. F stays in place (split internally)."""
    forward = {old: new for old, new, _ in SHIFTS}
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
    print(f"=== {mode}: Shift G-P -> H-Q ===")
    for m in step1_shift_g_to_p(dry_run):
        print(m)
    print(f"\n=== {mode}: Split Tooling Ecosystem -> F (Orchestration) + G (Agent Frameworks) ===")
    for m in step2_split_tooling(dry_run):
        print(m)
    print(f"\n=== {mode}: Book-wide rewrite ===")
    print(f"  {step3_book_wide(dry_run)} files updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
