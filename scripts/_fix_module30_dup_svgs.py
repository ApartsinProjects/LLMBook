"""Remove 5 duplicate inline-SVG figures in module 30. Each pair has two
captions promising different content but the same SVG. Author judgment:
keep the figure whose caption matches the SVG, drop the mis-captioned
duplicate.

Files affected (per duplicate-images-audit.md):
- section-30.2.html: Figure 30.2.4 (pipeline caption) shares SVG with 30.2.3 (mitigation)
- section-30.3.html: Figure 30.3.4 (docs standards caption) shares SVG with 30.3.3 (env impact)
- section-30.4.html: Figure 30.4.4 (jurisdictions caption) shares SVG with 30.4.3 (sectors)
- section-30.5.html: Figure 30.5.3 (three-lines caption) shares SVG with 30.5.2 (audit trail)
- section-30.6.html: Figure 30.6.3 (DP-SGD caption) shares SVG with 30.6.2 (IP ownership)

Per pair, this script:
  1. Removes the SECOND <div class="diagram-container"> block (which contains
     the duplicate SVG + mis-captioned <div class="diagram-caption">).
  2. Replaces any prose paragraph that pre-introduces the dropped figure
     with a footnote-style explanation ("[Note: dedicated diagram pending]")
     so the reader still gets the conceptual content via prose.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "part-9-safety-strategy" / "module-30-safety-ethics-regulation"


# Each pair: (file, the_second_figure_caption_marker, dropped_label, replacement_note)
# The marker is unique text inside the SECOND diagram-caption that lets us
# locate the wrapper block.
PAIRS = [
    ("section-30.2.html", "Figure 30.2.4",
     "30.2.4",
     "A production hallucination pipeline routes LLM output through detection checks (consistency, citation, NLI) and selects a response strategy: emit grounded answer, abstain, or escalate to a human. The strategy choice is risk-tier dependent: high-stakes domains default to abstention when confidence is low."),
    ("section-30.3.html", "Figure 30.3.4",
     "30.3.4",
     "Three complementary documentation standards cover progressively broader scope: a <strong>model card</strong> documents the model itself (intended use, performance, known limitations); a <strong>datasheet</strong> documents the training data (provenance, demographics, consent); a <strong>system card</strong> documents the deployed application (the model in its operational context, including UI, retrieval layer, and safety filters). Use all three together for full auditability."),
    ("section-30.4.html", "Figure 30.4.4",
     "30.4.4",
     "Regulatory approaches vary by jurisdiction: the EU enforces binding obligations via the AI Act (with conformity assessments for high-risk systems); the US currently relies on voluntary frameworks (NIST AI RMF) and sector-specific rules (FTC, HHS, FDA); China has a notification regime through the Cyberspace Administration; the UK follows a principles-based regulator approach. A multinational deployment must satisfy the strictest applicable regime, which typically means designing to EU requirements then validating against local rules."),
    ("section-30.5.html", "Figure 30.5.3",
     "30.5.3",
     "<strong>SR 11-7's three lines of defense</strong> separate concerns to prevent any single team from grading its own work. The <strong>first line</strong> (model owners and developers) builds and runs the model. The <strong>second line</strong> (an independent validation function) reviews the first line's work against the firm's model risk policy. The <strong>third line</strong> (internal audit, reporting to the board) verifies that the first two lines are doing their jobs. Banks regulated under SR 11-7 must demonstrate all three lines exist and function; the framework now applies in practice to LLM-based decision systems even though SR 11-7 predates LLMs."),
    ("section-30.6.html", "Figure 30.6.3",
     "30.6.3",
     "<strong>Differentially-private SGD (DP-SGD)</strong> protects training-data privacy through two coordinated mechanisms: (1) per-example gradient clipping bounds any single sample's contribution to the parameter update; (2) calibrated Gaussian noise is added to the clipped gradients before each step. Together they give a mathematical bound on how much any individual training example can influence the final model, expressed as the (ε, δ)-DP privacy budget. The trade-off: stronger privacy (smaller ε) requires more noise and thus more training compute for the same accuracy."),
]


def remove_block_around_caption(text: str, marker: str) -> tuple[str, bool]:
    """Find a <div class="diagram-container"> whose caption contains the marker,
    remove the whole container block. Return (new_text, removed)."""
    cap_idx = text.find(marker)
    if cap_idx == -1:
        return text, False
    # Walk back to the enclosing <div class="diagram-container">
    container_start = text.rfind('<div class="diagram-container">', 0, cap_idx)
    if container_start == -1:
        return text, False
    # Find the matching </div> by counting depth from container_start
    depth = 0
    i = container_start
    while i < len(text):
        if text[i:i+5] == '<div ':
            depth += 1
            i += 5
            continue
        if text[i:i+6] == '</div>':
            depth -= 1
            i += 6
            if depth == 0:
                break
            continue
        i += 1
    if depth != 0:
        return text, False
    return text[:container_start] + text[i:], True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    removed_count = 0
    for fname, marker, label, replacement_prose in PAIRS:
        p = DIR / fname
        text = p.read_text(encoding="utf-8")
        new_text, removed = remove_block_around_caption(text, marker)
        if not removed:
            print(f"  SKIP {fname}: marker {marker!r} not found (already fixed?)")
            continue
        # Insert a replacement <p class="figure-replaced"> at the position where
        # the diagram-container used to be, so the reader still sees the content
        # the dropped figure was supposed to convey.
        # The new text was obtained by deleting the block; insert the prose now.
        anchor = text.rfind('<div class="diagram-container">', 0, text.find(marker))
        # Find what immediately preceded the dropped container in the NEW text
        prefix_len = anchor
        replacement_html = (
            f'<p class="figure-replaced"><em>'
            f'{replacement_prose}'
            f'</em></p>'
        )
        new_text = new_text[:prefix_len] + replacement_html + new_text[prefix_len:]
        if not args.dry_run:
            p.write_text(new_text, encoding="utf-8")
        print(f"  {fname}: removed Figure {label} duplicate SVG block "
              f"({len(text) - len(new_text)} chars), inserted prose replacement "
              f"({len(replacement_html)} chars)")
        removed_count += 1

    print()
    print(f"TOTAL: {removed_count} duplicate SVG figures removed")
    if args.dry_run:
        print("(dry run; nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
