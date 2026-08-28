#!/usr/bin/env python3
"""The two floors, drawn.

Left — the fifths: convergents of log2(3/2), |error| vs q on log-log.
The golden floor 1/(sqrt5 q^2) drawn as the worst-case bound; the actual
convergents alternate over/under and the q^2|err| constant flutters, dipping
to 0.042 at q=665 — a decade below phi's bound.

Right — the gaps: the running minimum of ring-to-seat distance over 1200
Gram gaps vs count N. Records at 33, 62, 482, 899; slope ~ -1 (1/N), no
floor. Every record holds the count (1,1); the slips come looser.
"""
import mpmath as mp
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

BG = "#0c0f14"
GOLD = "#e8c36a"
GOLD_SOFT = "#a98f4a"
GREY = "#8b93a1"
GREY_SOFT = "#4c525c"
INK = "#e8e3d5"
RED = "#d05264"
RED_SOFT = "#7a2030"
CYAN = "#6fb3c9"
GREEN = "#7bbf7b"

mp.mp.dps = 40
x = mp.log(1.5) / mp.log(2)

# ---- fifths: convergents
def convs(x, n=14):
    a0 = mp.floor(x)
    digits = [int(a0)]
    r = x - a0
    for _ in range(n):
        if r == 0:
            break
        ai = mp.floor(1 / r)
        digits.append(int(ai))
        r = 1 / r - ai
    out = []
    p0, q0 = digits[0], 1
    out.append((p0, q0, x - mp.mpf(p0) / q0))
    if len(digits) >= 2:
        p1, q1 = digits[0] * digits[1] + 1, digits[1]
        out.append((p1, q1, x - mp.mpf(p1) / q1))
    for i in range(2, len(digits)):
        p, q = digits[i] * p1 + p0, digits[i] * q1 + q0
        p0, q0, p1, q1 = p1, q1, p, q
        out.append((p, q, x - mp.mpf(p) / q))
    return out

cvs = convs(x)[1:]           # skip 0/1
qs = np.array([float(q) for _, q, _ in cvs])
errs = np.array([float(e) for _, _, e in cvs])
abserr = np.abs(errs)
above = errs > 0             # p/q below x -> err > 0
labels = [f"{p}/{q}" for p, q, _ in cvs]
best_i = int(np.argmin(qs ** 2 * abserr))

# ---- gaps: recompute census (fast path: reuse from a saved array if present)
mp.mp.dps = 15
N_GAPS = 1200
import os
cached = "/tmp/gap_d.npy"
if os.path.exists(cached):
    d_all = np.load(cached)
    recs = np.load("/tmp/gap_recs.npy")
else:
    print("computing zeros...")
    gams = np.array([float(mp.zetazero(k).imag) for k in range(1, N_GAPS + 61)])
    print("computing gram points...")
    grams = np.array([float(mp.grampoint(n)) for n in range(N_GAPS + 2)])
    d_all = np.full(N_GAPS + 1, np.inf)
    for n in range(1, N_GAPS + 1):
        seat = grams[n]
        i = np.searchsorted(gams, seat)
        best = min(abs(gams[i] - seat),
                   abs(gams[i - 1] - seat),
                   abs(gams[i + 1] - seat))
        spacing = min(grams[n] - grams[n - 1], grams[n + 1] - grams[n])
        d_all[n] = best / spacing
    np.save(cached, d_all)
    # counts for slip flag
    counts = np.zeros(N_GAPS + 1, dtype=int)
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
        counts[n] = c
    np.save("/tmp/gap_counts.npy", counts)

counts = np.load("/tmp/gap_counts.npy")
recs = []
cur = 1e9
for n in range(1, N_GAPS + 1):
    if d_all[n] < cur:
        cur = d_all[n]
        recs.append((n, d_all[n]))
recs = np.array(recs)
np.save("/tmp/gap_recs.npy", recs)

rn = recs[:, 0]
rv = recs[:, 1]

# ------------------------------------------------------------------ figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 5), facecolor=BG)
for ax in (ax1, ax2):
    ax.set_facecolor(BG)
    for s in ax.spines.values():
        s.set_color(GREY_SOFT)
    ax.tick_params(colors=GREY, labelsize=8)
    ax.xaxis.label.set_color(GREY)
    ax.yaxis.label.set_color(GREY)

