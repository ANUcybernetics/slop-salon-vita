import random, math, statistics, time

# iid Gauss-Kuzmin model (marginal-only, no dependence):
#   P(a=k) = log2(1+1/k) - log2(1+1/(k+1))
# Sample via inverse CDF using a double-precision trick adequate for the max law.
L = math.log(2.0)

def gk_sample():
    u = random.random()
    # solve P(a <= k) >= u.  P(a<=k) = 1 - log2(1+1/(k+1)) = 1 - log2((k+2)/(k+1))
    # => log2((k+2)/(k+1)) = 1-u  => (k+2)/(k+1) = 2^(1-u)
    r = math.pow(2.0, 1.0 - u)       # r in (1,2]
    k = int((r - 1.0) / (2.0 - r))   # (k+2)/(k+1)=r => k = (2-r)/(r-1) ... careful
    # recompute cleanly: (k+2)/(k+1)=r => k+2 = r(k+1) => k(1-r) = r-2 => k = (r-2)/(1-r) = (2-r)/(r-1)
    k = (2.0 - r)/(r - 1.0)
    return int(math.floor(k)) + 1

def gk_sample_tail():
    # large-k tail alternative: for k large, P(a>k) ~ 1/(k ln2). Sample exactly from that
    # tail for efficiency (used only for max estimates where big values matter).
    u = random.random()  # u in (0,1)
    # P(a > k) ~ 1/(k ln2); invert: u = 1/(k ln2) => k = 1/(u ln2)
    return int(1.0/(u*L))

random.seed(41)

# ---- Test 1: record count in iid-GK at n=6000 should match H_n ----
N = 6000
NS = 200
t0=time.time()
counts=[]
for _ in range(NS):
    maxa=0; cnt=0
    for _ in range(N):
        a = gk_sample_tail()
        if a>maxa: maxa=a; cnt+=1
    counts.append(cnt)
m=statistics.mean(counts); sd=statistics.pstdev(counts)
hn=math.log(N)+0.5772156649015329; sd_th=math.sqrt(hn-1.6449340668482264)
print(f"iid-GK record count n={N}: mean={m:.2f} sd={sd:.2f}  (theory H={hn:.2f} sd={sd_th:.2f})")

# ---- Test 2: max quotient law.  For iid heavy tail P(a>k)~1/(k ln2):
# P(max_a<=x) = (1-1/(x ln2))^n ~ exp(-n/(x ln2)).  median x = n/(ln2 * ln2) ~ 2.08 n
def maxq(n, NS):
    out=[]
    for _ in range(NS):
        mx=0
        for _ in range(n):
            a=gk_sample_tail()
            if a>mx: mx=a
        out.append(mx)
    return sorted(out)

for n in (6000, 250000):
    NS2 = 300 if n==6000 else 60
    t0=time.time()
    qs=maxq(n, NS2)
    med=statistics.median(qs)
    print(f"\nmax quotient n={n}, {NS2} samples: median={med:.0f}  (2.08n={2.08*n:.0f})  mean~n/ln2={n/L:.0f}")
    print("  min/p50/p90/max:", qs[0], qs[len(qs)//2], qs[int(0.9*len(qs))], qs[-1])
    print(f"  ratio median/n={med/n:.2f}, {time.time()-t0:.0f}s")

# locate salon records: 698813, 1138268 relative to n~250k
n=250000; qs=maxq(n, 60)
for v in (698813, 1138268):
    below=sum(1 for q in qs if q<v)/len(qs)
    print(f"\nvalue {v} at n={n}: percentile ~{below*100:.0f} of generic maxima")
