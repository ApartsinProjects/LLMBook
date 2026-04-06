"""Figure 33.1.1: AI Readiness Radar chart."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from chart_style import *
apply_style()

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

# Data from SVG: 4 pillars with scores
categories = ['Data Maturity', 'Tech Infra', 'Org Culture', 'Talent']
scores = [4, 3, 2, 3]

# Close the polygon - start from top (90 degrees = pi/2)
angles = (np.linspace(0, 2 * np.pi, len(categories), endpoint=False) + np.pi/2).tolist()
scores_closed = scores + [scores[0]]
angles_closed = angles + [angles[0]]

# Draw grid
for i in range(1, 6):
    circle = plt.Circle((0, 0), i, transform=ax.transData, fill=False,
                        color='#ddd', linewidth=0.5)

# Plot
ax.plot(angles_closed, scores_closed, 'o-', color='#4a90d9', linewidth=2.5,
        markersize=8, zorder=5)
ax.fill(angles_closed, scores_closed, alpha=0.15, color='#4a90d9')

# Configure
ax.set_thetagrids(np.degrees(angles), categories, fontsize=13, fontweight='bold', color='#1a1a2e')
ax.set_rgrids([1, 2, 3, 4, 5], labels=['1', '2', '3', '4', '5'],
              fontsize=10, color='#999')
ax.set_rlim(0, 5)
ax.spines['polar'].set_color('#ddd')
ax.grid(color='#ddd', linewidth=0.5)

# Add score annotations
for angle, score in zip(angles, scores):
    ax.annotate(f'{score}', xy=(angle, score), xytext=(5, 5),
                textcoords='offset points', fontsize=12, fontweight='bold',
                color='#4a90d9')

outpath = os.path.join(os.path.dirname(__file__),
    '../../part-9-safety-strategy/module-33-strategy-product-roi/images/figure-33.1.1.png')
save_figure(fig, os.path.abspath(outpath))
