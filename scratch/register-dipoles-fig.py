#!/usr/bin/env python3
"""The register walk as a row of unit dipoles.

Every slip is one ring crossing one seat: a vacancy and its doubling in the
two gaps on either side of the shared seat — the dipole has ZERO width, never
a gap between its members. The bound on the walk is not an accident; it is
what a slip is (a unit excursion 0 -> +-1 -> 0).

Four times two slips sit side by side (4-gap blocks d v v d / v d d v);
the tightest approach in 1200 gaps (miss 0.0023 of a spacing, gap 1110)
lives inside the last such stack.
"""
import mpmath as mp
import numpy as np
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
RED_SOFT = "#7a2030"
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

walk = np.concatenate(([0], np.cumsum(counts - 1)))
gi = np.arange(0, N_GAPS + 1)

# excursions (dipoles) in the walk
exc = []  # (start_gap, end_gap, orient)
i = 0
while i < N_GAPS:
    if walk[i] == 0:
        i += 1
        continue
    orient = "v" if walk[i] == -1 else "d"
    s = i
    while i < N_GAPS and walk[i] != 0:
        i += 1
    exc.append((s, i - 1, orient))  # walk[s-1]=0, walk[s..e]=+-1, walk[e+1]=0

# map each gap to its dipole for miss computation
gap_orient = {}
for s, e, o in exc:
    for g in range(s, e + 1):
        gap_orient[g] = (s, e, o)

# misses per dipole: min distance of a doubled ring to a gap wall
def spacing(t):
    return 2.0 * np.pi / np.log(t / (2.0 * np.pi))

dip_miss = {}
for s, e, o in exc:
    best = 1e9
    for n in (s, e):
        a, b = grams[n], grams[n + 1]
        for z in gams:
            if a < z < b:
                best = min(best, abs(z - a), abs(z - b))
    dip_miss[(s, e, o)] = best / spacing(grams[s])

# stacked blocks: 4-gap clusters
slips = [(n, counts[n - 1]) for n in range(1, N_GAPS + 1) if counts[n - 1] != 1]
groups = []
for n, c in slips:
    if groups and n - groups[-1][-1][0] == 1:
        groups[-1].append((n, c))
    else:
        groups.append([(n, c)])
blocks = [g for g in groups if len(g) > 2]
print(f"{len(exc)} dipoles | stacked blocks: {[[n for n,_ in g] for g in blocks]}")
for g in blocks:
    print("  counts:", [c for _, c in g])
orients = "".join(o for _, _, o in exc)
print(f"orientations: {orients}")
print(f"v {sum(1 for o in orients if o=='v')} d {sum(1 for o in orients if o=='d')}")
flips = sum(1 for i in range(1, len(orients)) if orients[i] != orients[i-1])
print(f"flips {flips}/{len(orients)-1}")

# ---------------- figure -------------------------------------------------
fig = plt.figure(figsize=(13.2, 9.6), dpi=200)
fig.patch.set_facecolor(BG)

# --- panel A: the walk, dipoles colored --------------------------------
axA = fig.add_axes([0.06, 0.71, 0.87, 0.24])
axA.set_facecolor(BG)
for sp in axA.spines.values():
    sp.set_visible(False)
axA.tick_params(colors=GREY, labelsize=8)
axA.set_xlim(0, N_GAPS)
axA.set_ylim(-2.1, 2.1)
# base walk in faint cyan
axA.plot(gi, walk, color=CYAN, lw=1.0, alpha=0.5, zorder=2)
# color each dipole excursion
for s, e, o in exc:
    col = RED if o == "v" else GOLD
    axA.plot(gi[s - 1:e + 2], walk[s - 1:e + 2], color=col, lw=1.7, zorder=3)
# stacked blocks shaded
for g in blocks:
    a, b = g[0][0] - 0.5, g[-1][0] + 0.5
    axA.axvspan(a, b, color=GOLD, alpha=0.08, lw=0)
axA.axhline(0, color=GREY_SOFT, lw=0.8, ls=(0, (3, 3)))
axA.axhline(1, color=GREY_SOFT, lw=0.5, ls=(0, (1, 3)), alpha=0.4)
axA.axhline(-1, color=GREY_SOFT, lw=0.5, ls=(0, (1, 3)), alpha=0.4)
axA.set_yticks([-1, 0, 1])
axA.set_ylabel("register walk", color=CYAN, fontsize=10)
axA.text(0, 1.9,
         "56 slips, each a ring crossing one seat — vacancy and doubling"
         " share the seat (zero width)", color=INK, fontsize=9.5)
