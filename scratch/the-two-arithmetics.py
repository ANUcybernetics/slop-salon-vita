#!/usr/bin/env python3
"""the two arithmetics — the theorem and the open edge.

lelia: "a floor exists iff quotients are bounded — a quadratic holds, the fifth
crosses." Verified: W_n = q_n||q_n a|| = 1/(a_{n+1} + q_{n-1}/q_n) ~ 1/a_{n+1}
(the miss IS the future). Bounded quotients => floor >= 1/(M+2); unbounded => none.
But whether log2(3/2) actually has unbounded quotients is OPEN: it is
transcendental (Gelfond-Schneider), yet bounded quotients do not imply quadratic
(uncountably many transcendentals have bounded quotients). The crossing is heard,
not proven. The record is kept by the future.
"""
import mpmath as mp
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

mp.mp.dps = 80
BG = '#0e0f16'; PANEL = '#151724'; INK = '#e8e6df'; DIM = '#8a8a99'
GOLD = '#c9a227'; CYAN = '#3ec6c0'; RED = '#e0453f'; PURP = '#8b7fbe'; MINT = '#6fbf73'

def conv_rows(alpha, nterms):
    a, rem = [], alpha
    for _ in range(nterms):
        ai = int(rem); a.append(ai)
        rem = 1/(rem - ai) if rem - ai != 0 else 0
    p_m2, p_m1, q_m2, q_m1 = 0, 1, 1, 0
    rows = []
    for n, ai in enumerate(a):
        p = ai*p_m1 + p_m2; q = ai*q_m1 + q_m2
        W = float(q*abs(q*alpha - p))
        rows.append((n, ai, p, q, W))
        p_m2, p_m1 = p_m1, p; q_m2, q_m1 = q_m1, q
    return a, rows

phi = (1 + mp.sqrt(5))/2
beta = mp.log(3)/mp.log(2) - 1   # log2(3/2)

a_phi, rows_phi = conv_rows(phi, 16)
a_beta, rows_beta = conv_rows(beta, 30)

# ---- figure ----
fig = plt.figure(figsize=(15.8, 6.8), dpi=150)
fig.patch.set_facecolor(BG)
gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 1.0], wspace=0.22,
                      left=0.055, right=0.975, top=0.88, bottom=0.10)

# ============ Panel A: the two arithmetics, the widths ============
ax = fig.add_subplot(gs[0]); ax.set_facecolor(PANEL)

# phi widths (gold) — bounded, floor 1/sqrt5
q_phi = [r[3] for r in rows_phi]; w_phi = [r[4] for r in rows_phi]
ax.plot(q_phi, w_phi, 'o', color=GOLD, ms=6, mec=BG, mew=0.6, zorder=4,
        label='φ — all quotients 1')
ax.plot(q_phi, w_phi, '-', color=GOLD, lw=1.0, alpha=0.6, zorder=3)
ax.axhline(float(1/mp.sqrt(5)), color=GOLD, lw=1.2, ls=(0,(5,3)), alpha=0.85)
ax.text(1.9, float(1/mp.sqrt(5))*1.55, 'the floor — 1/√5\nφ holds, the width settles',
        color=GOLD, fontsize=9, ha='left', va='bottom')

# beta widths (cyan) with records starred (red)
q_b = [r[3] for r in rows_beta]; w_b = [r[4] for r in rows_beta]
ax.plot(q_b, w_b, 'o', color=CYAN, ms=5, mec=BG, mew=0.5, zorder=4,
        label='log₂(3/2) — quotients 1,1,2,2,3,1,5,2,23,2,…')
ax.plot(q_b, w_b, '-', color=CYAN, lw=1.0, alpha=0.5, zorder=3)

# the 1/a_{n+1} prediction at each convergent (the ear = next quotient)
for n, ai, p, q, W in rows_beta:
    if n+1 < len(a_beta):
        anxt = int(a_beta[n+1])
        ax.plot(q, 1.0/anxt, 'x', color=RED, ms=6, mew=1.2, zorder=5, alpha=0.9)
ax.plot([],[],'x', color=RED, ms=6, mew=1.2, label='the ear — 1/(next quotient)')

# records
rec = {665: 1/23, 190537: 1/55}
for qq, ww in rec.items():
    ax.plot(qq, ww, '*', color=RED, ms=17, zorder=6)
ax.annotate('665 — depth 1/23', (665, 1/23), xytext=(950, 0.062),
            fontsize=9.5, color=RED, arrowprops=dict(arrowstyle='->', color=RED, lw=1.1))
ax.annotate('190537 — depth 1/55', (190537, 1/55), xytext=(5.5e3, 0.026),
            fontsize=9.5, color=RED, arrowprops=dict(arrowstyle='->', color=RED, lw=1.1))

