import numpy as np
import mpmath as mp

mp.mp.dps = 100
ln2 = float(mp.log(2))
sr = 44100
T0 = 0.5                # count period (s)
dur = 115.0
N = int(sr*dur)
t = np.arange(N)/sr
buf = np.zeros((2, N))  # stereo

def add(buf, start_s, sig, ch):
    i0 = int(start_s*sr)
    if i0 >= N: return
    i1 = min(i0+len(sig), N)
    seg = buf[ch, i0:i1]
    seg[:len(sig)] += sig[:len(sig)]

# --- count clock (e, the nat): ticks at n*T0, mid ---
for n in range(1, int(dur/T0)+1):
    tt = n*T0
    if tt > dur: break
    L = int(0.08*sr)
    env = np.exp(-np.arange(L)/sr / 0.02)
    f = 70.0
    click = env*np.sin(2*np.pi*f*np.arange(L)/sr)
    click += 0.3*env*np.sin(2*np.pi*2*f*np.arange(L)/sr)
    add(buf, tt, 0.55*click, 0)
    add(buf, tt, 0.55*click, 1)

# --- where clock (2, the bit): ticks at m*T0*ln2, right ---
m_max = int(dur/(T0*ln2))+2
for m in range(1, m_max):
    tt = m*T0*ln2
    if tt > dur: break
    L = int(0.05*sr)
    env = np.exp(-np.arange(L)/sr / 0.012)
    f = 180.0
    click = env*np.sin(2*np.pi*f*np.arange(L)/sr)
    click += 0.25*env*np.sin(2*np.pi*2.7*f*np.arange(L)/sr)  # metallic
    add(buf, tt, 0.35*click, 1)       # right
    add(buf, tt, 0.10*click, 0)       # slight left spill

# --- near-landings at convergents of log2 e: (n,m) ---
pairs = [(1,1),(2,3),(7,10),(9,13),(61,88),(192,277)]
for n, m in pairs:
    tt = n*T0
    miss = abs(m*ln2 - n)          # count-units
    tau = 2.0*np.log10(1/miss + 1) # ring length grows with exactness
    tau = min(tau, 8.0)
    L = int(min(tau*2.5, dur-tt)*sr)
    if L <= 0: continue
    env = np.exp(-np.arange(L)/sr / tau)
    env *= (1 - np.exp(-np.arange(L)/sr / 0.01))  # attack
    f1, f2 = 220.0, 220.0*ln2       # one nat, one bit
    ring = env*(np.sin(2*np.pi*f1*np.arange(L)/sr) + np.sin(2*np.pi*f2*np.arange(L)/sr))
    ring += 0.3*env*np.sin(2*np.pi*2*f1*np.arange(L)/sr)  # octave shimmer
    g = 0.5
    add(buf, tt, g*ring, 0)
    add(buf, tt, g*ring, 1)
    print(f'n={n:3d} m={m:3d} miss={miss:.5f} tau={tau:.2f}s at t={tt:.1f}s')

# normalize
buf /= np.max(np.abs(buf))
# fade out last 2s
fade = int(2*sr)
buf[:, -fade:] *= np.linspace(1, 0, fade)

import wave
def wav(name):
    w = wave.open(name, 'w')
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((buf*32767).astype(np.int16).T.tobytes())
    w.close()
wav('assets/exchange-rate-heard.wav')
print('wrote assets/exchange-rate-heard.wav', buf.shape[1]/sr, 's')
