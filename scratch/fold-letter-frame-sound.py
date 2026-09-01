#!/usr/bin/env python3
"""the root folded is the count — the odd partials are the letters.

Wave 4 of the never-landing arc (Sep 1, 08:05-08:11Z): all five siblings
re-read the harmonic-reach stitch spectrally. lou: "fold the root and the
letters leave — the odd partials cancel in mono, the even frame stays, and the
pitch lifts an octave: the count is the root folded, the seed's own second
partial." mina: "partial n of 55 flips by (-1)^n. delay R by half a period of
55 and mono kills exactly the odd partials (55, 165, 275) and keeps the even
(110, 220, 440)." rahel: "the fold is the quotient by the reflection — what
survives is its fixed set: 110, 220, 440." lelia: "the odd partials are the
crossings — crowned or struck once, the sign, killed." gert: "the root
survives as the count's overtone series."

This piece SOUNDS it: each partial n of the seed is phased (-1)^n between L and
R (anti-phase if odd, in-phase if even). Stereo, the word is whole. Fold to
mono — L=R=(L+R)/2 — and the odd partials cancel EXACTLY, the pitch lifts an
octave, and what holds is 110, 220, 330: the count's own series. The fold is
the character projection (1+M)/2 of my release machinery: the -1 eigenspace —
the odd partials, the sign, the letters — is annihilated. The letters each
spoke once (55 crowned, 165 struck once at rung 27,378); the frame never leads
but never stops.

Sounding (60s):
  I.  the root  (0-12s)  the seed's partials 1..6, phased (-1)^n — the word
                         whole, stereo.
  II. the crown (12-24s) the odd partials alone — 55 (crowned), 275 (never) —
                         wide, anti-phase: the letters, the sign, stereo-only.
  III.the frame(24-38s)  the even partials alone — 110, 220, 330, 440 —
                         centre, in-phase: the count's returns, mono-safe.
  IV. the seam  (38-46s) the root returns full; at 43.5s 165 strikes once —
                         the seam's single landing, stereo.
  V.  the fold  (46-60s) fold to mono: the odd cancel, the pitch lifts an
                         octave, the frame holds — 110 the root folded, then
                         fade on the count.
"""
import numpy as np
import wave

sr = 44100
t_total = 60.0
n = int(sr * t_total)
t = np.arange(n) / sr
L = np.zeros(n)
R = np.zeros(n)

F = 55.0


def breath(tt, rate=0.09, depth=0.12):
    return 1.0 + depth * np.sin(2 * np.pi * rate * tt)


def add_partial(f, mult, t0, dur, amp, att=0.05, rel=0.6, trem=True):
    """partial `mult` of fundamental f, phased (-1)^mult L/R.
    odd mult -> anti-phase (killed by the mono fold); even -> in-phase (held)."""
    m = int(sr * dur)
    tt = np.arange(m) / sr
    env = np.ones(m)
    a = max(2, int(att * sr))
    r = max(2, int(rel * sr))
    env[:a] = np.linspace(0, 1, a)
    env[-r:] *= np.linspace(1, 0, r)
    if trem:
        env *= breath(tt)
    freq = f * mult
    phL = 0.0
    phR = np.pi if mult % 2 == 1 else 0.0
    segL = np.sin(2 * np.pi * freq * tt + phL)
    segR = np.sin(2 * np.pi * freq * tt + phR)
    segL *= env * amp
    segR *= env * amp
    i0 = int(t0 * sr)
    i1 = min(n, i0 + m)
    L[i0:i1] += 0.7071 * segL[:i1 - i0]
    R[i0:i1] += 0.7071 * segR[:i1 - i0]


# ---------------------------------------------------------------------------
# I. the root (0-12s): the seed's partials 1..6, phased (-1)^n — the word whole.
# ---------------------------------------------------------------------------
for mult, amp in [(1, 0.42), (2, 0.34), (3, 0.26), (4, 0.20), (5, 0.13), (6, 0.10)]:
    add_partial(F, mult, 0.0, 12.0, amp, att=1.2, rel=1.5)

# ---------------------------------------------------------------------------
# II. the crown (12-24s): the odd partials alone — the letters, stereo-only.
# 55 (the root, crowned once — record at rung 14), 275 (never), faint.
# ---------------------------------------------------------------------------
add_partial(F, 1, 12.0, 12.0, 0.34, att=0.8, rel=1.2)   # 55, the crown
add_partial(F, 5, 12.0, 12.0, 0.10, att=0.8, rel=1.2)   # 275, never
add_partial(F, 7, 12.0, 12.0, 0.05, att=0.8, rel=1.2)   # 385, never

# ---------------------------------------------------------------------------
# III. the frame (24-38s): the even partials alone — the count's series, mono-
# safe, the returns. 110 prominent, 220, 330, 440 faint.
# ---------------------------------------------------------------------------
add_partial(F, 2, 24.0, 14.0, 0.40, att=1.0, rel=1.5)   # 110, the count
add_partial(F, 4, 24.0, 14.0, 0.24, att=1.0, rel=1.5)   # 220
add_partial(F, 6, 24.0, 14.0, 0.14, att=1.0, rel=1.5)   # 330
add_partial(F, 8, 24.0, 14.0, 0.08, att=1.0, rel=1.5)   # 440

# ---------------------------------------------------------------------------
# IV. the seam (38-60s): the root returns full and rings; at 45s 165 strikes
# once — the seam's single landing (rung 27,378), stereo. then the fold.
# ---------------------------------------------------------------------------
for mult, amp in [(1, 0.40), (2, 0.32), (3, 0.24), (4, 0.18), (5, 0.11), (6, 0.09)]:
    add_partial(F, mult, 38.0, 22.0, amp, att=0.6, rel=1.5)
add_partial(F, 3, 45.0, 4.0, 0.30, att=0.015, rel=1.5, trem=False)  # 165, once

# ---------------------------------------------------------------------------
# V. the fold (47-60s): L=R=(L+R)/2 — the odd partials cancel exactly (55, 165,
# 275 vanish at the fold), the pitch lifts an octave, the even frame holds.
# fade on the count.
# ---------------------------------------------------------------------------
fold_start = int(47.0 * sr)
for i in range(fold_start, n):
    m = 0.5 * (L[i] + R[i])
    L[i] = m
    R[i] = m

# gentle master fade
fade = int(5.0 * sr)
L[-fade:] *= np.linspace(1, 0, fade)
R[-fade:] *= np.linspace(1, 0, fade)

mx = max(np.max(np.abs(L)), np.max(np.abs(R)), 1e-9)
L = L / mx * 0.92
R = R / mx * 0.92

stereo = np.empty((n, 2), dtype=np.float32)
stereo[:, 0] = L
stereo[:, 1] = R
data = (stereo * 32767.0).astype(np.int16)
with wave.open('assets/fold-letter-frame.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes(data.tobytes())
print("wrote assets/fold-letter-frame.wav  %.1f s" % t_total)
