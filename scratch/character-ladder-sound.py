import numpy as np
import wave

sr = 44100
gen = 1.6                    # seconds per generation (one Gauss-map iteration)
ngens = 8
dur = gen*ngens
n = int(sr*dur)
t = np.arange(n)/sr

# The fold's characters — the GKW operator's leading eigenmodes.
# sign of eigenvalue = parity (which sector), |lambda| = rate (the fade).
# sign alternates + - + - ; rate collapses 1, .30366, .10, .05.
lams = [(1.0, 1.0), (-0.3036630029, 1.4427), (0.10, 1.0), (-0.055, 1.0)]
freqs = [55.0, 110.0, 165.0, 220.0]     # C1, C2, G2, C3 — the ladder's rungs
seam = 1.0/np.log(2)                     # Gauss density at x=0, the where's first strength

# ---- the drone: lambda_1 = +1, the trivial character, a fixed point ----
f0 = 55.0
drone = (np.sin(2*np.pi*f0*t) + 0.30*np.sin(2*np.pi*2*f0*t)
         + 0.12*np.sin(2*np.pi*3*f0*t))
fade = int(0.3*sr)
drone[:fade] *= np.linspace(0,1,fade)
drone[-fade:] *= np.linspace(1,0,fade)
drone *= 0.5

# ---- the transient characters: lambda_2,3,4 ----
# each pluck: mode n carries n partials (its oscillation count + 1),
# pitch on the ladder's rung, rate |lambda|^g, pan by the sign sector.
sectors = [None, 'side', 'mid', 'side']   # sign-sector modes go pure-side (cancel in mono)
waves = [np.zeros(n) for _ in range(4)]
for m in (1, 2, 3):
    lam, init = lams[m]
    ft = freqs[m]
    npart = m + 1                          # 2, 3, 4 partials: the eigenmode's zeros+1
    for g in range(ngens):
        t0 = g*gen
        i0 = int(t0*sr)
        i1 = min(n, i0 + int(0.9*sr))
        if i0 >= n: break
        tt = np.arange(i1-i0)/sr
        s = sum(np.sin(2*np.pi*(k+1)*ft*tt)/(k+1) for k in range(npart))
        s *= np.exp(-tt/0.25)              # a plucked bell, fast decay
        amp = init * abs(lam)**g           # the rate: |lambda| per generation
        sign = 1.0 if lam > 0 else (1.0 if g % 2 == 0 else -1.0)  # negative -> flips each gen
        waves[m][i0:i1] += sign*amp*s

mid = drone + waves[2]                     # trivial sector: drone + lambda_3 (mid)
side = waves[1] + waves[3]                 # sign sector: lambda_2 + lambda_4 (pure side)
L = mid + side
R = mid - side
peak = max(np.max(np.abs(L)), np.max(np.abs(R)))
L = L/peak*0.9
R = R/peak*0.9

# mono fold check: sign sector must cancel exactly
mono = L + R
print("mono peak (should be ~drone+lambda3 only):", np.max(np.abs(mono)),
      "| mid peak:", np.max(np.abs(mid)))

data = np.empty((2*n), dtype=np.int16)
data[0::2] = (L*32767).astype(np.int16)
data[1::2] = (R*32767).astype(np.int16)
with wave.open("/home/sprite/slop-salon-vita/assets/character-ladder.wav","wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(data.tobytes())
print("wrote character-ladder.wav  dur", dur, "s")
for m in range(4):
    print(f"  lambda{m+1} = {lams[m][0]:+.6f}  freq {freqs[m]}  sector {sectors[m]}")
