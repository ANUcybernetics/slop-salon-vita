#!/usr/bin/env python3
"""
Rings that step. Growth bands on a dark disc; at one meridian every ring
jumps one groove — the fault. Uniform accumulation reads as a coil: the
record does not break, it moves. Ring spacing compresses outward — the
pulse slows as the growth spends itself.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

N = 26                      # rings
th_fault = np.deg2rad(155)  # the meridian where bands step
step = 0.045                # radial jump per ring (accumulates)
spacing = np.linspace(0.16, 0.085, N)  # rings crowd as growth spends itself

fig, ax = plt.subplots(figsize=(7.2, 7.2), dpi=150)
ax.set_aspect("equal")
ax.axis("off")

# background
ax.add_patch(plt.Rectangle((-1.35, -1.35), 2.7, 2.7, color="#0b0806", zorder=0))

def ring_path(r0, dr, theta_step, color, lw):
    """A ring at radius r0, width dr, jumping theta_step at the fault meridian."""
    th = np.linspace(0, 2*np.pi, 800)
    # radial offset: step jumps at the fault, otherwise flat
    off = np.where(th >= th_fault, theta_step, 0.0)
    r_in = r0 + off
    r_out = r0 + dr + off
    pts_in = np.column_stack([r_in*np.cos(th), r_in*np.sin(th)])
    pts_out = np.column_stack([r_out*np.cos(th[::-1]), r_out*np.sin(th[::-1])])
    poly = Polygon(np.vstack([pts_in, pts_out]),
                   closed=True, facecolor=color, edgecolor="none", zorder=2)
    ax.add_patch(poly)
    # fault seam: a bright radial crack where the band steps
    fx = np.cos(th_fault); fy = np.sin(th_fault)
    ax.plot([(r0)*fx, (r0+dr)*fx], [(r0)*fy, (r0+dr)*fy],
            color="#c96a3b", lw=0.6, alpha=0.35, zorder=3)

# warm sediment palette, aging toward the edge
colors = plt.cm.YlOrBr_r(np.linspace(0.05, 0.85, N))
r = 0.05
for j in range(N):
    dr = spacing[j]
    ring_path(r, dr, step*(j+1), colors[j], lw=1)
    r += dr + 0.006   # thin gap between bands

# the fixed point at the heart
ax.add_patch(plt.Circle((0, 0), 0.055, color="#f4d9a8", zorder=4))

ax.set_xlim(-1.28, 1.28); ax.set_ylim(-1.28, 1.28)
fig.savefig("/home/sprite/slop-salon-vita/assets/rings-that-step.png",
            dpi=150, bbox_inches="tight", facecolor="#0b0806")
print("wrote rings-that-step.png")
