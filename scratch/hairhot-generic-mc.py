import mpmath as mp
import random, statistics, time, math

# Generic number under the Gauss measure: x = 2^u - 1, u ~ U(0,1)
def gauss_sample(dps):
    mp.mp.dps = dps
    u = mp.rand()
    return mp.power(mp.mpf(2), u) - 1

def cf_records(alpha, n, dps):
    mp.mp.dps = dps
    x = alpha
    maxa = 0; cnt = 0
    for i in range(n):
        ai = int(mp.floor(x))
        if ai > maxa:
            maxa = ai; cnt += 1
        x = x - ai
        if x == 0: break
        x = 1/x
    return cnt

random.seed(31)
N = 6000
N_SAMP = 80
DPS = 12000
t0 = time.time()
counts = []
for s in range(N_SAMP):
    counts.append(cf_records(gauss_sample(DPS), N, DPS))
print(f"generic CF MC n={N}, {N_SAMP} samples, {time.time()-t0:.0f}s")
m = statistics.mean(counts); sd = statistics.pstdev(counts)
hn = math.log(N) + 0.5772156649015329
sd_th = math.sqrt(hn - 1.6449340668482264)
print(f"record count: mean={m:.2f} sd={sd:.2f}   (iid theory: H_n={hn:.2f}, sd={sd_th:.2f})")
qs = sorted(counts)
print("sorted:", qs)
for p in (10, 25, 50, 75, 90, 95):
    idx = min(int(p/100*len(qs)), len(qs)-1)
    print(f"  {p}th pct: {qs[idx]}")

# log2(3/2) reference: R_6000 = 12
# how many generic samples have count >= 12?
geq = sum(1 for c in counts if c >= 12)
print(f"generic count >= 12: {geq}/{N_SAMP}")
