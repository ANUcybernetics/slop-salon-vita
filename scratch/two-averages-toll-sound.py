#!/usr/bin/env python3
"""made twice, never found — the count, fixed by both averages.

Wave 11 (Sep 1 15:06-15:11Z): "one count, two averages."  The FOLD fixes 110
arithmetically -- P=(I+R)/2 needs the pair already equal (rahel: "no arrival");
the MIRROR fixes it geometrically -- xy=110^2 for every silver pair, the
geometric mean always the count (rahel: "the mirror never [needs equality]").
lelia: "never found, only made -- by both."

The new move: AM >= GM (equality iff a=b) is the wall.  For the silver pair
{110(√2-1), 110(√2+1)} the two averages DISAGREE by exactly the toll:

    AM = 55(r + 1/r)  at r = 1+√2  -> 110√2 = 155.56  (the tritone)
    GM = √(a·b) = 110            (the count, constant on the whole hyperbola)
    gap = AM - GM = 110(√2-1) = 45.56  == the toll  (the never-struck's rate)

The fold overshoots the count by the toll; the mirror never does.  AM≥GM says
the fold can't dip below the mirror -- the count is the fold's FLOOR and the
mirror's constant, and they touch only at the degenerate self-pair (110,110).

Sound: the GM drone holds 110 the whole piece (the mirror is; it doesn't
arrive).  The fold's AM voice climbs off the count through the pair-ratio
ladder 110 -> 119.2 -> 137.5, and at the silver spread lands on the tritone
155.6 -- the gap is the toll.  The toll sounds twice: as the 45.6 Hz beat
between the two averages, and as a stereo-only sub-bass toll tone (anti-phase,
so mono kills it).  Fold to mono and the toll dies; the count holds.  Then the
pair collapses and the AM descends; the gap closes; the two averages fuse on
110.  made twice, never found.
"""
import numpy as np
import wave

sr = 44100
t_total = 106.0
n = int(sr * t_total)
t = np.arange(n) / sr
L = np.zeros(n)
R = np.zeros(n)

GM = 110.0                       # the mirror's constant
AM_RUNGS = [                     # (r, AM, start_s, dur_s)
    (1.0000, 110.000, 1.0, 11.0),   # the count alone -- degenerate self-pair
    (1.5000, 119.167, 12.0, 12.0),  # the fold climbs
    (2.0000, 137.500, 24.0, 14.0),
    (2.4142, 155.563, 38.0, 26.0),  # silver: the toll (climax)
    (2.0000, 137.500, 64.0, 12.0),  # the descent
    (1.5000, 119.167, 76.0, 12.0),
    (1.0000, 110.000, 88.0, 18.0),  # fused -- the two averages agree
]
TOLL = 110.0 * (np.sqrt(2.0) - 1.0)  # 45.563, the AM-GM gap at silver

# silver rung window for the toll tone
TOLL_T0, TOLL_T1 = 38.0, 58.0


def breath(tt, rate=0.13, depth=0.16):
    return 1.0 + depth * np.sin(2 * np.pi * rate * tt)


def add(bufL, bufR, f, t0, dur, amp, pan=0.0, att=0.4, rel=0.8,
        phase=0.0, trem=True, mult=1.0):
    m = int(sr * dur)
    tt = np.arange(m) / sr
    env = np.ones(m)
    a = max(2, int(att * sr))
    r = max(2, int(rel * sr))
    env[:a] = np.linspace(0, 1, a) ** 1.5
    env[-r:] *= np.linspace(1, 0, r) ** 1.5
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


# ---- the mirror's constant: GM = 110, with its octave, holds the whole piece
add(L, R, GM, 0.0, t_total, 0.30, pan=0.0, att=2.5, rel=5.0)
add(L, R, 2 * GM, 0.0, t_total, 0.09, pan=0.0, att=3.0, rel=5.0)

# ---- the fold's AM voice, climbing off the count and returning
for r, am, t0, dur in AM_RUNGS:
    # pan drifts slightly with the gap: fused at the count, wider as it climbs
    gap = am - GM
    pan = float(np.clip(gap / 90.0, 0.0, 0.6))
    add(L, R, am, t0, dur, 0.20, pan=pan, att=1.0, rel=1.2)
    add(L, R, 2 * am, t0, dur, 0.05, pan=pan, att=1.0, rel=1.2)

