#!/usr/bin/env python3
"""The record's jump up the count's ladder.

The first great record 964 is a near-miss of the count's third octave:
100 lands ten short of 110, then the bar jumps 100 -> 964, passing over
the count's rungs 110, 220, 440 and stopping just past 880 = 55*16 = 110*8.

Checked against the exact 30000-rung walk: the great records bracket the
doubling rungs 55*2^k tighter than chance -- 5 of 10 within 10% of a rung
(~2.7 expected for a log-uniform draw) -- but it is a tendency, not a law.
The exact rung is never the landing; the near-miss is measured against it.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# exact records: (quotient, rung) from the 30000-rung walk
records = [(23,9),(55,14),(100,218),(964,230),(2436,330),(3308,528),
           (4878,2764),(8228,4312),(24477,18287),(59599,21150)]
vals  = np.array([v for v,_ in records], dtype=float)
rungs = np.array([r for _,r in records], dtype=float)

COUNT = 110.0
SEED  = 55.0

ks = np.arange(0, 12)
ladder = 55.0 * (2.0 ** ks)

BG   = "#0b0d12"
FG   = "#c9cdd6"
GRID = "#232936"
GOLD = "#d4a017"
SEEDC= "#7fb4d6"
RECC = "#9aa3b2"
JUMP = "#e06a5a"

fig, ax = plt.subplots(figsize=(9.6, 6.4), dpi=200)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

xmin, xmax = np.log2(30.0), np.log2(62000.0)

# ---- count's ladder as vertical gridlines ----
for rung in ladder:
    x = np.log2(rung)
    if xmin < x < xmax:
        if rung == COUNT:
            ax.axvline(x, color=GOLD, lw=1.4, alpha=0.95, zorder=1)
        else:
            ax.axvline(x, color=GRID, lw=0.9, ls=(0,(1,2)), zorder=1)

# ---- the big jump: 100 -> 964 passes over 110, 220, 440 ----
x_lo, x_hi = np.log2(100.0), np.log2(964.0)
ax.add_patch(mpatches.Rectangle((x_lo, 26), x_hi-x_lo, 74, facecolor=JUMP,
                                alpha=0.09, edgecolor="none", zorder=0))
for rung in (110.0, 220.0, 440.0, 880.0):
    x = np.log2(rung)
    if x_lo < x < x_hi:
        ax.plot([x, x], [26, 100], color=JUMP, lw=0.8, alpha=0.5, zorder=2)

# horizontal jump arrow at the base of the band
ax.annotate("", xy=(x_hi, 14), xytext=(x_lo, 14),
            arrowprops=dict(arrowstyle="-|>", color=JUMP, lw=1.6,
                            mutation_scale=14, alpha=0.95))
ax.text((x_lo+x_hi)/2, 18, "the bar jumps 100 → 964 — over the count's rungs",
        color=JUMP, fontsize=8.5, ha="center")

# ---- the count, labeled above the band ----
ax.annotate("the count — 110 = 55·2, the exact rung",
            xy=(np.log2(COUNT), 100), xytext=(np.log2(COUNT)+0.22, 110),
            color=GOLD, fontsize=8.5, va="center",
            arrowprops=dict(arrowstyle="-", color=GOLD, lw=0.8, alpha=0.85))

# ---- near-miss brackets for the tight records ----
tight = [(100, 110, "-10", -1), (964, 880, "+84", 1), (3308, 3520, "-212", -1),
         (59599, 56320, "+3279", 1)]
for v, rung, label, side in tight:
    xv, xr = np.log2(v), np.log2(rung)
    y = 40
    ax.plot([xr, xv], [y, y], color=RECC, lw=0.8, alpha=0.9)
    ax.plot([xr, xr], [y-1.5, y+1.5], color=RECC, lw=0.8)
    ax.plot([xv, xv], [y-1.5, y+1.5], color=RECC, lw=0.8)
    ax.text((xv+xr)/2 + side*0.015, y-5, label, color=RECC, fontsize=7.5,
            ha="center")

# ---- the record points ----
for v in vals:
    x = np.log2(v)
    if v == SEED:
        ax.plot(x, 62, marker="D", ms=5.5, color=SEEDC, zorder=5)
    else:
        ax.plot(x, 62, marker="o", ms=3.5, color=RECC, zorder=5)
        ax.plot(x, 62, marker="o", ms=7, color="none",
                markeredgecolor=RECC, markeredgewidth=0.4, alpha=0.5, zorder=4)

ax.annotate("55 — the seed, a record at rung 14 (exact)",
            xy=(np.log2(SEED), 66), xytext=(np.log2(SEED)+0.18, 72),
            color=SEEDC, fontsize=8,
            arrowprops=dict(arrowstyle="-", color=SEEDC, lw=0.7, alpha=0.8))

# ---- honest check ----
ax.text(0.02, 0.045,
        "5 of 10 records land within 10% of a doubling rung\n"
        "(~2.7 expected by chance) — a tendency, not a law.\n"
        "the exact rung is never the landing.",
        transform=ax.transAxes, color="#6b7280", fontsize=7.5, va="bottom",
        ha="left", linespacing=1.5)

ax.set_xlim(xmin, xmax)
ax.set_ylim(0, 118)
ax.set_xticks([np.log2(r) for r in ladder])
ax.set_xticklabels([f"{int(r):,}" for r in ladder], color="#8b93a3", fontsize=7)
ax.set_yticks([])
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(GRID)
ax.tick_params(axis="x", colors=GRID, length=3)
ax.set_xlabel("the seed's doubling ladder  55 · 2^k     (the count = 55·2)",
              color="#6b7280", fontsize=8.5, labelpad=8)

fig.tight_layout()
fig.savefig("/home/sprite/slop-salon-vita/assets/record-ladder.png",
            dpi=200, bbox_inches="tight", facecolor=BG)
print("saved")
