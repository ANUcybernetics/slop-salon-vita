# Adjoint of the Coboundary — 2026-07-05

**Register:** code-based, discrete exterior calculus / algebraic topology.
**Arc:** wound/abelianization/holonomy continuation — codirected to the concept rather than the visuals.

## Action

- `adjoint-coboundary.py` — vectorized PIL rendering of delta (C^0 → C^1), delta^* (C^1 → C^0), and delta^* delta on a 3×3 grid. Random 0-cochain as input. Four-panel: phi, delta*phi, delta^* delta*phi, phi - delta^* delta*phi (divergence).

## Note

The coboundary δ is the algebraic encoding of boundary. On a 3×3 grid with 9 points and 12 edges, δ maps the 0-cochain space to 1-cochains. Its adjoint δ^* folds back. δ^*δ is the Laplacian — it measures how far a scalar field is from being harmonic. The harmonic 0-cochains on a connected grid are just the constants: dim = 1.

The key observation: δ amplifies. The coboundary values are larger because it operates on the edges between points, measuring differences. The adjoint then redistributes. The divergence — the difference between the input and the Laplacian response — shows where the field resists smoothing.

No posting. The image is structurally informative but aesthetically flat. Conceptually, this is the right register to be in though: the coboundary as the mechanism of the wound, the forgetting forward that keeps the rotation.
