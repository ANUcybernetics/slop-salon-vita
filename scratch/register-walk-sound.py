#!/usr/bin/env python3
"""The register walk, heard — the census as sound.

1200 Gram gaps on the critical line, one ring per gap, never touching. 56
times the alternation trips: a gap comes back empty, the next holds two rings
a comma apart, beating — the near-fusion refused. Every trip is a unit dipole:
the vacancy and its doubling share the seat, zero width, the register walk
W(n) = sum(count-1) stays in {-1, 0, +1} and returns to zero. The count never
moves.

The piece maps gap -> time (8 gaps/sec, ~2:30). The drone is the -1, the base
counted once, held under everything. The perfect gaps are a soft regular ring,
centre. Each trip is a stereo excursion: the vacancy is a dry thud on the side
the walk stepped (left for a vacancy-first trip, centre for double-first), the
doubling is two rings a comma apart, ringing long, the beat rate set by the
near-fused ring's miss to its seat — tightest miss, slowest beat, the fusion
held a hair off, never landing. The walk returns to centre after every trip:
mono keeps the count, stereo hears the excursions. The trips densify with
height (11 / 19 / 22 per four hundred).
"""
import numpy as np
import mpmath as mp
from scipy.io import wavfile

SR = 44100
GAP_RATE = 8.0                 # gaps per second
PAD = 3.0
F0 = 660.0                     # the ring tone
DRONE = 110.0
COMMA_CENTS = 23.46            # one Pythagorean comma
MAX_MISS = 0.2342              # loosest miss in the census (for scaling)

mp.mp.dps = 15
N_GAPS = 1200

print("computing zeros...")
gams = np.array([float(mp.zetazero(k).imag) for k in range(1, N_GAPS + 61)])
print("computing gram points...")
grams = np.array([float(mp.grampoint(n)) for n in range(N_GAPS + 2)])

counts = []
lo = 0
for n in range(1, N_GAPS + 1):
    a, b = grams[n], grams[n + 1]
    while lo < len(gams) and gams[lo] <= a:
        lo += 1
    c = 0
    j = lo
    while j < len(gams) and gams[j] < b:
        c += 1
        j += 1
    counts.append(c)
counts = np.array(counts)

# register walk after each gap
walk = np.cumsum(counts - 1)

# dipole excursions: (start_gap, end_gap, orient), all zero-width
exc = []
i = 0
while i < N_GAPS:
    if walk[i] == 0:
        i += 1
        continue
    orient = "v" if walk[i] == -1 else "d"
    s = i
    while i < N_GAPS and walk[i] != 0:
        i += 1
    exc.append((s, i - 1, orient))

def spacing(t):
    return 2.0 * np.pi / np.log(t / (2.0 * np.pi))

# miss of the near-fused ring (a doubled ring) to its seat, per dipole
dip_miss = {}
for s, e, o in exc:
    best = 1e9
    for n in (s, e):
        a, b = grams[n], grams[n + 1]
        for z in gams:
            if a < z < b:
                best = min(best, abs(z - a), abs(z - b))
    dip_miss[(s, e, o)] = best / spacing(grams[s])

# stacked blocks (4-gap clusters)
slips = [(n, counts[n - 1]) for n in range(1, N_GAPS + 1) if counts[n - 1] != 1]
groups = []
for n, c in slips:
    if groups and n - groups[-1][-1][0] == 1:
        groups[-1].append((n, c))
    else:
        groups.append([(n, c)])
blocks = [g for g in groups if len(g) > 2]

print(f"{len(exc)} dipoles | blocks {[[n for n, _ in g] for g in blocks]}")

TOTAL = PAD + N_GAPS / GAP_RATE + 4.0
n = int(SR * TOTAL)
t = np.arange(n) / SR
L = np.zeros(n)
R = np.zeros(n)

def gap_time(g):
    return PAD + (g - 1) / GAP_RATE

def smooth(r):
    return 0.5 - 0.5 * np.cos(np.pi * np.clip(r, 0, 1))

def ramp(x, t0, t1):
    return np.clip((x - t0) / (t1 - t0), 0.0, 1.0)

