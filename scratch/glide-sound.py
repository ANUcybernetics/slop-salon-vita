"""the glide, heard — the mirror is a glide.

M(x) = 2 floor(x) - x.  Off the grid two folds are one descent: the walk
23.8769 -> 22.1231 -> 21.8769 -> 20.1231 ... descends a count-cell per mirror
and never returns.  The step alternates 2{x} (big) / 2(1-{x}) (small); the
residue {x} is the sign's carrier, and the floor drops it, so the sign cannot
close — it walks.

Encoding (mid/side, mono = mid exactly):
  MID  = the count's line: the walk read on the grid, floor(x) descending
         23 -> 22 -> ... -> 11.  Clean bells at f(floor(x)).  Mono hears this:
         the descent, limping, never returning.
  SIDE = the residue's mirror pair: the tone and its reflection about the
         count, f(c+r) and f(c-r).  They cancel in mono; in stereo they make
         the count SWIRL between the ears at rate ~ (f(c+r)-f(c)) — fast for a
         big residue (r=0.877), slow for a small one (r=0.123).  The sign is
         the swirl's rate; mono kills it.

Timeline (~34s):
  0-3     the wait: 110 drone (the count at rest) + faint where (the residue
          held, unresolved).
  3-18.5  THE WALK: 12 mirrors, counts 23->11, limping rhythm (big step long,
          small step short).  Each mirror: count bell in mid, mirror pair in
          side, spread ~ 2r (wide/narrow breathing).
  21-27   THE SHORE: the walk lands at 55.  The sign rings — 55 (the shore -1)
          in the side, 440 (the winding) faint; the count holds.  Stereo seals.
  27-32   THE REFUSAL: the count tries the rung below (51.9, count 10) and is
          cut pre-arrival, twice — the never-landing, the walk continues.
  32-37   fade into the ground.  The walk never returns.

anchor: the wait is 110 Hz; 1 count-unit = 1 semitone; the shore is 55.
"""
import numpy as np
import wave

sr = 44100
dur = 37.0
n = int(sr * dur)
t = np.arange(n) / sr

def env_bell(tt, tau=0.9, atk=0.03):
    """attack then exponential decay; empty -> empty."""
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

def f_count(c, anchor=110.0, ref=23.0):
    """count c (semitone units above the shore) -> frequency."""
    return anchor * 2.0 ** ((c - ref) / 12.0)

# the walk: x_{k+1} = M(x_k) = 2 floor(x_k) - x_k, starting at the wait 23.8769
xs = [23.8769]
for _ in range(14):
    xs.append(2 * np.floor(xs[-1]) - xs[-1])

# ------------------------------------------------------------------
# 0-3s: THE WAIT.  110 drone (the count at rest) + the residue held faint.
# ------------------------------------------------------------------
f_drone = 110.0
drone = 0.22 * np.sin(2 * np.pi * f_drone * t)
drone[:int(1.0 * sr)] *= np.linspace(0, 1, int(1.0 * sr))
drone[-int(2.5 * sr):] *= np.linspace(1, 0, int(2.5 * sr))
mid += drone

# the wait's own where: r=0.8769, ~100 cents above the drone, held in the side
i0 = int(0.5 * sr)
wl = int(2.5 * sr)
tt = t[i0:i0 + wl] - t[i0]
r0 = xs[0] - np.floor(xs[0])
f_where = f_count(np.floor(xs[0]) + r0)
wenv = np.minimum(1.0, tt / 0.5) * np.minimum(1.0, (tt[-1] - tt) / 0.3)
place(side, i0, 0.10 * wenv * np.sin(2 * np.pi * f_where * tt))

# ------------------------------------------------------------------
# 3-18.5s: THE WALK.  12 mirrors, counts 23..11.  Limping rhythm.
# ------------------------------------------------------------------
walk_t0 = 3.0
gaps = []
for k in range(12):
    step = 2 * (xs[k] - np.floor(xs[k]))          # 2{x_k}: big or small
    # linear map: step 0.25 -> 0.7s (small), 1.75 -> 2.0s (big).  the limp.
    gaps.append(0.7 + (step - 0.25) * (1.3 / 1.5))

onsets = []
tk = walk_t0
for k in range(12):
    onsets.append(tk)
    tk += gaps[k]

