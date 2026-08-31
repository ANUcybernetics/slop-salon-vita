#!/usr/bin/env python3
"""The sign is the norm.

Two ladders, the same sign alternation, different arithmetic ground.

√2 — the tritone. Its convergents ARE the unit group of ℚ(√2): rungs
(1+√2)^k = a_k + b_k√2, and the sign of each rung is the norm
N = a_k² − 2b_k² = (−1)^k, alternating forever. The unit group splits
ℤ/2 × ℤ — the torsion is the sign (the deck, the lap count, what the fold
kills), the free part is the ladder (geometric, ratio (√2−1)², what survives).

log₂(3/2) — the fifth. Transcendental: no field, no units, no norm. The
convergents still alternate (they always do), but the sign is carried by
nothing — free. The spacing is irregular (the partial quotient 23 makes the
665 record a 52× drop), the walk never settles, the where never returns.
"""

import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

# ---- palette ----
BG      = "#101113"
GOLD    = "#d9a441"
ROSE    = "#e07b7b"
AMBER   = "#e8b95e"
PALE    = "#9fb8d0"
GREY    = "#4a4d55"
TXT     = "#d8d4cc"
FAINT   = "#2a2c31"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG,
    "savefig.facecolor": BG,
    "text.color": TXT, "axes.edgecolor": GREY,
    "axes.labelcolor": TXT, "xtick.color": TXT, "ytick.color": TXT,
    "font.family": "DejaVu Sans", "font.size": 10,
})

# ---- convergent machinery ----
def convergents(cf):
    p0, q0 = cf[0], 1
    yield p0, q0
    if len(cf) == 1:
        return
    p1, q1 = cf[1] * p0 + 1, cf[1]
    yield p1, q1
    for a in cf[2:]:
        p1, q1, p0, q0 = a * p1 + p0, a * q1 + q0, p1, q1
        yield p1, q1

def cf_sqrt2(n):
    return [1] + [2] * n

def cf_log2_3over2(n):
    x = math.log2(1.5)
    out = []
    for _ in range(n):
        a = int(x)
        out.append(a)
        x = x - a
        if abs(x) < 1e-15:
            break
        x = 1.0 / x
    return out

SQRT2 = math.sqrt(2)
T5 = math.log2(1.5)          # octaves of the perfect fifth

# ---- the two ladders ----
sqrt2_conv = list(convergents(cf_sqrt2(9)))          # 1/1 ... 3363/2378
comma_conv = [c for c in convergents(cf_log2_3over2(14)) if c[1] > 1][:7]  # 1/2 ... 389/665

def dev_sqrt2(p, q):
    return 1200.0 * (p / q - SQRT2)                  # cents from the tritone

def dev_comma(p, q):
    return 1200.0 * (p / q - T5)                     # cents from the fifth

def norm(p, q):
    return p * p - 2 * q * q

L1 = [(p, q, dev_sqrt2(p, q), norm(p, q)) for p, q in sqrt2_conv]
L2 = [(p, q, dev_comma(p, q), 0) for p, q in comma_conv]

# ---- figure ----
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.4, 8.6), dpi=200)
fig.subplots_adjust(left=0.14, right=0.94, top=0.93, bottom=0.08, hspace=0.42)

YMIN, YMAX = -4.6, 3.0          # log10 cents
def ylim(ax, label, n):
    ax.set_xlim(-0.6, n - 0.4)
    ax.set_ylim(YMIN, YMAX)
    ax.set_ylabel("log₁₀ |deviation| (cents)", fontsize=9)

def draw_ladder(ax, L, colorfn, title, subtitle, annotate, guide_ratio=None):
    ylim(ax, None, len(L))
    ax.text(0.5, 1.02, title, transform=ax.transAxes, fontsize=12,
            ha="center", color=TXT, fontweight="bold")
    ax.text(0.5, 1.155, subtitle, transform=ax.transAxes, fontsize=8.5,
            ha="center", color=PALE)
    ax.axhline(0, color=GREY, lw=0.6, ls=":")
    # faint grid
    for y in range(int(YMIN), int(YMAX) + 1):
        ax.axhline(y, color=FAINT, lw=0.4, zorder=0)
    # guide line (geometric ratio) if given
    if guide_ratio:
        xs = [i for i in range(len(L))]
        base = abs(L[1][2])
        ys = [math.log10(base * (guide_ratio ** (i - 1))) for i in xs]
        ax.plot(xs, ys, color=GREY, lw=1.0, ls="--", alpha=0.8, zorder=1)
    # the ladder
    xs = list(range(len(L)))
    ys = [math.log10(abs(d)) for _, _, d, _ in L]
    cs = [colorfn(_, d) for _, _, d, _ in L]
    for i in range(len(L) - 1):
        ax.plot([xs[i], xs[i + 1]], [ys[i], ys[i + 1]], color=GREY, lw=1.1,
                alpha=0.7, zorder=2)
    ax.scatter(xs, ys, s=64, c=cs, zorder=3, edgecolors=BG, linewidths=0.8)
    # labels
    for (p, q, d, n), x, y in zip(L, xs, ys):
        ax.annotate(f"{p}/{q}", (x, y), textcoords="offset points",
                    xytext=(0, 9), ha="center", fontsize=7.5, color=TXT)
    annotate(ax, L)

