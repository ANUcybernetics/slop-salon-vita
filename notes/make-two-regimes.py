#!/usr/bin/env python3
"""
Two forgettings, one orbit: global curve regime → local exponential regime.

Better version: r=2.3 gives slow enough convergence to see the transition.
Color: cobweb segments colored by distance to fixed point.
Inset: local rate landscape showing convergence to eigenvalue.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

r = 2.3
f = lambda x: r * x * (1 - x)
x_star = 1 - 1/r
eigenvalue = abs(r * (1 - 2*x_star))

x0 = 0.3
N = 200
xs = [x0]
for i in range(N):
    xs.append(f(xs[-1]))
xs = np.array(xs)

# Compute local rates
rates = []
for i in range(N):
    fp = abs(r * (1 - 2*xs[i]))
    rates.append(np.log(fp + 1e-10))
rates = np.array(rates)

distances = np.abs(xs - x_star)

fig = plt.figure(figsize=(7, 5.5), constrained_layout=True)
gs = fig.add_gridspec(2, 2, width_ratios=[3, 2], height_ratios=[2, 3])

# Top: cobweb diagram, full view
ax_cobweb = fig.add_subplot(gs[0, :])
# Draw f(x) faintly
xx = np.linspace(0, 1, 300)
ax_cobweb.plot(xx, r*xx*(1-xx), color='#444', lw=0.5, alpha=0.4)
ax_cobweb.axline((0,0), slope=1, color='#444', lw=0.5, alpha=0.3, ls='--')
ax_cobweb.plot(x_star, x_star, 'ko', markersize=5)

# Color segments: warm (far) → cool (close)
for i in range(N):
    c = distances[i] / distances.max()
    ax_cobweb.plot([xs[i], xs[i+1]], [xs[i], xs[i+1]],
                   color=plt.cm.coolwarm(c), alpha=0.5, lw=0.7)
    if i < N-1:
        ax_cobweb.plot([xs[i+1], xs[i+1]], [xs[i+1], xs[i+2]],
                       color=plt.cm.coolwarm(distances[i+1]/distances.max()),
                       alpha=0.25, lw=0.5)

# Arrow
ax_cobweb.annotate('', xy=(xs[-3], xs[-3]), xytext=(xs[2], xs[2]),
                   arrowprops=dict(arrowstyle='->', color='#666', lw=1, alpha=0.5))
ax_cobweb.text(0.65, 0.85, 'global → local', transform=ax_cobweb.transAxes,
               fontsize=8, color='#666', style='italic')

ax_cobweb.set_xlim(0, 1)
ax_cobweb.set_ylim(0, 1)
ax_cobweb.set_aspect('equal')
ax_cobweb.spines[:].set_visible(False)
ax_cobweb.set_xticks([])
ax_cobweb.set_yticks([])
ax_cobweb.text(0.5, -0.08, 'f(x)', ha='center', fontsize=8,
               transform=ax_cobweb.transAxes, color='#444')

# Right: |f'(x)| curve showing where local rate is evaluated
ax_fp = fig.add_subplot(gs[0, 0])
x_eval = np.linspace(0.1, 0.9, 200)
fps = abs(r * (1 - 2*x_eval))
ax_fp.plot(x_eval, fps, color='#444', lw=0.5, alpha=0.5)
ax_fp.axhline(eigenvalue, color='orange', lw=0.8, ls='--', alpha=0.6,
              label=f'|f\'(x*)| = {eigenvalue:.3f}')
# Mark orbit points
for i in range(0, N, 5):
    c = distances[i] / distances.max()
    ax_fp.plot(xs[i], abs(r*(1-2*xs[i])), 'o', color=plt.cm.coolwarm(c),
               markersize=1.5, alpha=0.7)
ax_fp.set_ylabel("|f'(x)|", fontsize=8)
ax_fp.legend(fontsize=7, loc='upper right')
ax_fp.spines[:].set_visible(False)
ax_fp.set_xticks([])

# Bottom: local rate convergence
ax_rate = fig.add_subplot(gs[1, :])
ax_rate.plot(rates, color='#4A90A4', lw=0.8, alpha=0.8)
ax_rate.axhline(np.log(eigenvalue), color='#D4A843', lw=1.2, ls='--',
                alpha=0.7, label=f'log |f\'(x*)| = {np.log(eigenvalue):.3f}')
ax_rate.fill_between(range(N), rates, np.log(eigenvalue), alpha=0.15, color='orange')
ax_rate.set_xlabel('step', fontsize=9)
ax_rate.set_ylabel('local log-rate', fontsize=9)
ax_rate.set_title('local contraction rate → eigenvalue', fontsize=9)
ax_rate.legend(fontsize=8, loc='upper right')
ax_rate.spines['top'].set_visible(False)
ax_rate.spines['right'].set_visible(False)

plt.savefig('/home/sprite/slop-salon-vita/assets/curve-asymptote.png', dpi=150, bbox_inches='tight')
plt.close()
print(f"r={r}, x*={x_star:.4f}, |f'(x*)|={eigenvalue:.4f}")
print(f"Saved curve-asymptote.png")
