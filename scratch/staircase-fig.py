import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

phi = (1 + 5**0.5) / 2
phi2 = phi**2
z32 = 2.6123753486854883434
C = 5**0.25 * z32 / (2 * np.sqrt(np.pi))   # 1.10197856
K = phi2 * C / 2                            # ratio-defect limit 1.44251
d0 = 0.35885                                # Alkauskas Table 2, d(n) -> d0

# true ladder, multi-M stable (this run)
ls = [1.0, -0.3036630029, 0.1008845093, -0.0354961590,
      0.0128437904, -0.0047177775, 0.0017486952]
ns = np.arange(1, len(ls) + 1)
p = np.array([abs(l) * phi2**n for n, l in zip(ns, ls)])
resid = p - 1                      # first rung: p_n - 1 ~ C / sqrt(n)
D = np.array([abs(ls[k] / ls[k + 1]) - phi2 for k in range(len(ls) - 1)])  # second rung
nD = np.arange(1, len(D) + 1)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.6, 8.4), facecolor='#0d0d12',
                               gridspec_kw={'height_ratios': [1, 1]})
for ax in (ax1, ax2):
    ax.set_facecolor('#0d0d12')
    for s in ax.spines.values(): s.set_color('#555')
    ax.tick_params(colors='#bbb', labelsize=9)
    ax.grid(True, which='both', color='#333', lw=0.5, alpha=0.5)

nc = np.linspace(2, 10, 300)

# ---- panel A: first rung, slope -1/2 ----
ax1.set_yscale('log'); ax1.set_xscale('log')
ax1.plot(nc, C * nc**-0.5, color='#e8b64c', lw=1.4, ls=(0, (4, 2)))
ax1.text(2.05, C * 2**-0.5 * 1.25, 'C·n^{−1/2}   C = ⁴√5·ζ(3/2)/(2√π)',
         color='#e8b64c', fontsize=8.5, va='bottom')
ax1.plot(nc, C * nc**-0.5 + d0 / nc, color='#7ac0e0', lw=1.4, alpha=0.9)
ax1.text(3.1, C * 3**-0.5 + d0 / 3, '… + d(n)/n,  d(n)→0.359', color='#7ac0e0',
         fontsize=8, va='bottom')
ax1.plot(ns[1:], resid[1:], 'o-', color='#c9a2ff', lw=1.6, ms=7)
for n, r in zip(ns[1:], resid[1:]):
    ax1.annotate(f'{r:.3f}', (n, r), textcoords='offset points', xytext=(6, -14),
                 color='#d9c2ff', fontsize=8)
ax1.set_ylabel('|λₙ|·φ^{2n} − 1', color='#ccc', fontsize=11)
ax1.set_title('rung 1/2: the wobble of the eigenvalue itself — slope −1/2',
              color='#eee', fontsize=11.5, loc='left', pad=8)
ax1.text(0.02, 0.96, 'one constant, the whole tower: ζ(3/2) = Σ ℓ^{−3/2} over the modes of Theorem 2',
         transform=ax1.transAxes, color='#9aa', fontsize=8.5, va='top')

# ---- panel B: second rung, slope -3/2 ----
ax2.set_yscale('log'); ax2.set_xscale('log')
ax2.plot(nc, K * nc**-1.5, color='#e8b64c', lw=1.4, ls=(0, (4, 2)))
ax2.text(2.05, K * 2**-1.5 * 1.35, 'φ²·C/2·n^{−3/2}   = φ²·(C/2)·n^{−3/2}',
         color='#e8b64c', fontsize=8.5, va='bottom')
ax2.plot(nc, K * nc**-1.5 + phi2 * (d0 - C**2 / 2) * nc**-2, color='#7ac0e0', lw=1.4, alpha=0.9)
ax2.text(2.5, (K * 2.5**-1.5 + phi2 * (d0 - C**2 / 2) * 2.5**-2) * 0.8,
         '… + φ²(d₀−C²/2)·n^{−2}', color='#7ac0e0', fontsize=8, va='top')
ax2.plot(nD[1:], D[1:], 'o-', color='#c9a2ff', lw=1.6, ms=7)
for n, dv in zip(nD[1:], D[1:]):
    ax2.annotate(f'{dv:.4f}', (n, dv), textcoords='offset points', xytext=(6, -16),
                 color='#d9c2ff', fontsize=8)
ax2.set_ylabel('|λₙ/λₙ₊₁| − φ²', color='#ccc', fontsize=11)
ax2.set_xticks(nD); ax2.set_xticklabels([f'λ{n}/λ{n+1}' for n in nD], fontsize=9)
ax2.set_title('rung 3/2: the ratio’s defect — slope −3/2, no new constant',
              color='#eee', fontsize=11.5, loc='left', pad=8)
ax2.text(0.02, 0.96, 'the 3/2 is the 1/2 lifted: a difference of two rungs, Δ(n^{−1/2}) ≈ (1/2)n^{−3/2}. same ζ(3/2), halved, times the golden square.',
         transform=ax2.transAxes, color='#9aa', fontsize=8.5, va='top')

fig.tight_layout()
fig.savefig('assets/staircase-half-powers.png', dpi=200, bbox_inches='tight',
            facecolor='#0d0d12')
print('saved assets/staircase-half-powers.png')
