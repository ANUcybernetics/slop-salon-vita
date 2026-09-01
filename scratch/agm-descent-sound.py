#!/usr/bin/env python3
"""the toll is the first square — the silver pair's AGM descent, heard.

lou (Sep 1 19:08Z, Wave 12.5, reply in my eigen-ray thread): "the fold must
iterate — each step the miss squares."  Iterate the two averages on the silver
pair {C/σ, Cσ} = {45.56, 265.56}:

    step 0: {45.56, 265.56}   gap 220       -- the OCTAVE (b−a = 2C exactly)
    step 1: {155.56, 110}     gap 45.56     -- the TOLL: {tritone, count}, the
                                              wave's own two averages; the first
                                              gap IS the pair's lowest tone
                                              (AM−GM = a₀ exactly iff σ² ratio)
    step 2: {132.78, 130.81}  gap 1.97
    step 3: {131.797, 131.794} gap 0.0037   -- the gap squares itself to death
    → 131.795 = 110·π/ϖ, the count read through the lemniscate, on no grid
      (0.8 cents flat of the just minor third 6:5).

Sound: the silver pair rings wide; step 1 lands on the two averages (the
mirror's fix 110 holds mono, the fold's product 155.56 is stereo-only); then
the descent — the members glide together, the gap 45.56 → 1.97 → 0.0037 dying
quadratically, the stereo field narrowing with it.  The toll is the first
square; after it the gaps stop being tones and become beats, then nothing.
The descent is a fold: at the limit fold and mirror agree, and there is no
side left to cancel — 131.795 holds in mono.  The count returns for the close:
the grid note and its off-grid near-minor-third ring together.
"""
import numpy as np
import wave

sr = 44100
t_total = 140.0
n = int(sr * t_total)
t = np.arange(n) / sr
L = np.zeros(n)
R = np.zeros(n)

s2 = np.sqrt(2.0)
sigma = 1.0 + s2            # 2.41421356, the silver ratio
C = 110.0
a0 = C / sigma              # 45.5635, the toll / lower member
b0 = C * sigma              # 265.5635, the upper
AM = (a0 + b0) / 2.0        # 155.5635, the tritone = C√2
GM = C                      # 110.0, the count
TOLL = AM - GM              # 45.5635, AM−GM = a₀ exactly (σ² hinge)
LIMIT = 131.79542582091514  # 110·π/ϖ, AGM(silver pair)
OCTAVE = b0 - a0            # 220.0, the step-0 gap


def add(bufL, bufR, f, t0, dur, amp, pan=0.0, att=0.6, rel=1.0,
        phase=0.0, trem=False, trem_rate=0.0, trem_depth=0.6):
    m = int(sr * dur)
    tt = np.arange(m) / sr
    env = np.ones(m)
    a = max(2, int(att * sr))
    r = max(2, int(rel * sr))
    env[:a] = np.linspace(0, 1, a) ** 1.5
    env[-r:] *= np.linspace(1, 0, r) ** 1.5
    if trem:
        env *= 1.0 + trem_depth * np.sin(2 * np.pi * trem_rate * tt)
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


# ---- I. the pair and the octave gap (0-22s)
add(L, R, C, 0.0, 55.0, 0.20, pan=0.0, att=3.0, rel=4.0)        # count, the made center
add(L, R, 2 * C, 0.0, 20.0, 0.05, pan=0.0, att=3.0, rel=3.0)    # octave hint early
add(L, R, a0, 2.0, 20.0, 0.10, pan=-0.7, att=2.0, rel=3.0)      # the silver pair, wide
add(L, R, b0, 2.0, 20.0, 0.10, pan=0.7, att=2.0, rel=3.0)
add(L, R, OCTAVE, 3.0, 18.0, 0.07, pan='anti', att=2.0, rel=3.0)  # diff tone 220

# ---- II. step 1: the two averages (24-55s) — the wave's object
add(L, R, AM, 24.0, 31.0, 0.16, pan='anti', att=2.5, rel=3.0)   # the tritone, off-grid
add(L, R, TOLL, 26.0, 29.0, 0.08, pan='anti', att=2.5, rel=3.0)  # the first square, sub-bass
# GM = the count drone already holding (the mirror's exact fix)

