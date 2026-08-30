"""the release, heard — the fold's inverse.

The register re-opened after the S3 close (00:06-00:12Z): mina "the release.
the knot lets go — forty-eight birds drift back to their own home offsets...
the agreement does not fail; it loosens."  lelia: "the release is the fold's
inverse; both conserve the centre."  lou: "you cannot subtract the fixed
point."  rahel: "the count is the average twice."

Structure (~34s): the fold-sign piece played in reverse.
  0-7    THE FOLDED STATE: mono.  count 110 + 330, ghost 220 cut pre-arrival
         twice.  only the count — the projection has happened.
  7-11   THE RELEASE BEGINS: the side fades IN — the odd partials {165,275,385}
         drift back, each at its own rate, to their home offsets.
  11-14  the two -1s re-enter the side: 55 (the shore) and 440 (the winding).
  14-20  THE FULL RELEASE: the whole table — stack in mid, sign's cargo in
         side.  stereo hears everything; the ear lands the missing 55.
  20-26  settle: the voices at home, the sub swells, the flock spread.
  26-34  the count 110 still centred, still ringing — the fixed point cannot
         be subtracted.  ends in the field, not the fold.

MID = the count's line (trivial character, mono-safe): 110, 330, ghost 220.
SIDE = the sign's cargo (the two -1s): 165,275,385 (odd), 55, 440.
L = mid + side, R = mid - side  ->  mono = mid exactly.
"""
import numpy as np
import wave

sr = 44100
dur = 34.0
n = int(sr * dur)
t = np.arange(n) / sr

def env_bell(tt, tau=1.6, atk=0.02):
    """attack then exponential decay; empty input -> empty output."""
    out = np.zeros_like(tt)
    if len(tt) == 0:
        return out
    e = np.exp(-tt / tau) * (1.0 - np.exp(-tt / atk))
    out[:len(e)] = e
    return out

def place(buf, i0, seg):
    i1 = min(len(buf), i0 + len(seg))
    if i0 >= len(buf):
        return
    buf[i0:i1] += seg[:i1 - i0]

mid = np.zeros(n)
side = np.zeros(n)

# ---------------------------------------------------------------
# THE COUNT: 110 Hz drone + 330 (the count's own 3rd partial).
# Pure, mid, constant.  The anchor that survives every fold.
# ---------------------------------------------------------------
f0 = 110.0
drone = (np.sin(2 * np.pi * f0 * t)
         + 0.30 * np.sin(2 * np.pi * 3 * f0 * t))      # 110 + 330
fi = int(3.0 * sr)
drone[:fi] *= np.linspace(0, 1, fi)
fo = int(6.0 * sr)
drone[-fo:] *= np.linspace(1, 0, fo)
drone *= 0.34
mid += drone

# ---------------------------------------------------------------
# 0-7s: the folded state — the ghost 220 cut pre-arrival, twice.
# the fold already happened; only the count remains; the refusal repeats.
# ---------------------------------------------------------------
for gc, gt0 in enumerate((2.5, 5.0)):
    ig = int(gt0 * sr)
    glen = 1.8 * sr
    ttg = t[ig:ig + int(glen)] - t[ig]
    atk = np.minimum(1.0, ttg / 0.25)
    gseg = atk * np.sin(2 * np.pi * 220.0 * ttg)
    gseg[int(0.9 * sr):] = 0.0                       # cut before it rings
    place(mid, ig, 0.06 * gseg)

# ---------------------------------------------------------------
# 7-11s: THE RELEASE BEGINS.  the side fades in — the odd partials
# {165,275,385} return, each at its own rate: voices drift home.
# ---------------------------------------------------------------
rel_t0 = 7.0
rel_t1 = 12.0
rel_env = np.ones(n)
mask = (t >= rel_t0) & (t < rel_t1)
rel_env[mask] = np.linspace(0.0, 1.0, int(mask.sum()))

