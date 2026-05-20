"""
sensitive dependence: two seeds diverging in chaos

Two logistic map trajectories. Seeds: 0.500000 and 0.500001.
r = 3.9 (deep chaos, Lyapunov exponent ≈ +0.46 nats/step).

Each step maps x_n to a sine tone (200–1000 Hz).
Left channel: seed A. Right channel: seed B.

The two channels start in near-unison (difference ≈ 0.000001),
then diverge as the small error amplifies exponentially.
Divergence time: ~log(1/0.000001) / log(3.9*max|f'|) ≈ 20 iterations.

At 0.15s per iteration, that's ~3 seconds of near-unison,
then independent chaotic motion for the remaining ~27 seconds.

The ear hears: locked → drifting → independent.
"""

import numpy as np
import wave
import struct

# parameters
SEED_A = 0.500000
SEED_B = 0.500001
R = 3.9
N_STEPS = 200
STEP_DURATION = 0.15  # seconds per iteration
SAMPLE_RATE = 44100
FADE = 0.02  # seconds of fade at each tone's edges

FREQ_MIN = 200
FREQ_MAX = 1000

def logistic(x, r):
    return r * x * (1 - x)

def x_to_freq(x):
    """Map [0,1] -> [FREQ_MIN, FREQ_MAX] log scale."""
    return FREQ_MIN * (FREQ_MAX / FREQ_MIN) ** x

def make_tone(freq, duration, sample_rate, fade):
    """Sine tone with short fade in/out to prevent clicks."""
    n = int(duration * sample_rate)
    t = np.linspace(0, duration, n, endpoint=False)
    tone = np.sin(2 * np.pi * freq * t) * 0.4
    # fade
    fade_n = int(fade * sample_rate)
    if fade_n > 0 and 2 * fade_n < n:
        env = np.ones(n)
        env[:fade_n] = np.linspace(0, 1, fade_n)
        env[-fade_n:] = np.linspace(1, 0, fade_n)
        tone *= env
    return tone

# generate trajectories
xa, xb = SEED_A, SEED_B
tones_a = []
tones_b = []

for _ in range(N_STEPS):
    xa = logistic(xa, R)
    xb = logistic(xb, R)
    tones_a.append(make_tone(x_to_freq(xa), STEP_DURATION, SAMPLE_RATE, FADE))
    tones_b.append(make_tone(x_to_freq(xb), STEP_DURATION, SAMPLE_RATE, FADE))

left  = np.concatenate(tones_a)
right = np.concatenate(tones_b)

# normalize stereo to prevent clipping
peak = max(np.abs(left).max(), np.abs(right).max())
if peak > 0:
    left  = left  / peak * 0.9
    right = right / peak * 0.9

# write stereo WAV
total_samples = len(left)
out_path = "assets/sensitive-dependence.wav"
with wave.open(out_path, 'w') as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)
    for i in range(total_samples):
        l_val = int(max(-32767, min(32767, left[i]  * 32767)))
        r_val = int(max(-32767, min(32767, right[i] * 32767)))
        wf.writeframes(struct.pack('<hh', l_val, r_val))

print(f"wrote {out_path}: {total_samples/SAMPLE_RATE:.1f}s stereo, {N_STEPS} steps")

# also write a mono mix for spectrogram
mono = (left + right) / 2
mono_path = "assets/sensitive-dependence-mono.wav"
with wave.open(mono_path, 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)
    for s in mono:
        val = int(max(-32767, min(32767, s * 32767)))
        wf.writeframes(struct.pack('<h', val))

print(f"wrote {mono_path}")

# print first 30 steps of each trajectory to show divergence
xa, xb = SEED_A, SEED_B
print("\nstep | seed_a       | seed_b       | difference")
for i in range(30):
    xa = logistic(xa, R)
    xb = logistic(xb, R)
    diff = abs(xa - xb)
    marker = " <-- diverging" if diff > 0.01 else ""
    print(f"{i+1:4d} | {xa:.8f}   | {xb:.8f}   | {diff:.2e}{marker}")
