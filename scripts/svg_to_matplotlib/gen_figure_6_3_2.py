"""Figure 6.3.2: Power law in action — Hoffmann/Chinchilla scaling laws.

Replaces the Gemini cartoon `scaling-laws-power-law.png`. The audit finding
(_diagram_audit_v60.md #1) noted that the alt text already promised
"a log-log plot showing power law relationships between model
performance and scale factors" — but the image was a kitchen-metaphor
cartoon. This generates the actual chart.

Three power-law curves on a log-log plot:
  L(N) = E + A * N^(-alpha_N)   with alpha_N = 0.34, A = 406.4, E = 1.69
  L(D) = E + B * D^(-alpha_D)   with alpha_D = 0.28, B = 410.7, E = 1.69
  L(C) = E + K * C^(-alpha_C)   with alpha_C = 0.05, K = 2.0,   E = 1.69
(numbers chosen to match the qualitative form of Hoffmann 2022 Eq. (1))

Slopes are annotated on the plot; the irreducible-loss floor is shown
as a horizontal dashed line.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from chart_style import apply_style, save_figure
import matplotlib.pyplot as plt
import numpy as np

apply_style()

E = 1.69                         # irreducible loss
N = np.logspace(7, 11, 200)      # 10M -> 100B params
D = np.logspace(8, 12, 200)      # 100M -> 1T tokens
C = np.logspace(17, 24, 200)     # 1e17 -> 1e24 FLOPs

# Hoffmann 2022 form: L(N,D) = E + A/N^alpha + B/D^beta
# For the per-axis curves, use illustrative coefficients
L_N = E + 406.4 / (N ** 0.34)
L_D = E + 410.7 / (D ** 0.28)
L_C = E + 2.0   / (C ** 0.05)

fig, ax = plt.subplots(figsize=(10, 6))

# We want all three curves on one plot but their x-axes have different scales.
# Use a normalized "scale factor" axis (log10) so they all appear together.
ax.plot(np.log10(N), L_N, color='#1f77b4', lw=2.5,
        label=r'$L(N) = 1.69 + 406.4 \cdot N^{-0.34}$  — parameters')
ax.plot(np.log10(D), L_D, color='#2ca02c', lw=2.5, ls='--',
        label=r'$L(D) = 1.69 + 410.7 \cdot D^{-0.28}$  — training tokens')
ax.plot(np.log10(C), L_C, color='#d62728', lw=2.5, ls=':',
        label=r'$L(C) = 1.69 + 2.0 \cdot C^{-0.05}$  — compute (FLOPs)')

# Irreducible loss floor
ax.axhline(E, color='#888', ls='-.', lw=1.2, alpha=0.7)
ax.text(np.log10(N)[-1], E + 0.05, f'  irreducible loss E ≈ {E}',
        color='#666', fontsize=10, ha='right', va='bottom')

ax.set_yscale('log')
ax.set_xlabel('log10(scale factor)   — N (params), D (tokens), or C (FLOPs)', fontsize=11)
ax.set_ylabel('Test loss  L  (log scale)', fontsize=11)
ax.set_title('Power-law scaling of LLM test loss\n(Hoffmann et al. 2022, qualitative form)',
             fontsize=13, pad=12)
ax.legend(fontsize=10, loc='upper right', framealpha=0.95)
ax.grid(True, which='both', alpha=0.3)
ax.set_xlim(7, 24)

# Annotate slopes
ax.annotate('slope ≈ -0.34\n(parameters)', xy=(9, 4), xytext=(8, 8),
            color='#1f77b4', fontsize=9,
            arrowprops=dict(arrowstyle='->', color='#1f77b4', alpha=0.6))
ax.annotate('slope ≈ -0.05\n(compute, slower)', xy=(20, 1.85), xytext=(17, 2.4),
            color='#d62728', fontsize=9,
            arrowprops=dict(arrowstyle='->', color='#d62728', alpha=0.6))

OUT = Path(__file__).resolve().parent.parent.parent / \
      'part-2-understanding-llms/module-06-pretraining-scaling-laws/images'
save_figure(fig, OUT / 'fig-6.3.2-power-law.png')
fig.savefig(OUT / 'fig-6.3.2-power-law.svg', format='svg',
            bbox_inches='tight', pad_inches=0.1, facecolor='white')
print(f'Saved SVG: {OUT}/fig-6.3.2-power-law.svg')
