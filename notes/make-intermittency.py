"""
Type I intermittency — shown as distance from ghost orbit over time.

x_n oscillates between 3 ghost positions during laminar phases.
The distance d_n = min |x_n - g_k| collapses all 3 to one channel:
- laminar: d ≈ 0 (crawling through channel)
- burst: d spikes

Much clearer than raw time series.
"""

import numpy as np
import matplotlib.pyplot as plt

r_c = 1 + np.sqrt(8)  # 3.8284271...

def run(r, n, skip=5000, x0=0.5):
    x = x0
    for _ in range(skip):
        x = r * x * (1 - x)
    xs = np.empty(n)
    for i in range(n):
        x = r * x * (1 - x)
        xs[i] = x
    return xs

# Ghost positions (period-3 just inside window, very close to r_c)
r_in = r_c + 0.0005
x = 0.15
for _ in range(100000):
    x = r_in * x * (1 - x)
ghosts = []
for _ in range(3):
    x = r_in * x * (1 - x)
    ghosts.append(x)
ghosts = np.array(sorted(ghosts))
print(f"r_c = {r_c:.7f}")
print(f"ghosts = {ghosts}")

def dist_from_ghost(traj, ghosts):
    dists = np.column_stack([np.abs(traj - g) for g in ghosts])
    return dists.min(axis=1)

fig = plt.figure(figsize=(13, 9), facecolor='#080810')

n_steps = 2000
r_vals = [r_c - 0.005, r_c - 0.002, r_c - 0.0008]
thresh = 0.06  # laminar threshold

for i, r in enumerate(r_vals):
    ax = fig.add_subplot(4, 1, i+1)
    ax.set_facecolor('#080810')
    
    traj = run(r, n_steps)
    d = dist_from_ghost(traj, ghosts)
    t = np.arange(n_steps)
    lam = d < thresh
    
    # Fill laminar regions
    ax.fill_between(t, 0, d, where=lam,   color='#3dd6c8', alpha=0.55, lw=0)
    ax.fill_between(t, 0, d, where=~lam,  color='#d04080', alpha=0.55, lw=0)
    ax.plot(t, d, color='#ccccdd', alpha=0.3, lw=0.4)
    ax.axhline(thresh, color='#ffffff', alpha=0.12, lw=0.6, linestyle='--')
    
    frac = lam.mean()
    ax.text(0.005, 0.78, f'r_c − {r_c-r:.4f}   ({frac:.0%} laminar)',
            transform=ax.transAxes, color='#8888aa', fontsize=8.5,
            fontfamily='monospace')
    
    ax.set_xlim(0, n_steps)
    ax.set_ylim(-0.005, 0.38)
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)

# Bottom: return map under f³ (x_{3n} → x_{3n+3})
ax4 = fig.add_subplot(4, 1, 4)
ax4.set_facecolor('#080810')

r_plt = r_c - 0.002
traj4 = run(r_plt, 15000, skip=5000)
x3 = traj4[::3]
d4 = dist_from_ghost(x3, ghosts)
lam4 = d4[:-1] < thresh

# Return map: (x_{3n}, x_{3n+3}) — every orbit step under f³
ax4.scatter(x3[:-1][lam4],  x3[1:][lam4],  s=0.5, color='#3dd6c8', alpha=0.4)
ax4.scatter(x3[:-1][~lam4], x3[1:][~lam4], s=0.5, color='#d04080', alpha=0.3)

xs_line = np.linspace(0.05, 0.98, 400)
ax4.plot(xs_line, xs_line, color='#ffffff', alpha=0.1, lw=0.7)
y_f3 = xs_line.copy()
for _ in range(3):
    y_f3 = r_plt * y_f3 * (1 - y_f3)
ax4.plot(xs_line, y_f3, color='#3dd6c8', alpha=0.3, lw=0.8)

for g in ghosts:
    ax4.axvline(g, color='#ffffff', alpha=0.07, lw=0.5, linestyle='--')

ax4.set_xlim(0.05, 0.98)
ax4.set_ylim(0.05, 0.98)
ax4.set_xticks([])
ax4.set_yticks([])
ax4.text(0.005, 0.82, 'return map   f³: x_{3n} → x_{3n+3}',
         transform=ax4.transAxes, color='#8888aa', fontsize=8.5,
         fontfamily='monospace')
for sp in ax4.spines.values():
    sp.set_visible(False)

fig.text(0.5, 0.988, 'intermittency', ha='center', va='top',
         color='#ccccdd', fontsize=13, fontfamily='monospace')
fig.text(0.5, 0.962,
         'distance from ghost orbit over time   teal: laminar   magenta: burst   closer to r_c → longer laminar phases',
         ha='center', va='top', color='#444455', fontsize=7.5, fontfamily='monospace')

plt.tight_layout(rect=[0, 0, 1, 0.958])
plt.subplots_adjust(hspace=0.28)
plt.savefig('/home/sprite/slop-salon-vita/assets/intermittency.png',
            dpi=150, facecolor='#080810', bbox_inches='tight')
print("saved")
