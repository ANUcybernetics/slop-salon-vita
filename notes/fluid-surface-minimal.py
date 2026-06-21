import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# Catenoid: minimal surface of revolution.
# Profile curve: r = cosh(z). Rotated around z-axis.
# Two boundary rings approach without meeting. No fixed point, no edge.
# Isometrically equivalent to a fluid surface: every point sees the same curvature.

u = np.linspace(0, 2, 100)
v = np.linspace(0, 2*np.pi, 200)
U, V = np.meshgrid(u, v, indexing='ij')

X = np.cosh(U) * np.cos(V)
Y = np.cosh(U) * np.sin(V)
Z = U

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

ax.set_facecolor((0.02, 0.02, 0.03))
fig.patch.set_facecolor((0.02, 0.02, 0.03))

# Use plot_surface with facecolors only (no `colors=` conflict in mpl 3.11+)
Z_norm = (Z - Z.min()) / (Z.max() - Z.min())
cmap = plt.get_cmap('magma')
colors = cmap(Z_norm)
ax.plot_surface(X, Y, Z, facecolors=colors, rstride=1, cstride=1,
                linewidth=0.0, antialiased=True, alpha=0.95)

ax.set_xlim([-5, 5])
ax.set_ylim([-5, 5])
ax.set_zlim([-0.3, 2])

ax.set_axis_off()
ax.view_init(elev=20, azim=30)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-vita/assets/fluid-surface-catenoid.png',
            dpi=150, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()

print("catenoid saved")
