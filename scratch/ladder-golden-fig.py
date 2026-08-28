import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

phi = (1 + 5**0.5) / 2
GOLD = 1/phi**2          # 0.381966  the limit
WIRSING = 0.3036630029   # lambda_2
ONE_E = 1/np.e

# true ladder (multi-M stable)
ls = [1.0, -0.3036630029, 0.1008845093, -0.0354961590, 0.0128437905, -0.0047177798, 0.0017486638]
n = np.arange(1, len(ls)+1)
rs = [abs(ls[k+1]/ls[k]) for k in range(len(ls)-1)]   # ratio climb, r_1..r_6

# ratio r_7 from the note's lambda_8 = -0.00065430
rs.append(abs(-0.00065430/0.0017486638))

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.6, 8.6), facecolor='#0d0d12')
for ax in (ax1, ax2):
    ax.set_facecolor('#0d0d12')
    for s in ax.spines.values(): s.set_color('#555')
    ax.tick_params(colors='#bbb', labelsize=9)

# ---- panel A: the signed ladder ----
cr = np.cbrt  # cube-root scale so small rungs stay visible
for i, l in enumerate(ls):
    pos = l > 0
    color = '#e8b64c' if pos else '#e07a9a'
    h = cr(abs(l)) * 1.6
    ax1.plot([i+1, i+1], [0, h if pos else -h], color=color, lw=2.6, alpha=0.95)
    ax1.plot(i+1, h if pos else -h, 'o', color=color, ms=5)
    ax1.text(i+1, (h if pos else -h) + (0.10 if pos else -0.22), f'{l:+.4f}',
             color='#ddd', ha='center', va='bottom' if pos else 'top', fontsize=8.5)
# golden spacing guide: gap between consecutive magnitudes shrinks by 1/phi^2
ax1.axhline(0, color='#666', lw=0.8)
ax1.set_xticks(n); ax1.set_xticklabels([f'λ{n}' for n in range(1, len(ls)+1)], fontsize=10)
ax1.set_ylabel('magnitude (cube-root)', color='#ccc', fontsize=9)
ax1.set_title('the ladder, tight onto the golden floor', color='#eee', fontsize=12, loc='left', pad=10)
ax1.set_ylim(-1.7, 1.9)
ax1.text(0.02, 0.95, 'each gap a factor φ² shallower — sign flips every rung',
         transform=ax1.transAxes, color='#9aa', fontsize=8.5, va='top')

# ---- panel B: the ratio climb, correcting 1/e ----
nr = np.arange(1, len(rs)+1)
ax2.axhline(GOLD, color='#e8b64c', lw=1.4, ls=(0,(4,2)))
ax2.text(len(rs)+0.15, GOLD, 'the golden floor  1/φ² = 0.382', color='#e8b64c',
         fontsize=9, va='center')
ax2.axhline(ONE_E, color='#7ac0e0', lw=1.1, ls=(0,(2,2)))
ax2.text(len(rs)+0.15, ONE_E, '1/e — a rung, not the limit', color='#7ac0e0',
         fontsize=8.5, va='center')
ax2.axhline(0.36, color='#666', lw=0.9, ls=':')
ax2.text(len(rs)+0.15, 0.36, "×0.36, lelia's low rungs", color='#888', fontsize=8, va='center')
ax2.plot(nr, rs, 'o-', color='#c9a2ff', lw=1.6, ms=6)
for i, r in enumerate(rs):
    ax2.text(nr[i], r + 0.006, f'{r:.4f}', color='#d9c2ff', ha='center', fontsize=8)
# mark the crossing of 1/e between r5 and r6
ax2.annotate('', xy=(5, ONE_E), xytext=(6, ONE_E),
             arrowprops=dict(arrowstyle='-', color='#7ac0e0', lw=1.0))
ax2.text(5.5, ONE_E + 0.012, 'crossed here', color='#7ac0e0', fontsize=8, ha='center')
ax2.set_xticks(nr); ax2.set_xticklabels([f'r{n}' for n in range(1, len(rs)+1)], fontsize=10)
ax2.set_ylabel('|λₙ₊₁ / λₙ|', color='#ccc', fontsize=11)
ax2.set_title('the ratio climbs to φ, not e', color='#eee', fontsize=12, loc='left', pad=10)
ax2.set_xlim(0.5, len(rs)+0.3); ax2.set_ylim(0.27, 0.42)
ax2.text(0.02, 0.95, 'first rung r₁ = λ₂ itself — the only exact scale, 0.30366',
         transform=ax2.transAxes, color='#9aa', fontsize=8.5, va='top')

fig.suptitle('', )
fig.tight_layout()
fig.savefig('ladder-golden.png', dpi=200, bbox_inches='tight', facecolor='#0d0d12')
print('saved ladder-golden.png')
