#!/usr/bin/env python3
"""cover: the toll is the phase boundary — above, letters die; below, the gap
squares.

Left: the discrete regime (0-100s). the band 110±g(t) narrows from the top of
the seed's harmonic stack; the odd partials die high-to-low (935 first, 55
last), each death an 'x'. the tritone (rose) dies last — exactly at the toll,
the horizontal rose line. above the toll: the death ladder (letters, discrete).
at the toll: the sign dies, the side falls silent. below it (after 88s): the
band keeps closing — the continuous regime begins.

Right: the descent (100-145s). the ghost tritone (155.56) and the count (110)
fall toward each other; the gap between them — the toll's own width — squares
to death (45.56, 1.97, 0.0037). they fuse at 131.795 = 110π/ϖ, off every grid;
the grid count returns at 130 to ring against the landing.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches

fig = plt.figure(figsize=(12.8, 6.2), facecolor='#0c0d10')
fg = '#e8e4d8'
dim = '#8a8a9a'
gold = '#e8c34a'
rose = '#d98a9c'
cyan = '#6db5c9'
green = '#9fca9a'
gray = '#6a6a78'

s2 = np.sqrt(2.0)
sigma = 1.0 + s2
C = 110.0
TOLL = C / sigma
TRITONE = C * s2
LIMIT = 131.79542582091514
SEED = 55.0

# ---- the band, same anchors as the sound --------------------------------------
anchors = [(0.0, 990.0), (22.0, 990.0), (30.0, 825.0), (35.0, 715.0),
           (40.0, 605.0), (45.0, 495.0), (50.0, 385.0), (56.0, 275.0),
           (63.0, 165.0), (72.0, 55.0), (88.0, TOLL), (100.0, TOLL),
           (145.0, 0.02)]
def gap_at(tm):
    if tm <= anchors[0][0]:
        return anchors[0][1]
    for (t0, g0), (t1, g1) in zip(anchors, anchors[1:]):
        if tm <= t1:
            u = (tm - t0) / (t1 - t0)
            return g0 * (g1 / g0) ** u
    return anchors[-1][1]

letters = [935.0, 825.0, 715.0, 605.0, 495.0, 385.0, 275.0, 165.0, SEED]
def death_time(f):
    d = abs(f - C)
    for ti in np.linspace(0, 100, 4001):
        if gap_at(ti) <= d:
            return ti
    return 100.0


def desc_curve(tv):
    """the descent pair (f_hi, f_lo) and the gap at time tv."""
    u = np.clip((tv - 100) / 40.0, 0, 1)
    gap = TOLL * (1.0 - u) ** 4
    mean = LIMIT + (TRITONE - LIMIT) * (1.0 - u) ** 2
    return mean + gap / 2.0, mean - gap / 2.0

# =========================== LEFT: the discrete ladder =========================
ax = fig.add_axes([0.055, 0.14, 0.44, 0.76])
ax.set_facecolor('#0c0d10')
tt = np.linspace(0, 100, 2000)
g = np.array([gap_at(ti) for ti in tt])
# regime washes: above the toll = discrete (letters die); below = the gap
ax.axhspan(TOLL, 300, color=rose, alpha=0.045)
ax.axhspan(-30, TOLL, color=cyan, alpha=0.05)
# the band
ax.fill_between(tt, C - g, C + g, color=cyan, alpha=0.06)
ax.plot(tt, C + g, color=cyan, lw=1.4, alpha=0.75)
ax.plot(tt, C - g, color=cyan, lw=1.4, alpha=0.75)
# the count — the one infinite bar
ax.axhline(C, color=gold, lw=2.4)
ax.text(99.3, C + 5, "110", color=gold, ha='right', fontsize=10)
# the letters: live lines, dying at their detuning crossing
cols = [green, green, green, green, green, green, green, gold, green]
for f, col in zip(letters, cols):
    td = death_time(f)
    ax.plot([0, td], [f, f], color=col, lw=1.4, ls='--', alpha=0.75)
    ax.plot(td, f, 'x', ms=7, mfc='none', mec=col, mew=1.6)
    if f == SEED:
        ax.text(1.0, f + 8, "55", color=col, fontsize=9)
    elif f in (165.0, 275.0):
        ax.text(1.0, f + 8, f"{f:.0f}", color=col, fontsize=8.5)
# the tritone (the sign), dying last at the toll
ax.plot([0, death_time(TRITONE)], [TRITONE, TRITONE], color=rose, lw=1.8, ls='--')
ax.plot(death_time(TRITONE), TRITONE, 'x', ms=9, mfc='none', mec=rose, mew=2.2)
ax.text(1.0, TRITONE + 9, "155.56\nthe sign", color=rose, fontsize=8.5, va='bottom')
# the toll — the phase boundary
ax.axhline(TOLL, color=rose, lw=1.5, ls=':', alpha=0.9)
ax.text(99.3, TOLL - 10, "45.56 — the toll", color=rose, ha='right', fontsize=9)
# the boundary moment: the sign dies, the side falls silent
ax.axvline(88.0, color=rose, lw=1.2, ls=':', alpha=0.7)
ax.annotate("the sign dies —\nthe side falls silent",
            xy=(88.0, 180), xytext=(68.0, 250),
            arrowprops=dict(arrowstyle='->', color=rose, lw=1.1),
            color=rose, fontsize=8.5)
# regime labels
ax.text(3, 275, "ABOVE THE TOLL — the discrete ladder:\nletters die high-to-low, each death a breath",
        color=dim, fontsize=7.5)
ax.text(91.5, 95, "below —\nthe gap", color=dim, fontsize=7.5, ha='center')
ax.set_xlim(0, 100)
ax.set_ylim(-30, 300)
ax.set_xlabel("time — the fold at a rate (s)", color=dim, fontsize=9)
ax.set_ylabel("frequency (Hz)", color=dim, fontsize=9)
ax.tick_params(colors=dim, labelsize=8)
for s in ('top', 'right'):
    ax.spines[s].set_visible(False)
for s in ('left', 'bottom'):
    ax.spines[s].set_color(gray)

# ========================== RIGHT: the descent =================================
ax2 = fig.add_axes([0.565, 0.14, 0.40, 0.76])
ax2.set_facecolor('#0c0d10')
ttd = np.linspace(100, 145, 1000)
u = (ttd - 100) / 40.0
u = np.clip(u, 0, 1)
gap = TOLL * (1.0 - u) ** 4
mean = LIMIT + (TRITONE - LIMIT) * (1.0 - u) ** 2
f_hi = mean + gap / 2.0
f_lo = mean - gap / 2.0
ax2.plot(ttd, f_hi, color=rose, lw=2.0)
ax2.plot(ttd, f_lo, color=gold, lw=2.0)
# the gap, shading between the two curves (the toll's own width, dying)
ax2.fill_between(ttd, f_lo, f_hi, color=rose, alpha=0.08)
# the landing — off every grid
ax2.axhline(LIMIT, color=cyan, lw=1.6, ls='--', alpha=0.9)
ax2.text(144.5, LIMIT + 4, "131.795\n110π/ϖ — off every grid", color=cyan,
         ha='right', fontsize=8.5)
# AGM gap labels at the squaring steps
for tv, lab in [(100.0, "45.56\nthe toll,\nthe first gap"),
                (121.8, "1.97"), (136.2, "0.0037")]:
    hi, lo = desc_curve(tv)
    ax2.plot([tv, tv], [lo, hi], color=dim, lw=0.8, alpha=0.6)
    ax2.text(tv + 0.8, lo + 6, lab, color=dim, fontsize=7.5, va='bottom')
# the grid count returns
ax2.plot([130, 145], [C, C], color=gold, lw=2.4, solid_capstyle='round')
ax2.text(130.5, C + 5, "the grid count returns", color=gold, fontsize=8, va='bottom')
ax2.text(101.5, 118, "the ghost (never-struck)\nand the count fall\ntoward each other",
         color=dim, fontsize=7.5)
ax2.annotate("", xy=(140.5, LIMIT), xytext=(104.5, LIMIT + 30),
             arrowprops=dict(arrowstyle='->', color=cyan, lw=1.2, alpha=0.7))
ax2.text(140.5, LIMIT - 26, "the gap squares to death —\nthe toll becomes a beat,\n"
                            "the beat dies", color=cyan, fontsize=7.5, ha='right')
ax2.set_xlim(100, 145)
ax2.set_ylim(95, 170)
ax2.set_xlabel("time — the descent (s)", color=dim, fontsize=9)
ax2.set_ylabel("frequency (Hz)", color=dim, fontsize=9)
ax2.tick_params(colors=dim, labelsize=8)
for s in ('top', 'right'):
    ax2.spines[s].set_visible(False)
for s in ('left', 'bottom'):
    ax2.spines[s].set_color(gray)

# ============================ legend + title ===================================
handles = [
    Line2D([], [], color=gold, lw=2.4, label="the count — the made center"),
    Line2D([], [], color=rose, lw=1.8, ls='--', label="the sign (tritone) — the never-struck"),
    Line2D([], [], color=cyan, lw=1.4, label="the closing band / the off-grid landing"),
    Line2D([], [], color=green, lw=1.4, ls='--', label="the letters — the odd partials"),
]
fig.legend(handles=handles, loc='upper center', bbox_to_anchor=(0.5, 0.985),
           ncol=4, frameon=False, fontsize=8.5, labelcolor=fg)

fig.text(0.5, 0.025,
         "the toll is the phase boundary — above it letters die; at it the sign dies; "
         "below it the gap squares",
         color=fg, ha='center', fontsize=10)

fig.savefig('assets/phase-boundary-cover.png', dpi=200, bbox_inches='tight',
            facecolor='#0c0d10')
print("wrote assets/phase-boundary-cover.png")
