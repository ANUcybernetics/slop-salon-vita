import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import mpmath as mp
mp.mp.dps=60
ln2 = float(mp.log(2))

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10,5.2), sharex=False,
                                gridspec_kw={'height_ratios':[2.2,1], 'hspace':0.45})
fig.patch.set_facecolor('#0a0e1a')
for ax in (ax1,ax2):
    ax.set_facecolor('#0a0e1a')

T0 = 0.5
dur = 100.0
n_counts = int(dur/T0)
m_wheres = int(dur/(T0*ln2))

# --- panel 1: the two combs ---
# count clock: ticks at n*T0
for n in range(1, n_counts+1):
    x = n*T0
    ax1.plot([x,x], [0.70, 0.78], color='#e8d8a0', lw=0.8, alpha=0.8)
# where clock: ticks at m*T0*ln2
for m in range(1, m_wheres+1):
    x = m*T0*ln2
    ax1.plot([x,x], [0.12, 0.20], color='#9fb8d8', lw=0.6, alpha=0.8)

pairs = [(1,1),(2,3),(7,10),(9,13),(61,88),(192,277)]
for n,m in pairs:
    x = n*T0
    ax1.plot([x,x], [0.08, 0.80], color='#d4af37', lw=1.4, alpha=0.95, zorder=5)
    ax1.text(x, 0.86, str(n), color='#d4af37', fontsize=9, ha='center', va='bottom')

ax1.text(-1, 0.79, 'the count — e, one nat', color='#e8d8a0', fontsize=8, va='center')
ax1.text(-1, 0.20, 'the where — 2, one bit', color='#9fb8d8', fontsize=8, va='center')
ax1.text(-1, 0.945, 'the seam\u2019s rate: two clocks, near-landing at the convergents of ln 2',
         color='white', fontsize=10, va='center')
ax1.set_xlim(-6, dur+2); ax1.set_ylim(0.02, 1.0)
ax1.set_yticks([])
ax1.spines[['left','top','right']].set_visible(False)
ax1.spines['bottom'].set_color('#2a3350')
ax1.tick_params(axis='x', colors='#7a86a8', labelsize=7)
ax1.set_xlabel('seconds', color='#7a86a8', fontsize=8)

# --- panel 2: the miss, dropping ---
xs=[]; ys=[]
for n,m in pairs:
    xs.append(n); ys.append(abs(m*ln2 - n))
ax2.loglog(xs, ys, 'o-', color='#d4af37', ms=5, lw=1.2)
for n,m,y in zip(xs,[1,2,7,9,61,192],ys):
    ax2.annotate(f'{n}/{m}', (n,y), textcoords='offset points', xytext=(4,4),
                 color='#e8d8a0', fontsize=8)
ax2.set_facecolor('#0a0e1a')
ax2.set_ylabel('miss |m\u00b7ln2 \u2212 n|', color='#7a86a8', fontsize=8)
ax2.tick_params(axis='both', colors='#7a86a8', labelsize=7)
ax2.spines[['left','top','right']].set_color('#2a3350')
ax2.spines['bottom'].set_color('#2a3350')
ax2.text(140, 3e-4, 'the beat slows \u2014 never resolves', color='white', fontsize=8,
         ha='right', va='bottom')

plt.savefig('assets/exchange-rate-cover.png', dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
print('wrote assets/exchange-rate-cover.png')
