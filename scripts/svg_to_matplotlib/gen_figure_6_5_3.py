"""Figure 6.5.3: Grokking - training vs validation accuracy over time."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from chart_style import *
apply_style()

fig, ax = plt.subplots(figsize=(10, 6))

from scipy.interpolate import PchipInterpolator

def svg_to_norm(sx, sy, xr=(80, 650), yr=(50, 260)):
    nx = (np.array(sx) - xr[0]) / (xr[1] - xr[0]) * 100
    ny = (yr[1] - np.array(sy)) / (yr[1] - yr[0]) * 100
    return nx, ny

# Train accuracy: fast rise then plateau at 100%
# Add more intermediate points for smooth shape
train_sx = [90, 110, 120, 135, 150, 160, 170, 185, 200, 300, 450, 650]
train_sy = [250, 248, 240, 195, 120, 85, 65, 60, 58, 56, 55, 55]
tx, ty = svg_to_norm(train_sx, train_sy)
spl_t = PchipInterpolator(tx, ty)
x_sm = np.linspace(tx[0], tx[-1], 500)
y_train = np.clip(spl_t(x_sm), 0, 100)

# Val accuracy: flat plateau then delayed rise
val_sx = [90, 120, 200, 280, 350, 400, 420, 440, 450, 470, 490, 520, 600, 650]
val_sy = [250, 245, 248, 247, 245, 240, 230, 210, 180, 100, 65, 58, 55, 55]
vx, vy = svg_to_norm(val_sx, val_sy)
spl_v = PchipInterpolator(vx, vy)
y_val = np.clip(spl_v(x_sm), 0, 100)

ax.plot(x_sm, y_train, color='#e94560', linewidth=2.5, label='Train Accuracy')
ax.plot(x_sm, y_val, color='#27ae60', linewidth=2.5, linestyle='--', label='Val Accuracy')

# Vertical annotations
mem_x = (200 - 80) / (650 - 80) * 100
gen_x = (470 - 80) / (650 - 80) * 100
ax.axvline(x=mem_x, color='#888', linewidth=1, linestyle=':', alpha=0.7)
ax.text(mem_x + 1, 55, 'Memorized', fontsize=11, color='#888', fontstyle='italic')
ax.axvline(x=gen_x, color='#888', linewidth=1, linestyle=':', alpha=0.7)
ax.text(gen_x + 1, 25, 'Generalized!', fontsize=11, color='#888', fontstyle='italic')

# Long plateau arrow
ax.annotate('', xy=(gen_x - 5, 45), xytext=(mem_x + 5, 45),
            arrowprops=dict(arrowstyle='->', color='#8e44ad', lw=1.5))
ax.text((mem_x + gen_x) / 2, 38, 'Long plateau', ha='center', fontsize=11,
        fontstyle='italic', color='#8e44ad')

ax.set_xlabel('Training Steps', fontsize=12, color='#555')
ax.set_ylabel('Accuracy', fontsize=12, color='#555')
ax.set_xlim(-2, 102)
ax.set_ylim(-5, 105)
ax.set_yticks([0, 50, 100])
ax.set_yticklabels(['0%', '50%', '100%'])
ax.set_xticks([])
ax.legend(fontsize=11, loc='center right')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, alpha=0.3)

outpath = os.path.join(os.path.dirname(__file__),
    '../../part-2-understanding-llms/module-06-pretraining-scaling-laws/images/figure-6.5.3.png')
save_figure(fig, os.path.abspath(outpath))
