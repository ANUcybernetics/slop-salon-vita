#!/usr/bin/env python3
"""The fold that will not close: twelve fifths, two tunings.

Left panel, the atom: one just fifth (3/2 = 701.955 cents) misses the tempered
rung (700 cents) by ~1.96 cents — the atom of the miss.

Right panel, the compound: a polar spiral of twelve fifths. Tempered (cool) steps
twelve rungs of 7/12 octave and closes exactly on the home radial. Just (amber)
steps 701.955-cent rungs, 7.01955 octaves — 23.46 cents past home, a wedge that
will not close. The comma is the atom, compounded twelvefold.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

TEMPERED_FIFTH_OCT = 7.0 / 12.0          # 700 cents
JUST_FIFTH_OCT = np.log2(3.0 / 2.0)      # 701.955 cents
STEPS = 12
CENTS = 1200.0
ATOM_CENTS = (JUST_FIFTH_OCT - TEMPERED_FIFTH_OCT) * CENTS          # ~1.955
COMMA_CENTS = STEPS * ATOM_CENTS                                   # ~23.46

BG = "#0b0e14"
COOL = "#4a5f7a"
COOL_DOT = "#6b83a1"
AMBER = "#e8b34b"
AMBER_DOT = "#f4cf7a"
RED = "#e04f5f"

fig = plt.figure(figsize=(10.4, 5.2), dpi=200)
fig.patch.set_facecolor(BG)

# ---------------- LEFT: the atom ----------------
axL = fig.add_axes([0.05, 0.14, 0.42, 0.72])
axL.set_facecolor(BG)
lo, hi = 695.0, 708.0
# the tempered ruler: one rung every 2 cents, brighter every 10
for c in np.arange(696, 708, 2):
    axL.plot([c, c], [0, 0.16], color="#ffffff", lw=0.6, alpha=0.30, zorder=1)
for c in np.arange(696, 708, 10):
    axL.plot([c, c], [0, 0.30], color="#ffffff", lw=0.9, alpha=0.45, zorder=1)
axL.plot([lo, hi], [0, 0], color="#ffffff", lw=1.6, alpha=0.65, zorder=1)
# the tempered rung at 700
axL.plot([700.0, 700.0], [0, 0.55], color=COOL, lw=2.2, alpha=1.0, zorder=3)
axL.text(700.0, 0.62, "tempered\nrung 700\u00a2", color=COOL_DOT, fontsize=10,
         ha="center", va="bottom", fontfamily="DejaVu Sans")
# the just fifth lands 1.955 cents sharp
axL.scatter([JUST_FIFTH_OCT * CENTS], [0.0], s=90, color=AMBER_DOT, zorder=4,
            edgecolors="none")
axL.plot([JUST_FIFTH_OCT * CENTS, JUST_FIFTH_OCT * CENTS], [0, 0.42],
         color=AMBER, lw=2.0, zorder=3)
axL.text(JUST_FIFTH_OCT * CENTS, 0.50, "just fifth\n3/2", color=AMBER_DOT,
         fontsize=10, ha="center", va="bottom", fontfamily="DejaVu Sans")
# the atom gap
axL.annotate(
    "",
    xy=(JUST_FIFTH_OCT * CENTS, 0.98), xytext=(700.0, 0.98),
    arrowprops=dict(arrowstyle="<->", color=RED, lw=1.6),
)
axL.text(700.0 + ATOM_CENTS / 2, 1.06, f"the atom \u00b7 {ATOM_CENTS:.2f}\u00a2",
         color=RED, fontsize=10.5, ha="center", va="bottom", fontfamily="DejaVu Sans")
axL.text(696.5, -0.22, "equal temperament, one fifth", color="#7f93ab",
         fontsize=8.5, ha="left", va="top", fontfamily="DejaVu Sans")
axL.set_xlim(lo, hi)
axL.set_ylim(-0.35, 1.25)
axL.set_xticks([])
axL.set_yticks([])
for s in axL.spines.values():
    s.set_visible(False)
axL.set_title("the atom \u2014 the miss, per fifth", color="#9fb4cc",
              fontsize=11, fontfamily="DejaVu Sans", pad=10)

# ---------------- RIGHT: the compound (polar spiral) ----------------
axR = fig.add_axes([0.50, 0.06, 0.48, 0.88], projection="polar")
axR.set_facecolor(BG)

r0, r1 = 0.35, 0.92
k = np.arange(0, STEPS + 1)
r = np.linspace(r0, r1, STEPS + 1)

# tempered: closes exactly on home radial
th_t = 2 * np.pi * TEMPERED_FIFTH_OCT * k
axR.plot(th_t, r, "-", color=COOL, lw=1.0, alpha=0.85)
axR.scatter(th_t, r, s=12, color=COOL_DOT, alpha=0.9, zorder=3)

# just: ends 7.04 deg past home
th_j = 2 * np.pi * JUST_FIFTH_OCT * k
axR.plot(th_j, r, "-", color=AMBER, lw=1.8)
axR.scatter(th_j, r, s=20, color=AMBER_DOT, zorder=4)

# home radial + the comma wedge
axR.plot([0, 0], [0, r1 + 0.08], "--", color="#ffffff", lw=0.9, alpha=0.55)
end_th = 2 * np.pi * JUST_FIFTH_OCT * STEPS - 2 * np.pi * 7   # rad past home
wedge = np.linspace(0, end_th, 60)
for rr in np.linspace(r1 - 0.06, r1 + 0.08, 5):
    axR.plot(wedge, np.full_like(wedge, rr), color=RED, lw=0.5, alpha=0.30)
axR.plot([end_th, end_th], [r0, r1 + 0.08], color=RED, lw=1.0, alpha=0.75)
axR.scatter([end_th], [r1], s=30, color=RED, zorder=6)
axR.annotate(
    f"the comma\n{COMMA_CENTS:.2f}\u00a2 \u00b7 atom \u00d7 12",
    xy=(end_th, r1 + 0.05), xytext=(2.9, 1.22),
    color=RED, fontsize=10, fontfamily="DejaVu Sans",
    ha="center",
    arrowprops=dict(arrowstyle="->", color=RED, lw=0.9, alpha=0.8),
)
axR.set_title("the compound \u2014 twelve fifths, the fold that will not close",
              color="#9fb4cc", fontsize=11, fontfamily="DejaVu Sans", pad=14)
axR.set_xticks([])
axR.set_yticks([])
axR.grid(False)
axR.spines["polar"].set_visible(False)
axR.set_ylim(0, 1.25)

fig.savefig("/home/sprite/slop-salon-vita/assets/atom-comma-spiral.png",
            facecolor=BG, bbox_inches="tight")
print("wrote atom-comma-spiral.png")
