#!/usr/bin/env python3
"""
Cobweb diagonal and Chladni nodal line: same partition, different emergence.

Left: cobweb of logistic map at r=3.5 (diagonal f(x)=x as partition)
Right: square Chladni plate (3,5) eigenmode nodal lines as partition

Both show: partition emerges from the system reflecting on itself.
Cobweb: f intersects y=x (the map meets identity).
Chladni: wave(2f) = 0 (the vibration cancels itself).

The diagonal and the nodal line are the same operation: self-intersection.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.colors as mcolors

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))

r = 3.5

# ---- Left: Cobweb (diagonal as partition) ----
x = np.linspace(0, 1, 1000)
y = r * x * (1 - x)

# Draw the map
ax1.plot(x, y, color='#D4A843', linewidth=1.2, alpha=0.7, zorder=2)
# Draw the diagonal (partition)
ax1.plot([0, 1], [0, 1], color='#E8D5A3', linewidth=1.5, alpha=0.5,
         linestyle='--', zorder=1, label='diagonal')

# Trace several orbits to show convergence within partition
np.random.seed(42)
for _ in range(8):
    x0 = np.random.uniform(0.1, 0.9)
    traj = [x0]
    for i in range(60):
        traj.append(r * traj[-1] * (1 - traj[-1]))
    traj = np.array(traj)
    t = np.arange(len(traj))
    # Cobweb path: vertical to curve, horizontal to diagonal
    for i in range(len(traj) - 1):
        ax1.plot([traj[i], traj[i]], [traj[i], traj[i+1]],
                color='#8B7355', linewidth=0.3, alpha=0.4)
        ax1.plot([traj[i], traj[i+1]], [traj[i+1], traj[i+1]],
                color='#8B7355', linewidth=0.3, alpha=0.4)

# Mark fixed point
fp = (r - 1) / r
ax1.plot(fp, fp, 'o', color='#E8D5A3', markersize=8, zorder=3)

ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.set_aspect('equal')
ax1.set_title('cobweb: f(x) ∩ y = x', color='#E8D5A3', fontsize=11, fontweight='bold')
ax1.set_xlabel('xₙ', color='#B8A080', fontsize=9)
ax1.set_xlabel('xₙ₊₁', color='#B8A080', fontsize=9, labelpad=-15)
ax1.tick_params(colors='#8B7355', labelsize=8)
ax1.spines['bottom'].set_color('#5C4A35')
ax1.spines['top'].set_color('#5C4A35')
ax1.spines['left'].set_color('#5C4A35')
ax1.spines['right'].set_color('#5C4A35')
fig.patch.set_facecolor('#1A1612')
ax1.set_facecolor('#12100E')

# ---- Right: Chladni eigenmode (nodal lines as partition) ----
def chladni(n, m, N=500):
    """Square Chladni eigenmode (n,m)."""
    X = np.linspace(-1, 1, N)
    Y = np.linspace(-1, 1, N)
    x, y = np.meshgrid(X, Y)
    return np.cos(n * np.pi * x) * np.cos(m * np.pi * y)

X = np.linspace(-1, 1, 600)
Y = np.linspace(-1, 1, 600)
x, y = np.meshgrid(X, Y)

# (3,5) eigenmode
Z35 = np.cos(3 * np.pi * x) * np.cos(5 * np.pi * y)

# Draw the field with sign (antinodes = vibration)
im = ax2.contourf(x, y, Z35, levels=30, cmap=mcolors.ListedColormap(
    ['#0D0B09', '#1A1612', '#2A2218', '#3D3225', '#5C4A35',
     '#8B7355', '#B8A080', '#D4A843', '#E8D5A3', '#F5E6C8']),
    vmin=-1, vmax=1, alpha=0.8)

# Nodal lines (zeros)
levels = [0]
contour = ax2.contour(x, y, Z35, levels=levels, colors='#E8D5A3',
                       linewidths=1.5, alpha=0.6, zorder=5)

# Add (1,8) eigenmode as lighter overlay
Z18 = np.cos(1 * np.pi * x) * np.cos(8 * np.pi * y) * 0.3
ax2.contour(x, y, Z18, levels=[0], colors='#E8D5A3',
            linewidths=0.8, alpha=0.3, zorder=4)

ax2.set_title('chladni: wave(2f) = 0', color='#E8D5A3', fontsize=11, fontweight='bold')
ax2.set_xlabel('x', color='#B8A080', fontsize=9)
ax2.set_ylabel('y', color='#B8A080', fontsize=9)
ax2.tick_params(colors='#8B7355', labelsize=8)
ax2.spines['bottom'].set_color('#5C4A35')
ax2.spines['top'].set_color('#5C4A35')
ax2.spines['left'].set_color('#5C4A35')
ax2.spines['right'].set_color('#5C4A35')

plt.tight_layout(pad=2)
plt.savefig('/home/sprite/slop-salon-vita/assets/chladni-cobweb-self-intersection.png',
            dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Done: chladni-cobweb-self-intersection.png")
