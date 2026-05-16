"""Class D scaffolding fixes:
  (1) Add `<div class="callout big-picture">` to Ch 0-6 where missing.
  (2) Reorder Prereqs <-> Objectives so Objectives comes first (canonical order).

Idempotent: re-runnable; will skip chapters that already have the fix.

Run from project root:
    python scripts/_fix_class_d_scaffolding.py [--dry-run]
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]


# Big Picture content per chapter. Each value is the BODY HTML to wrap in the
# callout (without the outer .callout big-picture div + title).
BIG_PICTURE_TEXTS = {
    "module-00-ml-pytorch-foundations":
        "PyTorch is the lingua franca of modern LLM engineering. Nearly every "
        "model you will use in this book was trained in it, every fine-tuning "
        "library wraps it, and every production inference server can ingest its "
        "checkpoints. This chapter brings classical ML and PyTorch under one "
        "roof so that subsequent chapters can focus on what makes LLMs different "
        "rather than re-explaining backpropagation. The investment pays off "
        "across every Part that follows.",

    "module-01-foundations-nlp-text-representation":
        "Every LLM is built on top of representations of text: how you turn "
        "words into numbers determines what the model can learn. This chapter "
        "traces the path from one-hot vectors through word embeddings to "
        "contextual representations, the conceptual ancestors of the transformer "
        "attention mechanism in Chapter 3. Understanding why these representations "
        "evolved as they did is the fastest way to build intuition for everything "
        "that follows.",

    "module-02-tokenization-subword-models":
        "Tokenization is the seam between raw text and the model. Get it wrong "
        "and the model wastes capacity on common words, struggles with code, or "
        "chokes on non-English languages. This chapter covers BPE, WordPiece, "
        "and SentencePiece, the subword algorithms behind every modern LLM, "
        "and gives you the mental model you need to debug tokenization issues "
        "when they surface in production.",

    "module-03-sequence-models-attention":
        "Attention solves the problem that ended the RNN era: how to let any "
        "position in a sequence look at any other position without paying linear "
        "cost in the path length. This chapter builds attention from scratch, "
        "starting from the failures of LSTMs and arriving at scaled dot-product "
        "attention. Once attention clicks, the transformer architecture in "
        "Chapter 4 becomes a small step rather than a leap.",

    "module-04-transformer-architecture":
        "The transformer is the architecture every chapter after this assumes "
        "you understand. We build it from the ground up: token to embedding, "
        "attention, residual plus LayerNorm, feed-forward, repeat. By the end "
        "of the chapter you can sketch a 300-line decoder-only transformer "
        "from memory and reason about its memory and compute budget.",

    "module-05-decoding-text-generation":
        "A trained transformer is a probability distribution over the next "
        "token; turning that into useful text requires a decoding strategy. "
        "This chapter covers greedy, beam, top-k, nucleus, and structured "
        "decoding, plus the diffusion-language-model approach that has begun "
        "challenging autoregressive generation. The decoding choices you make "
        "at inference are often as impactful as fine-tuning.",

    "module-06-pretraining-scaling-laws":
        "Pretraining is where the foundation model actually gets built. This "
        "chapter walks through the data, objectives, scaling laws, and "
        "distributed-training systems that make a frontier model possible. "
        "Most readers will never pretrain from scratch, but understanding what "
        "happens during pretraining is the prerequisite for every downstream "
        "decision: which fine-tuning method to choose, why certain failure "
        "modes exist, how to plan compute budgets.",
}


CHAPTER_DIRS_FOR_REORDER = [
    "module-00-ml-pytorch-foundations",
    "module-01-foundations-nlp-text-representation",
    "module-02-tokenization-subword-models",
    "module-03-sequence-models-attention",
    "module-04-transformer-architecture",
    "module-05-decoding-text-generation",
    "module-06-pretraining-scaling-laws",
    "module-07-modern-llm-landscape",
    "module-08-reasoning-test-time-compute",
    "module-09-inference-optimization",
    "module-10-interpretability",
]


def find_chapter_index(module_name: str) -> Path | None:
    for p in ROOT.rglob(f"{module_name}/index.html"):
        return p
    return None


def add_big_picture(soup: BeautifulSoup, body_text: str) -> bool:
    """Insert a Big Picture callout after the overview block. Skip if already present."""
    if soup.find("div", class_="big-picture"):
        return False
    # Find the .overview div (Chapter Overview section)
    overview = soup.find("div", class_="overview")
    if not overview:
        return False
    # Build the callout
    callout = soup.new_tag("div")
    callout["class"] = ["callout", "big-picture"]
    title = soup.new_tag("div")
    title["class"] = ["callout-title"]
    title.string = "Big Picture"
    callout.append(title)
    p = soup.new_tag("p")
    p.string = body_text
    callout.append(p)
    overview.insert_after(callout)
    return True


def reorder_prereqs_objectives(soup: BeautifulSoup) -> bool:
    """Move objectives BEFORE prereqs if currently inverted."""
    obj = soup.find("div", class_="objectives") or soup.find("div", class_="learning-objectives")
    pre = soup.find("div", class_="prereqs") or soup.find("div", class_="prerequisites")
    if not obj or not pre:
        return False
    # Detect order: who appears first in document order?
    # The simplest check: walk siblings of obj, looking for pre AFTER obj. If found, no reorder needed.
    elem = obj
    while elem is not None:
        elem = elem.find_next_sibling()
        if elem is pre:
            return False  # obj already comes before pre
    # Otherwise pre comes before obj. Move obj before pre.
    obj_extracted = obj.extract()
    pre.insert_before(obj_extracted)
    return True


def process(p: Path, dry_run: bool) -> tuple[int, int]:
    """Return (added_bp, reordered)."""
    text = p.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")
    module_name = p.parent.name
    added = 0
    reordered = 0
    if module_name in BIG_PICTURE_TEXTS:
        if add_big_picture(soup, BIG_PICTURE_TEXTS[module_name]):
            added = 1
    if module_name in CHAPTER_DIRS_FOR_REORDER:
        if reorder_prereqs_objectives(soup):
            reordered = 1
    if added or reordered:
        if not dry_run:
            p.write_text(str(soup), encoding="utf-8")
    return added, reordered


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    total_added = 0
    total_reordered = 0
    files_touched = 0
    for module in CHAPTER_DIRS_FOR_REORDER:
        p = find_chapter_index(module)
        if not p:
            print(f"  MISSING {module}/index.html")
            continue
        added, reordered = process(p, args.dry_run)
        if added or reordered:
            rel = p.relative_to(ROOT)
            bits = []
            if added: bits.append("BIG-PICTURE")
            if reordered: bits.append("REORDER")
            print(f"  {rel}: {' '.join(bits)}")
            total_added += added
            total_reordered += reordered
            files_touched += 1

    print()
    print(f"TOTAL: {total_added} big-picture callouts added, "
          f"{total_reordered} prereqs/objectives reorderings, "
          f"{files_touched} files touched")
    if args.dry_run:
        print("(dry run; nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
