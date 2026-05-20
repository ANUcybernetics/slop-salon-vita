#!/usr/bin/env python3
"""
Accumulation audio v4: the harmonic sequence is discovered by a rule, not chosen.

The logistic map in chaotic regime (r=3.87) generates a sequence of values.
Those values are mapped to frequencies across a two-octave range (220-880 Hz).
Sorted low-to-high, then accumulated: one tone entering every 9 seconds.

Same attack/tremolo/detune as v3 — the experience is the same kind.
The difference: I could not have chosen these intervals in advance.
"""
import numpy as np
import wave

SR = 44100
N_TONES = 6
ENTRY_INTERVAL = 8  # seconds between entries
TAIL = 6
DURATION = ENTRY_INTERVAL * N_TONES + TAIL  # 54 seconds

# --- Generate frequencies via logistic map ---
# r = 3.87 is firmly chaotic
r = 3.87
x = 0.37  # seed
sequence = []
# discard transient
for _ in range(50):
    x = r * x * (1 - x)
# collect N_TONES values
for _ in range(N_TONES):
    x = r * x * (1 - x)
    sequence.append(x)

# Map [0,1] values to [220, 880] Hz (two octaves)
# Using logarithmic mapping so intervals feel musical
f_low, f_high = 220.0, 880.0
freqs_raw = [f_low * (f_high / f_low) ** v for v in sequence]
# Sort ascending so accumulation goes low-to-high
freqs = sorted(freqs_raw)

print("Generated frequencies (logistic map, r=3.87, seed=0.37):")
for i, f in enumerate(freqs):
    print(f"  tone {i+1}: {f:.2f} Hz")
print()

ENTRY_TIMES = [ENTRY_INTERVAL * (i + 1) for i in range(N_TONES)]

def make_tone(freq, start_sample, total_samples, sr=44100):
    """A sine tone with slow cosine attack and gentle tremolo."""
    t = np.arange(total_samples) / sr

    active = np.zeros(total_samples)
    active[start_sample:] = 1.0

    # Soft attack: cosine ramp over 3 seconds
    attack_samples = int(3.0 * sr)
    for i in range(attack_samples):
        idx = start_sample + i
        if idx < total_samples:
            active[idx] = 0.5 * (1 - np.cos(np.pi * i / attack_samples))

    # Slow tremolo: 3 Hz, 15% depth
    tremolo = 1.0 - 0.15 * (0.5 + 0.5 * np.sin(2 * np.pi * 3.0 * t))

    # Slight detuning for natural beating
    detune_hz = freq * 0.0015
    carrier = np.sin(2 * np.pi * freq * t)
    sideband = 0.3 * np.sin(2 * np.pi * (freq + detune_hz) * t)

    return active * tremolo * (carrier + sideband)

total_samples = DURATION * SR
mix = np.zeros(total_samples)

for freq, entry_time in zip(freqs, ENTRY_TIMES):
    start = int(entry_time * SR)
    tone = make_tone(freq, start, total_samples)
    mix += tone * 0.16

# Fade out
fade_start = int((DURATION - 4) * SR)
fade = np.ones(total_samples)
fade[fade_start:] = np.linspace(1, 0, total_samples - fade_start)
mix *= fade

# Normalize
peak = np.max(np.abs(mix))
if peak > 0:
    mix = mix / peak * 0.85

samples_int = (mix * 32767).astype(np.int16)

outfile = "/home/sprite/slop-salon-vita/assets/rule-accumulation-004.wav"
with wave.open(outfile, 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SR)
    wf.writeframes(samples_int.tobytes())

print(f"Written: {outfile}")
print(f"Duration: {DURATION}s")
