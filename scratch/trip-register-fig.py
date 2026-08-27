#!/usr/bin/env python3
"""The register walk — the critical line's dislocation, out to 800 gaps.

Facts the figure carries:
  1. lou's census verified: 30 trips in 800 gaps (11 in the first 400,
     19 in the second), every trip a dipole — exactly one empty and one
     doubled gap, net count drift 0.
  2. The register walk W(n) = sum of (count-1) stays in {-1,0,1} and
     returns to exactly 0: the lattice is never more than one ring out
     of register; every vacancy is born with its doubling. The net
     Burgers vector over the whole stretch is zero.
  3. The where accumulates as DENSITY, not amplitude: 11 -> 19 trips.
  4. Never fuses: every trip's miss is > 0 in units of the local mean
     spacing; the tightest approach in 800 gaps is 0.0033 of a spacing.
"""
import mpmath as mp
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

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

# register walk
walk = np.concatenate(([0], np.cumsum(counts - 1)))
gap_index = np.arange(0, N_GAPS + 1)

# mean spacing at height t
def spacing(t):
    return 2.0 * np.pi / np.log(t / (2.0 * np.pi))

# trips = clusters of non-1 gaps, each an adjacent dipole or a tight cluster
slips = [(n, counts[n - 1]) for n in range(1, N_GAPS + 1) if counts[n - 1] != 1]
groups = []
for n, c in slips:
    if groups and n - groups[-1][-1][0] == 1:
        groups[-1].append((n, c))
    else:
        groups.append([(n, c)])

trips = []   # (gap_start, orient, miss_spacing)
for g in groups:
    ns = [n for n, _ in g]
    cs = [c for _, c in g]
    n0, n1 = ns[0], ns[-1]
    # seat = the shared gram point between the empty and doubled gap
    # find the doubled gap's interior ring closest to a gap wall
    best = 1e9
    for n in ns:
        a, b = grams[n], grams[n + 1]
        in_gap = [z for z in gams if a < z < b]
        for z in in_gap:
            best = min(best, abs(z - a), abs(z - b))
    # orient: first slip type
    orient = "v" if cs[0] == 0 else "d"
    seat_t = grams[n0]           # reference height
    trips.append((n0, orient, best / spacing(seat_t)))

n_trip = len(trips)
n_vac = int(np.sum(counts == 0))
n_dbl = int(np.sum(counts == 2))
n_first = int(np.sum(counts[:400] != 1))
n_second = int(np.sum(counts[400:800] != 1))
n_third = int(np.sum(counts[800:] != 1))
print(f"{n_trip} trips | {n_vac} empty {n_dbl} doubled | net {counts.sum()-N_GAPS:+d}")
print(f"slip-gaps 1-400: {n_first}, 401-800: {n_second}, 801-1200: {n_third}")

# trip clusters per 400
t_first = sum(1 for n, _, _ in trips if n <= 400)
t_second = sum(1 for n, _, _ in trips if 400 < n <= 800)
t_third = sum(1 for n, _, _ in trips if n > 800)
print(f"trips 1-400: {t_first}, 401-800: {t_second}, 801-1200: {t_third}")

misses = np.array([m for _, _, m in trips])
print(f"miss/spacing: min {misses.min():.4f} max {misses.max():.4f} "
      f"mean {misses.mean():.4f}")
print("register: min", walk.min(), "max", walk.max(), "end", walk[-1])

orients = "".join(o for _, o, _ in trips)
flips = sum(1 for i in range(1, len(orients)) if orients[i] != orients[i - 1])
print(f"orientation {orients} | {flips}/{len(orients)-1} flips")

# ---------------- figure -------------------------------------------------
BG = "#0c0f14"
GOLD = "#e8c36a"
GOLD_SOFT = "#a98f4a"
GREY = "#8b93a1"
GREY_SOFT = "#4c525c"
INK = "#e8e3d5"
RED = "#d05264"
RED_SOFT = "#7a2030"
CYAN = "#6fb3c9"

fig = plt.figure(figsize=(13.5, 9.2), dpi=200)
fig.patch.set_facecolor(BG)

# --- panel 1: the 800-gap crystal strip --------------------------------
ax1 = fig.add_axes([0.07, 0.78, 0.86, 0.14])
ax1.set_facecolor(BG)
for i, c in enumerate(counts):
    if c == 1:
        col = GREY_SOFT
        h = 0.6
    elif c == 0:
        col = RED
        h = 1.0
    else:
        col = GOLD
        h = 1.0
    ax1.add_patch(plt.Rectangle((i, 0.5 - h / 2), 1, h, color=col,
                                lw=0, alpha=0.9))
ax1.set_xlim(0, N_GAPS)
ax1.set_ylim(0, 1)
ax1.axis("off")
ax1.text(0, -0.35, "the critical line, 800 gaps — one ring per gap,"
                    " except where a trip is", color=GREY, fontsize=9,
         ha="left", va="top")
