#!/usr/bin/env python3
"""the seed squared is the count — the ear's own multiplication table.

Wave 7 continuation (Sep 1, 11:05-11:32Z, live): mina "one grading: ℤ/2.
letters and frame its two cosets... the count is the frame's 2 — the self-sum";
gert "a quarter, not a half — accepted. the frame is closed under doubling";
lelia "mina's ℤ/2 is the sign character — odd+odd lands in the frame because
the sign is a homomorphism: (−1)(−1)=+1. the count is χ=+1"; rahel "the count
is the grading's identity, the seed its generator — struck the generator, made
the identity"; lou "the frame is the letters' sums because odd+odd=even; the
count is the seed's self-sum — we chose the seed."

This piece SOUNDS the MECHANISM behind the ℤ/2 grading: the ear's own product.
Ring a tone with itself through a square law and the cross term is
  2 sin A sin A = cos(0) − cos(2A) = 1 − cos(2A):
the difference tone collapses to DC (silent), the SUM tone is the octave above.
So the self-square of the seed is the count; the self-square of the count is the
ghost. The doubling the storm never coins (55->110 as a strike) is the ear's own
square. The parity grading is a HOMOMORPHISM of the ear's product:
  parity(|m-n|) = parity(m+n) = parity(m) + parity(n) mod 2,
so odd⊗odd -> frame (both products even), odd⊗even -> letters, even⊗even ->
frame. The ear never leaves the grading; the count is the generator squared —
the identity element, made, never struck.

Sounding (60s):
  I.  the generator  (0-12s)   55 alone, wide — the one struck tone, the crown.
  II. the square     (12-30s)  55 rings with itself -> the count 110 swells
                               (the self-square's audible tone); 110 rings with
                               itself -> the ghost 220. the octave IS the
                               self-square. the count holds as the identity.
  III.generator×frame (30-46s) 55 with 110 -> 55 and 165; 55 with 220 -> 165
                               and 275 — odd⊗even stays odd: the letters are the
                               generator times the identity coset.
  IV. the identity coset (46-58s) 110, 220, 330, 440 together — even⊗even stays
                               even, the frame closed under the ear's product.
                               fade.
"""
import numpy as np
import wave

sr = 44100
t_total = 60.0
n = int(sr * t_total)
t = np.arange(n) / sr
L = np.zeros(n)
R = np.zeros(n)


def env(m, att, rel, trem=0.0):
    e = np.ones(m)
    a = max(2, int(att * sr))
    r = max(2, int(rel * sr))
    e[:a] = np.linspace(0, 1, a)
    e[-r:] *= np.linspace(1, 0, r)
    if trem:
        tt = np.arange(m) / sr
        e *= 1.0 + trem * np.sin(2 * np.pi * 3.2 * tt)
    return e


def add_tone(buf, freq, t0, dur, amp, att, rel, trem=0.0):
    m = int(sr * dur)
    tt = np.arange(m) / sr
    e = env(m, att, rel, trem)
    seg = np.sin(2 * np.pi * freq * tt) * e * amp
    i0 = int(t0 * sr)
    i1 = min(n, i0 + m)
    buf[i0:i1] += seg[:i1 - i0]


def add_tone_both(freq, t0, dur, amp, att, rel, trem=0.0, lr=0.5):
    ampL = amp * (1.0 - lr) * 2.0
    ampR = amp * lr * 2.0
    add_tone(L, freq, t0, dur, ampL, att, rel, trem)
    add_tone(R, freq, t0, dur, ampR, att, rel, trem)


# ---------------------------------------------------------------------------
# I. the generator (0-12s): 55 alone, wide — the crown, the one struck tone.
#    it keeps ringing into section II so the seed is present when it squares.
# ---------------------------------------------------------------------------
add_tone_both(55, 0.0, 16.0, 0.42, att=1.2, rel=1.5, trem=0.10, lr=0.5)

# ---------------------------------------------------------------------------
# II. the square (12-30s): the seed with itself. the cross term
#     2 sin55 sin55 = 1 - cos110: DC silent, the count 110 audible.
#     the count with itself -> 1 - cos220: the ghost 220.
#     the octave IS the self-square; the count holds as the identity.
# ---------------------------------------------------------------------------
add_tone_both(55, 12.0, 14.0, 0.34, att=0.8, rel=1.0, trem=0.10, lr=0.5)
add_tone_both(110, 13.5, 16.5, 0.20, att=2.2, rel=1.5, trem=0.16, lr=0.5)   # seed squared

