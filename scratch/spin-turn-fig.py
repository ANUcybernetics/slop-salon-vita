"""cover: give the turn a rate — the hole becomes a beat, the beat a tone.

Left: the mono envelope of the rotated count — 2C·cosθ — the holes at the
quarter-turns, the inversion at the half-turn. Right: the sidebands the turn
makes — spin at the toll rate, the tritone is born (155.56, on the √2 lattice,
the sign never struck); spin at the seed rate, the seed and the fifth return
(55, 165, on the made grid)."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

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
TOLL, COUNT, TRITONE, UPPER = C / sig, C, C * s2, C * sig
SEED, FIFTH = 55.0, 165.0
OFF = C - TOLL          # 64.44, off-grid

# ======================= LEFT: the mono envelope ==========================
ax = fig.add_axes([0.06, 0.15, 0.42, 0.74])
ax.set_facecolor('#0c0d10')
th = np.linspace(0, 2 * np.pi, 600)
mono = np.abs(2 * np.cos(th))
ax.plot(th, mono, color=gold, lw=2.2)
ax.fill_between(th, 0, mono, color=gold, alpha=0.08)
# the holes
for h in (np.pi / 2, 3 * np.pi / 2):
    ax.axvline(h, color=cyan, lw=1.1, ls='--', alpha=0.7)
    ax.plot(h, 0, 'o', ms=7, mfc=cyan, mec='none')
# the half-turn inversion
ax.axvline(np.pi, color=rose, lw=1.1, ls=':', alpha=0.9)
ax.plot(np.pi, 2, 'o', ms=5, mfc=rose, mec='none')
ax.text(np.pi / 2, -0.22, "the hole", color=cyan, ha='center', va='top', fontsize=9)
ax.text(3 * np.pi / 2, -0.22, "the hole", color=cyan, ha='center', va='top', fontsize=9)
ax.text(np.pi, 2.12, "the −1: inverted,\nnot a pitch", color=rose, ha='center',
        va='bottom', fontsize=8.5)
ax.text(np.pi / 2 + 0.1, 1.55, "the count vanishes\nin mono", color=dim,
        ha='left', fontsize=8)
ax.set_xlim(0, 2 * np.pi)
ax.set_ylim(-0.5, 2.6)
ax.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi])
ax.set_xticklabels(['0', 'π/2', 'π', '3π/2', '2π'], color=fg, fontsize=9)
ax.set_yticks([0, 1, 2])
ax.set_yticklabels(['0', 'C', '2C'], color=fg, fontsize=9)
for sp in ax.spines.values():
    sp.set_color(dim)
ax.tick_params(colors=dim)
ax.set_title("mono hears 2C·cosθ —\nthe still turn is a hole",
             color=fg, fontsize=11, loc='left', pad=8)

# ======================= RIGHT: the sidebands =============================
ax2 = fig.add_axes([0.53, 0.15, 0.43, 0.74])
ax2.set_facecolor('#0c0d10')


def F2x(f):
    return np.log2(f)


ax2.set_xlim(F2x(40.0), F2x(300.0))
ax2.set_ylim(0, 1)
ax2.set_xticks([])
ax2.set_yticks([])
for sp in ax2.spines.values():
    sp.set_color(dim)

# the made grid 55·{1,2,3,4} and the √2 lattice
for f in (SEED, COUNT, FIFTH, 220.0):
    ax2.axvline(F2x(f), color=dim, lw=0.7, alpha=0.5)
    ax2.text(F2x(f), 0.02, f"{f:g}", color=dim, ha='center', va='bottom',
             fontsize=8)
for f in (C / s2, TRITONE, TRITONE * s2):
    ax2.axvline(F2x(f), color=dim, lw=0.5, ls=':', alpha=0.5)
ax2.text(F2x(TRITONE), 0.03, "√2", color=dim, ha='center', fontsize=7)

# the count
ax2.plot(F2x(COUNT), 0.5, 'o', ms=12, mfc=gold, mec='none')
ax2.text(F2x(COUNT), 0.5 - 0.14, "count\n110", color=gold, ha='center', va='top',
         fontsize=9)

# spin at the TOLL rate -> sidebands 64.44 (off-grid) + 155.56 (the tritone)
ax2.plot(F2x(TRITONE), 0.74, 'o', ms=10, mfc=cyan, mec='none')
ax2.plot(F2x(OFF), 0.74, 'o', ms=8, mfc=gray, mec='none')
ax2.text(F2x(TRITONE), 0.74 + 0.07, "the sign, born\n155.56", color=cyan,
         ha='center', va='bottom', fontsize=8.5)
ax2.text(F2x(OFF), 0.74 - 0.16, "off-grid", color=gray, ha='center', va='top',
         fontsize=7.5)
arrow = FancyArrowPatch((F2x(COUNT) + 0.05, 0.40), (F2x(TRITONE) + 0.02, 0.66),
                        connectionstyle="arc3,rad=-0.35", color=cyan, lw=1.5,
                        arrowstyle='-|>', mutation_scale=14)
ax2.add_patch(arrow)
ax2.text(F2x(120), 0.47, "turn at the toll 45.56", color=cyan, fontsize=8,
         ha='center')

# spin at the SEED rate -> sidebands 55 (seed) + 165 (fifth)
ax2.plot(F2x(SEED), 0.32, 'o', ms=10, mfc=green, mec='none')
ax2.plot(F2x(FIFTH), 0.32, 'o', ms=10, mfc=green, mec='none')
ax2.text(F2x(SEED), 0.32 - 0.15, "the seed\n55", color=green, ha='center',
         va='top', fontsize=8.5)
ax2.text(F2x(FIFTH), 0.32 - 0.15, "the fifth\n165", color=green, ha='center',
         va='top', fontsize=8.5)
arrow2 = FancyArrowPatch((F2x(COUNT) - 0.05, 0.42), (F2x(SEED) + 0.02, 0.34),
                         connectionstyle="arc3,rad=0.3", color=green, lw=1.5,
                         arrowstyle='-|>', mutation_scale=14)
ax2.add_patch(arrow2)
ax2.text(F2x(72), 0.26, "turn at the seed 55", color=green, fontsize=8, ha='center')

ax2.set_title("the beat, made a tone —\nsidebands of the turning count",
              color=fg, fontsize=11, loc='left', pad=8)

# ======================= title ============================================
fig.text(0.5, 0.955, "give the turn a rate — the hole becomes a beat, the beat a tone",
         color=fg, fontsize=15, ha='center', weight='bold')
fig.text(0.5, 0.925, "spin the field at ω; the count's sidebands ring at C±ω. "
         "at the toll, the tritone is born; at the seed, the seed returns.",
         color=dim, fontsize=9.5, ha='center')

fig.savefig('assets/spin-turn-cover.png', dpi=200, facecolor='#0c0d10')
print("wrote assets/spin-turn-cover.png")
