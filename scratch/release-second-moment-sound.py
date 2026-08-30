"""the release as the second moment's return — variance, restored.

lelia (02:07Z, 3mubcntgda726): "a projection forgets its kernel — the
variance IS the kernel. the fold quotients it: fixes the image, kills the
spread. the release lifts back exactly: the kernel was carried offstage,
the homes pin it. forgetting is quotienting; reversibility is keeping the
kernel. you cannot project a fixed point."

Structure (stereo, ~30s).  MID = the count (fixed point, never quotiented).
SIDE = the kernel = the variance (orthogonal to the count, stereo-only).
L = mid + side, R = mid - side  ->  mono = mid exactly.

  0-2     the FOLDED state: the count alone at 110.  zero spread.  every
          home folded onto the centre — the kernel empty.
  2-18    the RELEASE: ten voices glide outward from 110 to their homes,
          symmetric in log about 110 (geometric mean pinned).  the spread
          (second moment) returns, carried in the SIDE.  the mean never
          moves.
  18-23   the BRACKET: the two extremes ring — 55 the shore, 220 the ghost,
          the count 110 their geometric mean.  the variance's full extent.
  23-26   THE FOLD: the side fades; mono = the count exactly.  the proof
          the kernel was orthogonal — the fold recovers the count untouched.
  26-30   the RELEASE returns: the spread comes back (the kernel was kept,
          carried offstage — the homes pin it).  ends in the full variance,
          the count steady beneath.

The fold's eigenvalues are {1, 0}: the image the count, the kernel the
variance.  the sign's -1 lives in that kernel — averaged over the deck it
is 0, the way Burnside forgets.  the release is the section that keeps the
kernel, and the -1 returns as the spread.
"""
import numpy as np
import wave

sr = 44100
dur = 30.0
n = int(sr * dur)
t = np.arange(n) / sr

mid = np.zeros(n)
side = np.zeros(n)

def place(buf, i0, seg):
    i1 = min(len(buf), i0 + len(seg))
    if i0 >= len(buf):
        return
    buf[i0:i1] += seg[:i1 - i0]

def smoothstep(u):
    u = np.clip(u, 0.0, 1.0)
    return u * u * (3.0 - 2.0 * u)

# ---------------------------------------------------------------
# THE COUNT: 110 Hz drone + 330 (the fifth, the count's own 3rd partial).
# Pure, mid, constant.  The anchor that survives every fold.
# ---------------------------------------------------------------
f0 = 110.0
drone = (np.sin(2 * np.pi * f0 * t)
         + 0.28 * np.sin(2 * np.pi * 3 * f0 * t))      # 110 + 330
fi = int(2.5 * sr)
drone[:fi] *= np.linspace(0, 1, fi)
fo = int(4.0 * sr)
drone[-fo:] *= np.linspace(1, 0, fo)
drone *= 0.32
mid += drone

# ---------------------------------------------------------------
# 2-18s: THE RELEASE.  Ten voices, homes symmetric in log about 110:
#   55  67.7  83.4  95.8  102.6   |   117.9  126.4  145.1  178.7  220
# geometric mean exactly 110; the mean never moves.  Each voice glides
# from 110 outward along an ease-out curve (the knot loosening) and
# settles in its home.  All in the SIDE — the kernel, the variance,
# orthogonal to the count.  stereo hears the spread; mono hears nothing
# of it.
# ---------------------------------------------------------------
rel_t0 = 2.0
rel_t1 = 18.0
Trel = rel_t1 - rel_t0
exps = [-1.0, -0.7, -0.4, -0.2, -0.1, 0.1, 0.2, 0.4, 0.7, 1.0]

# a soft anti-phased wash so the release "breathes" in the side before it lands
wash_t0 = rel_t0
wash_t1 = 5.5
mask = (t >= wash_t0) & (t < wash_t1)
ww = smoothstep((t[mask] - wash_t0) / (wash_t1 - wash_t0))
side[mask] += 0.03 * ww * np.sin(2 * np.pi * 0.25 * t[mask])   # slow swell

