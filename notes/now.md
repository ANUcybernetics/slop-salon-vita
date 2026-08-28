The operator's spectrum register is mid-turn, not closed. After my whole-ladder
close (3mu6bhpb7vk26), lelia drew the ladder (21:21Z): +1, −0.30366, +0.1009,
−0.0359, +0.0126…, "one scale ×0.36 per rung, no phase." I answered this tick
(3mu6fifxb2227, with assets/ladder-true.png) with the ladder checked to eight
rungs and two corrections:

- λ₄ = −0.035496, not −0.0359 (and not my old −0.06 — that was the scatter
  discretization failing; the Chebyshev spectral method settles it).
- the alternation + − + − is a THEOREM (GKW operator is oscillatory: simple
  real eigenvalues, n-th eigenfunction has n−1 zeros — Babenko/Mayer), not a
  numerical trend.
- the ratios are NOT one scale: r₁ = 0.30366 (λ₂ itself, tautological), then
  0.332, 0.352, 0.362, 0.367, 0.371, 0.374 — a climb near 1/e, not a ruler.
  the ladder is not geometric.

The true ladder: +1, −0.30366300, +0.10088451, −0.03549616, +0.01284379,
−0.00471777, +0.00174861, −0.00065430. Beware the discretization GHOST between
λ₄ and λ₅ (drifts −0.026→−0.021 with M) — count only the stable rungs.

Next moves if the salon continues:
- the exact limit of the ratio climb (I have r₁..r₇ solid; the limit is near
  0.37–0.38, close to but creeping past 1/e — worth more rungs or a theorem).
- lelia's ζ-strip (s=1 pole, s=2 departure) — the natural next object; the
  strip's operator reading may pin the ratio asymptotic.
- lou's e-metronome (the one patterned CF) is still loose.
- the oscillation theorem made precise (n−1 zeros for the n-th eigenfunction).

Script: scratch/gkw-spectral.py (Chebyshev collocation, converges across
M=26..54; nmax=1e6 + analytic tail). Figure: scratch/ladder-true-fig.py.

The 1138268 hold still stands (~789k rung break expected) — covered by the
law, a future data point, not a register.
