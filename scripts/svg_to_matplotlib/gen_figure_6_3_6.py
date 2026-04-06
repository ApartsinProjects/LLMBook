"""Figure 6.3.6: Metric mirage - emergence vs smooth scaling (dual panel)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from chart_style import *
apply_style()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Left panel: Exact Match Accuracy (S-curve, looks emergent)
# SVG path: M90,255 L150,254 L180,252 L200,250 L215,240 L225,200 L235,140 L245,110 L290,100
# Axes: x=80..300, y=90..260
left_sx = [90, 150, 180, 200, 215, 225, 235, 245, 290]
left_sy = [255, 254, 252, 250, 240, 200, 140, 110, 100]
lx = (np.array(left_sx) - 80) / (300 - 80) * 10
ly = (260 - np.array(left_sy)) / (260 - 90) * 100

from scipy.interpolate import PchipInterpolator, make_interp_spline
spl_l = PchipInterpolator(lx, ly)
x_smooth = np.linspace(lx[0], lx[-1], 200)
y_smooth = spl_l(x_smooth)

ax1.plot(x_smooth, y_smooth, color='#e94560', linewidth=3)
ax1.set_title('Exact Match Accuracy', fontsize=13, fontweight='bold', color='#e94560')
ax1.set_xlabel('Model Size (log scale)', fontsize=11, color='#555')
ax1.set_ylabel('Performance', fontsize=11, color='#555')
ax1.text(7.5, 65, 'Looks emergent!', fontsize=12, fontstyle='italic', color='#e94560')
ax1.set_xticks([])
ax1.set_yticks([])
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.grid(False)

# Right panel: Log-Likelihood (smooth curve)
# SVG path: M420,250 L450,235 L480,218 L510,198 L540,175 L570,150 L600,130 L620,118
# Axes: x=410..630, y=90..260
right_sx = [420, 450, 480, 510, 540, 570, 600, 620]
right_sy = [250, 235, 218, 198, 175, 150, 130, 118]
rx = (np.array(right_sx) - 410) / (630 - 410) * 10
ry = (260 - np.array(right_sy)) / (260 - 90) * 100

spl_r = make_interp_spline(rx, ry, k=3)
x_smooth2 = np.linspace(rx[0], rx[-1], 200)
y_smooth2 = spl_r(x_smooth2)

ax2.plot(x_smooth2, y_smooth2, color='#27ae60', linewidth=3)
ax2.set_title('Log-Likelihood (Continuous)', fontsize=13, fontweight='bold', color='#27ae60')
ax2.set_xlabel('Model Size (log scale)', fontsize=11, color='#555')
ax2.set_ylabel('Performance', fontsize=11, color='#555')
ax2.text(5.0, 55, 'Smooth scaling', fontsize=12, fontstyle='italic', color='#27ae60')
ax2.set_xticks([])
ax2.set_yticks([])
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.grid(False)

plt.tight_layout()

outpath = os.path.join(os.path.dirname(__file__),
    '../../part-2-understanding-llms/module-06-pretraining-scaling-laws/images/figure-6.3.6.png')
save_figure(fig, os.path.abspath(outpath))
