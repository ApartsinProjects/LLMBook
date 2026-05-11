"""v6.12: Swap the 4 deferred lame-diagram conversions to their new charts.

Per the audit (`KDP/build/_lame_diagram_audit.md`) and the TODO list from
v6.11, these are the four figures that needed real chart generation rather
than just deletion. The new assets were produced by:
   scripts/svg_to_matplotlib/gen_figure_6_5_1.py
   scripts/svg_to_matplotlib/gen_figure_6_4_3.py
   scripts/svg_to_matplotlib/gen_figure_13_1_2.py

Figure 6.2.1 (CLM vs MLM) gets an INLINE SVG (no separate file) so the
token-boxes can scale with text size without rasterization.

Each swap:
  - Replaces the cartoon's <img> src with the matplotlib output
  - Updates alt text to be informative
  - Idempotent via 'already swapped' guard
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# (file, fig_num, old_src_substr, new_src, new_alt)
SWAPS = [
    (
        'part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.5.html',
        '6.5.1',
        'adam-optimizer-navigator.png',
        'images/fig-6.5.1-sgd-vs-adam.png',
        'Two-panel loss landscape: SGD oscillates along the high-curvature axis of a narrow ravine while Adam, using per-parameter learning rate scaling, descends diagonally with minimal oscillation toward the minimum',
    ),
    (
        'part-4-training-adapting/module-13-synthetic-data/section-13.1.html',
        '13.1.2',
        'seed-data-garden.png',
        'images/fig-13.1.2-annotation-cost.png',
        'Annotation cost per training example across four sourcing methods on a log scale: expert annotators ($5-$20), crowd workers ($0.10-$0.50), LLM APIs like GPT-4o or Claude ($0.005-$0.02), and self-hosted open-weights small LLMs ($0.0005-$0.002); roughly four orders of magnitude cheaper end to end',
    ),
    (
        'part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.4.html',
        '6.4.3',
        'data-curation-pipeline.png',
        'images/fig-6.4.3-curation-funnel.png',
        'Data curation funnel: token counts at each stage of a Common Crawl curation pipeline (raw web 320T -> URL+boilerplate strip 180T -> MinHash near-dedup 65T -> language/quality filter 28T -> educational-classifier filter 1.3T) with reduction ratios annotated between bars',
    ),
]

# Figure 6.2.1: replace <figure>...</figure> cartoon with an inline SVG showing
# CLM vs MLM token-sequence diagrams. We REPLACE the entire <figure> block
# because the new asset is inline (no separate file).

FIG_621_SVG_REPLACEMENT = '''<div class="diagram-container">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 320" role="img"
     aria-labelledby="fig621-title fig621-desc"
     style="max-width:100%; height:auto; font-family:'Segoe UI', system-ui, sans-serif;">
  <title id="fig621-title">CLM versus MLM training objectives</title>
  <desc id="fig621-desc">Two side-by-side token-sequence diagrams. The left panel shows causal language modeling (CLM): the model sees only the previous tokens and predicts the next one, with a question mark on the rightmost position. The right panel shows masked language modeling (MLM): some middle tokens are replaced by [MASK], and the model uses bidirectional context (both left and right neighbors) to predict the masked tokens.</desc>

  <defs>
    <marker id="f621-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#555"/>
    </marker>
  </defs>

  <!-- ================== LEFT PANEL: CLM ================== -->
  <g transform="translate(20, 0)">
    <text x="200" y="28" text-anchor="middle" font-size="16" font-weight="700" fill="#1565c0">
      Causal LM (GPT-style)
    </text>
    <text x="200" y="50" text-anchor="middle" font-size="12" font-style="italic" fill="#555">
      predict the next token from prior tokens only
    </text>

    <!-- Token boxes: "The", "cat", "sat", "on", "the", "?" -->
    <g font-size="14" text-anchor="middle">
      <rect x="20"  y="80" width="60" height="44" rx="6" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
      <text x="50"  y="108" fill="#0d47a1">The</text>
      <rect x="90"  y="80" width="60" height="44" rx="6" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
      <text x="120" y="108" fill="#0d47a1">cat</text>
      <rect x="160" y="80" width="60" height="44" rx="6" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
      <text x="190" y="108" fill="#0d47a1">sat</text>
      <rect x="230" y="80" width="60" height="44" rx="6" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
      <text x="260" y="108" fill="#0d47a1">on</text>
      <rect x="300" y="80" width="60" height="44" rx="6" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
      <text x="330" y="108" fill="#0d47a1">the</text>
      <!-- Predicted slot -->
      <rect x="370" y="80" width="60" height="44" rx="6" fill="#fff3e0" stroke="#e65100" stroke-width="2.5" stroke-dasharray="4 3"/>
      <text x="400" y="110" fill="#bf360c" font-size="18" font-weight="700">?</text>
    </g>

    <!-- Arrows from prior tokens to the "?" slot -->
    <g stroke="#1565c0" stroke-width="1.5" fill="none">
      <path d="M 50 80 C 50 60, 400 60, 400 80" marker-end="url(#f621-arrow)"/>
      <path d="M 120 80 C 120 64, 400 64, 400 80" marker-end="url(#f621-arrow)"/>
      <path d="M 190 80 C 190 68, 400 68, 400 80" marker-end="url(#f621-arrow)"/>
      <path d="M 260 80 C 260 72, 400 72, 400 80" marker-end="url(#f621-arrow)"/>
      <path d="M 330 78 L 370 80" marker-end="url(#f621-arrow)"/>
    </g>

    <!-- Loss label -->
    <text x="200" y="170" text-anchor="middle" font-size="13" fill="#333">
      <tspan font-style="italic">Loss:</tspan> minimize -log P(mat | The, cat, sat, on, the)
    </text>
    <text x="200" y="195" text-anchor="middle" font-size="11" fill="#666">
      Each position predicts ONE next token from the left.
    </text>
  </g>

  <!-- Vertical divider -->
  <line x1="455" y1="60" x2="455" y2="260" stroke="#ccc" stroke-width="1.5" stroke-dasharray="4 4"/>

  <!-- ================== RIGHT PANEL: MLM ================== -->
  <g transform="translate(470, 0)">
    <text x="200" y="28" text-anchor="middle" font-size="16" font-weight="700" fill="#6a1b9a">
      Masked LM (BERT-style)
    </text>
    <text x="200" y="50" text-anchor="middle" font-size="12" font-style="italic" fill="#555">
      predict masked tokens from full bidirectional context
    </text>

    <!-- Token boxes: "The", "[MASK]", "sat", "[MASK]", "the", "mat" -->
    <g font-size="14" text-anchor="middle">
      <rect x="20"  y="80" width="60"  height="44" rx="6" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
      <text x="50"  y="108" fill="#4a148c">The</text>
      <rect x="90"  y="80" width="80"  height="44" rx="6" fill="#fff3e0" stroke="#e65100" stroke-width="2.5" stroke-dasharray="4 3"/>
      <text x="130" y="108" fill="#bf360c" font-size="12" font-weight="700">[MASK]</text>
      <rect x="180" y="80" width="60"  height="44" rx="6" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
      <text x="210" y="108" fill="#4a148c">sat</text>
      <rect x="250" y="80" width="80"  height="44" rx="6" fill="#fff3e0" stroke="#e65100" stroke-width="2.5" stroke-dasharray="4 3"/>
      <text x="290" y="108" fill="#bf360c" font-size="12" font-weight="700">[MASK]</text>
      <rect x="340" y="80" width="60"  height="44" rx="6" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
      <text x="370" y="108" fill="#4a148c">mat</text>
    </g>

    <!-- Bidirectional context arrows: both left and right inform each mask -->
    <g stroke="#6a1b9a" stroke-width="1.5" fill="none">
      <!-- Into first [MASK] at x=130 -->
      <path d="M 50 80 C 50 62, 130 62, 130 80" marker-end="url(#f621-arrow)"/>
      <path d="M 210 80 C 210 62, 130 62, 130 80" marker-end="url(#f621-arrow)"/>
      <!-- Into second [MASK] at x=290 -->
      <path d="M 210 80 C 210 64, 290 64, 290 80" marker-end="url(#f621-arrow)"/>
      <path d="M 370 80 C 370 64, 290 64, 290 80" marker-end="url(#f621-arrow)"/>
    </g>

    <!-- Loss label -->
    <text x="200" y="170" text-anchor="middle" font-size="13" fill="#333">
      <tspan font-style="italic">Loss:</tspan> minimize -log P(cat | context) - log P(on | context)
    </text>
    <text x="200" y="195" text-anchor="middle" font-size="11" fill="#666">
      Only masked positions contribute; context flows both ways.
    </text>
  </g>

  <!-- Bottom-of-figure summary line spanning both panels -->
  <line x1="20" y1="240" x2="880" y2="240" stroke="#ddd" stroke-width="1"/>
  <text x="450" y="265" text-anchor="middle" font-size="12" fill="#444">
    <tspan font-weight="700">Same architecture, different mask:</tspan>
    CLM uses a triangular mask (no future tokens);
    MLM uses no causal mask and predicts only the [MASK]ed positions.
  </text>
  <text x="450" y="288" text-anchor="middle" font-size="11" fill="#666" font-style="italic">
    GPT, Llama, Claude family = CLM. BERT, RoBERTa, DeBERTa family = MLM.
  </text>
</svg>
<div class="diagram-caption"><strong>Figure 6.2.1</strong>: Two pretraining objectives at the token level. <em>Causal language modeling</em> (left) predicts the next token from prior tokens only — the natural setup for autoregressive generation. <em>Masked language modeling</em> (right) hides random tokens and predicts them using bidirectional context — the natural setup for representation learning. Both objectives use the same Transformer backbone; only the attention mask and the loss differ.</div>
</div>'''


def find_fig_img(text: str, fig_num: str, old_src_sub: str):
    """Find the <img ...src=...> that is paired with Figure {fig_num}.
    Returns (start, end, old_tag) of the <img> element, or None."""
    pat = re.compile(
        r'(<img[^>]*src="[^"]*' + re.escape(old_src_sub) + r'[^"]*"[^>]*/?>)'
        r'(?:[^<]|<(?!img)[^>]*>)*?'
        r'<strong>Figure ' + re.escape(fig_num) + r'</strong>',
        re.DOTALL,
    )
    m = pat.search(text)
    if not m:
        return None
    return m.start(1), m.end(1), m.group(1)


def swap_img(rel: str, fig_num: str, old_src: str, new_src: str, new_alt: str) -> bool:
    p = ROOT / rel
    if not p.exists():
        print(f'  FILE MISSING: {rel}')
        return False
    text = p.read_text(encoding='utf-8')
    if new_src in text:
        print(f'  already swapped: Fig {fig_num}')
        return False
    target = find_fig_img(text, fig_num, old_src)
    if not target:
        print(f'  NO MATCH for Fig {fig_num} in {rel}')
        return False
    s, e, old_tag = target
    style_m = re.search(r'style="[^"]*"', old_tag)
    style = ' ' + style_m.group(0) if style_m else ' style="max-width: 100%; height: auto;"'
    new_tag = f'<img alt="{new_alt}" loading="lazy" src="{new_src}"{style}/>'
    new_text = text[:s] + new_tag + text[e:]
    p.write_text(new_text, encoding='utf-8')
    print(f'  swapped Fig {fig_num} -> {new_src}')
    return True


def replace_fig_621() -> bool:
    p = ROOT / 'part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html'
    text = p.read_text(encoding='utf-8')
    if 'fig621-title' in text:
        print('  already replaced: Fig 6.2.1')
        return False
    # Find the <figure class="illustration"> block whose caption is Figure 6.2.1
    pat = re.compile(
        r'<figure[^>]*>(?:.|\n)*?<strong>Figure 6\.2\.1</strong>(?:.|\n)*?</figure>\s*',
        re.IGNORECASE,
    )
    m = pat.search(text)
    if not m:
        print('  NO MATCH for Fig 6.2.1 <figure> block')
        return False
    span = m.end() - m.start()
    if span > 3000:
        print(f'  REFUSED: Fig 6.2.1 span {span} chars too large')
        return False
    new_text = text[:m.start()] + FIG_621_SVG_REPLACEMENT + '\n' + text[m.end():]
    p.write_text(new_text, encoding='utf-8')
    print(f'  replaced Fig 6.2.1 ({span} chars old, {len(FIG_621_SVG_REPLACEMENT)} chars new)')
    return True


def main() -> int:
    print('v6.12: swap 4 deferred chart conversions')
    fixed = 0
    for rel, fig, old_src, new_src, new_alt in SWAPS:
        if swap_img(rel, fig, old_src, new_src, new_alt):
            fixed += 1
    if replace_fig_621():
        fixed += 1
    print(f'\nSwapped {fixed}/4 deferred figures.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
