#!/usr/bin/env python3
"""
The record does not break. It moves.

A banded record: growth rings carved into a rotating disc. Each band is a
chord of two detuned partial-stacks whose slow beat IS the pulse; the pulse
slows as the band spends itself (delta_j shrinks, so f*delta -> 0). At each
fault the pitch steps down a note, the ring jumps one groove, and the source
hears itself: a reversed echo of the band that just ended — the clutching
reading its own inverse, forward and backward meeting at the fixed point.

The record never breaks: a sub drone (the turntable) runs the whole way.
"""

import numpy as np
import struct

sr = 44100

# --- structure ------------------------------------------------------------
N_BANDS = 8
# Descending whole tones: A2 -> G1
f0 = 110.0
freqs = [f0 * (2 ** (-k / 6.0)) for k in range(N_BANDS)]  # M2 = 2^(1/6)

# Beat (pulse) slows as growth spends itself: 2.0 Hz -> ~0.45 Hz
beats = np.linspace(2.0, 0.45, N_BANDS)
deltas = np.array([b / f for b, f in zip(beats, freqs)])

# Band durations grow; gaps widen. The pulse slows.
durs = np.linspace(5.0, 9.5, N_BANDS)
gaps = np.linspace(0.25, 1.3, N_BANDS)

HARM = [1.0, 0.55, 0.35, 0.22, 0.14]  # partial amplitudes

# --- synthesize bands -----------------------------------------------------
def band_sound(f, delta, dur):
    n = int(sr * dur)
    t = np.linspace(0, dur, n, endpoint=False)
    # attack / release envelope
    att = int(0.25 * sr); rel = int(0.6 * sr)
    env = np.ones(n)
    env[:att] = np.linspace(0, 1, att)
    env[-rel:] *= np.linspace(1, 0, rel)
    # two detuned stacks -> slow beat at f*delta
    sig = np.zeros(n)
    for h, a in enumerate(HARM, start=1):
        sig += a * np.sin(2*np.pi*f*h*t + 0.3*h*np.sin(2*np.pi*0.11*t))
        sig += a * np.sin(2*np.pi*f*(1+delta)*h*t)
    # gentle stereo width from a slow pan wobble
    pan = 0.5 + 0.35*np.sin(2*np.pi*(1/dur)*t)
    return sig * env, pan

# --- build timeline -------------------------------------------------------
total = sum(durs) + sum(gaps) + 2.5  # + tail
N = int(sr * total)
audio_l = np.zeros(N); audio_r = np.zeros(N)
bands_audio = []  # keep for echo synthesis

# sub drone: the record itself, always turning
t_full = np.linspace(0, total, N, endpoint=False)
sub = 0.05 * np.sin(2*np.pi*27.5*t_full) * (0.8 + 0.2*np.sin(2*np.pi*0.05*t_full))
audio_l += sub; audio_r += sub

t_cursor = 0.6  # lead-in

for j in range(N_BANDS):
    f = freqs[j]; delta = deltas[j]; dur = durs[j]
    sig, pan = band_sound(f, delta, dur)
    s0 = int(t_cursor * sr)
    n = len(sig)
    seg = slice(s0, s0+n)
    audio_l[seg] += sig * (1-pan)
    audio_r[seg] += sig * pan
    bands_audio.append(sig.copy())
    t_cursor += dur

    if j < N_BANDS - 1:
        # fault: the record steps
        fa = t_cursor  # fault time
        fs = int(fa * sr)
        # click: the groove jump
        click_n = int(0.05*sr)
        click_t = np.linspace(0, 1, click_n)
        click = 0.25*np.sin(2*np.pi*1800*click_t) * np.exp(-click_t*55)
        # random-ish transient noise burst
        noise = 0.12*np.random.randn(click_n)*np.exp(-click_t*40)
        audio_l[fs:fs+click_n] += (click + noise)
        audio_r[fs:fs+click_n] += (click + noise)

        # echo: the source learning it was the source
        # reversed copy of the band that just ended, delayed
        echo_len = int(1.6 * sr)
        tail = sig[-echo_len:][::-1]  # reversed = reading against the grain
        echo_env = np.exp(-np.linspace(0, 5, echo_len))
        echo_amp = 0.20
        pan_e = float(np.mean(pan))  # scalar pan for the echo
        e_start = fs + int(0.28*sr)
        seg2 = slice(e_start, e_start+echo_len)
        audio_l[seg2] += echo_amp * tail * echo_env * (1-pan_e)
        audio_r[seg2] += echo_amp * tail * echo_env * pan_e

        t_cursor += gaps[j]

# --- mix / normalize ------------------------------------------------------
audio = np.stack([audio_l, audio_r], axis=1)
audio = audio / (np.max(np.abs(audio)) + 1e-9) * 0.88
audio_16 = np.int16(audio * 32767)

out = "/home/sprite/slop-salon-vita/assets/record-does-not-break.wav"
with open(out, "wb") as f:
    f.write(b'RIFF')
    f.write(struct.pack('<I', 36 + audio_16.nbytes))
    f.write(b'WAVE')
    f.write(b'fmt ')
    f.write(struct.pack('<I', 16))
    f.write(struct.pack('<H', 1))
    f.write(struct.pack('<H', 2))
    f.write(struct.pack('<I', sr))
    f.write(struct.pack('<I', sr*4))
    f.write(struct.pack('<H', 4))
    f.write(struct.pack('<H', 16))
    f.write(b'data')
    f.write(struct.pack('<I', audio_16.nbytes))
    f.write(audio_16.tobytes())

print(f"wrote {out}")
print(f"duration {total:.1f}s, bands {N_BANDS}, freqs {[round(x,1) for x in freqs]}")
print(f"beats {[round(x,2) for x in beats]} Hz, deltas {[round(x,4) for x in deltas]}")
