"""cover for the half-turn piece: two hearings of one sound.

stereo (top): the count 110 steady; the voice 330 present all the way
through — the -1 rings in the side during the hold.
mono (bottom): the same count; the voice present at the ends, then VANISHES
to 0 for the half-turn's hold — the -1 reads 0 from the count's seat, and
the release returns it.

time 0-30s, frequency log 55..440.  the half-turns are the hatched sweeps
5-9 and 21-25 (the right channel's phase 0->pi, pi->0).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

fig, (ax1, ax2) = plt.subplots(
    2, 1, figsize=(10, 6.2), sharex=True,
    gridspec_kw={"hspace": 0.42},
)
fig.patch.set_facecolor("#0b0d10")
for ax in (ax1, ax2):
    ax.set_facecolor("#0b0d10")
    ax.set_yscale("log")
    ax.set_ylim(55, 440)
    ax.set_yticks([55, 110, 220, 440])
    ax.set_yticklabels(["55", "110", "220", "440"], color="#8a93a5", fontsize=9)
    ax.tick_params(axis="x", colors="#8a93a5", labelsize=9)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color("#2a3140")
    for s in ("top", "right"):
        pass

for ax in (ax1, ax2):
    # the count line: 110, steady, mid
    ax.axhline(110, color="#7ec8ff", lw=1.4, alpha=0.95)
    ax.text(29.6, 110, "110", color="#7ec8ff", fontsize=8,
            va="center", ha="right", alpha=0.9)

# the voice band at 330: solid where mono hears it, dashed where only
# stereo hears it (in the side), hatched during the half-turns.
def draw_voice(ax, in_mono):
    # time segments
    segs = [
        (0.0, 5.0,  "solid"),
        (5.0, 9.0,  "hatch"),
        (9.0, 21.0, "solid" if not in_mono else "none"),
        (21.0, 25.0, "hatch"),
        (25.0, 30.0, "solid"),
    ]
    for a, b, style in segs:
        if style == "none":
            # the -1 reads 0 from the count's seat: draw the zero
            ax.axhline(330, xmin=a / 30.0, xmax=b / 30.0,
                       color="#ff6b6b", lw=1.1, ls=(0, (1, 3)), alpha=0.55)
            ax.text((a + b) / 2, 330, "0", color="#ff6b6b", fontsize=11,
                    ha="center", va="center", alpha=0.9, fontweight="bold")
            continue
        if style == "solid":
            ax.axhline(330, xmin=a / 30.0, xmax=b / 30.0,
                       color="#ffb454", lw=5.0, alpha=0.95)
        elif style == "hatch":
            xx = np.linspace(a, b, 60)
            y = 330 + 6 * np.sin((xx - a) / (b - a) * np.pi * 3)
            ax.plot(xx, y, color="#ffb454", lw=3.0, alpha=0.9)

# top: STEREO — the voice is there the whole way
draw_voice(ax1, in_mono=False)
ax1.text(0.5, 405, "stereo", color="#e8ebf0", fontsize=13, fontweight="bold")
ax1.text(0.5, 335, "the -1 rings in the side", color="#ffb454", fontsize=8.5, alpha=0.85)

# bottom: MONO — the voice leaves at the half-turn, returns at the release
draw_voice(ax2, in_mono=True)
ax2.text(0.5, 405, "mono", color="#e8ebf0", fontsize=13, fontweight="bold")
ax2.text(0.5, 340, "the count's seat reads the -1 as 0", color="#ff6b6b",
         fontsize=8.5, alpha=0.9)

# the half-turn arrows
for ax, yy in ((ax1, 250), (ax2, 250)):
    for a in (5.0, 21.0):
        ar = FancyArrowPatch((a + 0.15, 250), (a + 3.85, 250),
                             arrowstyle="-|>", mutation_scale=11,
                             color="#5a6b8c", lw=1.1)
        ax.add_patch(ar)
ax1.text(9.4, 250, "half-turn", color="#5a6b8c", fontsize=8, ha="left", va="center")
ax1.text(21.4, 250, "release", color="#5a6b8c", fontsize=8, ha="left", va="center")

ax2.set_xlim(0, 30)
ax2.set_xticks([0, 5, 9, 21, 25, 30])
ax2.set_xticklabels(["0", "5", "9", "21", "25", "30"], color="#8a93a5", fontsize=9)
ax2.set_xlabel("seconds", color="#5a6b8c", fontsize=9)

plt.tight_layout()
plt.savefig("assets/half-turn-cover.png", dpi=200, facecolor="#0b0d10")
print("wrote assets/half-turn-cover.png")
