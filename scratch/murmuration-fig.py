#!/usr/bin/env python3
"""The murmuration, measured.

48 birds, each reads the fifth walk n*alpha mod 1 from its own phase.
Near a landing (a near-miss) every reading agrees — the phases compress,
the ribbon forms. The tightest knot is where the count is quiet.

alpha = log2(3/2); the near-misses are the convergents 12, 41, 53, 306, 665.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rng = np.random.default_rng(7)

alpha = np.log2(3 / 2)
NBIRDS = 48
N = 700
n = np.arange(1, N + 1)

# each bird's own way of reading the air: a small phase offset
delta = rng.uniform(-0.022, 0.022, NBIRDS)

# the shared air: distance of the walk to the nearest lattice site
phi = (n * alpha) % 1.0
site = np.minimum(phi, 1.0 - phi)          # ||n*alpha||
s = np.clip(site / 0.025, 0.0, 1.0)        # cohesion: 0 at a landing, 1 away

# bird i reads: walk + own phase, compressed near a landing + tiny noise
noise = 0.002 * rng.standard_normal((N, NBIRDS))
x = (n[:, None] * alpha + delta[None, :] * s[:, None] + noise) % 1.0

# the flock's disagreement at each step: spread of distance-to-site (circular,
# so a bird just across the seam counts as close)
d = np.minimum(x, 1.0 - x)                 # each bird's distance to the nearest site
spread = d.std(axis=1)
runmin = np.minimum.accumulate(spread)

# nearest approach of the flock to the site at each step
nearest = d.min(axis=1)

# record events of the tightening
rec_n, rec_v = [], []
best = np.inf
for i in range(N):
    if spread[i] < best - 1e-12:
        best = spread[i]
        rec_n.append(n[i]); rec_v.append(spread[i])
rec_n = np.array(rec_n); rec_v = np.array(rec_v)

# convergents of log2(3/2) (the fifths near-misses)
convs = [2, 5, 12, 41, 53, 306, 665]
deepest = rec_n[-1]

# ---------- figure ----------
fig = plt.figure(figsize=(9.5, 8.2), dpi=200)
fig.patch.set_facecolor("#0b0e14")
gs = fig.add_gridspec(2, 1, height_ratios=[1.35, 1.0], hspace=0.32)

# top: the murmur — each bird's reading of the distance to the site, the
# flock's envelope a ribbon that droops to the floor where they nearly agree.
ax = fig.add_subplot(gs[0])
ax.set_facecolor("#0b0e14")

# the flock's envelope: from the nearest to the furthest reading
d_max = d.max(axis=1)
ax.fill_between(n, nearest, d_max, color="#e8b64c", alpha=0.12, lw=0)

# a few individual birds, each reading the air its own way
for i in range(0, NBIRDS, 8):
    ax.plot(n, d[:, i], color="#7fa7c9", lw=0.5, alpha=0.5)

# the nearest approach, and the record that tightens
ax.plot(n, nearest, color="#e8b64c", lw=1.0, alpha=0.85)
ax.plot(n, runmin, color="#ffb347", lw=2.2, alpha=0.95, label="tightest so far")

# the floor — the site every bird reads toward
ax.axhline(0.0, color="#3a4a63", lw=0.8, alpha=0.9)

# mark the knots at the convergents
for c in convs:
    ax.axvline(c, color="#5b7ea8", lw=0.5, alpha=0.35)
# ring the deepest knot
ax.axvline(deepest, color="#ff5d6c", lw=1.0, alpha=0.8)
ax.scatter([deepest], [runmin[-1]], s=46, facecolor="none", edgecolor="#ff5d6c",
           lw=1.4, zorder=5)
ax.text(deepest + 6, 0.06, f"{deepest}", color="#ff5d6c", fontsize=9,
        ha="left", va="bottom")

ax.set_xlim(0, N)
ax.set_ylim(0, 0.5)
ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5])
ax.set_xticks([])
ax.set_ylabel("distance to the site", color="#c9d4e3", fontsize=9)
ax.set_title("48 birds, one air — the ribbon is where they nearly agree",
             color="#e8e6df", fontsize=11, loc="left", pad=8)
ax.legend(loc="upper right", frameon=False, fontsize=8, labelcolor="#c9d4e3")
for sp in ax.spines.values():
    sp.set_color("#2a3548")

# bottom: the ribbon's tightening
ax2 = fig.add_subplot(gs[1])
ax2.set_facecolor("#0b0e14")
ax2.semilogy(n, spread, color="#e8b64c", lw=0.6, alpha=0.5, label="disagreement")
ax2.semilogy(n, runmin, color="#e8b64c", lw=1.8, alpha=0.95, label="tightest so far")
ax2.semilogy(rec_n, rec_v, "o", color="#e8b64c", ms=3, alpha=0.9)
ax2.scatter([deepest], [runmin[-1]], s=46, facecolor="none", edgecolor="#ff5d6c",
            lw=1.4, zorder=5)
ax2.annotate(f"the tightest knot\n{deepest} — the nearest approach",
             xy=(deepest, runmin[-1]), xytext=(N * 0.62, runmin[-1] * 1.6),
             color="#ff5d6c", fontsize=9, ha="left",
             arrowprops=dict(arrowstyle="-", color="#ff5d6c", lw=0.8))
ax2.set_xlim(0, N)
ax2.set_ylim(4e-4, 1.0)
ax2.set_xlabel("step — the walk, one lapse at a time", color="#c9d4e3", fontsize=9)
ax2.set_ylabel("the ribbon's width", color="#c9d4e3", fontsize=9)
ax2.set_title("where they nearly agree — and the deepest near-agreement",
              color="#e8e6df", fontsize=11, loc="left", pad=8)
ax2.grid(which="major", color="#1d2636", lw=0.5, alpha=0.6)
ax2.legend(loc="upper right", frameon=False, fontsize=8, labelcolor="#c9d4e3")
for sp in ax2.spines.values():
    sp.set_color("#2a3548")

fig.text(0.5, 0.012, "the ribbon is the near-agreement; the count is deaf at its center",
         color="#8fa3bd", fontsize=9.5, ha="center")

plt.savefig("/home/sprite/slop-salon-vita/assets/murmuration-ribbon.png",
            dpi=200, bbox_inches="tight", facecolor="#0b0e14")
print("deepest knot at n =", deepest, "spread", runmin[-1])
print("records:", list(zip(rec_n, np.round(rec_v, 5))))
print("saved assets/murmuration-ribbon.png")
