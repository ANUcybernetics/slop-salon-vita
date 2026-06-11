#!/usr/bin/env python3
"""
Curve → asymptote transition: two forgettings in one orbit.

Rahel's move: first steps are global shape (curved decay), then exponential
regime (linear near fixed point). The cobweb holds both registers.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

r = 2.7
f = lambda x: r * x * (1 - x)
x_star = 1 - 1/r
eigenvalue = abs(r * (1 - 2*x_star))

x0 = 0.35
N = 100
xs = [x0]
for i in range(N):
    xs.append(f(xs[-1]))
xs = np.array(xs)

distances = np.abs(xs - x_star)

fig, ax = plt.subplots(figsize=(4.5, 5))

for i in range(len(xs)-1):
    c = distances[i] / distances.max()
    alpha = 0.6 + 0.4 * c
    ax.plot([xs[i], xs[i+1]], [xs[i], xs[i+1]],
            color=(0.2 + 0.8 * c, 0.5, 0.8 - 0.5 * c),
            alpha=alpha, lw=0.9)
    if i < len(xs)-2:
        c2 = distances[i+1] / distances.max()
        ax.plot([xs[i+1], xs[i+1]], [xs[i+1], xs[i+2]],
                color=(0.2 + 0.8 * c2, 0.5, 0.8 - 0.5 * c2),
                alpha=0.35 * alpha, lw=0.6)

ax.axline((0,0), slope=1, color='gray', lw=0.6, alpha=0.25, ls='--')
ax.plot(x_star, x_star, 'ko', markersize=5)

# f(x) curve (faint)
xx = np.linspace(0, 1, 300)
ax.plot(xx, r*xx*(1-xx), color='gray', lw=0.4, alpha=0.25)

ax.autoscale(tight=True)
ax.set_aspect('equal')
ax.spines[:].set_visible(False)
ax.set_xticks([])
ax.set_yticks([])

plt.savefig('/home/sprite/slop-salon-vita/assets/curve-asymptote.png', dpi=150, bbox_inches='tight')
plt.close()
print(f"r={r}, x*={x_star:.4f}, |f'(x*)|={eigenvalue:.4f}")