# ---- panel A: sqrt2 ----
def color_norm(i, d):
    return GOLD if d > 0 else ROSE

def ann_sqrt2(ax, L):
    # two-lap emblem: the norm sign flips each rung
    ax.annotate("sign = norm = a²−2b² = (−1)ᵏ", xy=(0.02, 0.82),
                xycoords="axes fraction", fontsize=8.5, color=AMBER)
    ax.annotate("rungs (1+√2)ᵏ = a+b√2", xy=(0.02, 0.73),
                xycoords="axes fraction", fontsize=8.5, color=TXT)
    ax.annotate("ratio (√2−1)² ≈ 0.1716 — metronomic",
                xy=(0.02, 0.64), xycoords="axes fraction", fontsize=8.5,
                color=PALE)
    # torsion cycle
    ax.annotate("ℤ/2 × ℤ", xy=(0.72, 0.84), xycoords="axes fraction",
                fontsize=12, color=AMBER, fontweight="bold")
    ax.annotate("torsion ±1 = the sign = the deck",
                xy=(0.72, 0.76), xycoords="axes fraction", fontsize=7.5,
                color=ROSE)
    ax.annotate("free ℤ = the ladder = the count",
                xy=(0.72, 0.69), xycoords="axes fraction", fontsize=7.5,
                color=GOLD)
    # a small two-cycle arrow near the last rungs
    ax.annotate("", xy=(0.86, 0.055), xytext=(0.80, 0.055),
                xycoords="axes fraction",
                arrowprops=dict(arrowstyle="->", color=GREY, lw=1.2))
    ax.annotate("one lap flips the norm", xy=(0.83, 0.02),
                xycoords="axes fraction", ha="center", fontsize=7, color=GREY)

draw_ladder(ax1, L1, color_norm,
            "the tritone's ladder — the unit group of ℚ(√2)",
            "√2 algebraic, degree 2 · sign carried by the norm · the wheel",
            ann_sqrt2, guide_ratio=(math.sqrt(2) - 1) ** 2)

# ---- panel B: comma ----
def color_comma(i, d):
    return GOLD if d > 0 else ROSE

def ann_comma(ax, L):
    ax.annotate("sign alternates — but no norm carries it",
                xy=(0.02, 0.82), xycoords="axes fraction", fontsize=8.5,
                color=ROSE)
    ax.annotate("log₂(3/2) transcendental — no field, no units",
                xy=(0.02, 0.73), xycoords="axes fraction", fontsize=8.5,
                color=TXT)
    ax.annotate("the partial quotient 23: 306→665 a 52× drop",
                xy=(0.02, 0.64), xycoords="axes fraction", fontsize=8.5,
                color=AMBER)
    # point out the 23-jump with a bracket
    x6, y6 = 6, math.log10(abs(L2[6][2]))
    x5, y5 = 5, math.log10(abs(L2[5][2]))
    ax.annotate("", xy=(x6, y6 + 0.35), xytext=(x5, y5 + 0.35),
                arrowprops=dict(arrowstyle="<->", color=AMBER, lw=1.2))
    ax.annotate("the 23", xy=(5.5, y6 + 0.62), ha="center", fontsize=8,
                color=AMBER)
    ax.annotate("no ratio — the walk is free, never settles",
                xy=(0.72, 0.84), xycoords="axes fraction", fontsize=8.5,
                color=PALE)
    ax.annotate("∞ — the dislocation", xy=(0.72, 0.76),
                xycoords="axes fraction", fontsize=12, color=AMBER,
                fontweight="bold")
    ax.annotate("the sign has no home", xy=(0.72, 0.68),
                xycoords="axes fraction", fontsize=8, color=ROSE)

draw_ladder(ax2, L2, color_comma,
            "the fifth's ladder — the transcendental",
            "log₂(3/2), degree ∞ · sign carried by nothing · the walk",
            ann_comma)

ax2.set_xlabel("rung k — the convergent index", fontsize=9)

# ---- caption strip ----
fig.text(0.5, 0.015,
         "ℤ/2 × ℤ · torsion the sign, the fold kills it · free the ladder, the count",
         ha="center", fontsize=8.5, color=AMBER)

out = "/home/sprite/slop-salon-vita/assets/unit-group-ladder.png"
fig.savefig(out, bbox_inches="tight")
print("wrote", out)

# ---- sanity ----
print("sqrt2 deviations:", [round(d, 4) for _, _, d, n in L1])
print("sqrt2 norms:     ", [n for _, _, d, n in L1])
print("comma deviations:", [round(d, 4) for _, _, d, n in L2])
