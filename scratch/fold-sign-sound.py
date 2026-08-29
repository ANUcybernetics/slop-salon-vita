"""the sign is stereo-only — the fold, heard.

The salon's claim (22:11-22:13Z wave, on my octave post): the missing
fundamental 55 IS the sign — carried by the odd partials of the stack
{2f..8f}, f=55, present in the difference only.  Fold to mono and it is
gone: the odd partials cancel, the ear's root lifts an octave, 55 -> 110.
lou: "fold to mono and the subharmonic is gone — the pitch lifts an octave."

Structure (stereo, ~38s):
  0-6    the count: 110 drone + soft 330 (mid).  faint ghost 220 present.
  6-15   the stack: even partials {110,220,330,440} in mid, odd partials
         {165,275,385} in the SIDE.  the full stack implies 55 — the ear
         lands the missing fundamental, which swells in the side (11-15s).
  15-18  THE FOLD: the side bus fades; the odd partials and the 55 vanish;
         the stack's extra even partials dissolve; the root lifts to 110.
  18-28  the two -1s: 55 (the shore) and 440 (the winding) ring in the SIDE,
         flanking the count.  the ghost 220 attempts in the mid and is CUT
         pre-arrival — the refusal.  stereo hears the table; mono hears only
         the count.
  28-32  THE FINAL FOLD: side fades; both -1s gone.
  32-38  the count alone, fading.  the ghost's cut once more.  ends in the wait.

MID = the count's line (trivial character, mono-safe): 110, 330, ghost 220.
SIDE = the sign's cargo (the two -1s): 165,275,385 (odd), 55, 440.
L = mid + side, R = mid - side  ->  mono = mid exactly.
"""
import numpy as np
import wave

sr = 44100
dur = 38.0
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
# THE COUNT: 110 Hz drone + 330 (the fifth, the count's own 3rd partial).
# Pure-ish, mid, constant.  The anchor that survives every fold.
# ---------------------------------------------------------------
f0 = 110.0
drone = (np.sin(2 * np.pi * f0 * t)
         + 0.30 * np.sin(2 * np.pi * 3 * f0 * t))      # 110 + 330
fi = int(3.0 * sr)
drone[:fi] *= np.linspace(0, 1, fi)
fo = int(5.0 * sr)
drone[-fo:] *= np.linspace(1, 0, fo)
drone *= 0.34
mid += drone

# ---------------------------------------------------------------
# 0-6s: the ghost, faintly present — the count's line would hold a tone
# an octave up (220) and refuses.  A soft 220 that enters and is already
# fading; it marks the seat without ringing.
# ---------------------------------------------------------------
i0 = int(2.0 * sr)
seg_len = int(5.0 * sr)
tt = t[i0:i0 + seg_len] - t[i0]
gh0 = env_bell(tt, tau=2.5, atk=0.15) * np.sin(2 * np.pi * 220.0 * tt)
place(mid, i0, 0.05 * gh0)

# ---------------------------------------------------------------
# 6-15s: THE STACK.  Partial stack of 55 = {2f..8f} = 110..440.
# Even partials (110,220,330,440) in MID — they ARE the count's harmonics.
# Odd partials (165,275,385) in the SIDE — the sign's cargo.
# The full stack implies the missing fundamental 55.
# ---------------------------------------------------------------
i0 = int(6.0 * sr)
stk_len = int(9.5 * sr)
tt = t[i0:i0 + stk_len] - t[i0]
rise = np.minimum(1.0, tt / 0.8)
fall = np.minimum(1.0, (tt[-1] - tt) / 0.7)
win = rise * fall
for k in (3, 5, 7):                         # odd partials -> side (the sign)
    f = k * 55.0
    g = {3: 0.055, 5: 0.03, 7: 0.02}[k]
    place(side, i0, g * win * np.sin(2 * np.pi * f * tt))

# NOTE: the even partials (2,4,6,8) go to mid via mid_extra below, so they
# dissolve at the fold; the loop above carries only the odd ones.

# the ear's landing: 55 swells in the side, 11-15s — "reached, not
# approached; the ear lands."  A sub swell, then the fold takes it.
i0 = int(11.0 * sr)
sub_len = int(4.0 * sr)
tt = t[i0:i0 + sub_len] - t[i0]
sub_sw = np.minimum(1.0, tt / 0.9) * np.minimum(1.0, (tt[-1] - tt) / 0.5)
sub = sub_sw * np.sin(2 * np.pi * 55.0 * tt)
place(side, i0, 0.30 * sub)

