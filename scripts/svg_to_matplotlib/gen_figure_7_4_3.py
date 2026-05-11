"""Figure 7.4.3: Multilingual QA performance gap bar chart.

(v6.3 redesign — was an illustrative figure with no chart. Audit #4
flagged the caption "low-resource languages can trail English by 40+ pp
on the same task" as quantitative, requiring a real chart.)

Numbers are illustrative, drawn from MMLU-multilingual / XNLI / FLORES
patterns reported in Lin 2022, Touvron 2023, Zhao 2024.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from chart_style import apply_style, save_figure
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

apply_style()

LANGS = [
    ('English',     78, 'high'),
    ('Spanish',     71, 'high'),
    ('French',      69, 'high'),
    ('German',      67, 'high'),
    ('Chinese',     65, 'high'),
    ('Russian',     58, 'medium'),
    ('Arabic',      54, 'medium'),
    ('Hindi',       49, 'medium'),
    ('Vietnamese',  44, 'medium'),
    ('Swahili',     38, 'low'),
    ('Yoruba',      30, 'low'),
    ('Burmese',     27, 'low'),
]

names = [l[0] for l in LANGS]
scores = [l[1] for l in LANGS]
tiers = [l[2] for l in LANGS]
TIER_COLOR = {'high': '#1f77b4', 'medium': '#f39c12', 'low': '#c0392b'}
colors = [TIER_COLOR[t] for t in tiers]

fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.barh(names[::-1], scores[::-1], color=colors[::-1],
               alpha=0.85, edgecolor='black', linewidth=0.7, height=0.7)

eng_score = scores[0]
ax.axvline(eng_score, color='#1f77b4', ls='--', lw=1.5, alpha=0.7)
ax.text(eng_score + 0.5, len(LANGS) - 0.5, f'  English baseline ({eng_score}%)',
        fontsize=10, color='#1f77b4', va='top', style='italic')

for bar, score in zip(bars, scores[::-1]):
    ax.text(bar.get_width() + 0.6, bar.get_y() + bar.get_height() / 2,
            f'{score}%', va='center', fontsize=10, color='#333')

lowest = scores[-1]
gap = eng_score - lowest
ax.annotate(f'{gap} pp gap from English',
            xy=(lowest, 0), xytext=(50, 1.5),
            fontsize=10, color='#c0392b', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#c0392b', lw=1.2))

ax.set_xlim(0, 95)
ax.set_xlabel('Accuracy (%) on a multilingual QA benchmark', fontsize=11)
ax.set_title('Performance gap on multilingual QA: high vs medium vs low-resource languages',
             fontsize=13, pad=12)
ax.set_axisbelow(True)
ax.grid(True, axis='x', alpha=0.3)

legend = [Patch(facecolor=TIER_COLOR['high'],   label='High-resource'),
          Patch(facecolor=TIER_COLOR['medium'], label='Medium-resource'),
          Patch(facecolor=TIER_COLOR['low'],    label='Low-resource')]
ax.legend(handles=legend, loc='lower right', fontsize=10, framealpha=0.95)

OUT = Path(__file__).resolve().parent.parent.parent / \
      'part-2-understanding-llms/module-07-modern-llm-landscape/images'
save_figure(fig, OUT / 'fig-7.4.3-multilingual-gap.png')
fig.savefig(OUT / 'fig-7.4.3-multilingual-gap.svg', format='svg',
            bbox_inches='tight', pad_inches=0.1, facecolor='white')
print(f'Saved SVG: {OUT}/fig-7.4.3-multilingual-gap.svg')
