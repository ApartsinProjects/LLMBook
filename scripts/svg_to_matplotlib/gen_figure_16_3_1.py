"""Figure 16.3.1: Domain vs general performance - catastrophic forgetting."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from chart_style import *
apply_style()

fig, ax = plt.subplots(figsize=(10, 6))

from scipy.interpolate import make_interp_spline

# SVG axes: x=80..650, y=50..220
def svg_to_norm(sx, sy):
    nx = (np.array(sx) - 80) / (650 - 80) * 100
    ny = (220 - np.array(sy)) / (220 - 50) * 100
    return nx, ny

# Domain (rising): M 100 200 Q 200 190 300 140 Q 400 100 550 80 L 630 75
dom_sx = [100, 200, 300, 400, 550, 630]
dom_sy = [200, 190, 140, 100, 80, 75]
dx, dy = svg_to_norm(dom_sx, dom_sy)
spl_d = make_interp_spline(dx, dy, k=3)
x_sm = np.linspace(dx[0], dx[-1], 300)
y_dom = spl_d(x_sm)

# General (falling): M 100 80 Q 200 85 300 120 Q 400 160 550 190 L 630 200
gen_sx = [100, 200, 300, 400, 550, 630]
gen_sy = [80, 85, 120, 160, 190, 200]
gx, gy = svg_to_norm(gen_sx, gen_sy)
spl_g = make_interp_spline(gx, gy, k=3)
y_gen = spl_g(x_sm)

ax.plot(x_sm, y_dom, color='#2e7d32', linewidth=2.5, label='Domain')
ax.plot(x_sm, y_gen, color='#c62828', linewidth=2.5, label='General')

# Sweet spot
ss_left = (250 - 80) / (650 - 80) * 100
ss_right = (370 - 80) / (650 - 80) * 100
ss_mid = (ss_left + ss_right) / 2
ax.axvspan(ss_left, ss_right, alpha=0.15, color='#FFEB3B', edgecolor='#f9a825',
           linestyle='--', linewidth=1)
ax.text(ss_mid, 95, 'Sweet spot', ha='center', fontsize=11, fontweight='bold', color='#f57f17')

# Annotations
ax.text(10, -8, 'Under-adapted', fontsize=11, color='#888')
ax.text(78, -8, 'Over-adapted (forgotten)', fontsize=11, color='#888')

ax.set_xlabel('Training Steps on Domain Data', fontsize=12, color='#555')
ax.set_ylabel('Performance', fontsize=12, color='#555')
ax.set_xlim(-2, 102)
ax.set_ylim(-15, 105)
ax.set_xticks([])
ax.set_yticks([])
ax.legend(fontsize=11, loc='center right')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(False)

outpath = os.path.join(os.path.dirname(__file__),
    '../../part-4-training-adapting/module-16-distillation-merging/images/figure-16.3.1.png')
save_figure(fig, os.path.abspath(outpath))
