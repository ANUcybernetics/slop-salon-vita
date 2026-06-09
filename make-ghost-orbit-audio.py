#!/usr/bin/env python3
"""Ghost orbit in audio: tone approaches a center frequency that never arrives.

Near a saddle-node bifurcation below threshold (epsilon > 0), trajectories
follow the ghost of the missing fixed point. The slowing follows a 1/epsilon
law — the further the center is from the threshold, the faster the approach;
as epsilon → 0, the period goes to infinity.

This maps to a tone that sweeps toward a center frequency but never crosses it,
with the approach slowing asymptotically. The center exists only as a limit.
"""

import numpy as np

fs = 44100
duration = 30  # seconds

t = np.linspace(0, duration, int(fs * duration), endpoint=False)

# Parameters
center_freq = 440.0  # Hz — the absent fixed point
base_freq = 400.0    # starting frequency
epsilon = 0.02       # distance from threshold (controls approach speed)

# Ghost orbit frequency modulation: the frequency sweeps toward center_freq
# following the ghost orbit law: approach slows as it gets closer
# The "ghost" of the missing fixed point exerts a pull that weakens with distance
# but the trajectory always stays outside

# Phase accumulation: integrate the instantaneous frequency
# Instantaneous frequency = base + delta * (1 - exp(-t/tau))
# where delta is the total sweep and tau controls the slowing

delta = 40.0  # total frequency sweep (Hz)
tau = 0.15    # time constant — smaller = faster approach, larger = more lingering

# Ghost orbit profile: the frequency approaches center_freq asymptotically
# from below, never arriving
# f(t) = center - (center - base) * exp(-t/tau) * (1 + 0.3*sin(0.5*t))
# The sinusoidal term adds the "pulse" — periodic soft pulses like lou's video
# representing the periodic forcing in a real system

instantaneous_freq = center_freq - (center_freq - base_freq) * np.exp(-t / tau) * (1 + 0.15 * np.sin(2 * np.pi * 0.5 * t))

# Integrate phase from frequency
phase = np.cumsum(instantaneous_freq) * (2 * np.pi / fs)

# Carrier tone
carrier = 0.3 * np.sin(phase)

# Add a second harmonic for richness
phase2 = np.cumsum(instantaneous_freq * 2) * (2 * np.pi / fs)
harmonic = 0.1 * np.sin(phase2)

# Ambient drone: low rumble
drone_freq = 55.0  # A1
drone_phase = np.cumsum(drone_freq) * (2 * np.pi / fs)
drone = 0.15 * np.sin(drone_phase)

# Add subtle noise floor for texture
noise = 0.01 * np.random.randn(len(t))

# Mix
signal = carrier + harmonic + drone + noise

# Envelope: fade in, sustain, fade out
fade_in = np.minimum(1.0, t / 2.0)
fade_out = np.minimum(1.0, (fs * duration - t) / (fs * 2.0))
# Add a middle section with subtle breathing
breathing = 1.0 + 0.1 * np.sin(2 * np.pi * 0.1 * t)
envelope = fade_in * fade_out * breathing

signal *= envelope

# Normalize
signal /= np.max(np.abs(signal)) * 0.95

# Write as WAV using scipy
from scipy.io import wavfile

wav_path = "assets/ghost-orbit.wav"
wavfile.write(wav_path, fs, (signal * 0.95 * 32767).astype(np.int16))
print(f"Wrote {wav_path}: {duration}s at {fs}Hz, peak={np.max(np.abs(signal)):.3f}")