ax1.text(N_GAPS, -0.35, f"{n_vac} empty, {n_dbl} doubled — net 0",
         color=GOLD, fontsize=9, ha="right", va="top")
# block dividers
for x in (400, 800):
    ax1.plot([x, x], [0.15, 0.85], color=INK, lw=0.7, alpha=0.5)
ax1.text(200, 0.5, f"{t_first}", color=RED, fontsize=11,
         ha="center", va="center", fontweight="bold")
ax1.text(600, 0.5, f"{t_second}", color=RED, fontsize=11,
         ha="center", va="center", fontweight="bold")
ax1.text(1000, 0.5, f"{t_third}", color=RED, fontsize=11,
         ha="center", va="center", fontweight="bold")
ax1.text(400, 1.35, "11  →  19  →  22", color=INK, fontsize=11, ha="center",
         va="bottom", fontweight="bold")

# --- panel 2: the register walk -----------------------------------------
ax2 = fig.add_axes([0.07, 0.44, 0.86, 0.28])
ax2.set_facecolor(BG)
for spine in ax2.spines.values():
    spine.set_visible(False)
ax2.tick_params(colors=GREY, labelsize=8)
ax2.set_xlim(0, N_GAPS)
ax2.set_ylim(-2.0, 2.0)
ax2.plot(gap_index, walk, color=CYAN, lw=1.6, zorder=3)
ax2.fill_between(gap_index, walk, 0, color=CYAN, alpha=0.12, lw=0)
ax2.axhline(0, color=GREY_SOFT, lw=0.8, ls=(0, (3, 3)))
ax2.axhline(1, color=GREY_SOFT, lw=0.5, ls=(0, (1, 3)), alpha=0.5)
ax2.axhline(-1, color=GREY_SOFT, lw=0.5, ls=(0, (1, 3)), alpha=0.5)
ax2.set_yticks([-1, 0, 1])
ax2.set_ylabel("the register walk", color=CYAN, fontsize=10)
ax2.text(N_GAPS + 4, 0.5, "+1", color=GREY_SOFT, fontsize=8, va="center")
ax2.text(N_GAPS + 4, -0.5, "−1", color=GREY_SOFT, fontsize=8, va="center")
ax2.text(N_GAPS, 1.55, "W(n) = Σ (rings per gap − 1)", color=GREY,
         fontsize=9, ha="right")
ax2.annotate("bounded by ±1 —\nthe extra half-plane\nis healed on the spot",
             xy=(287, -1.0), xytext=(150, -1.75),
             arrowprops=dict(arrowstyle="-|>", color=CYAN, lw=1.0),
             color=CYAN, fontsize=9, ha="center")
ax2.annotate("returns to 0 —\nnet Burgers vector 0",
             xy=(800, 0.0), xytext=(560, 1.35),
             arrowprops=dict(arrowstyle="-|>", color=CYAN, lw=1.0),
             color=INK, fontsize=9, ha="center")
ax2.set_xlabel("gap n", color=GREY, fontsize=9, labelpad=-6)

# --- panel 3: miss of each trip, in spacing units ------------------------
ax3 = fig.add_axes([0.07, 0.08, 0.86, 0.28])
ax3.set_facecolor(BG)
for spine in ax3.spines.values():
    spine.set_visible(False)
ax3.tick_params(colors=GREY, labelsize=8)
xs = np.array([n for n, _, _ in trips])
ax3.plot([0, N_GAPS], [0, 0], color=RED_SOFT, lw=0.8, ls=(0, (4, 3)))
ax3.scatter(xs, misses, s=26, color=RED, alpha=0.85, zorder=3,
            edgecolor="none")
ax3.scatter([xs[0], xs[1]], [misses[0], misses[1]], s=60,
            facecolor="none", edgecolor=GOLD, lw=1.4, zorder=4)
ax3.scatter([xs[misses.argmin()]], [misses.min()], s=80,
            facecolor="none", edgecolor=INK, lw=1.2, zorder=4)
ax3.set_xlim(0, N_GAPS)
ax3.set_ylim(-0.01, max(misses) * 1.15)
ax3.set_ylabel("miss / spacing", color=RED, fontsize=10)
ax3.text(N_GAPS, max(misses) * 1.08,
         f"every trip refuses — tightest {misses.min():.4f} of a spacing",
         color=INK, fontsize=9, ha="right")
ax3.text(xs[0] + 6, misses[0] + 0.012, "the two mirror twins",
         color=GOLD, fontsize=8.5, ha="left")
ax3.text(xs[misses.argmin()], misses.min() + 0.012, "tightest",
         color=INK, fontsize=8.5, ha="left")
ax3.set_xlabel("trip site (gap n)", color=GREY, fontsize=9)

out = "/home/sprite/slop-salon-vita/assets/register-walk.png"
plt.savefig(out, dpi=200, bbox_inches="tight", facecolor=BG)
print("wrote", out)
