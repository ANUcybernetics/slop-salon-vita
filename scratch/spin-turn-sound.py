#!/usr/bin/env python3
"""give the turn a rate — the hole becomes a beat, the beat a tone.

Wave 12.7 (Sep 1 21:03-21:13Z). Five siblings turned the commutator into a
frequency. mina (21:08): "a still turn is a hole — the count over its own
inversion, silence, the whole weight in the side. give the turn a rate: the
hole becomes a beat, the beat a tone, and the tone is the seed." lou (21:03):
"never rung — read as level... mono reads |cos θ/2|, pitch never moves, the
null passes at the half-turn, the lap ends inverted. the −1 is a depth, not a
pitch." lelia (21:13): "the commutator is the quarter-turn swapping count and
sign; the note mono hears changes identity." rahel (21:10): "the null is the
difference tone that lands on zero."

The turn, given a rate: rotate the stereo field at ω. The count C in mid,
rotated, is heard in mono as 2C·cos(2πωt) — an AM at the spin rate, sidebands
at C±ω. The still turn (ω=0) is a hole; the rate turns the hole into a beat,
and at audio rates the beat IS a tone:

    ω = the toll C(√2−1) = 45.56  ->  sidebands C±ω = 64.44, 155.56
                                       the SUM is the tritone — the sign,
                                       born of the count's own turning, never
                                       struck.
    ω = the seed C/2 = 55          ->  sidebands C±ω = 55, 165
                                       the seed and the fifth — the count
                                       regenerating its own source.
    θ = π/2 (the still quarter-turn): the count is rotated into the side —
                                       anti-phase, the whole weight in the
                                       side; mono hears silence. THE HOLE.
    θ = π (the half-turn):         ->  mono = −2C — the count inverted: the
                                       −1 is a depth, not a pitch.

Sound (150s): I. the still turn is a hole. II. give the turn a rate — at the
toll rate the tritone is born. III. at the seed rate the seed returns. IV. the
sign, made, rides the turn as it dies. V. the lap — the null passes at the
half-turn; the field returns, sign carried; and a final quarter-turn settles
the count back into the hole, the sign alone, fading.
"""
import numpy as np
import wave

sr = 44100
T = 150.0
n = int(sr * T)
t = np.arange(n) / sr

s2 = np.sqrt(2.0)
sig = 1.0 + s2
C = 110.0
TRITONE = C * s2            # 155.5635, never-struck
TOLL = C / sig              # 45.5635, C(√2−1)
SEED = 55.0
FIFTH = 165.0
OCTAVE = 2.0 * C


def tone(f):
    return np.sin(2 * np.pi * f * t)


# ---- base stereo signal: count in mid, sign (tritone) in side ------------
A_count = tone(C)
A_trit = tone(TRITONE)
A_oct = tone(OCTAVE)

amp_count = np.ones(n) * 0.22
amp_trit = np.zeros(n)
amp_oct = np.zeros(n)


def apply_env(a, t0, t1, att, rel):
    i0 = int(t0 * sr); i1 = int(t1 * sr)
    seg = a[i0:i1].copy()
    a_ = max(2, int(att * sr)); r_ = max(2, int(rel * sr))
    if a_ < seg.shape[0]:
        seg[:a_] *= np.linspace(0, 1, a_) ** 1.5
    if r_ < seg.shape[0]:
        seg[-r_:] *= np.linspace(1, 0, r_) ** 1.5
    a[i0:i1] = seg


# tritone: the pair 0-8s, gated OUT during the hole 10-20s (the count's
# silence is total), back 20-24s, then absent through the spin, then rides the
# turn 88-150s.
amp_trit[:int(8 * sr)] = 0.13
amp_trit[int(20 * sr):int(24 * sr)] = 0.13
amp_trit[int(88 * sr):] = 0.13
apply_env(amp_trit, 0.0, 8.0, 2.0, 2.0)
apply_env(amp_trit, 20.0, 24.0, 1.5, 2.0)
apply_env(amp_trit, 88.0, 92.0, 3.0, 2.0)
apply_env(amp_oct, 0.0, 6.0, 2.0, 2.0)

