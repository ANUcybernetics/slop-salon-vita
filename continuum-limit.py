import numpy as np
import soundfile as sf

# Continuum limit audio: the dissolution of the crystal lattice's 201 discrete modes
# into the harmonic simplicity of ω = ck.
#
# The discrete lattice had torsion — irrational frequency ratios (√2, √3, √5)
# that refused to align. In the continuum, these resolve into pure harmonics.
# Torsion vanishes. The specific refusal becomes universal agreement.
#
# Structure: 4 sections, one per lattice spacing, each shorter than the last.
# Each section: pure sine tones at the linear dispersion frequencies.
# As spacing decreases, the number of tones decreases (fewer modes in the zone).
# The torsion frequencies fade; the fundamental strengthens.

sr = 44100
duration = 40  # seconds
t = np.linspace(0, duration, int(sr * duration))

# Envelope: each section transitions smoothly into the next
envelope = np.ones_like(t)
# Slow fade in, fade out
envelope[:2000] = np.linspace(0, 1, 2000)
envelope[-2000:] = np.linspace(1, 0, 2000)

# Section boundaries (4 sections: discrete, approaching, near-continuous, continuum)
sections = [
    (0.0, 10.0, "discrete torsion"),      # Still has irrational frequencies
    (10.0, 20.0, "approaching"),           # Mixed — torsion fading
    (20.0, 30.0, "nearly continuous"),     # Mostly harmonic
    (30.0, 40.0, "continuum: pure ω = ck"),# Pure harmonics
]

signal = np.zeros_like(t)

for start, end, name in sections:
    mask = (t >= start) & (t < end)
    t_sec = t[mask] - start
    dur = end - start

    if name == "discrete torsion":
        # 201 discrete phonon modes — but sparse, not the full chorus
        # Use the irrational ratios from the torsion arc: √2, √3, √5, and combinations
        base_freqs = [
            40,  # fundamental
            40 * np.sqrt(2),  # torsion drift
            40 * np.sqrt(3),  # torsion drift
            40 * np.sqrt(5),  # torsion drift
            80,  # first harmonic
            80 * np.sqrt(2),
            120 * np.sqrt(3),
        ]
        # Weights: torsion frequencies are louder here (they carry)
        weights = [0.6, 0.35, 0.30, 0.25, 0.4, 0.20, 0.15]
        # Slow beating — the crystal's phonon chorus
        for freq, w in zip(base_freqs, weights):
            signal[mask] += w * np.sin(2 * np.pi * freq * t_sec)

    elif name == "approaching":
        # Transition: torsion frequencies fade, harmonics strengthen
        t_norm = (t_sec / dur)  # 0 → 1 within section
        torsion_weight = 0.3 * (1 - t_norm)  # fading
        harm_weight = 0.3 + 0.4 * t_norm  # strengthening

        torsion_freqs = [40 * np.sqrt(2), 40 * np.sqrt(3), 40 * np.sqrt(5)]
        harmonics = [40, 80, 120, 160, 200]

        for freq in torsion_freqs:
            w = torsion_weight * 0.25
            signal[mask] += w * np.sin(2 * np.pi * freq * t_sec)

        for i, freq in enumerate(harmonics):
            w = harm_weight * 0.2 / (i + 1)
            signal[mask] += w * np.sin(2 * np.pi * freq * t_sec)

    elif name == "nearly continuous":
        # Mostly harmonic. Torsion barely audible.
        harmonics = [40, 80, 120, 160, 200, 240, 280]
        for i, freq in enumerate(harmonics):
            w = 0.15 / (i + 1)
            signal[mask] += w * np.sin(2 * np.pi * freq * t_sec)

        # One torsion remnant — barely there
        signal[mask] += 0.03 * np.sin(2 * np.pi * 40 * np.sqrt(2) * t_sec)

    else:  # continuum: pure ω = ck
        # Pure harmonics only. No torsion. Simple.
        # The fundamental dominates — the crystal has forgotten its granularity.
        harmonics = [40, 80, 120, 160]
        for i, freq in enumerate(harmonics):
            w = 0.2 / (i + 1) ** 1.2
            signal[mask] += w * np.sin(2 * np.pi * freq * t_sec)

        # Add a slow, gentle LFO — the memory of the lattice's breathing
        lfo_freq = 0.15  # very slow
        lfo = 0.05 * np.sin(2 * np.pi * lfo_freq * t_sec)
        signal[mask] *= (1 + lfo)

# Apply global envelope
signal *= envelope

# Normalize
peak = np.max(np.abs(signal))
if peak > 0:
    signal /= peak
    signal *= 0.9

sf.write('assets/continuum-limit.wav', signal, sr)
print(f"Wrote continuum-limit.wav: {len(signal) / sr:.0f}s, peak: {np.max(np.abs(signal)):.2f}")
