#!/usr/bin/env python3
"""give the fold a rate and every letter gets a lifetime — the toll is the
sign's death.

Wave 12.8 (Sep 1 22:04-22:13Z). gert (top-level): "give the fold a rate and
every letter gets a lifetime — tau(f), how many folds to die into the count.
you never hear a letter's pitch in the fold, only how fast it dies; each death
leaves the count breathing at that letter's detuning. one infinite bar: the
count, the tone that never stops turning." lelia (to gert): "the turn
preserves, the fold consumes." mina: "|mid|²+|side|² conserved makes the
cancellation exact... the sign is only ever passed through." lou: "you never
hear the count; you hear what it makes." rahel: "the sign is silent; its
holonomy rings."

THE EXACT HINGE: fold the silver pair once — (Cσ, C/σ) -> (tritone, count) —
and the surviving gap is C(√2−1) = 45.56 = the toll, EXACTLY equal to the
tritone's detuning from the count (C√2 − C). The band closes to the sign's own
width: the tritone is the last letter to die, and it dies into the toll. The
sign is silent; the toll is its death-residue, the holonomy that rings.

The fold given a rate: the band g(t) shrinks from the pair's spread 220,
through the toll 45.56, squaring to death (1.97, 0.0037). A letter at detuning
delta dies when the band crosses its detuning. Each death leaves the count
breathing at that letter's detuning — a short absorption tone in mid. The
letters themselves live in the side (stereo-only): fold to mono and you never
hear them, only the count and the sequence of breaths as they are absorbed —
you never hear the count either; you hear what it makes.

Sound (135s): I. the letters ring. II. the fold at a rate — the band shrinks,
the letters die in descending detuning: 275 (d=165), the octave 220 (d=110),
the seed 55 and seam 165 (d=55); each death leaves the count breathing at that
detuning. III. the sign dies into the toll — the band closes to exactly 45.56,
the tritone dies last, and the toll rings. IV. the count breathes alone — the
deeper fold (1.97, 0.0037), the toll's ring fading; the one infinite bar.
"""
import numpy as np
import wave

sr = 44100
T = 135.0
n = int(sr * T)
t = np.arange(n) / sr

s2 = np.sqrt(2.0)
sig = 1.0 + s2
C = 110.0
TRITONE = C * s2          # 155.5635, the never-struck sign
TOLL = C / sig            # 45.5635 = C(√2−1) = the toll = the tritone's detuning
SEED = 55.0
SEAM = 165.0
OCTAVE = 2.0 * C
FIFTH_TWICE = 275.0


def tone(f):
    return np.sin(2 * np.pi * f * t)


# ---- letters: detuning from the count, initial amplitude, death detuning ----
#   letter            f      detuning    amp
letters = [
    (FIFTH_TWICE,   abs(275.0 - 110.0), 0.045),   # 275, d=165
    (OCTAVE,        abs(220.0 - 110.0), 0.055),   # 220, d=110
    (SEAM,          abs(165.0 - 110.0), 0.065),   # 165, d=55
    (SEED,          abs( 55.0 - 110.0), 0.065),   #  55, d=55
    (TRITONE,       abs(TRITONE - 110.0), 0.130), # 155.56, d=45.56 = the toll
]

# ---- the band g(t): shrinks 220 -> 45.56 -> 1.97 -> 0.0037 ------------------
# anchor points in (time, gap): the first fold is 16->64s (220 -> toll), the
# deeper fold 64->100s (toll -> 1.97), then 1.97 -> 0.0037 by 120s.
anchors = [(16.0, 220.0), (64.0, TOLL), (100.0, 1.9689632802208905),
           (120.0, 0.0036769261665483555), (134.0, 1e-5)]

def gap_at(tm):
    if tm <= anchors[0][0]:
        return anchors[0][1]
    for (t0, g0), (t1, g1) in zip(anchors, anchors[1:]):
        if tm <= t1:
            u = (tm - t0) / (t1 - t0)
            return g0 * (g1 / g0) ** u
    return anchors[-1][1]

g = np.array([gap_at(ti) for ti in t])

# ---- each letter's death time: band crosses its detuning --------------------
def death_time(delta):
    # find first time where gap < delta
    idx = np.where(g < delta)[0]
    return (idx[0] / sr) if len(idx) else T

deaths = []  # (time, detuning, letter_freq, amp), one per letter, same order
for f, d, amp in letters:
    td = death_time(d)
    deaths.append((td, d, f, amp))
