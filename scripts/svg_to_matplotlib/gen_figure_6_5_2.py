"""Figure 6.5.2: Learning rate schedules — cosine decay + WSD.

Replaces the cartoon `learning-rate-warmup.png`. The audit (#3) noted
the data already exists in Code Fragments 6.5.2 and 6.5.3 in the same
section; we just need to plot it.

Two schedules on the same axes:
  - Linear warmup -> cosine decay to 10% of peak
  - WSD (Warmup-Stable-Decay): linear warmup, hold flat, then linear
    decay to 0
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from chart_style import apply_style, save_figure
import matplotlib.pyplot as plt
import numpy as np

apply_style()

TOTAL_STEPS = 10000
PEAK_LR = 3e-4
WARMUP_STEPS = 500
MIN_LR_FRAC = 0.1                       # cosine decays to 10% of peak

steps = np.arange(TOTAL_STEPS)

# Cosine schedule
def cosine_schedule(s):
    if s < WARMUP_STEPS:
        return PEAK_LR * (s + 1) / WARMUP_STEPS
    progress = (s - WARMUP_STEPS) / (TOTAL_STEPS - WARMUP_STEPS)
    return PEAK_LR * (MIN_LR_FRAC + (1 - MIN_LR_FRAC) * 0.5 * (1 + np.cos(np.pi * progress)))


# WSD schedule: warmup -> stable plateau -> decay to 0
STABLE_FRAC = 0.6                       # 60% of post-warmup is stable
def wsd_schedule(s):
    if s < WARMUP_STEPS:
        return PEAK_LR * (s + 1) / WARMUP_STEPS
    post_warmup = TOTAL_STEPS - WARMUP_STEPS
    stable_end = WARMUP_STEPS + int(STABLE_FRAC * post_warmup)
    if s < stable_end:
        return PEAK_LR
    decay_progress = (s - stable_end) / (TOTAL_STEPS - stable_end)
    return PEAK_LR * (1 - decay_progress)

cos_lr = np.array([cosine_schedule(s) for s in steps])
wsd_lr = np.array([wsd_schedule(s) for s in steps])

fig, ax = plt.subplots(figsize=(10, 5.5))

ax.plot(steps, cos_lr, color='#1f77b4', lw=2.5,
        label='Cosine decay (warmup → cosine to 10% of peak)')
ax.plot(steps, wsd_lr, color='#d62728', lw=2.5, ls='--',
        label='WSD (warmup → stable → linear decay to 0)')

# Annotate phases
ax.axvspan(0, WARMUP_STEPS, color='#fff3e0', alpha=0.7, label='_nolegend_')
ax.text(WARMUP_STEPS / 2, PEAK_LR * 1.05, 'warmup',
        ha='center', fontsize=10, color='#bf6000', style='italic')

ax.axvline(WARMUP_STEPS, color='#888', ls=':', lw=1, alpha=0.6)
stable_end_step = WARMUP_STEPS + int(STABLE_FRAC * (TOTAL_STEPS - WARMUP_STEPS))
ax.axvline(stable_end_step, color='#d62728', ls=':', lw=1, alpha=0.4)
ax.text(stable_end_step + 50, PEAK_LR * 0.7, 'WSD\ndecay\nbegins',
        fontsize=9, color='#d62728', style='italic')

ax.set_xlabel('Training step', fontsize=11)
ax.set_ylabel('Learning rate', fontsize=11)
ax.set_title(f'Learning rate schedules (peak LR = {PEAK_LR}, warmup = {WARMUP_STEPS} steps)',
             fontsize=13, pad=12)
ax.legend(fontsize=10, loc='center right', framealpha=0.95)
ax.grid(True, alpha=0.3)
ax.set_ylim(0, PEAK_LR * 1.15)

OUT = Path(__file__).resolve().parent.parent.parent / \
      'part-2-understanding-llms/module-06-pretraining-scaling-laws/images'
save_figure(fig, OUT / 'fig-6.5.2-lr-schedules.png')
fig.savefig(OUT / 'fig-6.5.2-lr-schedules.svg', format='svg',
            bbox_inches='tight', pad_inches=0.1, facecolor='white')
print(f'Saved SVG: {OUT}/fig-6.5.2-lr-schedules.svg')
