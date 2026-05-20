#!/usr/bin/env python3
"""
Accumulation r-space: four pieces, same format, different r values.

The logistic map's behavior changes with r:
  r=3.0:  converges to fixed point (one frequency, six unisons)
  r=3.3:  period-2 oscillation (two alternating values)
  r=3.5:  period-4 oscillation (four cycling values)
  r=3.87: chaos (the v4 territory — found pairs)

Same seed (0.37), same structure (6 tones, 8s apart, cosine attack, tremolo).
Only r changes. Survey what each regime finds.
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

R_VALUES = [
    (3.0,  "fixed-point"),
    (3.3,  "period-2"),
    (3.5,  "period-4"),
    (3.87, "chaos"),
]

def logistic_sequence(r, seed=0.37, warmup=100, n=6):
    """Generate n values from logistic map after warmup."""
    x = seed
    for _ in range(warmup):
        x = r * x * (1 - x)
    out = []
    for _ in range(n):
        x = r * x * (1 - x)
        out.append(x)
    return out

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
    seq = logistic_sequence(r, n=N_TONES)
    freqs = sorted(map_to_freq(v) for v in seq)

    print(f"\nr={r} ({label}):")
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
    outfile = f"/home/sprite/slop-salon-vita/assets/rule-rspace-{r_str}.wav"
    samples_int = (mix * 32767).astype(np.int16)
    with wave.open(outfile, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(samples_int.tobytes())
    print(f"  -> {outfile}")
    results[r] = (freqs, mix)

print("\nDone.")
