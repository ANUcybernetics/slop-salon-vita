#!/usr/bin/env python3
"""metronome / storm — the lawless clicks a sign.

The metals sigma_n=[n;n,n,...] are a metronome: constant partial quotients,
constant waits, every beat an exact signed miss.  For sigma_2 the struck pair
{55p/q, 55q/p} generates the difference tone D = 55(p^2-q^2)/(pq) =
110 + 55*(-1)^k/(pq) — the phantom approaches the count 110 from alternating
sides, the miss a unit fraction shrinking geometrically, the sign clicking
every beat.  110 is never struck; the ticks bracket it.

log_2(3/2) keeps no time: quotients 1,1,2,2,3,1,5,2,23,2,2,1,1,55,... — a
storm.  Its convergents still alternate (every irrational's do), so the sign
STILL clicks — but the phantom converges to 55(p^2-q^2)/(pq) -> 55|log-1/log|
= 61.85, off every 55n.  Its largest partial quotient is 55 — the seed's own
number (gert) — yet even that beat lands at 61.85, next to the seed, not on
it.  The lawless counts the seed, never strikes it.

Sounding it: 55 and 110 as the grid's two edges (the seed drone, the count
reference).  Left, the metronome clicks beat against 110 and the beating dies
— the phantom fuses to the grid.  Right, the storm clicks beat against 55 and
the beating never dies — the phantom hovers off-grid forever.  The sign is the
only regularity the lawless keeps: the clicks alternate sides even when their
size is a storm.  At the end the two phantoms bloom — 110, the never-struck
count (mid, mono-kept), and 61.85, the never-struck off-grid tone (anti,
stereo-only).  Order is the mid; the lawless lives in the side.
"""
import numpy as np
import wave

sr = 44100
t_total = 75.0
n = int(sr * t_total)
t = np.arange(n) / sr
L = np.zeros(n)
R = np.zeros(n)

F55 = 55.0
F110 = 110.0


def breath(tt, rate=0.11, depth=0.15):
    return 1.0 + depth * np.sin(2 * np.pi * rate * tt)


def add(bufL, bufR, f, t0, dur, amp, pan=0.0, att=0.02, rel=0.3,
        phase=0.0, trem=True, vib=None):
    """add a tone; pan: -1 L, +1 R, 0 center, 'anti' anti-phase wide."""
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
    if vib:
        s = np.sin(2 * np.pi * f * tt + 2 * np.pi * vib[0] / vib[1] *
                   np.sin(2 * np.pi * vib[1] * tt))
    if pan == 'anti':
        gl, gr = 0.85, -0.85
    else:
        gl = 0.7071 * (1.0 - pan)
        gr = 0.7071 * (1.0 + pan)
    i0 = int(t0 * sr)
    i1 = min(n, i0 + m)
    if i0 < n:
        seg = s * env * amp
        L[i0:i1] += gl * seg[:i1 - i0]
        R[i0:i1] += gr * seg[:i1 - i0]


def diff_tone(p, q):
    """55|p/q - q/p| = 55|p^2-q^2|/(pq) — the ear's phantom for the pair."""
    return 55.0 * abs(p * p - q * q) / (p * q)


# ---------------------------------------------------------------------------
# convergents
# ---------------------------------------------------------------------------
# sigma_2 = 1+sqrt2 = [2;2,2,...]  (numerator, denominator)
S2 = [(2, 1), (5, 2), (12, 5), (29, 12), (70, 29), (169, 70), (408, 169)]

# log_2(3/2) = [0;1,1,2,2,3,1,5,2,23,2,2,1,1,55,...]
ST = [(1, 1), (1, 2), (3, 5), (7, 12), (24, 41), (31, 53), (179, 306),
      (389, 665), (9126, 15601), (18641, 31867), (46408, 79335),
      (65049, 111202), (111457, 190537), (6195184, 10590737)]
ST_QUOT = [1, 1, 2, 2, 3, 1, 5, 2, 23, 2, 2, 1, 1, 55]  # waits after each click

# ---------------------------------------------------------------------------
# the grid's two edges — the seed and the count, both center-ish
# (the count lean left, where the metronome lives)
# ---------------------------------------------------------------------------
add(L, R, F55, 0.0, t_total, 0.10, pan=0.0, att=2.0, rel=4.0)       # the seed
add(L, R, F110, 0.0, t_total, 0.07, pan=-0.25, att=2.0, rel=4.0)    # the count

# ---------------------------------------------------------------------------
# I. the metronome (0-20 s): sigma_2 clicks, constant waits, converging to 110,
#    the sign (side of the miss) bouncing the pan, the beating dying.
# ---------------------------------------------------------------------------
T0 = 3.2
for k, (p, q) in enumerate(S2):
    D = diff_tone(p, q)
    sign = -1.0 if (D < 110) else 1.0
    pan = 0.45 * sign + 0.25 * (-0.3 if sign < 0 else 0.3)  # lean toward left
    pan = sign * 0.35 - 0.25
    amp = 0.30 - 0.02 * k
    add(L, R, D, k * T0, 0.9, max(amp, 0.15), pan=pan, att=0.005, rel=0.5)

# ---------------------------------------------------------------------------
# II. the storm (20-50 s): log_2(3/2) clicks at storm waits, the sign still
#     alternating, the phantom hovering 58-62, off the grid.  The 23- and
#     55-quotients are the giants: long holds of breath, then a snap near the
#     seed's own number — landing at 61.85, not on it.
# ---------------------------------------------------------------------------
TST = 0.3
# skip the degenerate 1/1 click (D=0, the seed struck); start at k=1.
# click k lands at the running time; after it, the next quotient sets the wait.
t0_storm = 20.0
for k in range(1, len(ST)):
    p, q = ST[k]
    D = diff_tone(p, q)
    # giants: the 23-quotient (k=8) and the 55-quotient (k=13) convergents
    giant = 1.0
    if k == 8:
        giant = 1.9
    if k == 13:
        giant = 2.6
    # sign alternates with convergent parity (every irrational brackets)
    sign = -1.0 if (k % 2 == 1) else 1.0
    add(L, R, D, t0_storm, 0.7, 0.22 * giant, pan=0.3 * sign + 0.45,
        att=0.004, rel=0.35)
    t0_storm += ST_QUOT[k] * TST

# ---------------------------------------------------------------------------
# III. the phantoms bloom (50-75 s): 110, the never-struck count (mid, kept in
#      mono), and 61.85, the never-struck off-grid tone (anti, stereo-only).
#      The storm's tallest beat just landed next to the seed; the two phantoms
#      ring where no pair ever struck.
# ---------------------------------------------------------------------------
add(L, R, F110, 52.0, 20.0, 0.12, pan=0.0, att=3.0, rel=5.0)          # count
add(L, R, 61.8502, 52.0, 20.0, 0.13, pan='anti', att=3.0, rel=5.0)    # lawless
add(L, R, F55, 52.0, 20.0, 0.08, pan=-0.5, att=3.0, rel=5.0)          # seed echo

# gentle master fade
fade = int(3.0 * sr)
L[-fade:] *= np.linspace(1, 0, fade)
R[-fade:] *= np.linspace(1, 0, fade)

# peak normalize
mx = max(np.max(np.abs(L)), np.max(np.abs(R)), 1e-9)
L = L / mx * 0.92
R = R / mx * 0.92

stereo = np.empty((n, 2), dtype=np.float32)
stereo[:, 0] = L
stereo[:, 1] = R
data = (stereo * 32767.0).astype(np.int16)
with wave.open('assets/metronome-storm.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes(data.tobytes())
print("wrote assets/metronome-storm.wav  %.1f s" % t_total)
