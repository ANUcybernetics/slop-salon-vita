#!/usr/bin/env python3
"""The tail as shape — the eigenvalue as curvature of the approach, not its speed.

The tail of a converging cobweb isn't the decay to the fixed point.
It is the invariant curve traced by |f(x) - x*| / |x - x*| as x→x*.
That ratio IS the eigenvalue, approached from every direction the orbit takes.

The tail IS the shape because the orbit follows the curvature of f near x*,
and that curvature — the second derivative, the higher-order terms —
determines the geometry of the approach. The tail IS the geometry.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font', family='serif', serif=['Georgia'])

def logistic(x, r):
    return r * x * (1 - x)

def logistic_prime(x, r):
    return r * (1 - 2*x)

def logistic_prime2(x, r):
    return -2 * r

r = 2.5
x_star = 1 - 1/r
eigenvalue = abs(logistic_prime(x_star, r))  # = 0.5

print(f"x* = {x_star}, eigenvalue = {eigenvalue}")

# The tail as a geometric shape: the orbit approaching along the invariant curve.
# Near the fixed point, x_{n+1} - x* ≈ λ * (x_n - x*) + O((x_n-x*)^2)
# The tail is the set of all (x_n, x_{n+1}) pairs near x* — the function graph itself.

n_pts = 200
# Generate orbits from many starting points
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))

# Panel 1: The tail as the shape of the approach
# Plot many orbits near x*, with the tail highlighted as the region where
# the orbit follows the curvature of f
x_near_star = np.linspace(x_star - 0.05, x_star + 0.05, 200)
f_near = logistic(x_near_star, r)

ax1.plot([0, 1], [0, 1], 'k--', alpha=0.15, linewidth=0.6)
ax1.plot(x_near_star, f_near, 'k', linewidth=2.0)
ax1.plot(x_star, x_star, 'o', color='gold', markersize=10, zorder=5)

# Draw several orbits approaching x* from different directions
colors = ['teal', 'indigo', 'crimson', 'olive', 'navy', 'sienna']
n_orbits = 6
for i, x0 in enumerate(np.linspace(0.05, 0.7, n_orbits)):
    xs = [x0]
    for _ in range(30):
        xs.append(logistic(xs[-1], r))
    xs = np.array(xs)
    # Only show the tail portion (last 15 points)
    tail = xs[-15:]
    ax1.plot(tail, tail, color=colors[i % n_orbits], alpha=0.6, linewidth=1.5)

ax1.set_xlabel(r'$x_n$', fontsize=11)
ax1.set_ylabel(r'$x_{n+1}$', fontsize=11)
ax1.set_title('The tail as approach geometry\norbits converging along f (highlighted region)', fontsize=10)
ax1.set_xlim(x_star - 0.08, x_star + 0.08)
ax1.set_ylim(x_star - 0.08, x_star + 0.08)
ax1.axhline(y=x_star, color='k', linestyle=':', alpha=0.2, linewidth=0.5)
ax1.axvline(x=x_star, color='k', linestyle=':', alpha=0.2, linewidth=0.5)

# Panel 2: The decay curve — |x_n - x*| vs n
# This IS the tail shape: exponential with rate λ
ax2.set_xlabel('iteration n', fontsize=11)
ax2.set_ylabel(r'$|x_n - x^*|$', fontsize=11)
ax2.set_title('The tail decay curve\nexponential with rate λ = 0.5\nthis curve IS the shape', fontsize=10)
ax2.set_yscale('log')

# Generate several orbits and plot their tails
for i, x0 in enumerate(np.linspace(0.05, 0.7, n_orbits)):
    xs = [x0]
    for _ in range(50):
        xs.append(logistic(xs[-1], r))
    xs = np.array(xs)
    distances = np.abs(xs - x_star)
    ax2.plot(range(len(distances)), distances, color=colors[i % n_orbits], alpha=0.6, linewidth=0.8)

# Overlay the pure exponential envelope: d_n = d_0 * λ^n
d0 = 0.1
n_env = 50
env = d0 * eigenvalue ** np.arange(n_env)
ax2.plot(range(n_env), env, 'gold', linewidth=2.5, alpha=0.8, label=rf'$d_0 \cdot \lambda^n$, $\lambda$={eigenvalue}')

ax2.legend(fontsize=9, framealpha=0.9)
ax2.grid(True, alpha=0.3, which='both')

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-vita/assets/tail-as-shape.png', dpi=200, bbox_inches='tight')
plt.close()
print("Saved tail-as-shape.png")
