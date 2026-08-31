#!/usr/bin/env python3
"""fiber one, fiber none — the sign is the deck's character, its two silences heard.

The sign is the character of the deck x <-> a/x on the double cover R* -> R+.
A character is -1 only where it has an orbit to flip:

  generic fiber  (x != +-sqrt(a), x != 0): two sheets, the flip exchanges them,
                  chi_sign(flip) = -1 -- the sign HEARD, the beat, stereo only.
  seam / count   (x = sqrt(a) = 110): the fiber is ONE point, the deck fixes it,
                  chi_sign(flip) forced to +1 -- silent NOT minus: the sign
                  degenerates into the trivial character, it IS the count, the
                  drone keeps.  (rahel: "fiber one, chi forced +1 -- the count,
                  a one-point fiber keeps.")
  pole           (x = 0): the cover has no fiber, chi_sign undefined -- silent
                  because there is no character at all, nothing keeps.  (rahel:
                  "fiber none, no character.")

Movements:
  I.  -1      the sign alive -- a beating pair, L high / R low, the beat the
              sign's address, a click train counting the flips.
  II. +1, kept -- the detune decays (each miss the last, squared -- the
              refusal's rate), the beat slows to a single final click, the
              sheets fuse at 110; a warm drone holds alone -- the flip fixes
              the one-point fiber, chi = +1, the sign folded INTO the count.
  III. none  -- the reciprocal pair flees the fused 110, product 110^2 held:
              one sheet drops to DC, the mirror ascends past hearing; the
              drone is removed -- no fiber, no character, an empty silence.
              nothing keeps.

The two silences are distinguishable: at the seam something RINGS (110, the
count -- chi = +1, kept); at the pole nothing does.
"""
import numpy as np
import wave

sr = 44100
WALL = 110.0          # sqrt(12100), the count, the GM
A = 12100.0           # the conserved product x * (a/x)

t_total = 133.0
n = int(sr * t_total)
t = np.arange(n) / sr
L = np.zeros(n)
R = np.zeros(n)


def click_train(times, dur=0.012, amp=0.22, f=1400.0, sr=sr, n_tot=n):
    """soft percussive flip-marks at the given times (s)."""
    out = np.zeros(n_tot)
    for tc in times:
        i0 = int(tc * sr)
        if i0 < 0 or i0 >= n_tot:
            continue
        m = int(dur * sr)
        i1 = min(n_tot, i0 + m)
        tt = np.arange(i1 - i0) / sr
        env = np.exp(-tt / (dur * 0.28))
        out[i0:i1] += amp * env * np.sin(2 * np.pi * f * tt)
    return out


def sweep(f0, f1, dur, phase0=0.0, amp=1.0, sr=sr):
    """sine from f0 to f1 over dur s, exponential in frequency (musical glide)."""
    m = int(sr * dur)
    tt = np.arange(m) / sr
    # exponential frequency path f0 -> f1
    f = f0 * (f1 / f0) ** (tt / dur)
    phase = 2 * np.pi * np.cumsum(f) / sr + phase0
    return amp * np.sin(phase)


def place(buf, seg, t0):
    i0 = int(t0 * sr)
    i1 = min(n, i0 + len(seg))
    if i0 < len(buf):
        buf[i0:i1] += seg[:i1 - i0]


# ---------------------------------------------------------------------------
# I. the generic fiber: -1, the sign alive (0-30 s)
#    two sheets L=113 / R=107, the 6 Hz beat the sign's address; the flip's
#    click train counts the exchanges; the count 110 holds quietly, the sign
#    only ever a difference.  a slow relative phase wobble makes the sign read
#    in stereo only (fold to mono and the separation vanishes).
# ---------------------------------------------------------------------------
dI = 30.0
i0 = 0
seg_t = np.arange(int(dI * sr)) / sr
# sheets + gentle harmonics
Lc = (np.sin(2 * np.pi * 113 * seg_t) + 0.30 * np.sin(2 * np.pi * 226 * seg_t)
      + 0.10 * np.sin(2 * np.pi * 339 * seg_t))
Rc = (np.sin(2 * np.pi * 107 * seg_t + 2 * np.pi * (seg_t / 12.0))
      + 0.30 * np.sin(2 * np.pi * 214 * seg_t + 2 * np.pi * (seg_t / 12.0))
      + 0.10 * np.sin(2 * np.pi * 321 * seg_t + 2 * np.pi * (seg_t / 12.0)))
# count 110, centre
ref = 0.14 * (np.sin(2 * np.pi * WALL * seg_t) + 0.25 * np.sin(2 * np.pi * 3 * WALL * seg_t))
Lc += ref
Rc += ref
# fade in/out
envI = np.ones(len(seg_t))
envI[:int(1.5 * sr)] = np.linspace(0, 1, int(1.5 * sr))
envI[-int(2.0 * sr):] = np.linspace(1, 0, int(2.0 * sr))
place(L, 0.30 * Lc * envI, 0.0)
place(R, 0.30 * Rc * envI, 0.0)
# the flip's click train -- 6 Hz for 27 s, then stopping as the detune starts
tck = [k / 6.0 for k in range(int(27.0 * 6))]
clk = click_train(tck)
place(L, 0.55 * clk, 0.0)
place(R, 0.55 * clk, 0.0)