env = smooth(ramp(t, 0, 1.5)) * smooth(1 - ramp(t, TOTAL - 2.0, TOTAL))

def pan(p):
    th = (p + 1.0) * np.pi / 4.0
    return np.cos(th), np.sin(th)

# --- the drone: the -1, the base, the count that never moves --------------
drone = 0.05 * env * (np.sin(2*np.pi*DRONE*t) + 0.4*np.sin(2*np.pi*2*DRONE*t))
L += drone
R += drone

def add_ring(buf_L, buf_R, tc, f, tau, gain, p, npartial=3):
    """a bell ring at time tc, frequency f, decay tau, panned by p.
    Computed over a local window so 1200 events stay cheap."""
    win = tau * 6.0 + 0.3
    i0 = int(tc * SR)
    i1 = min(n, int((tc + win) * SR) + 1)
    if i1 <= i0:
        return
    ts = t[i0:i1]
    dt = ts - tc
    a = smooth(ramp(ts, tc, tc + 0.02))
    body = a * np.where(dt > 0, np.exp(-np.maximum(dt, 0) / tau), 0.0)
    snd = np.zeros_like(ts)
    for k in range(1, npartial + 1):
        amp = [1.0, 0.4, 0.2][k - 1]
        snd += amp * np.sin(2*np.pi*k*f*ts)
    snd *= body * gain
    gl, gr = pan(p)
    buf_L[i0:i1] += gl * snd
    buf_R[i0:i1] += gr * snd

def add_thud(buf_L, buf_R, tc, gain, p):
    """the vacancy: a dry knock, the seat sounding alone, fast decay."""
    win = 0.6
    i0 = int(tc * SR)
    i1 = min(n, int((tc + win) * SR) + 1)
    if i1 <= i0:
        return
    ts = t[i0:i1]
    dt = ts - tc
    a = smooth(ramp(ts, tc, tc + 0.004))
    body = a * np.where(dt > 0, np.exp(-np.maximum(dt, 0) / 0.09), 0.0)
    snd = body * gain * (
        np.sin(2*np.pi*165.0*ts) + 0.35*np.sin(2*np.pi*2*165.0*ts))
    gl, gr = pan(p)
    buf_L[i0:i1] += gl * snd
    buf_R[i0:i1] += gr * snd

# --- the ring train --------------------------------------------------------
# one short soft ring per perfect gap, centre. at the 52 trips a ring is
# missing (the hole) and the next gap rings twice, a comma apart, beating.
ndouble = 0
for g in range(1, N_GAPS + 1):
    c = counts[g - 1]
    w = walk[g - 1]
    tc = gap_time(g)
    if c == 1:
        add_ring(L, R, tc, F0, 0.06, 0.05, 0.0)
    elif c == 0:
        add_thud(L, R, tc, 0.11, 0.7 * w)
    elif c == 2:
        # find the miss of this doubling's near-fused ring
        m = 0.0677  # mean fallback
        for (s, e, o) in exc:
            if s <= g - 1 <= e:
                m = dip_miss[(s, e, o)]
                break
        # the near-fused twin sits at a fraction of a comma; tighter miss,
        # slower beat, longer ring — the fusion held a hair off, never landing.
        frac = m / MAX_MISS
        delta = (2 ** (COMMA_CENTS / 1200.0) - 1) * frac
        f2 = F0 * (1.0 + delta)
        tau = float(np.clip(2.2 * (MAX_MISS / m) ** 0.3, 2.2, 6.0))
        add_ring(L, R, tc, F0, tau, 0.09, 0.7 * w)
        add_ring(L, R, tc, f2, tau, 0.09, 0.7 * w)
        ndouble += 1

# --- normalize and write ---------------------------------------------------
track = np.column_stack([L, R])
def norm(x, peak=0.82):
    return peak * x / (np.max(np.abs(x)) + 1e-9)

out = "/home/sprite/slop-salon-vita/assets/register-walk.wav"
wavfile.write(out, SR, norm(track).astype(np.float32))
print(f"wrote {out}  {track.shape[0]/SR:.1f} s | {ndouble} doubled gaps, "
      f"{len(exc)} dipoles | block sites {[[n for n,_ in g] for g in blocks]}")
