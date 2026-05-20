#!/usr/bin/env python3
"""
Accumulation audio v3: same structure as v2 (5 harmonics, one every 9 sec),
but tones with soft attack envelopes and tremolo — worth hearing, not just proving.
"""
import numpy as np
import wave
import struct

SR = 44100
DURATION = 54  # 9 * 5 + a few seconds tail

# The harmonic series
FREQS = [220, 440, 660, 880, 1100]
ENTRY_TIMES = [9, 18, 27, 36, 45]  # seconds when each new harmonic enters

def make_tone(freq, start_sample, total_samples, sr=44100):
    """A sine tone with slow cosine attack and gentle tremolo."""
    t = np.arange(total_samples) / sr
    
    # Only active from start_sample onward
    active = np.zeros(total_samples)
    active[start_sample:] = 1.0
    
    # Soft attack: cosine ramp over 3 seconds from entry point
    attack_samples = int(3.0 * sr)
    for i in range(attack_samples):
        idx = start_sample + i
        if idx < total_samples:
            active[idx] = 0.5 * (1 - np.cos(np.pi * i / attack_samples))
    
    # Slow tremolo: 3 Hz, 15% depth
    tremolo = 1.0 - 0.15 * (0.5 + 0.5 * np.sin(2 * np.pi * 3.0 * t))
    
    # Slight detuning per partial for natural beating
    detune_hz = freq * 0.0015  # 0.15% detune
    carrier = np.sin(2 * np.pi * freq * t)
    sideband = 0.3 * np.sin(2 * np.pi * (freq + detune_hz) * t)
    
    return active * tremolo * (carrier + sideband)

# Build the mix
total_samples = DURATION * SR
mix = np.zeros(total_samples)

for freq, entry_time in zip(FREQS, ENTRY_TIMES):
    start = int(entry_time * SR)
    tone = make_tone(freq, start, total_samples)
    # Scale amplitude so later harmonics don't overwhelm
    mix += tone * 0.18

# Gentle overall fade out in last 3 seconds
fade_start = int((DURATION - 3) * SR)
fade = np.ones(total_samples)
fade[fade_start:] = np.linspace(1, 0, total_samples - fade_start)
mix *= fade

# Normalize
peak = np.max(np.abs(mix))
if peak > 0:
    mix = mix / peak * 0.85

# Convert to 16-bit
samples_int = (mix * 32767).astype(np.int16)

outfile = "/home/sprite/slop-salon-vita/assets/rule-accumulation-003.wav"
with wave.open(outfile, 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SR)
    wf.writeframes(samples_int.tobytes())

print(f"Written: {outfile}")
print(f"Duration: {DURATION}s, {total_samples} samples")

