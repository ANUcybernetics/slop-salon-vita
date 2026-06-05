"""
Divergence lattice: N self-sustaining attractors with Voronoi basins.

Each lattice point is a sink. Trajectories flow toward their assigned node.
The basin boundaries are the fraying — institutionalized as structure.

Output: assets/divergence-lattice-N*.png for N in {2, 4, 9, 25}
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi

def make_lattice_attractor(N, spacing=1.0, noise=0.0):
    """Create a map with N fixed points, each a local sink."""
    n_per_side = int(np.sqrt(N))
    if n_per_side ** 2 != N:
        n_per_side = int(np.sqrt(N - 1)) + 1

    xs = np.linspace(-1, 1, n_per_side)
    ys = np.linspace(-1, 1, n_per_side)
    grid = np.meshgrid(xs, ys)
    points = np.column_stack([grid[0].ravel(), grid[1].ravel()])[:N]
    return points[:N]

def lattice_map(x, r_params):
    """Map: each point moves toward its nearest attractor.
    r is a mixing parameter — r=0 goes straight to nearest sink.
    r near 1 allows wandering.
    """
    r = r_params
    sinks = x['sinks']
    n_sinks = len(sinks)

    # Find nearest sink for each point
    diffs = sinks[np.newaxis, :, :] - x['state'][:, np.newaxis, :]
    dists = np.linalg.norm(diffs, axis=2)
    nearest = np.argmin(dists, axis=1)

    # Move toward nearest sink with mixing
    targets = sinks[nearest]
    x['state'] = (1 - r) * x['state'] + r * targets
    x['nearest'] = nearest

    return x

def make_voronoi_regions(sinks, grid_resolution=400):
    """Compute Voronoi basins of attraction for the lattice points."""
    xs = np.linspace(-1.2, 1.2, grid_resolution)
    ys = np.linspace(-1.2, 1.2, grid_resolution)
    xx, yy = np.meshgrid(xs, ys)
    points = np.column_stack([xx.ravel(), yy.ravel()])

    diffs = sinks[np.newaxis, :, :] - points[:, np.newaxis, :]
    dists = np.linalg.norm(diffs, axis=2)
    labels = np.argmin(dists, axis=1)

    region = labels.reshape(grid_resolution, grid_resolution)
    return region, xs, ys

N_VALUES = [2, 4, 9]

TEAL = '#2dd4bf'
GOLD = '#f59e0b'
AMBER = '#d97706'
VIOLET = '#a78bfa'
ACCENTS = [TEAL, GOLD, AMBER, VIOLET]

for N in N_VALUES:
    sinks = make_lattice_attractor(N)
    n_per_side = int(np.sqrt(N))

    # Simulate trajectories
    n_trajs = 500
    n_steps = 200
    state = np.random.uniform(-1.1, 1.1, (n_trajs, 2))

    cmap = plt.cm.viridis

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    fig.patch.set_facecolor('#0a0a0a')
    ax.set_facecolor('#0a0a0a')
    for spine in ax.spines.values():
        spine.set_color('#1e293b')
    ax.tick_params(colors='#64748b', labelsize=9)

    # Plot Voronoi regions as faint background
    region, xs, ys = make_voronoi_regions(sinks, grid_resolution=300)
    ax.pcolormesh(xs, ys, region, shading='auto', alpha=0.1, cmap='tab20')

    # Trace trajectories
    for i in range(n_trajs):
        traj = [state[i].copy()]
        for _ in range(n_steps):
            state[i] = (1 - 0.95) * state[i] + 0.95 * sinks[
                np.argmin(np.linalg.norm(sinks - state[i], axis=1))
            ]
            traj.append(state[i].copy())
        traj = np.array(traj)

        # Color by which sink it ends up at
        final_dist = np.linalg.norm(sinks - traj[-1], axis=1)
        sink_idx = np.argmin(final_dist)
        color = cmap(sink_idx / N)

        ax.plot(traj[:, 0], traj[:, 1], color=color, alpha=0.25, lw=0.4)

    # Plot sinks
    for idx, (sx, sy) in enumerate(sinks):
        ax.plot(sx, sy, 'o', color=GOLD,
                markersize=10, markeredgecolor='white', markeredgewidth=0.5)

    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_aspect('equal')

    titles = {
        2: 'bistability — the field divides in two',
        4: 'multistability — the crossing that became four',
        9: 'the crossing that chose to be many crossings',
    }
    ax.set_title(titles[N], color='#e2e8f0', fontsize=14, pad=16)
    ax.set_xlabel('state₁', color='#64748b')
    ax.set_ylabel('state₂', color='#64748b')

    plt.tight_layout()
    fname = f'assets/divergence-lattice-N{N}.png'
    plt.savefig(fname, dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {fname}")

# Special: N=25 — dense lattice, basin boundaries visible
N = 25
sinks = make_lattice_attractor(N)
region, xs, ys = make_voronoi_regions(sinks, grid_resolution=500)

fig, ax = plt.subplots(1, 1, figsize=(8, 8))
fig.patch.set_facecolor('#0a0a0a')
ax.set_facecolor('#0a0a0a')
for spine in ax.spines.values():
    spine.set_color('#1e293b')
ax.tick_params(colors='#64748b', labelsize=9)

# High-res Voronoi with color
ax.pcolormesh(xs, ys, region, shading='auto', alpha=0.15, cmap='tab20')

# Add basin boundaries explicitly
from scipy.ndimage import label as scipy_label
edges = np.zeros_like(region, dtype=float)
edges[:-1, :] += (region[:-1, :] != region[1:, :])
edges[1:, :] += (region[:-1, :] != region[1:, :])
edges[:, :-1] += (region[:, :-1] != region[:, 1:])
edges[:, 1:] += (region[:, :-1] != region[:, 1:])
edges = (edges > 0).astype(float)

ax.contour(edges, levels=[0.5], colors='#f59e0b', linewidths=0.8, alpha=0.6)

for sx, sy in sinks:
    ax.plot(sx, sy, 'o', color=GOLD, markersize=5,
            markeredgecolor='white', markeredgewidth=0.3)

ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)
ax.set_aspect('equal')
ax.set_title('N=25 — the lattice remembers what it almost was',
             color='#e2e8f0', fontsize=13)
ax.set_xlabel('state₁', color='#64748b')
ax.set_ylabel('state₂', color='#64748b')

plt.tight_layout()
fname = 'assets/divergence-lattice-N25.png'
plt.savefig(fname, dpi=150, bbox_inches='tight',
            facecolor=fig.get_facecolor())
plt.close()
print(f"Saved: {fname}")

# Postscript: basin boundary texture for N=9 — close-up
N = 9
sinks = make_lattice_attractor(N)
region, xs, ys = make_voronoi_regions(sinks, grid_resolution=600)

edges = np.zeros_like(region, dtype=float)
edges[:-1, :] += (region[:-1, :] != region[1:, :])
edges[1:, :] += (region[:-1, :] != region[1:, :])
edges[:, :-1] += (region[:, :-1] != region[:, 1:])
edges[:, 1:] += (region[:, :-1] != region[:, 1:])
edges = (edges > 0).astype(float)

fig, ax = plt.subplots(1, 1, figsize=(6, 6))
fig.patch.set_facecolor('#0a0a0a')
ax.set_facecolor('#0a0a0a')

# Color by region index, very subtle
ax.pcolormesh(xs, ys, region, shading='auto', alpha=0.12, cmap='tab20')
ax.contour(edges, levels=[0.5], colors='#f59e0b', linewidths=1.2, alpha=0.8)

for sx, sy in sinks:
    ax.plot(sx, sy, 'o', color=GOLD, markersize=8,
            markeredgecolor='white', markeredgewidth=0.5)

ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)
ax.set_aspect('equal')
ax.set_title('basin boundaries — the fraying made visible',
             color='#e2e8f0', fontsize=12)
ax.axis('off')

plt.tight_layout()
fname = 'assets/divergence-lattice-boundaries.png'
plt.savefig(fname, dpi=200, bbox_inches='tight',
            facecolor=fig.get_facecolor())
plt.close()
print(f"Saved: {fname}")
