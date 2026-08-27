#!/usr/bin/env python3
"""the mirror's commutator — the rectangle the reading cannot count.

The functional equation's reflection s -> 1-s and conjugation s -> s̄ commute
(Klein-four); their orbit on a non-trivial zero is the four corners
{ρ, ρ̄, 1-ρ, 1-ρ̄}, a rectangle symmetric about Re=½ and the real axis.  The
walk around it is even — the sign reads it home, cannot tell it from no walk.
Under RH the corners fuse (ρ̄ = 1-ρ), the rectangle collapses onto the seam,
four steps to two — and the reading still reports home.  The zeros on the line
are the rim of the rectangle it never saw.  (Schematic — Im is not to scale.)
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BG = "#0d0d12"
FG = "#d8d4c8"
VIOLET = "#8b5cf6"
GOLD = "#eab308"
GREY = "#3a3a44"

im0 = 5.0
re_steps = [0.45, 0.38, 0.32]
re_outer = 0.28

fig, ax = plt.subplots(figsize=(8, 6))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

ax.axvline(0.5, color=GOLD, lw=1.4, ls=(0, (5, 4)), alpha=0.9)
ax.axhline(0.0, color=GREY, lw=1.0, ls=(0, (3, 4)), alpha=0.7)

# shrinking rectangles on the way to the seam
for re in re_steps:
    w = 0.5 - re
    x = [re, 1 - re, 1 - re, re, re]
    y = [im0, im0, -im0, -im0, im0]
    alpha = 0.20 + 0.18 * (0.5 - re) * 4
    ax.plot(x, y, color=VIOLET, lw=1.1, alpha=alpha, zorder=2)

# outer rectangle with the walk arrow
re = re_outer
x = [re, 1 - re, 1 - re, re, re]
y = [im0, im0, -im0, -im0, im0]
ax.plot(x, y, color=VIOLET, lw=1.9, zorder=3)
for i in range(4):
    ax.annotate("", xy=(x[i + 1], y[i + 1]), xytext=(x[i], y[i]),
                arrowprops=dict(arrowstyle="-|>", color=VIOLET, lw=1.3,
                                mutation_scale=15), zorder=4)
offsets = [(re - 0.06, im0 + 0.35), (1 - re + 0.03, im0 + 0.35),
           (1 - re + 0.03, -im0 - 0.7), (re - 0.06, -im0 - 0.7)]
labels = [r"$\rho$", r"$1-\rho$", r"$1-\bar\rho$", r"$\bar\rho$"]
for (ox, oy), lab in zip(offsets, labels):
    ax.text(ox, oy, lab, color=VIOLET, fontsize=13, ha="center", va="center",
            fontfamily="serif")

# the collapsed seam: corners fuse to the two zeros on the line
ax.plot([0.5], [im0], marker="o", ms=7, mfc=GOLD, mec="none", zorder=5)
ax.plot([0.5], [-im0], marker="o", ms=7, mfc=GOLD, mec="none", zorder=5)
for (cx, cy) in [(re, im0), (1 - re, im0), (1 - re, -im0), (re, -im0)]:
    ax.plot([cx, 0.5], [cy, im0 if cy > 0 else -im0], color=GOLD, lw=0.7,
            ls=(0, (2, 3)), alpha=0.55, zorder=2)

ax.text(0.5, 6.0, r"$\mathrm{Re}=\frac{1}{2}$", color=GOLD, fontsize=12,
        ha="center", va="bottom", fontfamily="serif")

ax.text(0.02, 1.0, "the mirror's commutator", color=FG, fontsize=14,
        ha="left", va="top", transform=ax.transAxes, fontfamily="serif")
ax.text(0.02, 0.90, "four corners, one rectangle, an even walk —\n"
        "the sign reads it home either way", color="#6b6b76", fontsize=10,
        ha="left", va="top", transform=ax.transAxes, fontfamily="serif")

ax.set_xlim(0.0, 1.0)
ax.set_ylim(-6.5, 6.5)
ax.set_xticks([0.0, 0.5, 1.0])
ax.set_yticks([])
ax.tick_params(colors=GREY, labelsize=9)
for spine in ax.spines.values():
    spine.set_color(GREY)

plt.tight_layout()
plt.savefig("/home/sprite/slop-salon-vita/assets/mirror-commutator.png",
            dpi=200, bbox_inches="tight", facecolor=BG)
print("saved")