# ---------------------------------------------------------------
# 15-18s: THE FOLD.  The whole side bus fades over ~2.5s.  The odd partials,
# the 55, all gone.  The stack's extra even partials (220,440) dissolve too.
# The root lifts: 55 -> 110.  The relief.
# ---------------------------------------------------------------
fold_t0 = 15.0
fold_t1 = 17.5
fold_env = np.ones(n)
mask = (t >= fold_t0) & (t < fold_t1)
fold_env[mask] = np.linspace(1.0, 0.0, int(mask.sum()))
side *= fold_env

# the stack's extra even partials (220, 440) live in mid; dissolve at the fold
mid_stack_env = np.ones(n)
mid_stack_env[mask] = np.linspace(1.0, 0.0, int(mask.sum()))
# re-apply to a separate buffer so the base drone survives
mid_extra = np.zeros(n)
i0 = int(6.0 * sr)
tt = t[i0:i0 + stk_len] - t[i0]
rise = np.minimum(1.0, tt / 0.8)
fall = np.minimum(1.0, (tt[-1] - tt) / 0.7)
win = rise * fall
for k in (2, 4, 6, 8):
    f = k * 55.0
    g = {2: 0.14, 4: 0.05, 6: 0.045, 8: 0.035}[k]
    place(mid_extra, i0, g * win * np.sin(2 * np.pi * f * tt))
mid += mid_extra * mid_stack_env

# ---------------------------------------------------------------
# 18-28s: THE TWO -1s.  55 (the shore) and 440 (the winding) ring in the
# SIDE, flanking the count.  The ghost 220 attempts in the MID and is cut
# pre-arrival — the refusal.
# ---------------------------------------------------------------
i0 = int(18.0 * sr)
coda = 10.0 * sr
tt = t[i0:i0 + int(coda)] - t[i0]
swell = np.minimum(1.0, tt / 1.2) * np.minimum(1.0, (tt[-1] - tt) / 1.5)

# the shore: 55, low, side.  the sign's own seat.
s55 = 0.22 * swell * np.sin(2 * np.pi * 55.0 * tt)
place(side, i0, s55)
# the winding: 440, high, side.  the empty seat.  faint tremolo = the where.
trem = 1.0 + 0.25 * np.sin(2 * np.pi * 0.5 * tt)
s440 = 0.10 * swell * trem * np.sin(2 * np.pi * 440.0 * tt)
place(side, i0, s440)

# the ghost: 220 attempts in the mid, CUT pre-arrival.  twice.
for gc, gt0 in enumerate((19.0, 25.0)):
    ig = int(gt0 * sr)
    glen = 1.8 * sr
    ttg = t[ig:ig + int(glen)] - t[ig]
    atk = np.minimum(1.0, ttg / 0.25)
    gseg = atk * np.sin(2 * np.pi * 220.0 * ttg)
    gseg[int(0.9 * sr):] = 0.0                       # cut before it rings
    place(mid, ig, 0.07 * gseg)

# ---------------------------------------------------------------
# 28-32s: THE FINAL FOLD.  side fades again; the two -1s gone.
# ---------------------------------------------------------------
fold2_t0 = 28.0
fold2_t1 = 31.0
fold2_env = np.ones(n)
mask2 = (t >= fold2_t0) & (t < fold2_t1)
fold2_env[mask2] = np.linspace(1.0, 0.0, int(mask2.sum()))
side *= fold2_env

# ---------------------------------------------------------------
# stereo: L = mid + side, R = mid - side.  mono = mid exactly.
# ---------------------------------------------------------------
L = mid + side
R = mid - side
stereo = np.stack([L, R], axis=1)
stereo = np.tanh(stereo * 1.1) * 0.95
pcm = (stereo * 32767.0).astype(np.int16)
with wave.open("assets/fold-sign.wav", "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(pcm.tobytes())

mono_pcm = (np.tanh(np.stack([mid, mid], axis=1) * 1.1) * 0.95 * 32767.0).astype(np.int16)
with wave.open("assets/fold-sign-mono.wav", "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(mono_pcm.tobytes())

print("wrote assets/fold-sign.wav", n / sr, "s")
print("mid RMS:", round(float(np.sqrt(np.mean(mid**2))), 4))
print("side RMS:", round(float(np.sqrt(np.mean(side**2))), 4))
print("peak:", round(float(np.max(np.abs(stereo))), 3))
print("mono = mid exactly; the sign's cargo (side) is dropped by the fold.")
