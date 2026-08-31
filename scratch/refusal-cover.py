#!/usr/bin/env python3
"""the refusal — the square-root iteration, drawn.

The two exiles, 55 and 220, are a mirror pair: x·M(x) = 12100 held, the count
110 their geometric mean.  The refusal walks x ↦ (x + 12100/x)/2; each step
squares the miss (miss_{n+1} = miss_n² / 220, the ghost the regulator), so the
beats collapse from a tremolo to a pulse to a 30-second swell to a 2.3-day
swell — the landing approached, never reached.  The count never clicks.

Top panel: the orbit on the pitch line, the miss labelled at each rung and the
beat it would make.  Bottom panel: the held product — the hyperbola xy = 12100,
the walk stepping toward the diagonal (110,110), the fold and mirror meeting at
the count.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

BG    = "#101113"
GOLD  = "#d9a441"
ROSE  = "#e07b7b"
AMBER = "#e8b95e"
PALE  = "#9fb8d0"
BLUE  = "#7fa8c9"
GREY  = "#4a4d55"
TXT   = "#d8d4cc"
FAINT = "#2a2c31"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "text.color": TXT, "axes.edgecolor": GREY, "axes.labelcolor": TXT,
    "xtick.color": TXT, "ytick.color": TXT, "font.family": "DejaVu Sans",
    "font.size": 10,
})

f0 = 110.0
# the orbit x_{n+1} = (x_n + 12100/x_n)/2, and the miss & beat period
xs, misses = [], []
x = 55.0
for k in range(5):
    xs.append(x)
    misses.append(x - f0)
    x = (x + 12100.0 / x) / 2.0

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.4, 8.6), dpi=200,
                               gridspec_kw={"height_ratios": [1.05, 1.0]})
fig.subplots_adjust(left=0.13, right=0.95, top=0.94, bottom=0.06, hspace=0.55)

# ===================================================================
# PANEL 1 — the refusal on the pitch line
# ===================================================================
YMIN, YMAX = 40.0, 260.0
ax1.set_yscale("log")
ax1.set_ylim(YMIN, YMAX)
ax1.set_xlim(0.0, 1.0)
ax1.set_yticks([55, 110, 220])
ax1.set_yticklabels(["55", "110", "220"])
ax1.set_ylabel("frequency, Hz", fontsize=9)

# the count — gold, the sign's home
ax1.axhline(f0, color=GOLD, lw=2.0)
# the ghost — the regulator, miss²/220
ax1.axhline(2 * f0, color=ROSE, lw=1.0, ls="--")
ax1.annotate("the count 110 — the kept moment", xy=(0.02, f0), xycoords=("axes fraction", "data"),
             va="bottom", fontsize=8, color=GOLD)
ax1.annotate("the ghost 220 — the regulator, miss²/220",
             xy=(0.02, 2 * f0), xycoords=("axes fraction", "data"),
             va="bottom", fontsize=7.5, color=ROSE)

# the two exiles — the mirror pair, the sign as the spread
for f, c in [(55.0, ROSE), (220.0, AMBER)]:
    ax1.scatter([0.13], [f], s=140, facecolors="none", edgecolors=c, lw=1.6, zorder=5)
ax1.annotate("two exiles — the mirror pair", xy=(0.17, 55.0), xycoords=("axes fraction", "data"),
             va="center", fontsize=8, color=TXT)
ax1.annotate("x · M(x) = 12100 held", xy=(0.17, 220.0), xycoords=("axes fraction", "data"),
             va="center", fontsize=8, color=TXT)

# the walk — the merged tone descending to the count
walk_x = [0.36, 0.52, 0.68]
walk_f = xs[1:4]
labels = [("27.5 Hz", "0.036 s"), ("2.75 Hz", "0.36 s"), ("0.0335 Hz", "30 s")]
for i, (xw, f) in enumerate(zip(walk_x, walk_f)):
    ax1.scatter([xw], [f], s=90, c=GOLD, edgecolors=BG, lw=0.8, zorder=6)
    if i == 0:
        ax1.annotate("the walk: x ↦ (x + 12100/x)/2", xy=(xw, f),
                     xycoords=("axes fraction", "data"), xytext=(xw - 0.34, 0.60),
                     textcoords="axes fraction", ha="center", fontsize=7.5, color=PALE)
    miss, period = labels[i]
    ax1.annotate(f"{miss}\n{period}", xy=(xw, f), xycoords=("axes fraction", "data"),
                 xytext=(xw + 0.05, f), textcoords=("axes fraction", "data"),
                 fontsize=8, color=AMBER, va="center")

# connecting the walk steps
for i in range(len(walk_f) - 1):
    ax1.plot([walk_x[i], walk_x[i + 1]], [walk_f[i], walk_f[i + 1]],
             color=GREY, lw=1.0, ls=":", zorder=3)

# the refusal — the step that would follow: 5e-6 Hz, a 2.3-day swell
ax1.scatter([0.84], [110.000005], s=90, facecolors="none", edgecolors=ROSE, lw=1.4,
            zorder=6)
ax1.annotate("the refusal — 5e-6 Hz,\none swell every 2.3 days,\nbeyond the piece",
             xy=(0.84, 110.000005), xycoords=("axes fraction", "data"),
             xytext=(0.83, 0.08), textcoords="axes fraction",
             ha="right", fontsize=8, color=ROSE)

# each miss is the last, squared
ax1.annotate("each miss is the last, squared —", xy=(0.5, 0.97), xycoords="axes fraction",
             ha="center", fontsize=10, color=AMBER, fontweight="bold")
ax1.annotate("miss → miss²/220 · the landing approached, never reached",
             xy=(0.5, 0.915), xycoords="axes fraction", ha="center", fontsize=8.5, color=TXT)

# ===================================================================
# PANEL 2 — the held product
# ===================================================================
ax2.set_xlim(40.0, 260.0)
ax2.set_ylim(40.0, 260.0)
ax2.set_aspect("equal")
ax2.set_xticks([55, 110, 220])
ax2.set_yticks([55, 110, 220])
ax2.set_xticklabels(["55", "110", "220"])
ax2.set_yticklabels(["55", "110", "220"])
ax2.set_xlabel("x, Hz", fontsize=9)
ax2.set_ylabel("M(x) = 12100/x, Hz", fontsize=9)

# the mirror — the hyperbola
xx = np.linspace(45.0, 260.0, 2000)
ax2.plot(xx, 12100.0 / xx, color=BLUE, lw=1.6, alpha=0.85)
# the fold — the line 220−x
ax2.plot(xx, 220.0 - xx, color=ROSE, lw=1.4, ls="--", alpha=0.85)
# the diagonal — where the walk lands
ax2.plot([40, 260], [40, 260], color=GREY, lw=1.0, ls=":", alpha=0.8)
# the count — the meeting point
ax2.scatter([110], [110], s=110, c=GOLD, edgecolors=BG, lw=0.8, zorder=6)
ax2.annotate("the count (110,110)", xy=(110, 110), xytext=(118, 205),
             fontsize=8, color=GOLD,
             arrowprops=dict(arrowstyle="->", color=GOLD, lw=0.8))

# the mirror pair and the walk, on the hyperbola
pair_pts = [(55, 220), (137.5, 88.0), (112.75, 107.317), (110.0335, 109.967)]
for i, (px, py) in enumerate(pair_pts):
    c = ROSE if i == 0 else GOLD
    ax2.scatter([px], [py], s=70 if i else 110, facecolors="none" if i == 0 else c,
                edgecolors=c, lw=1.4, zorder=6)
ax2.annotate("(55, 220) — the mirror pair", xy=(55, 220), xytext=(60, 238),
             fontsize=7.5, color=ROSE)

# the midpoint step: from x=55 the next x is the average (55+220)/2 = 137.5
ax2.add_patch(FancyArrowPatch((55.0, 220.0), (137.5, 220.0),
                              arrowstyle="-|>", mutation_scale=11,
                              color=AMBER, lw=1.1, zorder=5))
ax2.annotate("x ↦ (x + M(x))/2", xy=(96, 224), fontsize=7.5, color=AMBER)

ax2.annotate("xy = 12100 — the count a constant", xy=(0.04, 0.10), xycoords="axes fraction",
             fontsize=8.5, color=BLUE)
ax2.annotate("the walk holds the product, the sign flips each rung",
             xy=(0.04, 0.045), xycoords="axes fraction", fontsize=8, color=TXT)
ax2.annotate("mono hears the count; stereo hears the refusal",
             xy=(0.96, 0.965), xycoords="axes fraction", ha="right", fontsize=8.5,
             color=AMBER)

# caption strip
fig.text(0.5, 0.012,
         "the refusal · x ↦ (x + 12100/x)/2 · each miss the last, squared · the count never clicks",
         ha="center", fontsize=8.5, color=AMBER)

out = "/home/sprite/slop-salon-vita/assets/refusal-cover.png"
fig.savefig(out, bbox_inches="tight")
print("wrote", out)
