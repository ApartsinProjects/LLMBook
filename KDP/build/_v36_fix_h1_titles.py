"""v3.6 R5 P1: Fix H1 titles for the 9 sections renamed in v3.5.

The v3.5 rename script `_v35_rewrite_titles.py` had a regex that REQUIRED
the H1 to start with the section number (`<h1>X.Y title</h1>`). But these
H1s use plain `<h1>title</h1>` without numeric prefix. So the regex
matched 0 H1s; only the `<title>` tag and meta got updated.

Result: tab/title says "What Every LLM Engineer Needs From Classical ML",
but the visible H1 still says "ML Basics: Features, Optimization &
Generalization". Reader sees two different chapter titles.

Fix: rewrite the H1 directly (no number prefix expected). Also update
breadcrumb-style references and any chapter-card titles that still show
the old name.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE = {"_archive", "KDP", "node_modules", "vendor", "scripts"}

# (section_num, OLD_h1, NEW_title)
RENAMES = [
    ("0.1",  "ML Basics: Features, Optimization &amp; Generalization",
              "What Every LLM Engineer Needs From Classical ML"),
    ("0.3",  "PyTorch Tutorial",
              "PyTorch in 90 Minutes: Tensors to Training Loop"),
    ("3.1",  "Recurrent Neural Networks &amp; Their Limitations",
              "Why RNNs Couldn't Scale to Modern LLMs"),
    ("4.1",  "Transformer Architecture Deep Dive",
              "How a Transformer Computes One Token"),
    ("6.1",  "The Landmark Models",
              "BERT, GPT, T5: Three Bets That Shaped Today's LLMs"),
    ("8.1",  "The Test-Time Compute Paradigm",
              "Trading FLOPs for IQ: The Test-Time Compute Bet"),
    ("17.1", "RLHF: Reinforcement Learning from Human Feedback",
              "RLHF: Teaching a Model What 'Helpful' Means"),
    ("22.1", "Foundations of AI Agents",
              "What Makes an LLM an Agent (and What Doesn't)"),
    ("32.2", "Hallucination &amp; Reliability",
              "Why LLMs Hallucinate and How to Catch Them"),
]


def find_section_file(num: str) -> Path | None:
    for p in ROOT.glob(f"part-*/module-*/section-{num}.html"):
        return p
    return None


def main() -> int:
    n_h1 = 0
    n_inbound_files = 0
    for num, old_h1, new_title in RENAMES:
        p = find_section_file(num)
        if not p:
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        # Replace the H1 directly
        new_text = text.replace(f"<h1>{old_h1}</h1>", f"<h1>{new_title}</h1>")
        if new_text != text:
            p.write_text(new_text, encoding="utf-8")
            n_h1 += 1
            print(f"  H1 renamed in section-{num}.html")

    # Also update any other places that still show the old title:
    # - chapter card titles in module index pages
    # - 'previous/next' nav links
    # - <a> link text in module index pointing to renamed section
    print("\n  Updating chapter-card / nav references to old titles...")
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        original = text
        for num, old_h1, new_title in RENAMES:
            # Direct text substitutions WHERE the old title appears as link text or card title
            text = re.sub(
                rf'(<a[^>]*href="[^"]*section-{re.escape(num)}\.html(?:#[^"]*)?"[^>]*>){re.escape(old_h1)}(</a>)',
                rf'\g<1>{new_title}\g<2>',
                text,
            )
            # Card title (h2/h3 inside chapter-card)
            text = re.sub(
                rf'(<h[23][^>]*class="[^"]*chapter-card-title[^"]*"[^>]*>){re.escape(old_h1)}(</h[23]>)',
                rf'\g<1>{new_title}\g<2>',
                text,
            )
        if text != original:
            p.write_text(text, encoding="utf-8")
            n_inbound_files += 1

    print(f"\nFixed {n_h1} H1s; updated {n_inbound_files} inbound files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
