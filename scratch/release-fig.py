"""the release, cover: forty-eight birds mid-flight, folding -> releasing.

Horizontal axis = the tonal ladder in octave units from the shore 55:
  0 = 55 (the shore, the sign's -1)
  1 = 110 (the count, the centre)
  2 = 220 (the ghost, never a seat)
  3 = 440 (the winding, the other -1)
Each bird has a home offset x_home (drawn clustered on the ladder seats) and
a release progress p in [0,1]: p=0 folded at the centre, p=1 home.  The
centre is the deck's fixed point: the one place no bird can leave, the one
value the whole ladder holds.  Draw a few arcs as the near-miss ribbon.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rng = np.random.default_rng(48)                     # the flock number
seats = np.array([0.0, 1.0, 2.0, 3.0])              # 55, 110, 220, 440

n_birds = 48
# home offsets: clustered on the ladder seats, with some drift (the flock
# is the stack made birds — a few sit exactly on each seat).
weights = np.array([0.15, 0.4, 0.3, 0.15])
home = rng.choice(len(seats), size=n_birds, p=weights) + rng.normal(0, 0.12, n_birds)
home = np.clip(home, 0.05, 2.95)
# release progress: the knot is letting go — most birds still near the
# centre, the outer ones already far toward home.
prog = rng.beta(1.6, 2.2, n_birds) ** 1.4
# position: folded centre -> home
x = 1.0 + (home - 1.0) * prog
y = rng.normal(0, 0.16, n_birds) * (0.35 + 0.65 * prog)   # the spread grows

fig, ax = plt.subplots(figsize=(9.6, 5.4), dpi=200)
fig.patch.set_facecolor("#0b0b12")
ax.set_facecolor("#0b0b12")

# the ladder: seats as vertical hairlines
seat_colors = {"55": "#7a6a9e", "110": "#e8d9a0", "220": "#6d8a9e", "440": "#9e6a7a"}
for sx, lab in zip(seats, ["55\nshore", "110\ncount", "220\nghost", "440\nwinding"]):
    ax.axvline(sx, color=seat_colors[lab.split()[0]], lw=0.5, alpha=0.35, ls=":")
    ax.text(sx, 1.42, lab, ha="center", fontsize=7, color=seat_colors[lab.split()[0]], alpha=0.9)

# the near-miss ribbon: a few release arcs from the centre to home
for hx in (0.1, 0.5, 1.5, 2.4, 2.9):
    a = np.linspace(0, 1, 40)
    rx = 1.0 + (hx - 1.0) * a
    ry = 0.5 * np.sin(np.pi * a) * np.sign(hx - 1.0) * 0.5
    ax.plot(rx, ry, color="#55607a", lw=0.6, alpha=0.4)

# the birds: size + alpha by release progress
sc = ax.scatter(x, y, s=6 + 10 * prog, c=prog, cmap="plasma",
                vmin=0, vmax=1, alpha=0.9, zorder=3, edgecolors="none")

# the count: the fixed point, ringed — the one seat with nowhere else to go
ax.scatter([1.0], [0.0], s=340, facecolors="none", edgecolors="#e8d9a0",
           linewidths=1.4, zorder=4)
ax.scatter([1.0], [0.0], s=46, color="#e8d9a0", zorder=5)

# the bracket: 55·220 = 110² — the two absences flanking the count
ax.annotate("", xy=(2.0, -1.30), xytext=(0.0, -1.30),
            arrowprops=dict(arrowstyle="<->", color="#8f8fb0", lw=0.9))
ax.text(1.0, -1.44, "√(55·220) = 110", ha="center", fontsize=8, color="#8f8fb0")

ax.set_xlim(-0.3, 3.3)
ax.set_ylim(-1.6, 1.5)
ax.set_xticks([])
ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
ax.text(-0.3, 1.5, "the release", fontsize=15, color="#d8d8e8", fontstyle="italic")
ax.text(-0.3, 1.30, "forty-eight birds drift back to their home offsets —\n"
                    "the centre never moves", fontsize=7, color="#a0a0b8")
ax.text(3.3, -1.6, "fold forgets which · release remembers which",
        ha="right", fontsize=7, color="#6d6d8a")

fig.tight_layout()
fig.savefig("assets/release-cover.png", dpi=200, bbox_inches="tight", facecolor="#0b0b12")
print("wrote assets/release-cover.png")
