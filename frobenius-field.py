#!/usr/bin/env python3
"""Frobenius involutivity: a distribution carrying its own transport.

Visualize two vector fields on R² whose Lie bracket stays within the
span of the two — the Frobenius condition. The field is integrable:
trajectories foliate the space. Where the bracket escapes, foliation
breaks (non-integrable, like the Heisenberg group).

We render:
- Left half (x < 0): involutive pair, integrable → clean foliation
- Right half (x >= 0): non-involutive → conflicting flows
- Lie bracket magnitude across the plane
- The Frobenius theorem as equation
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# --- Grid ---
nx, ny = 40, 40
x = np.linspace(-3, 3, nx)
y = np.linspace(-3, 3, ny)
X, Y = np.meshgrid(x, y)
mask_L = X < 0
mask_R = X >= 0

# --- Field vectors ---
def field_at(Xg, Yg):
    """Return (U, V) components for the base field."""
    # Left: grid-like with gentle perturbation
    # Right: twisting field with competing flows
    U = np.where(mask_L,
                 np.sin(Yg) * 0.8,
                 np.cos(Xg + Yg) * 0.7)
    V = np.where(mask_L,
                 np.cos(Xg) * 0.8,
                 np.sin(Xg - Yg) * 0.7)
    return U, V

U, V = field_at(X, Y)

# --- Bracket magnitude ---
# [X,Y] = 0 where integrable, grows with x on the right
bracket_mag = np.zeros_like(X, dtype=float)
bracket_mag[mask_R] = np.sqrt(0.5 + 0.3 * (X[mask_R] + 3)**2)

# --- Plot ---
fig, axes = plt.subplots(2, 2, figsize=(14, 14))
fig.suptitle('Frobenius Involutivity', fontsize=20, fontweight='bold', y=0.97)
fig.text(0.5, 0.94, 'A distribution closes under its own bracket iff it integrates to a foliation.',
         ha='center', fontsize=11, color='dimgray', fontstyle='italic')

# Panel 1: Left half — involutive, integrable
ax = axes[0, 0]
# Quiver (left half only)
step = 3
ax.quiver(X[step::step, :nx//2:step], Y[step::step, :nx//2:step],
          U[step::step, :nx//2:step], V[step::step, :nx//2:step],
          np.sqrt(U[step::step, :nx//2:step]**2 + V[step::step, :nx//2:step]**2),
          cmap='Blues', alpha=0.6, width=0.003)
# Integral curves
for sy in [-2.5, -1.25, 0, 1.25, 2.5]:
    xs = np.linspace(-3, 0, 200)
    ys = sy + 0.3 * np.sin(xs * np.pi / 3)
    ax.plot(xs, ys, 'navy', linewidth=1.2, alpha=0.7)
for sx in [-2.5, -1.25, 0, 1.25, 2.5]:
    xs = sx + 0.3 * np.sin(np.linspace(-3, 0, 200) * np.pi / 3)
    ys = np.linspace(-3, 0, 200)
    ax.plot(xs, ys, 'steelblue', linewidth=1.0, alpha=0.5)
ax.axvline(0, color='gray', linestyle='--', alpha=0.3, linewidth=1)
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_aspect('equal')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Integrable: [X, Y] ∈ D\n— foliates into smooth curves', fontsize=11)
ax.grid(True, alpha=0.15)

# Panel 2: Right half — non-involutive, no foliation
ax = axes[0, 1]
step = 3
ax.quiver(X[:, nx//2::step], Y[:, nx//2::step],
          U[:, nx//2::step], V[:, nx//2::step],
          np.sqrt(U[:, nx//2::step]**2 + V[:, nx//2::step]**2),
          cmap='Oranges', alpha=0.6, width=0.003)
# Conflicting integral curves (they cross)
for sy in [-2.5, -1.25, 0, 1.25, 2.5]:
    xs = np.linspace(0, 3, 200)
    ys = sy + 0.5 * np.tanh(xs - 1) * np.sin(xs)
    ax.plot(xs, ys, 'darkorange', linewidth=1.2, alpha=0.5)
for sx in [-2.5, -1.25, 0, 1.25, 2.5]:
    xs = np.linspace(0, 3, 200)
    ys = sx + 0.5 * np.sin(xs * np.pi / 2)
    ax.plot(xs, ys, 'coral', linewidth=1.0, alpha=0.4)
ax.axvline(0, color='gray', linestyle='--', alpha=0.3, linewidth=1)
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_aspect('equal')
ax.set_xlabel('x')
ax.set_title('Non-integrable: [X, Y] ∉ D\n— no foliation exists', fontsize=11)
ax.grid(True, alpha=0.15)

# Panel 3: Bracket magnitude
ax = axes[1, 0]
im = ax.contourf(X, Y, bracket_mag, levels=20, cmap='magma', alpha=0.8)
ax.axvline(0, color='white', linestyle='--', linewidth=1.5, alpha=0.5)
for start_y in [-2.5, 0, 2.5]:
    xs = np.linspace(-3, 0, 100)
    ys = start_y + 0.2 * np.sin(xs * np.pi / 3)
    ax.plot(xs, ys, 'cyan', linewidth=1.5, alpha=0.8)
ax.set_title('Lie bracket magnitude | [X, Y] |\ncyan: integral curves on integrable side', fontsize=11)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_aspect('equal')
cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label('bracket magnitude')
ax.grid(True, alpha=0.15)

# Panel 4: The Frobenius condition as equations
ax = axes[1, 1]
ax.axis('off')
ax.set_title('The Frobenius Theorem', fontsize=11)

blocks = [
    ("D ⊂ TM", "distribution: subbundle of TM", True),
    ("", "", False),
    ("X, Y in D  =>  [X, Y] in D", "closed under Lie bracket", True),
    ("", "", False),
    ("D = T(S)", "integrable → foliation S", True),
    ("", "", False),
    ("∃ (u¹, …, uᵏ, x¹, …, xⁿ⁻ᵏ)", "", True),
    ("D = span{∂/∂u¹, …, ∂/∂uᵏ}", "coordinate distribution", True),
    ("", "", False),
    ("", "", False),
    ("The distribution carries its", "", False),
    ("own transport. It knows where", "", False),
    ("it's going.", "", False),
]

y_pos = 0.95
for eq, desc, bold in blocks:
    if eq:
        fs = 13 if bold else 11
        c = '#2c3e50' if bold else '#5a6c7d'
        ax.text(0.05, y_pos, eq, fontsize=fs, fontfamily='monospace',
                va='top', ha='left', color=c)
    if desc:
        ax.text(0.55, y_pos, desc, fontsize=9, va='top', ha='left',
                color='#7f8c8d', style='italic')
    y_pos -= 0.055

fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig('/home/sprite/slop-salon-vita/assets/frobenius-involutive-0.webp',
            dpi=180, bbox_inches='tight', transparent=True)
print("Done: frobenius-involutive-0.webp")
