#!/usr/bin/env python3
"""the wait is the future — the CF clock, heard.

The near-misses of the fifth, q·||q·log2(3/2)|| in cents: +204, -90, +23.5,
-19.8, +3.6, -1.8, +0.076.  Each is a convergent of log2(3/2) — and each
carries the next quotient inside it:  miss  ~  1200/(a_{n+1} · q).

So the future quotient is heard twice.  As a PITCH: the miss is the small
detuning of the strike from the count, 110.  As a WAIT: the same quotient a_{n+1}
is the silence before the next convergent arrives (wait = a_{n+1}·T0).

  0.076  ~  1200/(23·665)   — the deepest near-miss is fused with the count,
and the silence that follows it is 23 clicks long.  precision is patience;
the count is the never-landed; the future is the wait.

Structure (stereo, ~28s):
  the count: 110 Hz drone + soft 330, mid, held throughout — the seat, the
             never-landed, never rings until the end.
  seven strikes, one per convergent q = 2,5,12,41,53,306,665:
             a bell at 110 · 2^(miss/1200), panned by sign (over -> right,
             under -> left); the detuning IS the miss, the beat against the
             drone slows as the miss shrinks.
  after each strike, the wait = a_{n+1}·T0 of near-silence — the future
             quotient, in time.  after q=665 the wait is 23·T0: long.
  the fused count rings once in the long wait, then fades.
"""
import numpy as np
import wave
from decimal import Decimal, getcontext

getcontext().prec = 50
sr = 44100
T0 = 0.55

# ----------------------------------------------------------------------
# the convergent data, computed exactly
# ----------------------------------------------------------------------
alpha = (Decimal(3) / Decimal(2)).ln() / Decimal(2).ln()

def cf_digits(x, n):
    d = []
    r = x
    for _ in range(n):
        ai = int(r)
        d.append(ai)
        r = r - ai
        if r == 0:
            break
        r = Decimal(1) / r
    return d

digits = cf_digits(alpha, 12)          # [0,1,1,2,2,3,1,5,2,23,2,2]
p0, q0 = Decimal(0), Decimal(1)
p1, q1 = Decimal(1), Decimal(0)
convs = []                              # (q, miss_cents, next_quotient)
for i, ai in enumerate(digits):
    p2 = ai * p1 + p0
    q2 = ai * q1 + q0
    if q2 > 0:
        miss_alpha = q2 * alpha - p2                      # SIGNED: over/under
        miss_c = float(miss_alpha * 1200)
        a_next = digits[i + 1] if i + 1 < len(digits) else None
        if 2 <= q2 <= 665 and a_next is not None:
            convs.append((int(q2), miss_c, a_next))
    p0, q0 = p1, q1
    p1, q1 = p2, q2

print("convergents q, miss cents, next quotient:")
for q, m, a in convs:
    print(f"  q={q:<5} miss={m:+10.6f} cents   next={a}")
    if a >= 5:
        assert abs(a * q * m / 1200 - 1) < 0.3, (q, m, a)  # miss ~ 1200/(a·q) at big a

# ----------------------------------------------------------------------
# build the timeline
# ----------------------------------------------------------------------
F0 = 110.0
intro = 3.0                                   # drone fade-in before first strike
dur = intro + sum(a * T0 for _, _, a in convs) + 6.0   # +6s outro
n = int(sr * dur)
t = np.arange(n) / sr

def env_bell(tt, tau=2.0, atk=0.02):
    """attack then exponential decay; empty input -> empty output."""
    out = np.zeros_like(tt)
    if len(tt) == 0:
        return out
    e = np.exp(-tt / tau) * (1.0 - np.exp(-tt / atk))
    out[:len(e)] = e
    return out

def place(buf, i0, seg):
    i1 = min(len(buf), i0 + len(seg))
    if i0 >= len(buf):
        return
    buf[i0:i1] += seg[:i1 - i0]

mid = np.zeros(n)
side = np.zeros(n)

# ---- the count: 110 + soft 330, mid, held. the seat that never rings ----
drone = (np.sin(2 * np.pi * F0 * t)
         + 0.28 * np.sin(2 * np.pi * 3 * F0 * t))
fi = int(3.0 * sr)
drone[:fi] *= np.linspace(0, 1, fi)
fo = int(5.0 * sr)
drone[-fo:] *= np.linspace(1, 0, fo)
drone *= 0.30
mid += drone

# ---- the seven strikes ----
cursor = intro
for q, miss_c, a in convs:
    f = F0 * 2.0 ** (miss_c / 1200.0)
    pan = 0.65 if miss_c > 0 else -0.65        # over -> right, under -> left
    i0 = int(cursor * sr)
    tail = 3.0 if a >= 23 else 1.8             # the long future rings longer
    tt = t[i0:i0 + int(tail * sr)] - t[i0]
    strike = (np.sin(2 * np.pi * f * tt)
              + 0.35 * np.sin(2 * np.pi * 2 * f * tt)
              + 0.12 * np.sin(2 * np.pi * 3 * f * tt))
    strike *= env_bell(tt, tau=tail, atk=0.008)
    g = 0.55 if q < 100 else 0.42              # later, fainter, more fused
    place(side, i0, g * pan * strike)
    place(mid, i0, g * strike)                 # mono-safe strike core
    cursor += a * T0

# ---- the fused count rings once in the long wait ----
last_q, last_miss, last_a = convs[-1]
ring_t0 = intro + sum(a * T0 for _, _, a in convs[:-1])   # just after q=665
ring_t1 = ring_t0 + last_a * T0
i0 = int((ring_t0 + 0.6) * sr)
rl = int((ring_t1 - ring_t0 - 0.6) * sr)
if rl > 0:
    tt = t[i0:i0 + rl] - t[i0]
    swell = np.minimum(1.0, tt / 1.5) * np.minimum(1.0, (tt[-1] - tt) / 3.0)
    ring = swell * np.sin(2 * np.pi * F0 * tt)        # pure 110, breathing, no note
    place(mid, i0, 0.16 * ring)
    place(side, i0, 0.06 * ring)

# ---- stereo: L = mid + side, R = mid - side.  mono = mid exactly ----
L = mid + side
R = mid - side
stereo = np.stack([L, R], axis=1)
stereo = np.tanh(stereo * 1.2) * 0.92
pcm = (stereo * 32767.0).astype(np.int16)
with wave.open("assets/cf-clock-future.wav", "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(pcm.tobytes())

mono_pcm = (np.tanh(np.stack([mid, mid], axis=1) * 1.2) * 0.92 * 32767.0).astype(np.int16)
with wave.open("assets/cf-clock-future-mono.wav", "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(mono_pcm.tobytes())

print(f"wrote assets/cf-clock-future.wav {n / sr:.1f}s")
print("final wait:", last_a * T0, "s  (the 23, in time)")
print("last miss:", f"{last_miss:+.4f} cents (fused with the count)")
print("mid RMS:", round(float(np.sqrt(np.mean(mid ** 2))), 4))
print("peak:", round(float(np.max(np.abs(stereo))), 3))
