"""v3.5 R3#7: Rewrite 9 academic-sounding chapter/section titles to
benefit-oriented prose for sample-and-buy adoption.

For each (chapter, section, new_title), updates:
  - <h1> in the section file
  - <title> tag
  - meta description
  - inbound cross-reference link text (anchor text inside <a>)
  - TOC and chapter-index references
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE = {"_archive", "KDP", "node_modules", "vendor", "scripts"}

# (chapter.section, NEW title)
RENAMES = [
    ("0.1",  "What Every LLM Engineer Needs From Classical ML"),
    ("0.3",  "PyTorch in 90 Minutes: Tensors to Training Loop"),
    ("3.1",  "Why RNNs Couldn't Scale to Modern LLMs"),
    ("4.1",  "How a Transformer Computes One Token"),
    ("6.1",  "BERT, GPT, T5: Three Bets That Shaped Today's LLMs"),
    ("8.1",  "Trading FLOPs for IQ: The Test-Time Compute Bet"),
    ("17.1", "RLHF: Teaching a Model What 'Helpful' Means"),
    ("22.1", "What Makes an LLM an Agent (and What Doesn't)"),
    ("32.2", "Why LLMs Hallucinate and How to Catch Them"),
]


def find_section(num: str) -> Path | None:
    for p in ROOT.glob(f"part-*/module-*/section-{num}.html"):
        return p
    return None


def main() -> int:
    n_files = 0
    n_inbound_total = 0
    for num, new_title in RENAMES:
        p = find_section(num)
        if not p:
            print(f"  [skip] section-{num}.html not found")
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        original = text
        # H1 — keep the leading "X.Y "
        text = re.sub(
            rf'(<h1[^>]*>\s*{re.escape(num)}\s+)([^<]+)(</h1>)',
            rf'\1{new_title}\3',
            text,
        )
        # <title>
        text = re.sub(
            rf'(<title[^>]*>Section\s+{re.escape(num)}:\s*)([^<]+)(</title>)',
            rf'\g<1>{new_title}\3',
            text,
        )
        # meta description
        text = re.sub(
            rf'(name="description"[^>]*content="Section\s+{re.escape(num)}:\s*)([^"]+?)(\.\s*A comprehensive)',
            rf'\g<1>{new_title}\3',
            text,
        )
        if text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1
            print(f"  Renamed {num}: '{new_title}'")

    # Update inbound link anchor text in other files
    print("\n  Updating inbound cross-reference anchor text...")
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        original = text
        for num, new_title in RENAMES:
            # Find <a href="...section-N.M.html">OLD TITLE</a> -> rewrite TITLE
            # Be conservative: only rewrite when the link text contains a generic
            # academic title hint (we don't have the OLD title at hand, so use
            # a permissive pattern that catches "Section N.M" followed by old title).
            # Skip links whose anchor is just "Section N.M" (numeric-only fine to leave).
            text = re.sub(
                rf'(<a[^>]*href="[^"]*section-{re.escape(num)}\.html(?:#[^"]*)?"[^>]*>)([^<]*?)(</a>)',
                lambda m: m.group(1) + (
                    new_title if any(c.isalpha() for c in m.group(2).strip())
                    and "Section" not in m.group(2)
                    and m.group(2).strip() != ""
                    else m.group(2)
                ) + m.group(3),
                text,
            )
        if text != original:
            p.write_text(text, encoding="utf-8")
            n_inbound_total += 1

    print(f"  Updated anchor text in {n_inbound_total} inbound files")
    print(f"\nRenamed {n_files} chapter titles")
    return 0


if __name__ == "__main__":
    sys.exit(main())
