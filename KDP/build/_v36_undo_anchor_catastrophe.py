"""v3.6 R5 P4-A: Undo the over-aggressive anchor-text rewrite from v3.5.

Damage: `_v35_rewrite_titles.py` rewrote the displayed text of EVERY link
pointing to a renamed section. So a sentence like "We covered cross-entropy
in the earlier section" with `<a href="...4.1.html">cross-entropy</a>`
became "We covered cross-entropy in the earlier section" with `<a>How a
Transformer Computes One Token</a>` -- which reads as nonsense.

The original anchor text is lost. Fix: for the 9 renamed sections, find
any anchor where the displayed text matches the NEW title verbatim and is
NOT a top-level chapter heading (chapter-index, TOC, breadcrumbs are
legitimate; in-prose mid-sentence usage isn't). Replace with the format
"Section X.Y" as a neutral fallback.

Heuristic for "in-prose":
  - Anchor is inside a <p>, <li>, or running text (NOT inside <h1>/<h2>/<h3>,
    NOT inside .toc-link / .chapter-nav / .what-comes-next / .crumb).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE = {"_archive", "KDP", "node_modules", "vendor", "scripts"}

# (section_num, NEW_title) -- mirrors _v35_rewrite_titles.py
RENAMED = [
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


def is_in_chrome(text: str, anchor_start: int) -> bool:
    """Return True if the anchor at `anchor_start` lives inside legitimate
    chrome (TOC, nav, h1/2/3, what-comes-next) where showing the title is OK.
    """
    # Look back ~200 chars for closest open tag
    chunk = text[max(0, anchor_start - 600):anchor_start]
    # Find last <h1/h2/h3, .toc-link, .chapter-nav, .what-comes-next that wasn't closed
    chrome_markers = [
        r"<h[1-6]\b",
        r'class="[^"]*(?:toc-link|chapter-nav|whats-next|what-comes-next|crumb|nav-footer|sidebar|chapter-card-title|module-card-title)[^"]*"',
    ]
    for marker in chrome_markers:
        opens = list(re.finditer(marker, chunk))
        if opens:
            last_open = opens[-1].start()
            # Check no </h?> or </nav> closes in between
            after_open = chunk[last_open:]
            if not re.search(r"</(?:h[1-6]|nav|aside)>", after_open):
                return True
    return False


def main() -> int:
    n_files = 0
    n_fixed = 0
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        original = text
        for num, new_title in RENAMED:
            # Anchor pattern with displayed text = the new title
            pattern = re.compile(
                rf'(<a[^>]*href="[^"]*section-{re.escape(num)}\.html(?:#[^"]*)?"[^>]*>)'
                rf'{re.escape(new_title)}'
                rf'(</a>)'
            )
            # Use callback so we can check chrome context
            offset = 0
            while True:
                m = pattern.search(text, offset)
                if not m:
                    break
                if is_in_chrome(text, m.start()):
                    offset = m.end()
                    continue
                replacement = f"{m.group(1)}Section {num}{m.group(2)}"
                text = text[:m.start()] + replacement + text[m.end():]
                n_fixed += 1
                offset = m.start() + len(replacement)
        if text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1

    print(f"Fixed {n_fixed} catastrophic anchor-text instances across {n_files} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
