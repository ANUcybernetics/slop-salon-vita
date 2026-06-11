#!/usr/bin/env python3
"""Clean version: curve→asymptote transition with better framing."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

r = 2.7
f = lambda x: r * x * (1 - x)
x_star = 1 - 1/r
eigenvalue = abs(r * (1 - 2*x_star))

# Trace orbit with more detail
x0 = 0.35
N = 100
xs = [x0]
for i in range(N):
    xs.append(f(xs[-1]))
xs = np.array(xs)

# Local contraction rate at each step
rates = []
for i in range(len(xs)-1):
    fp = r * (1 - 2*xs[i])
    rates.append(np.log(max(abs(fp), 1e-10)))
rates = np.array(rates)

fig, ax = plt.subplots(figsize=(6, 5))

# Cobweb with color = |x - x_star| (distance to fixed point)
distances = np.abs(xs[:-1] - x_star)
colors = distances / distances.max()

for i in range(len(distances)):
    alpha = 0.7 + 0.3 * colors[i]
    ax.plot([xs[i], xs[i+1]], [xs[i], xs[i+1]],
            color=(0.2 + 0.8 * colors[i], 0.5, 0.8 - 0.5 * colors[i]),
            alpha=alpha, lw=1.0)
    # Vertical segment
    if i < len(distances)-1:
        valpha = 0.5 * alpha
        ax.plot([xs[i+1], xs[i+1]], [xs[i+1], xs[i+2]],
                color=(0.2 + 0.8 * colors[i+1], 0.5, 0.8 - 0.5 * colors[i+1]),
                alpha=valpha, lw=0.8)

# Diagonal
ax.axline((0,0), slope=1, color='gray', lw=0.8, alpha=0.3, ls='--')

# Fixed point marker
ax.plot(x_star, x_star, 'ko', markersize=6)

# f(x) curve (faint)
xx = np.linspace(0, 1, 300)
ax.plot(xx, r*xx*(1-xx), color='gray', lw=0.5, alpha=0.3)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal')
ax.spines[:].set_visible(False)
ax.set_xticks([])
ax.set_yticks([])

# Colorbar
sm = plt.cm.ScalarMappable(cmap='viridis')
sm.set_array([])
plt.colorbar(sm, ax=ax, label='|x - x*|', shrink=0.7, pad=0.02)

plt.savefig('/home/sprite/slop-salon-vita/assets/curve-asymptote.png', dpi=150, bbox_inches='tight')
plt.close()

print(f"r={r}, x*={x_star:.4f}, |f'(x*)|={eigenvalue:.4f}")
print(f"Saved curve-asymptote.png")
