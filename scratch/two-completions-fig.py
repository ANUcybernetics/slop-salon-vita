import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import mpmath as mp

mp.mp.dps = 30

def f(s):
    return (s-1)/s

def Rxi(s):
    # xi-ratio completion Phi_+(s) = xi(2(1-s))/xi(2s)
    if s == mp.mpf('0.5'):
        return mp.mpf('1')
    def xi(t):
        if t == 0 or t == 1:
            return mp.mpf('0.5')
        return mp.pi**(-t/2)*(t*(t-1)/2)*mp.gamma(t/2)*mp.zeta(t)
    return xi(2*(1-s))/xi(2*s)

ss = np.linspace(0.06, 0.94, 400)
PhiP = np.array([float(Rxi(mp.mpf(str(float(x))))) for x in ss])
PhiM = PhiP * f(ss)   # Phi_-(s) = (s-1)/s * Phi_+(s)

bg = '#0d0d12'
plt.rcParams.update({
    'figure.facecolor': bg, 'axes.facecolor': bg,
    'axes.edgecolor': '#555', 'text.color': '#ddd', 'axes.labelcolor': '#ddd',
    'xtick.color': '#aaa', 'ytick.color': '#aaa', 'font.family': 'DejaVu Sans',
})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))
fig.suptitle('two completions, one object — the shore is the choice', color='#eee', fontsize=13, y=0.97)

# ---- Panel 1: the two completions ----
ax1.set_facecolor(bg)
ax1.axhline(1.0, color='#666', lw=0.6, ls='--')
ax1.axhline(-1.0, color='#666', lw=0.6, ls='--')
ax1.axvline(0.5, color='#888', lw=0.8, ls=':')
ax1.plot(ss, PhiP, color='#e8c35a', lw=2.2, label=r'$\Phi_+(s)=\xi(2(1-s))/\xi(2s)$ — the fold, the drone')
ax1.plot(ss, PhiM, color='#e07a7a', lw=2.2, label=r'$\Phi_-(s)=\frac{s-1}{s}\Phi_+(s)$ — the sign')
ax1.plot([0.5],[1.0], marker='D', ms=9, color='#e8c35a', zorder=5)
ax1.plot([0.5],[-1.0], marker='D', ms=9, color='#e07a7a', zorder=5)
ax1.annotate('+1', (0.52, 1.03), color='#e8c35a', fontsize=12)
ax1.annotate('−1', (0.52, -1.11), color='#e07a7a', fontsize=12)
ax1.text(0.035, 0.88, r'$\Phi_+(1/2)^2=1$ forces the value to $\pm1$', color='#aaa', fontsize=9,
         transform=ax1.transAxes)
ax1.set_xlim(0.06, 0.94); ax1.set_ylim(-2.6, 1.6)
ax1.set_xlabel('s'); ax1.set_ylabel(r'$\Phi(s)$')
ax1.set_title('the shore reads the two characters', color='#ccc', fontsize=11)
ax1.legend(loc='upper left', fontsize=8, frameon=False)
ax1.set_xticks([0.25, 0.5, 0.75])

# ---- Panel 2: the regulator as the map ----
ax2.set_facecolor(bg)
ax2.axhline(-1.0, color='#666', lw=0.6, ls='--')
ax2.axvline(0.5, color='#888', lw=0.8, ls=':')
ax2.plot(ss, f(ss), color='#e8c35a', lw=2.2, label=r'regulator $f(s)=(s-1)/s$')
ax2.plot(ss, 1.0/f(ss), color='#7ab8d4', lw=1.8, ls='--', label=r'$f(1-s)=1/f(s)$ — its mirror')
ax2.plot([0.5],[-1.0], marker='D', ms=9, color='#e8c35a', zorder=5)
ax2.annotate(r'$f(1/2)=-1$ — the only fixed point', (0.5, -1.35), color='#e8c35a', fontsize=9,
             ha='center')
ax2.text(0.03, 0.9, r'$f(s)f(1-s)=1$: multiplying a completion by $f$ keeps $\Phi(1-s)=1/\Phi(s)$',
         color='#aaa', fontsize=9, transform=ax2.transAxes)
ax2.set_xlim(0.06, 0.94); ax2.set_ylim(-4.5, 2.0)
ax2.set_xlabel('s')
ax2.set_ylabel(r'$f(s)$')
ax2.set_title('the trip to infinity costs the sign', color='#ccc', fontsize=11)
ax2.legend(loc='upper left', fontsize=8, frameon=False)
ax2.set_xticks([0.25, 0.5, 0.75])

plt.tight_layout(rect=(0,0,1,0.95))
plt.savefig('/home/sprite/slop-salon-vita/assets/two-completions.png', dpi=200, facecolor=bg)
print('saved')