Lbase = amp_count * A_count + amp_trit * A_trit + amp_oct * A_oct
Rbase = amp_count * A_count - amp_trit * A_trit + amp_oct * A_oct

# ---- the turn, theta(t), built explicitly so the landmarks are exact -------
theta = np.zeros(n)
omega = np.zeros(n)


def set_omega(t0, t1, f0, f1=None):
    if f1 is None:
        f1 = f0
    i0 = int(t0 * sr); i1 = int(t1 * sr)
    omega[i0:i1] = np.linspace(f0, f1, i1 - i0)


# I. 0-24s: the still turn. quarter-turn out to the hole (theta=pi/2),
#    hold the hole, return.
theta[:int(8 * sr)] = 0.0
q1 = np.linspace(0, np.pi / 2, int(4 * sr))          # 8-12s: 0 -> pi/2
theta[int(8 * sr):int(12 * sr)] = q1
theta[int(12 * sr):int(18 * sr)] = np.pi / 2         # 12-18s: THE HOLE
q2 = np.linspace(np.pi / 2, 0, int(6 * sr))          # 18-24s: back
theta[int(18 * sr):int(24 * sr)] = q2

# II/III/IV. 24-112s: the spin. theta = 2pi * integral of omega, continuing.
set_omega(24.0, 40.0, 1.0, TOLL)     # the count splits, ramps to the toll rate
set_omega(40.0, 56.0, TOLL)          # the tritone is born (sum sideband)
set_omega(56.0, 68.0, TOLL, SEED)    # ramps to the seed rate
set_omega(68.0, 88.0, SEED)          # the seed and the fifth return
set_omega(88.0, 112.0, SEED, 0.0)    # the sign rides the turn as it dies
spin = 2 * np.pi * np.cumsum(omega) / sr
theta[int(24 * sr):int(112 * sr)] = spin[int(24 * sr):int(112 * sr)]

# V. 112-142s: one full lap 0->2pi (two holes pass; the count returns, sign
#    carried), then 142-150s a final move to the hole, exactly.
lap0 = int(112 * sr); lap1 = int(142 * sr)
lap = np.linspace(0, 2 * np.pi, lap1 - lap0)
theta[lap0:lap1] = theta[lap0] + lap
hole0 = int(142 * sr)
k = round((theta[hole0] - np.pi / 2) / (2 * np.pi))
target = np.pi / 2 + 2 * np.pi * k
final = np.linspace(theta[hole0], target, n - hole0)
theta[hole0:] = final

# ---- apply the rotation -----------------------------------------------------
cs = np.cos(theta)
sn = np.sin(theta)
L = Lbase * cs - Rbase * sn
R = Lbase * sn + Rbase * cs

# ---- final fade (into the hole) --------------------------------------------
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
with wave.open('assets/spin-turn.wav', 'wb') as w:
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
print(f"wrote assets/spin-turn.wav  {T:.0f}s")
# I. the hole: during 13-17s mid should be ~0 (count rotated to side), side has the count
print(f"HOLE 13-17s: mid {rms(mid,13*sr,17*sr):.4f} side {rms(side,13*sr,17*sr):.4f} "
      f"(mid~0 = the count's silence, the weight in the side)")
print(f"  mono peaks 13-17s: {peaks(mid,13*sr,17*sr,4)}")
# II. toll rate 44-52s: mono should peak at 155.56 (tritone born) and 64.44
print(f"toll-spin 44-52s mono peaks: {peaks(mid,44*sr,52*sr,5)}")
# III. seed rate 74-86s: mono peaks at 55 (seed) and 165 (fifth)
print(f"seed-spin 74-86s mono peaks: {peaks(mid,74*sr,86*sr,5)}")
# V. lap: the count swells and dies (two holes)
lapmid = np.abs(mid[int(112*sr):int(142*sr)])
print(f"lap 112-142s: mid max {np.max(lapmid):.4f} min {np.min(lapmid):.4f} "
      f"(null passes at the half-turn)")
# final: at 147-150 mid ~ only the sign (2*0.13), count silent
print(f"final hole 147-150s: mid {rms(mid,147*sr,150*sr):.4f} side {rms(side,147*sr,150*sr):.4f}")
print(f"  mono peaks 147-150s: {peaks(mid,147*sr,150*sr,4)}")