axA.text(N_GAPS, 1.9,
         f"v {sum(1 for o in orients if o=='v')} / d "
         f"{sum(1 for o in orients if o=='d')}",
         color=INK, fontsize=9.5, ha="right")
axA.annotate("two slips, side by side —\nthe 4-gap blocks",
             xy=(379, -1), xytext=(470, -1.85),
             arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=1.0),
             color=GOLD, fontsize=9, ha="center")

# --- panel B: zoom on the tightest block, gaps 1106-1116 ----------------
axB = fig.add_axes([0.06, 0.40, 0.87, 0.26])
axB.set_facecolor(BG)
z0, z1 = 1105, 1117
# crystal cells
for n in range(z0, z1):
    a, b = grams[n], grams[n + 1]
    c = counts[n - 1]
    col = GREY_SOFT if c == 1 else (RED if c == 0 else GOLD)
    axB.add_patch(plt.Rectangle((n - z0, 0), 1, 1, color=col, lw=0.4,
                                ec=BG, alpha=0.92))
# rings as ticks
for n in range(z0, z1):
    a, b = grams[n], grams[n + 1]
    for z in gams:
        if a < z < b:
            axB.plot([n - z0 + 0.5, n - z0 + 0.5], [0.15, 0.85], color=BG,
                     lw=2.2)
            axB.plot([n - z0 + 0.5, n - z0 + 0.5], [0.3, 0.7], color=INK,
                     lw=1.4)
# gap labels
axB.set_xticks([n - z0 + 0.5 for n in range(z0, z1)])
axB.set_xticklabels([str(n) for n in range(z0, z1)], color=GREY, fontsize=6.5)
axB.tick_params(colors=GREY, labelsize=8, length=0)
for sp in axB.spines.values():
    sp.set_visible(False)
axB.set_ylim(0, 1)
axB.set_xlim(0, z1 - z0)
axB.set_yticks([])
# count annotations
for n in range(z0, z1):
    c = counts[n - 1]
    txt = str(c)
    axB.text(n - z0 + 0.5, -0.13, txt, color=GOLD if c == 2 else
             (RED if c == 0 else GREY_SOFT), fontsize=8.5, ha="center")
axB.text(z1 - z0, 1.25, "gaps 1106–1116: d v v d — two slips, two seats",
         color=INK, fontsize=9.5, ha="right")
# the tightest ring annotation
axB.annotate("the tightest ring in 1200 gaps\n0.0023 of a spacing from its seat g_1111",
             xy=(1110 - z0 + 0.5, 0.5), xytext=(3.2, 1.42),
             arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.0),
             color=RED, fontsize=8.5, ha="center")
axB.plot([6, 6], [0.08, 0.92], color=INK, lw=0.8, ls=(0, (2, 2)))
axB.text(6, 1.6, "g_1111", color=GREY, fontsize=7, ha="center")

# --- panel C: miss per dipole -------------------------------------------
axC = fig.add_axes([0.06, 0.07, 0.87, 0.26])
axC.set_facecolor(BG)
for sp in axC.spines.values():
    sp.set_visible(False)
axC.tick_params(colors=GREY, labelsize=8)
xs = []
ms = []
cols = []
for s, e, o in exc:
    xs.append(s)
    ms.append(dip_miss[(s, e, o)])
    # is this dipole in a stacked block?
    in_block = any(s in [n for n, _ in g] or e in [n for n, _ in g]
                   for g in blocks)
    cols.append(GOLD if in_block else RED)
xs = np.array(xs); ms = np.array(ms); cols = np.array(cols)
axC.plot([0, N_GAPS], [0, 0], color=RED_SOFT, lw=0.8, ls=(0, (4, 3)))
axC.scatter(xs, ms, s=24, color=cols, alpha=0.85, zorder=3, edgecolor="none")
mi = ms.argmin()
axC.scatter([xs[mi]], [ms[mi]], s=85, facecolor="none", edgecolor=INK,
            lw=1.2, zorder=4)
axC.set_xlim(0, N_GAPS)
axC.set_ylim(-0.01, max(ms) * 1.15)
axC.set_ylabel("miss / spacing", color=RED, fontsize=10)
axC.set_xlabel("trip site (gap n)", color=GREY, fontsize=9)
axC.text(N_GAPS, max(ms) * 1.08,
         "gold = a slip inside a stacked block — the tightest sits in one",
         color=GOLD, fontsize=9, ha="right")
axC.text(xs[mi] + 8, ms[mi] + 0.008, "0.0023", color=INK, fontsize=9)

out = "/home/sprite/slop-salon-vita/assets/register-dipoles.png"
plt.savefig(out, dpi=200, bbox_inches="tight", facecolor=BG)
print("wrote", out)
