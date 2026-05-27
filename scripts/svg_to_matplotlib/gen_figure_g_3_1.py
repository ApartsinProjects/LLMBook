"""Figure G.3.1: Mel filter bank with 10 triangular filters over a linear-frequency axis."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from chart_style import apply_style, save_figure
import matplotlib.pyplot as plt
import numpy as np

apply_style()

fs = 16000
fmin = 0.0
fmax = fs / 2  # 8000 Hz
M = 10  # number of mel filters

def hz_to_mel(f):
    return 2595.0 * np.log10(1.0 + f / 700.0)

def mel_to_hz(m):
    return 700.0 * (10.0 ** (m / 2595.0) - 1.0)

# Edges on mel scale -> back to Hz
mel_min = hz_to_mel(fmin)
mel_max = hz_to_mel(fmax)
mel_pts = np.linspace(mel_min, mel_max, M + 2)
hz_pts = mel_to_hz(mel_pts)  # M+2 points; each filter uses (i-1, i, i+1)

freqs = np.linspace(0, fmax, 4000)

fig, ax = plt.subplots(figsize=(10, 5.5))

palette = ['#1a4a80', '#e94560', '#27ae60', '#f39c12', '#6a1b9a',
           '#1a4a80', '#e94560', '#27ae60', '#f39c12', '#6a1b9a']

for i in range(M):
    fl, fc, fr = hz_pts[i], hz_pts[i + 1], hz_pts[i + 2]
    H = np.zeros_like(freqs)
    left = (freqs >= fl) & (freqs <= fc)
    right = (freqs >= fc) & (freqs <= fr)
    H[left] = (freqs[left] - fl) / (fc - fl + 1e-12)
    H[right] = (fr - freqs[right]) / (fr - fc + 1e-12)
    ax.plot(freqs, H, color=palette[i], linewidth=1.5, alpha=0.95)
    ax.fill_between(freqs, 0, H, color=palette[i], alpha=0.15)
    # Center label
    ax.text(fc, 1.04, f'{i+1}', ha='center', va='bottom',
            fontsize=9, color=palette[i], fontweight='bold')

# Annotation: low-frequency triangles are narrow and close; high-frequency are wide and far apart
ax.annotate('Narrow, dense filters\n(linear region of mel scale)',
            xy=(400, 0.5), xytext=(1400, 0.80),
            fontsize=10, color='#1a4a80',
            arrowprops=dict(arrowstyle='->', color='#1a4a80', lw=1.0))
ax.annotate('Wide, sparse filters\n(log region of mel scale)',
            xy=(6500, 0.5), xytext=(3300, 0.80),
            fontsize=10, color='#6a1b9a',
            arrowprops=dict(arrowstyle='->', color='#6a1b9a', lw=1.0))

ax.set_xlabel('Frequency (Hz, linear scale)', fontsize=12, color='#333')
ax.set_ylabel('Triangular filter weight $H_i(f)$', fontsize=12, color='#333')
ax.set_title('Mel filter bank (10 bands) on a linear frequency axis: equal spacing in mel becomes log-uniform spacing in Hz',
             fontsize=11.5, color='#1a1a2e', pad=12)

ax.set_xlim(0, fmax)
ax.set_ylim(0, 1.18)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

out = os.path.abspath(os.path.join(os.path.dirname(__file__),
    '..', '..', 'appendices', 'appendix-g-signal-processing-audio', 'images',
    'fig-g.3.1-mel-filter-bank.png'))
save_figure(fig, out)