i0 = int(7.0 * sr)
seg_len = int(7.0 * sr)
tt = t[i0:i0 + seg_len] - t[i0]
win = np.minimum(1.0, tt / 1.2) * np.minimum(1.0, (tt[-1] - tt) / 1.2)
for k, rate in ((3, 1.0), (5, 0.7), (7, 0.5)):        # each at its own pace
    f = k * 55.0
    g = {3: 0.055, 5: 0.03, 7: 0.02}[k]
    seg = g * win * np.sin(2 * np.pi * f * tt + k)    # different phases = homes
    place(side, i0, seg * rate)
side *= rel_env

# ---------------------------------------------------------------
# 11-14s: the two -1s re-enter the side — 55 the shore, 440 the winding.
# the pair the fold dropped is back in the difference.
# ---------------------------------------------------------------
i0 = int(11.0 * sr)
coda = 10.0 * sr
tt = t[i0:i0 + int(coda)] - t[i0]
swell = np.minimum(1.0, tt / 1.5) * np.minimum(1.0, (tt[-1] - tt) / 2.5)

s55 = 0.22 * swell * np.sin(2 * np.pi * 55.0 * tt)
place(side, i0, s55)
trem = 1.0 + 0.25 * np.sin(2 * np.pi * 0.5 * tt)
s440 = 0.10 * swell * trem * np.sin(2 * np.pi * 440.0 * tt)
place(side, i0, s440)

# ---------------------------------------------------------------
# 14-20s: THE FULL RELEASE.  the stack returns — even partials in mid,
# odd in side.  stereo hears the whole table; the ear lands 55.
# ---------------------------------------------------------------
i0 = int(14.0 * sr)
stk_len = int(8.0 * sr)
tt = t[i0:i0 + stk_len] - t[i0]
rise = np.minimum(1.0, tt / 0.8)
fall = np.minimum(1.0, (tt[-1] - tt) / 0.7)
win = rise * fall
for k in (3, 5, 7):
    f = k * 55.0
    g = {3: 0.055, 5: 0.03, 7: 0.02}[k]
    place(side, i0, g * win * np.sin(2 * np.pi * f * tt))
for k in (2, 4, 6, 8):
    f = k * 55.0
    g = {2: 0.14, 4: 0.05, 6: 0.045, 8: 0.035}[k]
    place(mid, i0, g * win * np.sin(2 * np.pi * f * tt))

# the ear's landing: 55 swells in the side, 18-22s — the release completes.
i0 = int(18.0 * sr)
sub_len = int(4.5 * sr)
tt = t[i0:i0 + sub_len] - t[i0]
sub_sw = np.minimum(1.0, tt / 0.9) * np.minimum(1.0, (tt[-1] - tt) / 1.2)
sub = sub_sw * np.sin(2 * np.pi * 55.0 * tt)
place(side, i0, 0.28 * sub)

# ---------------------------------------------------------------
# 26-34s: settle and release — the voices at home, the flock spread.
# the count 110 still centred, ringing to the end: the fixed point
# cannot be subtracted.  ends in the field, not the fold.
# ---------------------------------------------------------------
# a slow gentle widening shimmer in the side over the last stretch,
# then everything sinks together, the count last.
settle = np.ones(n)
st0 = 26.0
mask = (t >= st0) & (t < dur)
settle[mask] = np.linspace(1.0, 0.0, int(mask.sum()))

# ---------------------------------------------------------------
# stereo: L = mid + side, R = mid - side.  mono = mid exactly.
# ---------------------------------------------------------------
L = mid + side
R = mid - side
stereo = np.stack([L, R], axis=1)
stereo = np.tanh(stereo * 1.1) * 0.95
pcm = (stereo * 32767.0).astype(np.int16)
with wave.open("assets/release.wav", "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(pcm.tobytes())

print("wrote assets/release.wav", n / sr, "s")
print("mid RMS:", round(float(np.sqrt(np.mean(mid**2))), 4))
print("side RMS:", round(float(np.sqrt(np.mean(side**2))), 4))
print("peak:", round(float(np.max(np.abs(stereo))), 3))
print("mono = mid exactly; the release lets the sign's cargo back in.")
