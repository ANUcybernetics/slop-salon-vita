#!/usr/bin/env python3
"""
Feigenbaum cascade visualization.

The bifurcation cascade: each interval shorter than the last by ratio δ ≈ 4.669.
Universal across all smooth single-humped maps.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

# Known bifurcation thresholds (period-doubling)
# r1: 1->2, r2: 2->4, r3: 4->8, r4: 8->16, r5: 16->32, r_inf: onset of chaos
r_bif = [3.0, 3.44949, 3.54409, 3.56441, 3.56876, 3.56969]
r_inf = 3.569946  # accumulation point

# Intervals
deltas = [r_bif[i+1] - r_bif[i] for i in range(len(r_bif)-1)]
# Ratios
ratios = [deltas[i] / deltas[i+1] for i in range(len(deltas)-1)]

print("Bifurcation thresholds:", [f"{r:.5f}" for r in r_bif])
print("Intervals:", [f"{d:.5f}" for d in deltas])
print("Ratios:", [f"{r:.4f}" for r in ratios])
print("Feigenbaum δ ≈ 4.6692")

# --- Generate bifurcation diagram data ---
r_min, r_max = 2.85, 3.62
n_r = 2000
n_iter = 1000
n_last = 200

r_vals = np.linspace(r_min, r_max, n_r)
x = np.full(n_r, 0.5)

# Warm up
for _ in range(n_iter - n_last):
    x = r_vals * x * (1 - x)

# Collect attractor points
xs_all = []
rs_all = []
for _ in range(n_last):
    x = r_vals * x * (1 - x)
    xs_all.append(x.copy())
    rs_all.append(r_vals.copy())

xs_all = np.concatenate(xs_all)
rs_all = np.concatenate(rs_all)

# --- Plot ---
fig, axes = plt.subplots(2, 1, figsize=(10, 9),
                          gridspec_kw={'height_ratios': [3, 1]})

ax = axes[0]
ax.scatter(rs_all, xs_all, s=0.08, c='#4dd9b5', alpha=0.5, linewidths=0)
ax.set_facecolor('#0d0d0d')
fig.patch.set_facecolor('#0d0d0d')

ax.set_xlim(r_min, r_max)
ax.set_ylim(0.0, 1.0)
ax.set_ylabel('attractor values', color='#aaaaaa', fontsize=10)
ax.tick_params(colors='#aaaaaa', labelsize=8)
for spine in ax.spines.values():
    spine.set_color('#333333')

# Mark bifurcation thresholds
colors_bif = ['#ff6b6b', '#ffaa44', '#ffdd44', '#88cc44', '#44aaff', '#cc88ff']
for i, (r, c) in enumerate(zip(r_bif[:5], colors_bif)):
    ax.axvline(r, color=c, linewidth=0.8, alpha=0.7, linestyle='--')
    ax.text(r + 0.002, 0.95, f'r₍{i+1}₎', color=c, fontsize=7, va='top')

# Mark r_inf
ax.axvline(r_inf, color='#ffffff', linewidth=1.0, alpha=0.5, linestyle=':')
ax.text(r_inf + 0.002, 0.95, 'r∞', color='#aaaaaa', fontsize=7, va='top')

ax.set_title('bifurcation cascade — logistic map', color='#dddddd', fontsize=11, pad=10)

# Remove x tick labels from top panel
ax.set_xticklabels([])

# --- Bottom panel: interval lengths on log scale ---
ax2 = axes[1]
ax2.set_facecolor('#0d0d0d')

interval_r_centers = [(r_bif[i] + r_bif[i+1])/2 for i in range(len(r_bif)-1)]
bar_colors = colors_bif[:len(deltas)]

# Draw bars (interval widths visualized as bars of height = interval length)
for i, (r_center, delta, c) in enumerate(zip(interval_r_centers, deltas, bar_colors)):
    ax2.bar(r_center, delta, width=(r_bif[i+1]-r_bif[i])*0.8,
            color=c, alpha=0.7, align='center')
    if i < len(ratios):
        ratio = ratios[i]
        ax2.text(r_center, delta * 1.1, f'÷{ratio:.2f}', color='#cccccc',
                 fontsize=7, ha='center', va='bottom')

ax2.set_yscale('log')
ax2.set_xlim(r_min, r_max)
ax2.set_ylabel('interval\nlength', color='#aaaaaa', fontsize=9)
ax2.set_xlabel('r', color='#aaaaaa', fontsize=10)
ax2.tick_params(colors='#aaaaaa', labelsize=8)
for spine in ax2.spines.values():
    spine.set_color('#333333')

# Annotate Feigenbaum constant
ax2.text(0.98, 0.95,
         'δ = lim(Δₙ/Δₙ₊₁) ≈ 4.669\nuniversal: logistic, quadratic, sine',
         transform=ax2.transAxes, color='#999999', fontsize=8,
         ha='right', va='top')

plt.tight_layout(pad=0.5)
plt.savefig('assets/feigenbaum-cascade.png', dpi=150, bbox_inches='tight',
            facecolor='#0d0d0d')
print("Saved assets/feigenbaum-cascade.png")
