import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path
from scipy.spatial import Voronoi

# Lattice of attractors on a black field
# Golden points, trajectories flowing to their nearest
# The Voronoi boundary is the fraying made structural

N = 5  # grid spacing

# Create a grid of attractors
xs = np.linspace(-3, 3, N)
ys = np.linspace(-3, 3, N)
grid = np.array([(x, y) for x in xs for y in ys])
n_attractors = len(grid)

# Generate trajectories from random starting points
np.random.seed(42)
n_steps = 200
n_trajs = 30

# Map: each step moves toward nearest attractor with slight perturbation
def attract(x, y, grid):
    dists = np.sqrt((grid[:, 0] - x)**2 + (grid[:, 1] - y)**2)
    nearest = np.argmin(dists)
    target = grid[nearest]
    # Gradient descent toward nearest, with slight drift
    dx = (target[0] - x) * 0.15 + 0.02 * np.sin(x * 1.3 + y * 0.7)
    dy = (target[1] - y) * 0.15 + 0.02 * np.cos(x * 0.8 + y * 1.1)
    return dx, dy

# Render
fig, ax = plt.subplots(1, 1, figsize=(8, 8))
ax.set_facecolor('#0a0a0a')
fig.patch.set_facecolor('#0a0a0a')

# Draw trajectories
for i in range(n_trajs):
    x0, y0 = np.random.uniform(-4, 4, 2)
    traj_x, traj_y = [x0], [y0]
    x, y = x0, y0
    for _ in range(n_steps):
        dx, dy = attract(x, y, grid)
        x += dx
        y += dy
        traj_x.append(x)
        traj_y.append(y)
    # Fade trajectory from transparent to golden
    for j in range(len(traj_x) - 1):
        alpha = 0.05 + 0.35 * (j / len(traj_x))
        ax.plot(traj_x[j:j+2], traj_y[j:j+2], color='#c9a84c', alpha=alpha, linewidth=0.6)

# Draw attractors — golden dots
ax.scatter(grid[:, 0], grid[:, 1], c='#c9a84c', s=40, zorder=5)

# Draw Voronoi boundaries as faint gray
if len(grid) > 4:
    vor = Voronoi(grid)
    for simplex in vor.ridge_vertices:
        simplex = np.asarray(simplex)
        if np.all(simplex >= 0):
            ax.plot(vor.vertices[simplex, 0], vor.vertices[simplex, 1],
                   color='#333333', linewidth=0.3)

ax.set_xlim(-4.5, 4.5)
ax.set_ylim(-4.5, 4.5)
ax.set_aspect('equal')
ax.axis('off')
plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-vita/assets/divergence-lattice.png', dpi=150, facecolor='#0a0a0a')
plt.close()
print("done")
