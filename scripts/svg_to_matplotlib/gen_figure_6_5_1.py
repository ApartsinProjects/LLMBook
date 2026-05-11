"""Figure 6.5.1: SGD vs Adam on an anisotropic (ravine) loss landscape.

Replaces the GPS-navigator cartoon flagged by the v6.0 audit.
Two-panel contour plot:
  - Left:  SGD zigzags across the narrow ravine (the y-direction has much higher
           curvature than x), making slow progress along the valley floor.
  - Right: Adam's per-parameter learning rate scaling dampens the y-axis
           oscillation, producing a smooth diagonal descent toward the minimum.

The same starting point and the same number of steps are used in both panels
so the visual asymmetry shows the optimizer's effect, not the schedule.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from chart_style import apply_style, save_figure

import matplotlib.pyplot as plt
import numpy as np

apply_style()

# Anisotropic quadratic loss: L(x, y) = (1/2)(0.5 x^2 + 8 y^2)
# Gradient: dL/dx = 0.5 x ; dL/dy = 8 y
def loss(x, y):
    return 0.5 * (0.5 * x**2 + 8 * y**2)

def grad(x, y):
    return 0.5 * x, 8 * y


# Contour grid
xs = np.linspace(-2.5, 0.5, 200)
ys = np.linspace(-1.0, 1.0, 200)
X, Y = np.meshgrid(xs, ys)
Z = loss(X, Y)


def run_sgd(x0, y0, lr=0.05, steps=40):
    x, y = x0, y0
    path = [(x, y)]
    for _ in range(steps):
        gx, gy = grad(x, y)
        x -= lr * gx
        y -= lr * gy
        path.append((x, y))
    return np.array(path)


def run_adam(x0, y0, lr=0.4, beta1=0.9, beta2=0.999, eps=1e-8, steps=40):
    x, y = x0, y0
    mx, my = 0.0, 0.0
    vx, vy = 0.0, 0.0
    path = [(x, y)]
    for t in range(1, steps + 1):
        gx, gy = grad(x, y)
        mx = beta1 * mx + (1 - beta1) * gx
        my = beta1 * my + (1 - beta1) * gy
        vx = beta2 * vx + (1 - beta2) * gx**2
        vy = beta2 * vy + (1 - beta2) * gy**2
        m_hat_x = mx / (1 - beta1**t)
        m_hat_y = my / (1 - beta1**t)
        v_hat_x = vx / (1 - beta2**t)
        v_hat_y = vy / (1 - beta2**t)
        x -= lr * m_hat_x / (np.sqrt(v_hat_x) + eps)
        y -= lr * m_hat_y / (np.sqrt(v_hat_y) + eps)
        path.append((x, y))
    return np.array(path)


START = (-2.2, 0.85)
sgd_path = run_sgd(*START)
adam_path = run_adam(*START)

fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
levels = np.geomspace(0.05, 12, 14)

for ax, path, name, color in zip(
    axes, [sgd_path, adam_path], ['SGD', 'Adam'], ['#d62728', '#1f77b4']
):
    cs = ax.contour(X, Y, Z, levels=levels, colors='#aaaaaa', linewidths=0.8)
    ax.plot(path[:, 0], path[:, 1], color=color, lw=2.5, alpha=0.85)
    ax.plot(path[:, 0], path[:, 1], 'o', color=color, markersize=4, alpha=0.6)
    ax.plot(START[0], START[1], 'o', color='#222', markersize=8,
            markeredgecolor='white', label='start')
    ax.plot(0, 0, '*', color='#f1c40f', markersize=18,
            markeredgecolor='#222', label='minimum')
    ax.set_xlim(-2.5, 0.5)
    ax.set_ylim(-1.0, 1.0)
    ax.set_xlabel('x  (low-curvature direction)', fontsize=11)
    ax.set_title(f'{name}: {len(path)-1} steps', fontsize=13, fontweight='bold', color=color)
    ax.grid(True, alpha=0.25)
    ax.set_axisbelow(True)
    ax.legend(loc='lower left', fontsize=9, framealpha=0.95)

axes[0].set_ylabel('y  (high-curvature direction)', fontsize=11)

fig.suptitle('Optimizer behavior on an anisotropic loss landscape '
             '(y has 16× higher curvature than x)',
             fontsize=13, y=1.02)
fig.text(0.5, -0.04,
         "SGD's single learning rate oscillates along the high-curvature y axis "
         "and crawls along x. Adam scales each parameter's step by its own gradient "
         "history, so the y-axis bounce is damped and progress along x is fast.",
         ha='center', fontsize=10, style='italic', color='#444')

OUT = (Path(__file__).resolve().parent.parent.parent /
       'part-2-understanding-llms/module-06-pretraining-scaling-laws/images')
save_figure(fig, OUT / 'fig-6.5.1-sgd-vs-adam.png')
fig.savefig(OUT / 'fig-6.5.1-sgd-vs-adam.svg', format='svg',
            bbox_inches='tight', pad_inches=0.1, facecolor='white')
print(f'Saved SVG: {OUT}/fig-6.5.1-sgd-vs-adam.svg')
