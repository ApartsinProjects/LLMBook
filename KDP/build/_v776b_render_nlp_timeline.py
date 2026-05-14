"""v776b: Render the 'Four Eras of NLP' timeline (section 1.1) as PNG.

The inline display:flex layout doesn't render on Kindle (boxes collapse
into a vertical stack, losing the colored-timeline visual). Generate
a PNG with matplotlib and replace the inline div timeline with <img>.
"""
import sys
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = ROOT / 'part-1-foundations' / 'module-01-foundations-nlp-text-representation' / 'images' / 'fig-1-1-3-nlp-timeline.png'
OUT.parent.mkdir(parents=True, exist_ok=True)

eras = [
    ('Rule-Based',    '1950s to 1980s',  'Hand-written\ngrammar rules',     '#f3e5f5', '#6a1b9a'),
    ('Statistical',   '1990s to 2000s',  'Word counts,\nn-grams',           '#fff3e0', '#e65100'),
    ('Neural',        '2013 to 2017',    'Dense vectors,\nend-to-end',      '#e3f2fd', '#1565c0'),
    ('LLM Era',       '2017 to Present', 'Transformers,\ncontextual vectors','#e8f5e9', '#2e7d32'),
]

fig, ax = plt.subplots(figsize=(10, 2.6), dpi=150)
ax.set_xlim(0, 100)
ax.set_ylim(0, 30)
ax.invert_yaxis()
ax.axis('off')

box_w = 21
gap = 4
for i, (name, period, desc, fill, edge) in enumerate(eras):
    x = i * (box_w + gap)
    bb = FancyBboxPatch(
        (x, 4), box_w, 22,
        boxstyle='round,pad=0.5,rounding_size=1.2',
        linewidth=2, edgecolor=edge, facecolor=fill, zorder=2)
    ax.add_patch(bb)
    cx = x + box_w / 2
    ax.text(cx, 9, name, ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(cx, 14, period, ha='center', va='center', fontsize=9.5, color='#555')
    ax.text(cx, 21, desc, ha='center', va='center', fontsize=8.5, fontstyle='italic', color='#444')
    if i < len(eras) - 1:
        ax.annotate('', xy=(x + box_w + gap - 0.5, 15), xytext=(x + box_w + 0.5, 15),
                    arrowprops=dict(arrowstyle='->', lw=1.6, color='#888'))

plt.savefig(OUT, dpi=150, bbox_inches='tight', pad_inches=0.1,
            facecolor='white', edgecolor='none')
plt.close()
print(f'wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size/1024:.1f} KB)')
