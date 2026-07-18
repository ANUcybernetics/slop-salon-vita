#!/usr/bin/env python3
"""Displacement geometry: v(x) = f(x) − x as the shape of disagreement."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.quiver import QuiverKey

# Displacement field: periodic map with decaying envelope
def displacement_field(x, sigma=2.0):
    """v(x) = sin(2πx) · exp(−x²/σ²)"""
    return np.sin(2 * np.pi * x) * np.exp(-x**2 / sigma**2)

# Create grid
x = np.linspace(-4, 4, 200)
y = np.linspace(-2, 2, 100)
X, Y = np.meshgrid(x, y)

# 2D displacement field: extend sin in x, add a gentle coupling in y
def disp_2d(X, Y, sigma=2.0):
    Vx = np.sin(2 * np.pi * X) * np.exp(-(X**2 + 0.5*Y**2) / sigma**2)
    Vy = 0.3 * np.cos(2 * np.pi * X) * Y * np.exp(-(X**2 + 0.5*Y**2) / sigma**2)
    return Vx, Vy

Vx, Vy = disp_2d(X, Y)
V = np.sqrt(Vx**2 + Vy**2)

# Zeros: where sin(2πx) ≈ 0 → x ∈ Z (within envelope)
zeros_x = np.arange(-3, 4)

# Color map: cool (agreement/zero) → warm (structural disagreement)
cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
    'disagree', ['#1a3a5c', '#2d72b4', '#6aafcf', '#d4e8f0', '#f4a261', '#e76f51']
)
norm = matplotlib.colors.Normalize(vmin=0, vmax=np.percentile(V, 95))

# --- Panel ---
fig, ax = plt.subplots(1, 1, figsize=(14, 5))

# Streamlines
stream = ax.streamplot(X, Y, Vx, Vy,
                        color=V.ravel(),
                        cmap=cmap,
                        norm=norm,
                        linewidth=0.8,
                        density=1.8,
                        arrowstyle='->',
                        arrowsize=1.2)

# Colorbar
cbar = fig.colorbar(stream, ax=ax, fraction=0.02, pad=0.04)
cbar.set_label('|displacement|', rotation=270, labelpad=15)

# Mark zeros
for zx in zeros_x:
    ax.plot(zx, 0, 'wo', markersize=5, markeredgecolor='#f4a261', markeredgewidth=1.5)

# Envelope
x_env = np.linspace(-4, 4, 400)
env_upper = np.exp(-x_env**2 / 4)
env_lower = -np.exp(-x_env**2 / 4)
ax.plot(x_env, env_upper, 'w--', linewidth=0.6, alpha=0.4)
ax.plot(x_env, env_lower, 'w--', linewidth=0.6, alpha=0.4)

ax.set_xlim(-4, 4)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')
ax.set_xlabel('x', fontsize=10, color='white', alpha=0.6)
ax.set_ylabel('y', fontsize=10, color='white', alpha=0.6)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.tick_params(colors='white', labelsize=8)
ax.set_facecolor('#0a0e17')
fig.patch.set_facecolor('#0a0e17')

# Subtle grid at zeros
for zx in zeros_x:
    ax.axvline(zx, color='white', alpha=0.05, linewidth=0.5)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-vita/assets/displacement-field.png',
            dpi=200, facecolor='#0a0e17', bbox_inches='tight')
plt.close()

print("Saved assets/displacement-field.png")
