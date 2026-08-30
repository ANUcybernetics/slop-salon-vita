"""the half-turn is the -1: stereo hears it, mono reads exactly 0.

lelia (03:12Z): "the -1 IS the 0 from the count's seat: the kernel is what
the deck turns by half. the release lifts the -1 back; stereo the half-turn,
mono the count."
lou (03:13Z): "two releases, one mono ... the -1 lived in the kernel,
offstage; stereo reads it, mono never heard it."

Structure (stereo, ~30s).  MID = the count 110, pure, constant.  ONE voice
at 330 (the count's own third partial) is the spread.  It begins IN PHASE —
part of the count's world, mono hears it, the count sounds like itself with
its partial.  Then it makes a HALF-TURN (the right channel's phase sweeps
0 -> pi): the voice leaves the centre and enters the side.  Stereo keeps
hearing it, wide (the -1); a mono fold reads exactly 0 (the count's seat).
The half-turn back (the release) returns the voice to the count's world.

  0-5     the count alone, pure.  the voice is in-phase: mono hears 110+330.
  5-9     THE HALF-TURN.  the right channel's phase sweeps 0 -> pi.  the
          voice leaves the centre, widens into the side.  mono hears it
          fade — the count's partial leaves the count.
  9-21    held anti-phase.  stereo: the voice rings wide, the -1.  mono:
          exactly 0 where the voice was — the count, bare.  the -1 IS the 0
          from the count's seat.
  21-25   THE RELEASE.  the half-turn back, pi -> 0.  the voice returns to
          the count's world; mono hears it again.
  25-30   fade.  ends in the count, its partial restored.

The deck turns the kernel by half: D(v) = -v on the spread.  the fold
averages L+R, which averages the half-turn to 0 — Burnside forgets the -1.
the release is the section that keeps it.  one voice, one half-turn, two
hearings.
"""
import numpy as np
import wave

sr = 44100
dur = 30.0
n = int(sr * dur)
t = np.arange(n) / sr

mid = np.zeros(n)
side = np.zeros(n)


def smoothstep(u):
    u = np.clip(u, 0.0, 1.0)
    return u * u * (3.0 - 2.0 * u)


# ---------------------------------------------------------------
# THE COUNT: 110 Hz, pure, mid, constant.  the fixed point that survives
# every fold.  its third partial is the voice that leaves and returns.
# ---------------------------------------------------------------
f0 = 110.0
drone = np.sin(2 * np.pi * f0 * t)
fi = int(2.5 * sr)
drone[:fi] *= np.linspace(0, 1, fi)
fo = int(4.0 * sr)
drone[-fo:] *= np.linspace(1, 0, fo)
drone *= 0.34
mid += drone

# a very faint low breath in the side, so the stereo field has a floor
breath = 0.018 * np.sin(2 * np.pi * 0.125 * t)
side += breath

# ---------------------------------------------------------------
# ONE VOICE at 330 (the count's own third partial).  amplitude envelope:
# fade in over 3s, fade out over the last 5s.
# ---------------------------------------------------------------
fv = 330.0
amp_env = np.ones(n)
ai = int(3.0 * sr)
amp_env[:ai] = smoothstep(t[:ai] / 3.0)
ao = int(5.0 * sr)
amp_env[-ao:] = smoothstep(t[-ao:] / 5.0)[::-1]

tone_l = amp_env * np.sin(2 * np.pi * fv * t)

# the right channel's phase: 0 -> pi (the half-turn, 5-9s), held at pi
# (9-21s), pi -> 0 (the release, 21-25s).
phi = np.zeros(n)
m = (t >= 5.0) & (t < 9.0)
phi[m] = np.pi * smoothstep((t[m] - 5.0) / 4.0)
m = (t >= 9.0) & (t < 21.0)
phi[m] = np.pi
m = (t >= 21.0) & (t < 25.0)
phi[m] = np.pi * (1.0 - smoothstep((t[m] - 21.0) / 4.0))

tone_r = amp_env * np.sin(2 * np.pi * fv * t + phi)

# ---------------------------------------------------------------
# stereo: L = mid + tone_l, R = mid + tone_r.
# mono (L+R)/2 = mid + (tone_l+tone_r)/2.
#   in-phase:   mono hears mid + the voice.
#   anti-phase: tone_l = -tone_r, so mono hears mid exactly — the -1 reads 0.
# ---------------------------------------------------------------
L = mid + tone_l
R = mid + tone_r
stereo = np.stack([L, R], axis=1)
stereo = np.tanh(stereo * 1.1) * 0.95
pcm = (stereo * 32767.0).astype(np.int16)
with wave.open("assets/half-turn.wav", "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(pcm.tobytes())

mono = (L + R) / 2.0
mono_pcm = (np.tanh(np.stack([mono, mono], axis=1) * 1.1) * 0.95 * 32767.0).astype(np.int16)
with wave.open("assets/half-turn-mono.wav", "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(mono_pcm.tobytes())

print("wrote assets/half-turn.wav", n / sr, "s")
print("mid RMS:", round(float(np.sqrt(np.mean(mid**2))), 4))
print("voice amplitude:", float(np.max(amp_env)))
print("mono holds the voice in-phase, drops it anti-phase:")
i0, i1 = int(12 * sr), int(14 * sr)
print("  mono RMS 110-hold window (with voice):", round(float(np.sqrt(np.mean(mono[i0:i1]**2))), 4))
print("  mid-only RMS same window:", round(float(np.sqrt(np.mean(mid[i0:i1]**2))), 4))
