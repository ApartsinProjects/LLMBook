"""Figure 8.1.2: Train-time vs test-time compute scaling curves."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from chart_style import *
apply_style()

fig, ax = plt.subplots(figsize=(10, 6))

from scipy.interpolate import PchipInterpolator

# SVG axes: x=100..700, y=60..350
# Train-time: M120,320 C200,280 350,180 680,120
# Test-time: M120,320 C180,260 280,140 500,85
# Combined: M120,320 C170,240 250,120 450,55

def svg_to_norm(sx, sy, xr=(100, 700), yr=(60, 350)):
    nx = (np.array(sx) - xr[0]) / (xr[1] - xr[0]) * 10
    ny = (yr[1] - np.array(sy)) / (yr[1] - yr[0]) * 100
    return nx, ny

x = np.linspace(0.3, 10, 300)

# Train-time curve
tt_sx = [120, 200, 300, 450, 600, 680]
tt_sy = [320, 280, 230, 180, 140, 120]
ttx, tty = svg_to_norm(tt_sx, tt_sy)
spl_tt = PchipInterpolator(ttx, tty)
y_train = spl_tt(x)

# Test-time curve
ts_sx = [120, 180, 250, 350, 450, 500]
ts_sy = [320, 275, 200, 140, 95, 85]
tsx, tsy = svg_to_norm(ts_sx, ts_sy)
spl_ts = PchipInterpolator(tsx, tsy)
x_ts = np.linspace(tsx[0], tsx[-1], 200)
y_test = spl_ts(x_ts)

# Combined curve
cb_sx = [120, 170, 220, 300, 400, 450]
cb_sy = [320, 260, 190, 120, 70, 55]
cbx, cby = svg_to_norm(cb_sx, cb_sy)
spl_cb = PchipInterpolator(cbx, cby)
x_cb = np.linspace(cbx[0], cbx[-1], 200)
y_comb = spl_cb(x_cb)

ax.plot(x, y_train, color='#8e44ad', linewidth=3, label='Train-time scaling (bigger model, single pass)')
ax.plot(x_ts, y_test, color='#27ae60', linewidth=3, label='Test-time scaling (same model, more thinking)')
ax.plot(x_cb, y_comb, color='#e94560', linewidth=3, linestyle='--', label='Combined (larger model + thinking)')

# Annotated points
pt_7b_x, pt_7b_y = svg_to_norm([250], [260])
pt_70b_x, pt_70b_y = svg_to_norm([450], [170])
pt_7b_256_x, pt_7b_256_y = svg_to_norm([250], [180])

ax.plot(pt_7b_x[0], pt_7b_y[0], 'o', color='#8e44ad', markersize=8, zorder=5)
ax.annotate('7B model', xy=(pt_7b_x[0], pt_7b_y[0]), xytext=(10, 5),
            textcoords='offset points', fontsize=10, color='#555')

ax.plot(pt_70b_x[0], pt_70b_y[0], 'o', color='#8e44ad', markersize=8, zorder=5)
ax.annotate('70B model', xy=(pt_70b_x[0], pt_70b_y[0]), xytext=(10, 5),
            textcoords='offset points', fontsize=10, color='#555')

ax.plot(pt_7b_256_x[0], pt_7b_256_y[0], 'o', color='#27ae60', markersize=8, zorder=5)
ax.annotate('7B + 256 samples', xy=(pt_7b_256_x[0], pt_7b_256_y[0]),
            xytext=(10, 10), textcoords='offset points', fontsize=10, color='#555')

# Equivalence line
ax.plot([pt_7b_256_x[0], pt_70b_x[0]], [pt_7b_256_y[0], pt_70b_y[0]],
        '--', color='#333', linewidth=1, alpha=0.5)
mid_x = (pt_7b_256_x[0] + pt_70b_x[0]) / 2
mid_y = (pt_7b_256_y[0] + pt_70b_y[0]) / 2 - 3
ax.text(mid_x, mid_y, 'Similar compute, similar accuracy',
        ha='center', fontsize=10, color='#333')

ax.set_xlabel('Total Compute (FLOPs per query)', fontsize=12, color='#555')
ax.set_ylabel('Performance (Accuracy)', fontsize=12, color='#555')
ax.set_xticks([])
ax.set_yticks([])
ax.legend(fontsize=10, loc='lower right')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(False)

outpath = os.path.join(os.path.dirname(__file__),
    '../../part-2-understanding-llms/module-08-reasoning-test-time-compute/images/figure-8.1.2.png')
save_figure(fig, os.path.abspath(outpath))
