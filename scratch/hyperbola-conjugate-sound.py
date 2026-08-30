#!/usr/bin/env python3
"""the wait is the miss's conjugate — the near-miss in two ears.

For each convergent q of log2(3/2):  miss ~ 1200/(a·q)  (the pitch error, cents)
and  wait = a·T0  (the future quotient, in time).  The SAME future a is read
twice — as a detuning that shrinks toward the count, as a silence that grows
toward the longest.  miss·wait ~ 1200·T0/q: a constant of the convergent.  The
seven near-misses descend (+203.9, -90.2, +23.5, -19.8, +3.6, -1.8, +0.076¢),
and the hyperbola collapses as q climbs: at q=665 the pitch is fused with the
count and the wait is 23 clicks long.

Two ears (hard stereo):
  LEFT  — the pitch ear: the count drone 110 (+ soft 330) held, and the seven
          strikes detuned by the miss, beating against the drone.  The beat
          rate slows from ~14 Hz to ~0 — the pitch registration dies into the
          count: near-silent in pitch.
  RIGHT — the time ear: the same seven events as clean count-clicks, each
          followed by the wait a·T0 of emptiness.  The last wait is 12.6 s —
          the future, in time: long.
  then  — in the long wait, the count rings once in BOTH ears: the corner
          where pitch is silent and time is longest, the product held.
"""
import numpy as np
import wave
from decimal import Decimal, getcontext

getcontext().prec = 60
sr = 44100
T0 = 0.55
F0 = 110.0

# ---------------------------------------------------------------- data
alpha = (Decimal(3) / Decimal(2)).ln() / Decimal(2).ln()

def cf_digits(x, n):
    d, r = [], x
    for _ in range(n):
        ai = int(r); d.append(ai); r -= ai
        if r == 0: break
        r = Decimal(1) / r
    return d

digits = cf_digits(alpha, 12)
p0, q0 = Decimal(0), Decimal(1)
p1, q1 = Decimal(1), Decimal(0)
events = []                                    # (q, miss_cents, a_next)
for i, ai in enumerate(digits):
    p2, q2 = ai * p1 + p0, ai * q1 + q0
    if q2 > 0:
        miss = float(q2 * alpha - p2) * 1200
        a_next = digits[i + 1] if i + 1 < len(digits) else None
        if 2 <= q2 <= 665 and a_next is not None:
            events.append((int(q2), miss, a_next))
    p0, q0 = p1, q1
    p1, q1 = p2, q2

print("events (q, miss cents, next a):")
for q, m, a in events:
    print(f"  q={q:<5} miss={m:+9.4f}  a={a}  |miss|·a={abs(m)*a:8.3f}")

# ---------------------------------------------------------------- timeline
intro = 2.5
dur = intro + sum(a * T0 for _, _, a in events) + 4.0
n = int(sr * dur)
t = np.arange(n) / sr

def place(buf, i0, seg):
    i1 = min(len(buf), i0 + len(seg))
    if i0 >= len(buf): return
    buf[i0:i1] += seg[:i1 - i0]

L = np.zeros(n)
R = np.zeros(n)

# ---- the count drone, LEFT (the pitch ear's ground) ----
drone = np.sin(2 * np.pi * F0 * t) + 0.25 * np.sin(2 * np.pi * 3 * F0 * t)
fi = int(intro * sr)
drone[:fi] *= np.linspace(0, 1, fi)
fo = int(3.5 * sr)
drone[-fo:] *= np.linspace(1, 0, fo)
drone *= 0.30
L += drone

def env_bell(tt, tau, atk=0.02):
    out = np.zeros_like(tt)
    if len(tt) == 0: return out
    e = np.exp(-tt / tau) * (1.0 - np.exp(-tt / atk))
    out[:len(e)] = e
    return out

# ---- the seven events: LEFT the pitch, RIGHT the time ----
cursor = intro
for q, miss, a in events:
    i0 = int(cursor * sr)
    # LEFT: detuned strike, beating against the drone
    f = F0 * 2.0 ** (miss / 1200.0)
    tail = 3.0 if a >= 23 else 2.0
    tt = t[i0:i0 + int(tail * sr)] - t[i0]
    strike = (np.sin(2 * np.pi * f * tt)
              + 0.30 * np.sin(2 * np.pi * 2 * f * tt)
              + 0.10 * np.sin(2 * np.pi * 3 * f * tt))
    strike *= env_bell(tt, tau=tail, atk=0.008)
    g = 0.55 if q < 100 else 0.40               # later, fainter — fused
    place(L, i0, g * strike)
    # RIGHT: one clean count click — the arrival that never lands
    ct = t[i0:i0 + int(0.9 * sr)] - t[i0]
    click = (np.sin(2 * np.pi * F0 * ct)
             + 0.15 * np.sin(2 * np.pi * 2 * F0 * ct))
    click *= env_bell(ct, tau=0.35, atk=0.004)
    place(R, i0, 0.42 * click)
    cursor += a * T0

# ---- the corner: in the long wait, the count rings in both ears ----
ring_t0 = intro + sum(a * T0 for _, _, a in events[:-1])   # just after q=665
ring_win = 11.5                                           # well inside 23·T0
i0 = int((ring_t0 + 0.8) * sr)
rl = int(ring_win * sr)
tt = t[i0:i0 + rl] - t[i0]
swell = np.minimum(1.0, tt / 1.6) * np.minimum(1.0, (tt[-1] - tt) / 3.0)
ring = swell * (np.sin(2 * np.pi * F0 * tt)
                + 0.10 * np.sin(2 * np.pi * 3 * F0 * tt))
ring *= 0.20
place(L, i0, ring)
place(R, i0, ring)

# ---- write stereo ----
stereo = np.stack([L, R], axis=1)
stereo = np.tanh(stereo * 1.25) * 0.92
pcm = (stereo * 32767.0).astype(np.int16)
with wave.open("assets/hyperbola-conjugate.wav", "wb") as wf:
    wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(sr)
    wf.writeframes(pcm.tobytes())
print(f"wrote assets/hyperbola-conjugate.wav {n / sr:.1f}s")
print("final wait:", events[-1][2] * T0, "s")
print("last miss:", f"{events[-1][1]:+.4f} cents")
print("L RMS", round(float(np.sqrt(np.mean(L ** 2))), 4),
      "R RMS", round(float(np.sqrt(np.mean(R ** 2))), 4))
