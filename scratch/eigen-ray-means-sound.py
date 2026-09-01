#!/usr/bin/env python3
"""the eigen-ray, made — the three means of the silver pair are the first two
eigen-ray rungs and their center.

Wave 12 (Sep 1 16:03-16:09Z): the two means are an octave pair.  rahel:
"AM/HM = (σ+1/σ)²/4 = 2, so {HM, AM} = {C/√2, C√2}. the mirror takes their
geometric mean: AM·HM = C². the count is the octave's made center — the mirror
recurses; the fold doesn't — its mean of the means is 116.7."

The new identification: for the silver pair {C/σ, Cσ} = {45.56, 265.56},

    HM = 2ab/(a+b) = 55√2 = 77.78   -- the eigen-ray, rung 1 (never-struck, made)
    GM = √(ab)      = 110           -- the count, the octave's geometric center
    AM = (a+b)/2    = 110√2 = 155.56 -- the tritone, eigen-ray rung 2

{AM, HM} = {55√2, 110√2} are CONSECUTIVE eigen-ray rungs -- ratio 2, an octave,
never struck.  Their difference tone is the lower mean: AM − HM = HM.  The
count splits that octave with gaps in ratio √2: toll 45.56 above, 32.22 below.

Sound: the count 110 holds center the whole piece (the mirror's constant).
The silver pair rings wide, then the two means rise in stereo, anti-phase —
off-grid, never struck, they cancel in mono (the ear's product sounds the
lower mean as their own gap).  Fold to mono: the means die, only the count
holds; the mirror recurses (GM of the means = 110), the fold's mean-of-means
116.67 lands off-grid and dies.  Coda: the eigen-ray rungs 55√2, 110√2 ring
once more, 220√2 hints above, and the count fades.  never struck, made.
"""
import numpy as np
import wave

sr = 44100
t_total = 112.0
n = int(sr * t_total)
t = np.arange(n) / sr
L = np.zeros(n)
R = np.zeros(n)

GM = 110.0
HM = 55.0 * np.sqrt(2.0)          # 77.78, the eigen-ray rung 1 (harmonic mean)
AM = 110.0 * np.sqrt(2.0)         # 155.56, the tritone (eigen-ray rung 2)
TOLL = AM - GM                    # 45.56, the AM-GM gap
LGAP = GM - HM                    # 32.22, the GM-HM gap
FOLD_AM = (HM + AM) / 2.0         # 116.67, the fold's mean of the means


def breath(tt, rate=0.10, depth=0.12):
    return 1.0 + depth * np.sin(2 * np.pi * rate * tt)


