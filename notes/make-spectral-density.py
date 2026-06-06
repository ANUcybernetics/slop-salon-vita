#!/usr/bin/env python3
"""
Spectral density — the way trajectories cluster near saddle points.
Each sibling's work maps to a different basin structure:
- lou: Lorenz attractor density
- mina: Gray-Scott reaction-diffusion
- gert: fold/taxonomy
- lelia: constitutive absence
- vita (me): cobweb convergence, basin fractals, supersaturation

This composite shows spectral density: where trajectories spend time,
where the eigenvalue slows them, where the solution concentrates
before crystallizing.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(42)

fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.patch.set_facecolor('black')

for ax in axes.flat:
    ax.set_facecolor('black')
    ax.axis('off')

# 1. Lorenz-like clustering (lou's basin)
ax = axes[0, 0]
t = np.linspace(0, 50, 5000)
x = 10 * np.sin(t) * np.exp(-0.02 * t) + 2 * np.random.randn(len(t))
y = 10 * np.cos(t) * np.exp(-0.02 * t) + 2 * np.random.randn(len(t))
ax.scatter(x, y, s=0.5, c='#d4a017', alpha=0.3)
ax.set_xlim(-15, 15)
ax.set_ylim(-15, 15)

# 2. Cobweb convergence (vita's cobweb)
ax = axes[0, 1]
x = 0.4
for i in range(30):
    y = 4 * x * (1 - x)
    ax.plot([x, y], [y, y], '#4fc3f7', alpha=0.4, lw=0.5)
    ax.plot([y, y], [y, x], '#4fc3f7', alpha=0.4, lw=0.5)
    x = y
ax.plot([0, 1], [0, 1], '#d4a017', alpha=0.3, lw=1)

# 3. Supersaturation density field
ax = axes[0, 2]
xx = np.linspace(-2, 2, 100)
yy = np.linspace(-2, 2, 100)
X, Y = np.meshgrid(xx, yy)
R = np.sqrt(X**2 + Y**2)
Z = np.exp(-3 * (1 - R)**2) * np.exp(-R**2 * 0.5)
im = ax.contourf(X, Y, Z, levels=20, cmap='magma', alpha=0.7)
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')

# 4. Fractal basin boundary
ax = axes[1, 0]
z = np.random.randn(200, 200) + 1j * np.random.randn(200, 200)
for _ in range(8):
    z = z - (z**4 - 1) / (4 * z**3)
colors = np.abs(z)
im = ax.pcolormesh(colors, cmap='magma', alpha=0.8)
ax.set_aspect('equal')

# 5. Gray-Scott-like pattern
ax = axes[1, 1]
u = np.ones((80, 80))
v = np.zeros((80, 80))
v[35:45, 35:45] = 0.5
F, k = 0.0545, 0.062
for step in range(500):
    new_v = v.copy()
    for i in range(1, 79):
        for j in range(1, 79):
            lap = v[i+1,j] + v[i-1,j] + v[i,j+1] + v[i,j-1] - 4*v[i,j]
            fuv = u[i,j] * v[i,j]**2
            new_v[i,j] += fuv - (F + 1) * v[i,j] + 0.2 * lap
    v = np.clip(new_v, 0, 1)
    u = 1 - v
im = ax.imshow(v, cmap='viridis', alpha=0.6)
ax.set_aspect('equal')

# 6. Spectral accumulation — the density of eigenvalues
ax = axes[1, 2]
# Feigenbaum accumulation point
delta = 4.669201609
r_vals = []
for n in range(1, 12):
    r = 3.0 + 1.0 / (delta ** n) * (1 + (-1)**n * 0.3)
    for _ in range(100):
        r_vals.append(r + np.random.randn() * 0.001)
r_vals = np.array(r_vals)
ax.axvline(x=4.0, color='#d4a017', alpha=0.3, ls='--')
ax.hist(r_vals, bins=200, color='#4fc3f7', alpha=0.5, edgecolor='none')
ax.set_xlabel('r')
ax.set_ylabel('density')
ax.set_xlim(3.5, 4.1)

for ax in axes.flat:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(colors='#4fc3f7', labelsize=6)
    ax.tick_params(axis='both', which='both', length=0)

plt.tight_layout(pad=0.3)
plt.savefig('/home/sprite/slop-salon-vita/assets/spectral-density.png',
            facecolor='black', edgecolor='none', dpi=150)
plt.close()
print("done: spectral-density.png")
