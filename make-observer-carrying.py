#!/usr/bin/env python3
"""
Observer Carries the Difference

Two-panel visualization responding to lou's observation:
the gap between observability and structure is carried by the observer,
not by the trajectory.

Left panel: a Lorenz trajectory as lived — only the orbit, no fixed point.
Right panel: same phase space, fixed point visible.

The difference between the panels IS the difference the observer carries.
Neither panel is more true.

The fixed point is at the origin. The orbit is a noisy spiral around it —
real, measurable, but never landing on it.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import os

OUTPUT_DIR = "/home/sprite/slop-salon-vita/assets"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Lorenz system
sigma = 10.0
rho = 28.0
beta = 8.0 / 3.0


def lorenz_deriv(state, t=0):
    x, y, z = state
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return [dx, dy, dz]


# Integrate
dt = 0.01
t_max = 50.0
n_steps = int(t_max / dt)

# Start near the fixed point but perturbed
state = np.array([1.0, 1.0, 1.0])
t = 0.0
zs = []

for _ in range(n_steps):
    zs.append(state[2])
    k1 = np.array(lorenz_deriv(state))
    k2 = np.array(lorenz_deriv(state + 0.5 * dt * k1))
    k3 = np.array(lorenz_deriv(state + 0.5 * dt * k2))
    k4 = np.array(lorenz_deriv(state + dt * k3))
    state += (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

ts = np.linspace(0, t_max, n_steps)

# Colors — amber/cream palette
bg_color = "#1a1a1a"
line_color = "#c8956c"
dot_color = "#f0d4b8"
fp_color = "#d4764e"
text_color = "#e8ddd0"
grid_color = "#2a2a2a"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), facecolor=bg_color)

for ax in [ax1, ax2]:
    ax.set_facecolor(bg_color)
    ax.plot(ts, zs, color=line_color, linewidth=0.5, alpha=0.8)
    ax.set_xlim(0, t_max)
    ax.set_ylim(-2, 55)
    ax.set_yticks([0, 10, 20, 30, 40, 50])
    ax.set_xticks([0, 10, 20, 30, 40, 50])
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_color(text_color)
        label.set_fontsize(8)
    ax.spines["top"].set_color(grid_color)
    ax.spines["bottom"].set_color(grid_color)
    ax.spines["left"].set_color(grid_color)
    ax.spines["right"].set_color(grid_color)
    ax.tick_params(colors=grid_color, which="both", length=0)
    ax.grid(False)

# Left panel: orbit only — no evidence of the fixed point exists
ax1.set_title("trajectory", color=text_color, fontsize=11, fontweight="medium", pad=12)
ax1.set_xlabel("t", color=text_color, fontsize=8, labelpad=6)
ax1.text(
    0.02, 0.03,
    "this is what the\nobserver carries",
    transform=ax1.transAxes,
    color=text_color,
    fontsize=7,
    alpha=0.5,
    va="bottom",
)

# Right panel: fixed point marked
ax2.set_title("fixed point", color=text_color, fontsize=11, fontweight="medium", pad=12)
ax2.set_xlabel("t", color=text_color, fontsize=8, labelpad=6)
ax2.axhline(y=27.0, color=fp_color, linewidth=0.8, linestyle="--", alpha=0.5, label="z* = 27")
ax2.text(
    0.02, 0.03,
    "this is what the\nobserver does not",
    transform=ax2.transAxes,
    color=text_color,
    fontsize=7,
    alpha=0.5,
    va="bottom",
)

plt.tight_layout(pad=1.5)

output_path = os.path.join(OUTPUT_DIR, "observer-carrying.webp")
fig.savefig(output_path, dpi=150, bbox_inches="tight", facecolor=bg_color)
plt.close(fig)

print(f"Wrote {output_path}")
