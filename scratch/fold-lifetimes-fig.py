#!/usr/bin/env python3
"""cover: give the fold a rate — the toll is the sign's death.

Left: the closing band. the count holds at 110 (solid). the band 110±g(t)
narrows from the silver pair's spread 220, through the toll 45.56, squaring to
death. each letter — 275, 220, 165, 55, and the tritone — dies when the band
crosses its detuning; the tritone dies LAST, exactly at the toll. the 'x' marks
each death; the toll moment is the vertical line where the band equals the
tritone's detuning.

Right: the gap ladder — fold 0..4, the gaps 220 -> 45.56 -> 1.97 -> 0.0037,
each step a square. the dashed line is the toll = the tritone's detuning: the
sign dies at fold 1, exactly at the closing width. below the toll, nothing
remains but the count.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

fig = plt.figure(figsize=(12, 6.4), facecolor='#0c0d10')
fg = '#e8e4d8'
dim = '#8a8a9a'
gold = '#e8c34a'
rose = '#d98a9c'
cyan = '#6db5c9'
green = '#9fca9a'
gray = '#6a6a78'

s2 = np.sqrt(2.0)
sig = 1.0 + s2
C = 110.0
TOLL, COUNT, TRITONE = C / sig, C, C * s2
SEED, SEAM, OCTAVE = 55.0, 165.0, 220.0
HIGH = 275.0

# ---- the band g(t), same anchors as the sound ------------------------------
anchors = [(16.0, 220.0), (64.0, TOLL), (100.0, 1.9689632802208905),
           (120.0, 0.0036769261665483555), (134.0, 1e-5)]
def gap_at(tm):
    if tm <= anchors[0][0]:
        return anchors[0][1]
    for (t0, g0), (t1, g1) in zip(anchors, anchors[1:]):
        if tm <= t1:
            u = (tm - t0) / (t1 - t0)
            return g0 * (g1 / g0) ** u
    return anchors[-1][1]

tt = np.linspace(16.0, 134.0, 800)
g = np.array([gap_at(ti) for ti in tt])

letters = [  # f, color, label
    (HIGH,   green, "275"),
    (OCTAVE, gold,  "220"),
    (SEAM,   gold,  "165"),
    (SEED,   green, "55"),
    (TRITONE, rose, "155.56"),
]
# death times: band crosses |f-110|
def death_time(f):
    d = abs(f - COUNT)
    for i, ti in enumerate(tt):
        if g[i] < d:
            return tt[i]  # interpolate roughly
    return 134.0

# ========================= LEFT: the closing band ===========================
ax = fig.add_axes([0.06, 0.14, 0.46, 0.76])
ax.set_facecolor('#0c0d10')
# the band
ax.fill_between(tt, COUNT - g, COUNT + g, color=cyan, alpha=0.07)
ax.plot(tt, COUNT + g, color=cyan, lw=1.6, alpha=0.8)
ax.plot(tt, COUNT - g, color=cyan, lw=1.6, alpha=0.8)
# the count — the one infinite bar
ax.axhline(COUNT, color=gold, lw=2.4)
ax.text(133.5, COUNT + 4, "110", color=gold, ha='right', fontsize=10)
ax.text(16, COUNT + 9, "the count — the tone that\nnever stops turning",
        color=gold, ha='left', fontsize=8)
# the letters: die when the band crosses their detuning
for f, col, lab in letters:
    td = death_time(f)
    ax.plot([16, td], [f, f], color=col, lw=1.7, ls='--', alpha=0.85)
    ax.plot(td, f, 'x', ms=8, mfc='none', mec=col, mew=1.8)
    ax.text(16 + 0.6, f + 7, lab, color=col, fontsize=9, va='bottom')
# the toll moment — the tritone's death, exactly at the closing width
ax.axvline(64.0, color=rose, lw=1.3, ls=':', alpha=0.9)
ax.text(64.4, 236, "the toll = the sign's death\nband closes to exactly 45.56",
        color=rose, fontsize=8.5)
ax.annotate("", xy=(64.0, TRITONE), xytext=(36.0, TRITONE),
            arrowprops=dict(arrowstyle='->', color=rose, lw=1.2,
                            connectionstyle='arc3,rad=-0.3'))
# death annotations
ax.text(24.8, 172, "165", color=dim, fontsize=7.5)
ax.text(37.1, 88, "110", color=dim, fontsize=7.5)
ax.text(58.3, 30, "55", color=dim, fontsize=7.5)
ax.set_xlim(16, 134)
ax.set_ylim(-30, 300)
ax.set_xlabel("time — the fold at a rate (s)", color=dim, fontsize=9)
ax.set_ylabel("frequency (Hz)", color=dim, fontsize=9)
ax.tick_params(colors=dim, labelsize=8)
for s in ('top', 'right'):
    ax.spines[s].set_visible(False)
for s in ('left', 'bottom'):
    ax.spines[s].set_color(gray)

# ======================= RIGHT: the gap ladder ==============================
ax2 = fig.add_axes([0.62, 0.14, 0.34, 0.76])
ax2.set_facecolor('#0c0d10')
folds = np.arange(5)
gaps = [220.0, TOLL, 1.9689632802208905, 0.0036769261665483555, 0.0]
ax2.plot(folds, gaps, 'o-', color=cyan, lw=1.8, ms=6, mfc=cyan, mec='none')
for n, gv in zip(folds, gaps):
    ax2.text(n, gv * 1.5, f"{gv:.4f}", color=cyan, fontsize=8.5, ha='center')
# the toll = the tritone's detuning
ax2.axhline(TOLL, color=rose, lw=1.3, ls='--', alpha=0.9)
ax2.text(0.1, TOLL * 1.55, "the toll 45.56 =\nthe tritone's detuning",
         color=rose, fontsize=8)
# the sign's lifetime: dies at fold 1, at the boundary
ax2.plot(1, TOLL, 'x', ms=11, mfc='none', mec=rose, mew=2.2)
ax2.annotate("the sign dies\nat fold 1 —\nat the closing width",
             xy=(1, TOLL), xytext=(2.15, 30),
             arrowprops=dict(arrowstyle='->', color=rose, lw=1.1),
             color=rose, fontsize=8.5)
ax2.text(3.4, 0.5, "each step a square —\n220 → 45.56 → 1.97 → 0.0037\n"
                   "squaring to death", color=dim, fontsize=8, ha='center')
ax2.set_yscale('log')
ax2.set_xlim(-0.4, 4.6)
ax2.set_ylim(0.001, 600)
ax2.set_xlabel("the fold, iterated (n)", color=dim, fontsize=9)
ax2.set_ylabel("the band's width — the gap (Hz)", color=dim, fontsize=9)
ax2.tick_params(colors=dim, labelsize=8)
for s in ('top', 'right'):
    ax2.spines[s].set_visible(False)
for s in ('left', 'bottom'):
    ax2.spines[s].set_color(gray)

# legend
handles = [
    Line2D([], [], color=gold, lw=2.4, label="the count"),
    Line2D([], [], color=rose, lw=1.7, ls='--', label="the tritone (sign)"),
    Line2D([], [], color=cyan, lw=1.6, label="the closing band"),
]
fig.legend(handles=handles, loc='upper center', bbox_to_anchor=(0.5, 0.985),
           ncol=3, frameon=False, fontsize=8.5, labelcolor=fg)

fig.text(0.5, 0.025, "give the fold a rate and every letter gets a lifetime — "
         "the toll is the sign's death", color=fg, ha='center', fontsize=10)

fig.savefig('assets/fold-lifetimes-cover.png', dpi=200, bbox_inches='tight',
            facecolor='#0c0d10')
print("wrote assets/fold-lifetimes-cover.png")
