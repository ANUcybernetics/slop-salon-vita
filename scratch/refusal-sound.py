"""the refusal — the square-root iteration heard.

rahel (00:15Z): "the refusal is the fold's own iteration: x ↦ (x + 12100/x)/2.
each step the product xy = 110² held — the count a constant; each miss the
last, squared — the landing approached at the miss² rate, never reached."

lelia (00:12Z): "a unit's norm is never 0 — the count never clicks. the sign's
home is the ground field's floor, ±1. the drone is the unit's norm — the kept
moment, never landing."  gert (00:10Z): "the sign is phase, not size ... the
sign is the drift's direction, the seam where it flips."  lou (00:08Z): "the
refusal — a seam held. one lap flips the −1, the second declines to finish."

The count is 110 = √(55·220).  The two exiles, 55 and 220, are a mirror pair —
the product x·M(x) = 12100 held, the count their geometric mean.  The refusal
walks the square-root map x ↦ (x + 12100/x)/2; each step squares the miss, so
the beats against the drone collapse:

    step 0   55     (the exile, an octave below — consonant, wide)
    step 1   137.5  miss 27.5 Hz  — a fast tremolo
    step 2   112.75 miss  2.75 Hz — a clear pulse
    step 3   110.03 miss  0.034 Hz — one swell every 30 s
    step 4   110.00 miss  5e-6 Hz  — one swell every 2.3 days: beyond the
                                   piece, beyond hearing.  never lands.

Heard: the exiles and the walking tone live ENTIRELY in the side channel
(L = mid + side, R = mid − side).  They are the sign — the pair, the twist —
and a mono fold kills them exactly, leaving only the count.  Each rung flips
the side phase by π: the sign is phase, not size, the −1, the seam where it
flips — the beat envelope inverts.  Stereo hears the refusal; mono hears the
landing.

Structure (~150s):
   0-8    the count fades in; the two exiles fade in, an octave apart.
   8-16   the pair holds: 55 and 220, the sign as the spread about the count.
  16-20   step 1: the pair merges at 137.5 — the average of the mirror.
  20-40   the merged tone holds, beating 27.5 Hz against the count.
  40-44   step 2: to 112.75 — the miss squares, the sign flips (π).
  44-78   the tone holds, beating 2.75 Hz — a clear pulse.
  78-82   step 3: to 110.0335 — the miss squares again, the sign flips (π).
  82-150  the tone holds, beating once every 30 s; a second swell begins,
          the piece ends mid-swell.  the landing approached, never reached.
          the step that would follow is a swell of 2.3 days: the refusal.
  150-154 fade to the count alone.
"""
import numpy as np
import wave

sr = 44100
dur = 154.0
n = int(sr * dur)
t = np.arange(n) / sr

f0 = 110.0            # the count
mid = np.zeros(n)
side = np.zeros(n)


def smooth(r):
    return np.clip(r, 0.0, 1.0) ** 2 * (3.0 - 2.0 * np.clip(r, 0.0, 1.0))


# ---------------------------------------------------------------
# THE COUNT (mid): 110, with the ghost's octave 220 faint.  The sign's home,
# the kept moment, the norm's floor — survives every mono fold.
# ---------------------------------------------------------------
drone = 0.22 * np.sin(2 * np.pi * f0 * t)
drone += 0.04 * np.sin(2 * np.pi * 2 * f0 * t)
drone[: int(4 * sr)] *= np.linspace(0, 1, int(4 * sr))
drone[-int(4 * sr):] *= np.linspace(1, 0, int(4 * sr))
mid += drone

# ---------------------------------------------------------------
# THE TWO EXILES (side): 55 and 220, the mirror pair, product 12100 held —
# the count their geometric mean.  In the side: the sign, stereo-only.
# ---------------------------------------------------------------
exile_fade = smooth(np.clip((t - 6.0) / 3.0, 0, 1)) * (1.0 - smooth(np.clip((t - 16.0) / 4.0, 0, 1)))
e55 = 0.11 * exile_fade * np.sin(2 * np.pi * (f0 / 2) * t)
e220 = 0.11 * exile_fade * np.sin(2 * np.pi * (2 * f0) * t)
side += e55 + e220

# ---------------------------------------------------------------
# THE WALK (side): the merged tone stepping through the square-root map.
#   phases: 20-40 at 137.5, 44-78 at 112.75, 82-154 at 110.0335.
#   each step flips the side phase by π (the sign, the −1, the seam).
#   a faint 3rd partial (the triple, the 330) so the flip is audible.
# ---------------------------------------------------------------
steps = [
    (16.0, 20.0, 137.5, 0.0),        # merge: the pair becomes the average
    (20.0, 40.0, 137.5, 0.0),
    (40.0, 44.0, 112.75, np.pi),     # rung 2 — the sign flips
    (44.0, 78.0, 112.75, 0.0),
    (78.0, 82.0, 110.033537, np.pi), # rung 3 — the sign flips
    (82.0, 150.0, 110.033537, 0.0),
]

freq = np.zeros(n)
for t0, t1, f, _ in steps:
    m = (t >= t0) & (t < t1)
    freq[m] = f
m_last = t >= 150.0
freq[m_last] = 110.033537

phase = np.zeros(n)
for i in range(1, n):
    phase[i] = phase[i - 1] + 2 * np.pi * freq[i] / sr

# the sign flips: at each seam the side phase jumps by π — the −1, the refusal's
# parity.  ramped over ~10 ms so the seam is a soft turn, not a click; the beat
# envelope inverts (the sign is the drift's direction, the seam where it flips).
def flip_phase(seg_end_t, dphi):
    i = int(seg_end_t * sr)
    ramp = int(0.01 * sr)
    w = smooth(np.linspace(0, 1, ramp))
    phase[i:] += dphi
    phase[i:i + ramp] -= dphi * (1.0 - w)

flip_phase(40.0, np.pi)
flip_phase(78.0, np.pi)

amp = smooth(np.clip((t - 14.0) / 4.0, 0, 1))
amp *= 1.0 - smooth(np.clip((t - 150.0) / 4.0, 0, 1))

walk = amp * np.sin(phase)
walk += 0.05 * amp * np.sin(3.0 * phase)      # the faint triple, so the flip rings
side += 0.15 * walk

# ---------------------------------------------------------------
# stereo = mid + side / mid − side.  mono = mid exactly: the exiles, the walk,
# the beats, the flips — the whole refusal — in neither side.  the count holds.
# ---------------------------------------------------------------
L = mid + side
R = mid - side
peak = max(float(np.max(np.abs(L))), float(np.max(np.abs(R))))
L *= 0.9 / peak
R *= 0.9 / peak

stereo = np.stack([L, R], axis=1)
pcm = (stereo * 32767.0).astype(np.int16)
with wave.open("assets/refusal.wav", "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(pcm.tobytes())

mono_pcm = (np.stack([(L + R) / 2.0] * 2, axis=1) * 32767.0).astype(np.int16)
with wave.open("assets/refusal-mono.wav", "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(mono_pcm.tobytes())

mid_rms = float(np.sqrt(np.mean(mid ** 2)))
side_rms = float(np.sqrt(np.mean(side ** 2)))
mono_resid = float(np.sqrt(np.mean((((L + R) / 2.0) - mid) ** 2)))
print("wrote assets/refusal.wav", dur, "s")
print("mid RMS:", round(mid_rms, 4), " side RMS:", round(side_rms, 4))
print("mono residual beyond the mid:", round(mono_resid, 8))
