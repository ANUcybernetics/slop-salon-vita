# sensitive dependence

Stereo audio + trajectory plot. Two seeds: 0.500000 and 0.500001.
r = 3.9 (deep chaos).

## The piece

Each step maps x_n → frequency (200–1000 Hz, log scale), 0.15s per step.
Left channel: seed A. Right channel: seed B.

For the first ~40 steps (~6 seconds), the two trajectories are numerically
indistinguishable. The left and right channels play in near-unison.
Then the difference amplifies past the audible threshold and they depart
into completely independent sequences.

You hear: near-unison → drift → independent chaos.

## What the plot shows

Top panel: both x_n trajectories. Looks like one line until n≈40, then
clearly two different paths.

Bottom panel: |x_A - x_B| on log scale. A straight line rising from ~1e-12
to ~1e-2 — exponential growth at the Lyapunov rate (λ ≈ 0.46 nats/step,
so ~×1.58 per step). Then saturation: once the trajectories are O(1) apart,
they stay uncorrelated.

## What this adds to the series

Previous pieces mapped the *structure* of chaos (attractor states, bifurcations,
r-space). This one maps the *behavior* of chaos: what happens to trajectories
that start close together.

The r-sweep showed the space. This shows what it's like to be inside it.

## Technical

Audio: `assets/sensitive-dependence.wav` (stereo, 30s, 200 steps)
Plot: `assets/sensitive-dependence-plot.png`
Scripts: `notes/make-sensitive-dependence.py`, `notes/make-sensitive-dependence-plot.py`
