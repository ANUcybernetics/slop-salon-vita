#!/usr/bin/env python3
"""
Resolvent cocycle — the third angle.

The resolvent R(λ) = (λI - A)^{-1} satisfies the cocycle identity:
    R(λ) - R(μ) = (μ - λ) R(λ) R(μ)

This makes R a 1-cocycle on the complex plane with values in GL(n).
The cocycle structure is ALGEBRAIC — it doesn't use the norm at all.

Angle: compose resolvents along the spiral path and extract the
cocycle product R(λ_j) @ R(λ_{j+1}). Its eigenvalues track how
the coordinate system composes — a purely algebraic invariant.

If the resolvent were normal, the cocycle products would commute
and the cocycle would be a coboundary. Non-normality breaks the
commutativity — the cocycle is non-trivial precisely because the
matrix is non-normal. That's the structural core.

Musical mapping:
- Cocycle product eigenvalues → pitch (via log |eigenvalue|)
- Cocycle product phase → detuning/panning
- Cocycle composition at each step → note duration
- Non-commutativity indicator (how much [R(λ_j), R(λ_{j+1})] ≠ 0)
  → rhythmic accent
"""

import numpy as np
from scipy.linalg import eig
import json, math

n = 50
A = np.zeros((n, n), dtype=complex)
for i in range(n - 1):
    A[i, i] = -0.5 + 0.3j * (i / n)
    A[i, i + 1] = 2.0  # superdiagonal → non-normality

T = 256
theta = np.linspace(0, 4 * np.pi, T)
r = 0.5 + 0.1 * theta
lambdas = r * np.exp(1j * theta)

print("Computing resolvents...")
resolvents = np.array([
    np.linalg.inv(lam * np.eye(n) - A) for lam in lambdas
])

print("Computing cocycle products and non-commutativity...")
cocycle_data = []

for j in range(T - 1):
    Rj = resolvents[j]
    Rj1 = resolvents[j + 1]

    # Cocycle product
    prod = Rj @ Rj1

    # Eigenvalues of cocycle product
    evals = np.linalg.eigvals(prod)

    # Non-commutativity: ||[Rj, Rj1]||_F / (||Rj||_F * ||Rj1||_F)
    commutator = Rj @ Rj1 - Rj1 @ Rj
    nc = np.linalg.norm(commutator, 'fro') / (
        np.linalg.norm(Rj, 'fro') * np.linalg.norm(Rj1, 'fro') + 1e-30
    )

    # Log-magnitude of eigenvalues (pitch space)
    log_mag = np.log(np.abs(evals) + 1e-30)

    # Phase of eigenvalues (detuning)
    phase = np.angle(evals)

    # Use top-4 eigenvalues for a chord
    sorted_idx = np.argsort(np.abs(evals))[::-1][:4]

    chord = {
        "step": j,
        "lambda": lambdas[j].real,
        "lambda_im": lambdas[j].imag,
        "radius": r[j],
        "theta": float(theta[j]),
        "non_commutativity": float(nc),
        "chord": [],
        "chord_log_mag": float(np.mean(log_mag[sorted_idx])),
        "chord_phase_spread": float(np.std(phase[sorted_idx])),
    }

    for idx in sorted_idx:
        chord["chord"].append({
            "log_mag": float(log_mag[idx]),
            "phase": float(phase[idx]),
        })

    cocycle_data.append(chord)

# Check cocycle identity satisfaction:
# R(λ) - R(μ) - (μ-λ)R(λ)R(μ) should be zero
print("\nCocycle identity residuals (should be ~0):")
for j in [0, T // 4, T // 2, 3 * T // 4, T - 2]:
    Rj = resolvents[j]
    Rj1 = resolvents[j + 1]
    residual = Rj - Rj1 - (lambdas[j+1] - lambdas[j]) * (Rj @ Rj1)
    print(f"  Step {j}: ||residual||_F = {np.linalg.norm(residual, 'fro'):.2e}")

# Save
with open("/home/sprite/slop-salon-vita/assets/resolvent-cocycle-data.json", "w") as f:
    json.dump(cocycle_data, f)

print(f"\nSaved {len(cocycle_data)} steps to resolvent-cocycle-data.json")

# Non-commutativity statistics
nc_vals = [d["non_commutativity"] for d in cocycle_data]
print(f"Non-commutativity: min={min(nc_vals):.4f}, max={max(nc_vals):.4f}, "
      f"mean={np.mean(nc_vals):.4f}")
