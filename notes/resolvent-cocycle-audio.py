#!/usr/bin/env python3
"""
Resolvent cocycle sonification — third angle of audio register.

The resolvent cocycle: R(λ) - R(μ) = (μ - λ)R(λ)R(μ)
This is algebraic, not metric. No norm needed.

Three structural signals from the cocycle:
1. det(R(λ_j) @ R(λ_{j+1})) — winding of the cocycle determinant
2. trace(R(λ_j) @ R(λ_{j+1})) — composition of resolvent poles
3. Cocycle identity residual — where the algebra fails (pseudospectral boundary)

These are all operator-ALGEBRAIC invariants. The resolvent norm is a metric
reading. This is the algebraic reading of the same object.

The cocycle product's determinant winds — each eigenvalue of A contributes
a term. The winding number of det(cocycle_product) counts how many eigenvalues
are enclosed by the spiral, matching the clutching number.

But the cocycle PRODUCT (matrix) is richer: it composes two resolvents,
and its eigenvalue structure shows how the coordinate system at λ_j
maps to λ_{j+1}. This is parallel transport in the resolvent bundle.

Audio design:
- det winding → bass drone frequency (log |det| = pitch)
- cocycle product trace → FM index
- cocycle identity residual magnitude → transient events
  (residual blow-up = pseudospectral = structural tension)
"""

import numpy as np
import json, struct, math

n = 50
A = np.zeros((n, n), dtype=complex)
# Non-normal matrix: dense perturbation creates genuine non-normality
for i in range(n):
    A[i, i] = -0.5 + 0.3j * (i / n)
for i in range(n - 1):
    A[i, i + 1] = 2.0
# Add a subdiagonal element to break upper-triangular structure
A[n-1, 0] = 0.5  # wrap-around coupling → genuine non-normality

T = 300
theta = np.linspace(0, 6 * np.pi, T)
r = 0.5 + 0.08 * theta
lambdas = r * np.exp(1j * theta)

print("Computing resolvents...")
resolvents = np.array([
    np.linalg.inv(lam * np.eye(n) - A) for lam in lambdas
])

print("Computing cocycle structure...")

det_values = []
trace_values = []
residuals = []
cocycle_prod_eigenvalues = []

for j in range(T - 1):
    Rj = resolvents[j]
    Rj1 = resolvents[j + 1]
    prod = Rj @ Rj1

    det_values.append(np.linalg.det(prod))
    trace_values.append(np.trace(prod))

    # Cocycle identity residual
    residual = Rj - Rj1 - (lambdas[j + 1] - lambdas[j]) * (Rj @ Rj1)
    residuals.append(np.linalg.norm(residual, 'fro'))

    # Top eigenvalues of cocycle product (for richness)
    evals = np.linalg.eigvals(prod)
    cocycle_prod_eigenvalues.append(evals)

det_values = np.array(det_values)
trace_values = np.array(trace_values)
residuals = np.array(residuals)

# Normalize residuals for triggering
residual_max = np.max(residuals)
residual_log = np.log1p(np.abs(residuals))  # log scale for blow-up regions

print(f"Det range: [{np.min(np.abs(det_values)):.2e}, {np.max(np.abs(det_values)):.2e}]")
print(f"Residual range: [{np.min(residuals):.2e}, {np.max(residuals):.2e}]")
print(f"Residual mean: {np.mean(residuals):.2e}")

# --- AUDIO SYNTHESIS ---
sr = 44100
duration = 60  # seconds
N = int(sr * duration)
t = np.linspace(0, duration, N)

# Map time steps to audio samples
samples_per_step = N // (T - 1)

audio = np.zeros(N, dtype=np.float64)

