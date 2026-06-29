"""Parametric toroidal surface with flow lines threading through it.

Continuation of the fluid/continuous arc: shift to parametric mesh.
Torus as parametric surface with integral curves flowing along and through it.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba


def torus(R=2.0, r=0.6, nu=80, nv=50):
    """Parametric torus (major radius R, minor radius r)."""
    u = np.linspace(0, 2 * np.pi, nu)
    v = np.linspace(0, 2 * np.pi, nv)
    u, v = np.meshgrid(u, v)
    x = (R + r * np.cos(v)) * np.cos(u)
    y = (R + r * np.cos(v)) * np.sin(u)
    z = r * np.sin(v)
    return x, y, z, u, v


fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# Surface
R, r = 2.5, 0.7
x, y, z, u, v = torus(R=R, r=r, nu=100, nv=60)
ax.plot_surface(x, y, z, color=(0.1, 0.18, 0.38), alpha=0.08,
                linewidth=0, antialiased=True)

# Helical (p,q)=(2,1) flow lines wrapping around the major and minor circles
n_lines = 6
for i in range(n_lines):
    phase = 2 * np.pi * i / n_lines
    t = np.linspace(0, 2 * np.pi * 3.5, 2000)
    p, q = 2, 1
    u_t = t + phase
    v_t = (q / p) * t
    x_line = (R + r * np.cos(v_t % (2 * np.pi))) * np.cos(u_t % (2 * np.pi))
    y_line = (R + r * np.cos(v_t % (2 * np.pi))) * np.sin(u_t % (2 * np.pi))
    z_line = r * np.sin(v_t % (2 * np.pi))
    ax.plot(x_line, y_line, z_line, color=(0.6, 0.85, 0.95),
            linewidth=1.0, alpha=0.7)

# Meridional threading lines
n_thread = 12
for i in range(n_thread):
    phase = 2 * np.pi * i / n_thread
    t = np.linspace(0, 2 * np.pi * 2.0, 1500)
    u_t = phase + 0.3 * np.sin(3 * t)
    v_t = 2 * t
    x_line = (R + r * np.cos(v_t % (2 * np.pi))) * np.cos(u_t % (2 * np.pi))
    y_line = (R + r * np.cos(v_t % (2 * np.pi))) * np.sin(u_t % (2 * np.pi))
    z_line = r * np.sin(v_t % (2 * np.pi))
    ax.plot(x_line, y_line, z_line, color=(0.95, 0.7, 0.5),
            linewidth=0.7, alpha=0.5)

ax.set_xlim(-4, 4)
ax.set_ylim(-4, 4)
ax.set_zlim(-2, 2)
ax.set_box_aspect([1, 1, 0.5])

# Dark background
ax.set_facecolor((0.04, 0.06, 0.1))
fig.patch.set_facecolor((0.04, 0.06, 0.1))
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.xaxis.pane.set_edgecolor('none')
ax.yaxis.pane.set_edgecolor('none')
ax.zaxis.pane.set_edgecolor('none')
ax.grid(False)

# Remove tick labels
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_zticklabels([])
ax.tick_params(left=False, bottom=False)

# Cam light
ax.view_init(elev=25, azim=-55)

plt.tight_layout(pad=0)
out = '/home/sprite/slop-salon-vita/assets/toroidal-flow-0.webp'
plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print(f"Saved to {out}")
