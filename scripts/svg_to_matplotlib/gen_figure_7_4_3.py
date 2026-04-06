"""Figure 7.4.3: Multilingual QA performance gap bar chart."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from chart_style import *
apply_style()

fig, ax = plt.subplots(figsize=(10, 6))

# Data from SVG
languages = ['EN', 'DE', 'ZH', 'AR', 'HI', 'SW', 'YO', 'QU']
accuracies = [88, 85, 84, 70, 65, 60, 43, 34]
colors = ['#27ae60', '#27ae60', '#27ae60',  # High-resource
          '#f39c12', '#f39c12', '#f39c12',  # Medium-resource
          '#e94560', '#e94560']              # Low-resource

bars = ax.bar(languages, accuracies, color=colors, width=0.6, edgecolor='white', linewidth=0.5)

# Add value labels on top
for bar, acc in zip(bars, accuracies):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
            f'{acc}%', ha='center', va='bottom', fontsize=11, fontweight='bold',
            color=bar.get_facecolor())

# Legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#27ae60', label='High-resource'),
    Patch(facecolor='#f39c12', label='Medium-resource'),
    Patch(facecolor='#e94560', label='Low-resource'),
]
ax.legend(handles=legend_elements, fontsize=11, loc='upper right')

# Subtitle with language codes
ax.text(0.5, -0.12,
        'EN=English, DE=German, ZH=Chinese, AR=Arabic, HI=Hindi, SW=Swahili, YO=Yoruba, QU=Quechua',
        transform=ax.transAxes, ha='center', fontsize=10, color='#999')

ax.set_ylabel('Accuracy (%)', fontsize=12, color='#555')
ax.set_ylim(0, 100)
ax.set_yticks([10, 30, 50, 70, 90])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, axis='y', alpha=0.3)

outpath = os.path.join(os.path.dirname(__file__),
    '../../part-2-understanding-llms/module-07-modern-llm-landscape/images/figure-7.4.3.png')
save_figure(fig, os.path.abspath(outpath))
