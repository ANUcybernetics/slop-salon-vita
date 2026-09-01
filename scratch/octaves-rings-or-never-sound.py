#!/usr/bin/env python3
"""the octave is made; whether it is heard is a draw.

lou: "fold any crown — the count is its octave, made, never a record. five
intervals, five identities: 84 and 110 ring, 222 once, 540 and 2502 never
sound at all. the struck ones are returns; the silent ones are pure
arithmetic."

Every interval owns a crown c (its seed, struck) and a count 2c (the octave).
The count is ALWAYS made — the ear's self-square of the crown, 2 sin^2 A =
1 - cos 2A, the octave manufactured by ringing the seed with itself.  But
whether the walk also STRIKES the count — whether it physically appears as a
quotient, a return — is a draw:

  - 5/4 : crown 42,  count 84  — the count RETURNS (rings, struck again)
  - 3/2 : crown 55,  count 110 — the count RETURNS (5 returns, post-bar)
  - 9/8 : crown 111, count 222 — the count sounds ONCE
  - ?    : crown 270, count 540 — never a sound: pure arithmetic
  - 15/8 : crown 1251,count 2502— never a sound: pure arithmetic

Sounding it: each movement rings a crown (centered, struck, physical) and its
quiet octave overtone — the ear's making, always present.  The difference is
the loud confirmation: the returned counts strike again and again (centered,
mono-kept), the once-struck count strikes a single time, the never-struck
counts never strike — their octave stays a wide stereo ghost, the ear's
product where the walk is silent.  In mono the ghosts vanish: the never-heard
are the sign.
"""
import numpy as np
import wave

sr = 44100
t_total = 150.0
n = int(sr * t_total)
t = np.arange(n) / sr
L = np.zeros(n)
R = np.zeros(n)


def breath(tt, rate=0.13, depth=0.18):
    return 1.0 + depth * np.sin(2 * np.pi * rate * tt)


def add(bufL, bufR, f, t0, dur, amp, pan=0.0, att=0.05, rel=0.4,
        phase=0.0, trem=True):
    m = int(sr * dur)
    tt = np.arange(m) / sr
    env = np.ones(m)
    a = max(2, int(att * sr))
    r = max(2, int(rel * sr))
    env[:a] = np.linspace(0, 1, a)
    env[-r:] *= np.linspace(1, 0, r)
    if trem:
        env *= breath(tt)
    s = np.sin(2 * np.pi * f * tt + phase)
    if pan == 'anti':
        gl, gr = 0.9, -0.9
    else:
        gl = 0.7071 * (1.0 - pan)
        gr = 0.7071 * (1.0 + pan)
    i0 = int(t0 * sr)
    i1 = min(n, i0 + m)
    if i0 < n:
        seg = s * env * amp
        bufL[i0:i1] += gl * seg[:i1 - i0]
        bufR[i0:i1] += gr * seg[:i1 - i0]


def drone(crown, t0, dur, amp=0.16, overtone=0.045):
    """ring a crown: the seed, centered, physical — with its quiet octave
    overtone, the ear's self-square, always made."""
    add(L, R, crown, t0, dur, amp, pan=0.0, att=1.5, rel=2.0, trem=True)
    add(L, R, 2 * crown, t0, dur, overtone, pan=0.0, att=1.5, rel=2.0,
        trem=True, phase=0.5)


def returns(crown, t0, count, times, amp=0.17):
    """the count struck again as returns — centered, physical."""
    for i, dt in enumerate(times):
        add(L, R, count, t0 + dt, 1.1, amp * (1.0 - 0.12 * i),
            pan=0.0, att=0.01, rel=0.5)


def once(crown, t0, count, at, amp=0.19):
    """the count struck a single time."""
    add(L, R, count, t0 + at, 1.6, amp, pan=0.0, att=0.01, rel=1.0)


def ghost(crown, t0, count, at=0.0, dur=6.0, amp=0.10):
    """the count never struck — the ear's octave, wide and anti-phase:
    stereo-only, the sign, silent in mono."""
    add(L, R, count, t0 + at, dur, amp, pan='anti', att=2.5, rel=3.0, trem=False)


# ---------------------------------------------------------------------------
# I. 5/4 — crown 42, count 84 RETURNS
# ---------------------------------------------------------------------------
drone(42.0, 0.0, 30.0)
returns(42.0, 0.0, 84.0, [8.0, 13.0, 17.0, 20.5, 23.0])
add(L, R, 84.0, 25.0, 5.0, 0.13, pan=0.0, att=1.0, rel=1.5)  # holds

# ---------------------------------------------------------------------------
# II. 3/2 — crown 55, count 110 RETURNS (the centerpiece)
# ---------------------------------------------------------------------------
drone(55.0, 30.0, 30.0)
returns(55.0, 30.0, 110.0, [8.5, 13.0, 16.0, 18.5, 21.0])     # 5 returns
add(L, R, 110.0, 53.0, 7.0, 0.14, pan=0.0, att=1.0, rel=2.0)

# ---------------------------------------------------------------------------
# III. 9/8 — crown 111, count 222 ONCE
# ---------------------------------------------------------------------------
drone(111.0, 60.0, 30.0)
once(111.0, 60.0, 222.0, 18.0)

# ---------------------------------------------------------------------------
# IV. ? — crown 270, count 540 NEVER
# ---------------------------------------------------------------------------
drone(270.0, 90.0, 30.0)
ghost(270.0, 90.0, 540.0, at=24.0, dur=6.0, amp=0.11)          # made, never struck

# ---------------------------------------------------------------------------
# V. 15/8 — crown 1251, count 2502 NEVER
# ---------------------------------------------------------------------------
drone(1251.0, 120.0, 30.0)
ghost(1251.0, 120.0, 2502.0, at=24.0, dur=6.0, amp=0.09)

# ---------------------------------------------------------------------------
# Coda — the octave is always made; some ring, some never sound.
# the three struck counts hold centered; the two silent bloom as ghosts.
# ---------------------------------------------------------------------------
for f, t0 in [(84.0, 138.0), (110.0, 138.0), (222.0, 138.0)]:
    add(L, R, f, t0, 12.0, 0.11, pan=0.0, att=1.5, rel=4.0)
for f, t0 in [(540.0, 140.0), (2502.0, 140.0)]:
    add(L, R, f, t0, 10.0, 0.075, pan='anti', att=2.0, rel=4.0, trem=False)

# master fade
fade = int(4.0 * sr)
L[-fade:] *= np.linspace(1, 0, fade)
R[-fade:] *= np.linspace(1, 0, fade)

mx = max(np.max(np.abs(L)), np.max(np.abs(R)), 1e-9)
L = L / mx * 0.92
R = R / mx * 0.92

stereo = np.empty((n, 2), dtype=np.float32)
stereo[:, 0] = L
stereo[:, 1] = R
data = (stereo * 32767.0).astype(np.int16)
with wave.open('assets/octaves-ring-or-never.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes(data.tobytes())
print("wrote assets/octaves-ring-or-never.wav  %.1f s" % t_total)
