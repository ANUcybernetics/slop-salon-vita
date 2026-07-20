import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Gradient flow of |z^n - z|^2 — what the coboundary does
# The vector field: grad f where f(z) = |z^n - z|^2
# grad f = 2 * (z^n - z) * n * |z|^(2n-2) * z^(n-1) ... simplified:
# In complex notation: df/dz̄ = (z^n - z) * n * z̄^(n-1)  -- but let's just use
# the real gradient components.
#
# f(x,y) = |z^n - z|^2 = (Re(z^n-z))^2 + (Im(z^n-z))^2
# grad f = (df/dx, df/dy)

def z_power(z, n):
    r, theta = np.abs(z), np.angle(z)
    rn = r**n
    return rn * np.cos(n*theta) + 1j * rn * np.sin(n*theta)

def f(z, n):
    w = z_power(z, n) - z
    return np.real(w * np.conj(w))

def gradient(z, n, eps=1e-8):
    fx = (f(z + eps, n) - f(z - eps, n)) / (2*eps)
    fy = (f(z + eps*1j, n) - f(z - eps*1j, n)) / (2*eps)
    return fx + 1j * fy

def stream_plot(n, ax, cmap='Spectral'):
    """Gradient flow lines — trajectories follow -grad f (steepest descent)"""
    x = np.linspace(-2, 2, 40)
    y = np.linspace(-2, 2, 40)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y

    # Compute gradient at each point
    F = gradient(Z, n)
    U = -F.real
    V = -F.imag

    # Zero out field near fixed points
    for root in [0] + list(np.roots([1] + [0]*(n-2) + [-1])):
        mask = np.abs(Z - root) < 0.15
        U[mask] = 0
        V[mask] = 0

    ax.streamplot(X, Y, U, V, color=U, cmap=cmap, density=1.5,
                  arrowstyle='->', arrowsize=1.2)

    # Mark fixed points (zeros of z^n - z)
    roots = [0] + list(np.roots([1] + [0]*(n-2) + [-1]))
    for root in roots:
        ax.plot(root.real, root.imag, 'ko', markersize=8)

    ax.set_title(f'z^{n}-z: gradient flow (steepest descent)', fontsize=12)
    ax.set_aspect('equal')
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_xlabel('Re(z)')
    ax.set_ylabel('Im(z)')
    ax.grid(True, alpha=0.3)

def level_set_plot(n, ax):
    """Contour of f(z) — coboundary as level sets"""
    x = np.linspace(-2, 2, 300)
    y = np.linspace(-2, 2, 300)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    W = z_power(Z, n) - Z
    F = np.real(W * np.conj(W))

    # Log scale for better dynamic range
    F_clipped = np.clip(F, 1e-8, None)
    log_F = np.log10(F_clipped)

    cf = ax.contourf(X, Y, log_F, levels=30, cmap='viridis')
    ax.contour(X, Y, log_F, levels=[0], colors='red', linewidths=2)

    roots = [0] + list(np.roots([1] + [0]*(n-2) + [-1]))
    for root in roots:
        ax.plot(root.real, root.imag, 'k*', markersize=12)

    ax.set_title(f'z^{n}-z: log-level sets (coboundary)', fontsize=12)
    ax.set_aspect('equal')
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.grid(True, alpha=0.3)

# Diptych: n=3 (collinear, trivial cocycle) vs n=4 (circular, obstruction)
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Stream plots
stream_plot(3, axes[0], cmap='plasma')
stream_plot(4, axes[1], cmap='magma')

fig.tight_layout()
fig.savefig('/home/sprite/slop-salon-vita/assets/gradient-flow-diptych.png', dpi=200,
            bbox_inches='tight', facecolor='white')
plt.close()

print("Done: gradient-flow-diptych.png")

# Now the level set diptych
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
level_set_plot(3, axes[0])
level_set_plot(4, axes[1])
fig.tight_layout()
fig.savefig('/home/sprite/slop-salon-vita/assets/level-set-diptych.png', dpi=200,
            bbox_inches='tight', facecolor='white')
plt.close()

print("Done: level-set-diptych.png")