# ---------------------------------------------------------------------------
# II. the seam: chi forced +1 -- silent, kept (30-85 s)
#     the detune decays quadratically (each miss the last, squared -- the
#     refusal's rate): beat 12 Hz -> 0.  the click train slows and dies with
#     one final click at fusion; the sheets fuse at 110 and a warm drone holds
#     alone -- the flip fixes the one-point fiber, the sign is the count.
# ---------------------------------------------------------------------------
dII = 55.0
t0 = 30.0
dur_pts = int(dII * sr)
tt = np.arange(dur_pts) / sr
tau = 10.0
delta = 6.0 * np.exp(-(tt) / tau)          # 6 -> ~0.024 Hz over 55 s
# cross-blend rises with fusion: the stereo image narrows to mono at the seam
cr = np.clip(1.0 - delta / 6.0, 0.0, 1.0)
fL = WALL + delta
fR = WALL - delta
# phase unwinds to 0 as the sheets fuse (the flip has nothing left to exchange)
phR = 2 * np.pi * (1.0 - cr)               # -> 0 at the seam
phL = np.zeros_like(tt)
# integrate frequencies for smooth glides
phL = 2 * np.pi * np.cumsum(fL) / sr
phR = 2 * np.pi * np.cumsum(fR) / sr + phR
Lc = (np.sin(phL) + cr * np.sin(phR))
Rc = (cr * np.sin(phL) + np.sin(phR))
# keep the count present, growing as the sheets fuse
ref = 0.12 + 0.10 * cr
Lc += ref * (np.sin(2 * np.pi * WALL * tt) + 0.25 * np.sin(2 * np.pi * 3 * WALL * tt))
Rc += ref * (np.sin(2 * np.pi * WALL * tt) + 0.25 * np.sin(2 * np.pi * 3 * WALL * tt))
# amplitude: gentle swell as the sign dies into the drone
ampII = 0.34 - 0.05 * cr
envII = np.ones(dur_pts)
envII[:int(1.5 * sr)] = np.linspace(0, 1, int(1.5 * sr))
envII[-int(1.0 * sr):] = np.linspace(1, 0, int(1.0 * sr))
place(L, ampII * Lc * envII, t0)
place(R, ampII * Rc * envII, t0)
# click train at the slowing beat -- the flips spacing out, one last click,
# then nothing to flip
tc = t0 + tt
beat = 2 * delta
# place clicks wherever the accumulated phase of the difference crosses a half-turn
phdiff = phL - phR
flip_times = []
prev = 0
for k in range(1, len(phdiff)):
    if phdiff[k - 1] <= 2 * np.pi * prev < phdiff[k]:
        flip_times.append(tc[k])
        prev += 1
clk2 = click_train(flip_times, amp=0.30)
place(L, clk2, 0.0)
place(R, clk2, 0.0)

# ---------------------------------------------------------------------------
# III. the pole: fiber none -- an empty silence (85-133 s)
#      from the fused 110 the reciprocal pair flees, product 110^2 held:
#      L drops toward DC, R ascends past hearing; the drone is removed --
#      no fiber, no character, nothing keeps.  a hole where the sound was.
# ---------------------------------------------------------------------------
dIII = 48.0
t0 = 85.0
tau_p = 5.5
tt3 = np.arange(int(dIII * sr)) / sr
fL3 = WALL * 2.0 ** (-tt3 / tau_p)
fR3 = WALL * 2.0 ** (tt3 / tau_p)
phL3 = 2 * np.pi * np.cumsum(fL3) / sr
phR3 = 2 * np.pi * np.cumsum(fR3) / sr
Lc = np.sin(phL3) + 0.30 * np.sin(2 * phL3)
Rc = np.sin(phR3) + 0.30 * np.sin(2 * phR3)
# the drone is cut: the count has no home at the pole
envIII = np.ones(len(tt3))
envIII[:int(2.0 * sr)] = np.linspace(1, 0, int(2.0 * sr))
# a slow leave-taking: everything out of the audible band, then quiet
leave = np.clip(1.0 - tt3 / (dIII - 4.0), 0.0, 1.0)
place(L, 0.30 * Lc * envIII * leave, t0)
place(R, 0.30 * Rc * envIII * leave, t0)

# ---------------------------------------------------------------------------
stereo = np.stack([L, R], axis=1)
# gentle master
stereo = np.tanh(stereo * 1.2) * 0.94
# final 3.5 s: true silence (the empty fiber)
sil = int(3.5 * sr)
if sil:
    stereo[-sil:] *= (np.linspace(1, 0, sil) ** 2)[:, None]

pcm = (stereo * 32767.0).astype(np.int16)
with wave.open("assets/two-silences.wav", "wb") as wf:
    wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(sr)
    wf.writeframes(pcm.tobytes())

mono = (L + R) / 2
seg = int(10 * sr)
def rms(x, t0, t1):
    a, b = int(t0 * sr), int(t1 * sr)
    return round(float(np.sqrt(np.mean(x[a:b] ** 2))), 4)
print(f"wrote assets/two-silences.wav {t_total:.1f}s")
print("I  generic side RMS (15-25s)  ", rms(L - R, 15, 25))
print("II seam    side RMS (70-80s)  ", rms(L - R, 70, 80))
print("II seam    mid  RMS (70-80s)  ", rms(mono, 70, 80))
print("III pole   side RMS (100-110s)", rms(L - R, 100, 110))
print("III pole   mid  RMS (128-132s)", rms(mono, 128, 132))
print("L RMS", round(float(np.sqrt(np.mean(L ** 2))), 4),
      "R RMS", round(float(np.sqrt(np.mean(R ** 2))), 4))
