#!/usr/bin/env python3
"""Commutator loop: AB A⁻¹ B⁻¹ as a trajectory through non-commuting transformations.

When A and B don't commute, the commutator loop doesn't close.
The trajectory traces the figure-eight that IS the commutator geometrically.

The self-intersection point is where the Jacobian vanishes — the fold.
"""

import numpy as np
import matplotlib.pyplot as plt

def A(p):
    """Rotation by 30 degrees."""
    theta = np.pi / 6
    x, y = p
    return (x * np.cos(theta) - y * np.sin(theta),
            x * np.sin(theta) + y * np.cos(theta))

def A_inv(p):
    """Inverse rotation: -30 degrees."""
    theta = -np.pi / 6
    x, y = p
    return (x * np.cos(theta) - y * np.sin(theta),
            x * np.sin(theta) + y * np.cos(theta))

def B(p, s=1.3):
    """Shear in x."""
    x, y = p
    return (x + s * y, y)

def B_inv(p, s=1.3):
    """Inverse shear."""
    x, y = p
    return (x - s * y, y)

def commutator(p):
    """AB A⁻¹ B⁻¹ applied to p."""
    q = B_inv(p)
    q = A_inv(q)
    q = B(q)
    q = A(q)
    return q

def Jacobian_determinant(p, eps=1e-6):
    """Numerical Jacobian determinant at p."""
    x, y = p
    # Numerical Jacobian matrix
    J = np.zeros((2, 2))
    f0 = commutator((x + eps, y))
    f1 = commutator((x, y + eps))
    f00 = commutator((x, y))
    J[0, 0] = (f0[0] - f00[0]) / eps
    J[0, 1] = (f1[0] - f00[0]) / eps
    J[1, 0] = (f0[1] - f00[1]) / eps
    J[1, 1] = (f1[1] - f00[1]) / eps
    return np.linalg.det(J)

# Generate commutator loops from a grid of starting points
fig, axes = plt.subplots(1, 2, figsize=(10, 5))

# Left: individual commutator trajectories
ax = axes[0]
N = 15
xs = np.linspace(-2, 2, N)
ys = np.linspace(-2, 2, N)

for x0 in xs:
    for y0 in ys:
        p = (x0, y0)
        trajectory = [p]
        for _ in range(4):
            p = commutator(p)
            trajectory.append(p)
        traj = np.array(trajectory)
        alpha_val = 0.3 + 0.7 * abs(Jacobian_determinant((x0, y0))) / 2.0
        ax.plot(traj[:, 0], traj[:, 1], 'c', alpha=alpha_val, linewidth=0.8)

# Draw the fixed point (origin) where figure-eight crosses
ax.plot(0, 0, 'w.', markersize=12, alpha=0.9)
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-2.5, 2.5)
ax.set_aspect('equal')
ax.axhline(0, color='w', alpha=0.1, linewidth=0.5)
ax.axvline(0, color='w', alpha=0.1, linewidth=0.5)
ax.set_title('com(m, n) = AB A⁻¹ B⁻¹', color='w', fontsize=10)
ax.set_xlabel('commutator = non-commutation traced as geometry', color='w', fontsize=8)
ax.invert_xaxis()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.set_xticks([])
ax.set_yticks([])

# Right: Jacobian determinant heatmap
ax2 = axes[1]
N_heat = 200
xh = np.linspace(-2, 2, N_heat)
yh = np.linspace(-2, 2, N_heat)
X, Y = np.meshgrid(xh, yh)
Z = np.zeros_like(X)
for i in range(N_heat):
    for j in range(N_heat):
        Z[j, i] = Jacobian_determinant((X[j, i], Y[j, i]))

# Clip for visualization
Z_clipped = np.clip(Z, -1, 1)
im = ax2.contourf(X, Y, Z_clipped, levels=30, cmap='twilight', extend='both')
ax2.contour(X, Y, Z_clipped, levels=[0], colors='gold', linewidths=2)
ax2.plot(0, 0, 'w.', markersize=15)
ax2.set_title('Jacobian determinant\n(commutator) — zero at fold locus', color='w', fontsize=9)
ax2.set_xlabel('determinant = 0 is the figure-eight crossing', color='w', fontsize=8)
ax2.invert_xaxis()
ax2.set_aspect('equal')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['bottom'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.set_xticks([])
ax2.set_yticks([])

plt.tight_layout()
plt.savefig('commutator-field.png', dpi=150, facecolor='black', edgecolor='none')
plt.close()

print("Done: commutator-field.png")
