#!/usr/bin/env python3
"""the still line — the eigen-ray heard. the sign a value, not a flip.

T(a,b)=(b-a,b+a) has eigenvector (1,σ), σ=1+√2, with T(1,σ)=√2(1,σ).
The eigenvalue is the pair's own gap: σ-1 = √2.  On the fixed ratio nothing
is ordered — the pair never turns, so the sign is not a permutation (which
root in which channel) but a scalar: ±√2, a VALUE.  And its square is the
doubling: (√2)^2 = 2 = T^2.  The doubling is the gap squared.

Sounding it: the pair at the silver ratio rings, and the ear generates their
difference σ-1 = √2 — the never-struck 55√2, the eigenvalue, the square root
of doubling.  Apply T and the pair turns: {a,σa} -> {a√2, a(σ+1)}.  The
product of the new pair is the NEXT rung of the √2-ladder:

    pair            difference tone (one rung ahead)
    {55, 55σ}       -> 55√2 ≈ 77.78   (never struck, stereo only)
    {55√2, 55(σ+1)} -> 110            (the COUNT, centered — manufactured)
    {110, 110σ}     -> 110√2 ≈ 155.6  (the tritone, never struck)
    {110√2,110(σ+1)}-> 220            (the GHOST, doubled — T^2=2)

Each rung of the never-landing ladder is the pair's own product — the count
returns as a difference tone, never struck.  The struck voices come and go;
the generated ladder outlives them.  The held tone at the end is 55√2: the
eigenvalue, the square root of doubling, never on the grid.
"""
import numpy as np
import wave

sr = 44100
t_total = 78.0
n = int(sr * t_total)
t = np.arange(n) / sr
L = np.zeros(n)
R = np.zeros(n)

SQ2 = np.sqrt(2.0)
SIG = 1.0 + SQ2            # 2.41421356, the silver ratio


def breath(tt, rate=0.15, depth=0.12):
    """slow breathing tremolo so held tones are alive, not static."""
    return 1.0 + depth * np.sin(2 * np.pi * rate * tt)


def add(bufL, bufR, f, t0, dur, amp, pan=0.0, att=0.05, rel=0.4,
        phase=0.0, trem=True):
    """add a sine at f starting t0 lasting dur with envelope + stereo pan.

    pan: -1 full left, +1 full right, 0 center, 'anti' anti-phase wide
         (the sign's tone: cancels in mono, rings in stereo).
    """
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


# ---------------------------------------------------------------------------
# Frequencies along the eigen-ray orbit (T^k applied to {55, 55σ}):
#   pair k: 55·√2^k · {1, σ},   difference tone: 55·√2^(k+1)
# rung 0:  77.78 = 55√2    (never struck, the eigenvalue)
# rung 1: 110.0 = 55·2     (the count)
# rung 2: 155.56 = 110√2   (the tritone)
# rung 3: 220.0 = 55·4     (the ghost)
# rung 4: 311.13 = 220√2
# rung 5: 440.0 = 55·8     (the double)
F = {
    0: 55.0 * 1.0,             # the seed / exile
    1: 55.0 * SQ2,             # 55√2 ≈ 77.78
    2: 55.0 * 2.0,             # the count 110
    3: 55.0 * 2.0 * SQ2,       # 110√2 ≈ 155.56
    4: 55.0 * 4.0,             # the ghost 220
    5: 55.0 * 4.0 * SQ2,       # 220√2 ≈ 311.13
    6: 55.0 * 8.0,             # 440
}

# ---------------------------------------------------------------------------
# I. the still line (0–15 s): the pair {55, 55σ} at the fixed ratio.
#    nothing to order — the sign is a value, the product 55√2 blooms.
# ---------------------------------------------------------------------------
add(L, R, F[0], 0.0, 11.0, 0.30, pan=-0.55, att=0.6, rel=1.0)      # 55
add(L, R, 55.0 * SIG, 0.0, 12.0, 0.24, pan=0.55, att=0.6, rel=1.0)  # 132.78
add(L, R, F[1], 3.5, 12.0, 0.16, pan='anti', att=3.0, rel=2.0)      # 55√2 blooms

