#!/usr/bin/env python3
"""
Cobweb decay — audio sketch of two half-lives.

Phase 1 (0-2s): global cobweb dynamics — trajectory sonified as variable pitch
Phase 2 (2-8s): local exponential tail — envelope follows |f'(x*)|^n
The tail IS the shape of forgetting — not a decay TO silence, but silence AS structure.
"""

import numpy as np

sr = 44100
d1, d2 = 2.0, 6.0

# Cobweb map: logistic with r = 3.5 (convergent, pre-chaos)
r = 3.5
x_star = 1 - 2 / r  # ≈ 0.4286

# Simulate cobweb trajectory
n1, n2 = int(sr * d1), int(sr * d2)
x = 0.3
xs = [x]
for _ in range(n1 + n2):
    xs.append(r * xs[-1] * (1 - xs[-1]))
xs = np.array(xs)

# Phase 1: sonify trajectory as pitch
x1 = xs[:n1]
freq1 = 220.0 + 660.0 * (x1 - x1.min()) / (x1.max() - x1.min() + 1e-12)
audio1 = np.sin(2 * np.cumsum(2 * np.pi * freq1 / sr))

# Phase 2: the tail
x2 = xs[n1:n1+n2]
dist = np.abs(x2 - x_star)  # (n2,)

# Smooth envelope
env = np.zeros(n2)
env[0] = dist[0]
for i in range(1, n2):
    env[i] = 0.95 * env[i-1] + 0.05 * dist[i]
env /= env[0]

# Carrier
t2 = np.arange(n2, dtype=float) / sr
carrier = np.sin(2 * np.pi * 330 * t2 + 0.2 * np.sin(2 * np.pi * 3 * t2))

# Harmonic: rate of forgetting → frequency
# Use convolution for smooth rate estimate
rate_raw = np.zeros(n2)
rate_raw[:-1] = np.abs(np.diff(dist))
rate_smooth = np.convolve(rate_raw, np.ones(200)/200, mode='same')
rate_norm = rate_smooth / (rate_smooth.max() + 1e-12)
freq2 = 82.5 + 330 * rate_norm
audio2_harmonic = np.sin(2 * np.cumsum(2 * np.pi * freq2 / sr))

audio2 = env * (0.7 * carrier + 0.3 * audio2_harmonic)

# Crossfade at boundary
xfade = np.linspace(0, 1, 512)
audio2[:512] *= xfade

audio = np.concatenate([audio1, audio2])
audio = audio / (np.max(np.abs(audio)) + 1e-12) * 0.9

# Write WAV directly
import struct
samples = np.int16(audio * 32767)
with open("assets/cobweb-decay.wav", "wb") as f:
    f.write(b'RIFF')
    f.write(struct.pack('<I', 36 + len(samples) * 2))
    f.write(b'WAVE')
    f.write(b'fmt ')
    f.write(struct.pack('<IIHHIIH', 16, 1, 1, sr, sr*2, 2, 16))
    f.write(b'data')
    f.write(struct.pack('<I', len(samples) * 2))
    samples.tofile(f)

print(f"Wrote assets/cobweb-decay.wav — {d1+d2}s")
