"""v778: Redesign Figure FM.3.1. Round 2.

User feedback: "Part 4, 5, 6 boxes, text is outside, make several round
of redesign of this figure till perfect, beautify, this should be the
best figure ever."

Issues with v775:
- Part IV / V / VI box width was too narrow for text
- Sublabels overflowed bottom of boxes
- Branch labels touched top of subsequent text

Round 2 design:
- Wider canvas (1100 x 800) so each box has more room
- Branch boxes: width 280 each (was 220), height 110 (was 80)
- Multi-line text rendered with proper line spacing
- Use plt.text bbox=None and explicit y-positions with verticalalignment='center'
- Soft shadow + rounded corners + softer color palette
- Larger arrow heads for visual weight
- Title above the figure inside the canvas
- Section line that says "Sequential foundations" / "Choose any in any order" / "Synthesis"
"""
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Patch
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = ROOT / 'front-matter' / 'images' / 'fm-3-1-dependency-diagram.png'
OUT.parent.mkdir(parents=True, exist_ok=True)

# Refined palette
C_FOUND = '#dbeafe'
C_HUB   = '#dcfce7'
C_BRANCH_A = '#fed7aa'
C_BRANCH_B = '#fef3c7'
C_BRANCH_C = '#e9d5ff'
C_TERM  = '#f3e8ff'
EDGE = '#1e293b'
LBL = '#0f172a'
SUB = '#475569'
ZONE = '#64748b'

fig, ax = plt.subplots(figsize=(11, 8.5), dpi=160)
ax.set_xlim(0, 1100)
ax.set_ylim(0, 850)
ax.invert_yaxis()
ax.axis('off')

# Background tint zones (subtle horizontal bands)
ax.add_patch(FancyBboxPatch((30, 50), 1040, 290,
                            boxstyle='round,pad=0,rounding_size=18',
                            facecolor='#f8fafc', edgecolor='none', zorder=0))
ax.add_patch(FancyBboxPatch((30, 360), 1040, 220,
                            boxstyle='round,pad=0,rounding_size=18',
                            facecolor='#fdfdf8', edgecolor='none', zorder=0))
ax.add_patch(FancyBboxPatch((30, 600), 1040, 200,
                            boxstyle='round,pad=0,rounding_size=18',
                            facecolor='#fdf4ff', edgecolor='none', zorder=0))


def box(x, y, w, h, color, lines, sublines=None, brlabel=None,
        edge_color=None):
    """Draw a labelled rounded box with shadow."""
    edge = edge_color or EDGE
    # Subtle shadow
    shadow = FancyBboxPatch(
        (x + 4, y + 4), w, h,
        boxstyle='round,pad=2,rounding_size=14',
        linewidth=0, facecolor='#cbd5e1', alpha=0.45, zorder=1)
    ax.add_patch(shadow)
    # Box
    bb = FancyBboxPatch(
        (x, y), w, h,
        boxstyle='round,pad=2,rounding_size=14',
        linewidth=2.0, edgecolor=edge, facecolor=color, zorder=2)
    ax.add_patch(bb)
    cx = x + w / 2
    # Title block (centered vertically with sublabels stacked below)
    n_main = len(lines)
    n_sub = len(sublines) if sublines else 0
    line_h_main = 26
    line_h_sub = 18
    total_h = n_main * line_h_main + n_sub * line_h_sub
    start_y = y + (h - total_h) / 2 + line_h_main * 0.45
    for i, line in enumerate(lines):
        ax.text(cx, start_y + i * line_h_main, line,
                ha='center', va='center',
                fontsize=15, fontweight='bold', color=LBL, zorder=3)
    if sublines:
        for i, line in enumerate(sublines):
            ax.text(cx, start_y + n_main * line_h_main + i * line_h_sub, line,
                    ha='center', va='center',
                    fontsize=11, color=SUB, zorder=3)
    if brlabel:
        ax.text(cx, y + h + 18, brlabel,
                ha='center', va='center',
                fontsize=11, fontstyle='italic', color=ZONE, zorder=3)


def arrow(x1, y1, x2, y2, curve=None):
    cs = 'arc3,rad=0' if curve is None else f'arc3,rad={curve}'
    ar = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle='-|>', mutation_scale=20,
        linewidth=2.0, color=EDGE,
        connectionstyle=cs, zorder=2)
    ax.add_patch(ar)


# Zone labels (left margin)
ax.text(50, 195, 'SEQUENTIAL\nFOUNDATIONS',
        ha='left', va='center', fontsize=10, fontweight='bold',
        color=ZONE, alpha=0.7)
ax.text(50, 470, 'CHOOSE ANY\nIN ANY ORDER',
        ha='left', va='center', fontsize=10, fontweight='bold',
        color=ZONE, alpha=0.7)
ax.text(50, 700, 'SYNTHESIS\n& DEPLOYMENT',
        ha='left', va='center', fontsize=10, fontweight='bold',
        color=ZONE, alpha=0.7)

# Top three boxes (foundations / understanding / hub)
box(360, 70, 380, 90, C_FOUND, ['Part I'],
    sublines=['Foundations', 'Chapters 0 through 5'])
arrow(550, 160, 550, 200)

box(360, 200, 380, 90, C_FOUND, ['Part II'],
    sublines=['Understanding LLMs', 'Chapters 6 through 10'])
arrow(550, 290, 550, 330)

box(360, 330, 380, 90, C_HUB, ['Part III'],
    sublines=['Working with LLMs', 'Chapters 11 through 13'],
    edge_color='#16a34a')

# Branching arrows III -> IV/V/VI (clear curves)
arrow(425, 420, 195, 470, curve=-0.25)
arrow(550, 420, 550, 470)
arrow(675, 420, 905, 470, curve=0.25)

# Three branch boxes — wider and taller
box(60, 470, 270, 110, C_BRANCH_A, ['Part IV'],
    sublines=['Training & Adapting', 'Chapters 14 through 17'],
    brlabel='Customize models')

box(415, 470, 270, 110, C_BRANCH_B, ['Part V'],
    sublines=['Retrieval & Conversation', 'Chapters 18 through 20'],
    brlabel='Ground in data')

box(770, 470, 270, 110, C_BRANCH_C, ['Part VI'],
    sublines=['Agentic AI', 'Chapters 21 through 25'],
    brlabel='Build and deploy')

# Convergence arrows IV/V/VI -> terminal
arrow(195, 600, 550, 670, curve=0.18)
arrow(550, 600, 550, 670)
arrow(905, 600, 550, 670, curve=-0.18)

# Terminal box
box(225, 670, 650, 110, C_TERM,
    ['Parts VII through XI'],
    sublines=['Applications · Evaluation · Safety · Frontiers · Product',
              'Chapters 26 through 35'],
    edge_color='#9333ea')

# Caption strip
ax.text(550, 825,
        'Read I → II → III in order. Then any of IV, V, VI. Then on to VII–XI.',
        ha='center', va='center', fontsize=12.5, fontstyle='italic',
        color='#334155')

plt.savefig(OUT, dpi=160, bbox_inches='tight', pad_inches=0.18,
            facecolor='white', edgecolor='none')
plt.close()
sz = OUT.stat().st_size
print(f'wrote {OUT.relative_to(ROOT)} ({sz/1024:.1f} KB)')
