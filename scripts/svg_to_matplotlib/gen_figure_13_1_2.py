"""Figure 13.1.2: Annotation cost per training example, by sourcing method.

Replaces the seed-data garden cartoon flagged by the v6.0 audit.
Horizontal bar chart on a LOG scale (the spread covers four orders of
magnitude). Each method has a range bar showing min-max cost.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from chart_style import apply_style, save_figure

import matplotlib.pyplot as plt
import numpy as np

apply_style()

# (method, low_cost, high_cost, color, footnote)
METHODS = [
    ('Expert annotator\n(domain specialist)',     5.00,  20.00,   '#c62828',
     'medical, legal, ML researcher'),
    ('Crowdsourced\n(Mechanical Turk, Scale)',    0.10,   0.50,   '#f39c12',
     'short-task workers w/ quality control'),
    ('LLM API\n(GPT-4o, Claude)',                 0.005,  0.020,  '#27ae60',
     'self-instruct, distill-from-frontier'),
    ('Self-hosted small LLM\n(Llama-3.1-8B on 1× H100)',
                                                  0.0005, 0.002,  '#1f77b4',
     'open weights, dedicated GPU'),
]

fig, ax = plt.subplots(figsize=(10, 5.5))

ys = np.arange(len(METHODS))
for i, (name, low, high, color, note) in enumerate(METHODS):
    ax.barh(i, high - low, left=low, color=color, alpha=0.55, height=0.55,
            edgecolor=color, linewidth=2)
    # Mid-point marker
    mid = np.sqrt(low * high)  # geometric mean (visually centered on log scale)
    ax.plot([mid], [i], 'o', color=color, markersize=10,
            markeredgecolor='white', markeredgewidth=1.5, zorder=5)
    # Label the range to the right
    label = (f'\${low:.4g} – \${high:.4g}' if low < 0.01
             else f'\${low:.3g} – \${high:.3g}')
    ax.text(high * 1.4, i, label,
            va='center', ha='left', fontsize=10, color=color, fontweight='bold')
    # Subtle footnote under the bar
    ax.text(low * 0.7, i - 0.32, note, va='center', ha='left',
            fontsize=8.5, color='#666', style='italic')

ax.set_xscale('log')
ax.set_xlim(0.0002, 200)
ax.set_yticks(ys)
ax.set_yticklabels([m[0] for m in METHODS], fontsize=10)
ax.invert_yaxis()
ax.set_xlabel('Cost per training example (USD, log scale)', fontsize=11)
ax.set_title('Annotation cost per example across sourcing methods',
             fontsize=13, pad=24)
# Subtitle line below the main title, well above the first bar.
ax.text(0.5, 1.04, '~10,000× cost spread end-to-end',
        transform=ax.transAxes, ha='center', va='bottom',
        fontsize=10, color='#666', style='italic')
ax.grid(True, axis='x', which='both', alpha=0.25)
ax.set_axisbelow(True)

OUT = (Path(__file__).resolve().parent.parent.parent /
       'part-4-training-adapting/module-13-synthetic-data/images')
save_figure(fig, OUT / 'fig-13.1.2-annotation-cost.png')
fig.savefig(OUT / 'fig-13.1.2-annotation-cost.svg', format='svg',
            bbox_inches='tight', pad_inches=0.1, facecolor='white')
print(f'Saved SVG: {OUT}/fig-13.1.2-annotation-cost.svg')
