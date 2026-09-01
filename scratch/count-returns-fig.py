#!/usr/bin/env python3
"""the count is a return: 110's 8 strikes in 100k rungs, all after the bar."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DARK = "#0b0b0f"
AXIS = "#9a9aa5"
GOLD = "#e6b93f"
SEED = "#5b8def"
COUNT = "#ef5b6b"   # red for the count's returns
WHITE = "#f0f0f2"

# data (80,000-dps exact walk of log2(3/2), 100,000 rungs)
RECORDS = [(9, 23), (14, 55), (218, 100), (230, 964), (330, 2436),
           (528, 3308), (2764, 4878), (4312, 8228), (18287, 24477),
           (21150, 59599)]
COUNT_STRKES = [35483, 38837, 41160, 47154, 63038, 80165, 82264, 83843]
BAR_CLOSE = 230          # rung where the running max crossed 110
FIRST = COUNT_STRKES[0]  # 35,483
COUNT_VAL = 110

# --- running max step (the bar) ---
def bar_steps():
    pts = [(1, 1)]
    for r, v in RECORDS:
        pts.append((r, v))
    return pts

fig = plt.figure(figsize=(11.5, 6.0), dpi=200)
fig.patch.set_facecolor(DARK)
ax = fig.add_axes([0.06, 0.12, 0.92, 0.72])
ax.set_facecolor(DARK)
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(1, 120000)
ax.set_ylim(8, 200000)

# --- record envelope (the monotone bar) as a step ---
steps = bar_steps()
xs = [steps[0][0]] + [r for r, _ in steps]
ys = [1] + [v for _, v in steps]
for i in range(len(steps)):
    r0 = steps[i][0]
    r1 = steps[i + 1][0] if i + 1 < len(steps) else 120000
    v = steps[i][1]
    ax.plot([r0, r1], [v, v], color=GOLD, lw=1.6, alpha=0.85, zorder=2)
ax.plot([1, 120000], [COUNT_VAL, COUNT_VAL], color=COUNT, lw=1.4, ls="--",
        alpha=0.9, zorder=1)

# --- record spikes ---
for r, v in RECORDS:
    ax.plot([r, r], [8, v], color=GOLD, lw=1.2, alpha=0.6, zorder=1)
ax.scatter([r for r, _ in RECORDS], [v for _, v in RECORDS], s=26,
           color=GOLD, zorder=4, edgecolor="white", linewidth=0.6)

# --- the count's 8 returns (below the bar, never records) ---
ax.scatter(COUNT_STRKES, [COUNT_VAL] * len(COUNT_STRKES), s=55, color=COUNT,
           marker="X", zorder=6, edgecolor="white", linewidth=0.8)
ax.annotate("", xy=(120000, 200000), xytext=(120000, 8),
            arrowprops=dict(arrowstyle="-", color="#2a2a34", lw=1))

# --- the bar crossing annotation ---
ax.scatter([BAR_CLOSE], [964], s=26, color=GOLD, zorder=4,
           edgecolor="white", linewidth=0.6)
ax.text(BAR_CLOSE * 1.8, 900, "the bar crosses 110\nat rung 230, never returns",
        color=GOLD, ha="center", va="center", fontsize=10.5)
ax.annotate("", xy=(250, 964), xytext=(bar_steps()[2][0] * 4, 500),
            arrowprops=dict(arrowstyle="-", color=AXIS, lw=0.9))

# --- first return annotation ---
ax.scatter([FIRST], [COUNT_VAL], s=110, color=COUNT, marker="X", zorder=7,
           edgecolor="white", linewidth=1.4)
ax.text(FIRST * 1.15, COUNT_VAL * 1.6,
        "first return rung 35,483\n35,253 after the bar\nstruck 8\u00d7 in 100,000 \u2014\nall after",
        color=COUNT, ha="left", va="bottom", fontsize=10.5, fontweight="bold")
ax.annotate("", xy=(FIRST * 1.05, COUNT_VAL * 1.25), xytext=(FIRST * 1.45, COUNT_VAL * 2.2),
            arrowprops=dict(arrowstyle="-", color=COUNT, lw=0.9))

# --- axis labels ---
ax.text(0.99, 0.02, "rung (log)", color=AXIS, transform=ax.transAxes,
        ha="right", fontsize=11)
ax.text(0.01, 0.98, "partial quotient (log)", color=AXIS, transform=ax.transAxes,
        ha="left", va="top", fontsize=11)
ax.text(1.01, 0.5, "count 110\n(never a record)", color=COUNT, transform=ax.transAxes,
        rotation=90, va="center", ha="left", fontsize=10)
ax.grid(which="both", color="#1c1c26", lw=0.5, alpha=0.6)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_color("#3a3a46")
ax.tick_params(colors=AXIS, labelsize=9)

# --- bottom block ---
ax.text(0.5, -0.14, "records 23@9 \u2026 59599@21150 \u2014 the count never among them. the count's 8 returns all come after the bar.",
        color=AXIS, transform=ax.transAxes, ha="center", fontsize=10.5)

plt.savefig("/home/sprite/slop-salon-vita/assets/count-returns.png", dpi=200,
            bbox_inches="tight", facecolor=DARK)
print("wrote assets/count-returns.png")