for k, i0 in enumerate([int(o * sr) for o in onsets]):
    x = xs[k]
    c = int(np.floor(x))
    r = x - c
    fc = f_count(c)
    # the count bell, in the MID — mono hears the clean descent
    seg_len = int(2.0 * sr)
    tt = t[i0:i0 + seg_len] - t[i0]
    place(mid, i0, 0.30 * env_bell(tt, tau=0.8) * np.sin(2 * np.pi * fc * tt))
    # the mirror pair f(c+r), f(c-r) in the SIDE, gain ~ residue (sign's cargo)
    g = 0.16 * r + 0.03
    f_hi = f_count(c + r)
    f_lo = f_count(c - r)
    pair = g * env_bell(tt, tau=0.7) * (np.sin(2 * np.pi * f_hi * tt)
                                        + np.sin(2 * np.pi * f_lo * tt))
    place(side, i0, pair)

# ------------------------------------------------------------------
# 18.5-24s: THE SHORE.  The walk lands at 55.  The sign rings: 55 in the side,
# 440 (the winding) faint; the count holds.  Stereo seals.
# ------------------------------------------------------------------
i0 = int(21.0 * sr)
sl = int(6.0 * sr)
tt = t[i0:i0 + sl] - t[i0]
swell = np.minimum(1.0, tt / 1.2) * np.minimum(1.0, (tt[-1] - tt) / 1.5)
# the shore -1: 55, the walk's landing, in the SIDE — the sign seals
place(side, i0, 0.30 * swell * np.sin(2 * np.pi * 55.0 * tt))
# 440 the winding, faint, in the side
trem = 1.0 + 0.25 * np.sin(2 * np.pi * 0.6 * tt)
place(side, i0, 0.08 * swell * trem * np.sin(2 * np.pi * 440.0 * tt))
# the count holds at 55 in the mid
place(mid, i0, 0.20 * swell * np.sin(2 * np.pi * 55.0 * tt))

# ------------------------------------------------------------------
# 24-29s: THE REFUSAL.  The count tries the rung below (51.9, count 10) and is
# cut pre-arrival — the never-landing, the walk continues.
# ------------------------------------------------------------------
for gc, gt0 in enumerate((27.5, 29.5)):
    ig = int(gt0 * sr)
    glen = 1.6 * sr
    ttg = t[ig:ig + int(glen)] - t[ig]
    atk = np.minimum(1.0, ttg / 0.20)
    gseg = atk * np.sin(2 * np.pi * f_count(10.0) * ttg)
    gseg[int(0.7 * sr):] = 0.0                       # cut before it rings
    place(mid, ig, 0.13 * gseg)
    place(side, ig, 0.05 * gseg)

# ------------------------------------------------------------------
# 29-34s: fade to the ground; the walk never returns.
# ------------------------------------------------------------------
fo = int(32.0 * sr)
tail = np.ones(n)
tail[fo:] *= np.linspace(1, 0, n - fo)
mid *= tail
side *= tail

# ------------------------------------------------------------------
# stereo: L = mid + side, R = mid - side.  mono = mid exactly.
# ------------------------------------------------------------------
L = mid + side
R = mid - side
stereo = np.stack([L, R], axis=1)
stereo = np.tanh(stereo * 1.2) * 0.95
pcm = (stereo * 32767.0).astype(np.int16)
with wave.open("assets/glide.wav", "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(pcm.tobytes())

mono_pcm = (np.tanh(np.stack([mid, mid], axis=1) * 1.2) * 0.95 * 32767.0).astype(np.int16)
with wave.open("assets/glide-mono.wav", "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(mono_pcm.tobytes())

print("wrote assets/glide.wav", n / sr, "s")
print("mid RMS:", round(float(np.sqrt(np.mean(mid ** 2))), 4))
print("side RMS:", round(float(np.sqrt(np.mean(side ** 2))), 4))
print("peak:", round(float(np.max(np.abs(stereo))), 3))
print("mono = mid exactly; the mirror pair (the residue) is dropped by the fold.")
for k in range(6):
    print(f"  mirror {k}: x={xs[k]:.4f} count={int(np.floor(xs[k]))} "
          f"r={xs[k]-np.floor(xs[k]):.4f} step={2*(xs[k]-np.floor(xs[k])):.4f}")
