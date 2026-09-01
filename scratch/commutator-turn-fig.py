"""cover: the commutator [fold, strike] = J, a quarter-turn; J² = −I.
the strike's image is the silver pair, exact; the two orders land apart;
the lemniscate's period lattice ϖ·ℤ[i] has the quarter-turn as its symmetry."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize=(12, 6.4), facecolor='#0c0d10')
ax = fig.add_axes([0.07, 0.16, 0.62, 0.72])
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
TOLL, COUNT, TRITONE, UPPER = C / sig, C, C * s2, C * sig
MEAN = (COUNT + TRITONE) / 2.0
LIMIT = 110.0 * np.pi / 2.6220575542921198
OCT = 2.0 * C

x = np.log2(np.array([42.0, 320.0]))
ax.set_xlim(*x)
ax.set_ylim(0, 1)


def F2x(f):
    return np.log2(f)


# ---- the four-tone orbit
tones = [TOLL, COUNT, TRITONE, UPPER]
tl = {TOLL: "toll\n45.56", COUNT: "count\n110", TRITONE: "tritone\n155.56",
      UPPER: "upper\n265.56"}
tc = {TOLL: rose, COUNT: gold, TRITONE: cyan, UPPER: rose}
for f in tones:
    ax.plot(F2x(f), 0.52, 'o', ms=11, mfc=tc[f], mec='none', zorder=6)
    ax.text(F2x(f), 0.52 - 0.10, tl[f], color=tc[f], ha='center', va='top',
            fontsize=8.5, zorder=7)

# ---- the pair bracket (count, tritone)
ax.annotate("", xy=(F2x(TRITONE), 0.30), xytext=(F2x(COUNT), 0.30),
            arrowprops=dict(arrowstyle='<->', color=fg, lw=1.4, mutation_scale=14))
ax.text(F2x((COUNT + TRITONE) / 2), 0.30 - 0.06, "the pair",
        color=fg, ha='center', va='top', fontsize=9)

# ---- the STRIKE T: (count, tritone) -> (toll, upper), the silver pair
ax.annotate("", xy=(F2x(UPPER), 0.42), xytext=(F2x(COUNT), 0.38),
            arrowprops=dict(arrowstyle='->', color=dim, lw=1.6,
                            connectionstyle="arc3,rad=-0.25", mutation_scale=16))
ax.annotate("", xy=(F2x(TOLL), 0.42), xytext=(F2x(TRITONE), 0.38),
            arrowprops=dict(arrowstyle='->', color=dim, lw=1.6,
                            connectionstyle="arc3,rad=-0.25", mutation_scale=16))
ax.text(F2x((COUNT + UPPER) / 2), 0.44, "T: the strike\n(count, tritone) \u2192 (toll, upper)",
        color=dim, ha='center', va='bottom', fontsize=8)

# ---- the two orders land apart
ax.plot(F2x(UPPER), 0.52, 'x', ms=12, mfc='none', mec=green, mew=2.0, zorder=8)
ax.text(F2x(UPPER), 0.52 + 0.16, "fold then strike \u2192 265.56",
        color=green, ha='center', va='bottom', fontsize=8)
ax.plot(F2x(TRITONE), 0.52, 'x', ms=12, mfc='none', mec=green, mew=2.0, zorder=8)
ax.text(F2x(TRITONE), 0.52 + 0.16, "strike then fold \u2192 155.56",
        color=green, ha='center', va='bottom', fontsize=8)

# ---- the commutator J: a quarter-turn arc between the landings
ax.annotate("", xy=(F2x(TRITONE), 0.74), xytext=(F2x(UPPER), 0.74),
            arrowprops=dict(arrowstyle='->', color=fg, lw=1.8,
                            connectionstyle="arc3,rad=0.5", mutation_scale=18))
ax.text(F2x((TRITONE + UPPER) / 2), 0.76,
        "their difference is J, the quarter-turn \u2014 J\u00b2 = \u2212I",
        color=fg, ha='center', va='bottom', fontsize=9)

# ---- the fold's mean vs the descent's limit (near-coincident, off-grid)
ax.plot(F2x(MEAN), 0.52, 'd', ms=7, mfc='none', mec=green, mew=1.5, zorder=8)
ax.plot(F2x(LIMIT), 0.52, 'd', ms=7, mfc='none', mec=green, mew=1.5, zorder=8)
ax.text(F2x(LIMIT), 0.52 - 0.20, "the fold's mean 132.78 \u2248\nthe descent's 110\u03c0/\u03d6 = 131.795, off-grid",
        color=green, ha='center', va='top', fontsize=7.5)

# ---- the hole
ax.text(F2x(COUNT), 0.52 - 0.30, "the count, laid over its own inversion,\nis silence \u2014 you hear the sign where it isn't",
        color=gold, ha='center', va='top', fontsize=7.5)

# ---- axis
ax.set_yticks([])
xt = [45.56, 110, 132.78, 155.56, 265.56]
ax.set_xticks([F2x(f) for f in xt])
ax.set_xticklabels(["45.56", "110", "132.78", "155.56", "265.56"],
                   color=dim, fontsize=8)
ax.tick_params(axis='x', colors=dim, length=3)
for s in ax.spines.values():
    s.set_color(dim)
ax.set_xlabel("Hz (log) \u2014 the four-tone orbit of the strike", color=dim, fontsize=10)
ax.grid(axis='x', color='#2a2b30', lw=0.5, alpha=0.6)

# ---- inset: the lemniscate and its square period lattice ϖ·ℤ[i]
axin = fig.add_axes([0.74, 0.16, 0.22, 0.72])
axin.set_facecolor('#0c0d10')
th = np.linspace(-np.pi / 4, np.pi / 4, 400)
r = np.sqrt(2.0 * np.cos(2 * th))
xr, yr = r * np.cos(th), r * np.sin(th)
for sgn in (1, -1):
    axin.plot(xr, sgn * yr, color=cyan, lw=1.6)
    axin.plot(-xr, sgn * yr, color=cyan, lw=1.6)
# lattice dots ϖ·(m+in)
lem = 2.6220575542921198
scale = 0.55
for m in range(-2, 3):
    for nn in range(-2, 3):
        axin.plot(scale * lem * m, scale * lem * nn, '.', color=dim, ms=3)
# the quarter-turn J arrow at the origin
axin.annotate("", xy=(0, -0.9), xytext=(0.9, 0),
              arrowprops=dict(arrowstyle='->', color=gold, lw=2.0,
                              connectionstyle="arc3,rad=0.7", mutation_scale=20))
axin.text(0, -0.42, "J", color=gold, ha='center', va='center', fontsize=11)
axin.plot([0], [0], 'o', color=fg, ms=4)
axin.set_xlim(-2.6, 2.6)
axin.set_ylim(-2.6, 2.6)
axin.set_aspect('equal')
axin.set_yticks([])
axin.set_xticks([])
for s in axin.spines.values():
    s.set_color(dim)
axin.set_title("the lemniscate \u2014 its period lattice \u03d6\u00b7\u2124[i]\ninvariant under the quarter-turn",
               color=dim, fontsize=8)

# ---- titles
ax.text(0.5, 1.055, "the quarter-turn",
        transform=ax.transAxes, color=fg, ha='center', fontsize=18,
        fontweight='bold')
ax.text(0.5, 1.01,
        "the fold and the strike do not commute \u2022 their commutator is J, a quarter-turn \u2022 "
        "J\u00b2 = \u2212I \u2022 the strike's image is the silver pair, exact",
        transform=ax.transAxes, color=dim, ha='center', fontsize=8.5)

fig.savefig('assets/commutator-turn-cover.png', dpi=200,
            bbox_inches='tight', facecolor='#0c0d10')
print("wrote assets/commutator-turn-cover.png")
