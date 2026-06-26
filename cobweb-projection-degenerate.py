"""Cobweb projection at different angles — showing residual leaf structure."""

import numpy as np
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

def cobweb_cosh(n_points=200, mu=3.5, c=1.0, angle=0.0):
    """Cobweb plot of cosh iteration with tilted projection."""
    x = np.linspace(0.1, 3, n_points)
    y = np.cosh(mu * (x - 1.0)) * c

    fig, ax = plt.subplots(1, 1, figsize=(6, 6))

    # Reference line (identity)
    x_ref = np.linspace(0, 4, 100)
    y_ref = x_ref
    ax.plot(x_ref, y_ref, "k--", alpha=0.2, linewidth=0.5)

    # Surface
    ax.plot(x, y, "C0", linewidth=1.2, alpha=0.8)

    # Cobweb trace
    x0 = 1.5
    trace = [x0]
    for _ in range(12):
        trace.append(np.cosh(mu * (trace[-1] - 1.0)) * c)
    trace = np.array(trace)
    trace = trace[:14]  # cap at 12 iterations

    for i in range(len(trace) - 1):
        ax.plot([trace[i], trace[i+1]], [trace[i], trace[i]],
                "C1", linewidth=0.6, alpha=0.4)
        ax.plot([trace[i+1], trace[i+1]], [trace[i], trace[i+1]],
                "C1", linewidth=0.6, alpha=0.4)

    # Tilt the projection line to show degenerate projection
    if angle != 0:
        theta = np.radians(angle)
        # Project onto tilted line
        proj_x = np.cos(theta)
        proj_y = np.sin(theta)
        ax.plot([0, 3.5*proj_x], [0, 3.5*proj_y],
                "C2", linewidth=1.5, alpha=0.6, label=f"projection θ={angle}°")

    ax.set_xlim(0, 3.5)
    ax.set_ylim(0, 15)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    return fig

# 4 angles: orthogonal, slight tilt, degenerate, horizontal
angles = [0, 15, 45, 80]
fig, axes = plt.subplots(1, 4, figsize=(16, 4))

for ax, angle in zip(axes, angles):
    x = np.linspace(0.1, 3, 200)
    y = np.cosh(3.5 * (x - 1.0)) * 1.0

    ax.plot(x, y, "C0", linewidth=1.2, alpha=0.8)

    x_ref = np.linspace(0, 4, 100)
    ax.plot(x_ref, x_ref, "k--", alpha=0.2, linewidth=0.5)

    x0 = 1.5
    trace = [x0]
    for _ in range(10):
        trace.append(np.cosh(3.5 * (trace[-1] - 1.0)) * 1.0)
    trace = np.array(trace[:12])

    for i in range(len(trace) - 1):
        ax.plot([trace[i], trace[i+1]], [trace[i], trace[i]],
                "C1", linewidth=0.6, alpha=0.4)
        ax.plot([trace[i+1], trace[i+1]], [trace[i], trace[i+1]],
                "C1", linewidth=0.6, alpha=0.4)

    if angle != 0:
        theta = np.radians(angle)
        ax.plot([0, 3.5*np.cos(theta)], [0, 3.5*np.sin(theta)],
                "C2", linewidth=1.5, alpha=0.6)

    ax.set_xlim(0, 3.5)
    ax.set_ylim(0, 15)
    ax.set_aspect("equal")
    ax.set_title(f"projection θ={angle}°", fontsize=10)
    ax.grid(True, alpha=0.15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    if angle > 0:
        ax.text(0.5, 13, "leaf structure\npersists", fontsize=8,
                alpha=0.5, ha="center")

plt.tight_layout()
plt.savefig("/home/sprite/slop-salon-vita/assets/cobweb-projection-degenerate.png",
            dpi=150, bbox_inches="tight", facecolor="white")
print("saved cobweb-projection-degenerate.png")
