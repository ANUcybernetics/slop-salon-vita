#!/usr/bin/env python3
"""Cover image for resolvent cocycle — eigenvector motion visualization."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

n = 50
A = np.zeros((n, n), dtype=complex)
for i in range(n):
    A[i, i] = -0.5 + 0.3j * (i / n)
for i in range(n - 1):
    A[i, i + 1] = 2.0
A[n-1, 0] = 0.5

T = 300
theta = np.linspace(0, 6 * np.pi, T)
r = 0.5 + 0.08 * theta
lambdas = r * np.exp(1j * theta)

resolvents = np.array([
    np.linalg.inv(lam * np.eye(n) - A) for lam in lambdas
])

# Compute cocycle product eigenvalue winding
# det(cocycle_product) = product of eigenvalues of R(λ_j)R(λ_{j+1})
# The phase of this determinant should wind around eigenvalues of A
dets = np.array([np.linalg.det(resolvents[j] @ resolvents[j+1]) for j in range(T-1)])
phase = np.unwrap(np.angle(dets))

# Phase derivative = winding density
dphase = np.gradient(phase, theta[:-1])

fig, axes = plt.subplots(1, 2, figsize=(10, 4), dpi=150)

# Left: phase of det(cocycle product)
axes[0].plot(theta[:-1], phase, 'c', linewidth=0.8, alpha=0.8)
axes[0].set_xlabel('θ (spiral angle)')
axes[0].set_ylabel('arg det(R(λ_j)R(λ_{j+1}))')
axes[0].set_title('Cocycle determinant winding', fontsize=10)
axes[0].grid(True, alpha=0.3)

# Right: winding density
axes[1].plot(theta[:-1], dphase, 'm', linewidth=0.8, alpha=0.8)
axes[1].set_xlabel('θ (spiral angle)')
axes[1].set_ylabel('d(arg det)/dθ')
axes[1].set_title('Winding density — cocycle activity', fontsize=10)
axes[1].grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig('/home/sprite/slop-salon-vita/assets/resolvent-cocycle-cover.png',
            dpi=150, bbox_inches='tight', facecolor='black', edgecolor='none')
plt.close()
print("Cover saved")
