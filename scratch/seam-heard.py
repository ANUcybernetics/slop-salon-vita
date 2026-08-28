"""one set, two measures, heard.

The count is a drone, mid — measure 0, never moves.
The where is a twin, side — a tone stepping toward the drone, its detune
1 - d_K (the miss of the dimension ladder), the beat slowing, never landing.
In mono the side cancels: only the count remains.

d_K from the spectral radius of the continued-fraction transfer operator.
"""
import numpy as np
import subprocess, os

SR = 44100
F0 = 110.0
SCALE = 8.0          # Hz detune per unit miss
FINAL_HOLD = 15.0
INTRO = 2.0

# (K, miss=1-dim) ladder from two-ones-dim spectral computation
ladder = [
    (2, 0.4687), (3, 0.2943), (4, 0.2111), (5, 0.1632), (6, 0.1324),
    (8, 0.0954), (10, 0.0743), (13, 0.0555), (16, 0.0441), (20, 0.0346),
    (25, 0.0272), (30, 0.0224), (40, 0.0165), (60, 0.0108), (100, 0.0063),
]

# --- schedule ---
events = []   # (t_start, freq)
t = INTRO
for i, (K, miss) in enumerate(ladder):
    freq = F0 + miss * SCALE
    events.append((t, freq, K, miss))
    if i < len(ladder) - 1:
        t += min(0.125 / miss, 8.0)
    else:
        t += FINAL_HOLD
T = t + 1.0
N = int(SR * T)
tt = np.arange(N) / SR

# --- drone (mid): F0 with harmonics, gentle breathing, fade in ---
drone = np.zeros(N)
for h, a in [(1, 0.5), (2, 0.22), (3, 0.12)]:
    drone += a * np.sin(2 * np.pi * h * F0 * tt)
drone *= 1.0 + 0.04 * np.sin(2 * np.pi * tt / 26.0)
drone *= np.minimum(1.0, tt / 2.0)
drone *= np.minimum(1.0, (T - tt) / 0.8)   # gentle tail fade

# --- twin (side): piecewise-constant detune stepping down, attack at each step ---
twin = np.zeros(N)
ring = np.zeros(N)
for j, (t0, freq, K, miss) in enumerate(events):
    i0 = int(t0 * SR)
    i1 = int((events[j + 1][0] if j + 1 < len(events) else t + 0.5) * SR)
    i1 = min(i1, N)
    n = i1 - i0
    seg_t = np.arange(n) / SR
    # attack: quick swell so each step is heard as an event
    atk = np.minimum(1.0, seg_t / 0.04) * np.minimum(1.0, (n - seg_t * SR) / 0.05)
    twin[i0:i1] += np.sin(2 * np.pi * freq * seg_t) * atk
    # landing ring that doesn't land: decaying partial at the new pitch
    tau = 0.6 if j < len(events) - 1 else 2.0
    n_r = min(int(tau * 6 * SR), N - i0)
    r_t = np.arange(n_r) / SR
    ring[i0:i0 + n_r] += 0.28 * np.sin(2 * np.pi * freq * r_t) * np.exp(-r_t / tau)

# --- mix: drone mid, twin+ring side (mono cancels the where) ---
L = drone + twin + ring
R = drone - twin - ring
peak = max(np.abs(L).max(), np.abs(R).max())
L *= 0.85 / peak
R *= 0.85 / peak
stereo = np.stack([L, R], axis=1)

os.makedirs("assets", exist_ok=True)
wav = "assets/seam-heard.wav"
import wave
with wave.open(wav, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((stereo * 32767).astype(np.int16).tobytes())
print("wav", round(T, 1), "s ->", wav)
