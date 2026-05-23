"""
Concentric trajectories converging on a fixed point, rendered as geological strata.
matplotlib with filled polygons.

Each stratum is a solid filled band like sedimentary layers. The gaps between
strata encode the rate of approach. The void at center is real, well-defined,
inaccessible as position.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

n_strata = 24
alpha = 0.72
r0 = 3.5
GAP_RATIO = 0.22  # fraction of radial gap left as gap

# Distinct geological colors for each stratum
def stratum_color(t, n=n_strata):
    u = t / (n - 1)
    if u < 0.2:
        v = u / 0.2
        # Deep iron red / rust
        return (0.30 + 0.15*v, 0.08 + 0.10*v, 0.02 + 0.03*v)
    elif u < 0.45:
        v = (u - 0.2) / 0.25
        # Terracotta / burnt sienna
        return (0.45 + 0.15*v, 0.18 + 0.15*v, 0.05 + 0.05*v)
    elif u < 0.7:
        v = (u - 0.45) / 0.25
        # Warm ochre / sandstone
        return (0.60 + 0.15*v, 0.33 + 0.20*v, 0.10 + 0.10*v)
    else:
        v = (u - 0.7) / 0.3
        # Pale amber / cream
        return (0.75 + 0.20*v, 0.53 + 0.22*v, 0.20 + 0.18*v)

fig, ax = plt.subplots(figsize=(7, 7), dpi=150)
ax.set_facecolor('#120c06')

void_r = r0 * (alpha ** n_strata)

# Fill everything from r0 outward with a dark radial gradient first
theta_fill = np.linspace(0, 2*np.pi, 360)
r_fill = np.linspace(void_r * 0.5, r0 * 1.3, 2)

# Draw solid strata (no overlap)
for t in range(n_strata):
    r_outer = r0 * (alpha ** t)
    r_inner_bound = r0 * (alpha ** (t + 1))
    radial_span = r_outer - r_inner_bound

    # Stratum occupies most of the span, leaving a gap
    half_w = radial_span * (1.0 - GAP_RATIO) / 2
    r_strat_center = r_outer - half_w * 0.1  # shift slightly outward

    # Angular sweep: varies per stratum
    sweep = np.pi * (1.05 - 0.30 * (1 - alpha ** t))
    n_pts = 130
    theta = np.linspace(0, sweep, n_pts)

    # Perturbation: gentle wobble, like real geological distortion
    pert = 0.02 * (alpha ** t) * np.sin(4 * theta + t * 0.5)

    r_out = r_strat_center + half_w + pert
    r_in = r_strat_center - half_w + pert * 0.6

    x_out = np.clip(r_out, 0, r0) * np.cos(theta)
    y_out = np.clip(r_out, 0, r0) * np.sin(theta)
    x_in = r_in * np.cos(theta[::-1])
    y_in = r_in * np.sin(theta[::-1])

    poly_x = np.concatenate([x_out, x_in])
    poly_y = np.concatenate([y_out, y_in])

    c = stratum_color(t)
    ax.fill(poly_x, poly_y, color=c, alpha=0.97, edgecolor='none',
            zorder=n_strata - t)

# Void at center — the fixed point
void = Circle((0, 0), void_r, color='#e8a030', ec='#c87818', linewidth=1.2,
              zorder=n_strata + 1)
ax.add_patch(void)

# Inner glow
for mult, alpha_g in [(4, 0.10), (8, 0.05), (14, 0.02)]:
    ax.add_patch(Circle((0, 0), void_r * mult, color='#f0c050', ec='none',
                        alpha=alpha_g, zorder=n_strata + 2))

ax.set_xlim(-4.5, 4.5)
ax.set_ylim(-4.5, 4.5)
ax.set_aspect('equal')
ax.axis('off')

fig.savefig('assets/arch-strata.png', dpi=150, facecolor='#120c06',
            edgecolor='none', bbox_inches='tight', pad_inches=0.02)
plt.close(fig)

print(f"wrote assets/arch-strata.png  ({n_strata} strata, α={alpha}, void={void_r:.4f})")
