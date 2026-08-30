"""the kiss, seen — the fold and the mirror meet at the count alone.

On each count cell the fold P(x)=floor(x) is the flat line at the count and the
mirror M(x)=2floor(x)-x is the descending line through it; they agree at the
count (the kiss) and peel apart inside the cell.  Their difference is the miss,
which carries a sign — a direction.  0 cents is not a distance; it is an arrow
of zero length.  The wait 23.8769: the fold reads 23, the mirror 22.1231 — the
residue 0.877 is the arrow, pointing toward the shore.  The walk
23.8769 -> 22.1231 -> 21.8769 ... descends the mirror line, never returning.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

x = np.linspace(20.0, 25.0, 6000)
fold = np.floor(x)
mirror = 2 * np.floor(x) - x

fig, ax = plt.subplots(figsize=(7.2, 5.4))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# the count grid (horizontal bands at integers)
for c in range(20, 26):
    ax.axhline(c, color="#e2ddd4", lw=0.8, ls=(0, (4, 4)), zorder=1)

# the fold: the count's flat line, warm
ax.plot(x, fold, color="#9a6a33", lw=3.0, solid_capstyle="round", zorder=3,
        label="the fold  ⌊x⌋")
# the mirror: the descending sawtooth, cool
ax.plot(x, mirror, color="#3d6b8f", lw=2.4, ls="--", zorder=3,
        label="the mirror  2⌊x⌋−x")

# the kisses: where they agree — every integer
for c in range(21, 25):
    ax.plot(c, c, "o", ms=9, mfc="#111111", mec="#111111", zorder=6)

# the wait: x=23.8769, fold=23, mirror=22.1231 — the residue as an arrow
xw = 23.8769
fw = np.floor(xw)
mw = 2 * np.floor(xw) - xw
ax.annotate("", xy=(xw, mw), xytext=(xw, fw),
            arrowprops=dict(arrowstyle="-|>", lw=2.6, color="#c0392b",
                            shrinkA=0, shrinkB=0),
            zorder=5)
ax.text(xw + 0.05, (fw + mw) / 2, "  the residue\n  0.877, the arrow",
        fontsize=10, color="#c0392b", va="center", fontstyle="italic")

# the walk: x -> M(x), descending, never returning
xs = [23.8769]
for _ in range(5):
    xs.append(2 * np.floor(xs[-1]) - xs[-1])
xs = np.array(xs)
ax.scatter(xs, xs, s=26, color="#111111", zorder=7)
ax.plot(xs, xs, color="#111111", lw=1.4, ls=":", zorder=4)

ax.annotate("the kiss", xy=(23, 23), xytext=(23.35, 23.9),
            fontsize=11, color="#111111", fontstyle="italic",
            arrowprops=dict(arrowstyle="->", lw=1.1, color="#111111"))
ax.annotate("the wait 23.8769", xy=(xw, fw), xytext=(23.3, 23.05),
            fontsize=10, color="#111111", fontstyle="italic")
ax.annotate("the walk descends,\nnever returning", xy=(xs[2], xs[2]),
            xytext=(21.0, 24.0), fontsize=10, color="#111111",
            fontstyle="italic",
            arrowprops=dict(arrowstyle="->", lw=1.0, color="#111111"))

ax.set_title("0¢ is not a distance — it is an arrow",
             fontsize=13, color="#111111", pad=10)
ax.set_xlabel("the where x", fontsize=10)
ax.set_ylabel("the count (cell height)", fontsize=10)
ax.set_ylim(20.0, 25.2)
ax.set_xlim(20.0, 25.2)
ax.set_xticks(range(21, 25))
ax.set_yticks(range(21, 25))
ax.tick_params(labelsize=9)
ax.legend(loc="upper left", fontsize=9, frameon=False)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.spines["left"].set_color("#999999")
ax.spines["bottom"].set_color("#999999")

plt.tight_layout()
plt.savefig("assets/arrow-cover.png", dpi=200, bbox_inches="tight",
            facecolor="white")
print("wrote assets/arrow-cover.png")
