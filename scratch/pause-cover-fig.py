import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    'figure.facecolor': '#0a0e1a', 'axes.facecolor': '#0a0e1a',
    'savefig.facecolor': '#0a0e1a', 'axes.edgecolor': '#8892b0',
    'axes.labelcolor': '#c9d1e6', 'xtick.color': '#8892b0',
    'ytick.color': '#8892b0', 'text.color': '#c9d1e6',
    'font.family': 'serif', 'font.size': 11,
})
GOLD = '#e8b84b'; CYAN = '#5ad1e0'; RED = '#e06a6a'; DIM = '#8892b0'

# landings: (time, record, freq) and segment durs from the piece
land = [(0.0, 23, 220.0), (2.2, 55, 196.8), (9.4, 100, 182.3), (12.7, 964, 136.4),
        (18.9, 2436, 121.1), (26.1, 3308, 116.5), (36.5, 4878, 110.8), (46.4, 8228, 103.6),
        (59.3, 24477, 90.1), (70.0, 59599, 80.4), (83.4, 104733, 74.8), (96.8, 110819, 74.3),
        (112.9, 698813, 58.7), (129.9, 1138268, 55.1)]
durs = [2.2, 7.2, 3.4, 6.2, 7.1, 10.4, 9.9, 12.9, 10.7, 13.4, 13.4, 16.1, 17.1, 12.0]
final_open = 141.9

fig, ax = plt.subplots(figsize=(12, 5))
# staircase: each record's freq held for its duration
t0 = 0.0
for i, (t, q, f) in enumerate(land[:-1]):
    d = durs[i]
    ax.plot([t0, t0 + d], [f, f], color=GOLD, lw=2.5)
    ax.plot([t0, t0], [land[i][2], land[i+1][2]], color=GOLD, lw=1.0, alpha=0.5)
    t0 += d
# final open hold: dashed (its end is unknown — a pause or a floor)
ax.plot([t0, final_open], [55.1, 55.1], color=GOLD, lw=2.5, ls=(0, (2, 2)))
ax.plot(t0, 55.1, 'o', color=RED, ms=7)
ax.annotate('1138268 — held, open', (t0, 55.1), textcoords='offset points',
            xytext=(8, -16), color=RED, fontsize=10)
ax.set_xlim(0, 152); ax.set_ylim(40, 240)
ax.set_xlabel('seconds'); ax.set_ylabel('drone pitch (Hz)')
ax.set_title('the pause that broke — the descent, heard as pitch', color='#e6eaf6', fontsize=12)
ax.grid(alpha=0.15)
ax.text(3, 190, 'the count ticks throughout, deaf', color=DIM, fontsize=9)
ax.text(120, 170, '309,448-rung\nsilence', color=CYAN, fontsize=10)
plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-vita/assets/pause-that-broke-cover.png', dpi=200, bbox_inches='tight')
print("saved pause-that-broke-cover.png")
