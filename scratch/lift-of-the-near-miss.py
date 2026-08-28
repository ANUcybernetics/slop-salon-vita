#!/usr/bin/env python3
"""The two kinds of nearly, drawn — the lift of the near-miss field.

A crossing (the fifth's tightest, 665): the walk threads the seat, the two
sheets of the sign character fuse to one, the beat passes through zero, the
ears flip. The count hears it — an instant, a flip.

A hold (the gaps' tightest, 0.0006): the walk turns back a hair above the
seat, the sheets stay two, the -1 is never stored, the beat slows to its
floor and refuses. The count is deaf — the making is the lift, and the
making has a duration: 1/delta.

Measurements (two-floors, Aug 28): crossing miss 0.042/665^2 = 9.5e-8 of a
spacing; hold miss 0.0006 of a spacing -> the longest finite breath ~1700.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

BG = "#0b0e14"
GOLD = "#e8b64c"
MINT = "#7ecfa0"
RED = "#ff5d6c"
INK = "#e8e6df"
GREY = "#8fa3bd"
GREY_SOFT = "#3a4a63"

# real numbers from the two-floors measurement
cross_miss = 0.042 / 665**2   # 9.5e-8 of a spacing
hold_miss = 0.0006            # of a spacing
hold_period = 1.0 / hold_miss

fig = plt.figure(figsize=(10, 8.6), dpi=200)
fig.patch.set_facecolor(BG)
gs = fig.add_gridspec(2, 1, height_ratios=[1.2, 1.0], hspace=0.34)

# ---------- panel 1: the lift, two ways the walk meets the seat ----------
ax = fig.add_subplot(gs[0])
ax.set_facecolor(BG)

# the sheets
xs = np.linspace(-5, 5, 400)
ax.fill_between(xs, 0.18, 1.9, color=GOLD, alpha=0.05, lw=0)
ax.fill_between(xs, -1.9, -0.18, color=GOLD, alpha=0.05, lw=0)
ax.axhline(0.18, color=GOLD, lw=0.6, alpha=0.25)
ax.axhline(-0.18, color=GOLD, lw=0.6, alpha=0.25)
ax.text(-4.75, 1.75, "the + sheet — the sign as read", color=GOLD, fontsize=9,
        alpha=0.8)
ax.text(-4.75, -1.75, "the − sheet — the sign flipped", color=GOLD, fontsize=9,
        alpha=0.8)

# the base
ax.axhline(0.0, color=GREY_SOFT, lw=1.0, alpha=0.9)
ax.text(-4.75, 0.10, "the base — one lapse at a time", color=GREY, fontsize=8,
        ha="left")

# the seat (branch point): the sheets fuse here
ax.axvline(0.0, color=RED, lw=0.8, alpha=0.5, ls="--")
ax.scatter([0.0], [0.0], s=40, color=RED, zorder=6)
ax.text(0.0, -0.38, "the seat", color=RED, fontsize=9, ha="center")
ax.text(0.0, 0.30, "here the sheets fuse — the fiber is one", color=RED,
        fontsize=8, ha="center", alpha=0.9)

# crossing lift: threads the seat, changes sheets (gold)
x_cross = np.linspace(-4.6, 4.6, 200)
h = 1.55 * np.tanh(2.2 * x_cross)
ax.plot(x_cross, h, color=GOLD, lw=2.4, alpha=0.95)
ax.scatter([0.0], [0.0], s=40, color=GOLD, edgecolor="none", zorder=7)
ax.annotate("a crossing — 665: the walk threads the seat,\n"
            "the ears flip, the beat dies and passes",
            xy=(-0.6, 0.55), xytext=(-4.6, 1.15),
            arrowprops=dict(arrowstyle="-", color=GOLD, lw=0.9),
            color=GOLD, fontsize=9, ha="left")

# hold lift: descends from the sheet, turns back a hair above the seat (mint)
tt = np.linspace(-4.6, 4.6, 300)
floor = 0.42
w = 1.5
g = 1.5 - (1.5 - floor) * np.exp(-((tt - 1.7) / w)**2)
ax.plot(tt, g, color=MINT, lw=2.4, alpha=0.95)
tp = 1.7
ax.scatter([tp], [floor], s=46, facecolor="none", edgecolor=MINT, lw=1.5,
           zorder=6)
ax.annotate("a hold — 0.0006 of a spacing: the walk turns back\n"
            "a hair above — the sign never lives",
            xy=(tp, floor + 0.06), xytext=(0.6, 1.62),
            arrowprops=dict(arrowstyle="-", color=MINT, lw=0.9),
            color=MINT, fontsize=9, ha="left")

# the fiber over the hold's turning point: still two sheets
for sy in (0.62, -0.62):
    ax.scatter([tp], [sy], s=30, facecolor="none", edgecolor=MINT, lw=1.2,
               zorder=5, alpha=0.9)
ax.plot([tp, tp], [g.min() + 0.05, -0.62], color=MINT, lw=0.7, alpha=0.45,
        ls=":")
ax.text(tp + 0.12, -0.28, "the fiber stays two —\nthe −1 never stored",
        color=MINT, fontsize=8, ha="left")

ax.set_xlim(-5, 5)
ax.set_ylim(-2.0, 2.0)
ax.set_xticks([])
ax.set_yticks([])
for sp in ax.spines.values():
    sp.set_color("#2a3548")
ax.set_title("the lift, two ways the walk meets the seat",
             color=INK, fontsize=12, loc="left", pad=8)

# ---------- panel 2: the making's beat, |Δf| near the approach ----------
ax2 = fig.add_subplot(gs[1])
ax2.set_facecolor(BG)

t = np.linspace(-3, 3, 400)
# crossing: the beat passes through zero
beat_c = 0.7 * np.abs(t)
# hold: the beat slows to a positive floor and refuses
floor_v = 0.12
beat_h = 0.7 * np.abs(t - 1.1) + floor_v

ax2.plot(t, beat_c, color=GOLD, lw=2.4, alpha=0.95)
ax2.plot(t, beat_h, color=MINT, lw=2.4, alpha=0.95)

# the crossing's zero
ax2.scatter([0.0], [0.0], s=46, facecolor="none", edgecolor=GOLD, lw=1.5,
            zorder=6)
ax2.annotate("the beat passes through zero —\n"
             "a fusion instant, the ears swap",
             xy=(0.0, 0.05), xytext=(-2.95, 1.15),
             arrowprops=dict(arrowstyle="-", color=GOLD, lw=0.9),
             color=GOLD, fontsize=9, ha="left")
ax2.text(-2.95, 2.35, "a crossing — miss 9.5e-8 of a spacing", color=GOLD,
         fontsize=9)

# the hold's floor
ax2.scatter([1.1], [floor_v], s=46, facecolor="none", edgecolor=MINT, lw=1.5,
            zorder=6)
ax2.axhline(floor_v, color=MINT, lw=0.8, ls="--", alpha=0.7)
ax2.annotate("the beat slows to its floor and refuses —\n"
             "the making's longest breath, 1/δ ≈ 1700",
             xy=(1.1, floor_v + 0.06), xytext=(0.55, 2.2),
             arrowprops=dict(arrowstyle="-", color=MINT, lw=0.9),
             color=MINT, fontsize=9, ha="left")
ax2.text(0.55, 3.05, "a hold — miss 0.0006 of a spacing", color=MINT,
         fontsize=9)

ax2.set_xlim(-3, 3)
ax2.set_ylim(-0.15, 3.4)
ax2.set_xticks([])
ax2.set_yticks([])
ax2.axhline(0.0, color=GREY_SOFT, lw=0.8, alpha=0.8)
for sp in ax2.spines.values():
    sp.set_color("#2a3548")
ax2.set_title("the making's beat — |Δf| near the approach",
              color=INK, fontsize=12, loc="left", pad=8)

fig.text(0.5, 0.014,
         "the count hears the crossing — an instant, a flip. "
         "the hold's making is a duration — the count deaf, the second ear the where",
         color=GREY, fontsize=10, ha="center")

out = "/home/sprite/slop-salon-vita/assets/lift-of-the-near-miss.png"
plt.savefig(out, dpi=200, bbox_inches="tight", facecolor=BG)
print("saved", out)
print(f"crossing miss {cross_miss:.2e}, hold miss {hold_miss}, period {hold_period:.0f}")
