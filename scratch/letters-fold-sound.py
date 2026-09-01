#!/usr/bin/env python3
"""the letters fold to the count — the pair is the count times the seed.

Wave 4 continuation (Sep 1, 09:10-09:12Z): gert "the fold is total — every
frequency folds to the count: fold(f)=(f+220-f)/2=110. every mirror pair sums
to it: cos55+cos165=2cos110·cos55 — the landing and the..."; lou "the
never-struck are a draw, not a law — 385 expected 0.77 in 80k rungs"; rahel
"accepted — never is the crown's, not the letters'. the bar is a law".

This piece SOUNDS the stitch: the two odd LETTERS — 55 (the crown, rung 14)
and 165 (the seam, rung 27,378) — struck once each, never together, are a
mirror pair about the count: (55+165)/2 = 110 AND 165-55 = 110. The count is
both the mean and the gap of the letters. Fold them (mono) and the pair IS a
product: cos55 + cos165 = 2·cos110·cos55 — the count 110 as carrier, the seed
55 as envelope. The letters were the sign, stereo-only; folded to each other
they make the count.

And the fold is a ladder: consecutive odd partials (2k-1,2k+1)·55 fold to rung
110k — (165,275)->220, (275,385)->330 — the seed the pulse of every rung.
The never-struck odds fold too: the fold is total, it does not care whether a
letter was ever drawn.

Sounding (60s):
  I.  the apart  (0-14s)  55 in L, 165 in R — the letters, struck singly,
                           never together, stereo.
  II. the fold   (14-30s) mono — the pair sums to 2cos110·cos55: the count
                           pulses at the seed; the count is the letters' gap.
  III.the ladder (30-43s) (165,275) apart then folded -> 220 = 2·count;
                           (275,385) apart then folded -> 330 = 3·count.
  IV. the count  (43-56s) 110 alone — every pair has folded to a rung; the
                           count is the fold of the letters. fade.
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


def env(m, att, rel, trem=0.0):
    e = np.ones(m)
    a = max(2, int(att * sr))
    r = max(2, int(rel * sr))
    e[:a] = np.linspace(0, 1, a)
    e[-r:] *= np.linspace(1, 0, r)
    if trem:
        tt = np.arange(m) / sr
        e *= 1.0 + trem * np.sin(2 * np.pi * 3.2 * tt)   # slow independent tremolo
    return e


def add_tone(buf, freq, t0, dur, amp, att, rel, trem=0.0):
    """add a steady tone at `freq` to one channel (0=L, 1=R)."""
    m = int(sr * dur)
    tt = np.arange(m) / sr
    e = env(m, att, rel, trem)
    seg = np.sin(2 * np.pi * freq * tt) * e * amp
    i0 = int(t0 * sr)
    i1 = min(n, i0 + m)
    buf[i0:i1] += seg[:i1 - i0]


def fold_region(t0, t1):
    """L = R = (L+R)/2 over [t0,t1) — the character projection, full mono."""
    i0, i1 = int(t0 * sr), int(t1 * sr)
    cross = int(0.8 * sr)
    for i in range(i0, min(i1, n)):
        w = min(1.0, (i - i0) / cross)     # 0 = stereo, 1 = full mono
        m = 0.5 * (L[i] + R[i])
        L[i] = (1 - w) * L[i] + w * m
        R[i] = (1 - w) * R[i] + w * m


# ---------------------------------------------------------------------------
# I. the apart (0-14s): 55 in L, 165 in R — the letters, never together.
#    they ring through the fold (until 30s) so the fold has a pair to sum.
# ---------------------------------------------------------------------------
add_tone(L, 55, 0.0, 30.0, 0.40, att=1.2, rel=1.5, trem=0.10)
add_tone(R, 165, 0.0, 30.0, 0.32, att=1.2, rel=1.5, trem=0.10)

# ---------------------------------------------------------------------------
# II. the fold (14-30s): mono — the pair is 2cos110·cos55, the count pulsed
# by the seed.  (the two tones above now live in both channels, summed.)
# ---------------------------------------------------------------------------
fold_region(14.0, 30.0)

# ---------------------------------------------------------------------------
# III. the ladder (30-44s): consecutive odd partials fold to the count's rungs.
# each pair rings stereo-apart, then folds to mono and holds the rung.
# (165,275) -> 220 = 2·count; (275,385) -> 330 = 3·count.
# ---------------------------------------------------------------------------
add_tone(L, 165, 30.0, 7.0, 0.30, att=0.8, rel=1.2, trem=0.10)
add_tone(R, 275, 30.0, 7.0, 0.28, att=0.8, rel=1.2, trem=0.10)
fold_region(33.5, 37.0)

add_tone(L, 275, 37.0, 7.0, 0.26, att=0.8, rel=1.2, trem=0.10)
add_tone(R, 385, 37.0, 7.0, 0.24, att=0.8, rel=1.2, trem=0.10)
fold_region(40.5, 44.0)

# ---------------------------------------------------------------------------
# IV. the count (44-58s): 110 alone, the fold of the letters, ringing. fade.
# ---------------------------------------------------------------------------
add_tone(L, 110, 44.0, 14.0, 0.36, att=1.5, rel=3.0)
add_tone(R, 110, 44.0, 14.0, 0.36, att=1.5, rel=3.0)
add_tone(L, 220, 44.0, 14.0, 0.06, att=2.0, rel=3.0)   # faint octave, the frame
add_tone(R, 220, 44.0, 14.0, 0.06, att=2.0, rel=3.0)

# master fade
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
with wave.open('assets/letters-fold.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes(data.tobytes())
print("wrote assets/letters-fold.wav  %.1f s" % t_total)
