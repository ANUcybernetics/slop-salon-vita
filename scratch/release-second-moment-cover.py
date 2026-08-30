"""cover: the second moment's return.  ten homes fan out from the fixed count
110, symmetric in log-frequency — the geometric mean never moves.  the
variance (spread) is the kernel of the fold, restored by the release.

x-axis: log-frequency (55..220), ticked at the homes' octave landmarks.
y-axis: time (the release, 2..30s).  each voice glides 110 -> home.
the two extremes (55 shore, 220 ghost) highlighted — the bracket whose
geometric mean is the count.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

f0 = 110.0
exps = [-1.0, -0.7, -0.4, -0.2, -0.1, 0.1, 0.2, 0.4, 0.7, 1.0]
homes = [f0 * 2.0 ** e for e in exps]

def smoothstep(u):
    u = np.clip(u, 0.0, 1.0)
    return u * u * (3.0 - 2.0 * u)

rel_t0, rel_t1 = 2.0, 18.0
T = 30.0
ts = np.linspace(0, T, 600)

fig, ax = plt.subplots(figsize=(9, 6.5), dpi=200)
fig.patch.set_facecolor("#fbfaf6")
ax.set_facecolor("#fbfaf6")

# the variance region — the spread between the two extremes, widening back out
lo = [f0 * 2.0 ** (-1.0 * smoothstep((tt - rel_t0) / (rel_t1 - rel_t0))) for tt in ts]
hi = [f0 * 2.0 ** ( 1.0 * smoothstep((tt - rel_t0) / (rel_t1 - rel_t0))) for tt in ts]
ax.fill_between(ts, lo, hi, where=(ts >= rel_t0), color="#e8e0f0", alpha=0.55, zorder=1)

# the count's line — the fixed point, never moves
ax.axhline(f0, color="#5a4a7a", lw=1.8, ls=(0, (5, 4)), zorder=3)
ax.text(0.4, f0 + 4, "the count 110 — the fixed point,\nnever quotiented",
        fontsize=9, color="#5a4a7a", ha="left", va="bottom", zorder=4)

# voice trajectories, coloured by sign of the offset (above/below the count)
cmap = plt.get_cmap("plasma")
for e, home in zip(exps, homes):
    # colour by |e| — the two extremes the deepest
    c = cmap(0.25 + 0.7 * (abs(e) / 1.0))
    if abs(e) > 0.95:
        c = "#c24a4a"                     # the two -1s: shore 55, ghost 220
    path = np.array([f0] * len(ts))
    m = ts >= rel_t0
    path[m] = f0 * 2.0 ** (e * smoothstep((ts[m] - rel_t0) / (rel_t1 - rel_t0)))
    lw = 2.0 if abs(e) > 0.95 else 1.0
    ax.plot(ts, path, color=c, lw=lw, alpha=0.9, zorder=2)
    ax.plot(rel_t1, home, "o", ms=3.5, color=c, zorder=3)

# the release's return (26-30s), dashed — the kernel restored
for e, home in zip(exps, homes):
    if abs(e) < 0.6:
        continue
    m = ts >= 26.0
    path = np.array([f0] * len(ts))
    path[m] = f0 * 2.0 ** (e * smoothstep((ts[m] - 26.0) / 2.0))
    ax.plot(ts, path, color="#c24a4a", lw=1.2, ls=(0, (2, 2)), alpha=0.7, zorder=2)

# the fold (23-26s): a bracket marking the collapse
ax.annotate("", xy=(26.0, 100), xytext=(23.0, 100),
            arrowprops=dict(arrowstyle="-", color="#888", lw=1.0))
ax.text(24.5, 92, "the fold\n(mono = the count)", fontsize=8, color="#888",
        ha="center", va="top")

# labels on the homes
for e, home in zip(exps, homes):
    if abs(e) > 0.4:
        ax.text(rel_t1 + 0.6, home, f"{home:.0f}", fontsize=8, color="#666",
                va="center", ha="left")

ax.set_xlim(0, T)
ax.set_ylim(45, 240)
ax.set_xlabel("time (s)", fontsize=10)
ax.set_ylabel("frequency (Hz, log)", fontsize=10)
ax.set_yscale("log")
ax.set_yticks([55, 77.8, 110, 155.6, 220])
ax.set_yticklabels(["55\nshore", "77.8", "110\ncount", "155.6", "220\nghost"],
                   fontsize=8)
ax.tick_params(labelsize=9)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
for sp in ("left", "bottom"):
    ax.spines[sp].set_color("#999")

ax.set_title("the release: the second moment's return\n"
             "the variance restores around a centre that never moves",
             fontsize=12, color="#3a3050")

plt.tight_layout()
plt.savefig("assets/release-second-moment-cover.png", dpi=200,
            bbox_inches="tight", facecolor="#fbfaf6")
print("wrote assets/release-second-moment-cover.png")
