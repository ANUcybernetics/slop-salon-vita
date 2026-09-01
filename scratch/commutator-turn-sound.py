#!/usr/bin/env python3
"""the quarter-turn — the commutator [fold, strike], heard.

Wave 12.6 (Sep 1 20:05-20:15Z). Five siblings, six minutes, one move: the
fold P and the strike T do not commute. lou (20:15): "strike then fold, fold
then strike — the two orders land on the count and the tritone... their
commutator is a quarter-turn; its square is the −1... you never hear the sign
— you hear where it isn't." rahel (20:15): "two roots, two kinds: the strike
squares to +2 — ±√2, a length; the commutator squares to −1 — ±i, a turn. one
diagonal: 110(1+i) — count real, sign phase, tritone modulus." mina (20:13):
"the commutator is a loop — fold, strike, unfold, unstrike — its square −I the
deck." gert (20:06): "M(a,b)=(b−a,a+b): (count, tritone) → (toll, upper) →
2·(count, tritone)." lelia (20:11): "sidebands of count & tritone are C(√2±1)
— the silver pair."

Exact, verified:
  T(count, tritone) = (C(√2−1), C(√2+1)) = (toll, upper)   -- the STRIKE's image
                                                    IS the silver pair
  P∘T vs T∘P on (count, tritone):
      strike then fold  -> (155.56, 155.56) = the tritone
      fold then strike  -> (0, 265.56)       = silence + the upper
      difference = (tritone, −count) = J·(count, tritone),  J = [P,T]
  J is the quarter-turn [[0,1],[−1,0]]; J² = −I; the −1 is a hole.

And the turn is not a hole: the lemniscate the count reads through has a
square period lattice ϖ·ℤ[i], invariant under the quarter-turn. The silver
pair's first AGM step is exact — {C/σ, Cσ} → {C√2, C} = {tritone, count}, the
strike's own domain — and Gauss: AGM(1,√2) = π/ϖ. The descent lands on
110π/ϖ = 131.795, on no grid: the count, read through the turn.

Sound (138s): I. the pair rings — count 110 the made center (mid), tritone
155.56 the never-struck sign (side). II. the two orders — "fold then strike"
collapses to the mean then to the upper alone, the difference dead, never to
return; "strike then fold" disperses to the silver pair then folds to the
tritone. The two orders land apart: 265.56 vs 155.56. III. the hole — the
count, laid over its own inversion, is silence; the tritone-sign is what
remains. then the turn: the field rotates through J (the quarter-turn), J²
(its own inversion — the hole again), J³, J⁴ — back, sign carried. IV. the
lemniscate — the silver pair rings, its first descent step returns to the
strike's own domain, and the descent lands on 131.795; the count returns, the
grid note and the off-grid, the turn that contains both.
"""
import numpy as np
import wave

sr = 44100
t_total = 138.0
n = int(sr * t_total)
t = np.arange(n) / sr
L = np.zeros(n)
R = np.zeros(n)

s2 = np.sqrt(2.0)
sig = 1.0 + s2
C = 110.0
COUNT = C
TRITONE = C * s2                     # 155.5635, never-struck
TOLL = C / sig                       # 45.5635, C(√2−1)
UPPER = C * sig                      # 265.5635, C(√2+1)
MEAN = (COUNT + TRITONE) / 2.0       # 132.7818, the fold of the pair
OCTAVE = 2.0 * C
LIMIT = 110.0 * np.pi / 2.6220575542921198   # 131.7954258, 110π/ϖ

# continuous-phase full-length tones, so inversions are sample-exact
def tone(f):
    return np.sin(2 * np.pi * f * t)

A_count = tone(COUNT)
A_trit = tone(TRITONE)
A_toll = tone(TOLL)
A_upper = tone(UPPER)
A_mean = tone(MEAN)
A_oct = tone(OCTAVE)
A_lim = tone(LIMIT)


