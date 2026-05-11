"""Figure 33.1.1: AI Readiness — converted from radar chart to horizontal bar.

(v6.3 redesign — was a 4-axis radar before. Audit finding #10 noted that
radars with fewer than 6 axes systematically distort relative magnitudes
through quadratic area scaling. A horizontal bar chart with a "minimum
viable" reference line at 3 makes the weakest pillar immediately scannable.)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from chart_style import apply_style, save_figure
import matplotlib.pyplot as plt
import numpy as np

apply_style()

PILLARS = ['Talent\n(ML eng + product)',
           'Org Culture\n(experimentation, change mgmt)',
           'Tech Infra\n(GPUs, MLOps, data pipes)',
           'Data Maturity\n(quality, lineage, governance)']
SCORES  = [3, 2, 3, 4]
COLORS  = ['#2980b9', '#e74c3c', '#27ae60', '#f39c12']

fig, ax = plt.subplots(figsize=(10, 5.5))

bars = ax.barh(PILLARS, SCORES, color=COLORS, alpha=0.85,
               edgecolor='black', linewidth=0.8, height=0.55)

for bar, score, color in zip(bars, SCORES, COLORS):
    ax.text(bar.get_width() + 0.08, bar.get_y() + bar.get_height() / 2,
            f'{score} / 5',
            va='center', fontsize=11, color=color, fontweight='bold')

ax.axvline(3, color='#666', ls='--', lw=1.5, alpha=0.7)
ax.text(3, len(PILLARS) - 0.4, '  minimum viable (3 / 5)',
        fontsize=10, color='#444', style='italic', va='top')

ax.set_xlim(0, 5.5)
ax.set_xlabel('Readiness score (0 = absent, 5 = world-class)', fontsize=11)
ax.set_title('AI Readiness Pillars — example mid-size fintech',
             fontsize=13, pad=12)
ax.set_xticks([0, 1, 2, 3, 4, 5])
ax.set_axisbelow(True)
ax.grid(True, axis='x', alpha=0.3)

# Highlight weakest pillar
weakest_idx = SCORES.index(min(SCORES))
ax.text(0.05, weakest_idx, '  ← lowest pillar:\n  invest here first',
        fontsize=9, color='#c0392b', style='italic', va='center', fontweight='bold')

OUT = Path(__file__).resolve().parent.parent.parent / \
      'part-9-safety-strategy/module-33-strategy-product-roi/images'
save_figure(fig, OUT / 'fig-33.1.1-ai-readiness-bars.png')
fig.savefig(OUT / 'fig-33.1.1-ai-readiness-bars.svg', format='svg',
            bbox_inches='tight', pad_inches=0.1, facecolor='white')
print(f'Saved SVG: {OUT}/fig-33.1.1-ai-readiness-bars.svg')
