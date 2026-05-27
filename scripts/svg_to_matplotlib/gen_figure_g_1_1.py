"""Figure G.1.1: Hann vs Hamming vs rectangular windows over a 25 ms frame at 16 kHz."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from chart_style import apply_style, save_figure
import matplotlib.pyplot as plt
import numpy as np

apply_style()

fs = 16000
duration_ms = 25.0
N = int(fs * duration_ms / 1000.0)  # 400 samples
n = np.arange(N)
t_ms = n / fs * 1000.0

rect = np.ones(N)
hann = 0.5 * (1.0 - np.cos(2.0 * np.pi * n / (N - 1)))
hamming = 0.54 - 0.46 * np.cos(2.0 * np.pi * n / (N - 1))

fig, ax = plt.subplots(figsize=(10, 5.5))

ax.plot(t_ms, rect, color='#888888', linewidth=2.0, linestyle='--', label='Rectangular (no taper)')
ax.plot(t_ms, hamming, color='#e94560', linewidth=2.2, label='Hamming')
ax.plot(t_ms, hann, color='#1a4a80', linewidth=2.2, label='Hann')

ax.fill_between(t_ms, 0, hann, color='#1a4a80', alpha=0.08)

ax.set_xlabel('Time within frame (ms)', fontsize=12, color='#333')
ax.set_ylabel('Window amplitude $w[n]$', fontsize=12, color='#333')
ax.set_title('Hann, Hamming, and Rectangular windows over a 25 ms / 400-sample frame at 16 kHz',
             fontsize=13, color='#1a1a2e', pad=12)

ax.set_xlim(0, duration_ms)
ax.set_ylim(0, 1.15)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.legend(loc='lower center', frameon=True, fontsize=11)

ax.annotate('Hann reaches exactly 0\nat both endpoints',
            xy=(0.3, 0.0), xytext=(2.5, 0.35),
            fontsize=10, color='#1a4a80',
            arrowprops=dict(arrowstyle='->', color='#1a4a80', lw=1.0))
ax.annotate('Hamming leaves a\nsmall pedestal $\\approx 0.08$',
            xy=(24.7, 0.08), xytext=(15.5, 0.30),
            fontsize=10, color='#e94560',
            arrowprops=dict(arrowstyle='->', color='#e94560', lw=1.0))

out = os.path.abspath(os.path.join(os.path.dirname(__file__),
    '..', '..', 'appendices', 'appendix-g-signal-processing-audio', 'images',
    'fig-g.1.1-window-functions.png'))
save_figure(fig, out)
