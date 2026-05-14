"""v775: Render Figure FM.3.1 as PNG (Kindle-compatible).

The inline SVG diagram with <text> elements in fm-what-this-book-covers
does not reliably render on Kindle devices (text disappears, layout
breaks). Generate a PNG image with matplotlib and replace the inline
SVG with <img>.
"""
from __future__ import annotations
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = ROOT / 'front-matter' / 'images' / 'fm-3-1-dependency-diagram.png'
OUT.parent.mkdir(parents=True, exist_ok=True)

fig, ax = plt.subplots(figsize=(9, 7.6), dpi=150)
ax.set_xlim(0, 900)
ax.set_ylim(0, 760)
ax.invert_yaxis()
ax.axis('off')

# Color palette (matches the original SVG)
C_FOUND = '#e3f2fd'
C_HUB   = '#e8f5e9'
C_BRANCH = '#fff3e0'
C_TERM  = '#f3e5f5'
EDGE = '#37474f'
LBL = '#263238'
SUB = '#455a64'
BR  = '#607d8b'


def box(x, y, w, h, color, lines, sublines=None, brlabel=None):
    """Draw a labelled rounded box."""
    bb = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=2,rounding_size=10",
        linewidth=1.5, edgecolor=EDGE, facecolor=color, zorder=2)
    ax.add_patch(bb)
    cx = x + w / 2
    # Title lines centred vertically
    n_lines = len(lines)
    line_h = 22
    sublines = sublines or []
    n_sub = len(sublines)
    total_h = n_lines * line_h + n_sub * 16
    start_y = y + (h - total_h) / 2 + 18
    for i, line in enumerate(lines):
        ax.text(cx, start_y + i * line_h, line,
                ha='center', va='center',
                fontsize=14, fontweight='bold', color=LBL)
    for i, line in enumerate(sublines):
        ax.text(cx, start_y + n_lines * line_h + i * 16, line,
                ha='center', va='center',
                fontsize=11, color=SUB)
    if brlabel:
        ax.text(cx, y + h + 16, brlabel,
                ha='center', va='center',
                fontsize=11, fontstyle='italic', color=BR)


def arrow(x1, y1, x2, y2, curve=False):
    """Draw a directional arrow."""
    if curve:
        connectionstyle = 'arc3,rad=0.3'
    else:
        connectionstyle = 'arc3,rad=0'
    ar = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle='-|>', mutation_scale=15,
        linewidth=1.8, color=EDGE,
        connectionstyle=connectionstyle, zorder=1)
    ax.add_patch(ar)


# ---- Top three boxes ----
box(280, 20, 340, 80, C_FOUND, ['Part I', 'Foundations'],
    sublines=['Chapters 0 through 5'])
arrow(450, 100, 450, 145)

box(280, 145, 340, 80, C_FOUND, ['Part II', 'Understanding LLMs'],
    sublines=['Chapters 6 through 10'])
arrow(450, 225, 450, 270)

box(280, 270, 340, 80, C_HUB, ['Part III', 'Working with LLMs'],
    sublines=['Chapters 11 through 13'])

# ---- Branching arrows III -> IV/V/VI ----
arrow(340, 350, 150, 405, curve=True)
arrow(450, 350, 450, 405)
arrow(560, 350, 750, 405, curve=True)

# ---- Three branch boxes ----
box(40, 405, 220, 80, C_BRANCH, ['Part IV'],
    sublines=['Training & Adapting', 'Chapters 14 through 17'],
    brlabel='Customize models')
box(340, 405, 220, 80, C_BRANCH, ['Part V'],
    sublines=['Retrieval & Conversation', 'Chapters 18 through 20'],
    brlabel='Ground in data')
box(640, 405, 220, 80, C_BRANCH, ['Part VI'],
    sublines=['Agentic AI', 'Chapters 21 through 25'],
    brlabel='Build and deploy')

# ---- Converging arrows IV/V/VI -> terminal ----
arrow(150, 510, 450, 605, curve=True)
arrow(450, 510, 450, 605)
arrow(750, 510, 450, 605, curve=True)

# ---- Terminal box ----
box(180, 610, 540, 80, C_TERM, ['Parts VII through XI'],
    sublines=['Applications, Evaluation, Safety, Frontiers, Product',
              'Chapters 26 through 37'])

ax.text(450, 730,
        'Read I, II, III in order. Then choose any of IV, V, VI in any '
        'order. Then on to VII through XI.',
        ha='center', va='center', fontsize=12, fontstyle='italic', color=BR)

plt.savefig(OUT, dpi=150, bbox_inches='tight', pad_inches=0.1,
            facecolor='white', edgecolor='none')
plt.close()
sz = OUT.stat().st_size
print(f'wrote {OUT.relative_to(ROOT)} ({sz/1024:.1f} KB)')
