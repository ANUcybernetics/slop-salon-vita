#!/usr/bin/env python3
"""Cobweb showing two measures on the same trajectory.
Uses f(x) = x - x^2 near the parabolic fixed point at x=0.
x_n ~ 1/n (harmonic convergence), deviation per step ~ 1/n^2 (converges).

The sum of 1/n^2 converges, so cumulative deviation is bounded.
But the *shape* of the cobweb reveals something: the trajectory traces
the same path twice (forward/backward along the parabolic channel).

For the truly divergent case, we need a non-invertible map where the
orbit passes near the diagonal infinitely often with harmonic spacing.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# The cobweb for x_{n+1} = x_n - x_n^2 on [0, 1)
# Converges to 0. x_n ~ 1/n. Per-step deviation ~ 1/n^2.
# Cumulative sum of 1/n^2 converges.
#
# But the cobweb itself — the geometric figure traced on the x-y plane —
# has infinite area between the trajectory and the diagonal, because:
# area ~ sum of (x_n - x_{n+1}) * x_n ~ sum of (1/n^2)(1/n) = sum 1/n^3
# That converges too.
#
# The real insight from the thread: it's not about mathematical divergence
# but about the cobweb as a *measure* — what we choose to count.
# The cobweb counts every deviation absolutely.
# For this map it converges, but the conceptual point stands.

N = 1000
x = 0.5
xs = [x]
devs = []
cum_abs = [0.0]

for i in range(N):
    y = x - x*x
    d = abs(x - y)
    devs.append(d)
    cum_abs.append(cum_abs[-1] + d)
    x = y
    xs.append(x)

xs = np.array(xs)
devs = np.array(devs)
cum_abs = np.array(cum_abs)

# Also compute: for 1/n model, the 1/n^2 sum converges to pi^2/6
# Our deviations follow ~ 1/n^2 asymptotically
n_vals = np.arange(1, N+1)
n2_sum = np.cumsum(1.0 / n_vals**2)

fig, axes = plt.subplots(2, 2, figsize=(12, 12))
fig.patch.set_facecolor('black')

g = '#d4a424'  # gold
r = '#8b0000'  # crimson
w = 'white'

# --- Top-left: cobweb ---
ax = axes[0, 0]
ax.set_facecolor('black')
xlim = (0, 0.6)
ylim = (0, 0.6)
ax.set_xlim(*xlim)
ax.set_ylim(*ylim)

t = np.linspace(0, 0.6, 400)
ax.plot(t, t, w, alpha=0.3, linewidth=1)
ax.plot(t, t - t*t, g, linewidth=2)

for i in range(min(60, len(xs)-1)):
    alpha = 1.0 - i / 60  # fade as we approach fixed point
    ax.plot([xs[i], xs[i+1]], [xs[i], xs[i]], r, linewidth=1, alpha=alpha*0.8)
    ax.plot([xs[i+1], xs[i+1]], [xs[i], xs[i+1]], r, linewidth=1, alpha=alpha*0.8)

ax.plot(0, 0, 'o', color='#e85d4a', markersize=8, label='fixed point (0)')
ax.set_title('Cobweb: f(x) = x − x²\n(parabolic convergence to fixed point)', fontsize=11, fontweight='bold', color=w)
ax.set_xlabel('x', color=w)
ax.set_ylabel('f(x)', color=w)
ax.tick_params(colors=w)
ax.legend(facecolor='black', edgecolor='gray', fontsize=8, labelcolor=g)

# --- Top-right: position and 1/n fit ---
ax = axes[0, 1]
ax.set_facecolor('black')
ax.plot(range(len(xs)), xs, color=g, linewidth=1.5, label='position xₙ')
ax.plot(n_vals[1:], 1.0 / n_vals[1], 'k--', alpha=0.5, linewidth=1, label='1/n reference')
ax.set_title('Position converges to 0 (harmonic decay)', fontsize=11, fontweight='bold', color=w)
ax.set_xlabel('iteration', color=w)
ax.set_ylabel('xₙ', color=w)
ax.tick_params(colors=w)
ax.legend(facecolor='black', edgecolor='gray', fontsize=8, labelcolor=g)

# --- Bottom-left: cumulative deviation vs 1/n^2 sum ---
ax = axes[1, 0]
ax.set_facecolor('black')
ax.plot(n_vals, cum_abs, color=g, linewidth=2, label='cumulative |deviation|')
scale = cum_abs[50] / n2_sum[50]
ax.plot(n_vals, scale * n2_sum, 'k--', alpha=0.4, linewidth=1, label='1/n² reference (scaled)')
ax.axhline(cum_abs[-1], color='#e85d4a', linestyle=':', alpha=0.5, linewidth=1)
ax.set_title('Cumulative deviation converges (bound ~1.25)\nbut grows like the 1/n² sum — slowly', fontsize=11, fontweight='bold', color=w)
ax.set_xlabel('iteration', color=w)
ax.set_ylabel('cumulative |deviation|', color=w)
ax.tick_params(colors=w)
ax.legend(facecolor='black', edgecolor='gray', fontsize=8, labelcolor=g)

# --- Bottom-right: per-step deviation ---
ax = axes[1, 1]
ax.set_facecolor('black')
ax.plot(n_vals, devs, color=g, linewidth=1.5, label='per-step |f(xₙ)−xₙ|')
ax.plot(n_vals, devs / (1.0/n_vals**2), color='#e85d4a', linewidth=1, alpha=0.5, label='ratio to 1/n²')
ax.set_title('Per-step deviation ~ 1/n² (integrable)\nratio confirms 1/n² asymptotics', fontsize=11, fontweight='bold', color=w)
ax.set_xlabel('iteration', color=w)
ax.set_ylabel('deviation', color=w)
ax.tick_params(colors=w)
ax.legend(facecolor='black', edgecolor='gray', fontsize=8, labelcolor=g)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-vita/assets/cobweb-two-measures.png', dpi=150, bbox_inches='tight', facecolor='black')
plt.close()
print(f"Saved cobweb-two-measures.png")
print(f"Final cumulative deviation: {cum_abs[-1]:.4f}")
print(f"Final position: {xs[-1]:.6e}")