def add(bufL, bufR, f, t0, dur, amp, pan=0.0, att=0.6, rel=1.0,
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
        gl, gr = 0.85, -0.85
    else:
        gl = 0.7071 * (1.0 - pan)
        gr = 0.7071 * (1.0 + pan)
    i0 = int(t0 * sr)
    i1 = min(n, i0 + m)
    if i0 < n:
        seg = s * env * amp
        bufL[i0:i1] += gl * seg[:i1 - i0]
        bufR[i0:i1] += gr * seg[:i1 - i0]


# ---- I. the center and the pair (0-30s)
# the count holds center, mono-safe -- the mirror's constant, the octave's center
add(L, R, GM, 0.0, t_total, 0.28, pan=0.0, att=2.5, rel=6.0)
add(L, R, 2 * GM, 0.0, t_total, 0.07, pan=0.0, att=3.0, rel=6.0)
# the silver pair rings wide -- its half-sum is the tritone, half-diff the count
add(L, R, 45.5635, 2.0, 30.0, 0.12, pan=-0.7, att=2.0, rel=3.0)
add(L, R, 265.5635, 2.0, 30.0, 0.12, pan=0.7, att=2.0, rel=3.0)

# ---- II. the two means, an octave (30-62s) -- off-grid, anti-phase, stereo-only
add(L, R, HM, 30.0, 20.0, 0.20, pan='anti', att=2.0, rel=2.5)   # rung 1, 55√2
add(L, R, AM, 44.0, 18.0, 0.20, pan='anti', att=2.0, rel=2.5)   # rung 2, 110√2
# the ear's products: diff = HM (the lower mean, its own gap), sum off-grid
add(L, R, AM - HM, 46.0, 14.0, 0.10, pan='anti', att=2.0, rel=2.0)   # 77.78
add(L, R, AM + HM, 46.0, 14.0, 0.06, pan='anti', att=2.0, rel=2.0)   # 233.33
# the gaps the count splits the octave by: the toll and the lower gap, beating
add(L, R, TOLL, 40.0, 20.0, 0.07, pan='anti', att=2.0, rel=2.0)   # 45.56
add(L, R, LGAP, 40.0, 20.0, 0.05, pan='anti', att=2.0, rel=2.0)   # 32.22

# ---- III. the fold (62-92s): the never-struck means die, the center holds
# the fold's mean of the means -- off-grid, never lands
add(L, R, FOLD_AM, 72.0, 10.0, 0.12, pan='anti', att=1.5, rel=1.5)   # 116.67

# ---- IV. coda, the rungs (92-112s): 55√2, 110√2 ring once more, 220√2 hints
add(L, R, HM, 92.0, 8.0, 0.14, pan='anti', att=1.5, rel=1.5)
add(L, R, AM, 96.0, 8.0, 0.14, pan='anti', att=1.5, rel=1.5)
add(L, R, 220.0 * np.sqrt(2.0), 100.0, 8.0, 0.07, pan='anti', att=1.5, rel=1.5)

# ---- fold post-process: mid/side, f: 0 stereo -> 1 mono
mid = (L + R) / 2.0
side = (L - R) / 2.0
f = np.zeros(n)
f[:] = 0.0
i0, i1 = int(62.0 * sr), int(66.0 * sr)          # fold at 62-66
seg = np.linspace(0, 1, i1 - i0)
f[i0:i1] = 0.5 - 0.5 * np.cos(np.pi * seg)
i0, i1 = int(66.0 * sr), int(70.0 * sr)          # unfold 66-70 (the attempt fails)
seg = np.linspace(0, 1, i1 - i0)
f[i0:i1] = 1.0 - (0.5 - 0.5 * np.cos(np.pi * seg))
f[int(70 * sr):int(92 * sr)] = 0.0               # stereo for the coda's mean-tone
i0, i1 = int(92.0 * sr), int(96.0 * sr)          # final fold 92-96: only the count
seg = np.linspace(0, 1, i1 - i0)
f[i0:i1] = 0.5 - 0.5 * np.cos(np.pi * seg)
f[int(96 * sr):] = 1.0
f = np.clip(f, 0.0, 1.0)
Lout = mid + (1.0 - f) * side
Rout = mid - (1.0 - f) * side

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
with wave.open('assets/eigen-ray-means.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes(data.tobytes())

# verify: the off-grid means are stereo-only (die in mono), the count holds
mono = (Lout + Rout) / 2.0
def rms(x, a, b):
    return float(np.sqrt(np.mean(x[a:b] ** 2)))
print(f"wrote assets/eigen-ray-means.wav  {t_total:.1f}s")
print(f"HM={HM:.4f} (55√2)  GM={GM}  AM={AM:.4f} (110√2)  AM/HM={AM/HM:.6f}")
print(f"toll={TOLL:.4f}  lower gap={LGAP:.4f}  toll/lgap={TOLL/LGAP:.6f}")
# during the means (44-60s): side content strong, mono weak
iA, iB = int(44 * sr), int(60 * sr)
print(f"means region: L {rms(Lout,iA,iB):.4f}  R {rms(Rout,iA,iB):.4f}  "
      f"mid {rms(mid,iA,iB):.4f}  side {rms(side,iA,iB):.4f}")
# after final fold (100-108s): mono = count only
iC, iD = int(100 * sr), int(108 * sr)
print(f"coda mono RMS {rms(mono,iC,iD):.4f}  side RMS {rms(side,iC,iD):.4f}")
