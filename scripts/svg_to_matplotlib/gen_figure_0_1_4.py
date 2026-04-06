"""Figure 0.1.4: Bias-variance tradeoff chart."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from chart_style import *
apply_style()

fig, ax = plt.subplots(figsize=(10, 6))

# From SVG (viewBox 0 0 630 380, axes at x=80..550, y=55..310):
# Bias curve: M 100,100 Q 200,130 300,220 Q 400,275 530,290
# Variance curve: M 100,290 Q 200,278 300,230 Q 400,150 530,80
# Total error: M 100,120 Q 180,180 260,230 Q 300,245 340,235 Q 420,200 530,140
# Noise floor: y=295 horizontal

x = np.linspace(0, 10, 300)

# Bias^2: decreasing curve
# SVG points normalized (x: 100..530 -> 0..10, y: 55..310 -> invert to 0..10)
def svg_to_norm(sx, sy, x_range=(100, 530), y_range=(55, 310)):
    nx = (np.array(sx) - x_range[0]) / (x_range[1] - x_range[0]) * 10
    ny = (y_range[1] - np.array(sy)) / (y_range[1] - y_range[0]) * 10
    return nx, ny

from scipy.interpolate import make_interp_spline

# Bias^2
bx, by = svg_to_norm([100, 200, 300, 400, 530], [100, 130, 220, 275, 290])
bias_spline = make_interp_spline(bx, by, k=3)
bias_y = bias_spline(x)

# Variance
vx, vy = svg_to_norm([100, 200, 300, 400, 530], [290, 278, 230, 150, 80])
var_spline = make_interp_spline(vx, vy, k=3)
var_y = var_spline(x)

# Total error
tx, ty = svg_to_norm([100, 180, 260, 300, 340, 420, 530], [120, 180, 230, 245, 235, 200, 140])
total_spline = make_interp_spline(tx, ty, k=3)
total_y = total_spline(x)

# Noise floor at y_svg=295
_, noise_vals = svg_to_norm([100], [295])
noise_level = noise_vals[0]

ax.plot(x, bias_y, color='#3498db', linewidth=2.5, linestyle='--', label='Bias$^2$')
ax.plot(x, var_y, color='#e94560', linewidth=2.5, linestyle='--', label='Variance')
ax.plot(x, total_y, color='#1a1a2e', linewidth=3, label='Total Error')
ax.axhline(y=noise_level, color='#aaaaaa', linewidth=1.5, linestyle=':', label='Noise floor')

# Optimal point at SVG (300, 245)
opt_x, opt_y = svg_to_norm([300], [245])
ax.plot(opt_x[0], opt_y[0], 'o', color='#27ae60', markersize=10, zorder=5)
ax.axvline(x=opt_x[0], color='#27ae60', linewidth=1.5, linestyle='--', alpha=0.5)
ax.text(opt_x[0], opt_y[0] - 0.8, 'Optimal', ha='center', fontsize=12, fontweight='bold', color='#27ae60')

# Region labels
ax.text(1.5, 9.0, 'Underfitting', fontsize=11, color='#3498db',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#e8f4fd', edgecolor='#3498db', alpha=0.9))
ax.text(7.5, 9.0, 'Overfitting', fontsize=11, color='#e94560',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#fef9e7', edgecolor='#e94560', alpha=0.9))

ax.set_xlabel('Model Complexity \u2192', fontsize=12, color='#555')
ax.set_ylabel('Error', fontsize=12, color='#555')
ax.set_xlim(-0.2, 10.2)
ax.set_ylim(-0.5, 10.5)
ax.set_xticks([])
ax.set_yticks([])
ax.legend(loc='right', fontsize=11)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#999')
ax.spines['bottom'].set_color('#999')
ax.grid(False)

outpath = os.path.join(os.path.dirname(__file__),
    '../../part-1-foundations/module-00-ml-pytorch-foundations/images/figure-0.1.4.png')
save_figure(fig, os.path.abspath(outpath))