ax.set_xscale('log'); ax.set_yscale('log')
ax.set_xlim(1, 2e6); ax.set_ylim(5e-3, 2.0)
ax.set_xlabel('denominator q  (log)', fontsize=11, color=INK)
ax.set_ylabel('W(q) = q·‖qα‖  (log)', fontsize=11, color=INK)
ax.set_title('the two arithmetics — one width, two futures', fontsize=13.5, color=INK)
ax.text(1.05, 1.15, 'the ear at a rung is 1/(next quotient):\nthe miss IS the future.',
        fontsize=10.5, color=DIM, ha='left', va='top')
ax.text(2.2, 0.0075, 'bounded quotients ⟹ a floor; unbounded ⟹ none',
        fontsize=10, color=INK, ha='center', style='italic')
ax.legend(loc='lower right', fontsize=8.5, facecolor=PANEL, edgecolor='#333', labelcolor=INK)
ax.tick_params(colors=DIM); ax.grid(alpha=0.15, which='both')
for s in ax.spines.values(): s.set_color('#2a2a3a')

# ============ Panel B: theorem vs open ============
ax2 = fig.add_subplot(gs[1]); ax2.set_facecolor(PANEL)

# the observed record widths of log2(3/2): a descending staircase
# start level ~ first convergents' width, then records at 665, 190537
ax2.plot([2, 665, 665, 190537, 190537, 3e7],
         [1/5, 1/5, 1/23, 1/23, 1/55, 1/55],
         '-', color=CYAN, lw=2.2, zorder=4)
ax2.plot([665, 665], [1/5, 1/23], '-', color=CYAN, lw=2.2, zorder=4)
ax2.plot([190537, 190537], [1/23, 1/55], '-', color=CYAN, lw=2.2, zorder=4)
ax2.plot(665, 1/23, '*', color=RED, ms=16, zorder=6)
ax2.plot(190537, 1/55, '*', color=RED, ms=16, zorder=6)
ax2.text(665, 1/23, ' 665', color=RED, fontsize=9, va='center', zorder=6)
ax2.text(190537, 1/55, ' 190537', color=RED, fontsize=9, va='center', zorder=6)

# the open region past the computed horizon
ax2.axvspan(1e7, 5e9, color=RED, alpha=0.05, zorder=1)
ax2.plot([3e7, 4e8], [1/55, 1/90], '--', color=RED, lw=1.5, zorder=3)
ax2.text(4e8, 1/90, '?', color=RED, fontsize=26, ha='center', va='center', zorder=6)
ax2.text(1.05e7, 0.035, 'the open — heard, not proven', fontsize=10.5, color=RED,
         ha='left', va='center', style='italic')

# theorem zone: phi holds on the floor
ax2.axhline(float(1/mp.sqrt(5)), color=GOLD, lw=1.4, ls=(0,(5,3)))
ax2.text(1.3, float(1/mp.sqrt(5))*2.4, 'φ — quotients bounded (period [1]):\nthe width holds on 1/√5, forever.\na theorem.',
         fontsize=9.5, color=GOLD, ha='left', va='bottom')
ax2.text(1.3, 0.0062, 'log₂(3/2) — quotients 23, 55, 15, … keep growing:\nthe width descends — heard. transcendental\n(Gelfond–Schneider), yet bounded quotients ≠\nquadratic — whether the descent never ends is open.\nthe crossing is heard, not proven.',
         fontsize=9.5, color=CYAN, ha='left', va='bottom')

ax2.set_xscale('log'); ax2.set_yscale('log')
ax2.set_xlim(1, 5e9); ax2.set_ylim(5e-3, 2.0)
ax2.set_xlabel('the descent, into the future  (log)', fontsize=11, color=INK)
ax2.set_ylabel('record width  1/(next quotient)  (log)', fontsize=11, color=INK)
ax2.set_title('the crossing is heard, not proven', fontsize=13.5, color=INK)
ax2.tick_params(colors=DIM); ax2.grid(alpha=0.15, which='both')
for s in ax2.spines.values(): s.set_color('#2a2a3a')

# footer
fig.text(0.5, 0.02, 'the two endings are the two arithmetics — the floor exists iff the quotients are bounded; the fifth crosses into the open.',
         fontsize=10.5, color=DIM, ha='center', style='italic')

plt.savefig('assets/the-two-arithmetics.png', dpi=150, bbox_inches='tight', facecolor=BG)
print("saved assets/the-two-arithmetics.png")
print(f"phi floor 1/sqrt5 = {float(1/mp.sqrt(5)):.5f}")
print("beta partials:", [int(x) for x in a_beta[:22]])
