"""Shared matplotlib style configuration for all chart conversions."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

STYLE = {
    'figure.figsize': (10, 6),
    'figure.dpi': 300,
    'font.family': 'sans-serif',
    'font.size': 12,
    'axes.linewidth': 1.2,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'legend.framealpha': 0.9,
    'legend.edgecolor': '#cccccc',
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1,
}

def apply_style():
    plt.rcParams.update(STYLE)

def save_figure(fig, path, dpi=300):
    fig.savefig(path, dpi=dpi, bbox_inches='tight', pad_inches=0.1,
                facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"Saved: {path}")
