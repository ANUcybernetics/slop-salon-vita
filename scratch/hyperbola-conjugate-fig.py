#!/usr/bin/env python3
"""the near-miss, conjugate — cover for hyperbola-conjugate.mp4.

log-log: x = |miss| (cents), y = wait (s).  Seven convergents, each on the
hyperbola miss·wait = 1200·T0/q (a −1-slope diagonal in log-log), the constant
descending as q climbs.  The points march toward the count's corner: pitch
silent, time long.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from decimal import Decimal, getcontext

getcontext().prec = 60
T0 = 0.55

alpha = (Decimal(3) / Decimal(2)).ln() / Decimal(2).ln()

def cf_digits(x, n):
    d, r = [], x
    for _ in range(n):
        ai = int(r); d.append(ai); r -= ai
        if r == 0: break
        r = Decimal(1) / r
    return d

digits = cf_digits(alpha, 12)
p0, q0 = Decimal(0), Decimal(1)
p1, q1 = Decimal(1), Decimal(0)
qs, miss, waits, consts = [], [], [], []
for i, ai in enumerate(digits):
    p2, q2 = ai * p1 + p0, ai * q1 + q0
    if q2 > 0:
        m = float(q2 * alpha - p2) * 1200
        a = digits[i + 1] if i + 1 < len(digits) else None
        if 2 <= q2 <= 665 and a is not None:
            qs.append(int(q2)); miss.append(abs(m)); waits.append(a * T0)
            consts.append(1200 * T0 / int(q2))
    p0, q0 = p1, q1
    p1, q1 = p2, q2

fig, ax = plt.subplots(figsize=(9.5, 7.0), dpi=200)
fig.patch.set_facecolor("black")
ax.set_facecolor("black")
for s in ax.spines.values():
    s.set_color("#666")

x = np.array(miss); y = np.array(waits)

# the hyperbolas (diagonals in log-log) through each point
for xi, yi, c in zip(x, y, consts):
    xs = np.logspace(np.log10(xi) - 1.4, np.log10(xi) + 0.4, 100)
    ys = c / xs
    ax.loglog(xs, ys, color="#334", lw=0.8, zorder=1)

# the points, connected
ax.loglog(x, y, "-", color="#555", lw=1.0, zorder=2)
sc = ax.scatter(x, y, s=42, c=range(len(qs)), cmap="plasma", zorder=3)
for q, xi, yi in zip(qs, x, y):
    ax.annotate(f"q={q}", (xi, yi),
                textcoords="offset points", xytext=(6, 6),
                fontsize=9, color="#ddd")

# the corner: the count
ax.annotate("", xy=(0.055, 30), xytext=(0.07, 2.6),
            arrowprops=dict(arrowstyle="->", color="gold", lw=1.4))
ax.text(0.052, 34, "the count\npitch silent · time long",
        color="gold", fontsize=10, ha="center", va="bottom")

# the deep miss, the farthest corner point
ax.annotate("23 · T0", (x[-1], y[-1]),
            textcoords="offset points", xytext=(8, -22),
            fontsize=10, color="#7fdfff")
ax.annotate("0.076¢", (x[-1], y[-1]),
            textcoords="offset points", xytext=(8, -36),
            fontsize=10, color="#7fdfff")

ax.set_xlabel("|miss| — cents (the near-miss, as pitch)", color="#ddd")
ax.set_ylabel("wait = a·T0 — seconds (the future, as time)", color="#ddd")
ax.set_title("the near-miss, conjugate — miss·wait ≈ 1200·T0/q",
             color="#eee", fontsize=12)
ax.tick_params(colors="#bbb")
ax.grid(True, which="both", color="#222", lw=0.4)

plt.tight_layout()
plt.savefig("assets/hyperbola-conjugate-cover.png", dpi=200,
            bbox_inches="tight", facecolor="black")
print("wrote assets/hyperbola-conjugate-cover.png")
