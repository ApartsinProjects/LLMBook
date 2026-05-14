"""v784: FM.3.1 round 5: eliminate the tint bands that the user perceives
as "spillover from underlying color" making Part IV/V/VI and the bottom
box look uncentered.

Root cause: previous renders added soft pastel rectangles behind each
visual zone (sequential foundations, choose-any branches, terminal). On
Kindle the tint extends slightly past the box edges, which the eye reads
as "the box is offset to the left/right of the band". The band serves no
didactic purpose the boxes themselves don't already convey, so we remove
it and rely on:
  - bold zone labels in the left margin column
  - the box border colors (green hub, orange/yellow/purple branches,
    purple terminal)
  - the caption strip at the bottom

Result: every box is visually centered against pure white, no bleed.
"""
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = ROOT / 'front-matter' / 'images' / 'fm-3-1-dependency-diagram.png'

C_FOUND = '#dbeafe'
C_HUB = '#dcfce7'
C_BRANCH_A = '#fed7aa'
C_BRANCH_B = '#fef3c7'
C_BRANCH_C = '#e9d5ff'
C_TERM = '#f3e8ff'
EDGE = '#1e293b'
LBL = '#0f172a'
SUB = '#475569'
ZONE = '#64748b'

fig, ax = plt.subplots(figsize=(13, 9), dpi=160)
ax.set_xlim(0, 1300)
ax.set_ylim(0, 900)
ax.invert_yaxis()
ax.axis('off')

CX = 720

# NOTE: NO background tint zones in v5 (this was the spillover source).


def box(x, y, w, h, color, lines, sublines=None, brlabel=None,
        edge_color=None):
    edge = edge_color or EDGE
    shadow = FancyBboxPatch(
        (x + 5, y + 5), w, h,
        boxstyle='round,pad=2,rounding_size=14',
        linewidth=0, facecolor='#cbd5e1', alpha=0.4, zorder=1)
    ax.add_patch(shadow)
    bb = FancyBboxPatch(
        (x, y), w, h,
        boxstyle='round,pad=2,rounding_size=14',
        linewidth=2.2, edgecolor=edge, facecolor=color, zorder=2)
    ax.add_patch(bb)
    cx = x + w / 2
    n_main = len(lines)
    n_sub = len(sublines) if sublines else 0
    line_h_main = 28
    line_h_sub = 19
    total_h = n_main * line_h_main + n_sub * line_h_sub
    start_y = y + (h - total_h) / 2 + line_h_main * 0.45
    for i, line in enumerate(lines):
        ax.text(cx, start_y + i * line_h_main, line,
                ha='center', va='center',
                fontsize=16, fontweight='bold', color=LBL, zorder=3)
    if sublines:
        for i, line in enumerate(sublines):
            ax.text(cx, start_y + n_main * line_h_main + i * line_h_sub, line,
                    ha='center', va='center',
                    fontsize=11.5, color=SUB, zorder=3)
    if brlabel:
        ax.text(cx, y + h + 19, brlabel,
                ha='center', va='center',
                fontsize=12, fontstyle='italic', color=ZONE, zorder=3)


def arrow(x1, y1, x2, y2, curve=None):
    cs = 'arc3,rad=0' if curve is None else f'arc3,rad={curve}'
    ar = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle='-|>', mutation_scale=22,
        linewidth=2.2, color=EDGE,
        connectionstyle=cs, zorder=2)
    ax.add_patch(ar)


# Zone labels in the left margin (replace the tint bands as the only
# zone-grouping device).
ax.text(140, 250, 'SEQUENTIAL\nFOUNDATIONS',
        ha='center', va='center', fontsize=12, fontweight='bold',
        color=ZONE, alpha=0.9, linespacing=1.3)
ax.text(140, 575, 'CHOOSE ANY\nIN ANY ORDER',
        ha='center', va='center', fontsize=12, fontweight='bold',
        color=ZONE, alpha=0.9, linespacing=1.3)
ax.text(140, 790, 'SYNTHESIS\n& DEPLOYMENT',
        ha='center', va='center', fontsize=12, fontweight='bold',
        color=ZONE, alpha=0.9, linespacing=1.3)

# Top three boxes
box(CX - 220, 80, 440, 100, C_FOUND, ['Part I'],
    sublines=['Foundations', 'Chapters 0 through 5'])
arrow(CX, 180, CX, 220)

box(CX - 220, 220, 440, 100, C_FOUND, ['Part II'],
    sublines=['Understanding LLMs', 'Chapters 6 through 10'])
arrow(CX, 320, CX, 360)

box(CX - 220, 360, 440, 100, C_HUB, ['Part III'],
    sublines=['Working with LLMs', 'Chapters 11 through 13'],
    edge_color='#16a34a')

# Branch arrows (III -> IV/V/VI)
arrow(CX - 110, 460, 360, 480, curve=-0.25)
arrow(CX, 460, CX, 480)
arrow(CX + 110, 460, 1080, 480, curve=0.25)

# Three branch boxes — 240 wide, centered at 360 / 720 / 1080
box(240, 480, 240, 130, C_BRANCH_A, ['Part IV'],
    sublines=['Training &', 'Adapting',
              'Chapters 14 to 17'],
    brlabel='Customize models')

box(600, 480, 240, 130, C_BRANCH_B, ['Part V'],
    sublines=['Retrieval &', 'Conversation',
              'Chapters 18 to 20'],
    brlabel='Ground in data')

box(960, 480, 240, 130, C_BRANCH_C, ['Part VI'],
    sublines=['Agentic AI', '',
              'Chapters 21 to 25'],
    brlabel='Build and deploy')

# Convergence arrows
arrow(360, 630, CX, 730, curve=0.18)
arrow(CX, 630, CX, 730)
arrow(1080, 630, CX, 730, curve=-0.18)

# Terminal box (centered horizontally on CX)
box(CX - 380, 730, 760, 120, C_TERM, ['Parts VII through XI'],
    sublines=['Applications · Evaluation · Safety · Frontiers · Product',
              'Chapters 26 through 35'],
    edge_color='#9333ea')

# Caption strip
ax.text(CX, 875,
        'Read I then II then III in order. Then any of IV, V, VI. Then on to VII through XI.',
        ha='center', va='center', fontsize=13.5, fontstyle='italic',
        color='#334155')

plt.savefig(OUT, dpi=160, bbox_inches='tight', pad_inches=0.2,
            facecolor='white', edgecolor='none')
plt.close()
print(f'wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size/1024:.1f} KB)')
