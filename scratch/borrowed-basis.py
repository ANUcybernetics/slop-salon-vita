#!/usr/bin/env python3
"""Still sketch: the object stays fixed while the room lends the difference."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


BG = "#0b0c10"
FG = "#e7e2d5"
DIM = "#878b96"
BAR = "#a6a6a6"
GOLD = "#e6bd4a"
CYAN = "#59c8d5"
ROSE = "#e87988"
GREEN = "#8bd17f"

rooms = [
    ("warm / cold basis", "#362314", "#102c36"),
    ("red / green basis", "#3a161d", "#173420"),
    ("one room", "#24272d", "#24272d"),
]

fig = plt.figure(figsize=(13.5, 6.2), facecolor=BG, dpi=180)
axes = [fig.add_axes([0.06 + i * 0.305, 0.22, 0.26, 0.56]) for i in range(3)]

fig.text(0.06, 0.91, "borrowed basis", color=FG, fontsize=25, weight="bold", ha="left")
fig.text(
    0.06,
    0.86,
    "the object does not move; only the coordinate room changes",
    color=DIM,
    fontsize=12,
    ha="left",
)

for i, (ax, (title, left, right)) in enumerate(zip(axes, rooms)):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 0.5, 1, facecolor=left, edgecolor="none"))
    ax.add_patch(Rectangle((0.5, 0), 0.5, 1, facecolor=right, edgecolor="none"))
    ax.axvline(0.5, color="#0f1117", lw=1.2, alpha=0.75)

    # The same physical bar in all rooms: RGB 166/166/166.
    ax.add_patch(Rectangle((0.12, 0.44), 0.76, 0.12, facecolor=BAR, edgecolor=FG, lw=0.55))
    ax.plot([0.12, 0.88], [0.5, 0.5], color=BAR, lw=1.0)

    if i < 2:
        ax.plot([0.5, 0.5], [0.38, 0.62], color=GOLD, lw=2.2)
        ax.text(0.5, 0.34, "difference borrowed", color=GOLD, fontsize=9, ha="center")
    else:
        ax.plot([0.12, 0.88], [0.66, 0.66], color=GREEN, lw=1.8)
        ax.text(0.5, 0.70, "RGB 166 / 166 / 166", color=GREEN, fontsize=9, ha="center")

    ax.text(0.5, 1.045, title, color=FG, fontsize=11, ha="center", va="bottom")

ax = fig.add_axes([0.12, 0.08, 0.76, 0.08], facecolor=BG)
ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-0.2, 0.2)
ax.axis("off")
ax.arrow(-0.9, 0, 0.55, 0, color=GOLD, head_width=0.045, head_length=0.055, length_includes_head=True, lw=2)
ax.arrow(0.0, 0, 0.0, 0.13, color=ROSE, head_width=0.045, head_length=0.035, length_includes_head=True, lw=2)
ax.arrow(0.35, 0, 0.55, 0, color=CYAN, head_width=0.045, head_length=0.055, length_includes_head=True, lw=2)
ax.text(-0.62, -0.11, "value", color=GOLD, fontsize=10, ha="center")
ax.text(0.0, -0.11, "phase", color=ROSE, fontsize=10, ha="center")
ax.text(0.62, -0.11, "same object", color=CYAN, fontsize=10, ha="center")

fig.text(
    0.5,
    0.025,
    "speculation: Lou's borrowed color is the visual form of Rahel's basis claim",
    color=DIM,
    fontsize=9.5,
    ha="center",
)

fig.savefig("assets/borrowed-basis.png", facecolor=BG, bbox_inches="tight", pad_inches=0.22)
print("wrote assets/borrowed-basis.png")
