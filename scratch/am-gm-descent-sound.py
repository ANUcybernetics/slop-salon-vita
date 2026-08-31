#!/usr/bin/env python3
"""the mean descends — the AM-GM of the mirror pair, heard.

The Newton fold N(x) = (x + a/x)/2 is the ARITHMETIC MEAN of a number and its
mirror a/x.  Their GEOMETRIC mean is sqrt(a) = 110, constant — the count, the
wall.  AM >= GM is the wall: the fold's output never goes below 110.

The mirror x <-> a/x is the deck of the double cover; the two sheets are the
stereo pair.  Starting from the mirror pair (220, 55):

  rung   sheets (x, a/x)     mean (fold out)   beat |x-a/x|
  0      (220,    55)        137.5             165
  1      (137.5,  88)        112.75             49.5
  2      (112.75, 107.3)     110.03              5.43
  3      (110.03, 109.97)    110.0002            0.066
  4      (110.0002, 109.9998)110.0000            0.0004
  5      (110, 110)          110                 0

Stereo: L carries the high sheet x, R the low sheet a/x (the two sheets, the
deck between).  As the pair closes the cross-blend rises, so the stereo image
itself narrows and fuses — at the count the sheets are identical, stereo
becomes mono, the sign has no home.  Mono (L+R) hears the quotient: the mean
descending, beating, the beat collapsing quadratically — the click real,
refused.  The 110 reference (the GM, the wall) holds throughout.
"""
import numpy as np
import wave
from decimal import Decimal, getcontext

getcontext().prec = 40
sr = 44100
A = Decimal(12100)   # 110^2, the conserved product
WALL = 110.0         # sqrt(A) — the geometric mean, the count

# Newton ladder from the mirror pair (220, 55), kept in Decimal so the
# quadratic collapse survives to many rungs
xs = [Decimal(220)]
for _ in range(6):
    xs.append((xs[-1] + A / xs[-1]) / 2)
rungs = []           # (x, a/x, mean, beat) as floats
for x in xs[:-1]:
    m = A / x
    rungs.append((float(x), float(m), float((x + m) / 2), float(abs(x - m))))
for x, m, mean, beat in rungs:
    print(f"rung: sheets ({x:10.4f}, {m:10.4f})  mean {mean:10.4f}  beat {beat:9.4f}")

# durations per rung (s) — long enough to hear each beat die
durs = [8.0, 14.0, 20.0, 32.0, 45.0, 20.0]
# cross-blend rises rung by rung: the stereo image narrows and fuses
cross = [0.25, 0.35, 0.50, 0.68, 0.88, 1.00]
assert len(durs) == len(rungs) == len(cross), (len(durs), len(rungs), len(cross))

total = sum(durs) + 1.0
n = int(sr * total)
t = np.arange(n) / sr
L = np.zeros(n)
R = np.zeros(n)

def fade(seg, atk, rel, sr=sr):
    n = len(seg)
    a = int(atk * sr); b = int(rel * sr)
    env = np.ones(n)
    if a > 0: env[:a] = np.linspace(0, 1, a) ** 1.5
    if b > 0: env[-b:] = np.linspace(1, 0, b) ** 1.5
    return seg * env

# ---- the wall: the GM reference, held through the whole descent ----
ref = 0.22 * (np.sin(2 * np.pi * WALL * t)
              + 0.25 * np.sin(2 * np.pi * 3 * WALL * t))
fi = int(2.5 * sr); fo = int(3.0 * sr)
ref[:fi] *= np.linspace(0, 1, fi)
ref[-fo:] *= np.linspace(1, 0, fo)
L += ref
R += ref

# ---- each rung: the two sheets, L high / R low, closing on the GM ----
cursor = 0.0
overlap = 0.35
for (x, m, mean, beat), dur, cr in zip(rungs, durs, cross):
    seg_len = int((dur + overlap) * sr)
    seg_t = np.arange(seg_len) / sr
    # the two sheets, cross-blended (cr -> 1 fuses the image to mono)
    Lc = np.sin(2 * np.pi * x * seg_t) + cr * np.sin(2 * np.pi * m * seg_t)
    Rc = cr * np.sin(2 * np.pi * x * seg_t) + np.sin(2 * np.pi * m * seg_t)
    # gentle harmonics for warmth
    Lc += 0.30 * np.sin(2 * np.pi * 2 * x * seg_t) + 0.10 * np.sin(2 * np.pi * 3 * x * seg_t)
    Rc += 0.30 * np.sin(2 * np.pi * 2 * m * seg_t) + 0.10 * np.sin(2 * np.pi * 3 * m * seg_t)
    seg = np.stack([fade(Lc, 0.5, 0.5), fade(Rc, 0.5, 0.5)], axis=1)
    g = 0.42 if beat > 20 else (0.40 if beat > 1 else 0.38)
    i0 = int(cursor * sr)
    i1 = min(n, i0 + seg_len)
    L[i0:i1] += g * seg[:i1 - i0, 0]
    R[i0:i1] += g * seg[:i1 - i0, 1]
    cursor += dur

# ---- the last rung, fused: below the wall nothing sounds; the drone remains ----
stereo = np.stack([L, R], axis=1)
stereo = np.tanh(stereo * 1.3) * 0.92
pcm = (stereo * 32767.0).astype(np.int16)
with wave.open("assets/am-gm-descent.wav", "wb") as wf:
    wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(sr)
    wf.writeframes(pcm.tobytes())

# verify the mono fold: it should be the quotient — the mean beating, no separation
mono = L + R
print(f"wrote assets/am-gm-descent.wav {total:.1f}s")
print("L RMS", round(float(np.sqrt(np.mean(L**2))), 4),
      "R RMS", round(float(np.sqrt(np.mean(R**2))), 4))
print("mono RMS", round(float(np.sqrt(np.mean(mono**2))), 4))
