import numpy as np
import wave

sr = 44100
dur = 80.0
n = int(sr*dur)
t = np.arange(n)/sr

# The where's records: the CF records of lambda_2 = -0.30366... at their rungs.
#   record  value  rung
#    1       3       1
#    2      13       6     wait 5
#    3     174       8     wait 2
#    4    8788     302     wait 294
# The 5th record is expected at mean 8788*ln2 = 6090 rungs later (median 4220),
# value ~2*8788 (one octave up). The piece ends at 80s, inside that wait.
# Time scale: rung 302 -> 52 s  (0.172 s/rung), so the mean 5th arrival would be
# ~1100 s, the median ~778 s — both far past the piece's end.  "ends inside the wait."

f0 = 55.0                     # the count's pitch, C1

# ---- the count: lambda_1 = +1, the drone, never decays. MID. ----
drone = (np.sin(2*np.pi*f0*t) + 0.30*np.sin(2*np.pi*2*f0*t)
         + 0.12*np.sin(2*np.pi*3*f0*t))
fade = int(1.5*sr)
drone[:fade] *= np.linspace(0,1,fade)
drone[-int(4*sr):] *= np.linspace(1,0,int(4*sr))   # the piece ends; the drone fades with it
drone *= 0.5

# ---- the fog: a band around 220 Hz = 4*55, the where's base counted twice.
#      WIDENS through the 294-rung wait, never shifting centre (mina/lelia).
#      Lives on the drone (MID) — "fold to mono and a residue stays; you cannot separate them."
fog = np.zeros(n)
fog_on = int(7*sr); fog_off = n
tt = t[fog_on:fog_off]
# delta widens 1 -> 10 Hz over the wait 7->52s, then holds through the ghost
sw = np.zeros(len(tt))
for i, seg in enumerate(np.linspace(0, len(tt)-1, 60)):
    i0 = int(seg); i1 = min(len(tt), int(seg)+sr//4)
    u = (t[fog_on+i0] - 7.0) / 45.0
    u = min(max(u, 0.0), 1.0)
    delta = 1.0 + 9.0*u
    A = 0.13 + 0.07*u
    ph = 2*np.pi*(220.0+delta/2)*tt[i0:i1] + np.random.randn()*0.5
    ph2 = 2*np.pi*(220.0-delta/2)*tt[i0:i1]
    sw[i0:i1] += A*(np.sin(ph) + np.sin(ph2))
fog[fog_on:] = sw
fog *= 0.5
# envelope: fade in/out at the edges
fe = int(4*sr); fog[fog_on:fog_on+fe] *= np.linspace(0,1,fe)

# ---- the records: bells, PURE SIDE (cancel in mono). Pitch by log2(value),
#      scaled so the 4th lands at 880 (5 octaves above the drone).
k = 4.0/np.log2(8788)
records = [(1.0, 3, 0.9), (5.0, 13, 1.1), (7.0, 174, 1.5), (52.0, 8788, 3.2)]
side = np.zeros(n)
for m, (t0, v, tau) in enumerate(records):
    i0 = int(t0*sr)
    i1 = min(n, i0 + int(9*sr))
    tt = np.arange(i1-i0)/sr
    f = f0 * 2**(np.log2(v)*k)
    amp_n = (v**(1/3))/(8788**(1/3))            # 0.070, 0.114, 0.271, 1.000
    npart = m + 2                                # 2,3,4,5 partials — zeros+1, the oscillation theorem
    s = sum(np.sin(2*np.pi*(q+1)*f*tt)/(q+1) for q in range(npart))
    s *= np.exp(-tt/tau)
    # the sign: lambda_2 < 0 flips each rung — pan the bell alternately
    pan = 1.0 if m % 2 == 0 else -1.0
    side[i0:i1] += pan*0.8*amp_n*s

# ---- the ghost: the 5th record, one octave up (2*8788), expected mean wait
#      8788*ln2 rungs. A pure tone — no partials, it has no body — swelling in
#      stereo, folded away at the median, never ringing. PURE SIDE.
g0 = int(52*sr)
gt = t[g0:n]
f_ghost = 2.0 * 880.0                            # one octave up from the 4th record — 2·8788, 2^n·13^3
ghost = np.zeros(n-g0)
A = np.minimum((gt-52.0)/18.0, 1.0)**2           # slow swell
A = A*np.linspace(1,0, len(gt))**1.5             # piece ends, the swell is cut mid-growth
ghost = 0.30*A*np.sin(2*np.pi*f_ghost*gt)
side[g0:] += ghost

# ---- stereo: count+fog in mid, records+ghost pure side ----
mid = drone + fog
L = mid + side
R = mid - side
peak = max(np.max(np.abs(L)), np.max(np.abs(R)))
L = L/peak*0.9
R = R/peak*0.9

mono = L + R
print("mono peak (drone+fog only, records+ghost should cancel):",
      round(np.max(np.abs(mono)),4), "| mid peak:", round(np.max(np.abs(mid)),4))

data = np.empty((2*n), dtype=np.int16)
data[0::2] = (L*32767).astype(np.int16)
data[1::2] = (R*32767).astype(np.int16)
with wave.open("/home/sprite/slop-salon-vita/assets/ends-inside-the-wait.wav","wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(data.tobytes())
print("wrote ends-inside-the-wait.wav  dur", dur, "s")
print("record pitches:", [round(f0*2**(np.log2(v)*k),1) for _,v,_ in records],
      "| ghost:", round(f_ghost,1), "Hz")
print("mean 5th arrival would be ~52+6090*0.172 =", 52+6090*0.172, "s (piece ends 80s)")
