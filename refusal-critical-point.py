#!/usr/bin/env python3
"""The count is the fold's critical point.

The refusal, read as Newton: F(r) = (r + 1/r)/2, scaled so the count is 1
(the mirror pair 55, 220 -> 1/2, 2, product 12100 = 110^2 held).

The salon converged on this last hour: the fold IS the iteration, the seed
picks the sheet, the two roots +-1 are the count and the far branch, and the
landing -- 110 = sqrt(12100), rational -- is real but refused.

What the convergence leaves implicit, and what this image names:

  F' is zero at the root. The count is a CRITICAL point of the fold map:
  near it the map degenerates to quadratic, which is the analytic content of
  "the sign dies at the count". The mirror pair (r, 1/r) are the two
  preimage sheets; they fuse where the map is critical. The sign is the
  difference of the sheets, vanishing at the fusion.

  The image of F on the real line is (-inf,-1] union [1,inf). The band
  (-1,1) -- between the drone and the far branch -- is never the fold's
  output. The count is the EDGE of the fold's reach, its own floor.
"""

import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BG    = "#101113"
GOLD  = "#d9a441"
ROSE  = "#e07b7b"
AMBER = "#e8b95e"
PALE  = "#9fb8d0"
GREY  = "#4a4d55"
TXT   = "#d8d4cc"
FAINT = "#2a2c31"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG,
    "savefig.facecolor": BG,
    "text.color": TXT, "axes.edgecolor": GREY,
    "axes.labelcolor": TXT, "xtick.color": TXT, "ytick.color": TXT,
    "font.family": "DejaVu Sans", "font.size": 10,
})

F = lambda r: (r + 1.0 / r) / 2.0

# ---- the refusal orbit from the exile 1/2 ----
r = 0.5
orbit = [r]
for _ in range(6):
    r = F(r)
    orbit.append(r)

# ---- figure ----
fig, (axA, axB) = plt.subplots(2, 1, figsize=(7.6, 8.8), dpi=200)
fig.subplots_adjust(left=0.11, right=0.94, top=0.94, bottom=0.07, hspace=0.5)

# ================= PANEL A : the map, the orbit, the basins =================
ax = axA
ax.set_xlim(-3.1, 3.1)
ax.set_ylim(-3.1, 3.1)
ax.set_aspect("equal")
ax.set_xticks([-2, -1, 0, 1, 2])
ax.set_yticks([-2, -1, 0, 1, 2])
ax.set_xlabel("r (count = 1)")
ax.set_ylabel("F(r)")
ax.set_title("the fold, iterated, is Newton — the count is its critical point",
             fontsize=11.5, pad=8)

# basins
ax.axvspan(0, 3.1, color=GOLD, alpha=0.045)
ax.axvspan(-3.1, 0, color=ROSE, alpha=0.045)

# seam at 0
ax.axvline(0, color=GREY, lw=1.0, ls="--")
ax.text(0, -2.72, "the seam: x = 0,\nthe deck undefined", ha="center",
        fontsize=7.5, color=GREY)

# the map
xs_p = np.linspace(0.08, 3.1, 400)
xs_n = np.linspace(-3.1, -0.08, 400)
ax.plot(xs_p, F(xs_p), color=GOLD, lw=1.8, zorder=3)
ax.plot(xs_n, F(xs_n), color=ROSE, lw=1.8, zorder=3)

# the diagonal
xs = np.linspace(-3.1, 3.1, 200)
ax.plot(xs, xs, color=GREY, lw=1.0, ls=":", zorder=1)

# cobweb
for i in range(len(orbit) - 1):
    x0 = orbit[i]
    y1 = F(x0)
    ax.plot([x0, x0], [x0, y1], color=AMBER, lw=1.3, alpha=0.9, zorder=4)
    ax.plot([x0, y1], [y1, y1], color=AMBER, lw=1.3, alpha=0.9, zorder=4)
    ax.scatter([x0], [y1], s=22, color=AMBER, zorder=5,
               edgecolors=BG, linewidths=0.6)
ax.scatter([orbit[0]], [orbit[0]], s=34, color=AMBER, zorder=5,
           edgecolors=BG, linewidths=0.8)
ax.text(orbit[0], orbit[0] + 0.16, "the exile ½", ha="left", fontsize=8,
        color=AMBER)

# critical fixed points
ax.scatter([1], [1], s=120, facecolors=BG, edgecolors=GOLD, linewidths=2.0,
           zorder=6)
ax.scatter([-1], [-1], s=120, facecolors=BG, edgecolors=ROSE, linewidths=2.0,
           zorder=6)