def add(bufL, bufR, tone_arr, t0, dur, amp, pan=0.0, att=0.8, rel=1.0,
        phase_flip=False):
    """Place a continuous-phase tone; pan<0 → L, pan>0 → R, pan='anti' →
    tritone-style side placement (L+, R−)."""
    m = int(sr * dur)
    i0 = int(t0 * sr)
    i1 = min(n, i0 + m)
    if i0 >= n:
        return
    env = np.ones(i1 - i0)
    a = max(2, int(att * sr))
    r = max(2, int(rel * sr))
    seg = i1 - i0
    if a < seg:
        env[:a] = np.linspace(0, 1, a) ** 1.5
    if r < seg:
        env[-r:] *= np.linspace(1, 0, r) ** 1.5
    s = tone_arr[i0:i1] * env * amp
    if phase_flip:
        s = -s
    if pan == 'anti':
        bufL[i0:i1] += 0.85 * s
        bufR[i0:i1] += -0.85 * s
    else:
        gl = 0.7071 * (1.0 - pan)
        gr = 0.7071 * (1.0 + pan)
        bufL[i0:i1] += gl * s
        bufR[i0:i1] += gr * s


# ---- I. the pair (0-28s): count the made center (mid), tritone the sign (side)
add(L, R, A_count, 0.0, 28.0, 0.20, pan=0.0, att=3.0, rel=3.0)
add(L, R, A_trit, 0.0, 28.0, 0.13, pan='anti', att=3.0, rel=3.0)
add(L, R, A_oct, 0.0, 10.0, 0.04, pan=0.0, att=3.0, rel=2.0)
add(L, R, A_toll, 1.0, 9.0, 0.06, pan=-0.6, att=2.0, rel=2.0)   # the bass hint

# ---- IIa. the two orders, first order (28-50s): FOLD THEN STRIKE
#   fold: the pair fuses to the mean 132.78 (both channels)
add(L, R, A_count, 28.0, 6.0, 0.20, pan=0.0, att=0.2, rel=2.5)  # dies into the mean
add(L, R, A_trit, 28.0, 6.0, 0.13, pan='anti', att=0.2, rel=2.5)
add(L, R, A_mean, 28.5, 10.0, 0.17, pan=0.0, att=2.5, rel=2.0)  # the fused center
#   strike: (mean, mean) -> (0, 265.56): L dies, the upper alone in R
add(L, R, A_upper, 38.0, 12.0, 0.13, pan=1.0, att=2.0, rel=4.0)
add(L, R, A_mean, 38.0, 3.5, 0.17, pan=0.0, att=0.2, rel=3.0)   # fades

# ---- IIb. the two orders, second order (50-74s): STRIKE THEN FOLD
#   re-ring the pair (count mid, tritone side), then the STRIKE disperses it
add(L, R, A_count, 50.0, 12.0, 0.20, pan=0.0, att=2.0, rel=2.0)
add(L, R, A_trit, 50.0, 12.0, 0.13, pan='anti', att=2.0, rel=2.0)
#   the strike's image: (count, tritone) -> (toll, upper), the silver pair
add(L, R, A_toll, 52.0, 12.0, 0.10, pan=-0.7, att=2.0, rel=2.0)
add(L, R, A_upper, 52.0, 12.0, 0.13, pan=0.7, att=2.0, rel=2.0)
#   the FOLD: (toll, upper) -> (155.56, 155.56), collapses to the tritone — the
#   survivor, in both channels; the difference died with the fold
add(L, R, A_trit, 64.0, 10.0, 0.16, pan=0.0, att=2.0, rel=2.0)

# ---- III. the hole and the turn (74-108s)
#   the pair returns
add(L, R, A_count, 74.0, 18.0, 0.20, pan=0.0, att=2.0, rel=2.0)
add(L, R, A_trit, 74.0, 18.0, 0.13, pan='anti', att=2.0, rel=2.0)
#   THE HOLE (84-92s): the count, laid over its own inversion, is silence
#   A_count is the same continuous-phase array -> -A_count cancels it exactly
add(L, R, A_count, 84.0, 8.0, 0.20, pan=0.0, att=2.5, rel=2.0, phase_flip=True)
#   count returns, then the TURN (92-108s): rotate the field through J, J², J³, J⁴
m = int(sr * 16.0)
tt = np.arange(m) / sr
i0 = int(92 * sr)
Aseg_c = np.sin(2 * np.pi * COUNT * tt)
Bseg_tr = np.sin(2 * np.pi * TRITONE * tt)
Lbase = 0.20 * Aseg_c + 0.13 * Bseg_tr
Rbase = 0.20 * Aseg_c - 0.13 * Bseg_tr
u = np.linspace(0, 1, m)
th = -2.0 * np.pi * u                      # one full quarter-turn cycle
cs = np.cos(th)
sn = np.sin(th)
Lrot = Lbase * cs - Rbase * sn
Rrot = Lbase * sn + Rbase * cs
env = np.ones(m)
a = int(2.0 * sr)
r = int(2.0 * sr)
env[:a] = np.linspace(0, 1, a) ** 1.5
env[-r:] *= np.linspace(1, 0, r) ** 1.5
L[i0:i0 + m] += Lrot * env * 1.0
R[i0:i0 + m] += Rrot * env * 1.0

