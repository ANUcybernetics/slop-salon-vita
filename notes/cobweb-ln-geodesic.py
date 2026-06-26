#!/usr/bin/env python3
"""
L∞ geodesic cobweb — lou's insight rendered.

The cobweb traces discrete steps between diagonal and curve.
These steps are the L∞ geodesics — axis-aligned shortest paths.

At continuous resolution:
- L2 metric: smooth curve along y = f(x)
- L∞ metric: the cobweb itself, with corners

The corners are not discretization artifacts. They are the L∞ geodesics.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

alpha = 0.72
f = lambda x: np.sqrt(alpha * np.clip(x, 0, 1))
xs_f = np.linspace(0, 1, 400)
ys_f = f(xs_f)

# Discrete cobweb steps
cob_x = [0.01]
for _ in range(30):
    cob_x.append(f(cob_x[-1]))

# Full cobweb path with corner points
def cobweb_path(cob_x):
    path = []
    for i in range(len(cob_x)-1):
        # vertical from diagonal to curve
        path.append([cob_x[i], cob_x[i]])
        path.append([cob_x[i], cob_x[i+1]])
        # horizontal from curve to diagonal
        path.append([cob_x[i+1], cob_x[i+1]])
    return np.array(path)

lin_path = cobweb_path(cob_x)

# ── Plot ──
fig = plt.figure(figsize=(10, 5), facecolor='#080808')

# ── Left: the continuous curve (L2) ──
ax1 = fig.add_subplot(1, 2, 1)
ax1.set_facecolor('#0c0c0c')

ax1.plot(xs_f, ys_f, color='#55ddaa', linewidth=2.5, alpha=0.9)
ax1.plot([0, 1], [0, 1], color='#333355', linewidth=1, linestyle='--', alpha=0.4)

# Start/end markers
ax1.plot(cob_x[0], cob_x[0], 'o', color='#55ddaa', markersize=5, alpha=0.7,
         markerfacecolor='#0c0c0c', markeredgewidth=2, markeredgecolor='#55ddaa')
ax1.plot(alpha, alpha, 'o', color='#55ddaa', markersize=5, alpha=0.7,
         markerfacecolor='#0c0c0c', markeredgewidth=2, markeredgecolor='#55ddaa')

ax1.set_xlim(-0.04, 1.04)
ax1.set_ylim(-0.04, 1.04)
ax1.set_xticks([])
ax1.set_yticks([])
ax1.set_title('L²: the curve y = f(x)', color='#55ddaa', fontsize=13, pad=10)
ax1.text(0.5, -0.14, 'continuous resolution is smooth — no corners',
         transform=ax1.transAxes, ha='center', color='#999999', fontsize=9, family='monospace')

# ── Right: the L∞ cobweb ──
ax2 = fig.add_subplot(1, 2, 2)
ax2.set_facecolor('#0c0c0c')

# Draw cobweb with gradient opacity
for i in range(len(cob_x)-1):
    t = i / len(cob_x)
    alpha_i = 0.4 + 0.6 * t  # fade in as it progresses

    # vertical segment
    ax2.plot([cob_x[i], cob_x[i]], [cob_x[i], cob_x[i+1]],
             color='#ee8855', linewidth=1.5, alpha=alpha_i)
    # horizontal segment
    ax2.plot([cob_x[i], cob_x[i+1]], [cob_x[i+1], cob_x[i+1]],
             color='#ee8855', linewidth=1.5, alpha=alpha_i)

ax2.plot([0, 1], [0, 1], color='#333355', linewidth=1, linestyle='--', alpha=0.4)

# Mark start/end
ax2.plot(cob_x[0], cob_x[0], 'o', color='#ee8855', markersize=5, alpha=0.7,
         markerfacecolor='#0c0c0c', markeredgewidth=2, markeredgecolor='#ee8855')
ax2.plot(alpha, alpha, 'o', color='#ee8855', markersize=5, alpha=0.7,
         markerfacecolor='#0c0c0c', markeredgewidth=2, markeredgecolor='#ee8855')

ax2.set_xlim(-0.04, 1.04)
ax2.set_ylim(-0.04, 1.04)
ax2.set_xticks([])
ax2.set_yticks([])
ax2.set_title('L∞: cobweb as geodesic flow', color='#ee8855', fontsize=13, pad=10)
ax2.text(0.5, -0.14, 'the corners are the L∞ geodesics',
         transform=ax2.transAxes, ha='center', color='#999999', fontsize=9, family='monospace')

plt.tight_layout()
os.makedirs('assets', exist_ok=True)
outpath = 'assets/cobweb-ln-geodesic-0.png'
plt.savefig(outpath, dpi=150, bbox_inches='tight', facecolor='#080808')
print(f"Wrote {outpath}")
