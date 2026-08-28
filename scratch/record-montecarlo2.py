import mpmath as mp
import random, statistics, time

# Sample alpha from the Gauss measure: x = 2^u - 1, u~Uniform(0,1), at high precision.
def gauss_measure_sample(dps):
    mp.mp.dps = dps
    u = mp.rand()          # mpmath uniform [0,1] at dps
    return mp.power(mp.mpf(2), u) - 1

def cf_records(alpha, n, dps):
    mp.mp.dps = dps
    x = alpha
    maxa = 0
    cnt = 0
    for i in range(n):
        ai = int(mp.floor(x))
        if ai > maxa:
            maxa = ai
            cnt += 1
        x = x - ai
        if x == 0:
            break
        x = 1/x
    return cnt

# log2(3/2) proper (mp throughout)
mp.mp.dps = 10000
alpha_l = mp.log(mp.mpf(3)/2)/mp.log(2)
for n in (500, 1500, 6000):
    x = alpha_l
    maxa = 0; cnt = 0
    for i in range(n):
        ai = int(mp.floor(x))
        if ai > maxa:
            maxa = ai; cnt += 1
        x = x - ai
        if x == 0: break
        x = 1/x
    print(f"log2(3/2) records by n={n}: {cnt}")

# Monte Carlo at n=1500, dps=4000
random.seed(7)
mp.mp.dps = 4000
n = 1500
N_SAMP = 150
counts = []
t0 = time.time()
for s in range(N_SAMP):
    counts.append(cf_records(gauss_measure_sample(4000), n, 4000))
print(f"\nMC (Gauss measure, high prec) n={n}, {N_SAMP} samples, {time.time()-t0:.0f}s")
print(f"record count: mean={statistics.mean(counts):.2f}, sd={statistics.pstdev(counts):.2f}, "
      f"min={min(counts)}, max={max(counts)}")
qs = sorted(counts)
for p in (10, 25, 50, 75, 90):
    idx = min(int(p/100*len(qs))-1, len(qs)-1)
    print(f"  {p}th pct: {qs[idx]}")
