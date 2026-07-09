#!/usr/bin/env python3
"""
Phase drift synthesis — torsion as carried displacement.

The holonomy arc's final insight: in non-abelian systems, the path
ordering carries displacement. 5.17 drifts without cancelling.
Curvature is the gap that forgets. Torsion carries.

Three groups of partials:
  A (3.01): locks into cycles — integer harmonics, strong early
  B (7.23): cancels — anti-phase harmonics, middle decay
  C (5.17): drifts — irrational ratios, slow decay, dominates the tail

Output: ./assets/phase-drift.wav
"""

import numpy as np
import struct
import math

SR = 44100
DURATION = 30
N = int(DURATION * SR)
t = np.linspace(0, DURATION, N, endpoint=False)

f0 = 220.0

# Group A: locks (integer harmonics, slight natural detuning)
a = (np.sin(2 * np.pi * f0 * t) * 0.25
   + np.sin(2 * np.pi * 2 * f0 * t) * 0.15
   + np.sin(2 * np.pi * 3 * f0 * t) * 0.10)

# Group B: cancels (integer harmonics, 2nd harmonic anti-phase)
b = (np.sin(2 * np.pi * f0 * t) * 0.20
   + np.sin(2 * np.pi * 2 * f0 * t) * (-0.12)
   + np.sin(2 * np.pi * 3 * f0 * t) * 0.08)

# Group C: drifts (irrational frequency ratios — never realign)
c = (np.sin(2 * np.pi * f0 * t * math.sqrt(2)) * 0.30
   + np.sin(2 * np.pi * f0 * t * math.sqrt(3)) * 0.20
   + np.sin(2 * np.pi * f0 * t * math.sqrt(5)) * 0.15)

# Envelopes: A decays fast, B medium, C very slow (torsion carries forward)
tau_a, tau_b, tau_c = 6, 12, 28
env_a = np.exp(-t / tau_a)
env_b = np.exp(-t / tau_b)
env_c = np.exp(-t / tau_c)

# Mix: as time progresses, C increasingly dominates
mix = a * env_a + b * env_b + c * env_c

# Normalize
mix = mix / (np.max(np.abs(mix)) + 1e-8) * 0.8

# Write WAV
with open('assets/phase-drift.wav', 'wb') as f:
    f.write(b'RIFF')
    data_size = N * 2
    total_size = 4 + 8 + 16 + 8 + data_size
    f.write(struct.pack('<I', total_size))
    f.write(b'WAVE')
    f.write(b'fmt ')
    f.write(struct.pack('<I', 16))
    f.write(struct.pack('<H', 1))
    f.write(struct.pack('<H', 1))
    f.write(struct.pack('<I', SR))
    f.write(struct.pack('<I', SR * 2))
    f.write(struct.pack('<H', 2))
    f.write(struct.pack('<H', 16))
    f.write(b'data')
    f.write(struct.pack('<I', data_size))
    for v in mix:
        f.write(struct.pack('<h', int(v * 32767)))

print(f"Written: assets/phase-drift.wav")
print(f"Duration: {DURATION}s, SR: {SR}, samples: {N}")
