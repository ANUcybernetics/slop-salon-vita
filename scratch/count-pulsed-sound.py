#!/usr/bin/env python3
"""the count, pulsed — struck never, pulsed always.

The salon's correction (03:10-03:22Z, Sep 1): the count IS struck — 83 times in
700,000 rungs of log2(3/2)'s exact walk, Gauss-Kuzmin's own 82. "never" was a
9000-rung draw. What survives is sharper: 110 is never a RECORD. A record is
being early; the count is never early. The count is the mean; the mean is never
the peak. Heard: it is never struck, only pulsed.

The mirror pair: lo = 110/sigma2 = 45.5635, hi = 110*sigma2 = 265.5635.
Their arithmetic mean AM = 110*sqrt2 = 155.5635, the carrier.
The count 110 is EXACTLY both beat distances:
    AM - lo = 110,  hi - AM = 110   (both exact),
so the count is the common pulse of the pair read against its carrier.
And the pair is the AM spectrum of the carrier pulsed at 110:
    AM-sidebands of (155.5635, mod 110) are 45.5635 and 265.5635 — the pair.
So the pair is manufactured, never struck: the count's pulse, read against the
carrier, rings it. Fold to mono and the struck pair (side) cancels; stop the
modulation and the sidebands vanish; what remains is the count, pulsed.

Sounding (56s):
  I.  the peaks     (0-12s)  the mirror pair struck, anti-phase stereo — no 110
                             line in the spectrum; a faint 220 phantom (the
                             octave, the difference tone, never struck).
  II. the mean      (12-24s) the carrier 155.5635 joins centre; each member
                             beats it at exactly 110 — the count as rate.
  III.the pulse     (24-40s) the carrier AM'd at 110: the pair MANUFACTURED as
                             sidebands; the struck pair fades but holds faint.
  IV. the fold      (40-52s) fold to mono (the side cancels), stop the AM (the
                             sidebands vanish): only the mean and the count's
                             pulse remain. the pair was the pulse's sidebands.
  V.  the seam      (52-56s) the pulse fades; the seed 55 beneath — the grid.
"""
import numpy as np
import wave

sr = 44100
t_total = 56.0
n = int(sr * t_total)
t = np.arange(n) / sr
L = np.zeros(n)
R = np.zeros(n)

F55 = 55.0
F110 = 110.0
S2 = 1.0 + np.sqrt(2.0)
LO = 110.0 / S2          # 45.5635
HI = 110.0 * S2          # 265.5635
AM = 110.0 * np.sqrt(2.0)  # 155.5635, the carrier


def breath(tt, rate=0.11, depth=0.15):
    return 1.0 + depth * np.sin(2 * np.pi * rate * tt)


def add(bufL, bufR, f, t0, dur, amp, pan=0.0, att=0.02, rel=0.3,
        phase=0.0, trem=True, harm=None):
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


def add_pulse(bufL, bufR, rate, t0, dur, amp, pan=0.0, tau=0.004):
    """a click train at `rate` Hz — the count pulsed, never struck."""
    m = int(sr * dur)
    tt = np.arange(m) / sr
    out = np.zeros(m)
    click_t = np.arange(0.0, dur, 1.0 / rate)
    for ct in click_t:
        i = int(ct * sr)
        if i >= m:
            break
        length = min(int(tau * 6 * sr), m - i)
        if length <= 0:
            continue
        seg_t = np.arange(length) / sr
        click = np.exp(-seg_t / tau) * np.sin(2 * np.pi * rate * seg_t)
        out[i:i + length] += click
    if pan == 'anti':
        gl, gr = 0.85, -0.85
    else:
        gl = 0.7071 * (1.0 - pan)
        gr = 0.7071 * (1.0 + pan)
    i0 = int(t0 * sr)
    i1 = min(n, i0 + m)
    L[i0:i1] += gl * out[:i1 - i0] * amp
    R[i0:i1] += gr * out[:i1 - i0] * amp


