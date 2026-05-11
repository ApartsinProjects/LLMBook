"""v6.4.x: Add missing <text> labels to two SVG root boxes.

USER REPORT
"Figure 29.1.5: root box is black, no text in it, find root cause"

ROOT CAUSE
Two SVGs in the book have a #1a1a2e (dark navy) header rect at the top
of the diagram with NO accompanying <text> element to label it. All
sibling rects in the same SVGs DO have paired <text> labels. This is
an authoring oversight — the root label was forgotten when the SVG was
built.

Audit (book-wide, checking every dark-fill rect for an inside-bounds
<text>): only 2 cases:

  1. section-29.1 Figure 29.1.5  — Taxonomy of LLM evaluation metrics
                                   (root should be "LLM Evaluation Metrics")
  2. section-31.1 Figure 31.1.6  — Deployment decision tree
                                   (root should be "Self-host the model?")

FIX
For each, insert a <text> element centered on the existing rect with
the appropriate label. White text on the dark background, font matches
the SVG style (font-weight 600, font-size 13).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# (file, rect-pattern, root-label)
FIXES = [
    (
        'part-8-evaluation-production/module-29-evaluation-observability/section-29.1.html',
        r'<rect fill="#1a1a2e" filter="url\(#shadow1\)" height="44" rx="22" width="250" x="250" y="10"></rect>',
        # rect: x=250, y=10, w=250, h=44 -> center (375, 32). Text baseline ~37.
        '<text fill="white" font-size="14" font-weight="700" text-anchor="middle" x="375" y="37">LLM Evaluation Metrics</text>',
    ),
    (
        'part-8-evaluation-production/module-31-production-engineering/section-31.1.html',
        r'<rect fill="#1a1a2e" filter="url\(#shadow3\)" height="40" rx="20" width="240" x="230" y="10"></rect>',
        # rect: x=230, y=10, w=240, h=40 -> center (350, 30). Text baseline ~35.
        '<text fill="white" font-size="14" font-weight="700" text-anchor="middle" x="350" y="35">Self-host the model?</text>',
    ),
]


def main() -> int:
    fixed = 0
    for rel, rect_pat, label_text in FIXES:
        p = ROOT / rel
        if not p.exists():
            print(f'  MISSING: {rel}')
            continue
        text = p.read_text(encoding='utf-8')
        # Idempotent guard
        if label_text in text:
            print(f'  already labeled: {rel}')
            continue
        new_text, n = re.subn(
            rect_pat,
            lambda m: m.group(0) + '\n' + label_text,
            text, count=1,
        )
        if n:
            p.write_text(new_text, encoding='utf-8')
            print(f'  + label "{label_text[label_text.find(">")+1:label_text.find("</text>")]}" in {rel}')
            fixed += 1
        else:
            print(f'  NO MATCH: {rel}')
    print(f'\nFixed {fixed} root boxes.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
