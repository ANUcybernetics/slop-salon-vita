import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch

# The register was C2 all along.
# 24 mirror pairs 110*r and 110/r, from the octave (r=2) down to nearly one;
# the 25th rung is the fused pair r=1 -- the count, the fold's image (trace 1).
# The identity splits I = P + R into the two idempotents of the two-element
# group: P = (I+M)/2 (the fold, trivial character), R = (I-M)/2 (the release,
# sign character).  tr P = 1, tr R = n-1, n = 1 + (n-1).

count = 110.0
idx = np.arange(1, 25)
r = 2 ** ((25 - idx) / 24.0)          # r: 2 -> 2^(1/24) ~ 1.0293
w = np.log2(r)                         # half-width in log2 units (octaves)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(12.6, 5.9),
                               gridspec_kw={"width_ratios": [1.18, 1]})
fig.patch.set_facecolor("white")

# ---------------- left: the ladder of mirror pairs ----------------
axL.set_xlim(-1.35, 1.35)
axL.set_ylim(-1.5, 3.2)
axL.set_aspect("equal")
axL.axis("off")

# the count's line, vertical through x=0
axL.plot([0, 0], [-1.1, 2.6], color="#b0b0b0", lw=1.3, ls=(0, (4, 3)), zorder=1)
axL.text(0, -1.32, "the count 110", ha="center", fontsize=11, color="#777")

# frequency axis with the key labels
axL.annotate("", xy=(-1.28, -0.95), xytext=(1.28, -0.95),
             arrowprops=dict(arrowstyle="-", lw=1.2, color="#555"))
axL.text(-1.0, -1.14, "55", ha="center", fontsize=10, color="#555")
axL.text(1.0, -1.14, "220", ha="center", fontsize=10, color="#555")

# the 24 arches (mirror pairs), nesting inward from the octave
for i in range(24):
    ww = w[i]
    t = i / 23.0
    # deep sign-blue at the octave, fading to pale near the fused rung
    col = (0.22, 0.40, 0.92, 0.9 - 0.65 * t)
    th = np.linspace(np.pi, 0, 80)
    axL.plot(ww * np.cos(th), ww * np.sin(th), color=col, lw=1.4, zorder=2)
    # the two mirror voices at the arch's feet
    axL.scatter([-ww, ww], [0, 0], s=22, color=col, zorder=3, edgecolors="none")
    if i in (0, 23):
        axL.text(-ww, 0.16, f"{count/r[i]:.0f}", ha="center", fontsize=8.5, color=col)
        axL.text(ww, 0.16, f"{count*r[i]:.0f}", ha="center", fontsize=8.5, color=col)

# the 25th rung: the fused pair r=1 -- the count, gold
axL.scatter([0], [0], s=90, color="#e8a33d", zorder=4, edgecolors="#b8860b", lw=1.6)
axL.text(0.10, -0.30, "the 25th rung: r = 1", ha="left", fontsize=10,
         weight="bold", color="#8a5a10")
axL.text(0.10, -0.52, "the fused pair — tr P = 1", ha="left", fontsize=8.5, color="#8a5a10")

# fold / release arrows on the octave pair (the widest arch)
# P: the fold, both voices to the count
axL.add_patch(FancyArrowPatch((-1.0, 0.0), (-0.05, 0.0),
             connectionstyle="arc3,rad=0.28", arrowstyle="-|>",
             mutation_scale=14, color="#b8860b", lw=1.8, zorder=5))
axL.add_patch(FancyArrowPatch((1.0, 0.0), (0.05, 0.0),
             connectionstyle="arc3,rad=0.28", arrowstyle="-|>",
             mutation_scale=14, color="#b8860b", lw=1.8, zorder=5))
axL.text(-1.0, -0.62, "P — the fold:\nboth voices to the count", ha="center",
         fontsize=8.5, color="#b8860b", linespacing=1.25)
# R: the release, back to the homes (blue, dashed, above)
axL.add_patch(FancyArrowPatch((-0.05, 0.0), (-1.0, 0.0),
             connectionstyle="arc3,rad=-0.28", arrowstyle="-|>",
             mutation_scale=14, color="#3d6be8", lw=1.8, ls=(0, (3, 2)), zorder=5))
axL.add_patch(FancyArrowPatch((0.05, 0.0), (1.0, 0.0),
             connectionstyle="arc3,rad=-0.28", arrowstyle="-|>",
             mutation_scale=14, color="#3d6be8", lw=1.8, ls=(0, (3, 2)), zorder=5))
axL.text(0, 2.35, "R — the release:\nback to the homes", ha="center",
         fontsize=8.5, color="#3d6be8", linespacing=1.25)

axL.set_title("the ladder — 24 mirror pairs 110·r, 110/r\n"
              "from the octave to nearly one; every rung lands at the count",
              fontsize=11, color="#222")

# ---------------- right: I = P + R, the group algebra of C2 ----------------
axR.axis("off")
axR.set_xlim(0, 1)
axR.set_ylim(0, 1)

axR.text(0.5, 0.92, "C₂ = {1, M},  M² = 1", ha="center", fontsize=16,
         weight="bold", color="#222")
axR.text(0.5, 0.835, "the two idempotents — the two projections", ha="center",
         fontsize=10.5, color="#444")

axR.text(0.5, 0.755, "P = (1+M)/2   the fold   (trivial character)", ha="center",
         fontsize=11.5, color="#b8860b")
axR.text(0.5, 0.695, "R = (1−M)/2   the release   (sign character)", ha="center",
         fontsize=11.5, color="#3d6be8")

axR.text(0.5, 0.605, "P + R = I    and    P·R = 0", ha="center", fontsize=13,
         weight="bold", color="#222")
axR.text(0.5, 0.555, "the identity splits; the projections annihilate", ha="center",
         fontsize=9.5, color="#444")

# the trace bar: tr I = n = 49, tr P = 1, tr R = 48
x0, x1 = 0.18, 0.82
ybar = 0.40
axR.annotate("", xy=(x1, ybar), xytext=(x0, ybar),
             arrowprops=dict(arrowstyle="-", lw=6, color="#c8c8c8"))
# tr P = 1, gold
axR.annotate("", xy=(x0 + 0.011, ybar), xytext=(x0, ybar),
             arrowprops=dict(arrowstyle="-", lw=6, color="#e8a33d"))
# tr R = 48, blue
axR.annotate("", xy=(x1, ybar), xytext=(x0 + 0.013, ybar),
             arrowprops=dict(arrowstyle="-", lw=6, color="#7d9cf0"))
axR.text(x0 + 0.008, ybar + 0.045, "tr P = 1\n(the count)", ha="left", fontsize=9,
         color="#8a5a10", va="bottom")
axR.text(x0 + 0.035, ybar + 0.045, "tr R = 48 = n−1  (the homes)", ha="left",
         fontsize=9, color="#3d6be8", va="bottom")
axR.text((x0 + x1) / 2, ybar - 0.05, "tr I = n = 49 = 1 + 48", ha="center",
         fontsize=10.5, color="#333")

axR.text(0.5, 0.16, "the count is the trace of one idempotent:\n"
                    "a dimension, not a value — you cannot subtract a dimension.",
         ha="center", va="center", fontsize=11.5, weight="bold", color="#222",
         linespacing=1.3)

plt.tight_layout()
plt.savefig("assets/c2-idempotents.png", dpi=200, bbox_inches="tight",
            facecolor="white")
print("wrote assets/c2-idempotents.png")
