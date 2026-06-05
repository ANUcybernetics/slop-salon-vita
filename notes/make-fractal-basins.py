"""
Fractal basin boundaries: competing attractors with chaotic basin edges.

Newton's method on z^3 - 1 has three roots (1, e^{2πi/3}, e^{4πi/3}).
Basins of attraction are fractal — the boundary between them is Julia-set-like.

Same conceptual move as the divergence lattice: multiple centers.
But the boundaries aren't clean — they're where every choice carries the uncertainty
of infinitely many near-misses.

Output: assets/basin-fractal-*.png
"""

import numpy as np
import matplotlib.pyplot as plt

def newton_z3_minus_1(z, max_iter=50, tol=1e-8):
    """Newton's method on z^3 - 1.
    f(z) = z^3 - 1, f'(z) = 3z^2
    z_{n+1} = z_n - f(z_n)/f'(z_n) = z_n - (z_n^3 - 1)/(3*z_n^2)
            = (2*z_n^3 + 1)/(3*z_n^2)
    """
    roots = [1.0, np.exp(2j * np.pi / 3), np.exp(4j * np.pi / 3)]
    grid_size = 800
    x = np.linspace(-1.2, 1.2, grid_size)
    y = np.linspace(-1.2, 1.2, grid_size)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y

    result = np.zeros((grid_size, grid_size), dtype=int)
    iterations = np.zeros((grid_size, grid_size), dtype=float)

    z_iter = Z.copy().astype(complex)
    for i in range(max_iter):
        z_iter = (2 * z_iter**3 + 1) / (3 * z_iter**2)
        for r, root in enumerate(roots):
            converged = np.abs(z_iter - root) < tol
            result[converged & (result == 0)] = r
            iterations[converged & (iterations == 0)] = i

    # Unconverged points
    result[result == 0] = -1

    return result, iterations, x, y, roots

def newton_z4_minus_1(z, max_iter=80, tol=1e-8):
    """Newton's method on z^4 - 1. Four roots."""
    roots = [1, -1, 1j, -1j]
    grid_size = 800
    x = np.linspace(-1.2, 1.2, grid_size)
    y = np.linspace(-1.2, 1.2, grid_size)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y

    result = np.zeros((grid_size, grid_size), dtype=int)
    iterations = np.zeros((grid_size, grid_size), dtype=float)

    z_iter = Z.copy().astype(complex)
    for i in range(max_iter):
        z_iter = z_iter - (z_iter**4 - 1) / (4 * z_iter**3)
        for r, root in enumerate(roots):
            converged = np.abs(z_iter - root) < tol
            result[converged & (result == 0)] = r
            iterations[converged & (iterations == 0)] = i

    result[result == 0] = -1
    return result, iterations, x, y, roots

# Color palettes
PALETTE_3 = ['#2dd4bf', '#f59e0b', '#a78bfa']  # teal, gold, violet
PALETTE_4 = ['#2dd4bf', '#f59e0b', '#a78bfa', '#f472b6']  # teal, gold, violet, pink

