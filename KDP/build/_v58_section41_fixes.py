"""v5.8: section-4.1.html targeted fixes.

A. Fix 3 figures whose <img src> points to the wrong image:
   - Figure 4.1.3: caption is "encoder-decoder Transformer" but src is
     fig-4.1.4-pos-encoding.png. Swap to transformer-architecture-vaswani2017.png
     (the original Vaswani 2017 architecture figure that already exists).
   - Figure 4.1.5: caption is "Post-LN/Pre-LN" but src is fig-4.1.8-causal-mask.png.
     Swap to fig-4.1.7-pre-post-ln.png (correct image, just renamed).
   - Figure 4.1.7: caption is "residual stream perspective" but src is
     fig-4.1.7-pre-post-ln.png. Swap to fig-4.1.7-residual-stream.png.

B. Redesign Figure 4.1.6 (residual stream) as a proper SVG showing
   the branch-and-merge pattern that makes residuals intuitive:
     - A horizontal "residual stream" highway at top
     - Each sub-layer (Attn / FFN) branches DOWN from the stream
     - Sub-layer output flows BACK UP and is ADDED into the stream (+ node)
   The current inline HTML diagram is a flat horizontal pipeline that
   doesn't show the bypass-and-add structure.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SECTION = ROOT / "part-1-foundations/module-04-transformer-architecture/section-4.1.html"


# Three image-src swaps. Use very specific substring patterns that include the
# diagram-caption text so we can't accidentally swap the wrong figure.

SWAPS = [
    # Figure 4.1.3 (encoder-decoder Transformer): file says pos-encoding, alt says
    # pos-encoding too — both wrong. Swap to transformer-architecture-vaswani2017.png
    # with proper alt.
    (
        '<img alt="Positional encoding: low dimensions oscillate fast, high dimensions change slowly" loading="lazy" src="images/fig-4.1.4-pos-encoding.png"',
        '<img alt="High-level encoder-decoder Transformer with stacked attention and feed-forward sub-layers, each wrapped in a residual connection and LayerNorm" loading="lazy" src="images/transformer-architecture-vaswani2017.png"',
        1,
    ),
    # Figure 4.1.4 (positional encoding): src is correct, but alt was swapped
    # in. Restore the right alt text.
    (
        '<img alt="Post-LN normalizes after residual; Pre-LN normalizes before the sub-layer" loading="lazy" src="images/fig-4.1.4-pos-encoding.png"',
        '<img alt="Positional encoding heatmap: each row is a token position, each column a dimension; low-index dimensions oscillate quickly, high-index dimensions change slowly" loading="lazy" src="images/fig-4.1.4-pos-encoding.png"',
        1,
    ),
    # Figure 4.1.5 (Post-LN vs Pre-LN): src says causal-mask (wrong file),
    # alt says causal mask too. Swap both.
    (
        '<img alt="Causal lower-triangular attention mask: each position attends only to previous positions" loading="lazy" src="images/fig-4.1.8-causal-mask.png"',
        '<img alt="Post-LN (left) applies LayerNorm after the residual addition; Pre-LN (right) applies LayerNorm before each sub-layer, which produces more stable gradients in deep models" loading="lazy" src="images/fig-4.1.7-pre-post-ln.png"',
        1,
    ),
    # Figure 4.1.7 — already fixed in prior run; keep idempotent guard.
    (
        '<img alt="Residual stream perspective: attention and FFN sub-layers read from and write back to a shared communication channel" loading="lazy" src="images/fig-4.1.7-pre-post-ln.png"',
        '<img alt="Residual stream perspective: attention and FFN sub-layers read from and write back to a shared communication channel" loading="lazy" src="images/fig-4.1.7-residual-stream.png"',
        1,
    ),
]


# New SVG for Figure 4.1.6 that shows the branch-and-merge structure.
# Strategy: horizontal "residual stream" highway at top. Each sub-layer drops
# down, processes, and merges back via a + node.
NEW_FIG_416_SVG = '''<!-- Figure 4.1.6: Residual stream as branch-and-merge SVG (v5.8 redesign) -->
<div class="diagram-container">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 360" role="img" aria-labelledby="fig416-title fig416-desc" style="max-width:100%; height:auto;">
  <title id="fig416-title">The residual stream as a communication highway</title>
  <desc id="fig416-desc">A horizontal residual stream runs across the top. Two sub-layers (Attention, FFN) each branch downward from the stream, perform their computation, and merge their output back into the stream via a plus node. This shows that each sub-layer reads from and writes additively to a shared vector, rather than transforming a single hidden state in series.</desc>

  <defs>
    <marker id="fig416-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#444"/>
    </marker>
    <marker id="fig416-arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#1565c0"/>
    </marker>
  </defs>

  <!-- THE RESIDUAL STREAM (horizontal highway) -->
  <line x1="20"  y1="80" x2="900" y2="80" stroke="#1565c0" stroke-width="6" stroke-linecap="round"/>
  <text x="460" y="40" text-anchor="middle" font-family="sans-serif" font-size="18" font-weight="bold" fill="#1565c0">Residual stream (shared vector x)</text>
  <text x="460" y="62" text-anchor="middle" font-family="sans-serif" font-size="13" fill="#555" font-style="italic">each sub-layer reads from and writes additively into this stream</text>

  <!-- INPUT (left edge) -->
  <rect x="20" y="100" width="100" height="44" rx="6" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="70" y="127" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="#0d47a1">x_embed</text>
  <line x1="70" y1="100" x2="70" y2="83" stroke="#1565c0" stroke-width="2" marker-end="url(#fig416-arrow-blue)"/>

  <!-- BLOCK 1: ATTENTION -->
  <!-- Branch down -->
  <line x1="240" y1="83" x2="240" y2="170" stroke="#6a1b9a" stroke-width="2" marker-end="url(#fig416-arrow)"/>
  <text x="222" y="110" text-anchor="end" font-family="sans-serif" font-size="11" fill="#6a1b9a">read x</text>
  <!-- Sub-layer box -->
  <rect x="180" y="170" width="140" height="56" rx="6" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="250" y="194" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="#4a148c">Attention</text>
  <text x="250" y="214" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#6a1b9a">Attn(x)</text>
  <!-- Merge back up to + -->
  <line x1="250" y1="170" x2="250" y2="170" stroke="none"/>
  <path d="M 250 226 L 250 250 L 320 250 L 320 100" stroke="#6a1b9a" stroke-width="2" fill="none" marker-end="url(#fig416-arrow)"/>
  <text x="335" y="180" text-anchor="start" font-family="sans-serif" font-size="11" fill="#6a1b9a">write Attn(x)</text>
  <!-- + node on the stream -->
  <circle cx="320" cy="80" r="14" fill="#fff" stroke="#6a1b9a" stroke-width="2.5"/>
  <text x="320" y="86" text-anchor="middle" font-family="sans-serif" font-size="20" font-weight="bold" fill="#6a1b9a">+</text>
  <text x="320" y="20" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#6a1b9a">x ← x + Attn(x)</text>

  <!-- BLOCK 2: FFN -->
  <line x1="500" y1="83" x2="500" y2="170" stroke="#e65100" stroke-width="2" marker-end="url(#fig416-arrow)"/>
  <text x="482" y="110" text-anchor="end" font-family="sans-serif" font-size="11" fill="#e65100">read x</text>
  <rect x="440" y="170" width="140" height="56" rx="6" fill="#fff3e0" stroke="#e65100" stroke-width="2"/>
  <text x="510" y="194" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="#bf360c">FFN</text>
  <text x="510" y="214" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#e65100">FFN(x)</text>
  <path d="M 510 226 L 510 250 L 580 250 L 580 100" stroke="#e65100" stroke-width="2" fill="none" marker-end="url(#fig416-arrow)"/>
  <text x="595" y="180" text-anchor="start" font-family="sans-serif" font-size="11" fill="#e65100">write FFN(x)</text>
  <circle cx="580" cy="80" r="14" fill="#fff" stroke="#e65100" stroke-width="2.5"/>
  <text x="580" y="86" text-anchor="middle" font-family="sans-serif" font-size="20" font-weight="bold" fill="#e65100">+</text>
  <text x="580" y="20" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#e65100">x ← x + FFN(x)</text>

  <!-- Ellipsis showing more layers -->
  <text x="710" y="86" text-anchor="middle" font-family="sans-serif" font-size="20" fill="#777" font-weight="bold">. . .</text>
  <text x="710" y="115" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#777" font-style="italic">N more blocks</text>

  <!-- OUTPUT (right edge) -->
  <rect x="800" y="100" width="100" height="44" rx="6" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="850" y="127" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="#1b5e20">Output</text>
  <line x1="850" y1="83" x2="850" y2="100" stroke="#2e7d32" stroke-width="2" marker-end="url(#fig416-arrow)"/>

  <!-- LEGEND -->
  <g transform="translate(20,290)">
    <text x="0" y="0" font-family="sans-serif" font-size="13" font-weight="bold" fill="#333">Reading the diagram:</text>
    <text x="0" y="20" font-family="sans-serif" font-size="12" fill="#444">&#8226; The blue highway is the residual stream — a single shared vector x that flows from input to output.</text>
    <text x="0" y="38" font-family="sans-serif" font-size="12" fill="#444">&#8226; Each sub-layer (Attention, FFN) <tspan font-style="italic">branches down</tspan>, computes its function on x, then <tspan font-style="italic">merges back up</tspan>: the new x is x + sub-layer(x).</text>
    <text x="0" y="56" font-family="sans-serif" font-size="12" fill="#444">&#8226; The stream itself is never replaced — sub-layers only ever <tspan font-weight="bold">add</tspan> to it. This is what makes the residual stream a "communication channel" between distant layers.</text>
  </g>
</svg>
<div class="diagram-caption"><strong>Figure 4.1.6</strong>: The residual stream as a branch-and-merge highway. Each sub-layer (Attention, FFN) reads the current stream, computes its contribution, and adds it back. The stream is never overwritten — sub-layers can only add. This is why information from early layers reaches late layers directly, and why deleting a layer often degrades the model less than expected.</div>
</div>'''


def main() -> int:
    text = SECTION.read_text(encoding="utf-8")
    original = text
    edits = 0

    # A. Three image-src swaps
    for old, new, max_count in SWAPS:
        if old in text:
            text = text.replace(old, new, max_count)
            edits += 1
            print(f'  swapped img: {old[-50:]} -> {new[-50:]}')
        else:
            print(f'  WARNING: src pattern not found: {old[-60:]}')

    # B. Replace the inline HTML diagram for Figure 4.1.6 with the new SVG.
    OLD_BLOCK_PAT = re.compile(
        r'<!--\s*Figure 4\.1\.6[^>]*-->\s*'
        r'<div class="diagram-container">.*?'
        r'<div class="diagram-caption"><strong>Figure 4\.1\.6</strong>:.*?</div>\s*'
        r'</div>',
        re.DOTALL,
    )
    if OLD_BLOCK_PAT.search(text):
        text = OLD_BLOCK_PAT.sub(NEW_FIG_416_SVG, text, count=1)
        edits += 1
        print('  redesigned Figure 4.1.6 as branch-and-merge SVG')
    else:
        print('  WARNING: Figure 4.1.6 block not found')

    if text != original:
        SECTION.write_text(text, encoding="utf-8")
    print(f'\nTotal edits: {edits}')
    return 0


if __name__ == "__main__":
    sys.exit(main())
