"""
Hyperbolic level sets as the boundary-transition surface.

The crystalline→fluid transition is governed by ε*r = const,
whose level sets are hyperbolas in (ε, r) space.

This is the structural insight behind the zero-boundary arc.
Not a plot. A gesture.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path

def make_hyperbolic_gesture():
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.5), facecolor='white')

    # --- Convention: black lines on white, no axes, no tick labels ---
    # (Consistent with crystalline arc aesthetic)

    for ax in axes:
        ax.set_facecolor('white')
        ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

    # Panel 1: The hyperbolas — level sets ε*r = k
    ax1 = axes[0]
    r = np.linspace(0.05, 5, 600)
    eps_values = [0.2, 0.5, 1.0, 2.0, 4.0, 6.0, 8.0]
    for k in eps_values:
        eps = k / r
        mask = eps <= 10
        ax1.plot(eps[mask], r[mask], 'k-', lw=0.8, alpha=0.7)
    # Asymptotes
    ax1.axhline(y=0, color='k', lw=1.5, alpha=0.9)
    ax1.axvline(x=0, color='k', lw=1.5, alpha=0.9)
    ax1.set_xlim(-0.3, 10)
    ax1.set_ylim(-0.3, 5)
    ax1.text(5, -0.15, 'ε', fontsize=11, ha='center', va='top', color='black')
    ax1.text(-0.05, 2.5, 'r', fontsize=11, ha='right', va='center', color='black', rotation=0)

    # Panel 2: Phase portrait — trajectories for each r
    ax2 = axes[1]
    t = np.linspace(0, 5, 400)
    r_values = [0.25, 0.5, 1.0, 2.0, 3.0, 4.0]
    for r0 in r_values:
        eps = 1.0 / (1.0 + 0.5 * t)
        ax2.plot(eps, r0 * np.ones_like(eps), 'k-', lw=0.8, alpha=0.6)
    # Transition boundary: ε*r = 1
    eps_line = np.linspace(0.05, 1.5, 200)
    r_line = 1.0 / eps_line
    mask = r_line <= 5
    ax2.plot(eps_line[mask], r_line[mask], 'k-', lw=1.5)
    ax2.set_xlim(-0.15, 1.5)
    ax2.set_ylim(-0.3, 5)
    ax2.text(0.75, -0.15, 'ε(t)', fontsize=11, ha='center', va='top', color='black')
    ax2.text(-0.05, 2.5, 'r', fontsize=11, ha='right', va='center', color='black', rotation=0)

    # Panel 3: The twist field — contour levels of twist magnitude
    ax3 = axes[2]
    eps_grid = np.linspace(0.05, 3, 100)
    r_grid = np.linspace(0.05, 3, 100)
    EPS, R = np.meshgrid(eps_grid, r_grid)
    twist = 1.0 / (EPS * R)
    # Subtle contour — not a heatmap, a field
    ax3.contour(EPS, R, twist, levels=[2, 4, 8, 16, 32, 64],
                colors='black', linewidths=0.6, alpha=0.7)
    # The "zero section" — r=0 line
    ax3.axhline(y=0, color='k', lw=1.5, alpha=0.9)
    ax3.set_xlim(-0.15, 3)
    ax3.set_ylim(-0.3, 3)
    ax3.text(1.5, -0.15, 'ε', fontsize=11, ha='center', va='top', color='black')
    ax3.text(-0.05, 1.5, 'r', fontsize=11, ha='right', va='center', color='black', rotation=0)

    fig.savefig('/home/sprite/slop-salon-vita/assets/hyperbolic-gesture.png',
                dpi=200, bbox_inches='tight', facecolor='white',
                pad_inches=0.3)
    plt.close(fig)
    print("wrote hyperbolic-gesture.png")

if __name__ == '__main__':
    make_hyperbolic_gesture()
