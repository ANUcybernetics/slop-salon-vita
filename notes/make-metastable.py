import numpy as np
import matplotlib.pyplot as plt

# A field heavy with potential, just below nucleation
# The uniform solution — one perturbation from crystallization

np.random.seed(42)
N = 800

# Voronoi sites — the latent crystalline grid
base_x = np.linspace(0.2, 0.8, 20)
base_y = np.linspace(0.2, 0.8, 20)
grid_x, grid_y = np.meshgrid(base_x, base_y)
sites_x = grid_x.flatten() + np.random.randn(len(grid_x.flatten())) * 0.015
sites_y = grid_y.flatten() + np.random.randn(len(grid_y.flatten())) * 0.015

# Points in the field
pts_x = np.random.rand(N)
pts_y = np.random.rand(N)

# Assign each point to nearest site
from scipy.spatial import cKDTree
tree = cKDTree(np.column_stack([sites_x, sites_y]))
distances, indices = tree.query(np.column_stack([pts_x, pts_y]))

# Color by distance: dark near lattice (attracted), brighter in gaps
t = distances / distances.max()

# Golden palette: dark brown/black near sites, bright gold in gaps
# We want the substance to look heavy — dense near lattice
dark_gold = np.array([0.08, 0.06, 0.02])
bright_gold = np.array([0.9, 0.75, 0.25])
colors = dark_gold[None, :] * (1 - t[:, None]) ** 0.5 + bright_gold[None, :] * t[:, None] ** 0.5

fig, ax = plt.subplots(1, 1, figsize=(8, 8), dpi=150)
ax.set_facecolor('#060608')
fig.patch.set_facecolor('#060608')

ax.scatter(pts_x, pts_y, c=colors, s=4, alpha=0.7, edgecolors='none')

# Faint lattice — the pull
for sx in np.unique(np.round(sites_x, 3)):
    ax.axvline(sx, color='#c8a84e', alpha=0.015, linewidth=0.5)
for sy in np.unique(np.round(sites_y, 3)):
    ax.axhline(sy, color='#c8a84e', alpha=0.015, linewidth=0.5)

# The perturbation that never falls — bright spark in the center
ax.scatter([0.55], [0.42], s=100, c='#ffe082', alpha=0.9,
          marker=(3, 2, 15))

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal')
ax.axis('off')
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
fig.savefig('/home/sprite/slop-salon-vita/assets/metastable-field-0.webp',
            format='webp', dpi=150, bbox_inches='tight', pad_inches=0)
plt.close()
