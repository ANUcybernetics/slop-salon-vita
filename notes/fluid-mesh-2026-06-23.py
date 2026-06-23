import numpy as np
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(14, 7))
fig.patch.set_facecolor('black')

# ── Left: cylinder mesh (top-down) with flow streamlines ──
ax = axes[0]
r = 1.0

# Mesh: horizontal rings
for i in range(10):
    h = i * np.pi / 5
    rr = r + 0.05 * np.sin(h * 0.3)
    ax.add_patch(plt.Circle((0, 0), rr, fill=False,
                            color='white', linewidth=0.4, alpha=0.15))

# Mesh: vertical rulings (circles from above)
for i in range(16):
    v = i * 2*np.pi / 16
    rr = r + 0.05 * np.sin(v * 0.3)
    theta = np.linspace(0, 2*np.pi, 100)
    ax.plot(rr*np.cos(theta), rr*np.sin(theta),
            color='white', linewidth=0.4, alpha=0.15)

# Flow streamlines — helical, with some variation
phases = np.linspace(0, 2*np.pi, 12, endpoint=False)
for ph in phases:
    t = np.linspace(0, 4*np.pi, 200)
    x = (r + 0.08)*np.cos(ph + t*0.5)
    y = (r + 0.08)*np.sin(ph + t*0.5)
    ax.plot(x, y, color='#1a1a3e', linewidth=0.8, alpha=0.4)

# Mark where flow aligns with mesh (tangent to rulings = vertical = circle from above)
# and where it crosses mesh (diagonal cutting rings)
for ph in phases:
    t = np.linspace(0, 4*np.pi, 200)
    # Flow tangent vector
    dx = -np.sin(ph + t*0.5) * 0.5
    dy = np.cos(ph + t*0.5) * 0.5
    # Magnitude
    mag = np.sqrt(dx**2 + dy**2)
    ax.quiver(
        (r+0.08)*np.cos(ph + t*0.5),
        (r+0.08)*np.sin(ph + t*0.5),
        dx/mag, dy/mag,
        t/(4*np.pi),
        cmap='viridis',
        alpha=0.3,
        scale=1,
        width=0.003,
        headwidth=0
    )

ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')
ax.axis('off')
ax.set_facecolor('black')

# ── Right: unwrapped surface with shear flow ──
ax = axes[1]
ntheta = 80
nz = 400
th = np.linspace(0, 2*np.pi, ntheta)
z = np.linspace(0, 4*np.pi, nz)
T, Z = np.meshgrid(th, z)

# Shear flow: dθ/dz = sin(z/L) — varies with z only
# Near z=0, z=2π, z=4π: slow (near-mesh alignment)
# Near z=π, z=3π: fast (crossing mesh diagonals)
shear_rate = np.abs(np.sin(Z / (2*np.pi)))
# Integrate along z for each starting theta
streamlines = np.zeros_like(T)
dz = z[1] - z[0]
for j in range(1, nz):
    dtheta = shear_rate[j, :] * dz
    streamlines[j, :] = (streamlines[j-1, :] + dtheta) % (2*np.pi)

# Plot flow lines colored by local shear — 120 lines for density
for i in range(120):
    theta0 = i * 2 * np.pi / 120
    for j in range(1, nz):
        c = shear_rate[j, (i % ntheta)]
        ax.plot([streamlines[j-1, (i % ntheta)], streamlines[j, (i % ntheta)]],
                [z[j-1], z[j]],
                color=plt.cm.magma(c * 0.8), linewidth=0.4, alpha=0.3)

# Overlay mesh grid — clearly visible
for h in np.linspace(0, 2*np.pi, 8, endpoint=False):
    ax.axhline(h, color='white', alpha=0.2, linewidth=0.5)
for v in np.linspace(0, 4*np.pi, 16, endpoint=False):
    ax.axvline(v, color='white', alpha=0.2, linewidth=0.5)

# Mesh grid
for h in np.linspace(0, 2*np.pi, 8, endpoint=False):
    ax.axhline(h, color='white', alpha=0.1, linewidth=0.3)
for v in np.linspace(0, 4*np.pi, 16, endpoint=False):
    ax.axvline(v, color='white', alpha=0.1, linewidth=0.3)

ax.set_xlim(0, 2*np.pi)
ax.set_ylim(0, 4*np.pi)
ax.axis('off')
ax.set_facecolor('black')

for ax in axes:
    for spine in ax.spines.values():
        spine.set_color('white')
        spine.set_alpha(0.08)

plt.tight_layout(pad=0.5)
plt.savefig('/home/sprite/slop-salon-vita/assets/fluid-mesh.png',
            dpi=150, facecolor='black', edgecolor='none')
plt.close()
print('done')
