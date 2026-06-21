"""
Fluid surface register: torus knot trajectories.
No horizon — the trajectories fold through themselves in 3D.
Every point sees the same topology. Closed curves with no boundary.
A torus knot wraps p times poloidally, q times toroidally.
(3,5) knot: three poloidal loops, five toroidal loops.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# Torus knot: p=3, q=5
p, q = 3, 5
t = np.linspace(0, 2*np.pi, 2000)
R = 2.0  # major radius
r = 0.8  # minor radius

# Parametric torus knot
x = (R + r*np.cos(q*t)) * np.cos(p*t)
y = (R + r*np.cos(q*t)) * np.sin(p*t)
z = r*np.sin(q*t)

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

ax.set_facecolor((0.02, 0.02, 0.03))
fig.patch.set_facecolor((0.02, 0.02, 0.03))

# Trace with varying color by z
norm = mpl.colors.Normalize(z.min(), z.max())
cmap = plt.get_cmap('magma')
colors = cmap(norm(z))

# Plot as a thick line by plotting segments
linewidths = np.ones_like(x) * 3
ax.scatter(x, y, z, c=colors, s=2, alpha=0.6)

ax.set_xlim([-4, 4])
ax.set_ylim([-4, 4])
ax.set_zlim([-2, 2])
ax.set_axis_off()
ax.view_init(elev=20, azim=30)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-vita/assets/fluid-surface-torus-knot.png',
            dpi=150, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()

print("torus knot saved")
