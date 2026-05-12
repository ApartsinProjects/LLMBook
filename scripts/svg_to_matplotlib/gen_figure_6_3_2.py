"""Figure 6.3.2: Power law in action — Hoffmann/Chinchilla scaling laws.

Replaces the Gemini cartoon `scaling-laws-power-law.png`.

DESIGN
Three power-law curves L(N), L(D), L(C) — but each lives on a DIFFERENT
x-axis range (params 1e7-1e11, tokens 1e8-1e12, compute 1e17-1e24). The
v6.0 design crammed all three onto a shared "log10(scale factor)" axis,
which produced three disjoint curve segments that never overlap and
confused readers into thinking they should be compared at common x-values.
The original also placed slope annotations at (8, 8) which is far above the
chart's y range, creating massive top margin.

This rewrite uses 3 side-by-side subplots so each curve has its own
properly-scaled x-axis. The shared y-axis (log scale) makes magnitudes
comparable. The irreducible loss floor is shown on each panel.

  L(N) = E + A * N^(-alpha_N)   alpha_N = 0.34, A = 406.4, E = 1.69
  L(D) = E + B * D^(-alpha_D)   alpha_D = 0.28, B = 410.7, E = 1.69
  L(C) = E + K * C^(-alpha_C)   alpha_C = 0.05, K = 2.0,   E = 1.69
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from chart_style import apply_style, save_figure

import matplotlib.pyplot as plt
import numpy as np

apply_style()

E = 1.69
N = np.logspace(7, 11, 200)
D = np.logspace(8, 12, 200)
C = np.logspace(17, 24, 200)

L_N = E + 406.4 / (N ** 0.34)
L_D = E + 410.7 / (D ** 0.28)
L_C = E + 2.0   / (C ** 0.05)

fig, axes = plt.subplots(1, 3, figsize=(13, 5), sharey=True)

PANELS = [
    (axes[0], N, L_N, '#1f77b4', '-',   'Parameters  N',
     r'$L(N) = E + A\,N^{-\alpha_N}$',  r'$\alpha_N = 0.34$', 'params'),
    (axes[1], D, L_D, '#2ca02c', '--',  'Training tokens  D',
     r'$L(D) = E + B\,D^{-\alpha_D}$',  r'$\alpha_D = 0.28$', 'tokens'),
    (axes[2], C, L_C, '#d62728', ':',   'Compute  C  (FLOPs)',
     r'$L(C) = E + K\,C^{-\alpha_C}$',  r'$\alpha_C = 0.05$', 'compute'),
]

for ax, x, y, color, ls, xlabel, eq, slope_label, _short in PANELS:
    ax.plot(x, y, color=color, lw=2.5, ls=ls)
    ax.axhline(E, color='#888', ls='-.', lw=1.0, alpha=0.7)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel(xlabel, fontsize=11)
    ax.grid(True, which='both', alpha=0.3)
    # Equation goes in the top-LEFT corner of each subplot, in axes coords.
    ax.text(0.04, 0.95, eq, transform=ax.transAxes,
            fontsize=11, color=color, fontweight='bold',
            va='top', ha='left',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='white',
                      edgecolor=color, alpha=0.85))
    # Slope label below the equation
    ax.text(0.04, 0.84, slope_label, transform=ax.transAxes,
            fontsize=10, color=color, va='top', ha='left')

# Mark the irreducible-loss floor on the LEFT panel only, to avoid
# duplicating the same label across all three.
axes[0].text(N[0] * 1.15, E * 1.02, f'irreducible loss  $E \\approx {E}$',
             color='#666', fontsize=9, va='bottom', ha='left')

axes[0].set_ylabel('Test loss  $L$  (log scale)', fontsize=11)
fig.suptitle('Power-law scaling of LLM test loss '
             '(Hoffmann et al. 2022, qualitative form)',
             fontsize=13)
fig.tight_layout(rect=[0, 0, 1, 0.95])

OUT = (Path(__file__).resolve().parent.parent.parent /
       'part-2-understanding-llms/module-06-pretraining-scaling-laws/images')
save_figure(fig, OUT / 'fig-6.3.2-power-law.png')
fig.savefig(OUT / 'fig-6.3.2-power-law.svg', format='svg',
            bbox_inches='tight', pad_inches=0.1, facecolor='white')
print(f'Saved SVG: {OUT}/fig-6.3.2-power-law.svg')
