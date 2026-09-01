"""cover: the toll is the first square — the silver pair's AGM descent.
the two averages, iterated: gaps 220 → 45.56 → 1.97 → 0.0037, converging to
131.795 = 110·π/ϖ, the count read through the lemniscate, on no grid."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(11, 6.4), facecolor='#0c0d10')
ax.set_facecolor('#0c0d10')
fg = '#e8e4d8'
dim = '#8a8a9a'
gold = '#e8c34a'
rose = '#d98a9c'
cyan = '#6db5c9'
green = '#9fca9a'

s2 = np.sqrt(2.0)
sig = 1.0 + s2
C = 110.0
a0, b0 = C / sig, C * sig                      # 45.56, 265.56
AM, GM = (a0 + b0) / 2.0, C                    # 155.56, 110
TOLL = AM - GM                                 # 45.56
LIMIT = 131.79542582091514                     # 110π/ϖ
# AGM pairs
steps = [0, 1, 2, 3, 4]
pairs = [(a0, b0), (AM, GM)]
a, b = AM, GM
for _ in range(3):
    an, bn = (a + b) / 2.0, np.sqrt(a * b)
    pairs.append((an, bn))
    a, b = an, bn
pairs[4] = (LIMIT, LIMIT)
amem = [p[0] for p in pairs]
bmem = [p[1] for p in pairs]

ax.set_xlim(-0.4, 4.6)
ax.set_ylim(np.log2(40.0), np.log2(330.0))

def F2y(f):
    return np.log2(f)

# ---- grid lines: the count (gold), the limit (dashed), the tritone (dim)
for f, col, ls, lw in [(110.0, gold, '-', 1.2), (155.56, dim, ':', 0.8),
                       (45.56, rose, ':', 0.6), (265.56, cyan, ':', 0.6)]:
    ax.axhline(F2y(f), color=col, ls=ls, lw=lw, alpha=0.7)
ax.axhline(F2y(LIMIT), color=green, ls='--', lw=1.4, alpha=0.9)
ax.text(4.48, F2y(LIMIT) + 0.015, "131.795 = 110·π/ϖ", color=green,
        ha='right', va='bottom', fontsize=9, fontweight='bold')
ax.text(4.48, F2y(110.0) - 0.015, "110  the count", color=gold,
        ha='right', va='top', fontsize=9)

# ---- the two members converging: a_n (rose, AM line), b_n (cyan, GM line)
ax.plot(steps, [F2y(v) for v in amem], color=rose, lw=2.0, marker='o',
        ms=7, mfc=rose, mec='none', zorder=5, label='aₙ  the fold (AM)')
ax.plot(steps, [F2y(v) for v in bmem], color=cyan, lw=2.0, marker='o',
        ms=7, mfc=cyan, mec='none', zorder=5, label='bₙ  the mirror (GM)')
ax.plot(4, F2y(LIMIT), 'o', ms=10, mfc=gold, mec='none', zorder=6)

# ---- the gaps at each step, labeled
gaps = [(0, b0 - a0, "220 — the octave"),
        (1, TOLL, "45.56 — the toll (AM−GM = a₀ exactly)"),
        (2, bmem[2] - amem[2], "1.97"),
        (3, bmem[3] - amem[3], "0.0037")]
for st, gap, lab in gaps:
    if gap > 0.5:
        ax.annotate("", xy=(st, F2y(bmem[st])), xytext=(st, F2y(amem[st])),
                    arrowprops=dict(arrowstyle='<->', color=fg, lw=1.2,
                                    mutation_scale=13))
    ax.text(st, F2y(np.sqrt(amem[st] * bmem[st])) + 0.05, lab,
            color=fg if gap > 0.5 else green, ha='center', va='bottom',
            fontsize=8.5 if gap > 0.5 else 7.5)

# ---- labels under the steps
for st in steps[:4]:
    ax.text(st, np.log2(42.0), f"step {st}", color=dim, ha='center',
            fontsize=8)
ax.text(4, np.log2(42.0), "∞\n(131.795)", color=gold, ha='center', fontsize=8)

# ---- the silver pair note
ax.text(0, np.log2(305.0), "the pair {45.56, 265.56}", color=dim,
        ha='center', fontsize=8.5)

# ---- axis
ax.set_xticks([])
ax.set_yticks([F2y(f) for f in [45.56, 55, 77.78, 110, 131.795, 155.56, 220, 265.56, 311]])
ax.set_yticklabels(["45.56", "55", "77.78", "110", "131.8", "155.56", "220",
                    "265.56", "311"], color=dim, fontsize=7.5)
ax.tick_params(axis='y', colors=dim, length=3)
for s in ax.spines.values():
    s.set_color(dim)
ax.set_ylabel("Hz  (log scale)", color=dim, fontsize=10)
ax.grid(axis='y', color='#2a2b30', lw=0.5, alpha=0.6)

# ---- legend
ax.legend(loc='upper right', fontsize=8, frameon=False, labelcolor=fg,
          handlelength=1.5, borderaxespad=0.4)

ax.text(0.5, 1.065, "the toll is the first square",
        transform=ax.transAxes, color=fg, ha='center', fontsize=18,
        fontweight='bold')
ax.text(0.5, 1.012,
        "iterate the two averages on the silver pair \u2022 gaps 220 \u2192 45.56 \u2192 1.97 \u2192 0.0037 "
        "\u2014 the gap squares itself to death \u2022 the toll is the first square",
        transform=ax.transAxes, color=dim, ha='center', fontsize=8.5)
ax.text(0.5, -0.06,
        "step 1 lands on the two averages {tritone, count} \u2022 AM\u2212GM = the pair's own lowest "
        "tone (iff ratio \u03c3\u00b2) \u2022 the descent lands on 110\u00b7\u03c0/\u03d6, on no grid \u2014 "
        "0.8\u00a2 flat of the just minor third 6:5",
        transform=ax.transAxes, color=dim, ha='center', fontsize=8.5)

fig.tight_layout(rect=[0, 0.06, 1, 0.92])
plt.savefig('assets/agm-descent-cover.png', dpi=200,
            bbox_inches='tight', facecolor='#0c0d10')
print("wrote assets/agm-descent-cover.png")
