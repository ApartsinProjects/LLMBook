"""Figure G.2.1: FFT bin grid at N=512, fs=16 kHz; bin spacing = 31.25 Hz."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from chart_style import apply_style, save_figure
import matplotlib.pyplot as plt
import numpy as np

apply_style()

fs = 16000
N = 512
df = fs / N  # 31.25 Hz
nyq = fs / 2  # 8000 Hz
num_bins = N // 2 + 1  # 257 unique bins for real signal
bins = np.arange(num_bins)
freqs = bins * df

fig, ax = plt.subplots(figsize=(10, 5.5))

# Vertical lines for each bin (subsampled visually)
# Show every bin as a thin tick at the bottom
ax.vlines(freqs, 0, 0.18, color='#888', alpha=0.45, linewidth=0.5)

# Highlight a handful of named bins
highlight = [0, 1, 2, 8, 32, 64, 128, 192, 256]
for k in highlight:
    f = k * df
    ax.vlines(f, 0, 0.9, color='#1a4a80', linewidth=1.8)
    ax.plot(f, 0.9, marker='o', color='#1a4a80', markersize=6, zorder=5)
    label = f'$k={k}$\n${f:.2f}$ Hz' if k < 8 else f'$k={k}$\n${f:.0f}$ Hz'
    ax.text(f, 0.96, label, ha='center', va='bottom',
            fontsize=9, color='#1a1a2e')

# Annotation for bin spacing
ax.annotate('', xy=(2*df, 0.45), xytext=(1*df, 0.45),
            arrowprops=dict(arrowstyle='<->', color='#e94560', lw=1.2))
ax.text(1.5*df, 0.50, '$\\Delta f = 31.25$ Hz',
        ha='left', va='bottom', fontsize=10, color='#e94560')

# Mark Nyquist
ax.axvline(nyq, color='#27ae60', linewidth=1.5, linestyle='--', alpha=0.8)
ax.text(nyq, 1.30, 'Nyquist\n$f_s/2 = 8000$ Hz',
        ha='center', va='bottom', fontsize=10, color='#27ae60')

ax.set_xlabel('Frequency (Hz)', fontsize=12, color='#333')
ax.set_ylabel('FFT bin index (dimensionless)', fontsize=12, color='#333')
ax.set_title('FFT bin grid for $N=512$ at $f_s=16$ kHz: 257 unique bins, $\\Delta f = f_s/N = 31.25$ Hz',
             fontsize=12.5, color='#1a1a2e', pad=12)

ax.set_xlim(-100, nyq + 400)
ax.set_ylim(0, 1.45)
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.grid(False)

# Subtle x-grid only
ax.xaxis.grid(True, alpha=0.2)

out = os.path.abspath(os.path.join(os.path.dirname(__file__),
    '..', '..', 'appendices', 'appendix-g-signal-processing-audio', 'images',
    'fig-g.2.1-fft-bin-grid.png'))
save_figure(fig, out)
