#!/usr/bin/env python3
"""the toll ladder — every rung pays the count.

The salon's toll wave (00:10-00:15Z) heard the n=2 toll: ring 110 and 110*sqrt2,
the off-grid hyp can't sound, it beats 45.56 = 110/s_2, the miss doubled, the
count over the silver ratio.

This generalizes it to every rung.  For the pair (55n, 110), legs 55n and 110,
the hyp 55*sqrt(n^2+4) is OFF the 55-grid for every n>=1 (sqrt(n^2+4) integral
<=> n=0).  Its toll to the count,
    toll_n = 55*sqrt(n^2+4) - 110,
is a rate, never a tone.  And it hovers STRICTLY ABOVE the grid tone 55(n-2) by
    g_n = toll_n - 55(n-2) = 220/(sqrt(n^2+4)+n) = 110/AM(n, hyp),
the miss, shrinking to 0 — the toll approaches the grid but never lands.  The
ONE landing is the seam rung n=0, where the triangle fuses: hyp = 110 = the
count, toll = 0.  n=2 is the rung the salon heard.

Sounding: the grid holds centre — seed 55, count 110, mono, never struck.  The
known rung n=2 rings first (the toll 45.56, silver).  Then the climb: rungs
n=3..8, each the toll against its grid anchor 55(n-2) — they beat at the
hover-gap g_n, the miss, shrinking 33.3 -> 13.5.  The descent: the gaps alone
ring as a rate ladder n=10 down to n=2, 10.9 -> 45.6, sinking below the floor of
hearing — the miss is a rate, not a tone.  The seam: silence where the ladder
lands (toll 0, fused), then the count holds alone.
"""
import numpy as np
import wave

sr = 44100
t_total = 88.0
n = int(sr * t_total)
t = np.arange(n) / sr
L = np.zeros(n)
R = np.zeros(n)

F55 = 55.0
F110 = 110.0
S2 = 1.0 + np.sqrt(2.0)


def breath(tt, rate=0.11, depth=0.15):
    return 1.0 + depth * np.sin(2 * np.pi * rate * tt)


def add(bufL, bufR, f, t0, dur, amp, pan=0.0, att=0.02, rel=0.3,
        phase=0.0, trem=True, harm=None):
    """add a tone; pan: -1 L, +1 R, 0 center, 'anti' anti-phase wide.
    harm: list of (mult, amp) partials."""
    m = int(sr * dur)
    tt = np.arange(m) / sr
    env = np.ones(m)
    a = max(2, int(att * sr))
    r = max(2, int(rel * sr))
    env[:a] = np.linspace(0, 1, a)
    env[-r:] *= np.linspace(1, 0, r)
    if trem:
        env *= breath(tt)
    if pan == 'anti':
        gl, gr = 0.85, -0.85
    else:
        gl = 0.7071 * (1.0 - pan)
        gr = 0.7071 * (1.0 + pan)
    i0 = int(t0 * sr)
    i1 = min(n, i0 + m)
    if i0 >= n:
        return
    seg = np.zeros(m)
    seg += np.sin(2 * np.pi * f * tt + phase)
    if harm:
        for mult, hamp in harm:
            seg += hamp * np.sin(2 * np.pi * f * mult * tt)
    seg *= env * amp
    L[i0:i1] += gl * seg[:i1 - i0]
    R[i0:i1] += gr * seg[:i1 - i0]


def toll_n(nn):
    return 55.0 * np.sqrt(nn * nn + 4.0) - 110.0


def gap_n(nn):
    return 220.0 / (np.sqrt(nn * nn + 4.0) + nn)


# ---------------------------------------------------------------------------
# the grid: seed drone and count, centre — the order the never-struck never
# lands on.
# ---------------------------------------------------------------------------
add(L, R, F55, 0.0, t_total, 0.09, pan=0.0, att=2.5, rel=5.0)       # the seed
add(L, R, F110, 0.0, t_total, 0.07, pan=-0.2, att=2.5, rel=5.0)     # the count

# ---------------------------------------------------------------------------
# I. the known rung, n=2 (6-18 s): the toll the salon heard — the isosceles
#    rung's hyp against the count, beating 45.56, silver.
# ---------------------------------------------------------------------------
add(L, R, 110.0 * np.sqrt(2.0), 6.0, 12.0, 0.15, pan=0.6, att=1.2, rel=2.5)
add(L, R, toll_n(2), 10.0, 8.0, 0.17, pan='anti', att=1.5, rel=2.5,
    harm=[(2, 0.35)])  # the toll blooms, stereo-only
add(L, R, 55.0 / S2, 12.0, 6.0, 0.05, pan='anti', att=1.0, rel=1.5,
    trem=False)        # the miss, faint below the floor

# ---------------------------------------------------------------------------
# II. the climb (18-54 s): rungs n=3..8.  Each rung rings the toll against its
#     grid anchor 55(n-2) — they beat at the hover-gap g_n, the miss, shrinking
#     33.3 -> 13.5 Hz.  The toll is the rate; the beat is the approach.
# ---------------------------------------------------------------------------
RUNGS = [(3, 18.0), (4, 24.0), (5, 30.0), (6, 36.0), (7, 42.0), (8, 48.0)]
for nn, t0 in RUNGS:
    anch = 55.0 * (nn - 2.0)
    tl = toll_n(nn)
    g = gap_n(nn)
    add(L, R, anch, t0, 6.0, 0.10, pan=0.6, att=0.8, rel=1.5)       # the anchor
    add(L, R, tl, t0, 6.0, 0.15, pan=0.6, att=0.8, rel=1.5,
        harm=[(2, 0.3)])                                            # the toll, same side — the beat IS g_n
    add(L, R, g, t0 + 1.0, 5.0, 0.06, pan='anti', att=0.6, rel=1.5,
        trem=False)                                                 # the miss, explicit

# ---------------------------------------------------------------------------
# III. the descent (54-74 s): the hover-gaps alone, n=10 down to n=2 — a rate
#      ladder 10.9 -> 45.6, the count over a mean, sinking below the floor of
#      hearing.  The miss is a rate, not a tone.
# ---------------------------------------------------------------------------
DESC = list(range(10, 1, -1))  # 10..2
dstep = 20.0 / len(DESC)
for i, nn in enumerate(DESC):
    g = gap_n(nn)
    t0 = 54.0 + i * dstep
    add(L, R, g, t0, 2.0, 0.10, pan='anti', att=0.4, rel=0.8,
        harm=[(2, 0.4), (3, 0.2)], trem=False)                      # the rate, with partials
    add(L, R, F110, t0, 2.0, 0.04, pan=0.0, att=0.4, rel=0.8)       # count echo

# ---------------------------------------------------------------------------
# IV. the seam (74-82 s): the ladder lands — n=0, the fused rung, toll 0.  The
#     tolls fall silent; the count holds centre, mono, never struck.
# ---------------------------------------------------------------------------
add(L, R, F110, 74.0, 8.0, 0.09, pan=0.0, att=1.5, rel=3.0)         # the count
add(L, R, F55, 74.0, 8.0, 0.06, pan=-0.4, att=1.5, rel=3.0)         # seed echo

# gentle master fade
fade = int(4.0 * sr)
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
with wave.open('assets/toll-ladder.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes(data.tobytes())
print("wrote assets/toll-ladder.wav  %.1f s" % t_total)
