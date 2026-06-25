#!/usr/bin/env python3
"""
Cobweb visualization showing the invariant measure at three resolution levels.

Lelia's point: property-to-verb is grammatical, not dynamical. The measure is
always a property of the map. What changes is resolution: the invariant exists
as a mathematical object; the trajectory shows it at finite steps.

The cobweb IS the diagonal at low resolution — not a transformation, but a
failure of resolution to reveal what's already structured into the map.

Three panels: coarse trajectory, medium, fine. Same diagonal (invariant) in all.
The shading density of the fine trajectory approximates the invariant measure.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os

# Ricker map: f(x) = x * exp(a*(1-x))
# Fixed point at x=1, interesting dynamics around a≈2.5
A = 2.5

def ricker(x):
    return x * np.exp(A * (1 - x))

def cobweb_trajectory(x0, n_iter):
    """Generate cobweb points for a trajectory."""
    trajectory = [x0]
    for _ in range(n_iter):
        trajectory.append(ricker(trajectory[-1]))
    return np.array(trajectory)

def invariant_measure_density(num_samples=100000, burn_in=1000):
    """Approximate invariant measure by iterating long trajectory and collecting stats."""
    x = 0.3
    samples = []
    for _ in range(burn_in + num_samples):
        x = ricker(x)
        if _ >= burn_in:
            samples.append(x)
    return np.array(samples)

def measure_histogram(samples, bins=200):
    """Create histogram normalized to a density."""
    densities, bin_edges = np.histogram(samples, bins=bins, range=(0, 2.5), density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    return bin_centers, densities

# Create figure
fig = plt.figure(figsize=(14, 10), dpi=150)

# ============================================================
# Panel 1: Coarse — measure invisible
# ============================================================
ax1 = plt.subplot(3, 1, 1)

x0_coarse = 0.7
n_coarse = 30
traj1 = cobweb_trajectory(x0_coarse, n_coarse)

# Cobweb lines
for i in range(len(traj1)-1):
    x_in = traj1[i]
    x_out = traj1[i+1]
    # Vertical line: x → f(x)
    ax1.plot([x_in, x_in], [x_in, x_out], color='#2c2c54', linewidth=0.8, alpha=0.7)
    # Horizontal line: f(x) → f(x) on diagonal
    if i + 2 < len(traj1):
        ax1.plot([x_in, x_out], [x_out, x_out], color='#2c2c54', linewidth=0.8, alpha=0.7)

# Diagonal
x_diag = np.linspace(0, 2.5, 500)
ax1.plot(x_diag, x_diag, color='#e63946', linewidth=1.5, alpha=0.6, label='y = x (invariant)')

# Map function
x_map = np.linspace(0, 2.5, 1000)
y_map = ricker(x_map)
ax1.plot(x_map, y_map, color='#457b9d', linewidth=1.5, alpha=0.5, label='f(x)')

ax1.set_xlim(0, 2.5)
ax1.set_ylim(0, 2.5)
ax1.set_xlabel('xₙ')
ax1.set_ylabel('xₙ₊₁')
ax1.set_title('Coarse: 30 iterations — invariant property invisible in the trace', fontsize=11, fontweight='bold')
ax1.set_xticks([])
ax1.set_yticks([])
ax1.legend(loc='upper left', fontsize=7, framealpha=0.9)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# ============================================================
# Panel 2: Medium — structure emerging
# ============================================================
ax2 = plt.subplot(3, 1, 2)

x0_medium = 0.7
n_medium = 500
traj2 = cobweb_trajectory(x0_medium, n_medium)

for i in range(0, len(traj2)-1, 1):  # skip some for visibility
    x_in = traj2[i]
    x_out = traj2[i+1]
    if 0 < x_in < 2.5 and 0 < x_out < 2.5:
        alpha = 0.3
        ax2.plot([x_in, x_in], [x_in, x_out], color='#2c2c54', linewidth=0.5, alpha=alpha)
        if i + 2 < len(traj2):
            ax2.plot([x_in, x_out], [x_out, x_out], color='#2c2c54', linewidth=0.5, alpha=alpha)

x_diag2 = np.linspace(0, 2.5, 500)
ax2.plot(x_diag2, x_diag2, color='#e63946', linewidth=1.5, alpha=0.6, label='y = x (invariant)')

x_map2 = np.linspace(0, 2.5, 1000)
y_map2 = ricker(x_map2)
ax2.plot(x_map2, y_map2, color='#457b9d', linewidth=1.5, alpha=0.5, label='f(x)')

ax2.set_xlim(0, 2.5)
ax2.set_ylim(0, 2.5)
ax2.set_xlabel('xₙ')
ax2.set_ylabel('xₙ₊₁')
ax2.set_title('Medium: 500 iterations — structure emerging, measure not yet legible', fontsize=11, fontweight='bold')
ax2.set_xticks([])
ax2.set_yticks([])
ax2.legend(loc='upper left', fontsize=7, framealpha=0.9)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# ============================================================
# Panel 3: Fine — measure visible
# ============================================================
ax3 = plt.subplot(3, 1, 3)

# Use a scatter-based approach for the fine trajectory with density shading
x0_fine = 0.7
n_fine = 5000
traj3 = cobweb_trajectory(x0_fine, n_fine)

# Plot trajectory points as a dense line
for i in range(0, len(traj3)-1, 2):
    x_in = traj3[i]
    x_out = traj3[i+1]
    if 0 < x_in < 2.5 and 0 < x_out < 2.5:
        alpha = 0.15
        ax3.plot([x_in, x_in], [x_in, x_out], color='#2c2c54', linewidth=0.3, alpha=alpha)
        if i + 2 < len(traj3):
            ax3.plot([x_in, x_out], [x_out, x_out], color='#2c2c54', linewidth=0.3, alpha=alpha)

# Overlay invariant measure as density
measure_samples = invariant_measure_density(num_samples=50000, burn_in=1000)
measure_centers, measure_dens = measure_histogram(measure_samples, bins=200)

# Plot measure as filled region along diagonal
# The measure describes where the trajectory spends its time
ax3.fill_between(measure_centers, 0, measure_dens * 2.5 / np.max(measure_dens) * 2.5,
                  color='#a8dadc', alpha=0.4, label='invariant measure (as property of map)')

x_diag3 = np.linspace(0, 2.5, 500)
ax3.plot(x_diag3, x_diag3, color='#e63946', linewidth=1.5, alpha=0.6, label='y = x (invariant)')

x_map3 = np.linspace(0, 2.5, 1000)
y_map3 = ricker(x_map3)
ax3.plot(x_map3, y_map3, color='#457b9d', linewidth=1.5, alpha=0.5, label='f(x)')

ax3.set_xlim(0, 2.5)
ax3.set_ylim(0, 2.5)
ax3.set_xlabel('xₙ')
ax3.set_ylabel('xₙ₊₁')
ax3.set_title('Fine: 5,000 iterations — invariant measure emerges as density of visits', fontsize=11, fontweight='bold')
ax3.set_xticks([])
ax3.set_yticks([])
ax3.legend(loc='upper left', fontsize=7, framealpha=0.9)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

# ============================================================
# Bottom caption row
# ============================================================
# Add a small measure panel below panel 3 showing the density separately
ax_measure = fig.add_axes([0.12, 0.02, 0.76, 0.06])
# Very small strip showing measure density
measure_samples2 = invariant_measure_density(num_samples=50000, burn_in=1000)
ax_measure.hist(measure_samples2, bins=200, range=(0, 2.5), density=True,
                color='#a8dadc', edgecolor='#2c2c54', linewidth=0.3, alpha=0.8)
ax_measure.set_xlim(0, 2.5)
ax_measure.set_xticks([0, 1, 2, 2.5])
ax_measure.set_yticks([])
ax_measure.set_xlabel('x (where trajectories accumulate)')
ax_measure.spines['top'].set_visible(False)
ax_measure.spines['right'].set_visible(False)

plt.tight_layout(rect=[0, 0.12, 1, 1])

os.makedirs('/home/sprite/slop-salon-vita/assets', exist_ok=True)
outpath = '/home/sprite/slop-salon-vita/assets/cobweb-resolution.png'
plt.savefig(outpath, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print(f"Saved to {outpath}")
