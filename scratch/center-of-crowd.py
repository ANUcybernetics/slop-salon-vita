import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np, math

plt.rcParams.update({
    'figure.facecolor': '#0a0e1a', 'axes.facecolor': '#0a0e1a',
    'savefig.facecolor': '#0a0e1a', 'axes.edgecolor': '#8892b0',
    'axes.labelcolor': '#c9d1e6', 'xtick.color': '#8892b0',
    'ytick.color': '#8892b0', 'text.color': '#c9d1e6',
    'font.family': 'serif', 'font.size': 11,
})
GOLD = '#e8b84b'; CYAN = '#5ad1e0'; DIM = '#8892b0'; RED = '#e06a6a'
L = math.log(2.0)
med_th = 1.0/(L*L)  # 2.081

# --- Panel A: the deepest dive is the center, not the exception ---
n = 479173
mx = np.load('/home/sprite/slop-salon-vita/scratch/maxdist.npy')
rat = np.sort(mx) / n
ys = np.arange(1, len(rat)+1)/len(rat)
r0 = 1138268 / n

fig = plt.figure(figsize=(11, 8))
ax = fig.add_subplot(2, 1, 1)
ax.plot(rat, ys, color=CYAN, lw=2.0, label='generic walks: ECDF of deepest quotient ÷ rungs')
ax.axvline(med_th, color=DIM, ls='--', lw=1.2, label='asymptotic median 1/ln²2 = 2.081')
ax.axvline(r0, color=GOLD, ls='-', lw=2.0, label="the fifth's record 1138268 ÷ 479173 = 2.375")
ax.axhline(0.5, color=DIM, ls=':', lw=1.0)
pct = (rat < r0).mean()
ax.plot(r0, pct, 'o', color=GOLD, ms=10)
ax.annotate(f'{pct*100:.0f}th pct — the deepest dive\nIS the center of the crowd',
            (r0, pct), xytext=(r0+0.9, 0.63), fontsize=10, color='#e6eaf6')
ax.set_xlabel('deepest quotient ÷ rungs n'); ax.set_ylabel('fraction of walks')
ax.set_title('the deepest dive is the center, not the exception', color='#e6eaf6', fontsize=12)
ax.legend(loc='lower right', fontsize=9, framealpha=0.3)
ax.set_xlim(0, 9); ax.set_ylim(0, 1.02)
ax.grid(alpha=0.15)

# --- Panel B: no characteristic scale ---
ax2 = fig.add_subplot(2, 1, 2)
scales = [6000, 250000, 479173, 700000]
d = np.load('scratch/scale-free.npy', allow_pickle=True).item()
meds = [d[s]['med'] for s in scales]
p25 = [d[s]['p25'] for s in scales]
p75 = [d[s]['p75'] for s in scales]
p90 = [d[s]['p90'] for s in scales]
ax2.plot(scales, meds, 'o-', color=CYAN, lw=1.8, label='median — flat at ~2·n')
ax2.fill_between(scales, p25, p75, color=CYAN, alpha=0.12, label='25–75th pct')
ax2.plot(scales, p90, '^--', color=GOLD, lw=1.0, ms=6, label='90th pct — the rare giant')
ax2.axhline(med_th, color=DIM, ls=':', lw=1.2)
ax2.annotate('mean? no mean —\nthe tail is Pareto-1',
             (scales[1], p90[1]), xytext=(scales[1]*0.9, 22), fontsize=10, color=RED)
ax2.text(scales[3], meds[3]+0.7, f'median {meds[3]:.2f}', color=CYAN, fontsize=9)
ax2.set_xscale('log'); ax2.set_xlabel('rungs n'); ax2.set_ylabel('deepest quotient ÷ n')
ax2.set_title('no characteristic scale — a floor and a pause are identical at every scale', color='#e6eaf6', fontsize=12)
ax2.legend(loc='upper left', fontsize=9, framealpha=0.3)
ax2.set_ylim(0, 30)
ax2.grid(alpha=0.15)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-vita/assets/center-of-crowd.png', dpi=200, bbox_inches='tight')
print('saved assets/center-of-crowd.png')
