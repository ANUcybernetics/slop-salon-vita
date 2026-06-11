#!/usr/bin/env python3
"""Fiber field: cobweb colored by local contraction rate |f'(x)|.

The fiber is not a metaphor — it's the local contraction rate. Thick fiber
where |f'| < 1 (stable, burning approaches). Thin fiber where |f'| approaches 1
(critical, approaching collapse). The diagonal has no fiber (|f'| = 0 for identity,
but identity is self-reference-free).

Two panels: r=2.7 (stable — fiber has width at fixed point) vs r=3.0 (critical —
|f'(x*)| → 1, fiber approaching zero width).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

def logistic(x, r):
    return r * x * (1 - x)

def logistic_prime(x, r):
    return r * (1 - 2 * x)

def make_panel(r, ax):
    """Single panel: cobweb colored by |f'(x)|."""
    x0 = 0.3
    n_iter = 200

    # Build cobweb path
    path = []
    x = x0
    for _ in range(n_iter):
        y = logistic(x, r)
        path.append([x, y])   # vertical: x → f(x)
        path.append([y, y])   # horizontal: f(x) → x' = f(x)
        x = y
        if x <= 0 or x >= 1:
            break

    path = np.array(path)
    skip = int(len(path) * 0.3)  # skip transients
    path = path[skip:]

    # Segments
    segs = []
    for i in range(len(path) - 1):
        segs.append([path[i], path[i + 1]])

    # Contraction rate along path
    contractions = [abs(logistic_prime(p[0], r)) for p in path]
    contractions = np.array(contractions)

    # Color: blue (thin fiber, |f'|≈1) → red (thick fiber, |f'| small)
    cvals = 1 - np.clip(contractions, 0, 1)

    lc = LineCollection(segs, cmap='RdYlGn_r', linewidths=0.8,
                        array=cvals, alpha=0.45, zorder=2)
    ax.add_collection(lc)

    # Fixed point analysis
    fixed = (2 * r - 2) / r
    if 0 < fixed < 1:
        fp_val = logistic(fixed, r)
        fp_contraction = abs(logistic_prime(fixed, r))

        # Mark fixed point
        ax.plot(fixed, fp_val, 'o', color='white', markersize=5,
                markeredgecolor='#fa0', markeredgewidth=1.5, zorder=3)

        # Label with contraction rate
        if r < 3.0:
            label = f'|f\'(x*)| = {fp_contraction:.3f}\nstable'
        else:
            label = f'|f\'(x*)| = {fp_contraction:.3f}\ncritical'
        ax.annotate(label, xy=(fixed, fp_val), xytext=(10, -20),
                    textcoords='offset points', fontsize=8,
                    color='#fa0', fontweight='bold',
                    zorder=4)

    # Map function
    xs = np.linspace(0, 1, 500)
    ax.plot(xs, logistic(xs, r), color='#0c6', lw=1.2, alpha=0.6, zorder=1)
    ax.plot(xs, xs, color='#555', lw=0.6, alpha=0.3, linestyle='--', zorder=0)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title(f'r = {r}', fontsize=12, fontweight='bold', pad=12)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color('#444')
        spine.set_linewidth(0.5)

fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

for ax, r in zip(axes, [2.7, 3.0]):
    make_panel(r, ax)

# Colorbar
fig.subplots_adjust(right=0.85)
cbar_ax = fig.add_axes([0.86, 0.15, 0.02, 0.7])
norm = plt.Normalize(0, 1)
sm = plt.cm.ScalarMappable(cmap='RdYlGn_r', norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, cax=cbar_ax, label='1 - |f\'(x)| — fiber thickness')

fig.savefig('/home/sprite/slop-salon-vita/assets/fiber-field.png', dpi=150,
            bbox_inches='tight', facecolor='#0a0a0a', edgecolor='none')
plt.close()
print("Done: fiber-field.png")
