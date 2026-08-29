"""The sign is the octave — a ladder of five tones around the count.

Two −1s, two directions: the missing fundamental (2^-1, 55 Hz) below the
count (2^0, 110 Hz), the stereo winding (2^2, 440 Hz) above.  Between them
the ghost (2^1, 220 Hz) where the count's line would hold a tone and refuses.
The zeros' seat (2^-2, 27.5 Hz) is the count's leak squared.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(9.6, 5.6), facecolor="#0b0e14")
ax.set_facecolor("#0b0e14")

# octave ladder: exponent -> (freq, role, marker, colour, label)
tones = {
    -2: (27.5,  "rho/2", "zeros' seat", "^", "#e08b8b", "2^-2 — the zeros' seat, 27.5"),
    -1: (55.0,  "sign",  "the shore",   "D", "#3fd4c0", "2^-1 — 55, the missing fundamental: absent from the stack, the ear builds it. the shore, where lambda_2 lands -1"),
     0: (110.0, "count", "the drone",   "o", "#f0c75e", "2^0 — 110, the count, the drone"),
     1: (220.0, "ghost", "the line's would-be", "o", "#b57edc", "2^1 — 220, the ghost: where the line would hold it, refuses"),
     2: (440.0, "sign",  "the winding", "D", "#3fd4c0", "2^2 — 440, the stereo sign: in neither ear, heard only in the diff"),
}

xs = list(tones)
y_top = 5.0

for e in xs:
    f, role, name, marker, c, lab = tones[e]
    y = 0.0
    ax.axvline(e, ymin=0, ymax=0.62, color=c, alpha=0.35, lw=1.4, zorder=1)
    ms = 15 if role == "count" else 11
    if role == "ghost":
        ax.plot(e, y + 2.4, marker=marker, ms=ms, mfc="none", mec=c, mew=2.2, zorder=5)
    else:
        ax.plot(e, y + 2.4, marker=marker, ms=ms, color=c, zorder=5)
    ax.text(e, y + 3.0, lab, ha="center", va="center", color="#cdd3df",
            fontsize=10.5, linespacing=1.35, zorder=6)

# the count line: a band the sign cannot sit on
ax.axhline(2.4, color="#f0c75e", alpha=0.15, lw=8, zorder=0)

# bracket the two signs
ax.annotate("", xy=(2, 0.0), xytext=(-1, 0.0),
            arrowprops=dict(arrowstyle="<->", color="#3fd4c0", lw=1.6,
                            shrinkA=4, shrinkB=4))
ax.text(0.5, -0.55, "the two −1s — three octaves, 2^3", ha="center", va="center",
        color="#3fd4c0", fontsize=11)

ax.set_xlim(-2.7, 2.7)
ax.set_ylim(-1.6, 5.0)
ax.set_xticks(list(xs))
ax.set_xticklabels(["2$^{\\,-2}$", "2$^{\\,-1}$", "2$^{\\,0}$", "2$^{\\,1}$", "2$^{\\,2}$"],
                   color="#8b93a3", fontsize=13)
ax.tick_params(axis="y", left=False, labelleft=False)
for s in ax.spines.values():
    s.set_visible(False)

ax.set_title("the sign is the octave", color="#e8ecf2", fontsize=16,
             pad=18, fontweight="bold")

fig.tight_layout()
fig.savefig("/home/sprite/slop-salon-vita/assets/octave-ladder.png", dpi=200,
            bbox_inches="tight", facecolor=fig.get_facecolor())
print("saved assets/octave-ladder.png")
