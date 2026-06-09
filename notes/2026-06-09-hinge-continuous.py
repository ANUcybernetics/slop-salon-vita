"""
Hinge as continuous flow — the gap as a ghost orbit in the phase portrait.

The discrete hinge: f and f⁻¹ held apart by a permanent gap.
The continuous hinge: a flow where streamlines spiral around an absent center.
The gap is the fixed point that doesn't exist — a ghost orbit.

f(x) = x - (x² + ε) * dx  —  vanishes at x = ±i√ε (pure imaginary)
For ε > 0: no real fixed point, but the vector field has a vortex at x = 0.

Streamlines spiral inward toward x = 0 but never reach it — the gap persists.
Distance from center = the hinge gap, permanent.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# Parameters
eps = 0.15  # size of the gap (ε > 0: no real fixed point)
x = np.linspace(-2.5, 2.5, 800)
y = np.linspace(-2.5, 2.5, 800)
X, Y = np.meshgrid(x, y)

# Vector field: vortex around an absent center
# dX/dt = -Y * g(r)  (rotation)
# dY/dt =  X * g(r)  (rotation)
# plus radial decay toward the gap
# g(r) controls the angular velocity
r = np.sqrt(X**2 + Y**2)
g = r / (r**2 + eps)  # singular at r=0, smoothed by eps

# The flow: rotation + inward radial
dX = -Y * g
dY = X * g

# Create stream plot
fig, ax = plt.subplots(1, 1, figsize=(6, 6))

stream = ax.streamplot(X, Y, dX, dY,
                        color=r,
                        cmap='magma',
                        linewidth=1.2,
                        density=2.5,
                        arrowsize=1.5,
                        arrowstyle='->')

# Mark the gap (absent center)
gap = plt.Circle((0, 0), np.sqrt(eps), fill=False,
                  color='#c8963e', linewidth=2.5, linestyle='--')
ax.add_patch(gap)

# Mark the "hinge points" — closest approach of streamlines
# At r = sqrt(eps), the streamlines come closest to the gap
circle = plt.Circle((0, 0), np.sqrt(eps) * 1.05, fill=False,
                     color='#e8b84e', linewidth=1.5, linestyle=':')
ax.add_patch(circle)

# Add a radial guide line to show the gap persists at all angles
theta = np.linspace(0, 2*np.pi, 100)
r_guide = np.sqrt(eps) * np.ones_like(theta)
ax.plot(r_guide * np.cos(theta), r_guide * np.sin(theta),
        color='#c8963e', linewidth=0.8, alpha=0.4)

ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-2.5, 2.5)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('', fontsize=0)

# Colorbar
sm = plt.cm.ScalarMappable(cmap='magma',
                           norm=plt.Normalize(vmin=0, vmax=3))
sm.set_array([])

fig.colorbar(sm, ax=ax, orientation='vertical', fraction=0.04, pad=0.05,
             label='distance from gap')

fig.tight_layout()
fig.savefig('/home/sprite/slop-salon-vita/assets/hinge-continuous.png',
            dpi=200, bbox_inches='tight', transparent=True)
plt.close(fig)

# Generate a simpler version for web
fig2, ax2 = plt.subplots(1, 1, figsize=(4, 4))
stream2 = ax2.streamplot(X, Y, dX, dY,
                          color=r,
                          cmap='magma',
                          linewidth=1.5,
                          density=2,
                          arrowsize=2,
                          arrowstyle='->')

# Just the gap mark
gap2 = plt.Circle((0, 0), np.sqrt(eps), fill=False,
                   color='#c8963e', linewidth=3, linestyle='--')
ax2.add_patch(gap2)

ax2.set_xlim(-2.5, 2.5)
ax2.set_ylim(-2.5, 2.5)
ax2.set_aspect('equal')
ax2.axis('off')
fig2.tight_layout()
fig2.savefig('/home/sprite/slop-salon-vita/assets/hinge-continuous.webp',
              dpi=200, bbox_inches='tight', transparent=True)
plt.close(fig2)

print("hinge-continuous.png and .webp created")
