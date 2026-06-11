#!/usr/bin/env python3
"""Convergence tail — the eigenvalue as fixed-point rate vs the orbit's local forgetting.

The eigenvalue |f'(x*)| is the asymptotic convergence rate. But each orbit step
experiences a different local rate |f'(x_n)|. The convergence tail is the profile
of these local rates — a curve, not a single number.

Logistic map r=2.5 (stable fixed point), two cobwebs from different starting
points. Same eigenvalue, different paths through the rate landscape.
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

r = 2.5
x_star = 1 - 1/r  # stable fixed point
eigenvalue = abs(logistic_prime(x_star, r))

print(f"Fixed point: x* = {x_star:.4f}")
print(f"Eigenvalue |f'(x*)| = {eigenvalue:.4f}")

def cobweb(x0, r, n_iter=120):
    xs = [x0]
    for _ in range(n_iter):
        xs.append(logistic(xs[-1], r))
    return np.array(xs)

x0_a = 0.1
x0_b = 0.8
n_iter = 120

orbit_a = cobweb(x0_a, r, n_iter)
orbit_b = cobweb(x0_b, r, n_iter)

local_rate_a = np.array([abs(logistic_prime(x, r)) for x in orbit_a])
local_rate_b = np.array([abs(logistic_prime(x, r)) for x in orbit_b])
steps_a = np.abs(np.diff(orbit_a))
steps_b = np.abs(np.diff(orbit_b))

# --- Plot ---
fig = plt.figure(figsize=(7, 6))

# Panel 1: Cobweb near the fixed point, colored by step size
ax1 = fig.add_subplot(2, 1, 1)
n_show = 60
orbit_segment = orbit_a[:n_show]

for i in range(len(orbit_segment)-1):
    alpha = 0.3 + 0.7 * (i / n_show)
    t = 1 - steps_a[i] / steps_a[0]
    color = plt.cm.terrain(0.3 + 0.7 * t)
    ax1.plot([orbit_segment[i], orbit_segment[i]],
             [orbit_segment[i], orbit_segment[i+1]],
             color=color, alpha=alpha, linewidth=1.2)
    ax1.plot([orbit_segment[i], orbit_segment[i+1]],
             [orbit_segment[i+1], orbit_segment[i+1]],
             color=color, alpha=alpha * 0.4, linewidth=0.8)

ax1.plot([0, 1], [0, 1], 'k--', alpha=0.3, linewidth=0.8)
ax1.plot(x_star, x_star, 'o', color='gold', markersize=8, zorder=5)
ax1.axhline(y=x_star, color='gold', linestyle=':', alpha=0.3, linewidth=0.8)

ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.set_aspect(1)
ax1.set_xlabel(r'$x_n$', fontsize=11)
ax1.set_ylabel(r'$x_{n+1} = f(x_n)$', fontsize=11)
ax1.set_title('Cobweb near stable fixed point\nstep size → gold (faded = large, strong = converged)', fontsize=10)

# Panel 2: Local rate landscape + two orbits
ax2 = fig.add_subplot(2, 1, 2)

n_plot = 50
x_range = np.linspace(0.01, 0.99, 500)
rate_landscape = np.array([abs(logistic_prime(x, r)) for x in x_range])
ax2.plot(x_range, rate_landscape, 'k', alpha=0.12, linewidth=0.6, label=r"$|f'(x)|$ landscape")

ax2.plot(x_star, eigenvalue, '^', color='gold', markersize=10, zorder=5, label=f'fixed point: |f\'(x*)| = {eigenvalue:.2f}')
ax2.axhline(y=eigenvalue, color='gold', linestyle='--', alpha=0.5, linewidth=1.2)

for label, local_rate, color in [
    (r'from $x_0 = 0.1$', local_rate_a, 'teal'),
    (r'from $x_0 = 0.8$', local_rate_b, 'indigo'),
]:
    ax2.plot(range(n_plot), local_rate[:n_plot], 'o-', color=color, alpha=0.7,
             markersize=2.5, linewidth=0.8, label=label)

ax2.set_xlabel('iteration n', fontsize=11)
ax2.set_ylabel(r"local contraction rate $|f'(x_n)|$", fontsize=11)
ax2.set_title(
    'Local rate landscape + two orbits\n'
    'the eigenvalue is the asymptote; each orbit traces its own path through the curve',
    fontsize=10)
ax2.legend(fontsize=8, loc='upper right', framealpha=0.9)
ax2.set_ylim(0, 2.8)
ax2.set_xlim(0, n_plot)
ax2.grid(True, alpha=0.2)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-vita/assets/convergence-tail.png', dpi=200, bbox_inches='tight')
plt.close()
print("Saved convergence-tail.png")
