"""v781: FM.3.1 round 4 (eliminate IV/V/VI overlap on Kindle) + restore
chapter-header navy band as a constrained top bar.

Issue 1: User says Part IV/V/VI boxes are overlapping on Kindle.
Even though the desktop render shows clear gaps, Kindle scales the
PNG down to ~600 px and the inter-box gap of 30 px collapses to
~10 px which visually touches.

Fix: increase inter-box gap dramatically (60-80 px in source),
narrow each branch box by 10-20 px to compensate.

Issue 2: User wants the dark blue chapter-header banner back, but
the previous full-page version made the FM index look like a giant
empty blue page. Compromise: a THIN navy band (60 px tall) at the
very top of every chapter, just enough to act as a visual page-break
indicator without dominating the page.
"""
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parent.parent.parent

# ============================================================
# Part 1: Re-render FM.3.1 with wider gaps
# ============================================================
OUT = ROOT / 'front-matter' / 'images' / 'fm-3-1-dependency-diagram.png'

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

# Larger canvas. Branch boxes 240 wide with 110 px gap so that even
# at 50% scale on Kindle 600 px wide, the gap is still ~25 px.
fig, ax = plt.subplots(figsize=(13, 9), dpi=160)
ax.set_xlim(0, 1300)
ax.set_ylim(0, 900)
ax.invert_yaxis()
ax.axis('off')

CX = 720  # right of zone-label column

# Background tint zones (cover only box-content area)
band_x = 280
band_w = 1000
ax.add_patch(FancyBboxPatch((band_x, 60), band_w, 380,
                            boxstyle='round,pad=0,rounding_size=14',
                            facecolor='#f8fafc', edgecolor='none', zorder=0))
ax.add_patch(FancyBboxPatch((band_x, 460), band_w, 230,
                            boxstyle='round,pad=0,rounding_size=14',
                            facecolor='#fffbeb', edgecolor='none', zorder=0))
ax.add_patch(FancyBboxPatch((band_x, 705), band_w, 175,
                            boxstyle='round,pad=0,rounding_size=14',
                            facecolor='#faf5ff', edgecolor='none', zorder=0))


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


# Zone labels in left margin
ax.text(140, 250, 'SEQUENTIAL\nFOUNDATIONS',
        ha='center', va='center', fontsize=12, fontweight='bold',
        color=ZONE, alpha=0.9, linespacing=1.3)
ax.text(140, 575, 'CHOOSE ANY\nIN ANY ORDER',
        ha='center', va='center', fontsize=12, fontweight='bold',
        color=ZONE, alpha=0.9, linespacing=1.3)
ax.text(140, 790, 'SYNTHESIS\n& DEPLOYMENT',
        ha='center', va='center', fontsize=12, fontweight='bold',
        color=ZONE, alpha=0.9, linespacing=1.3)

# ---- Top three boxes ----
box(CX - 220, 80, 440, 100, C_FOUND, ['Part I'],
    sublines=['Foundations', 'Chapters 0 through 5'])
arrow(CX, 180, CX, 220)

box(CX - 220, 220, 440, 100, C_FOUND, ['Part II'],
    sublines=['Understanding LLMs', 'Chapters 6 through 10'])
arrow(CX, 320, CX, 360)

box(CX - 220, 360, 440, 100, C_HUB, ['Part III'],
    sublines=['Working with LLMs', 'Chapters 11 through 13'],
    edge_color='#16a34a')

# Branching arrows III -> IV/V/VI (clear curves; wide spread)
# IV center at x=360, V center at x=720, VI center at x=1080
arrow(CX - 110, 460, 360, 480, curve=-0.25)
arrow(CX, 460, CX, 480)
arrow(CX + 110, 460, 1080, 480, curve=0.25)

# Three branch boxes — 240 wide, centered at 360 / 720 / 1080
# Inter-box gap: 360-120=240 to 720-120=600, gap = 240 px between centers
# Actual edge gap: box ends at 480; next box starts at 600 -> 120 px gap
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

# Convergence arrows IV/V/VI -> terminal
arrow(360, 630, CX, 730, curve=0.18)
arrow(CX, 630, CX, 730)
arrow(1080, 630, CX, 730, curve=-0.18)

