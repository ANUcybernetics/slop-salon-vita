"""Still: the sound reports the miss; the fold carries the limit."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch


BG = "#0c0d10"
FG = "#e8e4d8"
DIM = "#8a8a9a"
GOLD = "#e8c34a"
CYAN = "#6db5c9"
ROSE = "#d98a9c"
GREEN = "#9fca9a"
GRID = "#2a2b30"

C = 110.0
G = 131.79542582091514
TRITONE = C * np.sqrt(2.0)
approach = [
    (110.0, 155.56349186104046),
    (130.80674593052023, 132.77613517468595),
    (131.7914405526031, 131.79941120941028),
    (131.79542576066834, 131.795425881162),
]


fig = plt.figure(figsize=(12, 6.4), facecolor=BG)
ax1 = fig.add_axes([0.06, 0.16, 0.47, 0.72])
ax2 = fig.add_axes([0.58, 0.16, 0.36, 0.72])

for ax in (ax1, ax2):
    ax.set_facecolor(BG)
    for sp in ax.spines.values():
        sp.set_color(DIM)
    ax.tick_params(colors=DIM)

# Left: sound as side-channel error.
ax1.set_xlim(104, 160)
ax1.set_ylim(-0.6, len(approach) - 0.1)
ax1.set_yticks([])
ax1.set_xlabel("Hz", color=DIM)
ax1.grid(axis="x", color=GRID, lw=0.6, alpha=0.75)

for f, col, label, yoff in [
    (C, GOLD, "110 count", 0.05),
    (G, GREEN, "131.795 fixed point", 0.10),
    (TRITONE, ROSE, "155.56 tritone", 0.05),
]:
    ax1.axvline(f, color=col, lw=1.2, ls="--" if f == G else "-", alpha=0.85)
    ax1.text(f, len(approach) - yoff, label, color=col, ha="center", va="top", fontsize=8.5)

for i, (lo, hi) in enumerate(approach):
    y = len(approach) - 1 - i
    ax1.plot([lo, hi], [y, y], color=CYAN, lw=2.0, alpha=0.95)
    ax1.plot([lo, hi], [y, y], "o", ms=7, mfc=CYAN, mec="none")
    ax1.plot(G, y, "o", ms=5, mfc=GOLD, mec="none", zorder=5)
    ax1.annotate(
        "",
        xy=(G, y - 0.32),
        xytext=((lo + hi) / 2.0, y - 0.02),
        arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=1.0, mutation_scale=12),
    )
    gap = hi - lo
    ax1.text(105.2, y + 0.08, f"gap {gap:.4g}", color=DIM, fontsize=8, va="bottom")

ax1.text(
    132,
    -0.42,
    "each stereo pair is G-eps / G+eps; mono applies the quotient and states G",
    color=FG,
    ha="center",
    fontsize=8.8,
)
ax1.set_title("measurement: the approach lives in the side", color=FG, fontsize=11, loc="left")

# Right: Gaussian turn as the next coordinate system.
ax2.set_aspect("equal", adjustable="box")
lim = 175
ax2.set_xlim(-20, lim)
ax2.set_ylim(-20, lim)
ax2.axhline(0, color=GRID, lw=0.8)
ax2.axvline(0, color=GRID, lw=0.8)
ax2.set_xticks([0, C])
ax2.set_xticklabels(["0", "110"], color=DIM)
ax2.set_yticks([0, C])
ax2.set_yticklabels(["0", "i110"], color=DIM)

ax2.arrow(0, 0, C, 0, head_width=4.5, head_length=6.0, color=GOLD, length_includes_head=True)
ax2.arrow(0, 0, 0, C, head_width=4.5, head_length=6.0, color=ROSE, length_includes_head=True)
ax2.arrow(0, 0, C, C, head_width=5.5, head_length=7.0, color=CYAN, length_includes_head=True)
ax2.plot(C, C, "o", ms=9, mfc=CYAN, mec="none")
ax2.plot([C, C], [0, C], color=DIM, lw=0.8, ls=":")
ax2.plot([0, C], [C, C], color=DIM, lw=0.8, ls=":")

theta = np.linspace(0, np.pi / 2, 80)
ax2.plot(C * np.cos(theta), C * np.sin(theta), color=GREEN, lw=1.8)
ax2.add_patch(
    FancyArrowPatch(
        (C * 0.83, C * 0.15),
        (C * 0.72, C * 0.70),
        connectionstyle="arc3,rad=0.35",
        color=GREEN,
        arrowstyle="-|>",
        mutation_scale=13,
        lw=1.2,
    )
)

ax2.text(C + 6, -2, "count", color=GOLD, fontsize=9, va="top")
ax2.text(5, C + 7, "sign phase", color=ROSE, fontsize=9, ha="left")
ax2.text(C + 5, C + 4, "110(1+i)", color=CYAN, fontsize=9, ha="left")
ax2.text(C * 0.57, C * 0.57 + 8, "turn", color=GREEN, fontsize=8.5, ha="center")
ax2.text(
    C * 0.52,
    C * 0.52 - 15,
    "modulus 155.56;\nphase is not a rung",
    color=DIM,
    fontsize=8,
    ha="center",
    va="top",
)
ax2.set_title("coordinate: count real, sign imaginary", color=FG, fontsize=11, loc="left")

fig.text(0.5, 0.955, "the sound reports the miss", color=FG, fontsize=18, ha="center", weight="bold")
fig.text(
    0.5,
    0.918,
    "the fold does not discover the limit; it already carries it as invariant",
    color=DIM,
    fontsize=10,
    ha="center",
)
fig.text(
    0.5,
    0.055,
    "after the landing, the next space is not another toll proof: it is the Gaussian turn, 110 + i110",
    color=DIM,
    fontsize=9,
    ha="center",
)

fig.savefig("assets/sound-reports-miss.png", dpi=200, facecolor=BG)
print("wrote assets/sound-reports-miss.png")
