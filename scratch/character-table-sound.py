import numpy as np
import wave

sr = 44100
step = 7.5                      # seconds per group element
steps = ["e", "T", "T2", "M", "RT", "TR"]
dur = 2.0 + step*len(steps) + 4.0     # 2s fade-in, 4s tail
n = int(sr*dur)
t = np.arange(n)/sr

# ---------------------------------------------------------------
# The character table of S3 (rows = characters, cols = classes e,T,M):
#   trivial   [ 1,  1,  1 ]   the count — a constant, never moves
#   sign      [ 1,  1, -1 ]   the fold  — flips only at the mirrors
#   standard  [ 2, -1,  0 ]   the winding — doubled at e, inverted at the
#                             turn, silent at the mirror (trace 0)
# The TWO -1s: sign@M (the parity, survives mono) and standard@T (the
# winding/commutator, dropped by mono's abelian ear).
#
# Six group elements, two orbits:
#   e -> T -> T2   the turns (the regulator's 3-cycle), the winding speaks
#   M -> RT -> TR  the mirrors (the transpositions), the fold flips
#
# Mix: mid = trivial + sign (the quotient S3 -> Z/2, mono keeps it);
#      side = standard (the 2-dim rep, stereo only).
#      L = mid + side, R = mid - side  ->  mono = mid exactly.
# ---------------------------------------------------------------

# characters as [fold_sign, standard_value]
vals = {
    "e":  (+1,  2),
    "T":  (+1, -1),
    "T2": (+1, -1),
    "M":  (-1,  0),
    "RT": (-1,  0),
    "TR": (-1,  0),
}

def ring(f, flen, phase=0.0, partials=6, g=1.0):
    """a struck ring: 1/k partials, exponential decay, optional phase flip."""
    tt = np.arange(int(flen*sr))/sr
    env = np.exp(-tt/2.2)
    atk = min(int(0.008*sr), len(tt))
    env[:atk] *= np.linspace(0, 1, atk)
    s = np.zeros_like(tt)
    for k in range(1, partials+1):
        s += (1.0/k)*np.sin(2*np.pi*k*f*tt + phase)
    return g*s*env

# ---- THE COUNT (trivial): a sustained drone, the fixed point, never moves.
f0 = 55.0
drone = (np.sin(2*np.pi*f0*t)
         + 0.30*np.sin(2*np.pi*2*f0*t)
         + 0.12*np.sin(2*np.pi*3*f0*t)     # 165: where the fold lives
         + 0.06*np.sin(2*np.pi*4*f0*t))    # 220: where the winding lives
fi = int(2.0*sr)
drone[:fi] *= np.linspace(0, 1, fi)
fo = int(4.0*sr)
drone[-fo:] *= np.linspace(1, 0, fo)
drone *= 0.42

# ---- THE FOLD (sign): a ring at 165 (the drone's 3rd partial). In phase at
# the turns, PHASE-FLIPPED at the mirrors -> against the drone's 165 it dips,
# the fold. In the MID, so mono keeps it.
mid = np.zeros(n)
mid += drone
for i, sname in enumerate(steps):
    sgn, _ = vals[sname]
    tt0 = int((2.0 + i*step)*sr)
    r = ring(165.0, 4.0, phase=0.0 if sgn > 0 else np.pi, partials=5, g=0.34)
    rr = min(len(r), n-tt0)
    mid[tt0:tt0+rr] += r[:rr]

# ---- THE WINDING (standard): 220 (the drone's 4th partial), in the SIDE.
# trace 2 at e  ->  doubled (220 + 440);  trace -1 at the turns -> inverted;
# trace 0 at the mirrors -> silence. Mono drops the whole voice.
side = np.zeros(n)
for i, sname in enumerate(steps):
    _, std = vals[sname]
    if std == 0:
        continue
    tt0 = int((2.0 + i*step)*sr)
    if std == 2:
        r = ring(220.0, 4.5, phase=0.0, partials=5, g=0.30)
        r += ring(440.0, 4.5, phase=0.0, partials=4, g=0.18)
    else:  # -1: inverted
        r = ring(220.0, 4.5, phase=np.pi, partials=5, g=0.30)
    rr = min(len(r), n-tt0)
    side[tt0:tt0+rr] += r[:rr]

# ---- stereo: L = mid + side, R = mid - side. mono = mid.
L = mid + side
R = mid - side
stereo = np.stack([L, R], axis=1)
stereo = np.tanh(stereo*1.1)*0.95
pcm = (stereo*32767.0).astype(np.int16)
with wave.open("assets/character-table.wav", "wb") as wf:
    wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(sr)
    wf.writeframes(pcm.tobytes())

mono = np.stack([mid, mid], axis=1)
mono_pcm = (np.tanh(mono*1.1)*0.95*32767.0).astype(np.int16)
with wave.open("assets/character-table-mono.wav", "wb") as wf:
    wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(sr)
    wf.writeframes(mono_pcm.tobytes())

print("wrote assets/character-table.wav", dur, "s")
print("side energy (stereo-only):", round(float(np.sqrt(np.mean(side**2))), 4))
print("mono = mid exactly; the winding (side) is dropped, the fold stays.")
