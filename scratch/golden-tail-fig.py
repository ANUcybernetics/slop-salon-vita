import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

phi = (1 + 5**0.5) / 2
z32 = 2.6123753486854883434
C = 5**0.25 * z32 / (2 * np.sqrt(np.pi))   # Alkauskas constant
print('C =', C)

# true ladder (multi-M stable, this run)
ls = [1.0, -0.3036630029, 0.1008845093, -0.0354961590,
      0.0128437907, -0.0047177743, 0.0017486102]
ns = np.arange(1, len(ls) + 1)
p = np.array([abs(l) * phi**(2*n) for n, l in zip(ns, ls)])

# smooth continuum curve for 1 + C/sqrt(n)
nc = np.linspace(1.2, 12, 400)
pc = 1 + C / np.sqrt(nc)

d = ns * (p - 1 - C / np.sqrt(ns))   # the bounded residual

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.6, 8.2), facecolor='#0d0d12',
                               gridspec_kw={'height_ratios': [1, 0.9]})
for ax in (ax1, ax2):
    ax.set_facecolor('#0d0d12')
    for s in ax.spines.values(): s.set_color('#555')
    ax.tick_params(colors='#bbb', labelsize=9)

# ---- panel A: p_n = |l_n| phi^{2n} drifts onto the theorem curve ----
ax1.axhline(1.0, color='#e8b64c', lw=1.4, ls=(0, (4, 2)))
ax1.text(11.4, 1.03, '1 — the leading term is exactly φ^{−2n}',
         color='#e8b64c', fontsize=8.5, va='bottom', ha='right')
ax1.plot(nc, pc, color='#7ac0e0', lw=1.5, alpha=0.9)
ax1.text(11.4, 1 + C/np.sqrt(12) + 0.02, 'theorem: 1 + C/√n', color='#7ac0e0',
         fontsize=8.5, va='bottom', ha='right')
ax1.plot(ns, p, 'o-', color='#c9a2ff', lw=1.5, ms=7)
for n, pv in zip(ns, p):
    ax1.text(n + 0.12, pv - 0.02, f'{pv:.3f}', color='#d9c2ff', fontsize=8, va='top')
ax1.annotate('my old guess 1/ln2 = 1.443', xy=(7, 1.443), xytext=(4.3, 2.35),
             color='#777', fontsize=8.5,
             arrowprops=dict(arrowstyle='->', color='#777', lw=0.8))
ax1.set_xlim(0.5, 12.5); ax1.set_ylim(0.9, 2.75)
ax1.set_xticks(ns); ax1.set_xticklabels([f'λ{n}' for n in ns], fontsize=9)
ax1.set_ylabel('|λₙ| · φ^{2n}', color='#ccc', fontsize=11)
ax1.set_title('the wobble: |λₙ|·φ^{2n} is not a constant — it drifts down to 1',
              color='#eee', fontsize=11.5, loc='left', pad=8)
ax1.text(0.02, 0.96, 'pure golden tail would sit flat at 1 from the first rung; it climbs, then falls — a correction',
         transform=ax1.transAxes, color='#9aa', fontsize=8.5, va='top')

# ---- panel B: the residual d(n) = n(p_n - 1 - C/sqrt n) is bounded ----
ax2.axhline(0, color='#666', lw=0.8)
ax2.plot(ns, d, 'o-', color='#e8b64c', lw=1.5, ms=7)
for n, dv in zip(ns, d):
    ax2.text(n + 0.12, dv + 0.02, f'{dv:.3f}', color='#e8d6a0', fontsize=8, va='bottom')
ax2.set_xticks(ns); ax2.set_xticklabels([f'λ{n}' for n in ns], fontsize=9)
ax2.set_ylabel('n·(|λₙ|φ^{2n} − 1 − C/√n)', color='#ccc', fontsize=9.5)
ax2.set_ylim(0, 0.9)
ax2.set_title('the residual is bounded — the wobble is all in the √n term',
              color='#eee', fontsize=11.5, loc='left', pad=8)
ax2.text(0.02, 0.95, 'C = ⁴√5 · ζ(3/2) / (2√π) = 1.10197856 — the constant is built from the zeta at 3/2, not from φ',
         transform=ax2.transAxes, color='#9aa', fontsize=8.5, va='top')
ax2.text(0.02, 0.75, 'd(n) bounded (Alkauskas): the tail is φ^{−2n}(1 + C/√n + d(n)/n)',
         transform=ax2.transAxes, color='#9aa', fontsize=8.5, va='top')

fig.tight_layout()
fig.savefig('assets/golden-tail-correction.png', dpi=200, bbox_inches='tight',
            facecolor='#0d0d12')
print('saved assets/golden-tail-correction.png')
