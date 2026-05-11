"""v6.11: Apply lame-diagram audit Top 15 recommendations.

Drops 20 decorative Gemini illustrations across 12 section files,
as specified in KDP/build/_lame_diagram_audit.md (2026-05-11).

DROP list (20 figure blocks total):
  section-20.1  : Fig 20.1.1, Fig 20.1.2
  section-13.3  : Fig 13.3.1, Fig 13.3.2, Fig 13.3.3, Fig 13.3.4, Fig 13.3.5
  section-6.6   : Fig 6.6.1, Fig 6.6.2
  section-13.1  : Fig 13.1.1  (keep 13.1.2)
  section-31.1  : Fig 31.1.1
  section-14.1  : Fig 14.1.1
  section-11.1  : Fig 11.1.2, Fig 11.1.3, Fig 11.1.4
  section-14.4  : Fig 14.4.1
  section-21.2  : Fig 21.2.1
  section-6.4   : Fig 6.4.1, Fig 6.4.2
  section-6.3   : Fig 6.3.1
  section-29.1  : Fig 29.1.1

Deferred (TODO only, not implemented here):
  6.5.1  matplotlib 2-panel SGD-vs-Adam loss-landscape
  6.2.1  SVG token-sequence boxes CLM vs MLM
  13.1.2 matplotlib annotation-cost bar chart
  6.4.3  matplotlib data-curation funnel chart

All edits are idempotent: re-running skips already-deleted figures.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

DROPS = [
    ('part-5-retrieval-conversation/module-20-rag/section-20.1.html', '20.1.1'),
    ('part-5-retrieval-conversation/module-20-rag/section-20.1.html', '20.1.2'),
    ('part-4-training-adapting/module-13-synthetic-data/section-13.3.html', '13.3.1'),
    ('part-4-training-adapting/module-13-synthetic-data/section-13.3.html', '13.3.2'),
    ('part-4-training-adapting/module-13-synthetic-data/section-13.3.html', '13.3.3'),
    ('part-4-training-adapting/module-13-synthetic-data/section-13.3.html', '13.3.4'),
    ('part-4-training-adapting/module-13-synthetic-data/section-13.3.html', '13.3.5'),
    ('part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.6.html', '6.6.1'),
    ('part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.6.html', '6.6.2'),
    ('part-4-training-adapting/module-13-synthetic-data/section-13.1.html', '13.1.1'),
    ('part-8-evaluation-production/module-31-production-engineering/section-31.1.html', '31.1.1'),
    ('part-4-training-adapting/module-14-fine-tuning-fundamentals/section-14.1.html', '14.1.1'),
    ('part-3-working-with-llms/module-11-prompt-engineering/section-11.1.html', '11.1.2'),
    ('part-3-working-with-llms/module-11-prompt-engineering/section-11.1.html', '11.1.3'),
    ('part-3-working-with-llms/module-11-prompt-engineering/section-11.1.html', '11.1.4'),
    ('part-4-training-adapting/module-14-fine-tuning-fundamentals/section-14.4.html', '14.4.1'),
    ('part-5-retrieval-conversation/module-21-conversational-ai/section-21.2.html', '21.2.1'),
    ('part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.4.html', '6.4.1'),
    ('part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.4.html', '6.4.2'),
    ('part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html', '6.3.1'),
    ('part-8-evaluation-production/module-29-evaluation-observability/section-29.1.html', '29.1.1'),
]


def delete_one(rel: str, fig_num: str) -> bool:
    """Delete the specific <figure> block containing Figure {fig_num}.

    Strategy (ported from KDP/build/_v63_chapter6_and_quickwins.py):
      1. Find <strong>Figure N.M.K</strong> in the file.
      2. Walk backwards to the nearest <figure ...> opening tag.
      3. Walk forwards to the first </figure> after the caption.
      4. Splice both out.
      5. Safety guard: refuse if the span exceeds 3000 chars (sibling-eating risk).

    Returns True if a deletion happened, False if skipped or failed.
    """
    p = ROOT / rel
    if not p.exists():
        print(f'  FILE NOT FOUND: {rel}')
        return False

    text = p.read_text(encoding='utf-8')

    cap_pat = re.compile(r'<strong>Figure ' + re.escape(fig_num) + r'</strong>')
    cap_m = cap_pat.search(text)
    if not cap_m:
        print(f'  skip (already removed): Fig {fig_num} in {rel}')
        return False

    cap_pos = cap_m.start()

    open_pat = re.compile(r'<figure[^>]*>', re.IGNORECASE)
    candidates = list(open_pat.finditer(text[:cap_pos]))
    if not candidates:
        print(f'  ERROR: no <figure> before Fig {fig_num} in {rel}')
        return False
    open_start = candidates[-1].start()

    close_match = re.search(r'</figure>', text[cap_pos:], re.IGNORECASE)
    if not close_match:
        print(f'  ERROR: no </figure> after Fig {fig_num} in {rel}')
        return False
    close_end = cap_pos + close_match.end()

    if close_end < len(text) and text[close_end] == '\n':
        close_end += 1

    span = close_end - open_start
    if span > 3000:
        print(f'  REFUSED: Fig {fig_num} in {rel} span {span} chars exceeds 3000 char limit')
        return False

    new_text = text[:open_start] + text[close_end:]
    p.write_text(new_text, encoding='utf-8')
    print(f'  DELETED Fig {fig_num} ({span} chars) {rel}')
    return True


def apply_drops() -> int:
    print('\n=== DROP PHASE: removing lame-diagram figures ===\n')
    total = 0
    for rel, fig_num in DROPS:
        if delete_one(rel, fig_num):
            total += 1
    print(f'\n  Drop phase complete: {total} figure(s) removed.')
    return total


def print_todos() -> None:
    print('\n=== TODO: figures deferred for chart generation ===\n')
    todos = [
        ('6.5.1', 'matplotlib',
         'Two-panel loss-landscape contour: left=SGD oscillating in narrow ravine, '
         'right=Adam descending diagonally. Replace GPS-navigator cartoon. '
         'File: part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.5.html'),
        ('6.2.1', 'SVG',
         'Horizontal token-sequence boxes: left CLM (rightmost masked with "?"); '
         'right MLM (middle tokens [MASK]). Replace puzzle cartoon. '
         'File: part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html'),
        ('13.1.2', 'matplotlib',
         'Horizontal bar chart: annotation costs per example (expert $5-$20, '
         'crowd $0.10-$0.50, GPT-4o $0.005-$0.02, self-hosted $0.0005-$0.002). '
         'Replace seed-data garden cartoon. '
         'File: part-4-training-adapting/module-13-synthetic-data/section-13.1.html'),
        ('6.4.3', 'matplotlib',
         'Waterfall/funnel chart: token counts at each curation stage using '
         'FineWeb numbers (100 TB raw -> 15T final). Upgrade existing pipeline cartoon. '
         'File: part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.4.html'),
    ]
    for fig_ref, chart_type, desc in todos:
        print(f'  TODO: regenerate Figure {fig_ref} as {chart_type}')
        print(f'        {desc}\n')


def final_audit() -> None:
    print('\n=== FINAL AUDIT: figure counts in affected files ===\n')
    cap_pat = re.compile(r'<strong>Figure \d+\.\d+\.\d+</strong>')
    for rel in sorted(set(r for r, _ in DROPS)):
        p = ROOT / rel
        if not p.exists():
            print(f'  MISSING {rel}')
            continue
        text = p.read_text(encoding='utf-8')
        found = len(cap_pat.findall(text))
        # Count drops scheduled for this file
        n_drops = sum(1 for r, _ in DROPS if r == rel)
        print(f'  {rel}: {found} figures remain (dropped {n_drops})')


def main() -> int:
    print('v6.11: Apply lame-diagram audit Top 15 (20 figure drops across 12 files)')
    drops_performed = apply_drops()
    print_todos()
    final_audit()
    print(f'\n=== SUMMARY: {drops_performed} figure block(s) deleted this run. ===')
    return 0


if __name__ == '__main__':
    sys.exit(main())