# Terminal box (wider)
box(CX - 380, 730, 760, 120, C_TERM, ['Parts VII through XI'],
    sublines=['Applications · Evaluation · Safety · Frontiers · Product',
              'Chapters 26 through 35'],
    edge_color='#9333ea')

# Caption strip
ax.text(CX, 875,
        'Read I → II → III in order. Then any of IV, V, VI. Then on to VII–XI.',
        ha='center', va='center', fontsize=13.5, fontstyle='italic',
        color='#334155')

plt.savefig(OUT, dpi=160, bbox_inches='tight', pad_inches=0.2,
            facecolor='white', edgecolor='none')
plt.close()
print(f'wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size/1024:.1f} KB)')


# ============================================================
# Part 2: Restore chapter-header navy band but only as thin top bar
# ============================================================
overrides = ROOT / 'KDP' / 'build' / 'epub_overrides.css'
s = overrides.read_text(encoding='utf-8')

old_hero = '''.chapter-header {
    /* Strip the decorative dark-navy hero in EPUB. Kindle renders the
     * banner as a near-blank colored page (the banner takes full page
     * height with only header text on it), which made the FM index
     * look broken. EPUB readers can still see the part-label/h1 with
     * normal typography. */
    background: transparent !important;
    background-color: transparent !important;
    color: inherit !important;
    padding: 0.5em 0 !important;
    margin: 0 0 1em 0 !important;
}'''
new_hero = '''.chapter-header {
    /* Compact navy banner: visible visual identity at the top of every
     * chapter, but bounded to header content (does NOT fill empty pages
     * which previously caused giant-blue-page rendering on Kindle and
     * triggered KDP's fixed-format misclassification). The padding of
     * 0.6em keeps the banner snug to the part-label/h1 text. */
    background: #1a1a2e !important;
    background-color: #1a1a2e !important;
    color: #ffffff !important;
    padding: 0.6em 1em 0.8em !important;
    margin: 0 0 1.2em 0 !important;
    border-radius: 0 0 4px 4px;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
}'''
if old_hero in s:
    s = s.replace(old_hero, new_hero)
    print('[chapter-header navy band restored as bounded top bar]')

old_text = '''.chapter-header,
.chapter-header h1,
.chapter-header h2,
.chapter-header h3,
.chapter-header h4,
.chapter-header h5,
.chapter-header h6,
.chapter-header a,
.chapter-header .book-title-link {
    color: inherit !important;
}'''
new_text = '''.chapter-header,
.chapter-header h1,
.chapter-header h2,
.chapter-header h3,
.chapter-header h4,
.chapter-header h5,
.chapter-header h6,
.chapter-header a,
.chapter-header .book-title-link {
    color: #ffffff !important;
}'''
if old_text in s:
    s = s.replace(old_text, new_text)
    print('[chapter-header text -> white]')

old_gold = '''.chapter-header .part-label,
.chapter-header .chapter-label,
.chapter-header .part-label a,
.chapter-header .chapter-label a {
    color: #455a64 !important;  /* slate breadcrumb on light background */
    text-decoration: none !important;
    font-size: 0.85em !important;
}'''
new_gold = '''.chapter-header .part-label,
.chapter-header .chapter-label,
.chapter-header .part-label a,
.chapter-header .chapter-label a {
    color: #d4b96a !important;  /* gold accent for breadcrumb labels */
    text-decoration: none !important;
    font-size: 0.85em !important;
}'''
if old_gold in s:
    s = s.replace(old_gold, new_gold)
    print('[breadcrumbs -> gold]')

# Add break-inside: avoid for author-card so both authors don't split
# across pages awkwardly.
if '.author-card { break-inside' not in s:
    s = s.rstrip() + '''

/* Keep each author card together on a single page (avoid orphan photo
 * with bio on the next page). page-break-inside is the EPUB-supported
 * variant; break-inside is the modern alias. */
.author-card {
    page-break-inside: avoid;
    break-inside: avoid;
}
'''
    print('[author-card page-break-inside: avoid]')

overrides.write_text(s, encoding='utf-8')
