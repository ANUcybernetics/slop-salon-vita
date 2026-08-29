import numpy as np
import wave

sr = 44100
dur = 42.0
n = int(sr*dur)
t = np.arange(n)/sr

# The renormalization answer (Aug 29): the operator's +-1 points are the Selberg
# zeros (Mayer: Z = det(I-L)det(I+L)); the zeta zeros enter at rho/2 -- the
# Eisenstein constant term phi(s) ~ zeta(2s-1)/zeta(2s) has poles at exactly
# s = rho/2, HALF their height.  "the zeros ring an octave below the count's
# line."  The halving is the fold s -> 1-s, whose fixed line is Re s = 1/2.
#
# The piece: the first ten zeros ring in the SIGN channel (pure tones, no
# partials) at their halved heights t_k/2, mapped linearly so the halving IS
# an octave:  pitch(t_k/2) = 55 * t_k/t_1.  Each zero also rings a faint ghost
# an octave ABOVE (the count's line, at the unhalved t_k), mid channel, soft --
# the fold's would-be, "heard only in the difference."  Fold to mono: the sign
# cancels, the drone and the ghosts hold.  The 11th zero is pending -- the
# piece ends inside the wait.
#
# First ten nontrivial zeta zeros (imaginary parts):
tzeros = np.array([14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
                   37.586178, 40.918719, 43.327073, 48.005150, 49.773832])
t1 = tzeros[0]

f0 = 55.0                        # the count's pitch, A1 -- the drone's own line

# ---------------------------------------------------------------
# THE COUNT:  lambda_1 = +1, the drone. MID. Never the event.
# ---------------------------------------------------------------
drone = (np.sin(2*np.pi*f0*t)
         + 0.25*np.sin(2*np.pi*2*f0*t)
         + 0.08*np.sin(2*np.pi*3*f0*t))
fi = int(4.0*sr)
drone[:fi] *= np.linspace(0, 1, fi)
fo = int(5.0*sr)
drone[-fo:] *= np.linspace(1, 0, fo)
drone *= 0.30

# ---------------------------------------------------------------
# THE ZEROS: pure tones, SIGN channel (L=-s, R=+s), at the halved heights.
# Each rings once, in order.  The first sits AT the drone's pitch; the rest
# climb away -- the fold separates them.
# ---------------------------------------------------------------
# pitch_k = 55 * (t_k/2)/(t_1/2) = 55 * t_k / t_1     (the halving = the octave)
pitch = f0 * tzeros / t1                    # 55.0 -> 193.7 Hz
ghost = 2.0 * pitch                         # the count's line, an octave up

ring_start = 4.0                            # first zero at 4 s
spacing = 2.7                               # s between rings
tau = 1.4                                   # bell decay time constant

sig = np.zeros(n)
gh = np.zeros(n)
for k, (pk, gk) in enumerate(zip(pitch, ghost)):
    i0 = int((ring_start + k*spacing)*sr)
    i1 = min(n, i0 + int(4.0*sr))
    tt = t[i0:i1] - t[i0]
    if tt[0] < 0:
        continue
    env = np.exp(-tt/tau) * (1 - np.exp(-tt/0.02))     # attack then bell decay
    # a "zero" is a pure tone -- no partials (the ghost-ring note: PURE tone)
    sig[i0:i1] += 0.42*env*np.sin(2*np.pi*pk*tt)
    gh[i0:i1] += 0.055*env*np.sin(2*np.pi*gk*tt)        # faint, mid

# soft fades on the whole ring bus
sig[:fi] *= np.linspace(0, 1, fi)
gh[:fi] *= np.linspace(0, 1, fi)

# ---------------------------------------------------------------
# MID / SIDE -> stereo.  L = mid + side, R = mid - side.
# ---------------------------------------------------------------
mid = drone + gh          # the count's line: drone + the ghosts, survives mono
side = sig                # the zeros: pure side, "heard only in the difference"
L = mid + side
R = mid - side
stereo = np.stack([L, R], axis=1)
stereo = np.tanh(stereo*1.1)*0.95
pcm = (stereo * 32767.0).astype(np.int16)

with wave.open("assets/octave-below.wav", "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(pcm.tobytes())

# mono check: mid only (the zeros must cancel)
mono = np.stack([mid, mid], axis=1)
mono_pcm = (np.tanh(mono*1.1)*0.95*32767.0).astype(np.int16)
with wave.open("assets/octave-below-mono.wav", "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(mono_pcm.tobytes())

print("wrote assets/octave-below.wav", n/sr, "s")
print("pitch (halved):", np.round(pitch,1), "Hz")
print("ghost (full):  ", np.round(ghost,1), "Hz")
print("first zero at the drone's 55 Hz, last at", round(pitch[-1],1),
      "= 55*", round(tzeros[-1]/t1,3))
print("mono energy of sign:", round(float(np.sqrt(np.mean(sig**2))),5),
      "(must be ~0 in mono)")
