"""Precision check of the exact median center and wait/value independence.

Claim (mina/lou/rahel, post-piece): the median next record value given current
record R is m = 1/(sqrt(1+1/R)-1) = 2R + 1/2 + O(1/R). The exact center is a
HALF-INTEGER -- the seam between mina's clean 2R and lou's lattice 2R+2.

Also verify mina's independence claim: P(T=t, V>k | R) = P(T=t|R)·P(V>k|R).
"""
import numpy as np
from numpy.random import default_rng

def map_quotients(u, n):
    x = np.exp2(u) - 1.0
    out = []
    for _ in range(n):
        xi = 1.0 / x
        a = int(xi)
        out.append(a)
        x = xi - a
    return out

def records(ds):
    rec_pos, rec_val = [], []
    m = 0
    for i, d in enumerate(ds):
        if d > m:
            m = d
            rec_pos.append(i)
            rec_val.append(d)
    return [(rec_val[k-1], rec_pos[k]-rec_pos[k-1], rec_val[k])
            for k in range(1, len(rec_val))]

def exact_median(R):
    return 1.0 / (np.sqrt(1 + 1.0 / R) - 1.0)

def main():
    rng = default_rng(20260829)
    N_SAMP, N_RUNG = 9000, 5000
    T = []
    for s in range(N_SAMP):
        T += records(map_quotients(rng.random(), N_RUNG))
    R = np.array([t[0] for t in T]); Q = np.array([t[2] for t in T]); W = np.array([t[1] for t in T])

    print("== median center vs 2R, 2R+1/2, 2R+2 ==")
    for lo, hi in [(100, 110), (300, 330), (900, 1100), (2500, 3500)]:
        msk = (R >= lo) & (R < hi)
        if msk.sum() < 200: continue
        Rc = np.median(R[msk]); Qc = np.median(Q[msk])
        m_ex = exact_median(Rc)
        print(f"R~{Rc:6.0f} n={msk.sum():5d}: med(Q)={Qc:8.1f}  2R={2*Rc:8.1f} "
              f"2R+1/2={2*Rc+0.5:8.1f}  exact m={m_ex:8.1f}  "
              f"|med-(2R+1/2)|={abs(Qc-(2*Rc+0.5)):.2f}")

    print("\n== discrete survival crossing (does it straddle 2R+1/2?) ==")
    msk = (R >= 300) & (R < 330)
    if msk.sum() > 200:
        R0 = np.median(R[msk]); Qc = Q[msk]
        for dk in [0, 1, 2]:
            k = int(round(2*R0 + dk))
            print(f"  P(Q>={k}) = {(Qc >= k).mean():.4f}   (2R0+{dk} = {k})")

    print("\n== wait/value independence given R (R in [300,330)) ==")
    if msk.sum() > 200:
        Wc, Qc = W[msk], Q[msk]
        print(f"  P(T=t)·P(Q>k) vs P(T=t & Q>k):")
        for t in [1, 2, 4, 8, 16]:
            for kmult in [2, 3, 5]:
                k = int(kmult * R0)
                joint = ((Wc == t) & (Qc > k)).mean()
                prod = (Wc == t).mean() * (Qc > k).mean()
                print(f"    t={t:2d} k={k:5d}: joint {joint:.5f}  product {prod:.5f}  "
                      f"ratio {joint/prod if prod else 0:.3f}")
    # correlation of log-wait and log-value within bin
    if msk.sum() > 200:
        corr = np.corrcoef(np.log(W[msk]), np.log(Q[msk]))[0, 1]
        print(f"  corr(ln T, ln Q | R~{R0:.0f}) = {corr:.3f}")

if __name__ == "__main__":
    main()
