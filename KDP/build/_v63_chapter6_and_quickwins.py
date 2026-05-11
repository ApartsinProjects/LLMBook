"""v6.3: Chapter 6 diagram remediation + quick-win fixes.

CHAPTER 6 (5 changes per audit findings #1, #2, #3, #6, #8):
  - Fig 6.3.2: cartoon  -> matplotlib power-law chart       (swap src)
  - Fig 6.3.3: cartoon  -> Chinchilla vs Kaplan chart       (swap src)
  - Fig 6.5.2: cartoon  -> LR-schedule chart                (swap src)
  - Fig 6.1.2: rocket cartoon -> DELETE (Fig 6.1.6 covers it)
  - Fig 6.3.4: butterfly cartoon -> DELETE (Fig 6.3.11 covers it)

QUICK WINS (audit findings #4, #7, #10):
  - Fig 7.4.3:  illustrative -> multilingual bar chart      (swap src)
  - Fig 33.1.1: 4-axis radar -> horizontal bar chart        (swap src)
  - Fig 14.1.3 / 15.7.3: dedup. Make 14.1.3 canonical;
                          replace 15.7.3 with cross-reference callout.

All edits idempotent.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# ---- src swaps ------------------------------------------------------

SWAPS = [
    # Chapter 6
    (
        'part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html',
        '6.3.2',
        'images/scaling-laws-power-law.png',
        'images/fig-6.3.2-power-law.png',
        'Power-law scaling of LLM test loss: log-log plot showing how loss decreases as parameters (N), training tokens (D), or compute (C) grow, each following a different power-law slope',
    ),
    (
        'part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html',
        '6.3.3',
        'images/chinchilla-vs-kaplan.png',
        'images/fig-6.3.3-chinchilla-vs-kaplan.png',
        'Chinchilla vs Kaplan compute-optimal scaling: two log-log curves of optimal model size N* vs compute budget C, with real models (GPT-3, Chinchilla, PaLM, LLaMA family) overlaid as scatter points',
    ),
    (
        'part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.5.html',
        '6.5.2',
        'images/learning-rate-warmup.png',
        'images/fig-6.5.2-lr-schedules.png',
        'Learning-rate schedules: cosine decay (warmup then cosine to 10%) vs WSD (warmup, stable plateau, linear decay to zero), plotted on shared step-vs-LR axes',
    ),
    # Quick wins
    (
        'part-2-understanding-llms/module-07-modern-llm-landscape/section-7.4.html',
        '7.4.3',
        None,  # any non-fig-7.4.3 image src; we'll search for a Fig 7.4.3 figure
        'images/fig-7.4.3-multilingual-gap.png',
        'Multilingual QA performance gap: bar chart of representative high, medium, and low-resource languages with English as the baseline; the lowest-resource language trails English by 51 percentage points',
    ),
    (
        'part-9-safety-strategy/module-33-strategy-product-roi/section-33.1.html',
        '33.1.1',
        'images/figure-33.1.1.png',
        'images/fig-33.1.1-ai-readiness-bars.png',
        'AI Readiness pillars as a horizontal bar chart with a "minimum viable" reference line at 3/5; the weakest pillar is immediately scannable',
    ),
]

def find_fig_img(text: str, fig_num: str, old_src: str | None) -> tuple[int, int, str] | None:
    """Find <img> tag paired with Figure {fig_num}. Returns (start, end, tag) or None."""
    pat = re.compile(
        r'(<img[^>]*src="[^"]+"[^>]*/?>)'
        r'(?:[^<]|<(?!img)[^>]*>)*?'
        r'<strong>Figure ' + re.escape(fig_num) + r'</strong>',
        re.DOTALL,
    )
    m = pat.search(text)
    if m:
        return m.start(1), m.end(1), m.group(1)
    return None


def swap_one(rel: str, fig_num: str, old_src: str | None, new_src: str, new_alt: str) -> bool:
    p = ROOT / rel
    if not p.exists(): return False
    text = p.read_text(encoding='utf-8')
    if new_src in text:
        print(f'  already swapped: {rel} Fig {fig_num}')
        return False
    target = find_fig_img(text, fig_num, old_src)
    if not target:
        print(f'  NO MATCH for Fig {fig_num} in {rel}')
        return False
    s, e, old_tag = target
    style_m = re.search(r'style="[^"]*"', old_tag)
    style = ' ' + style_m.group(0) if style_m else ''
    new_tag = f'<img alt="{new_alt}" loading="lazy" src="{new_src}"{style}/>'
    new_text = text[:s] + new_tag + text[e:]
    p.write_text(new_text, encoding='utf-8')
    print(f'  swapped Fig {fig_num} in {rel}')
    return True


# ---- deletions: Fig 6.1.2 + Fig 6.3.4 -------------------------------

DELETES = [
    (
        'part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.1.html',
        '6.1.2',
        'figure',  # element kind: <figure>...</figure>
    ),
    (
        'part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html',
        '6.3.4',
        'figure',
    ),
]


def delete_one(rel: str, fig_num: str, kind: str) -> bool:
    """Delete the SPECIFIC <figure> block containing Figure {fig_num}.

    Strategy: find the position of the <strong>Figure N.M.K</strong>
    caption, then walk BACKWARDS to the nearest <figure> open tag and
    FORWARDS to the next </figure> close tag. This avoids the trap of a
    naive `<figure>...Figure {N.M.K}.../figure>` regex which would
    swallow several siblings if there is no </figure> between them.
    """
    p = ROOT / rel
    text = p.read_text(encoding='utf-8')
    cap_pat = re.compile(r'<strong>Figure ' + re.escape(fig_num) + r'</strong>')
    cap_m = cap_pat.search(text)
    if not cap_m:
        print(f'  NO MATCH for delete Fig {fig_num} in {rel}')
        return False
    cap_pos = cap_m.start()
    # Walk back to nearest <figure> opening
    open_pat = re.compile(r'<' + kind + r'[^>]*>')
    candidates = list(open_pat.finditer(text[:cap_pos]))
    if not candidates:
        print(f'  NO opening <{kind}> before Fig {fig_num} in {rel}')
        return False
    open_start = candidates[-1].start()
    # Walk forward to first </figure> after the caption
    close_match = re.search(r'</' + kind + r'>', text[cap_pos:])
    if not close_match:
        print(f'  NO closing </{kind}> after Fig {fig_num} in {rel}')
        return False
    close_end = cap_pos + close_match.end()
    # Also consume trailing whitespace/newline
    while close_end < len(text) and text[close_end] in '\n\r ':
        close_end += 1
    # Sanity check: the deletion span should be small (< 3000 chars typical)
    span = close_end - open_start
    if span > 3000:
        print(f'  REFUSING to delete Fig {fig_num} in {rel} — span {span} chars too large')
        return False
    new_text = text[:open_start] + text[close_end:]
    p.write_text(new_text, encoding='utf-8')
    print(f'  deleted Fig {fig_num} block in {rel} ({span} chars)')
    return True


# ---- 14.1.3 / 15.7.3 dedup ------------------------------------------

CROSS_REF_BLOCK = '''<div class="callout note">
<div class="callout-title">See also</div>
<p>The crossing-curves dynamic shown for fine-tuning in <a href="../../part-4-training-adapting/module-14-fine-tuning-fundamentals/section-14.1.html"><strong>Figure 14.1.3</strong></a> applies identically to continual learning. As domain performance climbs, general capabilities decline; the goal is to find and maintain the sweet spot. The same chart and the same intervention strategies (replay, distillation, careful LR scheduling) apply.</p>
</div>'''


def replace_15_7_3_with_xref() -> bool:
    p = ROOT / 'part-4-training-adapting/module-15-peft/section-15.7.html'
    text = p.read_text(encoding='utf-8')
    # Replace the entire <figure ...>...Figure 15.7.3.../figure> with the cross-ref callout
    pat = re.compile(
        r'<figure[^>]*>(?:.|\n)*?<strong>Figure 15\.7\.3</strong>(?:.|\n)*?</figure>\s*',
        re.IGNORECASE,
    )
    if 'callout-title">See also' in text:
        print(f'  already cross-ref\'d 15.7.3')
        return False
    new, n = pat.subn(CROSS_REF_BLOCK + '\n', text, count=1)
    if n:
        p.write_text(new, encoding='utf-8')
        print(f'  replaced Fig 15.7.3 with cross-reference to 14.1.3')
        return True
    print(f'  NO MATCH for Fig 15.7.3')
    return False


def main() -> int:
    print('Chapter 6 + Quick Wins src swaps:')
    for rel, fig, old, new, alt in SWAPS:
        swap_one(rel, fig, old, new, alt)

    print('\nChapter 6 deletions:')
    for rel, fig, kind in DELETES:
        delete_one(rel, fig, kind)

    print('\nFig 14.1/15.7 dedup:')
    replace_15_7_3_with_xref()
    return 0


if __name__ == '__main__':
    sys.exit(main())
