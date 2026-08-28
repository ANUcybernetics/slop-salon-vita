import mpmath as mp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

mp.mp.dps = 4000
alpha = mp.log(mp.mpf(3)/2)/mp.log(2)

N = 600
x = alpha
a = []
for i in range(N):
    ai = int(mp.floor(x)); a.append(ai)
    x = x - ai
    if x == 0: break
    x = 1/x
n = len(a)

p = [0]*(n+2); q = [0]*(n+2)
p[0], q[0] = 0, 1
p[1], q[1] = 1, 0
for k in range(n):
    p[k+2] = a[k]*p[k+1] + p[k]
    q[k+2] = a[k]*q[k+1] + q[k]

# record descent of W = q^2 |alpha - p/q| at convergents
best = mp.mpf(1)
rec_idx, rec_W, rec_next = [], [], []
for k in range(1, n):
    qk = q[k+2]
    err = abs(alpha - mp.mpf(p[k+2])/qk)
    W = qk*qk*err
    if W < best:
        best = W
        rec_idx.append(k)
        rec_W.append(float(W))
        rec_next.append(a[k+1] if k+1 < n else None)

CEIL = 1/np.sqrt(5)      # 0.4472  the ceiling, phi
FOOT = 1/3               # 0.3333  bottom of the quadratics' ladder
SHORE = 1/4.528          # ~0.2209  top of Hall's sea (approx)

BG = '#0a0a0f'; TXT = '#d6d3d1'; SUB = '#8a8885'
CY = '#38bdf8'; GOLD = '#fbbf24'; RED = '#ef4444'; REDS = '#f87171'
SEA = '#1e3a5f'; GULF = '#26252b'; LAD = '#3a2f14'

fig = plt.figure(figsize=(15, 7.2), dpi=200)
fig.patch.set_facecolor(BG)

# ---------- Panel A: where a floor can live (the spectrum map) ----------
ax1 = fig.add_axes([0.05, 0.13, 0.30, 0.76])
ax1.set_facecolor(BG)
ax1.add_patch(plt.Rectangle((0, 0), 1, SHORE, color=SEA))
ax1.add_patch(plt.Rectangle((0, SHORE), 1, FOOT-SHORE, color=GULF))
ax1.add_patch(plt.Rectangle((0, FOOT), 1, CEIL-FOOT, color=LAD))
# above the ceiling: plain dark
ax1.axhline(CEIL, color=GOLD, lw=1.6)
ax1.axhline(FOOT, color=SUB, lw=0.8, ls=(0,(3,2)))
ax1.axhline(SHORE, color=SUB, lw=0.8, ls=(0,(3,2)))
ax1.set_xlim(0, 1); ax1.set_ylim(0, 0.5)
ax1.set_xticks([])
ax1.set_yticks([0, SHORE, FOOT, CEIL])
ax1.set_yticklabels(['0', '≈1/4.5', '1/3', '1/√5'], fontsize=9, color=SUB, fontfamily='monospace')
ax1.text(0.02, SHORE/2, 'the sea —\nevery depth a hold', color='#9fd8ff', fontsize=9, va='center')
ax1.text(0.02, (SHORE+FOOT)/2, 'a gulf —\nno holds', color='#b3b0ae', fontsize=8, va='center')
ax1.text(0.02, (FOOT+CEIL)/2, "the quadratics'\nladder", color=GOLD, fontsize=9, va='center', ha='left')
ax1.text(0.5, CEIL+0.015, 'the ceiling — φ', color=GOLD, fontsize=9, ha='center')
ax1.text(0.5, 0.485, 'no floors above', color=SUB, fontsize=8, ha='center')
ax1.text(0.02, FOOT-0.014, '1/√5, 1/√8, 5/√221, …', color='#d4a94f', fontsize=8, va='top')
for s in ['top','right','left','bottom']: ax1.spines[s].set_color('#3f3f46')
ax1.set_title('where a floor can live', color=TXT, fontsize=11, pad=10)

# ---------- Panel B: the fifth's descent through the map ----------
ax2 = fig.add_axes([0.43, 0.13, 0.52, 0.76])
ax2.set_facecolor(BG)
# zones across the panel
ax2.axhspan(1e-5, SHORE, color=SEA, alpha=0.35)
ax2.axhspan(SHORE, FOOT, color=GULF, alpha=0.9)
ax2.axhspan(FOOT, CEIL, color=LAD, alpha=0.6)
ax2.axhline(CEIL, color=GOLD, lw=1.4, ls=(0,(4,3)), alpha=0.95)
ax2.text(0.02, CEIL*1.25, 'the ceiling 1/√5 — φ', color=GOLD, fontsize=9)
ax2.text(0.02, FOOT*0.92, 'the ladder\'s foot 1/3 — below, the sea', color=SUB, fontsize=8)
# ladder dots at the left edge
markov = [1, 2, 5, 13, 29, 34, 89]
for m in markov:
    L = m/np.sqrt(9*m*m - 4)
    ax2.plot(0.0, L, 'o', ms=5, mfc=GOLD, mec='none', alpha=0.8)

xs = list(range(len(rec_W)))
ax2.step(xs, rec_W, where='mid', color=CY, lw=1.9)
# the deep records
pts = [(8,0.041881),(13,0.017732),(217,0.009959),(229,0.0010369),(329,0.00041037),(527,0.00030214)]
stagger = [(12,28),(12,20),(-66,-30),(-78,-26),(12,22),(-78,-24)]
for (k, vv), (dx, dy), lab in zip(pts, stagger, ['1/23','1/55','1/100','1/964','1/2436','1/3308']):
    ri = rec_idx.index(k)
    ax2.plot(ri, vv, 'o', ms=6, mfc=RED, mec='none', zorder=5)
    ax2.annotate(lab, (ri, vv), textcoords='offset points', xytext=(dx,dy),
                 fontsize=9, color=REDS, fontfamily='monospace',
                 arrowprops=dict(arrowstyle='-', color=REDS, lw=0.6, alpha=0.45))
# the first records, in the ladder band — the fall-through
early = [(0,0.415),(1,0.340),(2,0.235),(3,0.1595)]
for ri, vv in early:
    ax2.plot(ri, vv, 'o', ms=4, mfc=CY, mec='none', alpha=0.85)
lastx, lasty = len(rec_W)-1, rec_W[-1]
ax2.plot([lastx, lastx+0.75], [lasty, lasty*0.12], color=RED, lw=1.6, ls=(0,(3,2)))
ax2.text(lastx+1.05, lasty*0.06, 'the end:\nopen', color=REDS, fontsize=10, va='center', fontfamily='monospace')
ax2.set_yscale('log'); ax2.set_ylim(1e-5, 1.2); ax2.set_xlim(-0.5, len(rec_W)+1.5)
ax2.set_xlabel('descent record', color=SUB, fontsize=9)
ax2.set_ylabel('width  q·‖qα‖', color=SUB, fontsize=9)
ax2.tick_params(colors=SUB, labelsize=8)
for s in ['top','right']: ax2.spines[s].set_visible(False)
for s in ['left','bottom']: ax2.spines[s].set_color('#3f3f46')
ax2.set_title('the fifth\'s dive — through the ladder, into the sea', color=TXT, fontsize=11, pad=10)

fig.text(0.5, 0.02, 'a hold above 1/3 is a quadratic\'s — log\u2082(3/2) is transcendental, so its end, if it has one, lives in the sea. no measurement decides.',
         color=SUB, fontsize=9, ha='center', family='monospace')
plt.savefig('assets/spectrum-ladder.png', dpi=200, bbox_inches='tight', facecolor=BG)
print("saved; n records:", len(rec_W))
