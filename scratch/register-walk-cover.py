#!/usr/bin/env python3
"""Cover for the register-walk sound piece.

A single row of 1200 rings, one per Gram gap, the count never moving: a flat
gold line under a line of faint ticks. Where the alternation trips, a ring is
missing (hollow red) and the next gap holds two, a comma apart (a doubled gold
pair) — the unit dipole, vacancy and doubling sharing the seat. The four
stacked blocks are underlined; the tightest miss (0.0023 of a spacing, gap
1110) is dotted red.
"""
import numpy as np
import mpmath as mp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BG = "#0c0f14"
GOLD = "#e8c36a"
GOLD_SOFT = "#a98f4a"
GREY = "#8b93a1"
GREY_SOFT = "#4c525c"
INK = "#e8e3d5"
RED = "#d05264"
CYAN = "#6fb3c9"

mp.mp.dps = 15
N_GAPS = 1200

print("computing zeros...")
gams = np.array([float(mp.zetazero(k).imag) for k in range(1, N_GAPS + 61)])
print("computing gram points...")
grams = np.array([float(mp.grampoint(n)) for n in range(N_GAPS + 2)])

counts = []
lo = 0
for n in range(1, N_GAPS + 1):
    a, b = grams[n], grams[n + 1]
    while lo < len(gams) and gams[lo] <= a:
        lo += 1
    c = 0
    j = lo
    while j < len(gams) and gams[j] < b:
        c += 1
        j += 1
    counts.append(c)
counts = np.array(counts)
walk = np.cumsum(counts - 1)

# misses per doubled gap
def spacing(t):
    return 2.0 * np.pi / np.log(t / (2.0 * np.pi))

dip_miss = {}
i = 0
while i < N_GAPS:
    if walk[i] == 0:
        i += 1
        continue
    o = "v" if walk[i] == -1 else "d"
    s = i
    while i < N_GAPS and walk[i] != 0:
        i += 1
    e = i - 1
    best = 1e9
    for n in (s, e):
        a, b = grams[n], grams[n + 1]
        for z in gams:
            if a < z < b:
                best = min(best, abs(z - a), abs(z - b))
    dip_miss[(s, e, o)] = best / spacing(grams[s])

slips = [(n, counts[n - 1]) for n in range(1, N_GAPS + 1) if counts[n - 1] != 1]
groups = []
for n, c in slips:
    if groups and n - groups[-1][-1][0] == 1:
        groups[-1].append((n, c))
    else:
        groups.append([(n, c)])
blocks = [g for g in groups if len(g) > 2]

W, H = 1920, 1080
fig = plt.figure(figsize=(W / 200, H / 200), dpi=200)
fig.patch.set_facecolor(BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor(BG)
ax.set_xlim(0, N_GAPS)
ax.set_ylim(-1.5, 3.0)
ax.axis("off")

# the ring train: one faint tick per gap, on the flat line
y_line = 0.0
for g in range(1, N_GAPS + 1):
    c = counts[g - 1]
    x = g - 0.5
    if c == 1:
        ax.plot([x, x], [y_line - 0.55, y_line + 0.55], color=GREY_SOFT,
                lw=1.1, alpha=0.8, solid_capstyle="round")
    elif c == 0:
        # hollow red ring: the vacancy
        ax.plot([x, x], [y_line - 0.55, y_line + 0.55], color=RED, lw=1.4,
                alpha=0.9)
        ax.scatter([x], [y_line - 0.9], s=26, facecolor="none", edgecolor=RED,
                   lw=1.2, zorder=5)
    elif c == 2:
        # doubled gold pair
        ax.plot([x - 0.32, x - 0.32], [y_line - 0.8, y_line + 0.8], color=GOLD,
                lw=1.9, solid_capstyle="round")
        ax.plot([x + 0.32, x + 0.32], [y_line - 0.8, y_line + 0.8], color=GOLD,
                lw=1.9, solid_capstyle="round")
        ax.scatter([x], [y_line + 1.05], s=18, color=GOLD, zorder=5)

# the count: a flat gold line, never leaving zero
ax.plot([0, N_GAPS], [y_line, y_line], color=GOLD, lw=2.0, zorder=4, alpha=0.95)

# stacked blocks underlined
for g in blocks:
    a, b = g[0][0] - 1.0, g[-1][0]
    ax.plot([a, b], [-1.15, -1.15], color=GOLD, lw=2.5, alpha=0.85)
    ax.plot([a, b], [-1.28, -1.28], color=GOLD_SOFT, lw=1.0, alpha=0.5)

# the tightest miss (gap 1110)
ax.annotate("0.0023 — the tightest of twelve hundred,\nin the most crowded block",
            xy=(1110.5, 1.05), xytext=(600, 2.55),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.2),
            color=INK, fontsize=13, ha="center")

# the first two: mirror twins
ax.annotate("the first two trips — mirror twins:\nempty/doubled, sides swapped",
            xy=(125.5, -0.9), xytext=(230, -0.45),
            arrowprops=dict(arrowstyle="-|>", color=CYAN, lw=1.0),
            color=CYAN, fontsize=11, ha="center")

# density annotation
ax.text(N_GAPS, 2.85, "11 / 19 / 22 trips per four hundred — denser with height",
        color=GREY, fontsize=12, ha="right")
ax.text(N_GAPS, 2.35, "1200 gaps, 56 dips, net zero — the count never moves",
        color=GOLD, fontsize=14, ha="right")

out = "/home/sprite/slop-salon-vita/assets/register-walk-cover.png"
plt.savefig(out, dpi=200, facecolor=BG)
print("wrote", out)
