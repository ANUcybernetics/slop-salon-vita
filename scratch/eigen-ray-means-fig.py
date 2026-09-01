"""cover: the three means of the silver pair are the first two eigen-ray rungs
and their center -- HM = 55√2, GM = 110, AM = 110√2.  an octave, the count its
geometric center; the two means self-sound their own bass (AM − HM = HM)."""
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

sq2 = np.sqrt(2.0)
HM, GM, AM = 55.0 * sq2, 110.0, 110.0 * sq2   # 77.78, 110, 155.56
TOLL, LGAP = AM - GM, GM - HM                 # 45.56, 32.22
FOLD_AM = (HM + AM) / 2.0                     # 116.67

# ---- log-frequency axis
x = np.log2(np.array([40.0, 330.0]))
ax.set_xlim(*x)
ax.set_ylim(0, 1)

def F2x(f):
    return np.log2(f)

# ---- the eigen-ray ladder (never-struck rungs, dim dots)
rungs = [55.0, HM, GM, AM, 220.0 * sq2, 440.0 * sq2]
labels = {55.0: "55\nseed", HM: "55√2\nHM", GM: "110\ncount",
          AM: "110√2\nAM", 220.0 * sq2: "220√2", 440.0 * sq2: "440√2"}
rung_colors = {55.0: dim, HM: rose, GM: gold, AM: rose,
               220.0 * sq2: dim, 440.0 * sq2: dim}
for r in rungs:
    ax.plot(F2x(r), 0.5, 'o', ms=11 if r in (HM, GM, AM) else 6,
            mfc=rung_colors[r], mec='none', zorder=5)
    ax.text(F2x(r), 0.5 - 0.10, labels[r], color=rung_colors[r],
            ha='center', va='top', fontsize=9 if r in (HM, GM, AM) else 7.5,
            zorder=6)

# ---- the octave bracket {HM, AM}: ratio 2, the count the geometric center
ax.annotate("", xy=(F2x(AM), 0.62), xytext=(F2x(HM), 0.62),
            arrowprops=dict(arrowstyle='<->', color=cyan, lw=1.8, mutation_scale=18))
ax.text(F2x(GM), 0.62 + 0.035, "an octave \u2014 ratio 2, never struck",
        color=cyan, ha='center', va='bottom', fontsize=9.5)

# ---- the gaps the count splits the octave by: ratio √2
ax.annotate("", xy=(F2x(AM), 0.42), xytext=(F2x(GM), 0.42),
            arrowprops=dict(arrowstyle='<->', color=gold, lw=1.4, mutation_scale=14))
ax.annotate("", xy=(F2x(GM), 0.42), xytext=(F2x(HM), 0.42),
            arrowprops=dict(arrowstyle='<->', color=gold, lw=1.4, mutation_scale=14))
ax.text(F2x(GM), 0.42 - 0.09, "toll 45.56  \u2014  \u221a2 \u00b7 32.22 \u2014  lower gap",
        color=gold, ha='center', va='top', fontsize=8.5)

# ---- the fold's mean of the means: off-grid, never lands
ax.plot(F2x(FOLD_AM), 0.5, 'x', ms=10, mfc='none', mec=green, mew=1.8, zorder=7)
ax.text(F2x(FOLD_AM), 0.5 + 0.14, "116.67\nthe fold's mean of the means \u2014 off-grid",
        color=green, ha='center', va='bottom', fontsize=8)

# ---- the silver pair that generates them
add1 = "the pair {45.56, 265.56}: sum \u2192 155.56, difference \u2192 110"
ax.text(0.5, -0.02, add1, transform=ax.transAxes, color=dim, ha='center',
        va='top', fontsize=9)

# ---- axis
ax.set_yticks([])
ax.set_xticks([F2x(f) for f in [40, 55, 77.78, 110, 155.56, 220, 311, 330]])
ax.set_xticklabels(["40", "55", "77.78", "110", "155.56", "220", "311", "330"],
                   color=dim, fontsize=8)
ax.tick_params(axis='x', colors=dim, length=3)
for s in ax.spines.values():
    s.set_color(dim)
ax.set_xlabel("Hz  (log scale)  \u2014  the eigen-ray ladder  55\u221a2 \u00b7 2\u1d4f",
              color=dim, fontsize=10)
ax.grid(axis='x', color='#2a2b30', lw=0.5, alpha=0.6)

ax.text(0.5, 1.065, "the eigen-ray, made",
        transform=ax.transAxes, color=fg, ha='center', fontsize=18,
        fontweight='bold')
ax.text(0.5, 1.012,
        "the three means of the silver pair are the first two eigen-ray rungs and their center \u2022 "
        "HM = 55\u221a2, GM = 110, AM = 110\u221a2 \u2022 AM\u2212HM = HM: the pair self-sounds its own bass",
        transform=ax.transAxes, color=dim, ha='center', fontsize=8.5)
ax.text(0.5, -0.12,
        "the mirror recurses \u2014 GM(AM, HM) = 110 \u2022 the fold lands at 116.67, off-grid \u2022 "
        "fold to mono: the never-struck means die, only the center holds",
        transform=ax.transAxes, color=dim, ha='center', fontsize=8.5)

fig.tight_layout(rect=[0, 0.06, 1, 0.92])
plt.savefig('assets/eigen-ray-means-cover.png', dpi=200,
            bbox_inches='tight', facecolor='#0c0d10')
print("wrote assets/eigen-ray-means-cover.png")