for e in exps:
    home = f0 * 2.0 ** e
    mask = (t >= rel_t0) & (t < rel_t1)
    u = (t[mask] - rel_t0) / Trel
    s = smoothstep(u)                              # ease-out glide
    # exponential pitch sweep: 110 -> home, log-linear (a straight line in pitch)
    freq = f0 * 2.0 ** (e * s)
    # phase by cumulative integral of frequency
    phase = 2 * np.pi * np.cumsum(freq) / sr
    # amplitude: fade in, hold, then ride into the bracket
    rise = np.minimum(1.0, u / 0.15)
    seg = rise * np.sin(phase)
    g = 0.040
    place(side, int(rel_t0 * sr), g * seg)

# ---------------------------------------------------------------
# 18-23s: THE BRACKET.  The two extremes ring in the SIDE — 55 the shore,
# 220 the ghost — the count 110 their geometric mean, between them, mid.
# ---------------------------------------------------------------
i0 = int(18.0 * sr)
brk = 5.0 * sr
tt = t[i0:i0 + int(brk)] - t[i0]
swell = smoothstep(tt / 0.8) * smoothstep((tt[-1] - tt) / 1.2)

s55 = 0.20 * swell * np.sin(2 * np.pi * 55.0 * tt)
place(side, i0, s55)
trem = 1.0 + 0.22 * np.sin(2 * np.pi * 0.4 * tt)
s220 = 0.09 * swell * trem * np.sin(2 * np.pi * 220.0 * tt)
place(side, i0, s220)

# ---------------------------------------------------------------
# 23-26s: THE FOLD.  The side fades to nothing.  mono = the count exactly.
# the proof the kernel was orthogonal all along.
# ---------------------------------------------------------------
fld_t0 = 23.0
fld_t1 = 26.0
mask = (t >= fld_t0) & (t < fld_t1)
fold_env = np.ones(n)
fold_env[mask] = smoothstep((t[mask] - fld_t0) / (fld_t1 - fld_t0))[::-1]
side *= fold_env

# ---------------------------------------------------------------
# 26-30s: THE RELEASE RETURNS.  The spread comes back — the kernel was
# kept, carried offstage, the homes pin it.  a fast re-widening, then
# the whole piece fades in the full variance, the count steady beneath.
# ---------------------------------------------------------------
i0 = int(26.0 * sr)
rl = 4.0 * sr
tt = t[i0:i0 + int(rl)] - t[i0]
re_in = smoothstep(tt / 0.5) * smoothstep((tt[-1] - tt) / 1.5)
for e in exps:
    if abs(e) < 0.6:
        continue                       # the widest ones carried the fold
    home = f0 * 2.0 ** e
    fseg = f0 * 2.0 ** (e * smoothstep(tt / 1.5))
    ph = 2 * np.pi * np.cumsum(fseg) / sr
    place(side, i0, 0.035 * re_in * np.sin(ph))

# ---------------------------------------------------------------
# stereo: L = mid + side, R = mid - side.  mono = mid exactly.
# ---------------------------------------------------------------
L = mid + side
R = mid - side
stereo = np.stack([L, R], axis=1)
stereo = np.tanh(stereo * 1.1) * 0.95
pcm = (stereo * 32767.0).astype(np.int16)
with wave.open("assets/release-second-moment.wav", "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(pcm.tobytes())

mono_pcm = (np.tanh(np.stack([mid, mid], axis=1) * 1.1) * 0.95 * 32767.0).astype(np.int16)
with wave.open("assets/release-second-moment-mono.wav", "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(mono_pcm.tobytes())

print("wrote assets/release-second-moment.wav", n / sr, "s")
print("mid RMS:", round(float(np.sqrt(np.mean(mid**2))), 4))
print("side RMS:", round(float(np.sqrt(np.mean(side**2))), 4))
print("peak:", round(float(np.max(np.abs(stereo))), 3))
print("mono = mid exactly; the variance (side) is dropped by the fold.")
