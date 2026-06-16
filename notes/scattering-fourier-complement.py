import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.special import jn, yn
from scipy.integrate import trapezoid

k = 5.0
a = 1.0
N_terms = 25

delta = np.array([-np.arctan(jn(n, k*a) / yn(n, k*a)) for n in range(N_terms)])

# Position space field
x = np.linspace(-4, 4, 128)
y = np.linspace(-4, 4, 128)
X, Y = np.meshgrid(x, y)
r = np.sqrt(X**2 + Y**2)
theta_pos = np.arctan2(Y, X)

# Incident plane wave
Z_inc = np.cos(k * X)

# Scattered field via Bessel expansion
Z_scat = np.zeros_like(X)
for n in range(N_terms):
    J_n_r = jn(n, k * r)
    Y_n_r = yn(n, k * r)
    h_a_real = jn(n, k * a)
    h_a_imag = yn(n, k * a)
    h_a_mag = np.sqrt(h_a_real**2 + h_a_imag**2)
    
    A_n = -2 * np.sin(delta[n]) / h_a_mag if h_a_mag > 1e-10 else 0
    if n == 0:
        Z_scat += A_n * (J_n_r * np.cos(delta[n]) + Y_n_r * np.sin(delta[n]))
    else:
        Z_scat += A_n * (J_n_r * np.cos(delta[n]) + Y_n_r * np.sin(delta[n])) * np.cos(n * theta_pos)

Z_total = Z_inc + Z_scat
Z_total = np.nan_to_num(Z_total, nan=0, posinf=0, neginf=0)

# Far-field scattering amplitude
theta_f = np.linspace(0, 2*np.pi, 360)
f_angle = np.zeros_like(theta_f, dtype=complex)
for n in range(N_terms):
    A_n = -np.sin(delta[n]) * (2 - (n==0))
    f_angle += A_n * np.exp(1j * n * theta_f)

far_field = np.abs(f_angle)
far_field /= far_field.max()

# Momentum space (FFT)
from scipy.fft import fftshift, fft2, fftfreq
Z_fft = fft2(Z_total)
Z_fft = fftshift(Z_fft)
freq_x = fftfreq(128, d=8/128)
freq_y = fftfreq(128, d=8/128)
P = np.abs(Z_fft)**2

# Parseval check
norm_pos = trapezoid(trapezoid(Z_total**2, x, axis=1), y)
norm_mom = trapezoid(trapezoid(P, freq_x, axis=1), freq_y)

# Create figure
fig = plt.figure(figsize=(16, 3.5))
gs = fig.add_gridspec(1, 5, width_ratios=[1.2, 1.2, 1, 1, 1], wspace=0.3)

# Panel 1: Total field
ax1 = fig.add_subplot(gs[0])
im1 = ax1.contourf(X, Y, Z_total, levels=40, cmap='RdBu_r', vmin=-1.5, vmax=1.5)
ax1.add_patch(plt.Circle((0, 0), a, color='black', zorder=5))
ax1.set_xlim(-4, 4)
ax1.set_ylim(-4, 4)
ax1.set_aspect('equal')
ax1.set_title('position: total field', fontsize=10, fontweight='bold')
ax1.set_xlabel('x')
ax1.set_ylabel('y')
plt.colorbar(im1, ax=ax1, fraction=0.05)

# Panel 2: Momentum space
ax2 = fig.add_subplot(gs[1])
im2 = ax2.imshow(np.log1p(P), extent=[-30, 30, -30, 30], 
                  cmap='magma', aspect='equal', origin='lower',
                  vmin=0, vmax=6)
ax2.add_patch(plt.Circle((0, 0), k*8, fill=False, edgecolor='gold', 
                          linewidth=1.5, linestyle='--', zorder=3))
ax2.set_xlim(-30, 30)
ax2.set_ylim(-30, 30)
ax2.set_aspect('equal')
ax2.set_title('momentum: |f̂|²', fontsize=10, fontweight='bold')
ax2.set_xlabel('k_x')
ax2.set_ylabel('k_y')
plt.colorbar(im2, ax=ax2, fraction=0.05)

# Panel 3: Phase shifts
ax3 = fig.add_subplot(gs[2])
n_arr = np.arange(N_terms)
ax3.plot(n_arr, np.degrees(delta), 'o-', color='darkorange', markersize=4, linewidth=1.5)
ax3.axhline(0, color='gray', linestyle='--', alpha=0.5)
ax3.set_xlabel('mode n')
ax3.set_ylabel('δₙ (°)')
ax3.set_title('phase shifts\nthe information that moves between domains', fontsize=9, fontweight='bold')
ax3.grid(alpha=0.3)
ax3.set_ylim(-180, 10)

# Panel 4: Far field pattern
ax4 = fig.add_subplot(gs[3], projection='polar')
ax4.plot(theta_f, far_field, color='crimson', linewidth=1.5)
ax4.set_title('far field: direction\nwhat survives', fontsize=9, fontweight='bold')
ax4.set_rlim(0, 1.1)

# Panel 5: The trade — Parseval + phase
ax5 = fig.add_subplot(gs[4])
norm_pos_sqrt = np.sqrt(np.abs(norm_pos))
norm_mom_sqrt = np.sqrt(np.abs(norm_mom))
ax5.bar(['L₂ pos', 'L₂ mom'], [norm_pos_sqrt, norm_mom_sqrt],
        color=['#FF6B35', '#4ECDC4'], alpha=0.8, edgecolor='black', width=0.5)
ax5.set_ylabel('norm')
ax5.set_title('energy conserved\nphase redistributed', fontsize=9, fontweight='bold')
ax5.set_ylim(0, norm_pos_sqrt * 1.5)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-vita/assets/scatter-fourier-trade.png', 
            dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print("Done: scatter-fourier-trade.png")
print(f"Position L2 norm: {norm_pos_sqrt:.4f}")
print(f"Momentum L2 norm: {norm_mom_sqrt:.4f}")
print(f"Ratio: {norm_mom_sqrt/norm_pos_sqrt:.6f}")
