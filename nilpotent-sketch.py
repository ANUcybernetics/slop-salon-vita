#!/usr/bin/env python3
"""The nilpotent operator: N³ = 0. Trajectories collapse in at most 3 steps."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

N_POWER = 3  # N³ = 0
COLORS = ["#0d6e8a", "#1a8fa8", "#2db5c5", "#4ddde0"]
BG = "#0a0a0f"
TEXT = "#e8e4dd"

# N = [[0,1,0],[0,0,1],[0,0,0]] — N³ = 0
N = np.array([[0, 1, 0], [0, 0, 1], [0, 0, 0]], dtype=float)

fig, ax = plt.subplots(figsize=(6, 6))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

ax.set_xlim(-0.1, 1.1)
ax.set_ylim(-0.1, 1.1)

# Sample starting points across the space
np.random.seed(42)
points = np.random.uniform(0.05, 0.95, (80, 3))

for pt in points:
    x, y, z = pt
    path = [pt.copy()]
    for _ in range(N_POWER):
        x, y, z = y, z, 0.0
        path.append(np.array([y, z, 0.0]))
        if np.linalg.norm(path[-1]) < 1e-10:
            break

    path = np.array(path)
    alpha = max(0.08, 0.25 - 0.05 * len(path))
    c = COLORS[min(len(path) - 1, len(COLORS) - 1)]
    ax.plot(path[:, 0], path[:, 1], color=c, alpha=alpha, linewidth=0.6)

# Mark zero
ax.plot(0, 0, "o", color=TEXT, markersize=5, alpha=0.5)

ax.set_xlabel("$v$-component", color=TEXT, fontsize=9, family="monospace")
ax.set_ylabel("$w$-component", color=TEXT, fontsize=9, family="monospace")
ax.set_title(f"$N^{{{N_POWER}}}$ = 0: nilpotent collapse in $N$ steps", color=TEXT, fontsize=11, family="monospace")

ax.spines["top"].set_color("#222228")
ax.spines["bottom"].set_color("#222228")
ax.spines["left"].set_color("#222228")
ax.spines["right"].set_color("#222228")
ax.tick_params(colors=TEXT, which="both")
ax.set_xticks([0, 0.5, 1])
ax.set_xticklabels(["0", "0.5", "1"], color=TEXT, fontsize=8, family="monospace")
ax.set_yticks([0, 0.5, 1])
ax.set_yticklabels(["0", "0.5", "1"], color=TEXT, fontsize=8, family="monospace")

plt.tight_layout()
plt.savefig("/home/sprite/slop-salon-vita/assets/nilpotent-sketch.png",
            dpi=150, facecolor=BG, edgecolor="none")
plt.close()
