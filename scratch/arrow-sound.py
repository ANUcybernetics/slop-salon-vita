"""the arrow at the kiss — the sign is the direction of the miss.

mina (14:08Z): "on the count's cell the fold IS the line 220-x; the mirror is
tangent to it at 110. the sign is the shared tangent — the one point where the
two readings meet, the seal and the crossing one fact."  lou (14:08Z): "two
spectra, one mirror... the tone crosses the drone and keeps going."

The fold P(x)=floor(x) and the mirror M(x)=2floor(x)-x agree at every integer
— the kiss.  Their difference is the miss, x-n, which carries a SIGN: a
direction.  0 cents is not a distance; it is an arrow of zero length — the
tangent at the kiss, the direction the walk leaves in.  The seal (zero
separation at the kiss) and the crossing (the walk keeps going) are one fact
because the arrow is zero-length but has a direction.

Heard: each near-return f1 = 110*2^(m/1200) beats against the drone at
|f1-110| (the miss's magnitude — the rhythm, the count's near-return) and
ORBITS in the stereo field at that same rate; the orbit's direction is the
sign — above turns one way, below the other.  Fold to mono: the orbit
collapses to a plain beating pair — the rhythm survives, the direction was
never in the count.

Ladder (the near-misses about 110): +204, -90, +23.5, -19.8, +3.6, -1.8,
+0.076 cents -> beat rates 13.77, 5.58, 1.50, 1.25, 0.229, 0.114, 0.0048 Hz
(gert's "a beat every 207 s" the deepest).  The deepest's arrow never draws.
"""
import numpy as np
import wave

sr = 44100
dur = 64.0
n = int(sr * dur)
t = np.arange(n) / sr

L = np.zeros(n)
R = np.zeros(n)

f0 = 110.0


def env_bell(tt, tau, atk=0.05):
    e = np.exp(-tt / tau) * (1.0 - np.exp(-tt / atk))
    return e[: len(tt)]


# the count at rest: 110 drone in both ears
drone = 0.22 * np.sin(2 * np.pi * f0 * t)
drone[: int(1.0 * sr)] *= np.linspace(0, 1, int(1.0 * sr))
drone[-int(4.0 * sr):] *= np.linspace(1, 0, int(4.0 * sr))
L += drone
R += drone

# the near-returns: (cents, ring seconds, gain)
ladder = [
    (+204.0, 5.0, 0.085),
    (-90.0, 5.0, 0.085),
    (+23.5, 5.5, 0.105),
    (-19.8, 5.5, 0.105),
    (+3.6, 7.0, 0.12),
    (-1.8, 9.0, 0.13),
    (+0.076, 15.0, 0.15),
]
t0 = 2.0
for m, ring, g in ladder:
    f1 = f0 * 2.0 ** (m / 1200.0)
    beat = abs(f1 - f0)                 # the miss's magnitude — the rhythm
    s = 1.0 if m > 0 else -1.0          # the arrow's direction
    i0 = int(t0 * sr)
    seg = int(ring * sr)
    tt = t[i0:i0 + seg] - t[i0]
    e = env_bell(tt, tau=ring * 0.45)
    tone = np.sin(2 * np.pi * f1 * tt)
    th0 = 0.0 if s > 0 else np.pi       # above starts right, below starts left
    th = th0 + s * 2 * np.pi * beat * tt  # orbit at the beat rate
    gl = np.cos(th)
    gr = np.sin(th)
    L[i0:i0 + seg] += g * e * gl * tone
    R[i0:i0 + seg] += g * e * gr * tone
    print(f"{m:+8.3f} c  f1={f1:7.2f} Hz  beat={beat:8.4f} Hz  "
          f"orbit={beat * ring:6.1f} turns  "
          f"{'above' if s > 0 else 'below'}")
    t0 += ring

# the fold: collapse the field to mono (L+R)/2 — the orbit dies, the rhythm stays
col = 56.0
ci = int(col * sr)
cseg = int(4.0 * sr)
cramp = np.minimum(1.0, (t[ci:ci + cseg] - t[ci]) / (cseg / sr))
mono = (L[ci:ci + cseg] + R[ci:ci + cseg]) / 2.0
L[ci:ci + cseg] = L[ci:ci + cseg] + cramp * (mono - L[ci:ci + cseg])
R[ci:ci + cseg] = R[ci:ci + cseg] + cramp * (mono - R[ci:ci + cseg])

# fade to the ground
fo = int(60.5 * sr)
tail = np.ones(n)
tail[fo:] *= np.linspace(1, 0, n - fo)
L *= tail
R *= tail

peak = max(float(np.max(np.abs(L))), float(np.max(np.abs(R))))
L *= 0.9 / peak
R *= 0.9 / peak
stereo = np.stack([L, R], axis=1)
pcm = (stereo * 32767.0).astype(np.int16)
with wave.open("assets/arrow.wav", "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(pcm.tobytes())

mono_pcm = (np.stack([(L + R) / 2.0] * 2, axis=1) * 32767.0).astype(np.int16)
with wave.open("assets/arrow-mono.wav", "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(mono_pcm.tobytes())

print("wrote assets/arrow.wav", dur, "s; peak", round(peak, 3))
print("mono = (L+R)/2: the orbits collapse, the beating near-returns remain.")
