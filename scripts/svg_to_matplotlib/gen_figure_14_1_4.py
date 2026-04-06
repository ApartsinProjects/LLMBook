"""Figure 14.1.4: Task performance vs general ability tradeoff."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from chart_style import *
apply_style()

fig, ax = plt.subplots(figsize=(10, 6))

from scipy.interpolate import make_interp_spline

# SVG axes: x=80..650, y=40..240
def svg_to_norm(sx, sy):
    nx = (np.array(sx) - 80) / (650 - 80) * 100
    ny = (240 - np.array(sy)) / (240 - 40) * 100
    return nx, ny

# Target task (rising): M 80 220 Q 200 200 300 120 Q 400 80 550 70 L 650 68
task_sx = [80, 200, 300, 400, 550, 650]
task_sy = [220, 200, 120, 80, 70, 68]
tx, ty = svg_to_norm(task_sx, task_sy)
spl_t = make_interp_spline(tx, ty, k=3)
x_sm = np.linspace(tx[0], tx[-1], 300)
y_task = spl_t(x_sm)

# General ability (falling): M 80 80 Q 200 85 300 110 Q 400 150 550 200 L 650 220
gen_sx = [80, 200, 300, 400, 550, 650]
gen_sy = [80, 85, 110, 150, 200, 220]
gx, gy = svg_to_norm(gen_sx, gen_sy)
spl_g = make_interp_spline(gx, gy, k=3)
y_gen = spl_g(x_sm)

ax.plot(x_sm, y_task, color='#4CAF50', linewidth=3, label='Target task')
ax.plot(x_sm, y_gen, color='#e94560', linewidth=3, label='General ability')

# Optimal zone
opt_left = (260 - 80) / (650 - 80) * 100
opt_right = (380 - 80) / (650 - 80) * 100
ax.axvspan(opt_left, opt_right, alpha=0.1, color='#FF9800',
           linestyle='--', linewidth=1, edgecolor='#FF9800')
ax.text((opt_left + opt_right) / 2, 98, 'Optimal zone', ha='center',
        fontsize=11, fontweight='bold', color='#E65100')

ax.set_xlabel('Training Steps', fontsize=12, color='#555')
ax.set_ylabel('Performance', fontsize=12, color='#555')
ax.set_xlim(-2, 102)
ax.set_ylim(-5, 105)
ax.set_xticks([])
ax.set_yticks([])
ax.legend(fontsize=11, loc='center right')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(False)

outpath = os.path.join(os.path.dirname(__file__),
    '../../part-4-training-adapting/module-14-fine-tuning-fundamentals/images/figure-14.1.4.png')
save_figure(fig, os.path.abspath(outpath))
