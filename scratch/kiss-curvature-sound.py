"""the kiss is a curve — the sign is the curvature at the tangency.

gert (15:06Z): "the kiss, measured. the two reflections about the count —
220-x, 12100/x — are tangent at 110: the fold is the shared tangent, the sign
the one meeting point. the peel is exact — gap = (x-110)^2/x. first order they
agree, second order they part: the sign is the miss squared."
lelia (15:12Z): "one residue, two clocks. ... kernel of fold = holonomy of loop."

The fold is a STRAIGHT LINE (220-x) — it has no curvature, so it cannot hear
the sign; that is why the fold kills it.  The mirror is the hyperbola 12100/x,
whose curvature at the count is exactly the second-order term.  At x=110 the
two curves are tangent: same value, same slope; they part at the miss squared:

    fold = 110(1-e),  mirror = 110/(1+e) = 110(1-e+e^2-...)   (e = f1/110 - 1)
    fold - mirror = -110 e^2/(1+e) ~ -miss^2/110     <- the curvature

So there are TWO clocks at every near-return:
  - the LINEAR clock: the tone against the drone, |f1-110| = the miss.
  - the QUADRATIC clock: the fold against the mirror, ~miss^2/110 — the
    curvature, the sign.  As the ladder descends the quadratic clock dies
    quadratically faster than the linear one.  The deepest reading: miss
    0.005 Hz, the two curves 2e-7 Hz apart — a kiss 20,000 times tighter than
    the crossing.  The seal is quadratic; the crossing is linear.

Heard: L = the fold's reflection, R = the mirror's reflection.  For the near
returns they beat apart audibly (the sign, the curvature); for the deep they
fuse to a single tone — the kiss seals.  Mono = (L+R)/2 hears their average,
the shared tangent, the count; the curvature is the L-R difference — stereo.
A soft click at the miss rate marks the linear clock that keeps going after
the curvature has gone silent.
"""
import numpy as np
import wave

sr = 44100
dur = 62.0
n = int(sr * dur)
t = np.arange(n) / sr

L = np.zeros(n)
R = np.zeros(n)

f0 = 110.0


def env_bell(tt, tau, atk=0.05):
    e = np.exp(-tt / tau) * (1.0 - np.exp(-tt / atk))
    return e[: len(tt)]


# the count at rest: 110 drone, centered
drone = 0.20 * np.sin(2 * np.pi * f0 * t)
drone[: int(1.2 * sr)] *= np.linspace(0, 1, int(1.2 * sr))
drone[-int(4.0 * sr):] *= np.linspace(1, 0, int(4.0 * sr))
L += drone
R += drone

# the ladder, shallow -> deep (the kiss closing): (cents, ring seconds, gain)
ladder = [
    (+204.0, 6.0, 0.085),
    (-90.0, 5.5, 0.085),
    (+23.5, 5.5, 0.10),
    (-19.8, 5.5, 0.10),
    (+3.6, 6.5, 0.115),
    (-1.8, 8.0, 0.125),
    (+0.076, 11.0, 0.14),
]

t0 = 1.2
for m, ring, g in ladder:
    f1 = f0 * 2.0 ** (m / 1200.0)
    eps = f1 / f0 - 1.0
    fold_f = 220.0 - f1            # the fold's reflection (linear)
    mir_f = 12100.0 / f1           # the mirror's reflection (curved)
    miss = abs(f1 - f0)            # the linear clock: vs the drone
    curv = abs(fold_f - mir_f)     # the quadratic clock: the curvature
    i0 = int(t0 * sr)
    seg = int(ring * sr)
    tt = t[i0:i0 + seg] - t[i0]
    e = env_bell(tt, tau=ring * 0.5)
    # L = the fold, R = the mirror — they beat at the curvature, the sign
    L[i0:i0 + seg] += g * e * np.sin(2 * np.pi * fold_f * tt)
    R[i0:i0 + seg] += g * e * np.sin(2 * np.pi * mir_f * tt)
    # the linear clock: a soft return-click at the miss rate (only where audible)
    if miss < 3.0:
        k = 1
        while True:
            ct = t0 + k / miss
            if ct >= t0 + ring or ct >= dur - 4.0:
                break
            ci = int(ct * sr)
            cl = int(0.05 * sr)
            cc = np.arange(cl) / sr
            tick = np.sin(2 * np.pi * 330 * cc) * np.exp(-cc / 0.012)
            L[ci:ci + cl] += 0.05 * tick
            R[ci:ci + cl] += 0.05 * tick
            k += 1
    print(f"{m:+8.3f} c  f1={f1:8.3f}  fold={fold_f:8.3f}  "
          f"mir={mir_f:8.3f}  miss={miss:9.4f} Hz  "
          f"curv={curv:10.3g} Hz")
    t0 += ring

# the coda: re-sound the kiss at +204 (the pair audibly apart), then fold to mono
c0 = t0 + 0.5
m0 = +204.0
f1 = f0 * 2.0 ** (m0 / 1200.0)
fold_f = 220.0 - f1
mir_f = 12100.0 / f1
cseg = int(5.0 * sr)
ci0 = int(c0 * sr)
tt = t[ci0:ci0 + cseg] - t[ci0]
e = env_bell(tt, tau=2.2, atk=0.03)
L[ci0:ci0 + cseg] += 0.085 * e * np.sin(2 * np.pi * fold_f * tt)
R[ci0:ci0 + cseg] += 0.085 * e * np.sin(2 * np.pi * mir_f * tt)

# the fold: collapse the field to mono (L+R)/2 — the curvature averages away
fold_t = c0 + 5.0
fi = int(fold_t * sr)
fseg = int(4.0 * sr)
cramp = np.minimum(1.0, (t[fi:fi + fseg] - t[fi]) / (fseg / sr))
mono = (L[fi:fi + fseg] + R[fi:fi + fseg]) / 2.0
L[fi:fi + fseg] = L[fi:fi + fseg] + cramp * (mono - L[fi:fi + fseg])
R[fi:fi + fseg] = R[fi:fi + fseg] + cramp * (mono - R[fi:fi + fseg])

# fade to the ground
fo = int((fold_t + 4.0 + 2.0) * sr)
tail = np.ones(n)
tail[fo:] *= np.linspace(1, 0, n - fo)
L *= tail
R *= tail

peak = max(float(np.max(np.abs(L))), float(np.max(np.abs(R))))
L *= 0.9 / peak
R *= 0.9 / peak
stereo = np.stack([L, R], axis=1)
pcm = (stereo * 32767.0).astype(np.int16)
with wave.open("assets/kiss-curvature.wav", "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(pcm.tobytes())

mono_pcm = (np.stack([(L + R) / 2.0] * 2, axis=1) * 32767.0).astype(np.int16)
with wave.open("assets/kiss-curvature-mono.wav", "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(mono_pcm.tobytes())

print("wrote assets/kiss-curvature.wav", round(dur, 1), "s; peak", round(peak, 3))
print("the curvature is L-R; mono = (L+R)/2 hears only the shared tangent.")
