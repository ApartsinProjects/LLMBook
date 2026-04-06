"""Figure 0.1.2: Gradient descent on a loss surface with local/global minima.

Caption: Gradient descent follows the slope downhill, step by step.
The learning rate controls step size.
The chart shows a loss curve L(w) with two valleys. Red dots trace
gradient descent steps descending into the first (shallower) valley
labeled 'Local min'. A green dot marks the deeper second valley as
'Global min'. An annotation box explains step size = lr * gradient.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from chart_style import *
apply_style()

fig, ax = plt.subplots(figsize=(10, 5.5))

# Build a smooth loss curve with two valleys
# Valley 1 (local min) is shallower, Valley 2 (global min) is deeper
x = np.linspace(0, 10, 1000)

# Craft a curve with two valleys using a combination of functions
# Valley 1 around x=2.8 (shallower), Valley 2 around x=6.5 (deeper)
y = (4.0 * np.sin(0.55 * x - 0.3)
     + 1.5 * np.sin(1.1 * x + 0.5)
     + 0.8 * np.cos(1.7 * x - 1.0)
     + 0.3 * x + 5)

# Normalize to a nice range
y = (y - y.min()) / (y.max() - y.min()) * 8 + 1

ax.plot(x, y, color='#1a4a80', linewidth=2.8, zorder=3)

# Find the actual local and global minima on the curve
# Local min: first valley (roughly x=1.5..4)
mask1 = (x >= 1.5) & (x <= 4.5)
local_idx = np.argmin(y[mask1])
local_min_x = x[mask1][local_idx]
local_min_y = y[mask1][local_idx]

# Global min: second valley (roughly x=5..8)
mask2 = (x >= 5.0) & (x <= 8.5)
global_idx = np.argmin(y[mask2])
global_min_x = x[mask2][global_idx]
global_min_y = y[mask2][global_idx]

# Gradient descent steps: start on left slope, descend into local min
# Pick points along the curve descending toward local_min
start_x = 1.2
gd_positions = [start_x]
step = 0.55
for i in range(4):
    next_x = gd_positions[-1] + step
    step *= 0.65  # decreasing step sizes as gradient decreases near min
    gd_positions.append(next_x)

# Get y values on the curve for each step
gd_x_vals = []
gd_y_vals = []
for gx in gd_positions:
    idx = np.argmin(np.abs(x - gx))
    gd_x_vals.append(x[idx])
    gd_y_vals.append(y[idx])

# Plot gradient descent dots with fading opacity
for i, (gx, gy) in enumerate(zip(gd_x_vals, gd_y_vals)):
    alpha = 1.0 - i * 0.12
    ax.plot(gx, gy, 'o', color='#d12f48', markersize=9, alpha=alpha, zorder=5,
            markeredgecolor='white', markeredgewidth=0.5)

# Arrows between steps
for i in range(len(gd_x_vals) - 1):
    ax.annotate('', xy=(gd_x_vals[i+1], gd_y_vals[i+1]),
                xytext=(gd_x_vals[i], gd_y_vals[i]),
                arrowprops=dict(arrowstyle='->', color='#e94560', lw=1.8), zorder=4)

# "Start" label
ax.text(gd_x_vals[0] - 0.15, gd_y_vals[0] + 0.7, 'Start', fontsize=11,
        fontweight='bold', color='#e94560', ha='center')

# Local min marker and label (at actual curve minimum)
ax.plot(local_min_x, local_min_y, 'o', color='#d12f48', markersize=7, zorder=5,
        markeredgecolor='white', markeredgewidth=0.5, alpha=0.5)
ax.annotate('Local min', xy=(local_min_x, local_min_y),
            xytext=(local_min_x + 0.6, local_min_y - 1.2),
            fontsize=11, fontweight='bold', color='#e94560',
            arrowprops=dict(arrowstyle='->', color='#e94560', lw=1, ls='--'),
            zorder=6)

# Global min marker and label (at actual curve minimum)
ax.plot(global_min_x, global_min_y, 'o', color='#27ae60', markersize=9, zorder=5,
        markeredgecolor='white', markeredgewidth=0.5)
ax.annotate('Global min', xy=(global_min_x, global_min_y),
            xytext=(global_min_x + 0.6, global_min_y - 1.2),
            fontsize=11, fontweight='bold', color='#27ae60',
            arrowprops=dict(arrowstyle='->', color='#27ae60', lw=1, ls='--'),
            zorder=6)

# Learning rate annotation box
bbox_props = dict(boxstyle="round,pad=0.5", facecolor='#fffbe6', edgecolor='#f39c12',
                  alpha=0.95, linewidth=1)
ax.text(7.5, y.max() - 0.3, 'Step size = learning rate \u00d7 gradient\nToo big: overshoot. Too small: slow.',
        fontsize=10, ha='center', va='top', bbox=bbox_props, color='#555')

ax.set_xlabel('Parameter value (w)', fontsize=12, color='#555')
ax.set_ylabel('Loss L(w)', fontsize=12, color='#555')
ax.set_xlim(-0.2, 10.2)
ax.set_ylim(y.min() - 1.5, y.max() + 1.0)
ax.set_xticks([])
ax.set_yticks([])
ax.grid(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#999')
ax.spines['bottom'].set_color('#999')

outpath = os.path.join(os.path.dirname(__file__),
    '../../part-1-foundations/module-00-ml-pytorch-foundations/images/figure-0.1.2.png')
save_figure(fig, os.path.abspath(outpath))
print(f"Saved to {os.path.abspath(outpath)}")