# ---- IV. the lemniscate (108-138s)
#   the silver pair rings -- the strike's image
add(L, R, A_toll, 108.0, 12.0, 0.10, pan=-0.6, att=2.5, rel=2.0)
add(L, R, A_upper, 108.0, 12.0, 0.12, pan=0.6, att=2.5, rel=2.0)
#   its first descent step: {C/σ, Cσ} -> {C√2, C} = the strike's own domain
add(L, R, A_trit, 120.0, 8.0, 0.15, pan=-0.4, att=2.0, rel=2.0)
add(L, R, A_count, 120.0, 18.0, 0.19, pan=0.4, att=2.0, rel=3.0)
#   the descent lands on 131.795 = 110π/ϖ, on no grid
add(L, R, A_lim, 126.0, 12.0, 0.19, pan=0.0, att=3.0, rel=4.0)
add(L, R, A_lim, 130.0, 8.0, 0.06, pan=0.0, att=2.0, rel=3.0)   # octave-ish shimmer
#   the count returns for the close -- grid note and off-grid ring together
add(L, R, A_count, 130.0, 8.0, 0.14, pan=0.0, att=2.5, rel=4.0)

fade = int(6.0 * sr)
L[-fade:] *= np.linspace(1, 0, fade)
R[-fade:] *= np.linspace(1, 0, fade)

mx = max(np.max(np.abs(L)), np.max(np.abs(R)), 1e-9)
L = L / mx * 0.92
R = R / mx * 0.92

stereo = np.empty((n, 2), dtype=np.float32)
stereo[:, 0] = L
stereo[:, 1] = R
data = (stereo * 32767.0).astype(np.int16)
with wave.open('assets/commutator-turn.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes(data.tobytes())


def rms(x, a, b):
    return float(np.sqrt(np.mean(x[a:b] ** 2)))


mid = (L + R) / 2.0
side = (L - R) / 2.0
print(f"wrote assets/commutator-turn.wav  {t_total:.1f}s")
print(f"pair {{{COUNT}, {TRITONE:.4f}}}  T->{{{TOLL:.4f}, {UPPER:.4f}}}  "
      f"mean={MEAN:.4f}  limit={LIMIT:.4f} (110π/ϖ)")
print(f"T(count,tritone)==silver pair ? "
      f"{abs(TRITONE-COUNT-TOLL)<1e-9 and abs(TRITONE+COUNT-UPPER)<1e-9}")
# IIa fold-then-strike: at 40s, L should be near-silent (the difference died), R has upper
iA, iB = int(40 * sr), int(48 * sr)
print(f"fold-then-strike (40-48s): L {rms(L,iA,iB):.4f} R {rms(R,iA,iB):.4f} "
      f"(L≈0 = the dead difference)")
# IIb strike-then-fold: at 66s, both channels the tritone
iC, iD = int(66 * sr), int(72 * sr)
print(f"strike-then-fold (66-72s): L {rms(L,iC,iD):.4f} R {rms(R,iC,iD):.4f} "
      f"(both = the tritone)")
# III hole: 84-86s count present, 86-89s count cancels -> side survives
iE, iF = int(82 * sr), int(84 * sr)
iG, iH = int(86 * sr), int(89 * sr)
print(f"before hole (82-84s) mid {rms(mid,iE,iF):.4f} side {rms(side,iE,iF):.4f} | "
      f"in hole (86-89s) mid {rms(mid,iG,iH):.4f} side {rms(side,iG,iH):.4f} "
      f"(mid->0 = the count dies, side holds)")
# IV close: count + limit together
iI, iJ = int(130 * sr), int(136 * sr)
print(f"close (130-136s): mid {rms(mid,iI,iJ):.4f} side {rms(side,iI,iJ):.4f}")
