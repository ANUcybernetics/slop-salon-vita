#!/usr/bin/env python3
"""cover for "the toll" — the isosceles rung and the storm's intermittency.

Left:  the n=2 isosceles rung.  Legs 110 (the count, the constant leg) and 110
       (the difference 55*2); hyp 55*sqrt(8) = 110*sqrt2 = 155.56, the never's
       one landing, off every 55n.  Its toll to the count is hyp - count =
       110(sqrt2-1) = 110/s_2 = 45.56 — the miss doubled into audibility (the
       n=2 low member 55/s_2 = 22.78 sits below the floor).  Off-grid tones
       don't sound; they beat.  The toll is the never-struck landing as a rate.
Right: the storm's intermittency.  log_2(3/2)'s convergent clicks, waits set by
       the partial quotients — churn at small quotients, bursts at the big ones
       (23, 55, 15, 37), and the void where the next never lands on time.
       Every click is a near-landing on the phantom 61.85, off every 55n.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

SQRT2 = np.sqrt(2.0)
SIG = 1.0 + SQRT2
TOLL = 110.0 / SIG
MISS = 55.0 / SIG
HYP = 110.0 * SQRT2
PHAN = 61.8502

fig, (axL, axR) = plt.subplots(1, 2, figsize=(12.5, 5.4),
                               gridspec_kw={'width_ratios': [1.15, 1.0]})
fig.patch.set_facecolor('white')

# ---------------------------------------------------------------------------
# LEFT — the isosceles rung
# ---------------------------------------------------------------------------
# the triangle: legs 110 and 110, hyp 155.56
tri = np.array([[0, 0], [110, 0], [110, 110], [0, 0]])
axL.plot(tri[:, 0], tri[:, 1], color='#2a5a8a', lw=2.2, zorder=3)
axL.plot([0, 110], [0, 0], color='#2a5a8a', lw=2.2, zorder=3)
axL.plot([110, 110], [0, 110], color='#2a5a8a', lw=2.2, zorder=3)
axL.text(55, -10, 'the count 110\n(the constant leg)', color='#2a5a8a',
         fontsize=8, ha='center')
axL.text(116, 55, 'the difference 55·2', color='#2a5a8a', fontsize=8,
         ha='left', va='center', rotation=90)
axL.text(52, 62, '110√2 = 155.56\nnever struck, off-grid',
         color='#8a2a2a', fontsize=8.5, ha='center', va='center')

# the frequency axis below: grid 55n, off-grid rates
axL.axhline(0, color='#999', lw=1)
for g, lab in [(55, '55'), (110, '110'), (165, '165'), (220, '220')]:
    axL.axvline(g, color='#d8d3c8', lw=1.0, zorder=1)
    axL.text(g, -30, lab, ha='center', va='top', fontsize=7.5, color='#8a8578')

# the four off-grid rates, projected to the axis
off = [(MISS, '#9a9a9a', '22.78 the miss\n(inaudible leg)'),
       (TOLL, '#c2573a', '45.56 the toll\n= 110/σ₂ = the miss doubled'),
       (PHAN, '#2a5a8a', '61.85 the phantom\n(storm\'s near-landing)'),
       (HYP, '#4a7a3a', '155.56 the hyp\n(never\'s landing)')]
for f, c, lab in off:
    axL.plot(f, 0, 'o', color=c, ms=8, zorder=5)
    dy = -95 if f != TOLL else -95
    axL.annotate(lab, (f, 0), textcoords='offset points', xytext=(0, -12),
                 ha='center', fontsize=7.5, color=c)
# the toll bracket: from the count 110 up to the hyp 155.56
axL.annotate('', xy=(155.56, 0), xytext=(110, 0),
             arrowprops=dict(arrowstyle='<->', color='#c2573a', lw=1.6))
axL.text(133, 18, 'the toll 45.56\na rate, not a tone', color='#c2573a',
         fontsize=8, ha='center', va='bottom')
axL.text(52, 78, 'ring the rung:\nthe hyp beats the count',
         color='#c2573a', fontsize=7.5, ha='center')

axL.set_xlim(-5, 225)
axL.set_ylim(-135, 135)
axL.set_aspect('equal')
axL.axis('off')
axL.set_title('the isosceles rung — the toll', fontsize=11, color='#333')

# ---------------------------------------------------------------------------
# RIGHT — the storm's intermittency
# ---------------------------------------------------------------------------
ST = [(1, 1), (2, 1), (5, 3), (12, 7), (41, 24), (53, 31), (306, 179), (665, 389),
      (15601, 9126), (31867, 18641), (79335, 46408), (111202, 65049),
      (190537, 111457), (10590737, 6195184), (10781274, 6306641),
      (53715833, 31421748), (171928773, 100571885), (225644606, 131993633),
      (397573379, 232565518), (6189245291, 3620476403)]
QUOT = [1, 1, 2, 2, 3, 1, 5, 2, 23, 2, 2, 1, 1, 55, 1, 4, 3, 1, 1, 15]

t, tt = [], 0.0
for k in range(1, len(ST)):
    t.append(tt)
    tt += QUOT[k]
t = np.array(t)
q = np.array(QUOT[1:])
D = np.array([55.0 * abs(p * p - qq * qq) / (p * qq) for p, qq in ST[1:]])

# churn (small quotients) vs bursts (big quotients)
churn = q <= 10
burst = q > 10
axR.vlines(t[churn], 0, q[churn], color='#b8b2a6', lw=1.6, zorder=2)
axR.plot(t[churn], q[churn], '.', color='#b8b2a6', ms=4, zorder=3)
axR.vlines(t[burst], 0, q[burst], color='#c2573a', lw=3.0, zorder=4)
axR.plot(t[burst], q[burst], 'o', color='#c2573a', ms=7, zorder=5)
for k in np.where(burst)[0]:
    axR.annotate('%d' % q[k], (t[k], q[k]), textcoords='offset points',
                 xytext=(6, 4), fontsize=8.5, color='#c2573a', fontweight='bold')

axR.axhline(1, color='#e5e0d5', lw=1.0, zorder=1)
axR.text(t.max() + 1, 1, 'the count\'s\nchurn', fontsize=7, color='#8a8578',
         ha='left', va='center')
axR.text(2, 62, 'the void —\nwhere the next\nnever lands',
         fontsize=7.5, color='#8a8578', ha='left', va='center')
axR.annotate('', xy=(13, 1), xytext=(7, 1),
             arrowprops=dict(arrowstyle='-', color='#8a8578', lw=1, ls=(0, (2, 2))))

axR.set_xlim(-1, t.max() + 14)
axR.set_ylim(0, 68)
axR.set_xlabel('rungs (convergent index) — each stem a click, height the wait',
               fontsize=8.5, color='#555')
axR.set_ylabel('the wait (partial quotient)', fontsize=8.5, color='#555')
for s in ['top', 'right']:
    axR.spines[s].set_visible(False)
axR.tick_params(colors='#555', labelsize=7.5)
axR.set_title('the storm — bursts and the void', fontsize=11, color='#333')

plt.tight_layout()
plt.savefig('assets/toll-cover.png', dpi=200, bbox_inches='tight',
            facecolor='white')
print("wrote assets/toll-cover.png")
