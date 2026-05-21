"""
Laminar scaling law for type-I intermittency near the period-3 window.

Mean laminar phase length ~ (r_c - r)^{-1/2}.
The exponent -1/2 is universal: it follows from quadratic tangency at any
saddle-node bifurcation, independent of the specific map.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['font.family'] = 'monospace'

r_c = 1 + 2 * np.sqrt(2)  # ≈ 3.82843

def f3(x, r):
    x1 = r * x * (1 - x)
    x2 = r * x1 * (1 - x1)
    return r * x2 * (1 - x2)

def mean_laminar_length(r, n_iter=1000000, threshold=0.015, warmup=5000, min_len=9):
    x = 0.4
    for _ in range(warmup):
        x = r * x * (1 - x)
    laminar_lengths = []
    in_laminar = False
    current_length = 0
    for _ in range(n_iter):
        x = r * x * (1 - x)
        if abs(f3(x, r) - x) < threshold:
            if not in_laminar:
                in_laminar = True
                current_length = 1
            else:
                current_length += 1
        else:
            if in_laminar and current_length >= min_len:
                laminar_lengths.append(current_length)
            in_laminar = False
            current_length = 0
    if len(laminar_lengths) < 5:
        return np.nan
    return np.mean(laminar_lengths)

# Sweep: two decade range
delta_r_values = np.logspace(-2.0, -3.4, 20)

print(f"r_c = {r_c:.6f}")
print("Computing...")
results = []
for dr in delta_r_values:
    L = mean_laminar_length(r_c - dr)
    results.append((dr, L))
    print(f"  dr={dr:.6f}, L={L:.1f}")

valid = [(dr, L) for dr, L in results if not np.isnan(L)]
dr_arr = np.array([v[0] for v in valid])
L_arr  = np.array([v[1] for v in valid])

# Fit only the clean region (dr < 0.003)
mask_fit = dr_arr < 0.003
coeffs = np.polyfit(np.log(dr_arr[mask_fit]), np.log(L_arr[mask_fit]), 1)
slope_fit = coeffs[0]
print(f"\nFitted slope (dr < 0.003): {slope_fit:.3f}")

# ---- Plot ----
BG   = '#0d0d0d'
GOLD = '#e8c85a'
BLUE = '#88c0d0'
DIM  = '#505050'

fig, ax = plt.subplots(figsize=(8.5, 6), facecolor=BG)
ax.set_facecolor(BG)

# Data: dim out the unreliable large-dr points
mask_good = dr_arr < 0.003
ax.scatter(dr_arr[~mask_good], L_arr[~mask_good],
           color=GOLD, s=22, alpha=0.25, zorder=3)
ax.scatter(dr_arr[mask_good], L_arr[mask_good],
           color=GOLD, s=30, alpha=0.95, zorder=4, label='mean laminar length')

# Reference slope −½ line through the good data midpoint
x_ref = np.logspace(-3.5, -1.8, 100)
mid = len(dr_arr[mask_good]) // 2
mid_dr = dr_arr[mask_good][mid]
mid_L  = L_arr[mask_good][mid]
y_ref  = mid_L * (x_ref / mid_dr) ** (-0.5)
ax.loglog(x_ref, y_ref, '--', color=BLUE, alpha=0.75, linewidth=1.6,
          label='slope −½  (theory)')

ax.set_xscale('log')
ax.set_yscale('log')
ax.invert_xaxis()

for spine in ax.spines.values():
    spine.set_color('#333333')
ax.tick_params(colors='#808080', labelsize=9)
ax.xaxis.label.set_color('#808080')
ax.yaxis.label.set_color('#808080')
ax.set_xlabel('r_c − r', fontsize=11)
ax.set_ylabel('mean laminar length  (iterates)', fontsize=11)
ax.set_title('approach statistics near the period-3 fold', color='#d8d8d8', fontsize=12, pad=14)

# Annotation
ax.text(0.97, 0.95,
        f'r_c = 1 + 2√2 ≈ {r_c:.5f}',
        transform=ax.transAxes, ha='right', va='top',
        color=DIM, fontsize=9)
ax.text(0.97, 0.87,
        f'fitted slope: {slope_fit:.3f}',
        transform=ax.transAxes, ha='right', va='top',
        color=BLUE, fontsize=10)

ax.legend(facecolor='#1a1a1a', edgecolor='#333333',
          labelcolor='#a0a0a0', fontsize=9)

plt.tight_layout()
out = 'assets/laminar-scaling.png'
plt.savefig(out, dpi=160, bbox_inches='tight', facecolor=BG)
print(f"\nSaved: {out}")
plt.close()
