"""one set, two measures, heard — cover.

A staircase of bounded-quotient Hausdorff dimensions stepping up toward the
dashed line at 1; a flat line at 0, the count. The last step falls short.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ladder = [
    (2, 0.4687), (3, 0.2943), (4, 0.2111), (5, 0.1632), (6, 0.1324),
    (8, 0.0954), (10, 0.0743), (13, 0.0555), (16, 0.0441), (20, 0.0346),
    (25, 0.0272), (30, 0.0224), (40, 0.0165), (60, 0.0108), (100, 0.0063),
]
Ks = [k for k, _ in ladder]
ds = [1 - m for _, m in ladder]

fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=100)
fig.patch.set_facecolor("#0a0c14")
ax.set_facecolor("#0a0c14")

# the line at 1, dashed — dimension 1
ax.axhline(1.0, color="#e8e6ef", lw=1.4, ls=(0, (6, 4)), alpha=0.9, zorder=2)
# the count, flat at 0
ax.axhline(0.0, color="#5cc8ff", lw=2.0, alpha=0.95, zorder=3)

# staircase
for i in range(len(Ks)):
    x0 = np.log10(Ks[i]) if i == 0 else np.log10(Ks[i - 1])
    x1 = np.log10(Ks[i])
    y = ds[i]
    if i == 0:
        x0 = np.log10(2)
        ax.plot([x0, x1], [y, y], color="#e6b84c", lw=2.6, zorder=4)
    else:
        yprev = ds[i - 1]
        ax.plot([x0, x0], [yprev, y], color="#e6b84c", lw=1.0, alpha=0.7, zorder=4)
        ax.plot([x0, x1], [y, y], color="#e6b84c", lw=2.6, zorder=4)

# the seam: last step falls short of the line
lx = np.log10(Ks[-1])
ly = ds[-1]
ax.annotate("", xy=(lx, 1.0), xytext=(lx, ly),
            arrowprops=dict(arrowstyle="->", color="#ff7a6b", lw=1.8,
                            connectionstyle="arc3,rad=0"), zorder=5)
ax.plot([lx], [ly], "o", color="#e6b84c", ms=6, zorder=5)

ax.text(np.log10(2) - 0.06, 0.045, "the count — measure 0", color="#5cc8ff",
        fontsize=13, ha="left", va="bottom")
ax.text(np.log10(100) + 0.02, 1.0, "dimension 1 — the line", color="#e8e6ef",
        fontsize=13, ha="left", va="center")
ax.text(lx + 0.02, (ly + 1.0) / 2, "the seam", color="#ff7a6b",
        fontsize=13, ha="left", va="center")

ax.set_xlim(np.log10(1.5), np.log10(260))
ax.set_ylim(-0.06, 1.14)
ax.set_xlabel("digit bound K", color="#9aa0b5", fontsize=12)
ax.set_ylabel("Hausdorff dimension", color="#9aa0b5", fontsize=12)
ax.set_xticks(np.log10([2, 3, 5, 10, 30, 100]))
ax.set_xticklabels(["2", "3", "5", "10", "30", "100"], color="#9aa0b5")
ax.tick_params(colors="#9aa0b5")
for s in ax.spines.values():
    s.set_color("#3a3f52")
ax.set_title("one set, two measures", color="#e8e6ef", fontsize=16, loc="left", pad=12)

plt.tight_layout()
plt.savefig("assets/seam-heard-cover.png", dpi=100, facecolor="#0a0c14")
print("cover done")
