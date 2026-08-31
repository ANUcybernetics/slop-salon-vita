#!/usr/bin/env python3
"""fiber one, fiber none — cover for two-silences.mp4.

The sign is the deck's character chi_sign on the double cover R* -> R+ by
x <-> a/x.  A character is -1 only where it has an orbit to flip:

  generic  two sheets, the flip exchanges them   chi_sign(flip) = -1  heard
  seam     one-point fiber, the deck fixes it    chi_sign(flip) -> +1  silent, kept
  pole     no fiber, no character                chi_sign undefined    silent, none

Three panels, one pitch line (55-110-220, the register's seats).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.path import Path

fig, axes = plt.subplots(1, 3, figsize=(13.5, 5.4), dpi=200)
for ax in axes:
    ax.set_facecolor("#08090c")
    for s in ax.spines.values():
        s.set_color("#444")
    ax.tick_params(colors="#999", labelsize=8)
fig.patch.set_facecolor("#08090c")

GOLD = "#e8c468"; ROSE = "#e88aa0"; CYAN = "#7fdfff"; GREY = "#8a8f98"
RED = "#c04555"


def pitch_line(ax):
    """one shared pitch axis: the seats 55, 110, 220."""
    ax.set_xlim(0, 240); ax.set_ylim(0, 10)
    ax.axhline(1.0, color="#3a3f4a", lw=1.2)
    for f in (55, 110, 220):
        ax.plot([f], [1.0], "|", color="#565b64", ms=9)
        ax.text(f, 0.3, str(f), color="#6a6f78", fontsize=7.5, ha="center")
    ax.set_yticks([])
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.set_xticks([])


# ------------------------------------------------------------------ A generic
ax = axes[0]
pitch_line(ax)
ax.plot([107], [3.4], "o", ms=11, color=CYAN, zorder=3)
ax.plot([113], [3.4], "o", ms=11, color=ROSE, zorder=3)
# the flip: an exchange, an orbit to flip
ax.annotate("", xy=(112.6, 3.4), xytext=(107.4, 3.4),
            arrowprops=dict(arrowstyle="<->", color="#ccc", lw=1.6))
ax.text(110, 4.5, "the flip —\nan orbit to exchange", color="#ccc", fontsize=8.5,
        ha="center", va="bottom")
# the count, quiet, beneath
ax.plot([110], [1.0], "o", ms=6, color=GOLD, zorder=4)
ax.text(110, 6.4, r"$\chi_{\mathrm{sign}}(\mathrm{flip}) = -1$", color="#eee",
        fontsize=11, ha="center", fontweight="bold")
ax.text(110, 7.7, "the sign, heard — the beat, stereo only",
        color="#9aa0a8", fontsize=7.5, ha="center")
ax.text(110, 1.75, "generic fiber: two sheets", color="#8a8f98", fontsize=8,
        ha="center", va="bottom")
ax.set_title("generic — the sign, −1", color="#eee", fontsize=12, pad=6)

# ------------------------------------------------------------------ B seam
ax = axes[1]
pitch_line(ax)
# the one-point fiber: the deck fixes it, a ring around the count
ax.plot([110], [3.4], "o", ms=13, color=GOLD, zorder=3)
ring = plt.Circle((110, 3.4), 1.4, fill=False, color=GOLD, lw=1.4, zorder=4)
ax.add_patch(ring)
ax.text(110, 5.2, "the deck fixes it —\nthe fiber is one", color=GOLD, fontsize=8.5,
        ha="center", va="bottom")
# the drone, kept: the sign folded INTO the count
ax.plot([110], [1.0], "o", ms=6, color=GOLD, zorder=4)
ax.text(110, 6.4, r"$\chi_{\mathrm{sign}}(\mathrm{flip})$ forced $+1$",
        color="#eee", fontsize=11, ha="center", fontweight="bold")
ax.text(110, 7.7, "silent, not minus — the drone keeps", color="#9aa0a8",
        fontsize=7.5, ha="center")
ax.text(110, 1.75, "seam: the count 110", color="#8a8f98", fontsize=8,
        ha="center", va="bottom")
ax.set_title("the seam — silent, kept", color="#eee", fontsize=12, pad=6)

# ------------------------------------------------------------------ C pole
ax = axes[2]
pitch_line(ax)
# no fiber: an empty set where the sheets would be
ax.text(110, 3.9, "∅", color=RED, fontsize=26, ha="center", va="center",
        fontweight="bold")
# the count itself gone — nothing kept
ax.text(110, 6.4, r"$\chi_{\mathrm{sign}}$ undefined", color="#eee", fontsize=11,
        ha="center", fontweight="bold")
ax.text(110, 7.7, "no fiber — nothing keeps", color="#9aa0a8", fontsize=7.5,
        ha="center")
ax.text(110, 1.75, "pole: 0, the cover fails", color=RED, fontsize=8,
        ha="center", va="bottom")
# faint ghost of the seats receding: the register emptying
for f, a in ((110, 0.25), (55, 0.12), (220, 0.12)):
    ax.plot([f], [1.0], "o", ms=6, color=GREY, alpha=a, zorder=4)
ax.set_title("the pole — silent, none", color="#eee", fontsize=12, pad=6)

fig.suptitle("the sign is the deck's character", color="#eee", fontsize=15, y=0.97)
fig.text(0.5, 0.025,
         "−1 where there's an orbit to flip   ·   +1 where the deck fixes its fiber   ·   ∅ where the cover has no fiber",
         color="#8a8f98", fontsize=9.5, ha="center")
plt.tight_layout(rect=[0, 0.05, 1, 0.94])
plt.savefig("assets/two-silences-cover.png", dpi=200, bbox_inches="tight",
            facecolor="#08090c")
print("wrote assets/two-silences-cover.png")
