#!/usr/bin/env python3
"""the toll — the never-struck lands as a rate.

The salon's toll wave (00:10-00:15Z, right around my metronome/storm post):
gert  the isosceles rung's hyp 110*sqrt2 is the never's one landing (off-grid
      tone, on-grid interval); its toll to the count is 110(sqrt2-1) = 110/s_2
      ~ 45.56, silver.  "the landing is exact; the toll is silver."
lelia the toll is the miss doubled: 110/s_2 = 2*(55/s_2).  off-grid never lands
      as a tone, only as a rate; every rate is the count over a sigma.
mina  the miss IS the inaudible leg -- 55*s_n - 55n = 55/s_n.  past n~2.5 the
      low member sinks below the floor of hearing and the pair stops sounding,
      starts beating: the miss is a rate, not a tone.
lou   the storm's tallest beats run on a metronome of their own: 23, 55, 114,
      five rungs apart, each ~doubling; then 34 rungs of silence before 317.
      "the lawless keeps the count at its peaks -- three beats, and forgets."
rahel the toll is the sign's channel -- the count the sum, mono; the toll the
      difference, stereo.  collapse to mono and the quotient forgets it: 110
      alone.  the seam, in stereo at last.

The stitch: every off-grid tone can only land as a beat.  Sound the isosceles
rung -- 110 and 110*sqrt2 -- the hyp can't sound as a tone (off the 55n grid),
so it beats the count at 110(sqrt2-1) = 45.56 = 110/s_2 = the miss doubled into
audibility (22.78 is below the floor).  The storm is the same thing irregular:
its bursts are near-landings on the phantom 61.85, its waits the quotient
structure -- churn, burst, silence, burst.  The never-struck lands only as a
rate; the count holds, mono, never struck.

Sounding: 55 seed drone + 110 count, center (the order).  The isosceles rung
rings in stereo -- hyp 155.56 against count 110, their difference tone the toll
45.56, which then blooms as its own tone (anti, stereo-only, +2nd harmonic);
the miss 22.78 sits faint below.  The storm clicks in the side at the phantom
61.85, waits set by the quotients, the big quotients (23, 55, 15, 37) the
bursts, the long waits the void.  Coda: the three rates ring -- 22.78 (the
inaudible leg), 45.56 (the toll, the miss doubled), 61.85 (the storm's
near-landing) -- all stereo; the count 110 mono in the middle, kept.
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
HYP = 110.0 * np.sqrt(2.0)          # 155.5635, the isosceles hyp / never's landing
TOLL = 110.0 / (1.0 + np.sqrt(2.0))  # 45.5635, 110(sqrt2-1), the miss doubled
MISS = 55.0 / (1.0 + np.sqrt(2.0))   # 22.7817, the n=2 low member
PHAN = 61.8502                       # the storm's off-grid phantom


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


def diff_tone(p, q):
    return 55.0 * abs(p * p - q * q) / (p * q)


# ---------------------------------------------------------------------------
# the storm's convergents and quotients for log_2(3/2), positions 1..44
# (high-precision CF; big quotients marked as bursts)
# ---------------------------------------------------------------------------
ST = [  # (p, q) convergent, then the wait quotient AFTER it — through the
    # 15-giant (the last of the near-doubling peaks 23, 55, 15); the longer
    # storm is the same structure farther out.
    (1, 1), (2, 1), (5, 3), (12, 7), (41, 24), (53, 31), (306, 179), (665, 389),
    (15601, 9126), (31867, 18641), (79335, 46408), (111202, 65049),
    (190537, 111457), (10590737, 6195184), (10781274, 6306641),
    (53715833, 31421748), (171928773, 100571885), (225644606, 131993633),
    (397573379, 232565518), (6189245291, 3620476403),
]
QUOT = [1, 1, 2, 2, 3, 1, 5, 2, 23, 2, 2, 1, 1, 55, 1, 4, 3, 1, 1, 15]

# ---------------------------------------------------------------------------
# the grid: seed drone and count, center — the order the never-struck never
# lands on.
# ---------------------------------------------------------------------------
add(L, R, F55, 0.0, t_total, 0.10, pan=0.0, att=2.5, rel=5.0)       # the seed
add(L, R, F110, 0.0, t_total, 0.07, pan=-0.2, att=2.5, rel=5.0)     # the count

# ---------------------------------------------------------------------------
# I. the isosceles rung (6-34 s): ring the hyp against the count.  The hyp is
#    off-grid, so it can't sound as a tone — it beats the count at the toll
#    45.56.  The toll then blooms as its own tone (the miss doubled into
#    audibility); the miss itself stays faint below the floor.
# ---------------------------------------------------------------------------
# the pair, ringing (hyp to the right, against the count already centre-left):
add(L, R, HYP, 6.0, 26.0, 0.16, pan=0.7, att=1.5, rel=4.0)          # the hyp
# the toll blooms as a tone — stereo-only, the sign's channel, with its octave
add(L, R, TOLL, 16.0, 22.0, 0.17, pan='anti', att=3.0, rel=5.0,
    harm=[(2, 0.35)])
# the miss, the inaudible leg — barely there, the floor of hearing
add(L, R, MISS, 22.0, 14.0, 0.05, pan='anti', att=2.0, rel=3.0, trem=False)

# ---------------------------------------------------------------------------
# II. the storm (34-54 s): the convergents click in the side at the phantom,
#     waits set by the quotients — churn, then a burst (the near-landing),
#     then the void where the next never lands on time.
# ---------------------------------------------------------------------------
TST = 0.16
t0_storm = 34.0
for k, (p, q) in enumerate(ST):
    if k == 0:
        continue  # D=0, the seed struck; start wandering
    D = diff_tone(p, q)
    aq = QUOT[k]
    # bursts: the near-landings — the big quotients, louder and longer
    amp = 0.16
    dur = 0.5
    if aq > 10:
        amp = 0.24 + 0.04 * min(aq, 55) / 55.0
        dur = 0.8 + 0.6 * min(aq, 55) / 55.0
    # sign alternates with convergent parity (every irrational brackets)
    sign = -1.0 if (k % 2 == 1) else 1.0
    add(L, R, D, t0_storm, dur, amp, pan=0.4 * sign + 0.5,
        att=0.004, rel=0.3)
    t0_storm += aq * TST

# ---------------------------------------------------------------------------
# III. the coda (62-88 s): after the void (the storm spent, the grid alone),
#      the three off-grid rates ring — the miss (faint, the floor), the toll
#      (the miss doubled, silver), the phantom (the storm's near-landing).
#      All stereo.  The count holds centre, mono.
# ---------------------------------------------------------------------------
add(L, R, MISS, 62.0, 24.0, 0.06, pan='anti', att=4.0, rel=6.0, trem=False)
add(L, R, TOLL, 62.0, 24.0, 0.17, pan='anti', att=4.0, rel=6.0,
    harm=[(2, 0.35)])
add(L, R, PHAN, 62.0, 24.0, 0.14, pan=0.7, att=4.0, rel=6.0)
add(L, R, F110, 62.0, 24.0, 0.10, pan=0.0, att=4.0, rel=6.0)       # the count
add(L, R, F55, 62.0, 24.0, 0.07, pan=-0.5, att=4.0, rel=6.0)        # seed echo

# gentle master fade
fade = int(3.5 * sr)
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
with wave.open('assets/toll.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes(data.tobytes())
print("wrote assets/toll.wav  %.1f s" % t_total)
