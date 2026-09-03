#!/usr/bin/env python3
import math

import matplotlib.pyplot as plt
import numpy as np


C = 110.0
G = 131.795425820915
tritone = C * math.sqrt(2)

bg = "#090b10"
fg = "#d7d2c4"
muted = "#6f7788"
gold = "#f0b44c"
cyan = "#51d5dc"
rose = "#f06c7a"
green = "#86d77d"
violet = "#9f8cff"

fig = plt.figure(figsize=(18, 10), facecolor=bg, dpi=160)
gs = fig.add_gridspec(1, 2, width_ratios=[1.05, 1], wspace=0.12)

ax = fig.add_subplot(gs[0, 0], facecolor=bg)
ax2 = fig.add_subplot(gs[0, 1], facecolor=bg)

fig.text(
    0.06,
    0.94,
    "basis, not pitch",
    color=fg,
    fontsize=30,
    fontweight="bold",
    ha="left",
)
fig.text(
    0.06,
    0.905,
    "G is the quotient's value; 110+i110 is the lift's coordinate.",
    color=muted,
    fontsize=14,
    ha="left",
)

# Left: the same point under three coordinate readings.
ax.set_xlim(92, 170)
ax.set_ylim(-1.2, 1.2)
ax.axis("off")
ax.hlines(0, 96, 166, color="#28303a", lw=2)
for x, label, color, y in [
    (C, "110\ncount", gold, -0.38),
    (G, "G\nquotient", green, 0.35),
    (tritone, "110sqrt(2)\nmodulus", rose, -0.38),
]:
    ax.vlines(x, -0.14, 0.14, color=color, lw=3)
    ax.scatter([x], [0], s=110, color=color, zorder=3)
    ax.text(x, y, label, color=color, fontsize=13, ha="center", va="center")

eps = tritone - G
ax.annotate(
    "",
    xy=(G, 0.58),
    xytext=(tritone, 0.58),
    arrowprops=dict(arrowstyle="<->", color=rose, lw=1.8),
)
ax.text((G + tritone) / 2, 0.7, "miss from modulus", color=rose, fontsize=12, ha="center")

ax.annotate(
    "",
    xy=(G, -0.62),
    xytext=(C, -0.62),
    arrowprops=dict(arrowstyle="<->", color=green, lw=1.8),
)
ax.text((G + C) / 2, -0.82, "quotient stated as value", color=green, fontsize=12, ha="center")

ax.text(
    96,
    1.02,
    "one axis can only report values",
    color=fg,
    fontsize=16,
    fontweight="bold",
    ha="left",
)
ax.text(
    96,
    0.86,
    f"G = {G:.12f}\n110sqrt(2) = {tritone:.12f}\nmiss = {eps:.12f}",
    color=muted,
    fontsize=12,
    ha="left",
    va="top",
)

# Right: lifted coordinate plane.
ax2.set_aspect("equal")
ax2.set_xlim(-22, 178)
ax2.set_ylim(-22, 178)
ax2.axis("off")
ax2.arrow(0, 0, 160, 0, length_includes_head=True, head_width=3.5, head_length=5, color="#28303a", lw=1.7)
ax2.arrow(0, 0, 0, 160, length_includes_head=True, head_width=3.5, head_length=5, color="#28303a", lw=1.7)
ax2.text(164, 0, "real", color=muted, fontsize=12, ha="left", va="center")
ax2.text(0, 164, "phase", color=muted, fontsize=12, ha="center", va="bottom")

ax2.arrow(0, 0, C, 0, length_includes_head=True, head_width=4, head_length=6, color=gold, lw=4)
ax2.arrow(0, 0, 0, C, length_includes_head=True, head_width=4, head_length=6, color=rose, lw=4)
ax2.arrow(0, 0, C, C, length_includes_head=True, head_width=5, head_length=7, color=cyan, lw=4)
ax2.plot([C, C], [0, C], color="#293341", lw=1.2, ls="--")
ax2.plot([0, C], [C, C], color="#293341", lw=1.2, ls="--")
ax2.scatter([C], [C], s=150, color=cyan, zorder=5)

theta = np.linspace(0, math.pi / 2, 80)
ax2.plot(34 * np.cos(theta), 34 * np.sin(theta), color=green, lw=2.4)
ax2.text(25, 31, "quarter-turn", color=green, fontsize=12, ha="left")
ax2.text(C / 2, -10, "count", color=gold, fontsize=13, ha="center")
ax2.text(-10, C / 2, "sign", color=rose, fontsize=13, rotation=90, ha="center")
ax2.text(C + 8, C + 4, "110(1+i)", color=cyan, fontsize=15, ha="left", va="center")
ax2.text(
    0,
    152,
    "the second axis is not a higher note",
    color=fg,
    fontsize=16,
    fontweight="bold",
    ha="left",
)
ax2.text(
    0,
    139,
    "it is what the quotient forgot to say",
    color=muted,
    fontsize=12,
    ha="left",
)

fig.savefig("assets/basis-not-pitch.png", facecolor=bg, bbox_inches="tight", pad_inches=0.25)
