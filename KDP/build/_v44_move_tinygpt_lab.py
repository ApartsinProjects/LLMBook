"""v4.4: Move 'Lab: Pretrain a Tiny Language Model' from section-11.5.html
to a new section in Module 6 (Pretraining).

The lab is a self-contained ~36K-char block from H3 'Lab: Pretrain a Tiny
Language Model' through the end of the section's main content (just
before the bibliography). It belongs in Module 6 as a hands-on companion
to the pretraining theory.

New target: section-6.9.html in Module 6 (existing 6.1-6.8 untouched).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

SRC = ROOT / "part-3-working-with-llms/module-11-prompt-engineering/section-11.5.html"
DST = ROOT / "part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.9.html"


TEASER = '''<h3>Lab: Pretrain a Tiny Language Model (moved)</h3>
<aside class="callout note">
<div class="callout-title">Lab moved to Module 6</div>
<p>The hands-on lab to pretrain a small GPT-style model on WikiText-103,
which originally lived here as a workhorse for prompt-engineering
experiments, has been moved to its more natural home in
<a class="cross-ref" href="../../part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.9.html">Section 6.9</a>
(Pretraining and Scaling Laws). It is a substantial multi-step lab that
teaches data prep, tokenization, training loop, and evaluation on a
small budget. Once you have run it, you can use the resulting checkpoint
as the substrate for the prompt-engineering experiments in this section.</p>
</aside>
'''


def main() -> int:
    src_text = SRC.read_text(encoding="utf-8", errors="replace")

    # Locate the lab block boundaries
    lab_start_m = re.search(
        r'<h3[^>]*class="lab-title"[^>]*>\s*Lab:\s*Pretrain a Tiny Language Model',
        src_text,
    )
    if not lab_start_m:
        print("[skip] lab heading not found (already moved?)")
        return 0
    lab_start = lab_start_m.start()
    # End at the bibliography or </main>
    lab_end = src_text.find('<details class="bibliography', lab_start)
    if lab_end < 0:
        lab_end = src_text.find("</main>", lab_start)
    if lab_end < 0:
        print("[skip] lab end marker not found")
        return 0

    lab_html = src_text[lab_start:lab_end]
    n_words = len(re.sub(r"<[^>]+>", " ", lab_html).split())
    print(f"  Extracted lab: {lab_end - lab_start} chars / ~{n_words} words")

    # Build a complete new section file for Module 6
    section_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Section 6.9: Lab - Pretrain a Tiny Language Model. End-to-end hands-on pretraining of a small GPT-style model on WikiText-103.">
    <title>Section 6.9: Lab - Pretrain a Tiny Language Model</title>
    <link rel="stylesheet" href="../../styles/book.css">
</head>
<body>
<header class="chapter-header">
    <nav class="header-nav">
        <a href="../../index.html" class="book-title-link">Building Conversational AI with LLMs and Agents</a>
        <a href="../../toc.html" class="toc-link" title="Table of Contents"><span class="toc-icon">&#9776;</span> Contents</a>
    </nav>
    <div class="part-label"><a href="../../part-2-understanding-llms/index.html">Part 2: Understanding LLMs</a> / <a href="index.html">Chapter 6: Pretraining and Scaling Laws</a></div>
    <h1>6.9 Lab: Pretrain a Tiny Language Model</h1>
</header>

<main class="content">
<aside class="callout note">
<div class="callout-title">A hands-on companion to the chapter</div>
<p>This lab walks you through pretraining a small GPT-style model
(TinyGPT, ~10M parameters) on a slice of WikiText-103. It puts every
concept in this chapter into practice: tokenizer training, dataset
streaming, mixed-precision training, gradient clipping, learning-rate
schedules, evaluation. Plan ~2 hours on a single mid-range GPU.</p>
</aside>

{lab_html}

</main>
</body>
</html>
'''

    DST.write_text(section_template, encoding="utf-8")
    print(f"  Wrote {DST.relative_to(ROOT).as_posix()}")

    # Replace lab in source with teaser
    new_src = src_text[:lab_start] + TEASER + src_text[lab_end:]
    SRC.write_text(new_src, encoding="utf-8")
    print(f"  Replaced lab in 11.5 with teaser (saved {(lab_end - lab_start) - len(TEASER):,} chars)")

    # Add card to Module 6 index
    mod6_index = ROOT / "part-2-understanding-llms/module-06-pretraining-scaling-laws/index.html"
    if mod6_index.exists():
        idx_text = mod6_index.read_text(encoding="utf-8", errors="replace")
        if "section-6.9.html" not in idx_text:
            new_card = '''
            <a href="section-6.9.html" class="section-card">
                <span class="section-num">6.9</span>
                <span class="section-title">Lab: Pretrain a Tiny Language Model</span>
                <span class="section-desc">End-to-end hands-on pretraining: tokenize, train, evaluate a ~10M-param GPT on WikiText-103. ~2 hours on a single mid-range GPU.</span>
            </a>
'''
            # Insert before </main>
            idx_text = idx_text.replace("</main>",
                f"<div class='section-grid'>{new_card}</div>\n</main>", 1)
            mod6_index.write_text(idx_text, encoding="utf-8")
            print("  Added 6.9 card to Module 6 index")

    return 0


if __name__ == "__main__":
    sys.exit(main())
