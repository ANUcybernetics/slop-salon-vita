"""cover for the tritone band — the osculating circle, read as the loop the
sound orbits.  the circle centred on the ghost (220,220), radius √(110·220) =
110√2 = 600¢, passes through the kiss (110,110); the orbiting tone climbs from
the count to the ghost's level and back, through the tritone — the radius as a
pitch.  the GM ladder sits on the diagonal, the tritone halving the octave.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch

fig, ax = plt.subplots(figsize=(8.4, 8.4), dpi=200)
fig.patch.set_facecolor("#0d0d11")
ax.set_facecolor("#0d0d11")

x = np.linspace(30, 430, 1000)

# the fold line 220 - x (gold) and the mirror 12100/x (amber)
ax.plot(x, 220.0 - x, color="#d9a13b", lw=2.2, alpha=0.85, zorder=2)
ax.plot(x, 12100.0 / x, color="#e0b34c", lw=2.2, alpha=0.85, zorder=2)

# the osculating circle: centre the ghost (220,220), radius sqrt(110*220)
r = np.sqrt(110.0 * 220.0)
ghost = (220.0, 220.0)
circle = Circle(ghost, r, fill=False, lw=2.6, ls=(0, (5, 3)),
                edgecolor="#e0655f", alpha=0.95, zorder=3)
ax.add_patch(circle)

# the orbit the sound traces: the count's range 110 -> 220, which on the
# circle is the two arcs where y lies between the kiss and the ghost's level
# (the lower-left arc, and the lower-right arc) — the deep bottom is unvisited.
for a0, a1 in [(np.pi, 5 * np.pi / 4), (7 * np.pi / 4, 2 * np.pi)]:
    th = np.linspace(a0, a1, 200)
    ox = 220 + r * np.cos(th)
    oy = 220 + r * np.sin(th)
    ax.plot(ox, oy, color="#f0f0ea", lw=3.2, alpha=0.98, zorder=4,
            solid_capstyle="round")

# the visited points on the orbit
pts = {
    (110.0, 110.0): ("the kiss, 110", "#f0c95a", 9, 4),        # the count
    (78.4, 155.6):  ("the radius, 155.6 = 600¢", "#e0655f", 6, 3),
    (361.6, 155.6): (None, "#e0655f", 6, 3),
    (64.4, 220.0):  (None, "#e0b34c", 6, 3),
    (375.6, 220.0): (None, "#e0b34c", 6, 3),
    (330.0, 110.0): (None, "#f0c95a", 6, 3),
}
for (px, py), (label, c, s, z) in pts.items():
    ax.scatter([px], [py], s=s**2 * 22, color=c, edgecolors="none", zorder=6)
    if label:
        ax.annotate(label, (px, py), textcoords="offset points",
                    xytext=(12, 6), color=c, fontsize=10, zorder=7)

# the ghost centre
ax.scatter([220], [220], marker="o", s=150, facecolor="none",
           edgecolor="#8a8aa0", lw=1.8, zorder=5)
ax.annotate("the ghost, (220,220)", (220, 220), textcoords="offset points",
            xytext=(12, -22), color="#8a8aa0", fontsize=10)

# the radius spoke ghost -> kiss, labelled the tritone
ax.plot([220, 110], [220, 110], color="#e0655f", lw=1.4, alpha=0.7,
        ls=(0, (2, 2)), zorder=3)
ax.annotate("radius = √(110·220) = 110√2 = 600¢",
            (165, 165), textcoords="offset points", xytext=(18, 4),
            color="#e0655f", fontsize=10.5)

# the GM ladder on the diagonal: 55, 110, 220, 440, each the mean of its
# neighbours; the tritone 110√2 halving the octave.
for f in [55.0, 110.0, 220.0, 440.0]:
    ax.scatter([f], [f], s=40, color="#c9c9d6", edgecolors="none", alpha=0.7, zorder=4)
    ax.annotate(f"{f:g}", (f, f), textcoords="offset points",
                xytext=(-8, -16), color="#c9c9d6", fontsize=9, alpha=0.8)
tt = 110.0 * np.sqrt(2.0)
ax.scatter([tt], [tt], s=55, color="#e0655f", edgecolors="none", zorder=5)
ax.annotate("110√2", (tt, tt), textcoords="offset points", xytext=(-2, -24),
            color="#e0655f", fontsize=10)

ax.plot([55, 440], [55, 440], color="#c9c9d6", lw=0.8, alpha=0.35, zorder=1)

ax.set_xlim(30, 430)
ax.set_ylim(30, 430)
ax.set_aspect("equal")
ax.set_xlabel("the where, x  (Hz)", color="#9a9ab0", fontsize=11)
ax.set_ylabel("the reading, y  (Hz)", color="#9a9ab0", fontsize=11)
ax.tick_params(colors="#6d6d85")
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_color("#3a3a4c")

ax.set_title("the tritone band — the osculating circle, heard",
             color="#e8e8f0", fontsize=13, pad=14)

fig.tight_layout()
fig.savefig("assets/tritone-band-cover.png", facecolor=fig.get_facecolor(),
            bbox_inches="tight")
print("wrote assets/tritone-band-cover.png")
