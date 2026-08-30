#!/usr/bin/env python3
"""the exact wait — the landing is never an integer.

Left panel: for each near-miss convergent, the truncated wait a (open diamond,
the present) and the exact wait 1/(|x-p/q|·q²) (filled circle, the landing).
The vertical gap between them is the future+past share — every landing misses
the integer.  Right panel: the q=665 record decomposed — 23.8769 = 23 (present)
+ 0.4168 (future) + 306/665 (past) — the present swallowing the future.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from decimal import Decimal, getcontext

getcontext().prec = 80
alpha = (Decimal(3) / Decimal(2)).ln() / Decimal(2).ln()
ln2 = Decimal(2).ln()

# (q, p, next quotient a) for the seven near-misses
rows = [(2, 1, 2), (5, 3, 2), (12, 7, 3), (41, 24, 1),
        (53, 31, 5), (306, 179, 2), (665, 389, 23)]

qs = np.array([r[0] for r in rows])
a_trunc = np.array([r[2] for r in rows])
depths = []
for q, p, a in rows:
    diff = abs(alpha - Decimal(p) / Decimal(q))
    depths.append(float(Decimal(1) / (diff * Decimal(q) * Decimal(q))))
depths = np.array(depths)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(13.0, 6.4), dpi=200,
                               gridspec_kw={"width_ratios": [1.6, 1.0]})
for ax in (axL, axR):
    ax.set_facecolor("black")
    for s in ax.spines.values():
        s.set_color("#666")
    ax.tick_params(colors="#bbb")

fig.patch.set_facecolor("black")

# --- left: the seven waits, exact vs truncated ---
axL.set_yscale("log")
axL.scatter(qs, depths, s=52, color="#7fdfff", zorder=4, label="the landing (exact)")
axL.scatter(qs, a_trunc, s=40, marker="D", facecolors="none",
            edgecolors="gold", linewidths=1.3, zorder=4, label="the present (23 clicks)")
for q, d, a in zip(qs, depths, a_trunc):
    axL.plot([q, q], [a, d], color="#555", lw=1.0, zorder=1)
    if q == 665:
        axL.annotate(f"{d:.4f} = 23.8769",
                     (q, d), textcoords="offset points", xytext=(-4, -14),
                     fontsize=10, color="#7fdfff", ha="right")
        axL.annotate("future+past = 0.877",
                     (q, d), textcoords="offset points", xytext=(8, -6),
                     fontsize=9, color="#888")
axL.set_xscale("log")
axL.set_xticks(qs)
axL.set_xticklabels([f"{q}" for q in qs])
axL.set_xlabel("convergent q — the past deepens →", color="#ddd")
axL.set_ylabel("the wait, in steps", color="#ddd")
axL.set_title("every landing is non-integer", color="#eee", fontsize=12)
axL.legend(loc="lower right", fontsize=9, facecolor="#111", edgecolor="#333",
           labelcolor="#ddd")
axL.grid(True, which="both", color="#222", lw=0.4)

# --- right: the record decomposed ---
present, future, past = 23.0, 0.4168, 306 / 665
axR.barh(["past", "future", "present"], [past, future, present],
         color=["#9d6bff", "#ff9d6b", "#7fdfff"], edgecolor="none")
axR.set_xlim(0, 25)
axR.set_xticks([0, 5, 10, 15, 20, 23.8769])
axR.set_xticklabels(["0", "5", "10", "15", "20", "23.8769"], color="#ddd")
for y, val, lbl in zip([2, 1, 0], [past, future, present],
                       ["past\n306/665", "future\n0.4168", "present\n23"]):
    axR.text(val + 0.3, y, lbl, va="center", fontsize=9, color="#ddd")
axR.axvline(23.8769, color="#7fdfff", lw=1.2, ls=":")
axR.set_title("q=665: 23.8769 = 23 + 0.4168 + 306/665",
              color="#eee", fontsize=11)
axR.set_xlabel("steps", color="#ddd")
axR.grid(True, axis="x", color="#222", lw=0.4)

plt.tight_layout()
plt.savefig("assets/exact-wait.png", dpi=200, bbox_inches="tight", facecolor="black")
print("wrote assets/exact-wait.png")
