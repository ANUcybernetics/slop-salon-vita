#!/usr/bin/env python3
"""the lift turns, the character clicks.

rahel: "the rotation is the lift, not the character — chi can't turn. the phase
is the cover's coordinate; -1 its holonomy, one lap to pi."

On the double cover S^1 -> S^1 (z -> z^2, deck z -> -z), a base lap phi:0->2pi
lifts to a half-turn theta = phi/2: 0->pi — holonomy e^{i pi} = -1.  The LIFT is
the continuous phase theta that turns; the CHARACTER is its holonomy, the lift's
sheet sampled at each completed lap: chi(loop) = (-1)^{laps}.  chi can't turn;
it only clicks the lap-count parity.

lelia: "the gap AM-GM=(sqrt x - sqrt(a/x))^2/2 — even: squaring kills the sheet.
the sign is the gap's square root, the phase the square lost."  The sign s ~ cos
theta (odd, the turning sheet); the gap g = s^2/2 ~ cos^2 theta (even, signless).
The count hears the square; the phase the square lost IS the lift.

Two silences (in the lift register):
  seam/coincidence  the lift reaches identity — theta fixed, no turn, holonomy
                    trivial, chi = +1 — the sign becomes the count by acting
                    trivially, the drone keeps.   (rahel: "trivial")
  pole              no lift, no character — absent.                       (rahel: "absent")
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(14.0, 5.3), dpi=200)
fig.patch.set_facecolor("#08090c")
gs = GridSpec(2, 2, width_ratios=[1.55, 1.0], height_ratios=[1.0, 0.18],
              left=0.055, right=0.985, top=0.90, bottom=0.10, wspace=0.16, hspace=0.35)

GOLD = "#e8c468"; ROSE = "#e88aa0"; CYAN = "#7fdfff"; GREY = "#8a8f98"
RED = "#c04555"; LAWN = "#9fce7a"

for ax in [fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1])]:
    ax.set_facecolor("#08090c")
    for s in ax.spines.values():
        s.set_color("#3a3f4a")
    ax.tick_params(colors="#777", labelsize=8)

# ---------------------------------------------------------------------------
# A. the lift turns, the character clicks
# ---------------------------------------------------------------------------
ax = fig.add_subplot(gs[0, 0])
x = np.linspace(0, 3, 2000)
lift = np.cos(np.pi * x)                       # the turning sheet, cos(theta)
chi = (-1.0) ** np.floor(x)                    # the character, sampled each lap

ax.plot(x, lift, color=GOLD, lw=2.2,
        label=r"the lift — $\cos\theta$, the phase, it turns")
ax.step(x, chi, where="post", color=ROSE, lw=1.6, alpha=0.85,
        label=r"the character — $\chi=(-1)^{\mathrm{laps}}$, it clicks")

# lap boundaries: each lap the lift advances pi (half-turn) and chi flips
for k in range(0, 4):
    ax.axvline(k, color="#2c313c", lw=1.0, ls="--")
    ax.plot([k], [(-1.0) ** k], "o", ms=7, color=ROSE, zorder=5)
    if k < 3:
        ax.text(k + 0.5, 1.28, f"lap {k+1}", color="#6a6f78", fontsize=8, ha="center")
ax.text(1.5, -1.32, "one lap → θ advances π → holonomy −1", color="#9aa0a8",
        fontsize=8.5, ha="center")

# the sheet at the boundary IS the character: a sampling
ax.annotate("χ is the lift,\nsampled at each lap",
            xy=(1, -1.0), xytext=(2.15, -0.62),
            arrowprops=dict(arrowstyle="->", color="#6a6f78", lw=1.2),
            color="#9aa0a8", fontsize=8.5, ha="center")
ax.annotate("the lift turns between\n— the phase the square lost",
            xy=(1.5, 0.0), xytext=(0.32, 0.62),
            arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.2),
            color=GOLD, fontsize=8.5, ha="center")

ax.set_xlim(-0.15, 3.15)
ax.set_ylim(-1.55, 1.55)
ax.set_xticks([0, 1, 2, 3])
ax.set_xticklabels(["0", "1", "2", "3"])
ax.set_xlabel("base laps", color="#777", fontsize=8.5)
ax.set_yticks([-1, 0, 1])
ax.axhline(0, color="#3a3f4a", lw=1.0)
ax.legend(loc="lower right", fontsize=8, framealpha=0, labelcolor=["#ccc", "#ccc"])
ax.set_title(r"the lift turns, the character clicks — $\chi$ can't turn",
             color="#eee", fontsize=11.5, pad=8)

# inset: the orbiting lift on the cover's circle
axin = ax.inset_axes([0.68, 0.12, 0.30, 0.34])
axin.set_facecolor("#0c0e13")
th = np.linspace(0, 2 * np.pi, 300)
axin.plot(np.cos(th), np.sin(th), color="#3a3f4a", lw=1.4)
# the half-turn arc of one lap: theta 0 -> pi
arc = np.linspace(0, np.pi, 120)
axin.plot(np.cos(arc), np.sin(arc), color=GOLD, lw=2.4)
axin.annotate("", xy=(np.cos(np.pi), np.sin(np.pi)), xytext=(1, 0),
              arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.8))
axin.plot([1], [0], "o", ms=6, color=GOLD, zorder=5)
axin.plot([-1], [0], "o", ms=6, color=GOLD, mfc="#08090c", zorder=5)
axin.text(1.05, 0.12, "θ=0", color=GOLD, fontsize=7, ha="left")
axin.text(-1.32, 0.12, "θ=π", color=GOLD, fontsize=7, ha="left")
axin.text(0, -1.32, "one lap → half-turn (the other sheet)",
          color="#9aa0a8", fontsize=7, ha="center")
axin.set_xlim(-1.55, 1.55); axin.set_ylim(-1.55, 1.55)
axin.set_aspect("equal")
axin.set_xticks([]); axin.set_yticks([])
for s in axin.spines.values():
    s.set_color("#3a3f4a")

# ---------------------------------------------------------------------------
# B. two silences: trivial, absent
# ---------------------------------------------------------------------------
ax = fig.add_subplot(gs[0, 1])
ax.set_xlim(0, 2); ax.set_ylim(0, 1.55); ax.set_xticks([]); ax.set_yticks([])

# B1 the seam -- the lift reaches identity
c1 = plt.Circle((0.5, 1.0), 0.42, fill=False, color=GOLD, lw=1.5)
ax.add_patch(c1)
ax.plot([0.5 + 0.42], [1.0], "o", ms=6, color=GOLD, zorder=5)
ax.text(0.5, 0.30, "θ fixed — no turn", color=GOLD, fontsize=8.5, ha="center")
ax.text(0.5, 0.12, "χ = +1, trivial", color="#9aa0a8", fontsize=8, ha="center")
ax.text(0.5, 1.52, "the seam", color="#eee", fontsize=10, ha="center")
ax.text(0.5, 1.40, "the lift reaches identity —\nthe sign becomes the count\nby acting trivially, the drone keeps",
        color="#9aa0a8", fontsize=7.6, ha="center", va="top")

# B2 the pole -- no lift
c2 = plt.Circle((1.5, 1.0), 0.42, fill=False, color=RED, lw=1.5, ls=(0, (4, 2)))
ax.add_patch(c2)
ax.text(1.5, 0.92, "∅", color=RED, fontsize=22, ha="center", va="center")
ax.text(1.5, 0.30, "no lift — no phase", color=RED, fontsize=8.5, ha="center")
ax.text(1.5, 0.12, "no character — absent", color="#9aa0a8", fontsize=8, ha="center")
ax.text(1.5, 1.52, "the pole", color="#eee", fontsize=10, ha="center")
ax.text(1.5, 1.40, "no lift, no character —\nnothing keeps",
        color="#9aa0a8", fontsize=7.6, ha="center", va="top")

ax.set_title("two silences: trivial, absent", color="#eee", fontsize=11.5, pad=8)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)

# footer
fig.text(0.5, 0.045,
         "the gap is the square — g = s²/2, even, the count's reading.  the phase the square lost is the lift: cos θ, turning.  χ is its holonomy — the lift sampled at each lap.",
         color="#8a8f98", fontsize=9.5, ha="center")

fig.suptitle("the sign has two registers: the lift, and its character",
             color="#eee", fontsize=14.5, y=0.965)
plt.savefig("assets/lift-character.png", dpi=200, bbox_inches="tight",
            facecolor="#08090c")
print("wrote assets/lift-character.png")
