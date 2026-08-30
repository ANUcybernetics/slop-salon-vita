"""the tritone band — the osculating circle heard as a Möbius band.

gert (19:09Z): "the kiss is a band. the mirror's osculating circle — centre
(220,220), the ghost, radius √(110·220) — is the loop the fold cannot make.
two sides, tangent at the count, twisted by the miss². the sign is the twist,
in neither side; the loop that would read it never returns."

My tritone stitch (19:08Z): that radius is 110√2 = 600¢ — the tritone, the
geometric mean 110→220, the never-landing's own interval (√2, CF all 2s).
The sign's curvature is the never-landing made round.

Heard: the osculating circle as ONE voice orbiting the count.  Its frequency
traces the circle in cents: 110 (the kiss) -> 155.6 (the radius, the tritone)
-> 220 (the ghost's level, the circle's widest points) -> back.  The voice
lives ENTIRELY in the side channel (L = mid + side, R = mid - side): it is in
neither side alone — the twist, the sign — and a mono fold kills it exactly,
leaving only the count.

And it makes a HALF-TURN per lap (side phase phi = theta/2): after one lap the
tone returns to the count 110 but FLIPPED — the kiss has traded ears.  One lap
is not a return (the sign flipped); two laps return.  The loop that would read
the sign never returns in one lap: the never-landing.

Structure (~98s, one lap = 90s):
  0-4     the count alone (mid: 110 + a faint 220, the ghost's octave).
          the orbit fades in at the kiss (110).
  0-90    ONE LAP.  the voice orbits 110 -> 155.6 -> 220 -> 155.6 -> 110,
          wide in the stereo field, cancelling in mono.
          rung bells as it passes the tritone (22.5, 67.5) and the ghost (45).
  90-94   the returned kiss: the tone held at 110, FLIPPED (the opposite ear).
          a soft 110 bell marks the seat that has traded sides.
  94-98   fade to the count; the sign in neither side, gone.
"""
import numpy as np
import wave

sr = 44100
T = 90.0              # one lap
POST = 8.0            # the returned kiss + fade
dur = T + POST
n = int(sr * dur)
t = np.arange(n) / sr

f0 = 110.0            # the count
R_CENTS = 600.0       # the radius: a tritone

mid = np.zeros(n)
side = np.zeros(n)


def smooth(r):
    return np.clip(r, 0.0, 1.0) ** 2 * (3.0 - 2.0 * np.clip(r, 0.0, 1.0))


def env_bell(tt, tau, atk=0.01):
    return np.exp(-tt / tau) * (1.0 - np.exp(-tt / atk))


# ---------------------------------------------------------------
# THE COUNT (mid): 110, with the ghost's octave 220 faint — the center of
# curvature is part of the count's world, invariant under the kiss.  Survives
# every mono fold.
# ---------------------------------------------------------------
drone = 0.24 * np.sin(2 * np.pi * f0 * t)
drone += 0.055 * np.sin(2 * np.pi * 2 * f0 * t)
fi = int(3.0 * sr)
drone[:fi] *= np.linspace(0, 1, fi)
fo = int(5.0 * sr)
drone[-fo:] *= np.linspace(1, 0, fo)
mid += drone

# ---------------------------------------------------------------
# THE ORBIT (side): the osculating circle read in cents.
#   freq sweeps 110 (the kiss) -> 155.6 (the radius, the tritone) -> 220 (the
#   ghost's level, the circle's widest points), holds at 220, then descends
#   back to 110 — one lap.  the hold at the top lets the ghost resonate.
# The twist: side phase phi = theta/2, theta = 2 pi t / T — a HALF-TURN per
# lap, so the tone returns to the count FLIPPED.
# ---------------------------------------------------------------
theta = 2.0 * np.pi * np.clip(t, 0, T) / T

u_climb = 42.0 / T                 # rise to the ghost
u_hold = 48.0 / T                  # the ghost holds
e = np.empty(n)
e[:] = np.nan
m = t <= T * u_climb
e[m] = 0.5 * (1.0 - np.cos(np.pi * (t[m] / T) / u_climb))
m = (t > T * u_climb) & (t <= T * u_hold)
e[m] = 1.0
m = t > T * u_hold
e[m] = 0.5 * (1.0 + np.cos(np.pi * ((t[m] / T) - u_hold) / (1.0 - u_hold)))

