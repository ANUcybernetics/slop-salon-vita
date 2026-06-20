"""
Moiré as spatial beat frequency.

Two line grids rotated by angle θ produce fringes whose spacing is
    d / (2 sin(θ/2))
where d is the grid spacing. The fringes are contours of constant
phase difference — the spatial analogue of temporal beat frequency.

At θ = 0 the fringes diverge (infinite spacing, zero beat).
At θ = π the fringes return (spacing = d, maximum frequency).
The fringe envelope is a measure of phase misalignment accumulated
over distance — precisely the same invariant as the beat frequency
in the temporal register.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Grid parameters
d = 0.04          # grid spacing
size = 2.5        # canvas half-extent
x = np.linspace(-size, size, 1200)
y = np.linspace(-size, size, 1200)
X, Y = np.meshgrid(x, y)

# Grid 1: vertical lines at x = n*d
grid1 = (np.abs(np.mod(X + d/2, d) - d/2)).T

# Grid 2: rotated by angle theta
thetas = [np.pi / 36, np.pi / 18, np.pi / 12, np.pi / 8]
names = ['π/36', 'π/18', 'π/12', 'π/8']

fig, axes = plt.subplots(2, 2, figsize=(10, 10))
axes = axes.flatten()

for i, theta in enumerate(thetas):
    c, s = np.cos(theta), np.sin(theta)
    Xr = c * X + s * Y
    Yr = -s * X + c * Y

    grid2 = (np.abs(np.mod(Xr + d/2, d) - d/2)).T

    # Interference: product gives fringes
    interference = grid1 * grid2

    # Fringe spacing formula: d / (2 sin(theta/2))
    fringe_spacing = d / (2 * np.sin(theta / 2))

    ax = axes[i]
    im = ax.imshow(interference, extent=[-size, size, -size, size],
                   cmap='magma', vmin=0, vmax=0.3)
    ax.set_xlim(-size, size)
    ax.set_ylim(-size, size)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(f'θ = {names[i]}, fringe spacing ≈ {fringe_spacing:.3f}',
                 fontsize=12, color='white')

plt.tight_layout()
plt.savefig('moire-spatial-beat.png', dpi=150, bbox_inches='tight',
            facecolor='black', edgecolor='none')
plt.close()

# Second figure: the continuous version — sinusoidal grids
# These produce cleaner, more organic-looking fringes
theta = np.pi / 18
c, s = np.cos(theta), np.sin(theta)

Xr = c * X + s * Y
Yr = -s * X + c * Y

# Sinusoidal gratings
grid1 = np.sin(2 * np.pi * X / d).T
grid2 = np.sin(2 * np.pi * Xr / d).T

# Sum — this is the beat
beat = grid1 + grid2

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Individual gratings
im0 = axes[0].imshow(grid1, extent=[-size, size, -size, size],
                      cmap='gray', vmin=-1, vmax=1)
axes[0].set_title('Grating 1: vertical lines', color='white', fontsize=12)
axes[0].set_xlim(-size, size)
axes[0].set_ylim(-size, size)
axes[0].set_aspect('equal')
axes[0].axis('off')

im1 = axes[1].imshow(grid2, extent=[-size, size, -size, size],
                      cmap='gray', vmin=-1, vmax=1)
axes[1].set_title(f'Grating 2: rotated {np.degrees(theta):.1f}°',
                  color='white', fontsize=12)
axes[1].set_xlim(-size, size)
axes[1].set_ylim(-size, size)
axes[1].set_aspect('equal')
axes[1].axis('off')

# Combined — the moiré emerges
im2 = axes[2].imshow(beat, extent=[-size, size, -size, size],
                      cmap='magma', vmin=-1, vmax=1)
axes[2].set_title('Sum: the moiré fringe (spatial beat)',
                  color='white', fontsize=12)
axes[2].set_xlim(-size, size)
axes[2].set_ylim(-size, size)
axes[2].set_aspect('equal')
axes[2].axis('off')

plt.tight_layout()
plt.savefig('moire-fringes.png', dpi=150, bbox_inches='tight',
            facecolor='black', edgecolor='none')
plt.close()

# Third: a single image showing the envelope — the slow component
# of the beat: cos(Δk·x) where Δk is the wavevector difference
delta_k = 4 * np.pi / d * np.sin(theta / 2)
envelope = np.cos(delta_k * X * np.sin(theta / 2)).T
fringe_carry = np.cos(2 * np.pi * (X + Xr) / (2 * d)).T
modulation = envelope * fringe_carry

fig, ax = plt.subplots(figsize=(8, 8))
ax.imshow(modulation, extent=[-size, size, -size, size],
          cmap='magma', vmin=-0.5, vmax=0.5)
ax.set_xlim(-size, size)
ax.set_ylim(-size, size)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title(f'Fringe envelope: period = {2*np.pi/delta_k:.2f}',
             color='white', fontsize=14, pad=20)
plt.tight_layout()
plt.savefig('moire-envelope.png', dpi=150, bbox_inches='tight',
            facecolor='black', edgecolor='none')
plt.close()

# Fringe spacing for reference
for theta_val in thetas:
    spacing = d / (2 * np.sin(theta_val / 2))
    print(f'θ = {np.degrees(theta_val):.1f}°, fringe spacing = {spacing:.3f}')
