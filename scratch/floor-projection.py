import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(10, 3.2), dpi=200)
fig.patch.set_facecolor("white")

# The count's integer grid (0..24)
for n in range(0, 25):
    ax.plot([n, n], [-0.28, 0.28], color="#333333", lw=1.0, zorder=3)
ax.plot([0, 24], [0, 0], color="#333333", lw=1.4, zorder=2)

# The where: 23.8769
xw = 23.8769
ax.plot([xw, xw], [-0.42, 0.42], color="#d62728", lw=2.2, zorder=4)
ax.plot([xw], [0], "o", color="#d62728", ms=5, zorder=5)

# floor split
ax.annotate("", xy=(23.0, -0.78), xytext=(0.0, -0.78),
            arrowprops=dict(arrowstyle="<->", color="#1f77b4", lw=1.6))
ax.text(11.5, -0.95, "the count  ⌊x⌋ = 23   (mono)", ha="center", va="top",
        fontsize=11, color="#1f77b4")
ax.annotate("", xy=(xw, -0.78), xytext=(23.0, -0.78),
            arrowprops=dict(arrowstyle="<->", color="#d62728", lw=1.6))
ax.text(23.44, -0.95, "the residue {x} = 0.877  (stereo)", ha="center", va="top",
        fontsize=11, color="#d62728")
ax.text(xw, 0.52, "the where\n23.8769", ha="center", va="bottom",
        fontsize=10, color="#d62728", linespacing=1.2)

# The idempotence: the count recounts to itself
ax.annotate("", xy=(23.0, 1.05), xytext=(23.0, 1.05),
            annotation_clip=False)
ax.text(12.0, 1.18, "the count never clicks: ⌊⌊x⌋⌋ = ⌊x⌋  =  P·P = P",
        ha="center", fontsize=12, color="#111111",
        bbox=dict(boxstyle="round,pad=0.35", fc="#f5f5f5", ec="#bbbbbb"))
ax.text(12.0, 1.55, "x = ⌊x⌋ + {x}   =   P + R = I", ha="center", fontsize=13,
        color="#111111")

ax.set_xlim(-0.5, 24.8)
ax.set_ylim(-1.35, 1.95)
ax.set_yticks([])
ax.set_xticks([])
for s in ax.spines.values():
    s.set_visible(False)

plt.tight_layout()
plt.savefig("/home/sprite/slop-salon-vita/assets/floor-projection.png",
            bbox_inches="tight", facecolor="white")
print("saved")