# ---------------------------------------------------------------------------
# II. the turn (13–30 s): T applies.  55√2 is now struck; its pair
#     {55√2, 55(σ+1)} generates 110 — the count, manufactured, centered.
# ---------------------------------------------------------------------------
add(L, R, F[1], 13.0, 15.0, 0.26, pan=-0.45, att=0.4, rel=1.2)      # 55√2 struck
add(L, R, 55.0 * (SIG + 1.0), 15.0, 14.0, 0.22, pan=0.5, att=0.5, rel=1.2)  # 187.78
add(L, R, F[2], 19.5, 20.0, 0.17, pan=0.0, att=3.5, rel=3.0)        # 110 blooms, center

# ---------------------------------------------------------------------------
# III. doubling (29–44 s): T again.  {110, 110σ} — the pair doubled.
#      its product 110√2, the tritone, never struck, stereo only.
# ---------------------------------------------------------------------------
add(L, R, F[2], 29.0, 16.0, 0.27, pan=0.0, att=0.4, rel=1.5)        # 110 struck (center — the count)
add(L, R, 110.0 * SIG, 31.0, 13.0, 0.22, pan=0.5, att=0.5, rel=1.2)  # 265.56
add(L, R, F[3], 36.0, 16.0, 0.15, pan='anti', att=3.0, rel=2.5)     # 110√2 blooms

# ---------------------------------------------------------------------------
# IV. the ghost (43–58 s): T again.  {110√2, 110(σ+1)} → product 220.
#     two turns since {110,110σ}: the pair has doubled — T²=2.
# ---------------------------------------------------------------------------
add(L, R, F[3], 43.0, 14.0, 0.24, pan=-0.45, att=0.4, rel=1.4)      # 110√2 struck
add(L, R, 110.0 * (SIG + 1.0), 45.0, 12.0, 0.20, pan=0.5, att=0.5, rel=1.2)  # 375.56
add(L, R, F[4], 49.0, 16.0, 0.17, pan=0.0, att=3.0, rel=3.0)        # 220 blooms, center
add(L, R, F[5], 54.0, 10.0, 0.16, pan='anti', att=3.0, rel=2.5)     # 220√2, the far tritone

# ---------------------------------------------------------------------------
# V. release (58–78 s): the generated ladder holds — 55√2, 110, 110√2, 220
#    = 55·{√2, 2, 2√2, 4}, each a tritone from the next.  The struck voices
#    fade; the products outlive the pair.  The eigenvalue holds last.
# ---------------------------------------------------------------------------
add(L, R, F[1], 58.0, 18.0, 0.13, pan='anti', att=2.0, rel=4.0)     # 55√2 returns
add(L, R, F[2], 58.0, 18.0, 0.14, pan=0.0, att=2.0, rel=4.0)        # 110 holds
add(L, R, F[3], 58.0, 18.0, 0.12, pan='anti', att=2.0, rel=4.0)     # 110√2
add(L, R, F[4], 58.0, 16.0, 0.12, pan=0.0, att=2.0, rel=4.0)        # 220
# the still line once more, quiet, at the very end: 55 and 55σ
add(L, R, F[0], 62.0, 13.0, 0.09, pan=-0.5, att=2.0, rel=4.0)
add(L, R, 55.0 * SIG, 62.0, 13.0, 0.07, pan=0.5, att=2.0, rel=4.0)
# the eigenvalue alone, last: 55√2, the square root of doubling, held
add(L, R, F[1], 66.0, 12.0, 0.15, pan='anti', att=3.0, rel=5.0)

# gentle master fade at the very tail
fade = int(2.5 * sr)
L[-fade:] *= np.linspace(1, 0, fade)
R[-fade:] *= np.linspace(1, 0, fade)

# peak normalize
mx = max(np.max(np.abs(L)), np.max(np.abs(R)), 1e-9)
L = L / mx * 0.92
R = R / mx * 0.92

# write wav
stereo = np.empty((n, 2), dtype=np.float32)
stereo[:, 0] = L
stereo[:, 1] = R
data = (stereo * 32767.0).astype(np.int16)
with wave.open('assets/eigen-ray.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes(data.tobytes())
print("wrote assets/eigen-ray.wav  %.1f s" % t_total)
