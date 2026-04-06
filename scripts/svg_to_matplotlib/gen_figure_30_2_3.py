"""Figure 30.2.3: Quality monitoring timeline with silent degradation."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from chart_style import *
apply_style()

fig, ax = plt.subplots(figsize=(12, 5))

# SVG axes: x=60..700, y=40..200
# Quality line (good phase): 60,80 100,75 140,82 180,78 220,80 260,76 300,83 340,79 380,77
good_x = [60, 100, 140, 180, 220, 260, 300, 340, 380]
good_y_svg = [80, 75, 82, 78, 80, 76, 83, 79, 77]

# Quality line (degraded): 380,77 420,105 460,115 500,110 540,120 580,125 620,118 660,122 700,130
bad_x = [380, 420, 460, 500, 540, 580, 620, 660, 700]
bad_y_svg = [77, 105, 115, 110, 120, 125, 118, 122, 130]

# Convert SVG y to quality score: y=40 is top (high quality ~0.95), y=200 is bottom (~0.55)
def svg_y_to_quality(sy):
    return 0.95 - (np.array(sy) - 40) / (200 - 40) * 0.40

# Convert SVG x to weeks: x=60=Week1, x=700=Week5
def svg_x_to_weeks(sx):
    return 1 + (np.array(sx) - 60) / (700 - 60) * 4

gx = svg_x_to_weeks(good_x)
gy = svg_y_to_quality(good_y_svg)
bx = svg_x_to_weeks(bad_x)
by = svg_y_to_quality(bad_y_svg)

ax.plot(gx, gy, color='#27ae60', linewidth=2.5, marker='o', markersize=4, zorder=3)
ax.plot(bx, by, color='#e74c3c', linewidth=2.5, marker='o', markersize=4, zorder=3)

# Provider update marker at Week 3 (x=380)
update_week = svg_x_to_weeks([380])[0]
ax.axvline(x=update_week, color='#e74c3c', linewidth=1.5, linestyle='--', alpha=0.8)
ax.text(update_week + 0.05, 0.94, 'Provider model update', fontsize=11,
        fontweight='bold', color='#e74c3c')

# Alert threshold at y=110 in SVG
threshold = svg_y_to_quality([110])[0]
ax.axhline(y=threshold, color='#f39c12', linewidth=1, linestyle='--', alpha=0.8)
ax.text(1.05, threshold + 0.005, 'Alert threshold', fontsize=10, color='#f39c12')

# Baseline at y=80
baseline = svg_y_to_quality([80])[0]
ax.axhline(y=baseline, color='#27ae60', linewidth=1, linestyle='--', alpha=0.5,
           xmin=0, xmax=0.5)
ax.text(1.05, baseline + 0.005, 'Baseline (0.85)', fontsize=10, color='#27ae60')

# Alert annotation box
bbox_props = dict(boxstyle="round,pad=0.5", facecolor='#fef9e7', edgecolor='#f39c12', alpha=0.9)
ax.text(4.0, 0.70, 'Alert triggered: Week 3.5\nQuality dropped below 0.75',
        fontsize=10, ha='center', va='center', bbox=bbox_props, color='#333')

ax.set_xlabel('', fontsize=12)
ax.set_ylabel('Quality Score', fontsize=12, color='#555')
ax.set_xticks([1, 2, 3, 4, 5])
ax.set_xticklabels(['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'])
ax.set_ylim(0.55, 0.97)
ax.set_xlim(0.9, 5.1)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, alpha=0.3)

outpath = os.path.join(os.path.dirname(__file__),
    '../../part-8-evaluation-production/module-30-observability-monitoring/images/figure-30.2.3.png')
save_figure(fig, os.path.abspath(outpath))
