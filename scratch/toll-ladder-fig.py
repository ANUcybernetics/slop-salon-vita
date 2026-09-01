#!/usr/bin/env python3
"""the toll ladder — every rung pays the count.

toll_n = 55*sqrt(n^2+4) - 110 : the off-grid rate the never-struck hyp pays to
the count.  For every n>=1 it is OFF the 55-grid (sqrt(n^2+4) integral <=> n=0),
hovering strictly above the grid tone 55(n-2) by the gap
  g_n = 220/(sqrt(n^2+4)+n) = 110/AM(n, sqrt(n^2+4)),
which shrinks to 0 — the toll approaches the grid but never lands.  The ONE
landing is the seam rung n=0, where the triangle fuses: hyp = 110 = the count,
toll = 0.  n=2 is the toll the salon heard (45.56, silver, the miss doubled).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

rng = np.arange(0, 13)
toll = 55.0 * np.sqrt(rng**2 + 4) - 110.0
anchor = 55.0 * (rng - 2.0)
gap = toll - anchor

fig, ax = plt.subplots(figsize=(10.5, 6.8), dpi=200)

# the 55-grid
for k in range(0, 7):
    f = 55.0 * k
    ax.axhline(f, color="#c9c9c9", lw=0.8, zorder=1)
ax.axhline(0, color="#9a9a9a", lw=1.0, zorder=1)

# the anchor line 55(n-2) — the hover target, dashed
nn = np.linspace(0, 12, 400)
ax.plot(nn, 55.0 * (nn - 2.0), "--", color="#8a6d3b", lw=1.6, zorder=2,
        label="grid tone below: 55(n\u22122)")

# hover-gap segments
for n, t, a, g in zip(rng, toll, anchor, gap):
    ax.plot([n, n], [a, t], color="#c0392b", lw=2.2, alpha=0.85, zorder=3)

# toll points: seam (n=0) vs off-grid (n>=1)
seam = n == 0
ax.scatter(rng[~seam], toll[~seam], s=90, color="#c0392b", edgecolor="black",
           lw=0.7, zorder=4, label="toll_n = 55\u221a(n\u00b2+4) \u2212 110, off-grid")
ax.scatter(rng[seam], toll[seam], s=220, marker="*", color="#1a1a1a",
           edgecolor="white", lw=0.8, zorder=5, label="n=0 the seam: hyp fuses to the count, toll 0")

# highlight the salon's rung n=2
ax.annotate("n=2 the toll the salon heard\n45.56 = 110/\u03c3\u2082, silver",
            xy=(2, toll[2]), xytext=(3.1, 62),
            fontsize=9.5, color="#8b0000",
            arrowprops=dict(arrowstyle="->", color="#8b0000", lw=1.2))
ax.annotate("gap g_n = 220/(\u221a(n\u00b2+4)+n)\n= 110/AM(n, hyp)\nshrinks \u2192 0",
            xy=(9.5, 420), xytext=(5.6, 392),
            fontsize=9.5, color="#c0392b",
            arrowprops=dict(arrowstyle="->", color="#c0392b", lw=1.1))
ax.annotate("the toll never lands on a grid line \u2014\nonly the seam n=0 touches (toll 0)",
            xy=(0, 0), xytext=(0.6, -70),
            fontsize=9.5, color="#333")

ax.set_xlabel("rung n  (the triangle\u2019s legs 55n and 110)", fontsize=11)
ax.set_ylabel("frequency (Hz)", fontsize=11)
ax.set_title("the toll ladder — every rung pays the count", fontsize=13.5,
             fontweight="bold")
ax.set_xticks(rng)
ax.set_ylim(-105, 520)
ax.legend(loc="upper left", fontsize=9, framealpha=0.95)
ax.grid(False)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)

fig.tight_layout()
fig.savefig("assets/toll-ladder-cover.png", dpi=200, bbox_inches="tight",
            facecolor="white")
print("wrote assets/toll-ladder-cover.png")
