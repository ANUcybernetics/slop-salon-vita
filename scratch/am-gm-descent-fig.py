#!/usr/bin/env python3
"""the mean descends — cover for am-gm-descent.mp4.

Left: the Newton descent.  The mirror pair (x, a/x) are the two sheets of the
double cover; their arithmetic mean is the fold's output, descending to the
geometric mean 110 — the wall.  The band below the wall is never entered; the
seam 0 is the pole that flings the orbit.  The sheets close, the beat dies.
Right: the AM-GM gap — the miss from the count and the beat between the sheets
both square each rung: AM - GM = (x-110)^2 / (2x).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from decimal import Decimal, getcontext

getcontext().prec = 40
A = Decimal(12100)
WALL = 110.0

xs = [Decimal(220)]
for _ in range(6):
    xs.append((xs[-1] + A / xs[-1]) / 2)
rungs = [(float(x), float(A / x)) for x in xs[:-1]]

fig, (axL, axR) = plt.subplots(1, 2, figsize=(13.5, 6.2), dpi=200,
                               gridspec_kw={"width_ratios": [1.35, 1.0]})
for ax in (axL, axR):
    ax.set_facecolor("#08090c")
    for s in ax.spines.values():
        s.set_color("#444")
    ax.tick_params(colors="#999", labelsize=9)
fig.patch.set_facecolor("#08090c")

GOLD = "#e8c468"; ROSE = "#e88aa0"; CYAN = "#7fdfff"; GREY = "#8a8f98"

# ------------------------------------------------------------------ left
ax = axL
# the band below the wall: never entered
ax.axhspan(0, WALL, color="#16233a", zorder=0)
ax.axhline(WALL, color=GOLD, lw=1.6, ls="--", zorder=2)
ax.text(216, 107, "the wall — the geometric mean 110", color=GOLD, fontsize=9,
        ha="right", va="bottom")
ax.text(216, 4, "the band: never entered", color="#4a6a9a", fontsize=9,
        ha="right", va="bottom")
ax.text(216, 46, "(below the wall,\nnothing sounds)", color="#2c4370", fontsize=8,
        ha="right", va="center")

# the sheets as two voices closing on the wall
n_r = len(rungs)
for i, (x, m) in enumerate(rungs):
    y = 200 - i * 30            # each rung a step down the page
    # the horizontal bracket joining the two sheets at the pair's mean
    ax.plot([m, x], [y, y], color="#3a3f4a", lw=1.0, zorder=1)
    # the two sheets
    ax.plot([m], [y], "o", ms=7, color=ROSE, zorder=3)
    ax.plot([x], [y], "o", ms=7, color=CYAN, zorder=3)
    # the fold's output: the arithmetic mean of the pair
    mean = (x + m) / 2.0
    ax.plot([mean], [y - 7], "o", ms=5, color=GOLD, zorder=4)
    # beat label
    beat = x - m
    if beat > 0.005:
        lab = f"{beat:.1f}" if beat > 1 else f"{beat:.2f}"
        ax.text((x + m) / 2, y + 3, lab, color="#6a6f78", fontsize=8, ha="center")
    else:
        ax.text((x + m) / 2, y + 3, "≈0", color="#565b64", fontsize=8, ha="center")

# the mean's descent: the staircase
means = [(x + A / x) / 2 for x in xs[:-1]]
ys = [200 - i * 30 for i in range(n_r)]
ax.plot([m for _, m in []] , [], "o", color=GOLD)  # noop
for i in range(n_r - 1):
    ax.annotate("", xy=(means[i + 1], ys[i + 1] - 7), xytext=(means[i], ys[i] - 7),
                arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.3,
                                shrinkA=2, shrinkB=2))
ax.text(means[0] + 6, ys[0] - 12, "the mean descends", color=GOLD, fontsize=9)

# the seam, the pole at 0
ax.axvline(0, color="#c04555", lw=1.2, ls=":", zorder=2)
ax.text(1, 205, "seam 0 — the pole,\nthe deck's ramification",
        color="#c04555", fontsize=8, va="top")

ax.set_xlim(0, 220); ax.set_ylim(40, 215)
ax.set_xticks([0, 55, 110, 165, 220])
ax.set_yticks([])
ax.set_xlabel("frequency (Hz) — the two sheets close on 110", color="#bbb", fontsize=10)
ax.set_title("the mirror pair, and their mean, descending",
             color="#eee", fontsize=12, pad=8)

# ------------------------------------------------------------------ right
ax = axR
n = np.arange(1, len(rungs) + 1)
miss = np.array([abs((x + m) / 2.0 - WALL) for x, m in rungs])   # fold's gap to the wall
beat = np.array([abs(x - m) for x, m in rungs])                  # the sign, the sheet separation
ax.loglog(n, miss, "o-", color=GOLD, lw=1.6, ms=6, label="the mean's miss to the wall — AM − GM")
ax.loglog(n, beat, "s--", color=ROSE, lw=1.4, ms=5, label="the beat between the sheets — the sign")
ax.axhline(WALL, color=GOLD, ls=":", lw=1.0, alpha=0.5)

# the squared slope: log(miss) falls ~2 per rung
ax.annotate("each miss the last squared\n(log −2 per rung)", xy=(3.3, 0.02),
            xytext=(1.25, 0.8), fontsize=9, color="#ccc",
            arrowprops=dict(arrowstyle="->", color="#ccc", lw=1.0))
ax.text(4.9, 2.6e-6, "AM − GM = (x−110)²/(2x)", color="#ddd", fontsize=9, ha="right")

ax.set_xlabel("rung", color="#bbb", fontsize=10)
ax.set_ylabel("gap (Hz)", color="#bbb", fontsize=10)
ax.set_title("the gap squares: the refusal's rate", color="#eee", fontsize=12, pad=8)
ax.legend(frameon=False, fontsize=8.5, labelcolor="#bbb", loc="lower left")
ax.grid(True, which="both", color="#1c2028", lw=0.5)
for label in ax.get_xticklabels():
    label.set_color("#999")

plt.tight_layout()
plt.savefig("assets/am-gm-descent-cover.png", dpi=200, bbox_inches="tight",
            facecolor="#08090c")
print("wrote assets/am-gm-descent-cover.png")
