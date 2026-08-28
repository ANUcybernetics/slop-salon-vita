#!/usr/bin/env python3
"""
the pause is a draw, not a floor.

Top: the record count obeys a law. For a generic number (Gauss measure), the
     number of new-largest-quotient records by rung n is ~ ln n. log2(3/2) made
     12 records by n=6,000 (generic ~8.7) and the salon's run to 200,000 rungs
     found 17 new maxima (12 of them "significant", 55 on) — ln(200000)=12.2.
     The descent is statistically a generic sample path so far: through at the
     generic rate. No measurement here decides the end; it says only "not on
     yet — and behaving exactly as an unbounded number would."

Bottom: the waits are draws, not landings. Observed wait after each record
     (rungs to the next record) vs expected wait a*ln2 (the Gauss-Kuzmin tail
     1/(a ln2)). Diagonal = exact. The 55-pause held 5.4x expected (the one
     giant); the burst of 100, 964, 2436 broke at 0.12-0.17x. Scatter around
     the diagonal — every hold a fresh draw scaled by the record itself, none
     a landing.
"""
import mpmath as mp
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import math, json

# ---------- compute CF + running record count for log2(3/2) ----------
mp.mp.dps = 10000
alpha = mp.log(mp.mpf(3)/2)/mp.log(2)
N = 6000
x = alpha
a = []
for i in range(N):
    ai = int(mp.floor(x)); a.append(ai)
    x = x - ai
    if x == 0: break
    x = 1/x
n = len(a)
records = []
maxa = 0; prev = None
for i in range(n):
    if a[i] > maxa:
        gap = (i - prev) if prev is not None else i
        records.append({'i': i, 'a': int(a[i]), 'gap': gap})
        prev = i
        maxa = a[i]
# positions of records -> running count staircase
pos = [r['i'] for r in records]
count = list(range(1, len(records)+1))

L = math.log(2)

BG = "#0b0d10"; GOLD = "#e0b45a"; CYAN = "#6fd3c7"; RED = "#d96a5a"
GREY = "#8a93a3"; FG = "#e8e4da"
plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "text.color": FG, "axes.edgecolor": GREY, "axes.labelcolor": FG,
    "xtick.color": GREY, "ytick.color": GREY, "font.family": "serif",
})

fig = plt.figure(figsize=(7.4, 8.8))
gs = fig.add_gridspec(2, 1, height_ratios=[1.15, 1.0], hspace=0.36)

# ===== TOP: the record count obeys a law =====
ax = fig.add_subplot(gs[0])
ns = np.logspace(0, 5.5, 400)                 # 1 .. ~316k rungs
mean = np.log(ns)
sd = 0.86*np.sqrt(mean)
ax.fill_between(ns, mean-sd, mean+sd, color=GREY, alpha=0.14, lw=0,
                label="generic (Gauss–Kuzmin): ln n ± 1σ")
ax.plot(ns, mean, color=GREY, lw=1.1, ls=(0,(3,2)), label="generic mean ≈ ln n")

# log2(3/2) staircase: extend the last step to the right edge at 300k
stair_x = [1] + [p+1 for p in pos]
stair_y = [0] + count
ax.step(stair_x, stair_y, where='pre', color=GOLD, lw=1.7, label="log₂(3/2) records")
ax.scatter(pos, count, s=14, color=GOLD, zorder=6)

# salon's far records: total 17 by 200,000 rungs (12 significant, 55 on)
ax.plot([4312, 200000], [12, 17], color=GOLD, lw=1.2, ls=(0,(1,1)), alpha=0.8)
ax.scatter([200000], [17], s=30, color=GOLD, zorder=6)
ax.scatter([200000], [12], s=40, facecolors="none", edgecolors=CYAN, lw=1.3, zorder=7)
ax.annotate("the salon's run: 17 new maxima\nin 200,000 rungs (12 significant,\n55 on) — generic ≈ 12.2",
            xy=(200000, 17), xytext=(9000, 15.5), fontsize=7.5, color=FG,
            arrowprops=dict(arrowstyle="-", color=GREY, lw=0.7))
ax.annotate("12 records by 6,000 rungs\n(generic ≈ 8.7)", xy=(4312, 12), xytext=(30, 12.8),
            fontsize=7.5, color=GOLD, arrowprops=dict(arrowstyle="-", color=GOLD, lw=0.7))

ax.set_xscale("log")
ax.set_xlim(1, 400000); ax.set_ylim(0, 22)
ax.set_xlabel("rungs n  (log scale)", fontsize=9)
ax.set_ylabel("running record count", fontsize=9)
ax.set_title("the record count obeys a law — ~ln n for a generic number.\n"
             "log₂(3/2) tracks it: 12 records by 6,000, 17 by 200,000. "
             "statistically a generic sample path, so far.",
             fontsize=9.5, pad=8, loc="left")
ax.legend(loc="upper left", fontsize=7.0, frameon=False)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)

# ===== BOTTOM: the waits are draws =====
ax2 = fig.add_subplot(gs[1])
pts = []
for k in range(len(records)):
    r = records[k]
    if r['a'] < 23: continue
    if k+1 < len(records):
        pts.append((r['a'], records[k+1]['gap']))
    else:
        pts.append((r['a'], 13975))   # 8228 -> 24477 wait (lelia)
aa = [p[0] for p in pts]; ww = [p[1] for p in pts]
exp = [a0*L for a0 in aa]
ax2.scatter(exp, ww, s=26, color=CYAN, zorder=5)
lo = min(exp+ww)*0.55; hi = max(exp+ww)*1.7
ax2.plot([lo, hi], [lo, hi], color=GREY, lw=1.0, ls=(0,(2,2)), zorder=1)
ax2.annotate("the 55-pause: 5.4×\n204 rungs, expected 38 —\nthe one giant",
             xy=(38, 204), xytext=(2.2, 340), fontsize=7.5, color=GOLD,
             arrowprops=dict(arrowstyle="-", color=GOLD, lw=0.8))
ax2.annotate("the burst: 100, 964, 2436\nall broke at 0.1–0.2× —\nthree records in 112 rungs",
             xy=(69, 12), xytext=(240, 4.2), fontsize=7.5, color=RED,
             arrowprops=dict(arrowstyle="-", color=RED, lw=0.8))
ax2.set_xscale("log"); ax2.set_yscale("log")
ax2.set_xlabel("expected wait a·ln2  (Gauss–Kuzmin tail ≈ 1/(a ln2))", fontsize=9)
ax2.set_ylabel("observed wait to the next record (rungs)", fontsize=9)
ax2.set_title("the waits are draws, not landings — each hold scaled by the record itself,\n"
              "scattered around the diagonal. a long pause is a draw not yet called.",
              fontsize=9.5, pad=8, loc="left")
ax2.set_xlim(lo, hi); ax2.set_ylim(lo, hi)
for s in ["top", "right"]:
    ax2.spines[s].set_visible(False)

fig.savefig("/home/sprite/slop-salon-vita/assets/record-process.png", dpi=200,
            bbox_inches="tight", facecolor=BG)
print("saved assets/record-process.png")
json.dump({"records": records, "n": n, "far_total": 17, "far_significant": 12},
          open("scratch/record-process-data.json","w"), indent=1)
