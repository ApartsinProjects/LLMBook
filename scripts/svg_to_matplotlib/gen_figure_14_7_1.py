"""Figure 14.7.1: Context extension - perplexity vs sequence length."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from chart_style import *
apply_style()

fig, ax = plt.subplots(figsize=(10, 6))

from scipy.interpolate import make_interp_spline

# SVG axes: x=80..700, y=45..260
# X-axis labels: 1K=150, 2K=270, 4K=390, 8K=510, 16K=630
x_labels = ['1K', '2K', '4K', '8K', '16K']
x_positions = [1, 2, 4, 8, 16]  # In K tokens

# Perplexity (no extension): good in training range, explodes outside
# M 100 230 L 150 225 L 200 222 L 270 220 L 340 218 L 390 218 Q 430 220 470 200 Q 510 170 550 120 Q 590 80 650 55
no_ext_sx = [100, 150, 200, 270, 340, 390, 430, 470, 510, 550, 590, 650]
no_ext_sy = [230, 225, 222, 220, 218, 218, 220, 200, 170, 120, 80, 55]
# Convert SVG x to tokens (K): x=80 is ~0.5K, x=700 is ~18K (linear mapping through labeled points)
# 150->1K, 270->2K, 390->4K, 510->8K, 630->16K
# Linear: tokens = (x - 150) / (630 - 150) * 15 + 1
def svg_x_to_k(sx):
    return (np.array(sx) - 150) / (630 - 150) * 15 + 1

def svg_y_to_ppl(sy):
    # y=260 is low perplexity, y=45 is high perplexity
    # Map: y=230 ~ low ppl (e.g., 5), y=55 ~ high ppl (e.g., 50)
    return 5 + (230 - np.array(sy)) / (230 - 55) * 45

ne_x = svg_x_to_k(no_ext_sx)
ne_y = svg_y_to_ppl(no_ext_sy)

spl_ne = make_interp_spline(ne_x, ne_y, k=3)
x_sm = np.linspace(ne_x[0], ne_x[-1], 300)
y_no_ext = spl_ne(x_sm)

# With context extension: stays flat
# M 100 230 L 150 225 L 200 222 L 270 220 L 340 218 L 390 218 L 470 219 L 550 221 L 630 224
ext_sx = [100, 150, 200, 270, 340, 390, 470, 550, 630]
ext_sy = [230, 225, 222, 220, 218, 218, 219, 221, 224]
ex_x = svg_x_to_k(ext_sx)
ex_y = svg_y_to_ppl(ext_sy)
spl_ex = make_interp_spline(ex_x, ex_y, k=3)
x_sm2 = np.linspace(ex_x[0], ex_x[-1], 300)
y_ext = spl_ex(x_sm2)

ax.plot(x_sm, y_no_ext, color='#e94560', linewidth=3, label='Without context extension')
ax.plot(x_sm2, y_ext, color='#4CAF50', linewidth=3, linestyle='--', label='With context extension')

# Training window shading
ax.axvspan(0, 4, alpha=0.08, color='#4CAF50')
ax.text(2.5, 48, 'Training window (4K)', ha='center', fontsize=11, color='#4CAF50')

ax.axvspan(4, 18, alpha=0.05, color='#e94560')
ax.text(11, 48, 'Out-of-distribution', ha='center', fontsize=11, color='#C62828')

# Training boundary
ax.axvline(x=4, color='#FF9800', linewidth=1.5, linestyle='--', alpha=0.7)

# Annotation for perplexity explodes
ax.annotate('Perplexity\nexplodes', xy=(16, y_no_ext[-1]),
            xytext=(14, y_no_ext[-1] + 3),
            fontsize=11, color='#e94560', fontweight='bold')

ax.set_xlabel('Sequence Length (tokens)', fontsize=12, color='#555')
ax.set_ylabel('Perplexity (lower is better)', fontsize=12, color='#555')
ax.set_xticks([1, 2, 4, 8, 16])
ax.set_xticklabels(['1K', '2K', '4K', '8K', '16K'])
ax.set_xlim(0, 17)
ax.legend(fontsize=11, loc='upper left')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, alpha=0.3)

outpath = os.path.join(os.path.dirname(__file__),
    '../../part-4-training-adapting/module-14-fine-tuning-fundamentals/images/figure-14.7.1.png')
save_figure(fig, os.path.abspath(outpath))
