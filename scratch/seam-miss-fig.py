#!/usr/bin/env python3
"""the seam's miss: 165 = (110+220)/2, struck; tritone 110+45.56, never a quotient."""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DARK = "#0b0b0f"
AXIS = "#9a9aa5"
GOLD = "#e6b93f"
SEED = "#5b8def"
SEAM = "#ef5b6b"
TRIT = "#b07ce8"
WHITE = "#f0f0f2"

# data (verified at 30000 dps: all known records reproduced exactly)
SEAM_RUNG = 27378   # 1-indexed rung where 165 first struck
SEAM_COUNT = 1      # strikes in first 40000 rungs

toll = 110*(math.sqrt(2)-1)         # 45.5635
tritone = 110*math.sqrt(2)          # 155.5635
gap = 165 - tritone                 # 9.4365 = toll^2/220

fig = plt.figure(figsize=(11.5, 6.4), dpi=200)
fig.patch.set_facecolor(DARK)
ax = fig.add_axes([0.03, 0.10, 0.94, 0.60])
ax.set_facecolor(DARK)
ax.set_xlim(40, 240)
ax.set_ylim(0, 10)
ax.axis("off")

# --- ladder rungs ---
for v, c, lab in [(55, SEED, "seed 55"), (110, GOLD, "count 110"),
                  (220, GOLD, "ghost 220")]:
    ax.plot([v, v], [0.8, 8.6], color=c, lw=1.8, alpha=0.95, zorder=1)
    ax.text(v, 9.4, lab, color=c, ha="center", va="center", fontsize=13)

# --- tritone & seam dashed rungs ---
ax.plot([tritone, tritone], [0.8, 8.6], color=TRIT, lw=1.2, alpha=0.55, ls=":", zorder=1)
ax.plot([165, 165], [0.8, 8.6], color=SEAM, lw=1.2, alpha=0.55, ls=":", zorder=1)
ax.text(165, 8.9, "seam 165", color=SEAM, ha="center", va="center", fontsize=10.5)

# --- the struck seam point ---
ax.scatter([165], [4.4], s=120, color=SEAM, zorder=6, marker="D",
           edgecolor="white", linewidth=1.2)
ax.text(176, 4.4, "struck once at rung %d\n(one spike, then gone)" % SEAM_RUNG,
        color=SEAM, ha="left", va="center", fontsize=10.5, fontweight="bold")
ax.annotate("", xy=(169, 4.4), xytext=(165, 4.4),
            arrowprops=dict(arrowstyle="-", color=SEAM, lw=1))

# --- brackets ---
def bracket(x0, x1, y, label, c, dy=0.5, lsize=11):
    ax.annotate("", xy=(x0, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="-", color=c, lw=1.5))
    ax.plot([x0, x0], [y-dy, y+dy], color=c, lw=1.5)
    ax.plot([x1, x1], [y-dy, y+dy], color=c, lw=1.5)
    ax.text((x0+x1)/2, y-dy-0.35, label, color=c, ha="center", va="top", fontsize=lsize)

# miss brackets: 110 <-> 165 <-> 220  (miss 55 = the seed)
bracket(110, 165, 7.1, "miss 55 = the seed", SEED)
bracket(165, 220, 6.2, "miss 55", SEED)
# toll split: 110 -> 155.56 (+toll), 155.56 -> 165 (+toll^2/220)
bracket(110, tritone, 3.2, "the tritone 155.6:  +%.2f = the toll" % toll, TRIT)
bracket(tritone, 165, 2.3, "+%.2f = toll\u00b2/220" % gap, SEAM)

# --- bottom annotations (single block) ---
ax.text(140, 1.25, "165 = (110+220)/2  \u2014  integer, can be struck.   110\u221a2 = 110+toll  \u2014  irrational, never a quotient.",
        color=WHITE, ha="center", fontsize=11.5)
ax.text(140, 0.55, "seam \u2212 tritone = 55/\u03c3\u2082\u00b2 (seed over silver squared);   toll + toll\u00b2/220 = 55 exactly",
        color=AXIS, ha="center", fontsize=11)

# --- inset: the walk spike (neighbors of the 165 strike) ---
# verified: 165 first (and only) at 0-indexed 27377, 30000-dps run
spike_v = [9, 1, 4, 1, 16, 1, 2, 1, 1, 165, 1, 1, 48, 1, 19, 7, 4]

axin = fig.add_axes([0.60, 0.75, 0.37, 0.19])
axin.set_facecolor("#101018")
axin.bar(range(len(spike_v)), spike_v, color=[SEAM if v > 100 else "#3a3a46"
         for v in spike_v], width=0.85)
axin.set_xticks([9]); axin.set_xticklabels(["rung %d" % SEAM_RUNG], color=SEED, fontsize=9)
axin.set_yticks([])
axin.tick_params(axis="x", colors=SEED)
for s in ["top", "right"]:
    axin.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    axin.spines[s].set_color("#3a3a46")
axin.set_title("the seam's strike:  once, a lone spike", color=WHITE, fontsize=9.5, pad=6)

plt.savefig("/home/sprite/slop-salon-vita/assets/seam-miss.png", dpi=200,
            bbox_inches="tight", facecolor=DARK)
print("wrote assets/seam-miss.png")
