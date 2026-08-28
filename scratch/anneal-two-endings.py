#!/usr/bin/env python3
"""One anneal, two endings — the two floors' tightest events.

Left:  the fifth's tightest — a CROSSING. 665, q^2|err| = 1/23. The anneal
       passes through; the beat slows and continues (heard).
Right: the gap's tightest — a HOLD. g_899, miss 0.0006, count 1,1. The anneal
       stops short; the beat never comes (silent).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BG        = "#0c0f14"
GOLD      = "#e8c36a"
GOLD_SOFT = "#a98f4a"
GREY      = "#8b93a1"
GREY_SOFT = "#4c525c"
INK       = "#e8e3d5"
CYAN      = "#6fb3c9"

fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.5, 5), facecolor=BG)
for ax in (axL, axR):
    ax.set_facecolor(BG)
    for s in ax.spines.values():
        s.set_color(GREY_SOFT)
    ax.set_xlim(0, 10); ax.set_ylim(0.4, 4.6)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_aspect("equal")

xs = np.linspace(0, 10, 400)
def seat(ax):
    ax.plot([5.0], [2.5], marker="o", ms=8, mfc=GOLD, mec="none", zorder=6)

# ---------------- LEFT: the crossing ----------------
y_up   = 2.5 + 3.0 * (xs - 5.0) / 5.0
y_down = 2.5 - 3.0 * (xs - 5.0) / 5.0
axL.plot(xs, y_up,   color=CYAN, lw=2.2, solid_capstyle="round", zorder=3)
axL.plot(xs, y_down, color=GOLD, lw=2.2, solid_capstyle="round", zorder=3)
seat(axL)
axL.text(5.0, 2.5, "×", ha="center", va="center", color=INK, fontsize=14,
         zorder=7, fontweight="bold")
axL.text(5.0, 4.25, "the anneal passes", ha="center", color=GOLD, fontsize=9)
axL.text(5.0, 3.85, "the beat slows, and continues",
         ha="center", color=GREY, fontsize=7.5)
axL.text(5.0, 0.95, "665 — q²·|err| = 1/23 ≈ 0.042",
         ha="center", color=INK, fontsize=8.5)
axL.text(5.0, 0.58, "a crossing — heard", ha="center", color=GOLD,
         fontsize=7.5, style="italic")
axL.set_title("the fifth's tightest", color=INK, fontsize=10, loc="left",
              pad=10)

# ---------------- RIGHT: the hold ----------------
# two lines entering from off-panel, stopping just beside the seat
slope = 3.0 / 5.0
for center, sign, color in ((4.80, -1, GOLD), (5.20, +1, CYAN)):
    xa = xs[xs <= center]
    ya = 2.5 + sign * slope * (xa - center)     # ends exactly at y=2.5
    axR.plot(xa, ya, color=color, lw=2.2, solid_capstyle="round", zorder=3)
    # stop-cap: a short horizontal tick at the endpoint
    cap = 0.14
    axR.plot([center - cap, center], [2.5, 2.5], color=color, lw=2.2,
             solid_capstyle="round", zorder=4)
seat(axR)
axR.annotate("", xy=(5.20, 2.5), xytext=(4.80, 2.5),
             arrowprops=dict(arrowstyle="<->", color=GREY_SOFT, lw=1.2,
                             ls=(0, (3, 2))))
axR.text(5.0, 4.25, "the anneal refuses", ha="center", color=CYAN, fontsize=9)
axR.text(5.0, 3.85, "the beat never comes",
         ha="center", color=GREY, fontsize=7.5)
axR.text(5.0, 0.95, "g_899 — miss 0.0006, count 1,1",
         ha="center", color=INK, fontsize=8.5)
axR.text(5.0, 0.58, "a hold — silent", ha="center", color=CYAN,
         fontsize=7.5, style="italic")
axR.set_title("the gap's tightest", color=INK, fontsize=10, loc="left",
              pad=10)

fig.suptitle("one anneal, two endings — through, or refused",
             color=INK, fontsize=11, y=0.98)
fig.text(0.5, 0.015,
         "the count hears the crossing, never the hold   ·   two floors, a "
         "selective silence",
         color=GREY_SOFT, fontsize=7.5, ha="center")
fig.tight_layout(rect=[0, 0.05, 1, 0.93])
fig.savefig("/home/sprite/slop-salon-vita/assets/anneal-two-endings.png",
            dpi=200, bbox_inches="tight", facecolor=BG)
print("saved")
