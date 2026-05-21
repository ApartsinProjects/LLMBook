"""Generate the emergence 'metric-choice' twin-curve figure (Schaeffer et al. 2023):
a smooth per-token accuracy A and the same capability scored by exact match (A^N),
which looks like a sharp 'emergent' jump purely from the nonlinear metric."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "part-15-llm-agentic-ai-research-frontiers/module-75-frontier-architectures/images/fig-75.1.2-metric-choice"
lx = np.linspace(7, 11, 400)               # log10(model parameters)
A = 0.55 + 0.4495 / (1 + np.exp(-(lx - 9.0) * 3.0))  # smooth per-token accuracy
N = 40
B = A ** N                                  # exact-match: all N tokens correct

fig, ax = plt.subplots(figsize=(7.4, 4.5))
ax.plot(lx, A, color="#1e88e5", lw=2.8, label="Per-token accuracy  A   (smooth metric)")
ax.plot(lx, B, color="#e53935", lw=2.8, label="Exact match = A$^{N}$  (sharp metric, N=40)")
ax.fill_between(lx, 0, B, color="#e53935", alpha=0.06)

idx = int(np.argmin(np.abs(B - 0.5)))
ax.annotate("apparent\n'emergence'", xy=(lx[idx], B[idx]), xytext=(lx[idx] - 1.5, 0.72),
            arrowprops=dict(arrowstyle="->", color="#b71c1c", lw=1.4),
            color="#b71c1c", fontsize=10, ha="center", fontweight="bold")
ax.set_xlabel("Model scale  (log₁₀ parameters)", fontsize=10)
ax.set_ylabel("Accuracy", fontsize=10)
ax.set_ylim(-0.02, 1.03)
ax.set_title("A nonlinear metric can manufacture 'emergence' from smooth scaling",
             fontsize=11.5, fontweight="bold")
ax.legend(loc="upper left", fontsize=9.5, frameon=False)
ax.grid(alpha=0.22)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
plt.tight_layout()
plt.savefig(OUT + ".svg")
plt.savefig(OUT + ".png", dpi=150)
print("wrote", OUT + ".svg / .png")
