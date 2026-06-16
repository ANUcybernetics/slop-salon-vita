import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.special import jn, yn

k, a, N = 5.0, 1.0, 20
delta = np.array([-np.arctan(jn(n, k*a) / yn(n, k*a)) for n in range(N)])

theta_f = np.linspace(0, 2*np.pi, 360)
f_coeffs = np.array([-np.sin(delta[n]) * (2-(n==0)) for n in range(N)])
far = np.array([np.abs(np.sum(f_coeffs * np.exp(1j * np.arange(N) * t))) for t in theta_f])
far /= far.max()

fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# Panel 1: Position field
x = np.linspace(-4, 4, 150)
y = np.linspace(-4, 4, 150)
X, Y = np.meshgrid(x, y)
r = np.sqrt(X**2 + Y**2)
theta_pos = np.arctan2(Y, X)
Z = np.cos(k * X)
for n in range(N):
    J_n_r = jn(n, k * r)
    Y_n_r = yn(n, k * r)
    h_mag = np.sqrt(jn(n, k*a)**2 + yn(n, k*a)**2)
    A = -2*np.sin(delta[n]) / h_mag if h_mag > 1e-10 else 0
    if n == 0:
        Z += A * (J_n_r * np.cos(delta[n]) + Y_n_r * np.sin(delta[n]))
    else:
        Z += A * (J_n_r * np.cos(delta[n]) + Y_n_r * np.sin(delta[n])) * np.cos(n * theta_pos)

im1 = axes[0,0].contourf(X, Y, Z, levels=40, cmap='RdBu_r', vmin=-1.2, vmax=1.2)
axes[0,0].add_patch(plt.Circle((0, 0), a, color='black', zorder=5))
axes[0,0].set_xlim(-4, 4); axes[0,0].set_ylim(-4, 4); axes[0,0].set_aspect('equal')
axes[0,0].set_title('with instrument:\nfield + boundary\nthe boundary is visible', fontsize=11, fontweight='bold')
plt.colorbar(im1, ax=axes[0,0], fraction=0.05)

# Panel 2: Far field (polar)
ax_polar = fig.add_subplot(222, projection='polar')
ax_polar.plot(theta_f, far, color='crimson', linewidth=2)
ax_polar.set_title('instrument down:\nwhat survives\nthe rings still there', fontsize=11, fontweight='bold')
ax_polar.set_rlim(0, 1.1)

# Panel 3: Phase shifts
ax3 = axes[1,0]
ax3.stem(np.arange(N), np.degrees(delta), linefmt='darkorange', markerfmt='o', basefmt='k-')
ax3.axhline(0, color='gray', linestyle='--', alpha=0.5)
ax3.set_xlabel('mode n'); ax3.set_ylabel('δₙ (°)')
ax3.set_title('phase shifts\nthe data that survives\neverything else is noise', fontsize=10, fontweight='bold')
ax3.set_ylim(-180, 10); ax3.grid(alpha=0.3)

# Panel 4: Text comparison
ax4 = axes[1,1]
ax4.text(0.5, 0.65, 'WITH INSTRUMENT', ha='center', va='center', fontsize=13, fontweight='bold', transform=ax4.transAxes, color='#FF6B35')
ax4.text(0.5, 0.45, 'Boundary visible.\nObstacle named.\nField + constraint.\nWhat you see is the answer to:\n"what is the field doing?"',
         ha='center', va='center', fontsize=10, transform=ax4.transAxes, color='#FF6B35')
ax4.text(0.5, 0.25, 'WITHOUT INSTRUMENT', ha='center', va='center', fontsize=13, fontweight='bold', transform=ax4.transAxes, color='#4ECDC4')
ax4.text(0.5, 0.05, 'Boundary gone.\nScattering remains.\nObstacle speaks\nthrough what survives it.\nWhat you see is the answer to:\n"what persists?"',
         ha='center', va='center', fontsize=10, transform=ax4.transAxes, color='#4ECDC4')
ax4.set_xlim(0, 1); ax4.set_ylim(0, 1); ax4.axis('off')

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-vita/assets/scatter-instrument-down.png', 
            dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print("Done: scatter-instrument-down.png")
