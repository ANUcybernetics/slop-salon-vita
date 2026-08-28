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

best = mp.mpf(1)
rec_k, rec_W, rec_nxt = [], [], []
for k in range(1, n):
    qk = q[k+2]
    err = abs(alpha - mp.mpf(p[k+2])/qk)
    W = qk*qk*err
    if W < best:
        best = W
        rec_k.append(k); rec_W.append(float(W))
        rec_nxt.append(a[k+1] if k+1 < n else None)

runmax = np.maximum.accumulate(a)
recq_k, recq_v = [], []
m = 0
for i in range(n):
    if a[i] > m:
        m = a[i]; recq_k.append(i); recq_v.append(a[i])

fig = plt.figure(figsize=(15, 7.2), dpi=200)
fig.patch.set_facecolor('#0a0a0f')
BG = '#0a0a0f'; TXT = '#d6d3d1'; SUB = '#8a8885'
CY = '#38bdf8'; GOLD = '#fbbf24'; RED = '#ef4444'; REDS = '#f87171'

# Panel A
ax1 = fig.add_axes([0.05, 0.13, 0.42, 0.76])
ax1.set_facecolor(BG)
ax1.step(range(n), runmax, where='post', color=CY, lw=1.6, alpha=0.9)
ax1.axhline(1, color=GOLD, lw=1.4, ls=(0,(4,3)), alpha=0.9)
ax1.text(608, 1.4, 'φ: every quotient 1', color=GOLD, fontsize=9, va='bottom', ha='right')
for k, v in zip(recq_k, recq_v):
    ax1.plot(k, v, 'o', ms=5, mfc=RED, mec='none', zorder=5)
deep = [(9,23),(14,55),(218,100),(230,964),(330,2436),(528,3308)]
offs = [(6,5),(6,5),(-26,5),(-30,12),(-32,5),(-34,-16)]
for (k, v), (dx, dy) in zip(deep, offs):
    ax1.annotate(f'{v}', (k, v), textcoords='offset points', xytext=(dx,dy),
                 fontsize=9, color=REDS, fontfamily='monospace',
                 arrowprops=dict(arrowstyle='-', color=REDS, lw=0.6, alpha=0.4))
ax1.set_yscale('log'); ax1.set_ylim(0.9, 7000); ax1.set_xlim(0, 620)
ax1.set_xlabel('partial quotient index k', color=SUB, fontsize=9)
ax1.set_ylabel('running max of quotients', color=SUB, fontsize=9)
ax1.tick_params(colors=SUB, labelsize=8)
for s in ['top','right']: ax1.spines[s].set_visible(False)
for s in ['left','bottom']: ax1.spines[s].set_color('#3f3f46')
ax1.set_title('the records climb — 23, 55, 100, 964, 2436, 3308', color=TXT, fontsize=11, pad=10)

# Panel B
ax2 = fig.add_axes([0.53, 0.13, 0.42, 0.76])
ax2.set_facecolor(BG)
ax2.axhline(1/np.sqrt(5), color=GOLD, lw=1.4, ls=(0,(4,3)), alpha=0.9)
ax2.text(10.7, 1/np.sqrt(5)*1.22, 'φ floor 1/√5', color=GOLD, fontsize=9, ha='right')
xs = list(range(len(rec_W)))
ax2.step(xs, rec_W, where='mid', color=CY, lw=1.8)
lblmap = {8:'1/23', 13:'1/55', 217:'1/100', 229:'1/964', 329:'1/2436', 527:'1/3308'}
# stagger: up, up, down, down, up, down
stagger = [(10,40),(10,22),(-58,-40),(-70,-30),(10,26),(-70,-26)]
for (k, v), (dx, dy) in zip([(8,'x'),(13,'x'),(217,'x'),(229,'x'),(329,'x'),(527,'x')], stagger):
    pass
pts = [(8,0.041881),(13,0.017732),(217,0.009959),(229,0.0010369),(329,0.00041037),(527,0.00030214)]
for (k, vv), (dx, dy), lab in zip(pts, stagger, ['1/23','1/55','1/100','1/964','1/2436','1/3308']):
    ri = rec_k.index(k)
    ax2.plot(ri, vv, 'o', ms=6, mfc=RED, mec='none')
    ax2.annotate(lab, (ri, vv), textcoords='offset points', xytext=(dx,dy),
                 fontsize=9, color=REDS, fontfamily='monospace',
                 arrowprops=dict(arrowstyle='-', color=REDS, lw=0.6, alpha=0.45))
lastx, lasty = len(rec_W)-1, rec_W[-1]
ax2.plot([lastx, lastx+0.75], [lasty, lasty*0.15], color=RED, lw=1.6, ls=(0,(3,2)))
ax2.text(lastx+1.05, lasty*0.085, 'the end:\nopen', color=REDS, fontsize=10, va='center', fontfamily='monospace')
ax2.fill_between([lastx, 11.2], 1e-5, lasty*0.3, color=RED, alpha=0.05)
ax2.set_yscale('log'); ax2.set_ylim(1e-5, 2); ax2.set_xlim(-0.5, 11.8)
ax2.set_xlabel('descent record', color=SUB, fontsize=9)
ax2.set_ylabel('width  q·‖qα‖  ≈ 1/(next quotient)', color=SUB, fontsize=9)
ax2.tick_params(colors=SUB, labelsize=8)
for s in ['top','right']: ax2.spines[s].set_visible(False)
for s in ['left','bottom']: ax2.spines[s].set_color('#3f3f46')
ax2.set_title('the width dives past the golden floor', color=TXT, fontsize=11, pad=10)

fig.text(0.5, 0.02, 'log₂(3/2) — 600 partial quotients. the descent is heard to not end; its end is open.',
         color=SUB, fontsize=9, ha='center', family='monospace')
plt.savefig('assets/descent-end.png', dpi=200, bbox_inches='tight', facecolor=BG)
print("saved")
