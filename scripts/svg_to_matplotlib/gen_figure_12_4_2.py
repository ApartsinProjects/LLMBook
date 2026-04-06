"""Figure 12.4.2: Pareto frontier for classification task cost vs quality."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from chart_style import *
apply_style()

fig, ax = plt.subplots(figsize=(10, 7))

# Data points from SVG
models = {
    'TF-IDF + LR':     {'cost': 0.00001, 'acc': 72, 'color': '#27ae60'},
    'Fine-tuned BERT':  {'cost': 0.0005,  'acc': 85, 'color': '#3498db'},
    'Hybrid Router':    {'cost': 0.002,   'acc': 93, 'color': '#f39c12'},
    'GPT-4o-mini':      {'cost': 0.003,   'acc': 91, 'color': '#8e44ad'},
    'GPT-4o':           {'cost': 0.01,    'acc': 95, 'color': '#e94560'},
    'Claude Opus':      {'cost': 0.02,    'acc': 97, 'color': '#c0392b'},
}

# Pareto frontier curve
frontier_costs = [0.00001, 0.0005, 0.003, 0.01, 0.02]
frontier_accs = [72, 85, 91, 95, 97]
from scipy.interpolate import make_interp_spline
# Use log scale for x
fc_log = np.log10(frontier_costs)
spl = make_interp_spline(fc_log, frontier_accs, k=2)
x_smooth = np.linspace(fc_log[0], fc_log[-1], 200)
y_smooth = spl(x_smooth)
ax.plot(10**x_smooth, y_smooth, color='#e94560', linewidth=2.5, linestyle='--',
        alpha=0.7, zorder=2, label='Pareto Frontier')

# Plot each model
for name, d in models.items():
    marker = 'o' if name != 'Hybrid Router' else 'D'
    size = 100 if name != 'Hybrid Router' else 120
    edgecolor = d['color'] if name != 'Hybrid Router' else '#f39c12'
    facecolor = d['color'] if name != 'Hybrid Router' else 'none'
    linewidth = 1 if name != 'Hybrid Router' else 3
    ax.scatter(d['cost'], d['acc'], c=facecolor, edgecolors=edgecolor,
              s=size, linewidths=linewidth, zorder=5, marker=marker)
    # Label offset
    offset = (10, -5) if name != 'Claude Opus' else (-10, 10)
    ha = 'left' if name != 'Claude Opus' else 'right'
    ax.annotate(f"{name}\n${d['cost']}, {d['acc']}%",
                xy=(d['cost'], d['acc']),
                xytext=offset, textcoords='offset points',
                fontsize=10, fontweight='bold', color=d['color'], ha=ha)

# Suboptimal point
ax.scatter(0.005, 75, c='#cccccc', edgecolors='#999', s=80, zorder=4)
ax.annotate('Unoptimized\nprompt', xy=(0.005, 75), xytext=(12, -5),
            textcoords='offset points', fontsize=10, color='#999')
ax.plot([0.005, 0.003], [75, 91], color='#ccc', linewidth=1, linestyle=':', zorder=1)

# Suboptimal region label
ax.text(0.005, 68, 'Suboptimal Region\n(better configurations exist)',
        ha='center', fontsize=11, color='#bbb', fontstyle='italic')

ax.set_xscale('log')
ax.set_xlabel('Cost per Query ($)', fontsize=12, color='#555')
ax.set_ylabel('Quality (Accuracy %)', fontsize=12, color='#555')
ax.set_ylim(58, 100)
ax.set_xlim(5e-6, 0.03)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11, loc='lower right')

outpath = os.path.join(os.path.dirname(__file__),
    '../../part-3-working-with-llms/module-12-hybrid-ml-llm/images/figure-12.4.2.png')
save_figure(fig, os.path.abspath(outpath))
