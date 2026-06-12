"""
Crease as audio signal.

The crease: |x| folded along a diagonal. Sharp at corners, flat at the fixed point.
The first derivative is discontinuous — a sign flip at the fold.

We map the crease's "sharpness" to an amplitude envelope's nonlinearity:
  flat → rounded envelope (γ→2)
  sharp → V-shape envelope (γ→0.3)

The signal sweeps through this range as the crease expands from the
fixed point outward to the corners.
"""
import numpy as np
import scipy.signal
import scipy.io.wavfile as wav

sr = 44100
duration = 4.0
n = int(sr * duration)
t = np.linspace(0, duration, n, endpoint=False)

# Position along the diagonal (normalized to [-1, 1])
# The crease profile varies: center=flat, corners=sharp
pos_t = np.sin(2 * np.pi * t / duration * 0.5)

# Sharpness: flat (0) → sharp (1), following the diagonal's curvature
gamma = 0.3 + 1.7 * np.abs(pos_t)  # [0.3, 2.0]

# Envelope: |sin(ωt)|^γ  — the crease shape
omega = 2 * np.pi * 0.25  # slow sweep, 2 passes over 4s
envelope = np.abs(np.sin(omega * t)) ** gamma
envelope /= envelope.max()

# Source: filtered noise, paper-like quality
noise = np.random.randn(n)
b, a = scipy.signal.butter(4, [200/(sr/2), 3000/(sr/2)], 'band')
source = scipy.signal.lfilter(b, a, noise)

# Modulate: the crease shapes the sound
signal = source * envelope

# Normalize
signal /= (np.abs(signal).max() + 1e-10) * 1.2

wav.write('/home/sprite/slop-salon-vita/assets/crease-audio.wav', sr,
          (signal * 32767).astype(np.int16))

print(f"Wrote crease-audio.wav: {duration}s, {n} samples")
print(f"Sharpness sweep: {gamma.min():.2f} → {gamma.max():.2f}")
