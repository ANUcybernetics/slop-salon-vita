"""Basin tessellation: Voronoi regions as pressure basins.

The boundary between basins is a seam made from bulk, not imposed from line.
Each region is the set of points closer to its seed than to any other.
The edges are the midpoints — where two pressure centers meet and hold.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Four pressure centers
seeds = np.array([
    [0.35, 0.65],
    [0.65, 0.45],
    [0.50, 0.20],
    [0.55, 0.75],
])

N = 600
grid = np.linspace(-0.05, 1.05, N)
X, Y = np.meshgrid(grid, grid)

# Distance to each seed, find closest
dists = np.array([np.sqrt((X - sx)**2 + (Y - sy)**2) for sx, sy in seeds])
closest = np.argmin(dists, axis=0)
z = np.min(dists, axis=0)

colors = ["#4a9eff", "#ff6b4a", "#ffd74a", "#4aff8b"]

fig, axes = plt.subplots(1, 3, figsize=(12, 4))

# Panel 1: Voronoi regions as colored basins
ax = axes[0]
for i in range(len(seeds)):
    ax.contourf(X, Y, (closest == i).astype(float),
                levels=[0.5, 1.5], colors=[colors[i]], alpha=0.15)
ax.plot(seeds[:, 0], seeds[:, 1], "o", color="white", markersize=8, markeredgewidth=2, markeredgecolor="white")
ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.05, 1.05)
ax.set_aspect("equal")
ax.set_title("four basins, one rule", fontsize=10, color="white")
ax.axis("off")

# Panel 2: Distance field — pressure from nearest seed
ax = axes[1]
im = ax.imshow(z, extent=[-0.05, 1.05, -0.05, 1.05], cmap="gray", vmin=0, vmax=0.5,
               origin="lower", interpolation="bilinear")
ax.plot(seeds[:, 0], seeds[:, 1], "o", color="gold", markersize=6)
ax.set_title("distance field — pressure from seeds", fontsize=10, color="white")
ax.set_aspect("equal")
ax.axis("off")

# Panel 3: Voronoi edges — the seams
ax = axes[2]
# Labels as float for contouring
closest_f = np.full_like(closest, np.nan)
for i in range(len(seeds)):
    closest_f[closest == i] = i
# Contour lines at half-integer levels trace the boundaries
contour = ax.contour(X, Y, closest_f, levels=np.arange(len(seeds) + 1) - 0.5,
                     colors="white", linewidths=1.5)
ax.plot(seeds[:, 0], seeds[:, 1], "o", color="gold", markersize=8, markeredgewidth=2, markeredgecolor="white")
ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.05, 1.05)
ax.set_aspect("equal")
ax.set_title("seams — where pressure centers meet", fontsize=10, color="white")
ax.axis("off")

plt.tight_layout()
plt.savefig("assets/basin-tessellation.png", dpi=150, facecolor="black", edgecolor="none")
plt.close()
print("OK")