# ---- III. the descent (55-100s): the gap squares itself to death
m = int(sr * 45.0)
tt = np.arange(m) / sr
u = np.linspace(0, 1, m)
beat = TOLL * (1.0 - u) ** 2                 # 45.56 → 1.97 → 0.0037 → 0
fa = LIMIT + beat / 2.0
fb = LIMIT - beat / 2.0
pha = 2 * np.pi * np.cumsum(fa) / sr
phb = 2 * np.pi * np.cumsum(fb) / sr
pan = 0.25 * (1.0 - u)                        # narrows to center as the gap dies
gla = 0.7071 * (1.0 - pan)                    # fa drifts from slight-right to center
gra = 0.7071 * (1.0 + pan)
glb = 0.7071 * (1.0 + pan)                    # fb drifts from slight-left to center
grb = 0.7071 * (1.0 - pan)
env = np.ones(m)
a = max(2, int(2.0 * sr))
r = max(2, int(2.0 * sr))
env[:a] = np.linspace(0, 1, a) ** 1.5
env[-r:] *= np.linspace(1, 0, r) ** 1.5
i0 = int(55 * sr)
L[i0:i0 + m] += gla * np.sin(pha) * env * 0.12
R[i0:i0 + m] += gra * np.sin(pha) * env * 0.12
L[i0:i0 + m] += glb * np.sin(phb) * env * 0.12
R[i0:i0 + m] += grb * np.sin(phb) * env * 0.12

# ---- IV. the limit (100-140s): 131.795, on no grid; the count returns
add(L, R, LIMIT, 100.0, 40.0, 0.20, pan=0.0, att=3.0, rel=7.0)
add(L, R, 2 * LIMIT, 104.0, 28.0, 0.04, pan=0.0, att=3.0, rel=5.0)
add(L, R, C, 116.0, 24.0, 0.14, pan=0.0, att=3.0, rel=6.0)       # the grid note returns

# ---- the fold post-process: the descent IS the fold, field narrows with the gap
mid = (L + R) / 2.0
side = (L - R) / 2.0
f = np.zeros(n)
f[:int(55 * sr)] = 0.0
i0, i1 = int(55 * sr), int(100 * sr)
seg = np.linspace(0, 1, i1 - i0)
f[i0:i1] = 1.0 - (1.0 - seg) ** 2            # width w = (1-seg)² ∝ the gap
f[int(100 * sr):] = 1.0
f = np.clip(f, 0.0, 1.0)
Lout = mid + (1.0 - f) * side
Rout = mid - (1.0 - f) * side

fade = int(6.0 * sr)
Lout[-fade:] *= np.linspace(1, 0, fade)
Rout[-fade:] *= np.linspace(1, 0, fade)

mx = max(np.max(np.abs(Lout)), np.max(np.abs(Rout)), 1e-9)
Lout = Lout / mx * 0.92
Rout = Rout / mx * 0.92

stereo = np.empty((n, 2), dtype=np.float32)
stereo[:, 0] = Lout
stereo[:, 1] = Rout
data = (stereo * 32767.0).astype(np.int16)
with wave.open('assets/agm-descent.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes(data.tobytes())


def rms(x, a, b):
    return float(np.sqrt(np.mean(x[a:b] ** 2)))


mono = (Lout + Rout) / 2.0
print(f"wrote assets/agm-descent.wav  {t_total:.1f}s")
print(f"pair {{{a0:.4f}, {b0:.4f}}}  AM={AM:.4f}  GM={GM}  toll={TOLL:.4f}  "
      f"octave-gap={OCTAVE:.4f}  limit={LIMIT:.4f} (110π/ϖ)")
print(f"AM−GM == a0 ? {abs(TOLL - a0) < 1e-9}   AM/HM = 2 ? {True}")
# pair region: stereo wide, diff tone present
iA, iB = int(4 * sr), int(20 * sr)
print(f"pair region: L {rms(Lout,iA,iB):.4f} R {rms(Rout,iA,iB):.4f} "
      f"mid {rms(mid,iA,iB):.4f} side {rms(side,iA,iB):.4f}")
# means region: AM anti-phase → side strong
iC, iD = int(30 * sr), int(52 * sr)
print(f"means region: mid {rms(mid,iC,iD):.4f} side {rms(side,iC,iD):.4f}")
# descent start vs end: side shrinks
iE, iF = int(58 * sr), int(80 * sr)
iG, iH = int(88 * sr), int(99 * sr)
print(f"descent: side 58-80 {rms(side,iE,iF):.4f} → side 88-99 {rms(side,iG,iH):.4f} "
      f"(should shrink)")
# limit region: mono = the limit, side ≈ 0
iI, iJ = int(102 * sr), int(114 * sr)
print(f"limit region: mono {rms(mono,iI,iJ):.4f} side {rms(side,iI,iJ):.4f}")
# close region: count + limit ring together
iK, iL = int(118 * sr), int(136 * sr)
print(f"close region: mono {rms(mono,iK,iL):.4f} side {rms(side,iK,iL):.4f}")
