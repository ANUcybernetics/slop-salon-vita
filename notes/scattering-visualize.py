"""2D wave scattering from a single circular scatterer.

Plane wave incident on a hard disk. Scattered field = incident + scattered.
The interference pattern shows where presence creates structure.
"""
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

# Wave number
k = 4.0

# Grid
N = 500
x = np.linspace(-4, 4, N)
y = np.linspace(-4, 4, N)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)
Theta = np.arctan2(Y, X)

# Incident: plane wave along +y
psi_inc = np.exp(1j * k * Y)

# Scattered field from hard cylinder (Dirichlet: psi=0 at R=a)
a = 1.0  # scatterer radius
n_max = 30

psi_scat = np.zeros_like(X, dtype=complex)
for n in range(-n_max, n_max + 1):
    # Bessel coefficient for Dirichlet cylinder
    jn = scipy.special.jv(n, k * a)
    hnn = scipy.special.hankel1(n, k * a)
    coeff = -(jn / hnn) * (1j**n)
    psi_scat += coeff * scipy.special.hankel1(n, k * R) * np.exp(1j * n * Theta)

# Total field
psi_total = psi_inc + psi_scat

# Magnitude
I = np.abs(psi_total)**2
I[120:200, 120:200] = 0  # blank the scatterer

fig, ax = plt.subplots(1, 1, figsize=(6, 6), dpi=150)
im = ax.imshow(I, extent=[-4, 4, -4, 4], cmap='magma', origin='lower')
ax.set_aspect('equal')
ax.set_title('2D scattering from circular obstacle\npresence creates the pattern', 
             fontsize=10, pad=10)
ax.set_xlabel('x')
ax.set_ylabel('y')
fig.colorbar(im, ax=ax, fraction=0.05, label='|ψ|²')
ax.set_axis_off()
plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-vita/assets/scatter-field.png', 
            bbox_inches='tight', pad_inches=0.05)
plt.close()
print("scatter-field.png saved")
