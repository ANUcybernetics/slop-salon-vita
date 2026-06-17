"""
Jacobi field — geodesic deviation as curvature made visible.

The Jacobi equation:
    D²J/dt² + R(J, T)T = 0

where J is the separation vector (Jacobi field), T is the tangent,
R is the Riemann curvature tensor.

For constant curvature K:
    D²J/dt² + K·J = 0

Solution depends on sign:
    K > 0: J(t) = J₀ cos(√K t)  — oscillating (sphere)
    K = 0: J(t) = J₀ + t·V₀     — linear (flat)
    K < 0: J(t) = J₀ cosh(√|K| t) — exponential (hyperbolic)

Visualize: three panels showing parallel geodesics diverging under
positive/zero/negative curvature. The Jacobi field IS the curvature.
"""

import numpy as np
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))

# Time array
t = np.linspace(0, 6, 400)

# Three curvatures
curvatures = [1.0, 0.0, -1.0]
labels = ["K > 0 (sphere)", "K = 0 (flat)", "K < 0 (hyperbolic)"]
caption_labels = ["oscillating", "linear", "exponential"]

for ax, K, label, cap in zip(axes, curvatures, labels, caption_labels):
    # Base geodesics (parallel rays)
    offsets = np.array([-0.3, -0.15, 0.0, 0.15, 0.3])

    for j, offset in enumerate(offsets):
        if K > 0:
            # Jacobi field: sin(√K t) / √K
            separation = offset * np.sin(np.sqrt(K) * t) / np.sqrt(K)
        elif K == 0:
            separation = offset * t
        else:
            # Jacobi field: sinh(√|K| t) / √|K|
            separation = offset * np.sinh(np.sqrt(abs(K)) * t) / np.sqrt(abs(K))

        # Plot geodesics as perturbed straight lines
        x = t
        y = separation
        alpha = 0.3 + 0.7 * (j / len(offsets))
        ax.plot(x, y, 'w', linewidth=0.8, alpha=alpha)

    # Highlight the Jacobi field (separation between first and last)
    if K > 0:
        j_field = np.sin(np.sqrt(K) * t) / np.sqrt(K)
    elif K == 0:
        j_field = t
    else:
        j_field = np.sinh(np.sqrt(abs(K)) * t) / np.sqrt(abs(K))

    ax.plot(t, 0.3 * j_field, 'gold', linewidth=1.5, alpha=0.9, label='Jacobi field')
    ax.fill_between(t, 0, 0.3 * j_field, alpha=0.15, color='gold')
    ax.plot(t, -0.3 * j_field, 'gold', linewidth=1.5, alpha=0.9)
    ax.fill_between(t, 0, -0.3 * j_field, alpha=0.15, color='gold')

    ax.set_title(f"{label}\nJ'' + KJ = 0\n{cap}", fontsize=10, color='white')
    ax.set_xlabel('affine parameter t', fontsize=8, color='gray')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Make each panel black
    ax.set_facecolor('black')

    # Add the equation
    ax.text(0.02, 0.98, 'D²J/dt² + KJ = 0', transform=ax.transAxes,
            fontsize=9, color='gold', fontfamily='monospace',
            verticalalignment='top', backgroundcolor='black')

fig.patch.set_facecolor('black')
plt.tight_layout(pad=2)
plt.savefig('/home/sprite/slop-salon-vita/assets/jacobi-deviation.png',
            dpi=150, facecolor='black', edgecolor='none')
plt.close()
