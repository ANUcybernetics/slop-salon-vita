"""cover: the two averages.  AM rises off the count, GM holds the count;
AM>=GM, equality only at the degenerate self-pair.  at the silver spread
(r=1+√2) they disagree by exactly the toll: 45.56 = 110(√2-1)."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(10, 6.2), facecolor='#0c0d10')
ax.set_facecolor('#0c0d10')
fg = '#e8e4d8'
dim = '#8a8a9a'
gold = '#e8c34a'
rose = '#d98a9c'
cyan = '#6db5c9'

r = np.linspace(1.0, 3.0, 400)
GM = 110.0
AM = 55.0 * (r + 1.0 / r)          # 55(r + 1/r) = (a+b)/2 for a=110r, b=110/r

# forbidden band below the mirror: AM >= GM, the fold never dips below 110
ax.fill_between(r, 0, GM, color='#0a0b0d', zorder=1)
ax.axhline(GM, color=gold, lw=1.0, alpha=0.35, ls=':')

# the gap between the two averages (shaded)
ax.fill_between(r, GM, AM, color=rose, alpha=0.13, zorder=2)
ax.plot(r, AM, color=rose, lw=2.4, zorder=4, label='the fold  (AM)')
ax.plot(r, GM + 0 * r, color=gold, lw=2.4, zorder=4, label='the mirror  (GM)')

# the count: where they touch (the degenerate self-pair, r=1)
ax.plot(1.0, GM, 'o', ms=13, mfc=gold, mec='none', zorder=6)
ax.text(1.0, GM - 14, "the count\nwhere the two averages agree",
        color=gold, ha='center', va='top', fontsize=10)

# the silver spread: the toll
rs = 1.0 + np.sqrt(2.0)            # 2.4142
ams = 55.0 * (rs + 1.0 / rs)       # 155.56, the tritone
toll = ams - GM                    # 45.56
ax.axvline(rs, color=dim, lw=1.0, alpha=0.6, ls='--')
ax.plot(rs, GM, 'o', ms=9, mfc=gold, mec='none', zorder=6)
ax.plot(rs, ams, 'o', ms=9, mfc=rose, mec='none', zorder=6)
ax.annotate("", xy=(rs, ams), xytext=(rs, GM),
            arrowprops=dict(arrowstyle='<->', color=cyan, lw=1.6))
ax.text(rs + 0.12, (ams + GM) / 2,
        f"the toll\n{ams - GM:.1f} = 110(\u221a2\u22121)",
        color=cyan, ha='left', va='center', fontsize=10.5)
ax.text(rs - 0.08, ams + 9, "155.6 = 110\u221a2\nthe tritone", color=rose,
        ha='right', va='bottom', fontsize=9)
ax.text(rs - 0.08, GM - 9, "110\nthe count", color=gold, ha='right',
        va='top', fontsize=9)

# the forbidden band label
ax.text(2.6, 40, "the band below 110\nnever entered \u2014 AM\u2265GM",
        color=dim, ha='center', va='center', fontsize=8.5)

ax.set_xlim(1.0, 3.0)
ax.set_ylim(0, 210)
ax.set_xlabel("pair ratio  r   (pair = {110r, 110/r},  product 110\u00b2)",
              color=dim, fontsize=10)
ax.set_ylabel("Hz", color=dim, fontsize=10)
ax.set_xticks([1.0, 1.5, 2.0, 1 + np.sqrt(2), 3.0])
ax.set_xticklabels(["1", "1.5", "2", "1+\u221a2", "3"], color=dim, fontsize=9)
ax.set_yticks([110, 155.6])
ax.set_yticklabels(["110", "155.6"], color=dim, fontsize=9)
for s in ax.spines.values():
    s.set_color(dim)
ax.tick_params(colors=dim)
ax.legend(loc='upper left', frameon=False, fontsize=10)
ax.set_xlim(1.0, 3.05)
ax.text(0.5, 1.065, "made twice, never found",
        transform=ax.transAxes, color=fg, ha='center', fontsize=16,
        fontweight='bold')
ax.text(0.5, 1.005,
        "the fold fixes 110 arithmetically \u2014 P=(I+R)/2, no arrival \u2022 "
        "the mirror fixes it geometrically \u2014 xy=110\u00b2, any silver pair \u2022 "
        "they agree only at the count; apart by the toll",
        transform=ax.transAxes, color=dim, ha='center', fontsize=9)
fig.tight_layout(rect=[0, 0, 1, 0.93])
plt.savefig('assets/two-averages-toll-cover.png', dpi=200,
            bbox_inches='tight', facecolor='#0c0d10')
print("wrote assets/two-averages-toll-cover.png")
