"""Figure 6.4.3: Data curation funnel — Common Crawl to a clean training corpus.

Replaces / upgrades the generic data-pipeline cartoon. Shows token count at each
stage of the FineWeb-Edu / RedPajama-style curation pipeline. The y-axis is log
because the funnel removes 90%+ at each major stage.

Numbers are illustrative of FineWeb-Edu's reported magnitudes:
  raw Common Crawl text content -> URL dedup -> MinHash near-dedup ->
  language / quality filter -> classifier (educational score) -> final dataset.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from chart_style import apply_style, save_figure

import matplotlib.pyplot as plt
import numpy as np

apply_style()

# (stage label, token count in trillions, color, comment)
STAGES = [
    ('Raw web crawl\n(Common Crawl text)',         320.0, '#7d3c98', '~96 monthly dumps'),
    ('After URL +\nboilerplate stripping',         180.0, '#5b8def', 'remove duplicates and chrome'),
    ('After MinHash\nnear-deduplication',           65.0, '#1abc9c', 'fuzzy match across snapshots'),
    ('After language +\nquality heuristics',        28.0, '#2ecc71', 'rule filters + perplexity gate'),
    ('After educational\nclassifier (score ≥ 3)',    1.3, '#f39c12', 'small model rates each doc'),
    ('Final training\ncorpus',                       1.3, '#c0392b', 'what GPT-style pretraining sees'),
]

fig, ax = plt.subplots(figsize=(11, 6))

ys = np.arange(len(STAGES))
counts = [s[1] for s in STAGES]
labels = [s[0] for s in STAGES]
colors = [s[2] for s in STAGES]
notes  = [s[3] for s in STAGES]

bars = ax.barh(ys, counts, color=colors, alpha=0.85,
               edgecolor='black', linewidth=0.7, height=0.62)

# Annotate token count + reduction ratio
for i, (bar, n, note) in enumerate(zip(bars, counts, notes)):
    # Token count label (right of bar)
    if n >= 1:
        label = f'{n:.1f} T tokens' if n != round(n) else f'{int(n)} T tokens'
    else:
        label = f'{n*1000:.0f} B tokens'
    ax.text(bar.get_width() * 1.05, bar.get_y() + bar.get_height() / 2,
            label, va='center', ha='left',
            fontsize=11, color=colors[i], fontweight='bold')
    # Reduction vs previous stage
    if i > 0:
        ratio = counts[i - 1] / counts[i] if counts[i] > 0 else 0
        if ratio > 1.01:  # only annotate real reductions
            ax.text(bar.get_width() * 0.5, bar.get_y() + bar.get_height() / 2,
                    f'÷ {ratio:.1f}', va='center', ha='center',
                    fontsize=10, color='white', fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.25',
                              facecolor='#444', edgecolor='none', alpha=0.7))
    # Footnote
    ax.text(bar.get_width() * 1.05, bar.get_y() + bar.get_height() / 2 + 0.32,
            note, va='center', ha='left',
            fontsize=8.5, color='#666', style='italic')

ax.set_xscale('log')
ax.set_xlim(0.5, 1500)
ax.set_yticks(ys)
ax.set_yticklabels(labels, fontsize=10)
ax.invert_yaxis()
ax.set_xlabel('Token count (log scale)', fontsize=11)
ax.set_title('Data curation funnel: from raw web crawl to a training corpus',
             fontsize=13, pad=12)
ax.grid(True, axis='x', which='both', alpha=0.25)
ax.set_axisbelow(True)

fig.text(0.5, -0.04,
         'Each stage discards an order of magnitude of low-quality content. '
         'The final corpus is ~0.4% of the raw crawl — the rest is duplicates, '
         'boilerplate, non-English content, and low-educational-value pages.',
         ha='center', fontsize=10, style='italic', color='#444')

OUT = (Path(__file__).resolve().parent.parent.parent /
       'part-2-understanding-llms/module-06-pretraining-scaling-laws/images')
save_figure(fig, OUT / 'fig-6.4.3-curation-funnel.png')
fig.savefig(OUT / 'fig-6.4.3-curation-funnel.svg', format='svg',
            bbox_inches='tight', pad_inches=0.1, facecolor='white')
print(f'Saved SVG: {OUT}/fig-6.4.3-curation-funnel.svg')
