import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Denser lattice, more trajectories, no Voronoi lines
# Focus: trajectories finding their centers, the field proliferating

N = 7
xs = np.linspace(-2.8, 2.8, N)
ys = np.linspace(-2.8, 2.8, N)
grid = np.array([(x, y) for x in xs for y in ys])
n_attractors = len(grid)

np.random.seed(42)
n_steps = 500
n_trajs = 80

def attract(x, y, grid):
    dists = np.sqrt((grid[:, 0] - x)**2 + (grid[:, 1] - y)**2)
    nearest = np.argmin(dists)
    target = grid[nearest]
    dx = (target[0] - x) * 0.12 + 0.03 * np.sin(x * 1.5 + y * 0.5)
    dy = (target[1] - y) * 0.12 + 0.03 * np.cos(x * 0.6 + y * 1.3)
    return dx, dy

fig, ax = plt.subplots(1, 1, figsize=(10, 10))
ax.set_facecolor('#050505')
fig.patch.set_facecolor('#050505')

# Draw trajectories
for i in range(n_trajs):
    x0, y0 = np.random.uniform(-4, 4, 2)
    traj_x, traj_y = [x0], [y0]
    x, y = x0, y0
    for _ in range(n_steps):
        dx, dy = attract(x, y, grid)
        x += dx
        y += dy
        if x**2 + y**2 > 25:  # escaped
            break
        traj_x.append(x)
        traj_y.append(y)
    if len(traj_x) < 5:
        continue
    for j in range(0, len(traj_x) - 1, 3):
        alpha = 0.03 + 0.4 * (j / len(traj_x))
        ax.plot(traj_x[j:j+2], traj_y[j:j+2], color='#d4a843', alpha=alpha, linewidth=0.8)

# Attractors — bright gold, layered
ax.scatter(grid[:, 0], grid[:, 1], c='#d4a843', s=25, zorder=5)

ax.set_xlim(-4.5, 4.5)
ax.set_ylim(-4.5, 4.5)
ax.set_aspect('equal')
ax.axis('off')
plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-vita/assets/divergence-lattice.png', dpi=150, facecolor='#050505')
plt.close()
print("done")
