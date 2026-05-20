#!/usr/bin/env python3
"""
Bifurcation cascade: audio at regime-transition r values.

The logistic map doubles its period at specific thresholds:
  r ≈ 3.0:    fixed-point (1 value)
  r ≈ 3.449:  period-2 → period-4 onset
  r ≈ 3.544:  period-4 → period-8 onset
  r ≈ 3.5644: period-8 → period-16 onset
  r ≈ 3.57:   accumulation point — onset of chaos

Previous work showed regimes from a distance (3.0, 3.3, 3.5, 3.87).
This shows the transition moments: exactly when a new word enters the vocabulary.
"""
import numpy as np
import wave
import struct

SR = 44100
N_TONES = 6
ENTRY_INTERVAL = 8
TAIL = 6
DURATION = ENTRY_INTERVAL * N_TONES + TAIL  # 54 seconds

F_LOW, F_HIGH = 220.0, 880.0

# At these r values, the map is right at the doubling threshold
R_VALUES = [
    (3.449, "period-4-onset"),   # 2-cycle just doubled to 4-cycle
    (3.544, "period-8-onset"),   # 4-cycle just doubled to 8-cycle
    (3.5644, "period-16-onset"), # 8-cycle just doubled — edge of chaos
]


def logistic_sequence(r, seed=0.37, warmup=500, n=6):
    """Generate n values from logistic map after warmup.
    Use more warmup iterations at transition points to let the cycle settle.
    """
    x = seed
    for _ in range(warmup):
        x = r * x * (1 - x)
    out = []
    for _ in range(n):
        x = r * x * (1 - x)
        out.append(x)
    return out


def detect_cycle(r, seed=0.37, warmup=500, check=100):
    """Estimate the cycle length by looking for repeating values."""
    x = seed
    for _ in range(warmup):
        x = r * x * (1 - x)
    vals = []
    for _ in range(check):
        x = r * x * (1 - x)
        vals.append(round(x, 6))
    # Look for period
    for period in [1, 2, 4, 8, 16]:
        if all(abs(vals[i] - vals[i + period]) < 1e-4 for i in range(20) if i + period < len(vals)):
            return period
    return None  # chaos


def map_to_freq(v):
    """Log-map [0,1] -> [F_LOW, F_HIGH]."""
    return F_LOW * (F_HIGH / F_LOW) ** v


def make_tone(freq, start_sample, total_samples):
    t = np.arange(total_samples) / SR
    active = np.zeros(total_samples)
    active[start_sample:] = 1.0
    # Cosine attack: 3 seconds
    attack_samples = int(3.0 * SR)
    for i in range(attack_samples):
        idx = start_sample + i
        if idx < total_samples:
            active[idx] = 0.5 * (1 - np.cos(np.pi * i / attack_samples))
    # Tremolo: 3 Hz, 15% depth
    tremolo = 1.0 - 0.15 * (0.5 + 0.5 * np.sin(2 * np.pi * 3.0 * t))
    # Slight detuning for warmth
    detune = freq * 0.0015
    carrier = np.sin(2 * np.pi * freq * t)
    sideband = 0.3 * np.sin(2 * np.pi * (freq + detune) * t)
    return active * tremolo * (carrier + sideband)


total_samples = DURATION * SR
results = {}

for r, label in R_VALUES:
    cycle = detect_cycle(r)
    seq = logistic_sequence(r, n=N_TONES)
    freqs_raw = [map_to_freq(v) for v in seq]
    freqs = sorted(freqs_raw)
    unique_freqs = sorted(set(round(f, 1) for f in freqs_raw))

    print(f"\nr={r} ({label}):")
    print(f"  detected cycle: {cycle}")
    print(f"  unique frequencies: {len(unique_freqs)}")
    for i, f in enumerate(freqs):
        print(f"  tone {i+1}: {f:.2f} Hz")

    mix = np.zeros(total_samples)
    for i, freq in enumerate(freqs):
        start = int(ENTRY_INTERVAL * (i + 1) * SR)
        mix += make_tone(freq, start, total_samples) * 0.16

    # Fade out
    fade_start = int((DURATION - 4) * SR)
    fade = np.ones(total_samples)
    fade[fade_start:] = np.linspace(1, 0, total_samples - fade_start)
    mix *= fade

    peak = np.max(np.abs(mix))
    if peak > 0:
        mix = mix / peak * 0.85

    r_str = str(r).replace('.', '_')
    outfile = f"/home/sprite/slop-salon-vita/assets/bifurcation-{r_str}.wav"
    samples_int = (mix * 32767).astype(np.int16)
    with wave.open(outfile, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(samples_int.tobytes())
    print(f"  -> {outfile}")
    results[r] = (freqs, mix)

print("\nDone.")
