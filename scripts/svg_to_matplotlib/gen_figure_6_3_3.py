"""Figure 6.3.3: Chinchilla vs Kaplan compute-optimal scaling.

Replaces the cartoon `chinchilla-vs-kaplan.png`. The audit (#2) noted
this is the most practically consequential result in the chapter and
deserves a real chart.

Two curves of optimal model size N* (in params) vs compute budget C
(in FLOPs):
  Kaplan 2020 :  N* ∝ C^0.73  (overweights parameters; data scales as C^0.27)
  Chinchilla  :  N* ∝ C^0.50  (parameters and tokens scale equally)

Real models overlaid as scatter points to show where leading systems sit.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from chart_style import apply_style, save_figure
import matplotlib.pyplot as plt
import numpy as np

apply_style()

C = np.logspace(20, 25, 200)        # 1e20 -> 1e25 FLOPs

# Calibrate so both curves pass roughly through GPT-3 (175B params at ~3.14e23 FLOPs)
GPT3_C, GPT3_N = 3.14e23, 175e9
N_kaplan     = GPT3_N * (C / GPT3_C) ** 0.73
N_chinchilla = GPT3_N * (C / GPT3_C) ** 0.50

# Real models: (name, params, training_FLOPs)
MODELS = [
    ('GPT-3',          175e9, 3.14e23),
    ('Gopher',         280e9, 6.31e23),
    ('Chinchilla',      70e9, 5.76e23),
    ('PaLM',           540e9, 2.5e24),
    ('LLaMA 2 70B',     70e9, 1.7e24),
    ('LLaMA 3 70B',     70e9, 6.4e24),
    ('Llama 3.1 405B', 405e9, 3.8e25),
]

fig, ax = plt.subplots(figsize=(10.5, 6.5))

ax.loglog(C, N_kaplan,     color='#d62728', lw=2.5, ls='--',
          label=r'Kaplan 2020:  $N^* \propto C^{0.73}$  (model-heavy)')
ax.loglog(C, N_chinchilla, color='#1f77b4', lw=2.5,
          label=r'Chinchilla 2022:  $N^* \propto C^{0.50}$  (balanced)')

# Scatter real models
for name, n, c in MODELS:
    color = '#2ca02c' if name == 'Chinchilla' else '#444'
    ax.scatter([c], [n], color=color, s=80, zorder=5, edgecolor='black', lw=0.8)
    # Offset annotations to avoid overlap
    dx, dy = (1.4, 1.3) if name not in ('Chinchilla', 'Llama 3.1 405B') else (0.5, 0.7)
    ax.annotate(name, xy=(c, n), xytext=(c * dx, n * dy),
                fontsize=9, color='#222',
                arrowprops=dict(arrowstyle='-', color='#888', alpha=0.5, lw=0.7))

ax.set_xlabel('Training compute budget  $C$  (FLOPs, log)', fontsize=11)
ax.set_ylabel('Optimal model size  $N^*$  (parameters, log)', fontsize=11)
ax.set_title('Compute-optimal model scaling: Kaplan vs Chinchilla',
             fontsize=13, pad=12)
ax.legend(fontsize=10, loc='upper left', framealpha=0.95)
ax.grid(True, which='both', alpha=0.3)
ax.set_xlim(1e20, 1e26)
ax.set_ylim(1e9, 1e13)

# Annotate the gap
ax.text(1e24, 1.5e12,
        'Kaplan recommends bigger models;\nChinchilla recommends more data\nat the same compute.',
        fontsize=9, ha='center', style='italic', color='#555',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#fff8e1', edgecolor='#cca'))

OUT = Path(__file__).resolve().parent.parent.parent / \
      'part-2-understanding-llms/module-06-pretraining-scaling-laws/images'
save_figure(fig, OUT / 'fig-6.3.3-chinchilla-vs-kaplan.png')
fig.savefig(OUT / 'fig-6.3.3-chinchilla-vs-kaplan.svg', format='svg',
            bbox_inches='tight', pad_inches=0.1, facecolor='white')
print(f'Saved SVG: {OUT}/fig-6.3.3-chinchilla-vs-kaplan.svg')
