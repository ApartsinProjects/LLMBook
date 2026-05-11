"""Figure 5.2.4: Temperature controls the peakiness of a softmax distribution.

3-panel small-multiples bar chart showing softmax(logits/T) for the same
10-token candidate set at three temperatures: T=0.3, T=1.0, T=2.0.

This replaces the previous src=fig-5.2.3-top-p.png mismatch (the earlier
image was a top-p sampling diagram, not a temperature comparison).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from chart_style import apply_style, save_figure

import matplotlib.pyplot as plt
import numpy as np

apply_style()

# Synthetic logits roughly matching what an LLM might output for the next token
# after "The capital of France is". Sorted descending.
TOKENS = ['Paris', 'paris', 'France', 'the', 'a', 'France\'s', 'now', 'in', 'simply', 'often']
LOGITS = np.array([8.2, 6.5, 4.1, 3.8, 3.2, 2.7, 2.0, 1.5, 1.0, 0.5])

TEMPS = [0.3, 1.0, 2.0]
TITLES = [
    'T = 0.3   (sharpened — confident greedy)',
    'T = 1.0   (raw distribution)',
    'T = 2.0   (flattened — exploratory)',
]
COLORS = ['#1f77b4', '#2ca02c', '#d62728']

fig, axes = plt.subplots(1, 3, figsize=(13, 4.5), sharey=True)

for ax, T, title, color in zip(axes, TEMPS, TITLES, COLORS):
    scaled = LOGITS / T
    # Numerically stable softmax
    probs = np.exp(scaled - scaled.max())
    probs = probs / probs.sum()

    bars = ax.bar(range(len(TOKENS)), probs, color=color, alpha=0.85,
                  edgecolor='black', linewidth=0.7)
    ax.set_xticks(range(len(TOKENS)))
    ax.set_xticklabels(TOKENS, rotation=45, ha='right', fontsize=10)
    ax.set_title(title, fontsize=12, pad=10)
    ax.set_ylim(0, 1.0)
    ax.set_axisbelow(True)
    # Annotate top probability
    top_idx = int(np.argmax(probs))
    ax.text(top_idx, probs[top_idx] + 0.03, f'{probs[top_idx]:.2f}',
            ha='center', fontsize=10, color=color, fontweight='bold')

axes[0].set_ylabel('Probability  P(token)', fontsize=11)
fig.suptitle('Same logits, three temperatures', fontsize=14, fontweight='bold', y=1.02)
fig.text(0.5, -0.06,
         'Lower T concentrates probability on the top token (deterministic, "safe"). '
         'Higher T spreads it (creative, "risky").',
         ha='center', fontsize=10, style='italic', color='#444')

OUT = Path(__file__).resolve().parent.parent.parent / \
      'part-1-foundations/module-05-decoding-text-generation/images'
save_figure(fig, OUT / 'fig-5.2.4-temperature.png')
fig.savefig(OUT / 'fig-5.2.4-temperature.svg', format='svg',
            bbox_inches='tight', pad_inches=0.1, facecolor='white')
print(f'Saved SVG: {OUT}/fig-5.2.4-temperature.svg')
