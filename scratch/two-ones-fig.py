import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# ---- data from the transfer-operator computation ----
import json
data = json.load(open('scratch/two-ones-data.json'))
Ks = np.array(data['K'])
dims = np.array(data['dim'])

BG = '#0a0a0f'; TXT = '#d6d3d1'; SUB = '#8a8885'
CY = '#38bdf8'; GOLD = '#fbbf24'; RED = '#ef4444'; REDS = '#f87171'
BLUE = '#60a5fa'; SEA = '#0e2233'

# exact dimensions for the dust rows
d_by_K = {1: 0.0, 2: 0.5313, 3: 0.7057, 5: 0.8368, 8: 0.9046, 13: 0.9445}

def cylinders(K, n):
    """All cylinder intervals of depth n for digits in {1..K}: (p_k/q_k) fractions.
    Returns array of (lo, hi) with the exact endpoints via (p_n+p_{n-1})/(q_n+q_{n-1})
    and p_n/q_n — the cylinder is the interval between the two adjacent convergents."""
    N = K**n
    p = np.zeros((N, n+2), dtype=np.int64)
    q = np.zeros((N, n+2), dtype=np.int64)
    # standard convergent indexing: p_{-1}=1, p_0=0, q_{-1}=0, q_0=1
    p[:, 0] = 1
    q[:, 1] = 1
    # build words row-wise: iterate digits
    words = np.zeros((N, n), dtype=np.int64)
    for j in range(n):
        rep = K**(n-1-j)
        words[:, j] = np.tile(np.repeat(np.arange(1, K+1), rep), K**j)
    for k in range(n):
        a = words[:, k]
        p[:, k+2] = a*p[:, k+1] + p[:, k]
        q[:, k+2] = a*q[:, k+1] + q[:, k]
    pn, qn = p[:, n+1], q[:, n+1]
    pn1, qn1 = p[:, n], q[:, n]
    e1 = pn/qn
    e2 = (pn+pn1)/(qn+qn1)
    lo = np.minimum(e1, e2)
    hi = np.maximum(e1, e2)
    return lo, hi, qn

fig = plt.figure(figsize=(15, 8.2), dpi=200)
fig.patch.set_facecolor(BG)

# ================= Panel A: the dust thickens, the measure stays empty =========
ax1 = fig.add_axes([0.05, 0.14, 0.40, 0.76])
ax1.set_facecolor(BG)

rows = [(1, 6), (2, 6), (3, 6), (5, 6), (8, 5), (13, 4)]
labels = []
for i, (K, n) in enumerate(rows):
    y = i
    lo, hi, qn = cylinders(K, n)
    yy = np.full_like(lo, y)
    segs = np.array([np.column_stack([lo, yy]), np.column_stack([hi, yy])]).transpose(1, 0, 2)
    lc = LineCollection(segs, linewidths=0.8, colors=CY, alpha=0.55)
    ax1.add_collection(lc)
    labels.append(f'K={K}   d={d_by_K[K]:.3f}')

ax1.set_xlim(0, 1); ax1.set_ylim(-0.6, len(rows)-0.4)
ax1.set_yticks(range(len(rows)))
ax1.set_yticklabels(labels, fontsize=9, color=SUB, fontfamily='monospace')
ax1.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
ax1.tick_params(colors=SUB, labelsize=8)
for s in ['top', 'right']: ax1.spines[s].set_visible(False)
for s in ['left', 'bottom']: ax1.spines[s].set_color('#3f3f46')
ax1.set_title('the dust thickens — the measure stays empty', color=TXT, fontsize=11, pad=10)
ax1.text(0.02, -0.42, 'every row measure zero (λ\u2081 < 1) — the count sees nothing.\n'
                      'the dimension climbs to 1 — the where sees everything.',
         color=SUB, fontsize=8, va='bottom', family='monospace')

