import mpmath as mp
import random, statistics

# Sample alpha from the Gauss measure (density 1/((1+x)ln2) on [0,1]) via inverse CDF:
# F(x) = log2(1+x), so x = 2^u - 1 with u ~ Uniform(0,1).
def gauss_measure_sample():
    u = random.random()
    return 2.0**u - 1.0

def cf_records(alpha, n, dps=4000):
    mp.mp.dps = dps
    x = mp.mpf(alpha)
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

# log2(3/2) record count by n
alpha_l = float(mp.log(mp.mpf(3)/2)/mp.log(2))
for n in (500, 1500, 6000):
    mp.mp.dps = 10000
    x = mp.mpf(alpha_l)
    maxa = 0; cnt = 0
    for i in range(n):
        ai = int(mp.floor(x))
        if ai > maxa:
            maxa = ai; cnt += 1
        x = x - ai
        if x == 0: break
        x = 1/x
    print(f"log2(3/2) records by n={n}: {cnt}")

# Monte Carlo at n=1500
random.seed(7)
n = 1500
N_SAMP = 200
counts = []
t0 = time.time() if False else None
import time
t0 = time.time()
for s in range(N_SAMP):
    counts.append(cf_records(gauss_measure_sample(), n, dps=4000))
print(f"\nMC n={n}, {N_SAMP} samples, {time.time()-t0:.0f}s")
print(f"record count: mean={statistics.mean(counts):.2f}, sd={statistics.pstdev(counts):.2f}, "
      f"min={min(counts)}, max={max(counts)}")
qs = sorted(counts)
for p in (10, 25, 50, 75, 90):
    print(f"  {p}th pct: {qs[int(p/100*len(qs))-1]}")