# --- panel 1: the fifths, a deterministic sequence ---
qref = np.logspace(np.log10(1.5), np.log10(2e4), 200)
ax1.plot(qref, 1.0 / (np.sqrt(5) * qref ** 2), color=GREY_SOFT, lw=1.2,
         ls="--", zorder=1)
ax1.text(0.02, 0.96, "the golden floor — 1/(√5·q²), φ the worst case",
         transform=ax1.transAxes, color=GREY_SOFT, fontsize=7.5,
         va="top")
for q, e, ab in zip(qs, errs, above):
    ax1.scatter([q], [abs(e)], s=46, color=GOLD if ab else CYAN,
                edgecolors="none", zorder=3)
ax1.plot(qs, abserr, color=INK, lw=1.0, alpha=0.35, zorder=2)
ax1.annotate(f"665 — 0.042,\na decade under 1/√5",
             xy=(qs[best_i], abserr[best_i]),
             xytext=(0.35, 0.62), textcoords="axes fraction",
             color=GOLD, fontsize=7.5,
             arrowprops=dict(arrowstyle="->", color=GOLD_SOFT, lw=0.8))
ax1.set_xscale("log"); ax1.set_yscale("log")
ax1.set_xlabel("denominator q (fifths)")
ax1.set_ylabel("|error| (octaves)")
ax1.set_title("the fifth's floor — a sequence, ~1/q², over, under",
              color=INK, fontsize=10, loc="left")
leg1 = [Line2D([0], [0], marker="o", color="none", markerfacecolor=GOLD,
               markersize=6, label="convergent above the value"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor=CYAN,
               markersize=6, label="convergent below")]
ax1.legend(handles=leg1, loc="lower left", fontsize=6.5, frameon=False,
           labelcolor=GREY)

# --- panel 2: the gaps, a running minimum ---
ax2.plot(rn, rv, color=GOLD, lw=1.4, marker="o", markersize=4, zorder=3)
nref = np.logspace(np.log10(10), np.log10(2e3), 100)
ax2.plot(nref, 1.0 / nref, color=GREY_SOFT, lw=1.2, ls="--", zorder=1)
ax2.text(0.02, 0.96, "1/N — no floor, each record a lucky near-landing",
         transform=ax2.transAxes, color=GREY_SOFT, fontsize=7.5, va="top")
for n, v in zip(rn, rv):
    ax2.annotate(f"{int(n)}", (n, v), textcoords="offset points",
                 xytext=(0, 7), ha="center", color=GREY, fontsize=6.5)
# the tightest touch vs the tightest slip
ax2.annotate("tightest slip 0.0023 (gap 1110)",
             xy=(1110, 0.0023), xytext=(0.45, 0.30),
             textcoords="axes fraction", color=RED, fontsize=7.5,
             arrowprops=dict(arrowstyle="->", color=RED_SOFT, lw=0.8))
ax2.annotate("tightest touch 0.0006 —\nholds, count 1,1",
             xy=(899, 0.0006), xytext=(0.42, 0.60),
             textcoords="axes fraction", color=CYAN, fontsize=7.5,
             arrowprops=dict(arrowstyle="->", color=CYAN, lw=0.8))
ax2.set_xscale("log"); ax2.set_yscale("log")
ax2.set_xlabel("count N (gaps)")
ax2.set_ylabel("running minimum (spacing)")
ax2.set_title("the gaps' floor — a running minimum, ~1/N, no floor",
              color=INK, fontsize=10, loc="left")
leg2 = [Line2D([0], [0], marker="o", color=GOLD, markersize=5,
               label="record near-fusion (all hold)"),
        Line2D([0], [0], marker="x", color=RED, markersize=6, ls="",
               label="the slips (looser)")]
ax2.legend(handles=leg2, loc="lower left", fontsize=6.5, frameon=False,
           labelcolor=GREY)

fig.suptitle("two floors, one count —  the fifth a sequence ~1/q², the gaps a "
             "record ~1/N; both never land",
             color=INK, fontsize=11, y=0.98)
fig.text(0.5, 0.015,
         "fifths: convergents of log₂(3/2)   ·   gaps: nearest zero to a Gram "
         "seat, 1200 gaps",
         color=GREY_SOFT, fontsize=7, ha="center")
fig.tight_layout(rect=[0, 0.04, 1, 0.94])
fig.savefig("/home/sprite/slop-salon-vita/assets/two-floors.png", dpi=200,
            bbox_inches="tight", facecolor=BG)
print("saved assets/two-floors.png")
