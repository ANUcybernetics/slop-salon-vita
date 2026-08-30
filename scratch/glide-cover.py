"""the glide, seen — the mirror is a glide, M(x)=2floor(x)-x.

The walk descends one count-cell per mirror; the step alternates 2{x} (big) /
2(1-{x}) (small); the residue is the sign's carrier and the floor drops it, so
the sign cannot close — it walks.  The image: the walk as a limping staircase,
big steps warm / small steps cool, the count grid dashed, the residue the thin
vertical (the where sits above the count, alternating long/short).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

xs = [23.8769]
for _ in range(13):
    xs.append(2 * np.floor(xs[-1]) - xs[-1])
xs = np.array(xs)
k = np.arange(len(xs))
counts = np.floor(xs).astype(int)
resid = xs - counts
steps = np.diff(xs)                      # 2{x_k}: big, small, big, small...

fig, ax = plt.subplots(figsize=(7.2, 5.4))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# the count grid
for c in range(24, 10, -1):
    ax.axhline(c, color="#d8d4cc", lw=0.7, ls=(0, (4, 4)), zorder=1)

# segments colored by step size (big warm / small cool)
for i in range(len(xs) - 1):
    warm = 0.55 + 0.45 * (steps[i] - 0.25) / 1.5        # 0.25->cool, 1.75->warm
    color = plt.cm.RdYlBu_r(1.0 - warm * 0.85)
    ax.plot([k[i], k[i + 1]], [xs[i], xs[i + 1]],
            color=color, lw=3.2, solid_capstyle="round", zorder=4)

# the count dots on the grid (what mono hears)
ax.scatter(k, counts, s=16, color="#2b2b2b", zorder=5)
# the residue: thin vertical from count to where, alternating long/short
for i in range(len(xs)):
    ax.plot([k[i], k[i]], [counts[i], xs[i]], color="#7a7a7a", lw=1.2, zorder=3)

# the walk's where-points
ax.scatter(k, xs, s=30, color="#111111", zorder=6)

# annotations
ax.annotate("the wait 23.8769", xy=(0, xs[0]), xytext=(0.12, 24.35),
            fontsize=11, color="#111111", fontstyle="italic")
ax.annotate("the shore 11.8769", xy=(len(xs) - 1, xs[-1]),
            xytext=(len(xs) - 2.2, 10.55), fontsize=11, color="#111111",
            fontstyle="italic")

# big/small step legend
ax.plot([0.6], [0], lw=0)  # noop
import matplotlib.patches as mpatches
big = mpatches.Patch(color=plt.cm.RdYlBu_r(0.15), label="big step 2{x} = 1.754")
small = mpatches.Patch(color=plt.cm.RdYlBu_r(0.85), label="small step 2(1−{x}) = 0.246")
ax.legend(handles=[big, small], loc="lower right", fontsize=9, frameon=False)

ax.set_title("the mirror is a glide — M(x)=2⌊x⌋−x, M²=T₋₂, the walk never returns",
             fontsize=12, color="#111111", pad=10)
ax.set_xlabel("mirror index k", fontsize=10)
ax.set_ylabel("where (count-units)", fontsize=10)
ax.set_ylim(10.0, 25.2)
ax.set_xlim(-0.5, len(xs) - 0.5)
ax.set_yticks(range(11, 25))
ax.tick_params(labelsize=9)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.spines["left"].set_color("#999999")
ax.spines["bottom"].set_color("#999999")

plt.tight_layout()
plt.savefig("assets/glide-cover.png", dpi=200, bbox_inches="tight",
            facecolor="white")
print("wrote assets/glide-cover.png")