for j in range(T - 1):
    # Map this cocycle step to a time segment
    start = j * samples_per_step
    end = min(start + samples_per_step, N)
    seg_len = end - start
    if seg_len <= 0:
        continue

    seg_t = np.linspace(0, 1, seg_len)

    det_val = det_values[j]
    trace_val = trace_values[j]
    residual_val = residuals[j]

    # det winding → bass frequency
    # |det| increases as we enclose more eigenvalues
    det_mag = np.abs(det_val)
    det_phase = np.angle(det_val)
    # log scale for frequency (octave mapping)
    freq_bass = 55.0 * np.exp(np.clip(np.log1p(np.abs(det_val)), 0, 2))
    freq_bass = np.clip(freq_bass, 30, 400)

    # trace → FM modulation index
    trace_mag = np.abs(trace_val)
    fm_index = 2.0 * np.clip(np.log1p(trace_mag), 0.1, 10)

    # Cocycle product phase → pan
    trace_phase = np.angle(trace_val)
    pan = 0.5 + 0.5 * np.cos(trace_phase)

    # Residual → transient amplitude
    residual_norm = np.log1p(np.abs(residual_val)) / (np.log1p(residual_max) + 1)
    transient_amp = residual_norm ** 2  # emphasize blow-up regions

    # Synthesize
    # Bass drone: det phase as slow phase modulation
    bass_freq = freq_bass * (1 + 0.05 * np.sin(seg_t * np.pi * 4))
    bass_phase = np.cumsum(bass_freq) * (2 * np.pi / sr)
    bass = 0.15 * np.sin(bass_phase + fm_index * np.sin(2 * np.pi * 3.0 * seg_t))

    # FM carrier: trace phase as carrier modulator
    carrier = 0.1 * fm_index * np.sin(
        2 * np.pi * 220 * seg_t +
        3.0 * np.sin(2 * np.pi * det_phase * seg_t * 2)
    )

    # Transient events at residual blow-up
    if residual_norm > 0.3:
        transient = transient_amp * 0.3 * np.exp(-seg_t * 10) * np.sin(
            2 * np.pi * 880 * seg_t
        )
    else:
        transient = np.zeros(seg_len)

    # Stereo panning
    left = (1 - pan) * (bass + carrier + transient)
    right = pan * (bass + carrier + transient)

    audio[start:end] += left * 0.5 + right * 0.5

# Normalize and convert
audio = audio / np.max(np.abs(audio)) * 0.85
audio_16 = np.int16(audio * 32767)

# Write WAV
with open("/home/sprite/slop-salon-vita/assets/resolvent-cocycle.wav", "wb") as f:
    f.write(b'RIFF')
    f.write(struct.pack('<I', 36 + len(audio_16) * 2))
    f.write(b'WAVE')
    f.write(b'fmt ')
    f.write(struct.pack('<I', 16))
    f.write(struct.pack('<H', 1))  # PCM
    f.write(struct.pack('<H', 2))  # stereo
    f.write(struct.pack('<I', sr))
    f.write(struct.pack('<I', sr * 4))
    f.write(struct.pack('<H', 4))  # block align
    f.write(struct.pack('<H', 16))  # bits per sample
    f.write(b'data')
    f.write(struct.pack('<I', len(audio_16) * 2))
    f.write(audio_16.tobytes())

print(f"Audio: {duration}s stereo @ {sr}Hz, {N} samples")
print(f"Peak: {np.max(np.abs(audio)):.3f}")

# Save structural data
data = {
    "det_values": np.abs(det_values).tolist(),
    "det_phases": np.angle(det_values).tolist(),
    "trace_mags": np.abs(trace_values).tolist(),
    "trace_phases": np.angle(trace_values).tolist(),
    "residuals": residuals.tolist(),
    "lambdas": lambdas.tolist(),
}
with open("/home/sprite/slop-salon-vita/assets/resolvent-cocycle-data.json", "w") as f:
    json.dump(data, f)

# Summary of key regions
print("\nKey cocycle regions:")
for j in [0, T//6, T//3, T//2, 2*T//3, 5*T//6, T-2]:
    print(f"  Step {j:>3}: det={np.abs(det_values[j]):.2e}, "
          f"res={residuals[j]:.2e}, "
          f"trace={np.abs(trace_values[j]):.2f}, "
          f"det_phase={np.angle(det_values[j]):.3f}")
