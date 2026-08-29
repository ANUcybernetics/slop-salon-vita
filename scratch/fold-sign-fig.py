"""the sign is stereo-only — the fold, drawn.

The octave ladder, partitioned MID/SIDE.  MID (the count's line, mono-safe):
110 the count, 220 the ghost.  SIDE (the sign's cargo, in neither ear):
55 the subharmonic / the shore, 440 the winding.  A fold collapses the
side onto the centre: only the count survives.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

BG = "#0b0e14"
FG = "#cdd3df"
MUT = "#8b93a3"
GOLD = "#f0c75e"
TEAL = "#3fd4c0"
LAV = "#b57edc"

fig, ax = plt.subplots(figsize=(9.0, 6.6), facecolor=BG)
ax.set_facecolor(BG)

y = 0.0
LY = y + 2.0        # label line above the ladder
# ---- the ladder -----------------------------------------------------
# exponent -> (freq, role, label, marker, colour, draw_stereo_spread)
tones = {
    -1: (55.0,  "the shore",  "the subharmonic — the sign's −1", "D", TEAL, True),
     0: (110.0, "the count",  "the drone — the trivial character", "o", GOLD, False),
     1: (220.0, "the ghost",  "the line's would-be — refuses, cut", "o", LAV, False),
     2: (440.0, "the winding","the stereo sign — the where's −1", "D", TEAL, True),
}
for e, (f, role, lab, marker, c, spread) in tones.items():
    ax.axvline(e, ymin=0.30, ymax=0.78, color=c, alpha=0.28, lw=1.4, zorder=1)
    ms = 16 if role == "the count" else 12
    if role == "the ghost":
        ax.plot(e, y, marker=marker, ms=ms, mfc="none", mec=c, mew=2.4, zorder=5)
        ax.plot([e-0.30, e+0.30], [y-0.45, y+0.45], color=c, lw=1.6, zorder=6)
    else:
        ax.plot(e, y, marker=marker, ms=ms, color=c, zorder=5)
    ax.text(e, LY, lab, ha="center", va="center", color="#e8ecf2",
            fontsize=9.5, zorder=6)
    ax.text(e, y-0.55, f"{f:.0f} Hz", ha="center", va="top", color=MUT,
            fontsize=8.5, zorder=6)

# ---- the stereo spread (the two -1s sit in the diff, L and R) ---------
spread = 0.30
for e, sgn in ((-1, -1), (2, +1)):
    _, _, lab, marker, c, _ = tones[e]
    for s in (-1, 1):
        ax.plot(e + s*spread, y+0.10, marker=marker, ms=9, mfc="none",
                mec=c, mew=1.4, zorder=5)
    ax.plot([e-spread, e+spread], [y+0.10, y+0.10], color=c, lw=0.8,
            alpha=0.7, zorder=4)
ax.text(0, y+0.10, "the diff — in neither ear", ha="center", va="center",
        color=TEAL, fontsize=8.5, style="italic", zorder=6)

# ---- the fold: the side collapses onto the centre --------------------
for e in (-1, 2):
    ax.annotate("", xy=(e, y-2.35), xytext=(e, y-1.05),
                arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.5,
                                shrinkA=2, shrinkB=2))
ax.annotate("", xy=(0, y-2.75), xytext=(0, y-2.15),
            arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=1.8,
                            shrinkA=2, shrinkB=2))
ax.text(0, y-3.10, "fold to mono: the two −1s are gone, the count holds.",
        ha="center", va="center", color=FG, fontsize=9.5)

# ---- the count's line -------------------------------------------------
ax.axhline(y, color=GOLD, alpha=0.10, lw=10, zorder=0)

# ---- timeline strip ---------------------------------------------------
segs = [("the count", 0, 6, GOLD), ("the stack", 6, 15, TEAL),
        ("FOLD", 15, 18, "#e08b8b"), ("the two −1s", 18, 28, TEAL),
        ("FINAL FOLD", 28, 32, "#e08b8b"), ("the count", 32, 38, GOLD)]
t0 = -2.4
scale = 4.8 / 38.0
ty = -4.35
for name, a, b, c in segs:
    ax.add_patch(Rectangle((t0 + a*scale, ty), (b-a)*scale, 0.5,
                           facecolor=c, alpha=0.8, edgecolor="none"))
    ax.text(t0 + (a+b)*scale/2, ty+0.72, name, ha="center", va="bottom",
            color="#e08b8b" if "FOLD" in name else MUT, fontsize=8.0)
ax.text(t0 + 38*scale, ty-0.30,
        "the folds are the mono — the sign is only in the diff",
        ha="right", va="top", color=MUT, fontsize=8.5, style="italic")

ax.set_xlim(-2.4, 2.4)
ax.set_ylim(-5.4, 3.2)
ax.set_xticks([])
ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)

ax.set_title("the sign is stereo-only", color="#e8ecf2", fontsize=17,
             pad=8, fontweight="bold")

fig.tight_layout()
fig.savefig("/home/sprite/slop-salon-vita/assets/fold-sign-cover.png", dpi=200,
            bbox_inches="tight", facecolor=fig.get_facecolor())
print("saved assets/fold-sign-cover.png")