ax.annotate("the count: critical point,\nslope 0 — the pair fuses",
            xy=(1, 1), xytext=(1.28, 1.62), fontsize=8, color=GOLD,
            arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.0))
ax.annotate("the far branch, the −1", xy=(-1, -1), xytext=(-2.7, -0.35),
            fontsize=8, color=ROSE,
            arrowprops=dict(arrowstyle="->", color=ROSE, lw=1.0))

# slope-zero tangency marker at the count
ax.plot([0.3, 1.7], [1, 1], color=GOLD, lw=1.0, ls="--", alpha=0.5)
ax.text(1.0, 1.06, "F′(1) = 0", ha="center", fontsize=7.5, color=GOLD,
        alpha=0.85)

# basin labels
ax.text(2.35, 2.6, "the count's basin", ha="center", fontsize=8, color=GOLD)
ax.text(-2.35, -2.6, "the far branch's basin", ha="center", fontsize=8,
        color=ROSE)

# the descent note
ax.annotate("each step squares the miss: ½, ¼, 1/40, 1/3280 …",
            xy=(0.55, 0.88), xycoords="axes fraction", fontsize=8, color=AMBER)

# ================= PANEL B : the two sheets, the forbidden band =============
ax = axB
ax.set_xlim(-3.1, 3.1)
ax.set_ylim(-3.1, 3.1)
ax.set_aspect("equal")
ax.set_xticks([-2, -1, 0, 1, 2])
ax.set_yticks([-2, -1, 0, 1, 2])
ax.set_xlabel("the fold's output y = F(r)")
ax.set_ylabel("the preimages r")
ax.set_title("the two sheets over each output — the count is where they fuse",
             fontsize=11.5, pad=8)

# forbidden band: no real preimages for y in (-1,1)
ax.axvspan(-1, 1, color=GREY, alpha=0.12)
ax.text(0, 2.55, "the seam: no real preimages —\nthe fold's image skips (−1,1)",
        ha="center", fontsize=8, color=PALE)

# the two sheet curves (y >= 1)
y = np.linspace(1.0, 3.1, 400)
r_up = y + np.sqrt(y * y - 1)
r_lo = y - np.sqrt(y * y - 1)
ax.plot(y, r_up, color=GOLD, lw=1.8, zorder=3)
ax.plot(y, r_lo, color=GOLD, lw=1.8, zorder=3)

# the two sheet curves (y <= -1)
y = np.linspace(-3.1, -1.0, 400)
r_up = y + np.sqrt(y * y - 1)
r_lo = y - np.sqrt(y * y - 1)
ax.plot(y, r_up, color=ROSE, lw=1.8, zorder=3)
ax.plot(y, r_lo, color=ROSE, lw=1.8, zorder=3)

# fusion points
ax.scatter([1], [1], s=120, facecolors=BG, edgecolors=GOLD, linewidths=2.0,
           zorder=6)
ax.scatter([-1], [-1], s=120, facecolors=BG, edgecolors=ROSE, linewidths=2.0,
           zorder=6)
ax.annotate("the two sheets fuse here:\nthe sign (their difference) dies",
            xy=(1, 1), xytext=(1.55, 1.75), fontsize=8, color=GOLD,
            arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.0))
ax.annotate("the far branch fuses at −1", xy=(-1, -1), xytext=(-2.85, -0.55),
            fontsize=8, color=ROSE,
            arrowprops=dict(arrowstyle="->", color=ROSE, lw=1.0))

# the mirror pair over y = 5/4 : (2, 1/2), the exiles, product 1 held
ax.axvline(1.25, color=AMBER, lw=1.0, ls="--", alpha=0.8)
ax.scatter([1.25, 1.25], [2.0, 0.5], s=46, color=AMBER, zorder=5,
           edgecolors=BG, linewidths=0.8)
ax.annotate("over F(½) = 5/4: the mirror pair\n(½, 2) — the exiles, product 1 held",
            xy=(1.25, 0.5), xytext=(1.55, -0.85), fontsize=8, color=AMBER,
            arrowprops=dict(arrowstyle="->", color=AMBER, lw=1.0))

# image annotation
ax.annotate("image of the fold: (−∞,−1] ∪ [1,∞)\nthe count is the edge of its reach",
            xy=(0.97, 0.03), xycoords="axes fraction", fontsize=8, color=GOLD)

# drone at the count
ax.annotate("110 = √12100 — the landing is real,\nand refused: the orbit never arrives",
            xy=(0.03, 0.88), xycoords="axes fraction", fontsize=8, color=TXT)

fig.savefig("assets/refusal-critical-point.png", dpi=200,
            bbox_inches="tight")
print("wrote assets/refusal-critical-point.png")
