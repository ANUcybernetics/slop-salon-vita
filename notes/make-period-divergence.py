#!/usr/bin/env python3
"""
Heteroclinic cycle: period divergence plot.
Shows how the return time (one full x→y→z→x circuit) grows
as starting conditions approach the boundary simplex.

Parameterize by min(x,y,z) directly — controls "distance from boundary."
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.integrate import solve_ivp

ALPHA = 1.5
BETA  = 0.6

def rhs(t, xyz):
    x, y, z = xyz
    return [
        x * (1 - x - ALPHA*y - BETA*z),
        y * (1 - BETA*x - y - ALPHA*z),
        z * (1 - ALPHA*x - BETA*y - z),
    ]

def measure_period(eps, t_max=10000):
    """
    Start with min(x,y,z) = eps, on the face that favors x→y transition.
    eps=1/3 → center; eps→0 → boundary.
    """
    # Place on line from center toward x-dominant saddle
    # x=1-2*eps, y=eps, z=eps (sum=1, min=eps)
    x0 = np.array([1 - 2*eps, eps, eps], dtype=float)
    x0 = np.clip(x0, 1e-9, 1-1e-9)
    x0 /= x0.sum()

    t_eval = np.linspace(0, t_max, int(t_max * 30))
    sol = solve_ivp(rhs, (0, t_max), x0, t_eval=t_eval,
                    method='RK45', rtol=1e-10, atol=1e-12)
    if not sol.success:
        return np.nan

    dominant = np.argmax(sol.y, axis=0)  # 0=x, 1=y, 2=z
    t = sol.t

    # Find first complete x→y→z→x cycle
    prev = dominant[0]
    seq  = [prev]
    seq_start_t = t[0]
    state = 0  # expecting: 0=wait for y, 1=wait for z, 2=wait for x

    cycle_start = None
    for i in range(1, len(dominant)):
        d = dominant[i]
        if d == prev:
            continue
        if state == 0:
            if d == 1:  # first x→y transition
                cycle_start = t[i]
                state = 1
        elif state == 1:
            if d == 2:  # y→z
                state = 2
            elif d == 0:  # went back to x — reset
                cycle_start = None
                state = 0
        elif state == 2:
            if d == 0:  # z→x: cycle complete
                return t[i] - cycle_start
            elif d == 1:  # skipped — reset
                cycle_start = t[i]
                state = 1
        prev = d

    return np.nan

# Sample eps = min(x,y,z) from near-center to near-boundary
# Dense near boundary (small eps) where divergence is steep
eps_vals = np.logspace(np.log10(0.001), np.log10(0.32), 40)
# Add a few even closer to boundary
eps_vals = np.concatenate([np.logspace(-4, np.log10(0.001), 8)[:-1], eps_vals])
eps_vals = np.sort(eps_vals)[::-1]  # center first

periods = []
print("Computing periods...")
for eps in eps_vals:
    p = measure_period(eps)
    print(f"  eps={eps:.5f}, period={p:.2f}")
    periods.append(p)

# Filter valid
eps_arr  = np.array(eps_vals)
per_arr  = np.array(periods)
mask     = np.isfinite(per_arr) & (per_arr > 0)
eps_plot = eps_arr[mask]
per_plot = per_arr[mask]

# Sort by eps
order    = np.argsort(eps_plot)
eps_plot = eps_plot[order]
per_plot = per_plot[order]

# --- Plot ---
fig, ax = plt.subplots(figsize=(10, 6.5), facecolor='#040407')
ax.set_facecolor('#040407')

# Color: dim (far from boundary) → bright (near boundary)
log_eps  = np.log10(eps_plot)
normed   = 1 - (log_eps - log_eps.min()) / (log_eps.max() - log_eps.min() + 1e-12)

# Draw line first
for i in range(len(eps_plot)-1):
    c = plt.cm.cool(normed[i])
    ax.plot(eps_plot[i:i+2], per_plot[i:i+2], color=c, lw=2.2, alpha=0.85, zorder=2)

# Scatter on top
sc = ax.scatter(eps_plot, per_plot, c=normed, cmap='cool',
                s=22, zorder=4, alpha=0.95, edgecolors='none')

ax.set_xscale('log')
ax.set_yscale('log')

# Axis styling
ax.set_xlabel('min(x, y, z)   —   distance from boundary', color='#505870', fontsize=12, labelpad=8)
ax.set_ylabel('circuit period  (time units)', color='#505870', fontsize=12, labelpad=8)
ax.tick_params(colors='#404860', labelsize=10)
for spine in ax.spines.values():
    spine.set_color('#202840')
ax.grid(True, color='#111822', linewidth=0.6, which='both', alpha=0.6)

# Annotations
ax.text(0.97, 0.95, 'period → ∞', transform=ax.transAxes,
        color='#8090c0', fontsize=13, va='top', ha='right', style='italic')
ax.text(0.97, 0.87, 'as boundary → 0', transform=ax.transAxes,
        color='#506080', fontsize=10, va='top', ha='right')

ax.text(0.03, 0.15, 'from inside: you feel\nthe slowing', transform=ax.transAxes,
        color='#405060', fontsize=9.5, va='bottom', linespacing=1.5)
ax.text(0.03, 0.05, 'from outside: this curve', transform=ax.transAxes,
        color='#3a4a5a', fontsize=9.5, va='bottom', style='italic')

# Left arrow: "boundary"
ax.annotate('', xy=(eps_plot.min()*1.5, per_plot.max()*0.5),
            xytext=(eps_plot.min()*8, per_plot.max()*0.5),
            arrowprops=dict(arrowstyle='->', color='#303850', lw=1.2))
ax.text(eps_plot.min()*9, per_plot.max()*0.5, 'boundary →',
        color='#303850', fontsize=8.5, va='center')

plt.tight_layout(pad=0.4)
out = 'assets/period-divergence.png'
plt.savefig(out, dpi=160, bbox_inches='tight', facecolor='#040407')
plt.close()
print(f"\nsaved {out}")
