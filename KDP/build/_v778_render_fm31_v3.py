"""v778 v3: Final polish on Figure FM.3.1.

v2 issues:
- Zone label "CHOOSE ANY IN ANY ORDER" overlapped Part IV box
- Background tint bands extended too far horizontally
- Branch labels too close to box edges

v3 fixes:
- Move zone labels to RIGHT side margin (boxes are centered/leftish)
- Shrink background tint bands to box-content area only
- Add explicit margin between zone labels and boxes
- Strengthen color contrast on branch boxes
"""
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = ROOT / 'front-matter' / 'images' / 'fm-3-1-dependency-diagram.png'

# Palette
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

# Canvas: 1200 wide gives room for box layout + zone labels in left margin
fig, ax = plt.subplots(figsize=(12, 8.6), dpi=160)
ax.set_xlim(0, 1200)
ax.set_ylim(0, 860)
ax.invert_yaxis()
ax.axis('off')

# Compute box layout first; then place zone labels and bg bands in the gaps
# Centerline for top boxes:
CX = 660  # right of zone-label column

# Background tint bands cover only the box-area horizontal range
band_x = 240
band_w = 920
ax.add_patch(FancyBboxPatch((band_x, 50), band_w, 360,
                            boxstyle='round,pad=0,rounding_size=14',
                            facecolor='#f8fafc', edgecolor='none', zorder=0))
ax.add_patch(FancyBboxPatch((band_x, 425), band_w, 200,
                            boxstyle='round,pad=0,rounding_size=14',
                            facecolor='#fffbeb', edgecolor='none', zorder=0))
ax.add_patch(FancyBboxPatch((band_x, 640), band_w, 175,
                            boxstyle='round,pad=0,rounding_size=14',
                            facecolor='#faf5ff', edgecolor='none', zorder=0))


def box(x, y, w, h, color, lines, sublines=None, brlabel=None,
        edge_color=None):
    edge = edge_color or EDGE
    shadow = FancyBboxPatch(
        (x + 4, y + 4), w, h,
        boxstyle='round,pad=2,rounding_size=14',
        linewidth=0, facecolor='#cbd5e1', alpha=0.4, zorder=1)
    ax.add_patch(shadow)
    bb = FancyBboxPatch(
        (x, y), w, h,
        boxstyle='round,pad=2,rounding_size=14',
        linewidth=2.0, edgecolor=edge, facecolor=color, zorder=2)
    ax.add_patch(bb)
    cx = x + w / 2
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


# Zone labels in LEFT margin (in their own column, never touching boxes)
ax.text(120, 230, 'SEQUENTIAL\nFOUNDATIONS',
        ha='center', va='center', fontsize=11, fontweight='bold',
        color=ZONE, alpha=0.9, linespacing=1.3)
ax.text(120, 525, 'CHOOSE ANY\nIN ANY ORDER',
        ha='center', va='center', fontsize=11, fontweight='bold',
        color=ZONE, alpha=0.9, linespacing=1.3)
ax.text(120, 727, 'SYNTHESIS\n& DEPLOYMENT',
        ha='center', va='center', fontsize=11, fontweight='bold',
        color=ZONE, alpha=0.9, linespacing=1.3)

# ---- Top three boxes ----
box(CX - 200, 70, 400, 90, C_FOUND, ['Part I'],
    sublines=['Foundations', 'Chapters 0 through 5'])
arrow(CX, 160, CX, 200)

box(CX - 200, 200, 400, 90, C_FOUND, ['Part II'],
    sublines=['Understanding LLMs', 'Chapters 6 through 10'])
arrow(CX, 290, CX, 330)

box(CX - 200, 330, 400, 90, C_HUB, ['Part III'],
    sublines=['Working with LLMs', 'Chapters 11 through 13'],
    edge_color='#16a34a')

# Branching arrows III -> IV/V/VI
arrow(CX - 100, 420, 380, 440, curve=-0.25)
arrow(CX, 420, CX, 440)
arrow(CX + 100, 420, 940, 440, curve=0.25)

# Three branch boxes (wider canvas allows 290 wide each)
box(245, 440, 290, 130, C_BRANCH_A, ['Part IV'],
    sublines=['Training & Adapting', 'Chapters 14 through 17'],
    brlabel='Customize models')

box(CX - 145, 440, 290, 130, C_BRANCH_B, ['Part V'],
    sublines=['Retrieval & Conversation', 'Chapters 18 through 20'],
    brlabel='Ground in data')

box(795, 440, 290, 130, C_BRANCH_C, ['Part VI'],
    sublines=['Agentic AI', 'Chapters 21 through 25'],
    brlabel='Build and deploy')

# Convergence arrows IV/V/VI -> terminal
arrow(380, 590, CX, 660, curve=0.18)
arrow(CX, 590, CX, 660)
arrow(940, 590, CX, 660, curve=-0.18)

# Terminal box (wider)
box(CX - 350, 660, 700, 110, C_TERM, ['Parts VII through XI'],
    sublines=['Applications · Evaluation · Safety · Frontiers · Product',
              'Chapters 26 through 35'],
    edge_color='#9333ea')

# Caption strip
ax.text(CX, 835,
        'Read I → II → III in order. Then any of IV, V, VI. Then on to VII–XI.',
        ha='center', va='center', fontsize=13, fontstyle='italic',
        color='#334155')

plt.savefig(OUT, dpi=160, bbox_inches='tight', pad_inches=0.2,
            facecolor='white', edgecolor='none')
plt.close()
sz = OUT.stat().st_size
print(f'wrote {OUT.relative_to(ROOT)} ({sz/1024:.1f} KB)')