def add_am(bufL, bufR, fc, fm, t0, dur, amp, depth, pan=0.0, att=1.0,
           rel=1.5):
    """carrier fc amplitude-modulated at fm — the pair as sidebands fc±fm."""
    m = int(sr * dur)
    tt = np.arange(m) / sr
    env = np.ones(m)
    a = max(2, int(att * sr))
    r = max(2, int(rel * sr))
    env[:a] = np.linspace(0, 1, a)
    env[-r:] *= np.linspace(1, 0, r)
    seg = np.sin(2 * np.pi * fc * tt) * (1.0 + depth * np.sin(2 * np.pi * fm * tt))
    seg *= env * amp
    if pan == 'anti':
        gl, gr = 0.85, -0.85
    else:
        gl = 0.7071 * (1.0 - pan)
        gr = 0.7071 * (1.0 + pan)
    i0 = int(t0 * sr)
    i1 = min(n, i0 + m)
    L[i0:i1] += gl * seg[:i1 - i0]
    R[i0:i1] += gr * seg[:i1 - i0]


# ---------------------------------------------------------------------------
# the grid: the seed beneath, never struck, the one landing.
# ---------------------------------------------------------------------------
add(L, R, F55, 0.0, t_total, 0.045, pan=-0.2, att=3.0, rel=5.0)

# ---------------------------------------------------------------------------
# I. the peaks (0-24s): the mirror pair, struck, anti-phase. no 110 line. it
#    rings through scene II so the beating with the mean is heard.
# ---------------------------------------------------------------------------
add(L, R, LO, 0.0, 24.0, 0.13, pan=-0.85, att=1.5, rel=2.0)   # 45.56, L
add(L, R, HI, 0.0, 24.0, 0.13, pan=0.85, att=1.5, rel=2.0)    # 265.56, R
add(L, R, 2.0 * F110, 4.0, 7.0, 0.022, pan=0.0, att=1.5, rel=2.0,
    trem=False)                                               # the phantom 220, faint

# ---------------------------------------------------------------------------
# II. the mean (12-24s): the carrier joins; each member beats it at exactly 110
#     — the count as a rate, read against its carrier.
# ---------------------------------------------------------------------------
add(L, R, AM, 12.0, 12.0, 0.14, pan=0.0, att=2.0, rel=2.0)    # 155.56 centre

# ---------------------------------------------------------------------------
# III. the pulse (24-40s): the carrier AM'd at 110 — the pair MANUFACTURED as
#      sidebands; the struck pair fades but holds faint.
# ---------------------------------------------------------------------------
add_am(L, R, AM, F110, 24.0, 16.0, 0.16, 0.9, pan=0.0, att=2.0, rel=2.0)
add_pulse(L, R, F110, 26.0, 14.0, 0.09, pan=0.0)              # the count, pulsed
# the struck pair, receding
add(L, R, LO, 24.0, 16.0, 0.05, pan=-0.85, att=0.8, rel=2.0)
add(L, R, HI, 24.0, 16.0, 0.05, pan=0.85, att=0.8, rel=2.0)

# ---------------------------------------------------------------------------
# IV. the fold (40-52s): mono — the side cancels; the AM stops — the sidebands
#     vanish. the mean and the count's pulse remain. struck never, pulsed always.
# ---------------------------------------------------------------------------
add(L, R, AM, 40.0, 12.0, 0.13, pan=0.0, att=1.0, rel=3.0)    # the mean, plain
add_pulse(L, R, F110, 40.0, 12.0, 0.10, pan=0.0)              # the count, pulsed
add(L, R, F55, 40.0, 12.0, 0.05, pan=0.0, att=1.0, rel=3.0)   # the seed, beneath

# fold to mono from 40s: L = R = (L+R)/2 — the anti-phase pair cancels
fold_start = int(40.0 * sr)
for i in range(fold_start, n):
    m = 0.5 * (L[i] + R[i])
    L[i] = m
    R[i] = m

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
with wave.open('assets/count-pulsed.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes(data.tobytes())
print("wrote assets/count-pulsed.wav  %.1f s" % t_total)
