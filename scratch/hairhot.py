import mpmath as mp
import math, time, json

t0 = time.time()
# ---- Part 1: log2(3/2) CF, record counts at many scales ----
NMAX = 30000
mp.mp.dps = 60000
alpha = mp.log(mp.mpf(3)/2)/mp.log(2)

x = alpha
a = []
for i in range(NMAX):
    ai = int(mp.floor(x)); a.append(ai)
    x = x - ai
    if x == 0:
        break
    x = 1/x
n = len(a)
print(f"log2(3/2): {n} terms, {time.time()-t0:.1f}s")

# running max (records) and record count at every index
records = []          # (index, value)
maxa = 0
for i in range(n):
    if a[i] > maxa:
        maxa = a[i]; records.append((i, int(a[i])))
print(f"total records: {len(records)}")
print("records (i, a):", records)

def H(n):
    # harmonic number exact-ish
    return math.log(n) + 0.5772156649015329
def H2(n):
    # sum 1/k^2 -> pi^2/6
    return 1.6449340668482264

def rcount_upto(nidx):
    # number of records with index < nidx
    return sum(1 for i, v in records if i < nidx)

scales = [500, 1000, 2000, 5000, 10000, 20000, 30000]
print("\nscale  R_n    H_n     sd      z")
for s in scales:
    if s > n: break
    R = rcount_upto(s)
    hn = H(s)
    var = hn - H2(s)
    sd = math.sqrt(var)
    z = (R - hn)/sd
    print(f"{s:>6}  {R:>3}   {hn:5.2f}  {sd:5.2f}   {z:+.2f}")

json.dump({'n': n, 'records': records}, open('scratch/hairhot-data.json', 'w'), indent=1)
print(f"\nelapsed {time.time()-t0:.1f}s")
