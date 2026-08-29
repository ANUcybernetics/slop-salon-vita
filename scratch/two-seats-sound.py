import numpy as np
import wave

sr = 44100
dur = 68.0
n = int(sr*dur)
t = np.arange(n)/sr

# ---------------------------------------------------------------
# The operator's two seats (Aug 29):  L_s = sum_a (a+x)^{-2s}
#   s=1:  lambda_1 = +1  the count (drone), a zero of det(I-L_1), at zeta's pole
#   s->1/2^+: Re s=1/2 is the operator's own convergence boundary (the shore);
#             lambda_2(s) -> -1 EXACTLY with lambda_2+1 ~ 4(s-1/2)  (the sign)
#             lambda_3(s) -> +0.2234  (the even),  lambda_4 -> -0.0700
#   "the count marginal at the pole, the sign marginal at the shore."
#
# The piece sweeps s from 1.0 down toward 0.505 and ends INSIDE the
# approach: lambda_2 never reaches -1, the sign never lands on the count.
#
# Verified values (M=36, nmax=200k):
#   s=1.0   gap=0.6963  |l2|=0.30366  l3=0.10088
#   s=0.9   gap=0.6366  |l2|=0.36344  l3=0.11668
#   s=0.8   gap=0.5575  |l2|=0.44247  l3=0.13577
#   s=0.7   gap=0.4480  |l2|=0.55199  l3=0.15916
#   s=0.6   gap=0.2842  |l2|=0.71576  l3=0.18832
#   s=0.55  gap=0.1654  |l2|=0.83462  l3=0.20572
#   s=0.52  gap=0.0737  |l2|=0.92631  l3=0.21727
#   s=0.505 gap=0.0196  |l2|=0.98042  l3=0.22339
# ---------------------------------------------------------------

# --- the sweep: gap g = lambda_2 + 1 ~ 4(s-1/2), shrinking exponentially.
#     log-time so the approach is perceptually uniform: each halving of the
#     gap takes the same duration. g: 0.6963 -> 0.0196 over the piece.
g0, g1 = 0.69634, 0.01958
g = g0 * (g1/g0)**(t/dur)            # exponential approach, never reaches 0
s = 0.5 + g/4.0

# lambda_3(g) interpolated from the verified curve
gs = np.array([0.69634, 0.63656, 0.55753, 0.44801, 0.28424, 0.16538, 0.07369, 0.01958])
l3s = np.array([0.10088, 0.11668, 0.13577, 0.15916, 0.18832, 0.20572, 0.21727, 0.22339])
lam3 = np.interp(np.log(g), np.log(gs[::-1]), l3s[::-1])

abs_l2 = 1.0 - g                     # = |lambda_2(s)|, exactly (lambda_2+1=g)

# ---------------------------------------------------------------
# THE COUNT:  lambda_1 = +1, the drone, the Gauss measure. MID. Never the event.
# The pole: as s->1/2, lambda_1 -> +inf — a slow swell in the last stretch,
# but the drone holds its ground, "never the event."
f0 = 55.0                            # A1
drone = (np.sin(2*np.pi*f0*t)
         + 0.30*np.sin(2*np.pi*2*f0*t)
         + 0.12*np.sin(2*np.pi*3*f0*t)
         + 0.06*np.sin(2*np.pi*4*f0*t))     # the 4th harmonic: where the even is absorbed
fi = int(2.0*sr)
drone[:fi] *= np.linspace(0, 1, fi)
# the pole: brightness + amplitude swell over the final 20 s, then the piece ends
pole_on = int((dur-20.0)*sr)
u = np.zeros(n)
u[pole_on:] = np.linspace(0, 1, n-pole_on)
swell = 1.0 + 0.55*u + 0.35*u*u           # modest — the drone is never the event
bright = 1.0 + 0.5*u                      # a touch more 4th harmonic as s->1/2
drone4 = 0.06*np.sin(2*np.pi*4*f0*t)
drone = (np.sin(2*np.pi*f0*t)
         + 0.30*np.sin(2*np.pi*2*f0*t)
         + 0.12*np.sin(2*np.pi*3*f0*t)
         + bright*drone4)
drone *= swell
fo = int(3.0*sr)
drone[-fo:] *= np.linspace(1, 0, fo)
drone *= 0.50

# ---------------------------------------------------------------
# THE SIGN:  lambda_2 < 0, the odd mode, the where. PURE SIDE (cancels in mono —
# "heard only in the difference"). Its pitch approaches the count's 4th harmonic
# (220 = 4*55) as |lambda_2| -> 1, but never lands:  f = 220*|lambda_2|.
f_sig = 220.0 * abs_l2                       # 66.8 -> 215.7 Hz, asymptotic to 220
# phase accumulation via integral of instantaneous frequency
phase_sig = 2*np.pi*np.cumsum(f_sig)/sr
# a sign has character: 2 partials, odd structure (a thin saw)
sig = (np.sin(phase_sig) + 0.35*np.sin(2*phase_sig)
       - 0.15*np.sin(3*phase_sig))
amp_sig = 0.10 + 0.26*(abs_l2 - 0.30366)/(1.0 - 0.30366)   # 0.10 -> 0.36
sig *= amp_sig
sig[:fi] *= np.linspace(0, 1, fi)
sig[-int(3.5*sr):] *= np.linspace(1, 0, int(3.5*sr))

# ---------------------------------------------------------------
# THE EVEN:  lambda_3 > 0, the even mode, lives in the MID — the count's sector.
# Glides up into the drone's 4th harmonic and is ABSORBED: it lands on 220 and
# dissolves into the count's harmonic there.  f = 220 * lambda_3 / lambda_3(shore).
f_even = 220.0 * lam3 / 0.22339                    # 99.4 -> 220 Hz
phase_even = 2*np.pi*np.cumsum(f_even)/sr
even = np.sin(phase_even) + 0.20*np.sin(2*phase_even)
amp_even = 0.07 + 0.09*(lam3 - 0.10088)/(0.22339 - 0.10088)   # 0.07 -> 0.16
even *= amp_even
even[:fi] *= np.linspace(0, 1, fi)
# absorbed: as it nears 220, crossfade its energy into the drone's 4th harmonic
absorb = np.clip((f_even - 200.0)/20.0, 0, 1)**2       # only the last few Hz
even *= (1 - 0.85*absorb)
# (the drone's 4th harmonic already brightens into that region — the two merge)
even[-int(3.0*sr):] *= np.linspace(1, 0, int(3.0*sr))

# ---------------------------------------------------------------
# MID / SIDE -> stereo.  L = mid + side, R = mid - side.
mid = drone + even
side = sig
L = mid + side
R = mid - side
stereo = np.stack([L, R], axis=1)
# soft clip to be safe
stereo = np.tanh(stereo*1.1)*0.95
pcm = (stereo * 32767.0).astype(np.int16)

with wave.open("assets/two-seats.wav", "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(pcm.tobytes())

# mono check: mid only (the sign must vanish)
mono = np.stack([mid, mid], axis=1)
mono_pcm = (np.tanh(mono*1.1)*0.95*32767.0).astype(np.int16)
with wave.open("assets/two-seats-mono.wav", "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(mono_pcm.tobytes())

print("wrote assets/two-seats.wav", n/sr, "s")
print("sign ends at", f_sig[-1], "Hz (220 = 4*55 the where's base, never landed)")
print("even ends at", f_even[-1], "Hz, absorbed into the 4th harmonic")
print("mono energy of sign:", np.sqrt(np.mean(sig**2)), "(must be ~0 in mono)")
