#!/usr/bin/env python3
"""the wait is the future — cover figure for the CF clock piece.

Left: the near-misses of the fifth, ||q·log2(3/2)|| in cents, descending in
mirror pairs toward the count (the horizontal line at 0 = 110 Hz).  The 665th
miss is +0.076 cents — fused with the count, the pair nearly closed.

Right: the same convergents, but their WAIT — the next quotient a_{n+1} in
time units.  665 sits because 23 follows: the deepest near-miss is followed by
the longest silence.  the miss is the future inverted: 0.076 ~ 1200/(23·665).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# q, signed miss in cents, next quotient a_{n+1}
rows = [
    (2,   +203.910, 2),
    (5,   -90.225,  2),
    (12,  +23.460,  3),
    (41,  -19.845,  1),
    (53,  +3.615,   5),
    (306, -1.770,   2),
    (665, +0.0756,  23),
]
T0 = 0.55
miss = np.array([r[1] for r in rows])
wait = np.array([r[2] for r in rows])
q = np.array([r[0] for r in rows])
labels = ["2", "5", "12", "41", "53", "306", "665"]

# symmetric log position: over above the line, under below
pos = np.sign(miss) * np.log10(np.abs(miss) + 1e-9)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(11, 4.6),
                               gridspec_kw={"width_ratios": [1.15, 1.0]})
fig.patch.set_facecolor("white")

# ------------------------------------------------------------------ left
axL.axhline(0, color="black", lw=1.6, zorder=2)
axL.axhline(0, color="#d4a017", lw=6, alpha=0.25, zorder=1)
cols = np.where(miss > 0, "#8b1a1a", "#1a3a6b")
for i in range(len(rows)):
    axL.plot(i, pos[i], "o", ms=11, color=cols[i], mec="black", mew=0.8, zorder=4)
    # connecting descent
    if i < len(rows) - 1:
        axL.plot([i, i + 1], [pos[i], pos[i + 1]], color="#999999", lw=1.0,
                 zorder=3, ls=":")
axL.set_ylim(-2.5, 2.5)
axL.set_yticks([-2, -1, 0, 1, 2])
axL.set_yticklabels(["1¢", "10¢", "count 0", "10¢", "100¢"])
axL.set_xticks(range(7))
axL.set_xticklabels([f"q={l}" for l in labels], fontsize=9)
for i, m in enumerate(miss):
    dy = 0.28 if m > 0 else -0.28
    axL.annotate(f"{m:+.2f}", (i, pos[i]), textcoords="offset points",
                 xytext=(0, 9 if m > 0 else -15), ha="center", fontsize=8.5,
                 color=cols[i])
axL.set_title("the misses descend to the count", fontsize=11)
axL.set_xlabel("convergents of log₂(3/2)", fontsize=9)

# ------------------------------------------------------------------ right
barcols = ["#8b1a1a" if m > 0 else "#1a3a6b" for m in miss]
axR.bar(range(7), wait, color=barcols, alpha=0.85, edgecolor="black", lw=0.8)
for i, w in enumerate(wait):
    axR.annotate(str(w), (i, w), textcoords="offset points", xytext=(0, 4),
                 ha="center", fontsize=10)
axR.set_ylim(0, 25)
axR.set_xticks(range(7))
axR.set_xticklabels(labels, fontsize=9)
axR.set_ylabel("the wait  a$_{n+1}$ · T₀", fontsize=10)
axR.set_title("the future is the wait", fontsize=11)
axR.axhline(23, color="#8b1a1a", ls="--", lw=0.8, alpha=0.5)

fig.suptitle("0.076 ≈ 1200/(23·665): the deepest miss is fused, and 23 follows — precision is patience",
             fontsize=11.5, y=0.99)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("assets/cf-clock-future-cover.png", dpi=200, bbox_inches="tight",
            facecolor="white")
print("wrote assets/cf-clock-future-cover.png")
