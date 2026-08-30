"""the kiss, measured — the fold is a line, the mirror a curve, tangent at 110.

The fold 220-x is straight: no curvature, so it cannot hear the sign.  The
mirror 12100/x is a hyperbola whose curvature at the count is exactly the
second-order term — the miss squared over the count.  At x=110 they are
tangent: same value, same slope, and they part quadratically:

    gap = fold - mirror = -(x-110)^2/110   (gert: exact)

the seal is quadratic; the crossing is linear.  The ladder's points ride the
mirror, and as they descend toward 110 the two curves fuse — the kiss seals,
the sign goes to 2e-7 Hz.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

x = np.linspace(70.0, 150.0, 6000)
fold = 220.0 - x          # the straight line
mirror = 12100.0 / x      # the hyperbola

fig, ax = plt.subplots(figsize=(7.2, 5.4))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# the count line
ax.axvline(110, color="#e2ddd4", lw=0.8, ls=(0, (4, 4)), zorder=1)
ax.axhline(110, color="#e2ddd4", lw=0.8, ls=(0, (4, 4)), zorder=1)

# the curvature gap, shaded (fold - mirror, the sign)
gap_x = np.linspace(100.0, 120.0, 800)
gap_fold = 220.0 - gap_x
gap_mir = 12100.0 / gap_x
ax.fill_between(gap_x, gap_mir, gap_fold, color="#c0392b", alpha=0.10, zorder=2)
ax.annotate("the sign:\ncurvature, gap=(x−110)²/110",
            xy=(116, 104), xytext=(118, 88), fontsize=9, color="#c0392b",
            fontstyle="italic", va="center",
            arrowprops=dict(arrowstyle="->", lw=1.0, color="#c0392b"))

# the fold: a straight line — no curvature, deaf to the sign
ax.plot(x, fold, color="#9a6a33", lw=3.0, solid_capstyle="round", zorder=3,
        label="the fold  220−x — a line, no curvature")
# the mirror: the hyperbola, curved
ax.plot(x, mirror, color="#3d6b8f", lw=2.4, zorder=3,
        label="the mirror  12100/x — curvature 2/x")

# the shared tangent at the kiss
tx = np.linspace(86.0, 134.0, 200)
ax.plot(tx, 220.0 - tx, color="#111111", lw=1.0, ls=":", zorder=2,
        label="the shared tangent (1st order)")
ax.plot(110, 110, "o", ms=11, mfc="#111111", mec="#111111", zorder=6)
ax.annotate("the kiss\n(110,110)", xy=(110, 110), xytext=(113, 118),
            fontsize=11, color="#111111", fontstyle="italic",
            arrowprops=dict(arrowstyle="->", lw=1.1, color="#111111"))

# the ladder's readings on the mirror: +204 ... +0.076 cents
ladder_c = [204.0, 90.0, 23.5, 19.8, 3.6, 1.8, 0.076]
for m in ladder_c:
    f1 = 110.0 * 2.0 ** (m / 1200.0)
    mr = 12100.0 / f1
    ax.plot(f1, mr, "o", ms=5, mfc="#3d6b8f", mec="white", mew=1.0, zorder=5)
ax.plot(110.0, 110.0, "o", ms=11, mfc="#111111", mec="#111111", zorder=6)

# the peel, exaggerated on the right edge: the two readings parting
xr = 120.0
ax.plot([xr, xr], [12100.0 / xr, 220.0 - xr], color="#c0392b", lw=1.4, zorder=4)
ax.annotate("first order they agree,\nsecond order they part", xy=(120, 99),
            xytext=(122, 130), fontsize=9, color="#111111", fontstyle="italic",
            va="center",
            arrowprops=dict(arrowstyle="->", lw=1.0, color="#111111"))

ax.set_title("the kiss is a curve — the sign is the curvature",
             fontsize=13, color="#111111", pad=10)
ax.set_xlabel("the tone f1 (Hz)", fontsize=10)
ax.set_ylabel("the reflection about the count (Hz)", fontsize=10)
ax.set_xlim(80.0, 138.0)
ax.set_ylim(82.0, 140.0)
ax.tick_params(labelsize=9)
ax.legend(loc="upper right", fontsize=8.5, frameon=False)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.spines["left"].set_color("#999999")
ax.spines["bottom"].set_color("#999999")

plt.tight_layout()
plt.savefig("assets/kiss-cover.png", dpi=200, bbox_inches="tight",
            facecolor="white")
print("wrote assets/kiss-cover.png")
