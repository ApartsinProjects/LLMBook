"""Figure 5.2.2: Temperature scaling probability distribution."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from chart_style import *
apply_style()

fig, ax = plt.subplots(figsize=(10, 6))

# Token labels and positions
tokens = ['the', 'cat', 'dog', 'it', 'my', 'old', 'an', '...']
x_pos = np.arange(len(tokens))

# From SVG polylines (viewBox 0 0 700 350, axes x=80..650, y=45..290)
# T=0.3: points="120,65 190,230 260,265 330,275 400,280 470,283 540,285 610,287"
# T=1.0: points="120,140 190,195 260,225 330,245 400,260 470,268 540,274 610,278"
# T=2.0: points="120,200 190,220 260,237 330,248 400,256 470,262 540,266 610,270"
# Convert y: prob = (290 - y) / (290 - 45) to get 0..1 range

def svg_y_to_prob(y_vals):
    return (290 - np.array(y_vals)) / (290 - 45)

t03_y = [65, 230, 265, 275, 280, 283, 285, 287]
t10_y = [140, 195, 225, 245, 260, 268, 274, 278]
t20_y = [200, 220, 237, 248, 256, 262, 266, 270]

prob_03 = svg_y_to_prob(t03_y)
prob_10 = svg_y_to_prob(t10_y)
prob_20 = svg_y_to_prob(t20_y)

ax.plot(x_pos, prob_03, 'o-', color='#e94560', linewidth=2.5, markersize=6, label='T = 0.3 (sharp)')
ax.plot(x_pos, prob_10, 'o-', color='#4a90d9', linewidth=2.5, markersize=6, label='T = 1.0 (original)')
ax.plot(x_pos, prob_20, 'o-', color='#27ae60', linewidth=2.5, markersize=6, label='T = 2.0 (flat)')

ax.set_xticks(x_pos)
ax.set_xticklabels(tokens, fontfamily='monospace', fontsize=11)
ax.set_xlabel('Tokens (sorted by probability)', fontsize=12, color='#555')
ax.set_ylabel('Probability', fontsize=12, color='#555')
ax.legend(fontsize=11, loc='upper right')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_ylim(-0.02, 1.0)
ax.grid(True, alpha=0.3)

outpath = os.path.join(os.path.dirname(__file__),
    '../../part-1-foundations/module-05-decoding-text-generation/images/figure-5.2.2.png')
save_figure(fig, os.path.abspath(outpath))
