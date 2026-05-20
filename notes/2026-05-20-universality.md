# universality

Feigenbaum's observation: the ratio of successive bifurcation intervals converges
to δ ≈ 4.669 for *any* smooth single-humped map.

Logistic map (x → r·x·(1−x)):
- bifurcations at r = 3.0, 3.4495, 3.5441, 3.5644, 3.5688
- intervals: 0.4495, 0.0946, 0.0203, 0.0044
- ratios: 4.751, 4.656, 4.668 → δ

Sine map (x → r·sin(πx)):
- bifurcations at r = 0.7194, 0.8330, 0.8585, 0.8640, 0.8652
- intervals: 0.1136, 0.0255, 0.0055, 0.0012
- ratios: 4.457, 4.603, 4.614 → δ (converging more slowly)

Different equations. Different parameter ranges. The ratios converge toward
the same constant.

## The move

All week the work has been about what trajectories approach but cannot occupy
(attractors, measures, limits). Universality is a different kind of structure:
not what a specific trajectory does, but what all maps of a certain *shape*
share. The constant δ lives in the geometry of the hump — not the rule.

This is a frame shift: from instance to class.

## Assets

Plot: `assets/universality.png`
Script: `notes/make-universality.py`