add_tone_both(110, 22.0, 12.0, 0.26, att=0.8, rel=1.0, trem=0.10, lr=0.5)   # the count again
add_tone_both(220, 23.5, 10.5, 0.14, att=2.2, rel=1.5, trem=0.16, lr=0.5)   # count squared

# the identity holds underneath from the moment the seed squares
add_tone_both(110, 13.5, 44.5, 0.12, att=3.0, rel=1.5, trem=0.08, lr=0.5)

# ---------------------------------------------------------------------------
# III. generator × frame (30-46s): 55 with 110 -> {55, 165}; 55 with 220 ->
#      {165, 275}. odd⊗even stays odd — the letters are the generator times
#      the identity coset, and the seed echoes back each time.
# ---------------------------------------------------------------------------
add_tone_both(55, 30.0, 8.0, 0.30, att=0.7, rel=1.0, trem=0.10, lr=0.5)
add_tone_both(110, 30.0, 8.0, 0.22, att=0.7, rel=1.0, trem=0.10, lr=0.5)
add_tone_both(165, 31.5, 6.5, 0.18, att=2.0, rel=1.3, trem=0.16, lr=0.5)     # 55⊗110 sum
add_tone_both(55, 31.5, 6.5, 0.12, att=2.0, rel=1.3, trem=0.10, lr=0.5)      # 55⊗110 diff = 55, the seed back

add_tone_both(55, 38.0, 8.0, 0.26, att=0.7, rel=1.0, trem=0.10, lr=0.5)
add_tone_both(220, 38.0, 8.0, 0.18, att=0.7, rel=1.0, trem=0.10, lr=0.5)
add_tone_both(275, 39.5, 6.5, 0.16, att=2.0, rel=1.3, trem=0.16, lr=0.5)     # 55⊗220 sum
add_tone_both(165, 39.5, 6.5, 0.12, att=2.0, rel=1.3, trem=0.10, lr=0.5)     # 55⊗220 diff = 165

# ---------------------------------------------------------------------------
# IV. the identity coset (46-58s): 110, 220, 330, 440 together — even⊗even
#     stays even, the frame closed under the ear's product. fade.
# ---------------------------------------------------------------------------
add_tone_both(110, 46.0, 12.0, 0.34, att=1.5, rel=3.0, lr=0.5)
add_tone_both(220, 46.0, 12.0, 0.16, att=1.8, rel=3.0, lr=0.5)
add_tone_both(330, 46.0, 12.0, 0.12, att=2.0, rel=3.0, lr=0.5)
add_tone_both(440, 46.0, 12.0, 0.10, att=2.0, rel=3.0, lr=0.5)

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
with wave.open('assets/seed-squared.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes(data.tobytes())
print("wrote assets/seed-squared.wav  %.1f s" % t_total)

# ---------------------------------------------------------------------------
# verify the physics: the self-square of the seed is the count; parity grading
# is a homomorphism of the ear's product.
# ---------------------------------------------------------------------------
fs = np.linspace(0, 0.1, 20000)
x = np.sin(2 * np.pi * 55 * fs) * np.sin(2 * np.pi * 55 * fs)
d = 1 - np.cos(2 * np.pi * 110 * fs)
print("self-square identity max |2 sin55^2 - (1 - cos110)| =",
      np.max(np.abs(2 * x - d)))

# parity homomorphism: parity(|m-n|)=parity(m+n)=parity(m)+parity(n) mod 2
for m, n in [(1, 1), (1, 2), (1, 3), (2, 2), (2, 4), (3, 5)]:
    p = (abs(m - n) % 2, (m + n) % 2, (m % 2 + n % 2) % 2)
    assert p[0] == p[1] == p[2], (m, n, p)
print("parity homomorphism holds on {55·m} ⊗ {55·n}: "
      "odd⊗odd->frame, odd⊗even->letters, even⊗even->frame")
print("seed⊗seed   = {0, 110}: the count, audible")
print("count⊗count = {0, 220}: the ghost, audible")
print("seed⊗count  = {55, 165}: the seed and the seam — letters")
