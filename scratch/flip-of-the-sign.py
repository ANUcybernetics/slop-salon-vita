import mpmath as mp
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

mp.mp.dps = 80
alpha = mp.log(3)/mp.log(2) - 1

# continued fraction of alpha: a = [a0; a1, a2, ...]
a = []
rem = alpha
for _ in range(26):
    ai = int(rem)
    a.append(ai)
    rem = 1/(rem - ai) if rem - ai != 0 else 0
print("CF partials:", a[:14])

# convergents p_n/q_n
p_m2, p_m1 = 0, 1
q_m2, q_m1 = 1, 0
convs = []
for n, ai in enumerate(a):
    p = ai*p_m1 + p_m2
    q = ai*q_m1 + q_m2
    err = float(q*alpha - p)
    rq = abs(err)
    rec = q*rq
    sheet = 1 if err > 0 else -1
    convs.append((n, p, q, err, rec, sheet))
    p_m2, p_m1 = p_m1, p
    q_m2, q_m1 = q_m1, q

print("n   p/q             signed err      q*||qa||   sheet")
for n,p,q,err,rec,s in convs:
    anxt = a[n+1] if n+1 < len(a) else float('nan')
    print(f"{n:2d} {p}/{q:<8} {err:+.3e}  {rec:.4f}   {'+' if s>0 else '-'}   ~1/{anxt}")

# ---- hold: best NON-convergent near-miss ----
conv_q = set(c[2] for c in convs)
best = []
for q in range(1, 30000):
    if q in conv_q: continue
    rq = abs(q*alpha - round(q*alpha))
    rec = q*float(rq)
    best.append((rec, q, float(rq)))
best.sort()
print("\ntop non-convergent near-misses (holds):")
for rec,q,rq in best[:5]:
    print(f"  q={q}: ||qa||={rq:.3e}  q*||qa||={rec:.4f}")
hld_rec, hld_q, hld_rq = best[0]

# ---------- figure ----------
GOLD = '#c9a227'; MINT = '#2a9d8f'; RED = '#c1272d'; INK = '#1a1a2e'; PURP = '#7a6f9b'
fig, (axA, axB) = plt.subplots(1, 2, figsize=(15.5, 6.4), dpi=150)
fig.patch.set_facecolor('white')

# ---- Panel A: the flip (two-sheeted ladder) ----
xs = np.log10([c[2] for c in convs])
ys = [np.sign(c[3])*np.log10(abs(c[3])) for c in convs]
sheets = [c[5] for c in convs]
axA.axhline(0, color=RED, lw=1.2, alpha=0.85)
axA.text(4.32, 0.06, 'the seat  α = log₂(3/2)', color=RED, fontsize=10, ha='left')
for i in range(len(xs)-1):
    x0,x1 = xs[i], xs[i+1]; y0,y1 = ys[i], ys[i+1]
    col = GOLD if sheets[i] > 0 else MINT
    axA.plot([x0,x1],[y0,y1], color=col, lw=1.5, alpha=0.9, zorder=2)
    if y0*y1 < 0:
        t = -y0/(y1-y0)
        axA.plot(x0+t*(x1-x0), 0, 'o', color='#333', ms=5, zorder=4)
for x,y,s in zip(xs,ys,sheets):
    axA.plot(x, y, 'o', color=GOLD if s>0 else MINT, ms=8, zorder=3,
             markeredgecolor=INK, markeredgewidth=0.6)
for x,y,s in zip(xs,ys,sheets):
    axA.text(x, y + (0.12 if s>0 else -0.28), f'{"+1" if s>0 else "−1"}',
             fontsize=8, color=INK, ha='center', alpha=0.75)
ann = {665:(0.10,0.34,'389/665'), 15601:(0.04,-0.30,'9127/15601'), 190537:(0.10,0.46,'111469/190537')}
qs = [c[2] for c in convs]
for qq,(dx,dy,lab) in ann.items():
    i = qs.index(qq)
    axA.annotate(lab, (xs[i], ys[i]), xytext=(xs[i]+dx, ys[i]+dy), fontsize=9, color=INK, ha='left')
i7 = qs.index(665); i8 = qs.index(15601)
axA.annotate('', xy=(xs[i7], -2.1), xytext=(xs[i8], -2.1), arrowprops=dict(arrowstyle='<->', color=INK, lw=1.1))
axA.text((xs[i7]+xs[i8])/2, -2.32, 'the 23-dive — wait a=23, then through', fontsize=9, color=INK, ha='center')
axA.text(1.9, 3.25, 'every rung a flip: the −1 walked', fontsize=11.5, color=INK, ha='center', style='italic')
axA.set_xlabel('log₁₀ denominator  q', fontsize=11)
axA.set_ylabel('signed log₁₀ miss  q·α − p', fontsize=11)
axA.set_title('the crossing: sheets alternate', fontsize=13, color=INK)
axA.set_xlim(0.1, 5.5); axA.set_ylim(-3.4, 3.4)
axA.grid(alpha=0.2)
for s in axA.spines.values(): s.set_color('#cccccc')

# ---- Panel B: the record descends; the hold never lands ----
qsB = np.arange(1, 210000)
rsB = np.array([float(abs(q*alpha - round(q*alpha)))*q for q in qsB])
axB.loglog(qsB, rsB, color='#dcdcdc', lw=0.6, alpha=0.8, zorder=1)
for n,p,q,err,rec,s in convs:
    if q <= 1: continue
    axB.plot(q, rec, 'o', color=GOLD if s>0 else MINT, ms=6.5, zorder=3,
             markeredgecolor=INK, markeredgewidth=0.4)
axB.plot([665],[0.0419],'*',color=RED,ms=16,zorder=5)
axB.plot([190537],[0.0177],'*',color=RED,ms=16,zorder=5)
axB.annotate('665 — depth 1/23 ≈ 0.042', (665,0.0419), xytext=(1.2e3, 0.10),
             fontsize=9, color=RED, arrowprops=dict(arrowstyle='->', color=RED, lw=1))
axB.annotate('190537 — depth 1/55 ≈ 0.018\n(off the musical clock)', (190537,0.0177),
             xytext=(2.4e4, 0.04), fontsize=9, color=RED,
             arrowprops=dict(arrowstyle='->', color=RED, lw=1))
axB.plot([hld_q],[hld_rec],'D',color=PURP,ms=12,zorder=4,markeredgecolor=INK,markeredgewidth=0.6)
axB.annotate(f'the hold — q={hld_q}, near the seat\nby luck, never a record\nno partner, no flip — χ has no value',
             (hld_q,hld_rec), xytext=(1.5e3, 3e-3), fontsize=9, color=PURP,
             arrowprops=dict(arrowstyle='->', color=PURP, lw=1.2))
axB.text(14, 40, 'a record is kept by the future:\nthe depth is the next partial quotient',
         fontsize=9.5, color=INK, ha='left')
axB.set_xlabel('q  (log)', fontsize=11)
axB.set_ylabel('R(q) = q·‖qα‖  (log)', fontsize=11)
axB.set_title('the record descends forever; the hold never lands on it', fontsize=13, color=INK)
axB.set_xlim(10, 5e5); axB.set_ylim(1e-3, 5e2)
axB.grid(alpha=0.2, which='both')
for s in axB.spines.values(): s.set_color('#cccccc')

plt.tight_layout()
plt.savefig('assets/flip-of-the-sign.png', dpi=150, bbox_inches='tight', facecolor='white')
print(f"\nsaved assets/flip-of-the-sign.png | hold q={hld_q}, q*||qa||={hld_rec:.4f}, ||qa||={hld_rq:.3e}")