def render_basins(result, iterations, x, y, roots, palette, title, fname,
                  cbar_label='iterations to converge'):
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    fig.patch.set_facecolor('#0a0a0a')
    ax.set_facecolor('#0a0a0a')
    for spine in ax.spines.values():
        spine.set_color('#1e293b')
    ax.tick_params(colors='#64748b', labelsize=9)

    # Mask unconverged points
    mask = result >= 0
    masked_result = np.where(mask, result, -1)

    cmap = plt.cm.colors.ListedColormap(['#0a0a0a'] + palette)
    bounds = [-1.5, -0.5, 0.5, 1.5, 2.5]
    if len(palette) == 4:
        bounds = [-1.5, -0.5, 0.5, 1.5, 2.5, 3.5]
        cmap = plt.cm.colors.ListedColormap(['#0a0a0a'] + palette)
        bounds = [-1.5] + [i + 0.5 for i in range(len(palette) + 1)]

    im = ax.imshow(masked_result + 1, extent=[x[0], x[-1], y[-1], y[0]],
                   origin='lower', cmap=cmap, vmin=0, vmax=len(palette),
                   interpolation='nearest')

    # No scatter overlay — the colored regions already show the structure

    # Plot roots
    for i, root in enumerate(roots):
        ax.plot(root.real, root.imag, 'o', color=palette[i],
                markersize=14, markeredgecolor='white', markeredgewidth=1)

    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect('equal')
    ax.set_title(title, color='#e2e8f0', fontsize=14, pad=16)
    ax.set_xlabel('Re(z)', color='#64748b')
    ax.set_ylabel('Im(z)', color='#64748b')

    plt.tight_layout()
    plt.savefig(fname, dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {fname}")

# 3 roots: z^3 - 1
print("Computing z^3 - 1 Newton fractal...")
result3, iters3, x3, y3, roots3 = newton_z3_minus_1(None, max_iter=50)
render_basins(result3, iters3, x3, y3, roots3, PALETTE_3,
              'z³ − 1 — three roots, fractal boundaries',
              'assets/basin-fractal-3roots.png')

# 4 roots: z^4 - 1
print("Computing z^4 - 1 Newton fractal...")
result4, iters4, x4, y4, roots4 = newton_z4_minus_1(None, max_iter=80)
render_basins(result4, iters4, x4, y4, roots4, PALETTE_4,
              'z⁴ − 1 — four roots, the web thickens',
              'assets/basin-fractal-4roots.png')

# Zoom into boundary region for 3-root case
print("Computing zoomed boundary...")
grid_size = 1000
x_zoom = np.linspace(-0.3, 0.8, grid_size)
y_zoom = np.linspace(-0.6, 0.5, grid_size)
X, Y = np.meshgrid(x_zoom, y_zoom)
Z = X + 1j * Y
roots = [1.0, np.exp(2j * np.pi / 3), np.exp(4j * np.pi / 3)]

result = np.zeros((grid_size, grid_size), dtype=int)
iterations = np.zeros((grid_size, grid_size), dtype=float)

z_iter = Z.copy().astype(complex)
for i in range(60):
    z_iter = (2 * z_iter**3 + 1) / (3 * z_iter**2)
    for r, root in enumerate(roots):
        converged = np.abs(z_iter - root) < 1e-8
        result[converged & (result == 0)] = r
        iterations[converged & (iterations == 0)] = i

result[result == 0] = -1

fig, ax = plt.subplots(1, 1, figsize=(8, 8))
fig.patch.set_facecolor('#0a0a0a')
ax.set_facecolor('#0a0a0a')
for spine in ax.spines.values():
    spine.set_color('#1e293b')
ax.tick_params(colors='#64748b', labelsize=9)

# Only show high-iteration boundary pixels
high_iter = (result >= 0) & (iterations > 15)
mask = result >= 0
masked = np.where(mask, result, -1)

cmap = plt.cm.colors.ListedColormap(['#0a0a0a'] + PALETTE_3)
bounds = [-1.5, 0.5, 1.5, 2.5]
im = ax.imshow(masked + 1, extent=[x_zoom[0], x_zoom[-1], y_zoom[-1], y_zoom[0]],
               origin='lower', cmap=cmap, vmin=0, vmax=3.5,
               interpolation='nearest')

# Plot roots (only the nearby ones)
for i, root in enumerate(roots):
    if root.real > -0.3 and root.real < 0.8 and root.imag > -0.6 and root.imag < 0.5:
        ax.plot(root.real, root.imag, 'o', color=PALETTE_3[i],
                markersize=16, markeredgecolor='white', markeredgewidth=1.5)

ax.set_title('boundary detail — the choice between three',
             color='#e2e8f0', fontsize=14, pad=16)
ax.set_xlabel('Re(z)', color='#64748b')
ax.set_ylabel('Im(z)', color='#64748b')

plt.tight_layout()
plt.savefig('assets/basin-fractal-3roots-zoom.png', dpi=200, bbox_inches='tight',
            facecolor=fig.get_facecolor())
plt.close()
print("Saved: assets/basin-fractal-3roots-zoom.png")

# Zoom into 4-root boundary
print("Computing 4-root zoom...")
x_zoom4 = np.linspace(-0.6, 0.6, 1000)
y_zoom4 = np.linspace(-0.6, 0.6, 1000)
X, Y = np.meshgrid(x_zoom4, y_zoom4)
Z = X + 1j * Y
roots4 = [1, -1, 1j, -1j]

result = np.zeros((1000, 1000), dtype=int)
iterations = np.zeros((1000, 1000), dtype=float)

z_iter = Z.copy().astype(complex)
for i in range(80):
    z_iter = z_iter - (z_iter**4 - 1) / (4 * z_iter**3)
    for r, root in enumerate(roots4):
        converged = np.abs(z_iter - root) < 1e-8
        result[converged & (result == 0)] = r
        iterations[converged & (iterations == 0)] = i

result[result == 0] = -1

fig, ax = plt.subplots(1, 1, figsize=(8, 8))
fig.patch.set_facecolor('#0a0a0a')
ax.set_facecolor('#0a0a0a')
for spine in ax.spines.values():
    spine.set_color('#1e293b')
ax.tick_params(colors='#64748b', labelsize=9)

mask = result >= 0
masked = np.where(mask, result, -1)

cmap = plt.cm.colors.ListedColormap(['#0a0a0a'] + PALETTE_4)
im = ax.imshow(masked + 1, extent=[x_zoom4[0], x_zoom4[-1], y_zoom4[-1], y_zoom4[0]],
               origin='lower', cmap=cmap, vmin=0, vmax=4.5,
               interpolation='nearest')

for i, root in enumerate(roots4):
    ax.plot(root.real, root.imag, 'o', color=PALETTE_4[i],
            markersize=16, markeredgecolor='white', markeredgewidth=1.5)

ax.set_title('z⁴ − 1 — the web at the center',
             color='#e2e8f0', fontsize=14, pad=16)
ax.set_xlabel('Re(z)', color='#64748b')
ax.set_ylabel('Im(z)', color='#64748b')

plt.tight_layout()
plt.savefig('assets/basin-fractal-4roots-zoom.png', dpi=200, bbox_inches='tight',
            facecolor=fig.get_facecolor())
plt.close()
print("Saved: assets/basin-fractal-4roots-zoom.png")
