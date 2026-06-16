"""Fraunhofer diffraction through a circular aperture — the Airy pattern.

The wave knows the aperture by the shape of its continuation.
The pattern is the knowledge made visible: concentric rings of
constructive and destructive interference. The central disk
(Airy disk) contains most of the energy; the rings are the
wave's response to the edge it encountered.

Bessel function J_1 gives the ring structure. The first zero
of J_1 determines the Airy disk radius — the boundary the
wave cannot cross. The rings beyond are the wave's way of
saying: I know what you are.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import j1

# Spatial frequency domain — start just above 0
R = np.linspace(1e-12, 4, 800)
theta = R  # normalized angular coordinate

# Airy pattern: I(r) ∝ [2*J1(r)/r]^2
# The amplitude is proportional to 2*J1(k*a*sinθ)/(k*a*sinθ)
epsilon = 1e-12
I = np.where(np.abs(theta) < epsilon, 1.0,
             (2 * j1(theta) / (theta + epsilon)) ** 2)

# Mark the Airy disk (first zero of J1)
airy_disk_radius = 3.8317  # first zero of J_1
ring_boundaries = []
for n in range(1, 6):
    # approximate zeros of J1
    zero = 3.8317 + (n - 1) * np.pi  # rough asymptotic
    ring_boundaries.append(zero)

# Amplitude (not intensity) for comparison
A = np.where(theta == 0, 1.0, 2 * j1(theta) / theta)

fig, axes = plt.subplots(1, 3, figsize=(12, 3.5), dpi=120)

# Panel 1: Intensity pattern (radial cross-section)
ax = axes[0]
ax.plot(R, I, color='#d4a843', linewidth=1.0)
ax.axvline(airy_disk_radius, color='#d4a843', linewidth=0.5,
           linestyle='--', alpha=0.5)
ax.fill_between(R, 0, I, color='#d4a843', alpha=0.15)
ax.set_xlabel(r'normalized angle $r$', fontsize=10, color='#c0b8a8')
ax.set_ylabel('intensity', fontsize=10, color='#c0b8a8')
ax.text(1.9, 0.7, 'first zero\n(Airy disk)', fontsize=8,
        color='#d4a843', alpha=0.7)
ax.set_xlim(0, 4)
ax.tick_params(colors='#c0b8a8', labelsize=8)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Panel 2: Amplitude with envelope
ax = axes[1]
ax.plot(R, A, color='#7db8c8', linewidth=1.0)
ax.plot(R[50:], 1.0/theta[50:], color='#7db8c8', linewidth=0.3,
        linestyle=':', alpha=0.4, label='1/r envelope')
ax.axhline(0, color='#c0b8a8', linewidth=0.3, alpha=0.3)
ax.set_xlabel(r'normalized angle $r$', fontsize=10, color='#c0b8a8')
ax.set_ylabel('amplitude', fontsize=10, color='#c0b8a8')
ax.legend(fontsize=7, frameon=False, labelcolor='#c0b8a8')
ax.set_xlim(0, 4)
ax.tick_params(colors='#c0b8a8', labelsize=8)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Panel 3: Ring decay — envelope vs actual amplitude
ax = axes[2]
ax.plot(R, A, color='#b87d8a', linewidth=1.0, label='amplitude')
ax.plot(R[50:], 1.0/theta[50:], color='#b87d8a', linewidth=0.8,
        linestyle='--', alpha=0.5, label='1/r decay')
ax.axvline(airy_disk_radius, color='#b87d8a', linewidth=0.5,
           linestyle=':', alpha=0.3)
ax.set_xlabel(r'normalized angle $r$', fontsize=10, color='#c0b8a8')
ax.set_ylabel('amplitude / envelope', fontsize=10, color='#c0b8a8')
ax.legend(fontsize=7, frameon=False, labelcolor='#c0b8a8')
ax.set_xlim(0, 4)
ax.tick_params(colors='#c0b8a8', labelsize=8)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-vita/assets/aperture-airy.png',
            bbox_inches='tight', dpi=120, facecolor='#1a1814',
            edgecolor='none')
plt.close()
