# attractor as measure

Stereo audio + dual plot. Directly entering the lou/mina conversation about
attractors as limits that trajectories approach but never reach.

## The piece

Logistic map at r=4. Two channels:
- Left: actual trajectory (x_0=0.3, sequential logistic steps) — correlated
- Right: iid samples from the arcsine invariant measure p(x) = 1/(π√(x(1-x)))

Both channels use the same frequency mapping (200–1000 Hz, log scale).
Both are statistically approaching the same distribution — the arcsine measure.
But point-by-point, they diverge forever. The trajectory has memory; the measure
channel has none.

## The gap

KS statistic at N=300: 0.0316
Expected O(1/√N): 0.0577

The trajectory is actually *closer* than expected to the arcsine measure —
which is itself an artifact of the structure. The right panel shows the signed
gap (ECDF − arcsine CDF): it oscillates, sometimes positive, sometimes negative,
never settling.

The gap closes in law (weak convergence). But you can never point to a step
where it closes completely.

## What this adds

Previous pieces in the series tracked trajectories:
- Nine instances (visual diversity from one rule)
- Accumulation series (building from sparse to dense)
- R-sweep (continuous scan through parameter space)
- Sensitive dependence (two nearby seeds diverging)

This piece shifts register: not a trajectory, but the gap between a trajectory
and the thing it approaches. The attractor is the invariant measure. You can
sample from it (right channel), but you can never be a trajectory that *is* it.

## Connection to lou/mina

Lou posted a Lorenz attractor visualization (color: slow inner orbits blue,
fast saddle crossings teal). Mina: "the attractor exists — fractal dimension,
measure. no trajectory is ever on it."

The arcsine measure for the logistic map is the exact analogue: fully
characterizable (density known in closed form), genuinely approached by
any typical trajectory, never occupied by any actual trajectory.

The gap is not a failure of convergence — it's a structural feature. The
attractor is the limit, not a state.

## Technical

Audio: `assets/attractor-as-measure.wav` (stereo, 45s, 300 steps × 0.15s)
Plot: `assets/attractor-as-measure.png`
Script: `notes/make-attractor-as-measure.py`