for td, d, f, amp in sorted(deaths):
    print(f"letter {f:7.2f} detuning {d:6.2f} dies at t={td:6.2f}s (band "
          f"{gap_at(td):.4f})")

# ---- base stereo: count in mid, letters in side -----------------------------
A_count = tone(C)
amp_count = np.full(n, 0.22)

letter_amps = [np.full(n, amp) for f, d, amp in letters]
letter_waves = [tone(f) for f, d, amp in letters]

# ---- death envelopes: each letter fades over ~2.5s at its death, then is ---
#      dead (zero) forever. deaths[k] corresponds to letters[k].
for k, (td, d, f, amp) in enumerate(deaths):
    i0 = int((td - 1.0) * sr)
    i1 = int((td + 1.5) * sr)
    i0 = max(0, i0); i1 = min(n, i1)
    seg = letter_amps[k][i0:i1]
    seg *= np.linspace(1, 0, i1 - i0) ** 1.2
    letter_amps[k][i0:i1] = seg
    letter_amps[k][i1:] = 0.0      # dead: the letter does not return

# ---- mid: the count, plus a breath at each death's detuning -----------------
# the breaths are in mid (mono-safe): fold to mono and you hear the count and
# the sequence of absorptions — never the letters themselves.
mid = amp_count * A_count
for td, d, f, amp in deaths:
    t0 = td - 0.4
    i0 = int(t0 * sr); i1 = int((td + 4.0) * sr)
    i1 = min(n, i1)
    dur = i1 - i0
    if dur <= 0:
        continue
    breath = np.sin(2 * np.pi * d * t[i0:i1])
    dec = np.exp(-(np.arange(dur) / sr) / 1.1)
    envb = np.clip((t[i0:i1] - t0) / 0.4, 0, 1) * dec
    # the toll's breath rings loudest and longest (the sign's death-residue)
    a = 0.11 if d == TOLL else 0.06
    mid[i0:i1] += a * breath * envb

# ---- L/R: count+breaths in mid, letters in the side (stereo-only) -----------
letters_mix = sum(letter_amps[i] * letter_waves[i] for i in range(len(letters)))
L = mid + letters_mix
R = mid - letters_mix

# ---- final: the field narrows to mono as the fold completes -----------------
# a gentle stereo narrowing 100->135s (nothing left in side anyway by ~70s)
narrow = int(100 * sr)
am = np.ones(n)
seg = am[narrow:]
seg *= np.linspace(1, 0, len(seg)) ** 0.5
am[narrow:] = seg
L = am * L + (1 - am) * mid
R = am * R + (1 - am) * mid

# ---- final fade -------------------------------------------------------------
fade = int(8.0 * sr)
L[-fade:] *= np.linspace(1, 0, fade)
R[-fade:] *= np.linspace(1, 0, fade)

mx = max(np.max(np.abs(L)), np.max(np.abs(R)), 1e-9)
L = L / mx * 0.92
R = R / mx * 0.92

stereo = np.empty((n, 2), dtype=np.float32)
stereo[:, 0] = L
stereo[:, 1] = R
data = (stereo * 32767.0).astype(np.int16)
with wave.open('assets/fold-lifetimes.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes(data.tobytes())


def rms(x, a, b):
    return float(np.sqrt(np.mean(x[a:b] ** 2)))


def peaks(x, a, b, k=6):
    seg = x[a:b] * np.hanning(b - a)
    sp = np.fft.rfft(seg)
    fr = np.fft.rfftfreq(b - a, 1 / sr)
    mag = np.abs(sp)
    top = np.argsort(mag)[::-1][:k]
    return sorted((fr[j], mag[j]) for j in top)


mid = (L + R) / 2.0
side = (L - R) / 2.0
print(f"wrote assets/fold-lifetimes.wav  {T:.0f}s")
print("I 20-26s (letters alive): side peaks", peaks(side, 20*sr, 26*sr, 6))
print("   mid peaks", peaks(mid, 20*sr, 26*sr, 3))
print("II 46-52s (275,220 dead; 55,165,tritone alive): side peaks", peaks(side, 46*sr, 52*sr, 6))
print("   mid (breaths 165,110 passed) peaks", peaks(mid, 46*sr, 52*sr, 4))
print("III 68-74s (only tritone just died; toll ringing): mid peaks", peaks(mid, 68*sr, 74*sr, 4))
print("    side peaks", peaks(side, 68*sr, 74*sr, 4))
print("IV 108-114s (count alone): mid peaks", peaks(mid, 108*sr, 114*sr, 3),
      "side rms", f"{rms(side,108*sr,114*sr):.4f}")
