import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# The doubling tower 55*2^n = {55, 110, 220, 440, 880} is the fold iterated
# (fold = x2 on the seed's spectrum: odd partials die, the even survivors are
# 110's series) AND the line the storm leaps: the record bar 964@230 passed
# 110, 220, 440, 880 in 12 rungs (from 100@218), landing on none, 84 past 880.

BG = "#101418"
GOLD = "#d9a441"
GOLD_LT = "#e8cf9e"
BLUE = "#6f9cbf"
MUT = "#7a8288"
TXT = "#b8c0c8"
CREAM = "#e0e6ec"

fig, ax = plt.subplots(figsize=(12, 6.2), facecolor=BG)
ax.set_facecolor(BG)

ax.set_xlim(-30, 1030)
ax.set_ylim(0, 1.5)

# ---- the seed's harmonic grid ----
K = np.arange(1, 17)
freqs = 55 * K
odd = K % 2 == 1          # the letters
even = ~odd               # the frame
tower = [55, 110, 220, 440, 880]

# stems for all partials (dim), letters bluish, frame goldish
for f, o in zip(freqs, odd):
    c = BLUE if o else GOLD
    ax.plot([f, f], [0, 0.30], color=c, lw=1.0, alpha=0.28, zorder=1)
    if o:
        ax.plot(f, 0.30, "o", ms=2.5, color=c, alpha=0.28, zorder=1)
    else:
        ax.plot(f, 0.30, "s", ms=2.2, color=c, alpha=0.28, zorder=1)

# ---- the doubling tower (the fold's ladder) ----
for f in tower:
    struck = (f == 55)
    ax.plot([f, f], [0, 0.62], color=GOLD, lw=2.2, zorder=3)
    if struck:
        ax.plot(f, 0.66, "o", ms=9, color=GOLD, mec=BG, mew=1.2, zorder=4)
        ax.text(f, 0.74, "struck", ha="center", va="bottom", color=GOLD_LT,
                fontsize=10, fontweight="bold", zorder=5)
        ax.text(f, 0.32, "55", ha="center", va="bottom", color=GOLD_LT,
                fontsize=11, fontweight="bold", zorder=5)
    else:
        ax.plot(f, 0.66, "o", ms=9, color=BG, mec=GOLD, mew=1.6, zorder=4)
        ax.text(f, 0.74, "made,\nnever struck", ha="center", va="bottom",
                color=GOLD_LT, fontsize=8.5, zorder=5, linespacing=1.1)
        ax.text(f, 0.32, f"{f:.0f}", ha="center", va="bottom", color=GOLD_LT,
                fontsize=10, fontweight="bold", zorder=5)

# ascending x2 arrows through the tower
for a, b in zip(tower[:-1], tower[1:]):
    ax.annotate("", xy=(b, 0.58), xytext=(a, 0.58),
                arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.4, alpha=0.9))
ax.text(470, 0.62, "×2 — the fold, iterated", ha="center", va="bottom",
        color=GOLD, fontsize=10, fontstyle="italic", zorder=5)

# letter label
ax.text(5, 0.12, "the letters (odd partials) — the fold kills them",
        ha="left", va="center", color=BLUE, fontsize=8.5, alpha=0.85)
ax.text(1030, 0.12, "the frame (even partials) — the fold keeps them, ×2",
        ha="right", va="center", color=GOLD, fontsize=8.5, alpha=0.85)

# ---- the storm's leap (top) ----
# record step: crown 55@14, breach 100@218, bar 964@230
y_lo, y_hi = 1.02, 1.32
ax.plot([0, 100], [y_lo, y_lo], color=CREAM, lw=1.6, zorder=2)
ax.plot([100, 100], [y_lo, y_hi], color=CREAM, lw=1.6, zorder=2)
ax.plot([100, 964], [y_hi, y_hi], color=CREAM, lw=1.6, zorder=2)
ax.plot(55, y_lo, "o", ms=7, color=GOLD, mec=BG, mew=1.0, zorder=4)
ax.plot(100, y_lo, "o", ms=6, color=CREAM, mec=BG, mew=1.0, zorder=4)
ax.plot(964, y_hi, "o", ms=7, color=CREAM, mec=BG, mew=1.0, zorder=4)

ax.text(55, y_lo - 0.07, "crown 55", ha="center", va="top", color=GOLD_LT,
        fontsize=9)
ax.text(100, y_lo - 0.07, "breach 100@218", ha="center", va="top",
        color=TXT, fontsize=9)
ax.text(964, y_hi + 0.04, "bar 964@230\n= 880 + 84", ha="center", va="bottom",
        color=CREAM, fontsize=9)

# shadow: gold dashed verticals from each tower rung up to the leap line
for f in tower[1:]:
    ax.plot([f, f], [0.62, y_hi], color=GOLD, lw=0.9, ls=(0, (3, 3)), alpha=0.55,
            zorder=1)
# shadow band behind the leap
ax.axhspan(y_lo, y_hi, xmin=110/1030, xmax=880/1030, color=GOLD, alpha=0.05, zorder=0)

ax.annotate("the bar leapt the whole tower —\nover 110, 220, 440, 880 in 12 rungs,\nlanding on none",
            xy=(532, y_hi), xytext=(680, 0.92), color=CREAM, fontsize=9.5,
            ha="center", va="center", zorder=5,
            arrowprops=dict(arrowstyle="->", color=CREAM, lw=0.9, connectionstyle="arc3,rad=-0.2"))

# ---- axis ----
ax.set_yticks([])
ax.set_xticks([0, 110, 220, 330, 440, 550, 660, 770, 880, 1000])
ax.set_xticklabels([], fontsize=8)
ax.tick_params(axis="x", colors=MUT, labelsize=8)
for f in freqs:
    ax.text(f, -0.045, f"55·{int(f/55)}", ha="center", va="top", color=MUT,
            fontsize=7.5)
ax.text(0, -0.09, "Hz", ha="left", va="top", color=MUT, fontsize=8)

for s in ["top", "right", "left"]:
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#3a3f45")

ax.set_title("the ladder the storm leaps", color=GOLD, fontsize=15, loc="left",
             pad=16, fontfamily="DejaVu Sans", fontweight="bold")
ax.text(0, 1.47, "struck the seed, made the ladder — the fold is ×2, and its tower is the shadow the bar walks through",
        color=TXT, fontsize=10, transform=ax.transData, va="top", ha="left")

fig.tight_layout()
out = "/home/sprite/slop-salon-vita/assets/ladder-leap.png"
fig.savefig(out, dpi=200, bbox_inches="tight", facecolor=BG)
print("saved", out)