# ================= Panel B: two ones — measure vs dimension ===================
ax2 = fig.add_axes([0.56, 0.14, 0.40, 0.76])
ax2.set_facecolor(BG)
ax2.set_xlim(0, 1); ax2.set_ylim(-0.1, 1.15)
ax2.axis('off')

# left meter: Lebesgue measure
ax2.add_patch(plt.Rectangle((0.03, 0.0), 0.34, 0.9, color=RED, alpha=0.85))
ax2.add_patch(plt.Rectangle((0.03, 0.0), 0.34, 0.004, color=BLUE, alpha=0.9))
ax2.text(0.2, 0.47, '1', color='white', fontsize=13, ha='center', va='center', fontweight='bold')
ax2.text(0.2, 0.02, '0', color=BLUE, fontsize=10, ha='center', va='bottom')
ax2.text(0.2, -0.12, 'crossings: measure 1\nthe count\'s reading', color=TXT, fontsize=8.5, ha='center', va='top')
ax2.text(0.035, 0.018, 'the holds: measure 0 — a hairline', color=BLUE, fontsize=7.5, va='bottom')

# right meter: Hausdorff dimension
ax2.add_patch(plt.Rectangle((0.66, 0.0), 0.34, 0.9, color=RED, alpha=0.45))
ax2.add_patch(plt.Rectangle((0.66, 0.0), 0.34, 0.9, color=BLUE, alpha=0.55))
ax2.text(0.83, 0.47, '1', color='white', fontsize=13, ha='center', va='center', fontweight='bold')
ax2.text(0.83, -0.12, 'both: dimension 1 (Jarník)\nthe where\'s reading', color=TXT, fontsize=8.5, ha='center', va='top')

ax2.plot([0.54, 0.54], [0, 0.9], color=SUB, lw=1, ls=(0, (3, 2)))
ax2.text(0.54, 0.95, 'the second ear\nwas the dimension', color=GOLD, fontsize=9, ha='center', va='bottom', fontfamily='monospace')
ax2.text(0.5, -0.30, 'two ones, disjoint, both full —\n'
                     'the count reads measure; the where reads dimension.',
         color=TXT, fontsize=10, ha='center', va='top', family='monospace')

# ================= inset: d_K rising to 1 ====================================
ax3 = fig.add_axes([0.60, 0.66, 0.33, 0.22])
ax3.set_facecolor(BG)
ax3.plot(Ks, dims, color=GOLD, lw=2)
ax3.axhline(1.0, color=SUB, lw=0.8, ls=(0, (3, 2)))
ax3.text(24.5, 1.012, 'full — 1', color=SUB, fontsize=8, family='monospace')
ax3.plot([1], [0], 'o', ms=4, color=RED)
ax3.text(1.2, 0.02, 'φ: a point', color=REDS, fontsize=8, family='monospace')
ax3.annotate('K=2: 0.531', (2, 0.5313), xytext=(8, 0.36),
             fontsize=8, color=GOLD, family='monospace',
             arrowprops=dict(arrowstyle='-', color=GOLD, lw=0.5))
ax3.set_xlim(0.5, 30); ax3.set_ylim(0, 1.05)
ax3.set_xlabel('digit bound K', color=SUB, fontsize=8)
ax3.set_ylabel('dimension d(K)', color=SUB, fontsize=8)
ax3.tick_params(colors=SUB, labelsize=7)
for s in ['top', 'right']: ax3.spines[s].set_visible(False)
for s in ['left', 'bottom']: ax3.spines[s].set_color('#3f3f46')
ax3.set_title('the union of the dust is dimension-full', color=TXT, fontsize=9)

fig.text(0.5, 0.015, 'a number is a crossing (quotients unbounded, measure one) or a hold (quotients bounded, measure zero, dimension one). '
                     'the count cannot see the holds at any finite bound — the where reads them everywhere.',
         color=SUB, fontsize=9, ha='center', family='monospace')

plt.savefig('assets/two-ones.png', dpi=200, bbox_inches='tight', facecolor=BG)
print('saved assets/two-ones.png')
