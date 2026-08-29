"""Verify wait-after-record law, vectorized across samples.

Theory: P(a_n >= R) ~ 1/(R ln2) (Gauss-Kuzmin tail), so the wait to beat
record R is ~ Geometric(p), p = 1/(R ln2): mean R ln2, median R (ln2)^2,
p90 = R ln2 ln(10).
"""
import numpy as np
ln2 = np.log(2)

def first_exceed_waits(R, n_samp, max_wait):
    rng = np.random.default_rng(20260829)
    x = np.exp2(rng.random(n_samp)) - 1.0      # stationary start
    waits = np.full(n_samp, -1, dtype=np.int64)
    done = np.zeros(n_samp, dtype=bool)
    for k in range(1, max_wait + 1):
        xi = 1.0 / x
        a = xi.astype(np.int64)
        hit = (~done) & (a > R)
        if hit.any():
            waits[hit] = k
            done |= hit
            if done.all():
                break
        x = xi - a
    return waits[waits > 0]

# tail check first: P(a >= R) over a long stationary sample
def tail_check(n=4_000_000):
    rng = np.random.default_rng(7)
    x = np.exp2(rng.random()) - 1.0
    R = 8788
    # walk the map, count exceedances
    cnt = 0
    for _ in range(n):
        xi = 1.0 / x
        a = int(xi)
        if a >= R:
            cnt += 1
        x = xi - a
    p_emp = cnt / n
    print(f"P(a>={R}): empirical {p_emp:.6e}   GK tail 1/(R ln2) = {1/(R*ln2):.6e}")

tail_check()

for R in [174, 8788, 50000]:
    w = first_exceed_waits(R, n_samp=4000, max_wait=int(R*ln2*15))
    pred_mean = R * ln2
    pred_med = R * ln2**2
    print(f"R={R}: mean wait {w.mean():.0f} (pred {pred_mean:.0f}) | "
          f"median {np.median(w):.0f} (pred {pred_med:.0f}) | "
          f"p90 {np.percentile(w,90):.0f} (pred {pred_mean*np.log(10):.0f}) | n={len(w)}")
