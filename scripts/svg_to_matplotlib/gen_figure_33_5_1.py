"""Figure 33.5.1: API vs self-hosted cost curves with breakeven point."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from chart_style import *
apply_style()

fig, ax = plt.subplots(figsize=(10, 6))

# From SVG: simple linear API cost and flat self-hosted cost
# X: 0 to 7M requests, Y: monthly cost
x_range = np.linspace(0, 7, 300)  # in millions

# API cost: linear from $0 at 0 to ~$28K at 7M (from SVG proportions)
# Self-hosted: flat at ~$16K
# Breakeven at ~5.3M

api_rate = 3.0  # $/1000 requests => $3K per 1M
api_cost = x_range * api_rate

self_hosted_cost = np.full_like(x_range, 16.0)  # $16K/month flat

ax.plot(x_range, api_cost, color='#e94560', linewidth=2.5, label='API Cost')
ax.plot(x_range, self_hosted_cost, color='#4a90d9', linewidth=2.5, label='Self-hosted')

# Breakeven point
be_x = 16.0 / api_rate  # ~5.33M
ax.plot(be_x, 16.0, 'o', color='#27ae60', markersize=10, zorder=5)
ax.annotate('Breakeven\n~5.3M req/mo', xy=(be_x, 16.0),
            xytext=(be_x - 0.3, 20.0), fontsize=11, fontweight='bold', color='#27ae60',
            ha='center')

# Region labels
ax.text(2.0, 12.0, 'API wins', fontsize=12, fontweight='bold', color='#4a90d9', ha='center')
ax.text(6.3, 12.0, 'Self-hosted wins', fontsize=12, fontweight='bold', color='#e94560', ha='center')

# Fill regions lightly
ax.fill_between(x_range, api_cost, self_hosted_cost,
                where=(api_cost < self_hosted_cost), alpha=0.05, color='#4a90d9')
ax.fill_between(x_range, api_cost, self_hosted_cost,
                where=(api_cost >= self_hosted_cost), alpha=0.05, color='#e94560')

ax.set_xlabel('Monthly Request Volume (millions)', fontsize=12, color='#555')
ax.set_ylabel('Monthly Cost ($K)', fontsize=12, color='#555')
ax.set_xlim(0, 7)
ax.set_ylim(0, 25)
ax.set_xticks([0, 1, 3, 5, 7])
ax.set_xticklabels(['0', '1M', '3M', '5M', '7M'])
ax.legend(fontsize=11, loc='upper left')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, alpha=0.3)

outpath = os.path.join(os.path.dirname(__file__),
    '../../part-9-safety-strategy/module-33-strategy-product-roi/images/figure-33.5.1.png')
save_figure(fig, os.path.abspath(outpath))
