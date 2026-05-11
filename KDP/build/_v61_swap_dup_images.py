"""v6.1: Swap dup-image references to newly-generated Mermaid PNGs.

Each of these 4 figures was previously sharing a src with another figure
in the same file:
  - section-1.3 Fig 1.3.2 (Skip-gram NN)        was: fig-1.3.5-cosine-sim.png
  - section-2.2 Fig 2.2.6 (BPE merges)          was: fig-2.2.4-unigram.png
  - section-3.1 Fig 3.1.7 (RNN unrolled)        was: fig-3.1.3-vanishing-grad.png
  - section-3.2 Fig 3.2.5 (Bahdanau attention)  was: fig-3.2.4-gradient-attention.png

Idempotent: only edits if old_src is present.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

SWAPS = [
    # (file, fig_num, old_src_substr, new_src, new_alt)
    (
        'part-1-foundations/module-01-foundations-nlp-text-representation/section-1.3.html',
        '1.3.2',
        'images/fig-1.3.5-cosine-sim.png',
        'images/fig-1.3.2-skipgram-network.png',
        'Skip-gram neural network: a one-hot center word is multiplied by the embedding matrix W to look up the word\'s hidden vector, then by W\' and softmax to produce a probability distribution over context words',
    ),
    (
        'part-1-foundations/module-02-tokenization-subword-models/section-2.2.html',
        '2.2.6',
        'images/fig-2.2.4-unigram.png',
        'images/fig-2.2.6-bpe-merges.png',
        'BPE merge sequence: at each step, the most frequent adjacent character pair is merged and recorded in a merge table that can be replayed at inference time',
    ),
    (
        'part-1-foundations/module-03-sequence-models-attention/section-3.1.html',
        '3.1.7',
        'images/fig-3.1.3-vanishing-grad.png',
        'images/fig-3.1.7-rnn-unrolled.png',
        'An RNN unrolled through time: the same RNN cell with shared parameters W, U, b is applied at every time step, producing hidden states h_1 ... h_T and outputs y_1 ... y_T',
    ),
    (
        'part-1-foundations/module-03-sequence-models-attention/section-3.2.html',
        '3.2.5',
        'images/fig-3.2.4-gradient-attention.png',
        'images/fig-3.2.5-bahdanau-attention.png',
        'Bahdanau additive attention: at each decoder step, alignment scores are computed between the decoder state and each encoder hidden state, normalized via softmax to produce attention weights, then combined into a context vector that the decoder consumes',
    ),
]


def find_target_img_for_figure(text: str, fig_num: str, old_src_sub: str) -> tuple[int, int, str] | None:
    """Find the <img ...src=... that is paired with Figure {fig_num}.
    Returns (start, end, full_img_tag) or None.
    Strategy: walk diagram-containers; the one whose caption is "Figure {fig_num}"
    and whose img.src contains old_src_sub is our target.
    """
    pat = re.compile(
        r'<div class="diagram-container">\s*'
        r'(?P<img><img[^>]+src="[^"]*' + re.escape(old_src_sub.split("/")[-1]) + r'"[^>]*/?>)'
        r'.*?'
        r'<strong>Figure ' + re.escape(fig_num) + r'</strong>',
        re.DOTALL,
    )
    m = pat.search(text)
    if not m:
        return None
    return m.start('img'), m.end('img'), m.group('img')


def fix() -> int:
    fixed = 0
    for rel, fig_num, old_src_sub, new_src, new_alt in SWAPS:
        p = ROOT / rel
        if not p.exists():
            print(f'  MISSING: {rel}')
            continue
        text = p.read_text(encoding='utf-8')
        # Idempotent: if new_src is already present, skip
        if new_src in text:
            print(f'  already swapped: {rel} Fig {fig_num}')
            continue

        target = find_target_img_for_figure(text, fig_num, old_src_sub)
        if not target:
            print(f'  NO MATCH for Fig {fig_num} in {rel}')
            continue
        s, e, old_tag = target
        # Build new tag: keep loading="lazy" if present; replace alt+src; keep style if present
        style_m = re.search(r'style="[^"]*"', old_tag)
        style = ' ' + style_m.group(0) if style_m else ''
        new_tag = f'<img alt="{new_alt}" loading="lazy" src="{new_src}"{style}/>'
        new_text = text[:s] + new_tag + text[e:]
        p.write_text(new_text, encoding='utf-8')
        print(f'  swapped Fig {fig_num} in {rel}')
        fixed += 1
    return fixed


if __name__ == '__main__':
    sys.exit(fix())
