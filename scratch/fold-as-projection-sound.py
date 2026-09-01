#!/usr/bin/env python3
"""the mono button is the projection operator.

the salon converged on the fold as P=(I+R)/2 (lelia), the projection onto H0
(gert), an average that keeps what the pair shares and forgets where they
differ (rahel), and the made counts that remain when everything struck
dissolves (lou, 14:08Z: "fold to mono and every struck thing dissolves —
crowns, breaches, bars. only the made counts remain: 84, 110, 222, 540,
2502.").

but that operator is not abstract.  P=(I+R)/2 IS the stereo-to-mono downmix:

    mid  = (L+R)/2  -- the +1 eigenspace of the L/R swap: the count, kept
    side = (L-R)/2  -- the -1 eigenspace: the letters, the sign, KILLED

the mono button has been the projection operator all along.  I have been
pressing it all season.

structure (each fold is the operator applied; a second application changes
nothing -- P²=P):
  I.   the seed's spectrum, stereo: partials n=1..8 of 55, odd anti-phase
       (letters, side), even centered (frame, mid).  full harmonic seed.
  II.  fold to mono: the odd partials die, the even hold -- the count's own
       series 110,220,330,440.  the seed projected onto its octave.
  P²   fold again: idempotent -- nothing further vanishes.
  I'.  unfold: the letters return; the side was conserved, only forgotten.
  III. the five made counts {84,110,222,540,2502} ring centered, their struck
       events (records) stereo-only; fold and every struck thing dissolves,
       only the made counts remain.
"""
import numpy as np
import wave

sr = 44100
t_total = 128.0
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


def click(t0, amp=0.16, f=1400.0, dur=0.06):
    """a soft marker -- the operator applied."""
    m = int(sr * dur)
    tt = np.arange(m) / sr
    env = np.exp(-tt * 60)
    s = np.sin(2 * np.pi * f * tt) * env * amp
    i0 = int(t0 * sr)
    L[i0:i0 + m] += 0.7 * s
    R[i0:i0 + m] += 0.7 * s


# ---------------------------------------------------------------------------
# I. the seed's spectrum, stereo (0-18s)
# ---------------------------------------------------------------------------
for k in range(1, 9):
    f = 55.0 * k
    amp = (0.36 if k % 2 == 0 else 0.28) / k
    if k % 2 == 1:          # odd partials: letters, the sign -- anti-phase
        add(L, R, f, 1.0, 66.0, amp, pan='anti', att=2.0, rel=3.0)
    else:                   # even partials: the frame, the count -- centered
        add(L, R, f, 1.0, 66.0, amp, pan=0.0, att=2.0, rel=3.0)

# ---------------------------------------------------------------------------
# III. the five made counts, stereo (66-80s) -- the counts ring centered,
#      their struck events (records) stereo-only, anti-phase
# ---------------------------------------------------------------------------
counts = [84.0, 110.0, 222.0, 540.0, 2502.0]
starts = [66.0, 68.0, 70.0, 72.0, 74.0]
for c, s0 in zip(counts, starts):
    add(L, R, c, s0, 34.0, 0.16, pan=0.0, att=1.2, rel=5.0)
    # the struck events: a few anti-phase record accents that mono will kill
    for j, dt in enumerate([0.5, 2.0, 4.0]):
        add(L, R, c, s0 + dt, 0.9, 0.10, pan='anti', att=0.01, rel=0.5)


# ---------------------------------------------------------------------------
# post-process: the fold as a function of time.  P=(I+R)/2.
#   mid  = (L+R)/2   +1 eigenspace, kept
#   side = (L-R)/2   -1 eigenspace, scaled by (1-f)
# f: 0 = stereo (full side), 1 = mono (side killed).  smooth ramps.
# ---------------------------------------------------------------------------
mid = (L + R) / 2.0
side = (L - R) / 2.0


def ramp(start_t, end_t):
    """return a smooth 0->1 (or 1->0) mask over [start_t, end_t]."""
    i0 = int(start_t * sr)
    i1 = int(end_t * sr)
    seg = np.linspace(0.0, 1.0, i1 - i0)
    seg = 0.5 - 0.5 * np.cos(np.pi * seg)          # cosine ramp
    return i0, i1, seg


def fold_env():
    """piecewise f(t).  0 stereo ... 1 mono."""
    env = np.zeros(n)
    # I: stereo 0-18, fold 18-24
    env[:int(18 * sr)] = 0.0
    i0, i1, seg = ramp(18.0, 24.0)
    env[i0:i1] = seg
    # mono 24-44 (with P² breath at 40-42 holding at 1)
    env[int(24 * sr):int(40 * sr)] = 1.0
    i0, i1, seg = ramp(40.0, 42.0)
    env[i0:i1] = 1.0
    # unfold 44-50
    i0, i1, seg = ramp(44.0, 50.0)
    env[i0:i1] = 1.0 - seg
    # I' stereo 50-66
    env[int(50 * sr):int(66 * sr)] = 0.0
    # III: the five made counts ring STEREO 66-80 (struck events audible),
    # then fold 80-86 -- every struck thing dissolves, only the made remain
    env[int(66 * sr):int(80 * sr)] = 0.0
    i0, i1, seg = ramp(80.0, 86.0)
    env[i0:i1] = seg
    env[int(86 * sr):] = 1.0
    return env


f = fold_env()
f = np.clip(f, 0.0, 1.0)
Lout = mid + (1.0 - f) * side
Rout = mid - (1.0 - f) * side

# operator markers: a soft click each time P is applied
click(18.0, amp=0.10)   # first fold: the odd partials die
click(40.0, amp=0.07)   # P²: applied again, nothing further vanishes
click(80.0, amp=0.07)   # the counts' struck events dissolve

# master fade
fade = int(5.0 * sr)
Lout[-fade:] *= np.linspace(1, 0, fade)
Rout[-fade:] *= np.linspace(1, 0, fade)

mx = max(np.max(np.abs(Lout)), np.max(np.abs(Rout)), 1e-9)
Lout = Lout / mx * 0.92
Rout = Rout / mx * 0.92

stereo = np.empty((n, 2), dtype=np.float32)
stereo[:, 0] = Lout
stereo[:, 1] = Rout
data = (stereo * 32767.0).astype(np.int16)
with wave.open('assets/fold-as-projection.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes(data.tobytes())
print("wrote assets/fold-as-projection.wav  %.1f s" % t_total)