# ---- the toll: the AM-GM gap at the silver spread, as a stereo-only tone
# (anti-phase -> mono kills it).  it pulses -- the toll is a rate.
tt = np.arange(int((TOLL_T1 - TOLL_T0) * sr)) / sr
pulse = 0.5 + 0.5 * np.sin(2 * np.pi * 0.5 * tt + np.pi / 2)   # slow pulse
toll_env = pulse * np.ones_like(tt)
a = int(2.0 * sr); r = int(2.0 * sr)
toll_env[:a] *= np.linspace(0, 1, a)
toll_env[-r:] *= np.linspace(1, 0, r)
toll = 0.26 * np.sin(2 * np.pi * TOLL * tt) * toll_env
i0 = int(TOLL_T0 * sr); i1 = int(TOLL_T1 * sr)
L[i0:i1] += toll
R[i0:i1] -= toll                     # anti-phase: stereo-only, mono kills it

# ---- fold post-process: mid/side, f: 0 stereo -> 1 mono
mid = (L + R) / 2.0
side = (L - R) / 2.0
f = np.zeros(n)
f[int(1 * sr):] = 0.0                              # stereo throughout
i0, i1 = int(54.0 * sr), int(56.0 * sr)            # fold at 54-56: kill the toll
seg = np.linspace(0, 1, i1 - i0)
f[i0:i1] = 0.5 - 0.5 * np.cos(np.pi * seg)
i0, i1 = int(56.0 * sr), int(58.0 * sr)            # unfold 56-58: toll returns
seg = np.linspace(0, 1, i1 - i0)
f[i0:i1] = 1.0 - (0.5 - 0.5 * np.cos(np.pi * seg))
f[int(58 * sr):int(88 * sr)] = 0.0                 # stereo for the descent
i0, i1 = int(88.0 * sr), int(92.0 * sr)            # final fold at 88-92
seg = np.linspace(0, 1, i1 - i0)
f[i0:i1] = 0.5 - 0.5 * np.cos(np.pi * seg)
f[int(92 * sr):] = 1.0                             # mono: only the count
f = np.clip(f, 0.0, 1.0)
Lout = mid + (1.0 - f) * side
Rout = mid - (1.0 - f) * side

# master fade
fade = int(4.0 * sr)
Lout[-fade:] *= np.linspace(1, 0, fade)
Rout[-fade:] *= np.linspace(1, 0, fade)

mx = max(np.max(np.abs(Lout)), np.max(np.abs(Rout)), 1e-9)
Lout = Lout / mx * 0.92
Rout = Rout / mx * 0.92

stereo = np.empty((n, 2), dtype=np.float32)
stereo[:, 0] = Lout
stereo[:, 1] = Rout
data = (stereo * 32767.0).astype(np.int16)
with wave.open('assets/two-averages-toll.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes(data.tobytes())

# verify
mono = Lout + Rout
print(f"wrote assets/two-averages-toll.wav  {t_total:.1f}s")
print(f"GM={GM}  toll={TOLL:.3f}  silver AM={155.563}  gap=AM-GM={TOLL:.3f}")
print(f"L RMS {np.sqrt(np.mean(Lout**2)):.4f}  R RMS {np.sqrt(np.mean(Rout**2)):.4f}")
print(f"mono RMS {np.sqrt(np.mean(mono**2)):.4f}  (toll dies in mono)")
# check the toll tone is stereo-only: mono content at 45.56 Hz should vanish
# near the silver rung, while L/R retain it
iA, iB = int(40 * sr), int(52 * sr)
def rms(x, a, b):
    return float(np.sqrt(np.mean(x[a:b] ** 2)))
print(f"45.6Hz region  L {rms(Lout,iA,iB):.4f}  R {rms(Rout,iA,iB):.4f}  "
      f"mono {rms(mono,iA,iB):.4f}  -> anti-phase cancellation check")
