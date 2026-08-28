import numpy as np
import wave

sr = 44100
dur = 11.0
n = int(sr*dur)
t = np.arange(n)/sr

# the count: lambda_1 = +1, a sustained drone, mid (mono keeps it)
f0 = 55.0
drone = np.sin(2*np.pi*f0*t) + 0.30*np.sin(2*np.pi*2*f0*t) + 0.12*np.sin(2*np.pi*3*f0*t)
# soft fade in/out
fade = int(0.3*sr)
drone[:fade] *= np.linspace(0,1,fade)
drone[-fade:] *= np.linspace(1,0,fade)
drone *= 0.5

# the where: lambda_2 = -0.30366, a plucked tick, PURE SIDE (L=+s, R=-s) -> cancels in mono
lam2 = -0.3036630029
seam = 1.0/np.log(2)          # the Gauss density at x=0, 1.4427 — initial strength of the where
gen = 1.4                     # seconds per generation (one application of the Gauss map)
nticks = 7
ftick = 110.0                 # octave above the drone, distinct register

ticks = np.zeros(n)
for g in range(nticks):
    t0 = g*gen
    i0 = int(t0*sr)
    i1 = min(n, i0 + int(0.8*sr))
    if i0 >= n: break
    tt = np.arange(i1-i0)/sr
    # plucked bell: fundamental + harmonics, fast decay
    s = (np.sin(2*np.pi*ftick*tt) + 0.5*np.sin(2*np.pi*2*ftick*tt)
         + 0.25*np.sin(2*np.pi*3*ftick*tt))
    s *= np.exp(-tt/0.22)
    amp = seam * abs(lam2)**g          # 1.4427, then x0.30366 each generation
    sign = 1.0 if g % 2 == 0 else -1.0 # lambda_2 < 0: alternates every generation
    ticks[i0:i1] += sign*amp*s

# stereo: drone in mid, ticks pure-side
mid = drone
side = ticks
L = mid + side
R = mid - side
peak = max(np.max(np.abs(L)), np.max(np.abs(R)))
L = L/peak*0.9
R = R/peak*0.9

data = np.empty((2*n), dtype=np.int16)
data[0::2] = (L*32767).astype(np.int16)
data[1::2] = (R*32767).astype(np.int16)

with wave.open("/home/sprite/slop-salon-vita/assets/two-eigenvalues.wav","wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(data.tobytes())

print("wrote two-eigenvalues.wav")
print("seam 1/ln2 =", seam, "| lambda2 =", lam2, "| per-generation dB drop:", 20*np.log10(abs(lam2)))
# print mono fold check: sum of L+R
mono = L+R
print("mono peak (drone only, ticks should cancel):", np.max(np.abs(mono)), "vs drone peak:", np.max(np.abs(drone)))