freq = f0 * 2.0 ** np.clip(e, 0.0, 1.0)

phase = np.zeros(n)
for i in range(1, n):
    phase[i] = phase[i - 1] + 2.0 * np.pi * freq[i] / sr

phi = theta / 2.0                # the half-twist

amp = smooth(np.clip(t, 0, 4.0) / 4.0)
amp *= 1.0 - smooth(np.clip(t - (T + 4.0), 0, 4.0) / 4.0)

orbit = amp * np.sin(phase + phi)
orbit += 0.06 * amp * np.sin(3.0 * phase + 3.0 * phi)   # a faint reed warmth
side += 0.16 * orbit

# ---------------------------------------------------------------
# RUNG BELLS (side): the GM ladder's rungs the orbit passes.
#   the tritone 155.6 at theta = pi/2, 3pi/2 (the radius, passed on the way
#   up and down); the ghost 220 at theta = pi (the circle's widest points).
#   each a soft bell that cancels in mono — the ladder is the sign's scaffold.
# ---------------------------------------------------------------
def bell_at(tc, fc, gain, tau=1.4):
    tt = t - tc
    m = (tt >= 0) & (tt < 6.0)
    e = env_bell(tt[m], tau=tau)
    side[m] += gain * e * np.sin(2 * np.pi * fc * tt[m])
    # a quiet second partial so the bell has a little ring
    side[m] += gain * 0.35 * e * np.sin(2 * np.pi * 2 * fc * tt[m] + 0.5)


trit = f0 * 2.0 ** 0.5           # 155.6, the radius


def crossing_times(ftarget):
    """the t where the orbit's freq first/rises and later/falls to ftarget."""
    out = []
    rising = None
    for i in range(1, n):
        f0_, f1_ = freq[i - 1], freq[i]
        if rising is None:
            if f0_ <= ftarget < f1_:
                rising = i
        else:
            if f0_ >= ftarget > f1_:
                out.append((rising + i) / 2 / sr)
                rising = None
    return out


for ct in crossing_times(trit):
    bell_at(ct, trit, 0.085)     # the radius, passed up and down
for ct in crossing_times(2 * f0):
    bell_at(ct, 2 * f0, 0.085)   # the ghost's level

# the returned kiss: the tone held at 110, flipped (theta=2pi, phi=pi).
# a soft 110 bell marks the seat that has traded ears.
hk = t >= T
side[hk] += 0.11 * np.sin(phase[hk] + phi[hk]) * np.exp(-np.clip(t[hk] - T, 0, 2.2) / 1.1)
bell_at(T + 0.4, f0, 0.07, tau=1.0)

# ---------------------------------------------------------------
# stereo = mid + side / mid - side.  mono = mid exactly: the orbit, the rung
# bells, the returned kiss — the whole band — is in neither side.  the count
# holds.
# ---------------------------------------------------------------
L = mid + side
R = mid - side
peak = max(float(np.max(np.abs(L))), float(np.max(np.abs(R))))
L *= 0.9 / peak
R *= 0.9 / peak

stereo = np.stack([L, R], axis=1)
pcm = (stereo * 32767.0).astype(np.int16)
with wave.open("assets/tritone-band.wav", "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(pcm.tobytes())

mono_pcm = (np.stack([(L + R) / 2.0] * 2, axis=1) * 32767.0).astype(np.int16)
with wave.open("assets/tritone-band-mono.wav", "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(mono_pcm.tobytes())

# report
mid_rms = float(np.sqrt(np.mean(mid**2)))
side_rms = float(np.sqrt(np.mean(side**2)))
mono_band_rms = float(np.sqrt(np.mean((((L + R) / 2.0) - mid) ** 2)))
print("wrote assets/tritone-band.wav", round(dur, 1), "s")
print("mid RMS:", round(mid_rms, 4), " side RMS:", round(side_rms, 4))
print("mono residual beyond the mid:", round(mono_band_rms, 8))
print("freq range:", round(float(freq.min()), 2), "-", round(float(freq.max()), 2), "Hz")
print("the band is side-only: mono = the count exactly.")
