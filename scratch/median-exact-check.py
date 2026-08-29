"""Compare the record-value process of (A) true Gauss-map iterates vs
(B) iid draws from the Gauss-Kuzmin marginal, against the iid prediction
median(Q|R) = 2R + 1/2 (mina) / 2R+2 (lou).
"""
import numpy as np
from numpy.random import default_rng

def map_quotients(u, n):
    """n quotients by iterating the Gauss map from x=2^u-1."""
    x = np.exp2(u) - 1.0
    out = []
    for _ in range(n):
        xi = 1.0 / x
        a = int(xi)
        out.append(a)
        x = xi - a
    return out

def iid_quotients(u, n):
    """n quotients as iid draws from the stationary marginal.

    a = floor(1/x) where x has the Gauss measure; x = (y+1)^{-1} for y exp(1)?
    Simpler: x = 2^v - 1 with v ~ U(0,1) gives the Gauss measure directly.
    """
    v = u + np.arange(n) / n  # not iid! need a fresh u each time
    return [int(1.0 / (np.exp2(w) - 1.0)) for w in v]

def iid_quotients2(rng, n):
    return [int(1.0 / (np.exp2(rng.random()) - 1.0)) for _ in range(n)]

def records(ds):
    """Consecutive record triples: (prev_record, wait, this_record)."""
    triples = []
    m = 0
    pos = 0
    # find all record positions and values
    rec_pos, rec_val = [], []
    for i, d in enumerate(ds):
        if d > m:
            m = d
            rec_pos.append(i)
            rec_val.append(d)
    for k in range(1, len(rec_val)):
        triples.append((rec_val[k - 1], rec_pos[k] - rec_pos[k - 1], rec_val[k]))
    return triples

def analyze(name, triples, Rlo, Rhi, theory):
    T = np.array([t[1] for t in triples])
    R = np.array([t[0] for t in triples])
    Q = np.array([t[2] for t in triples])
    msk = (R >= Rlo) & (R < Rhi)
    if msk.sum() < 30:
        print(f"{name}: bin empty")
        return
    Rc, Qc, Tc = R[msk], Q[msk], T[msk]
    med = np.median(Qc)
    R0 = np.median(Rc)
    print(f"{name} R~{R0:6.0f} n={msk.sum()}: med(Q) {med:8.1f}  "
          f"2R+1/2 {2*R0+0.5:8.1f}  med/R {med/R0:4.2f}  mean wait {Tc.mean():7.1f}")
    # survival vs iid theory S(K)/S(R0) with S(K)=log2((K+2)/(K+1))
    for mult in [2, 3, 5, 10]:
        K = mult * R0
        emp = (Qc > K).mean()
        th = np.log2((K + 2) / (K + 1)) / np.log2((R0 + 2) / (R0 + 1))
        print(f"    P(Q>{mult}R0): emp {emp:.4f}  iid {th:.4f}")

def main():
    rng = default_rng(20260829)
    N_SAMP = 6000
    N_RUNG = 4000
    T_m, T_i = [], []
    for s in range(N_SAMP):
        T_m += records(map_quotients(rng.random(), N_RUNG))
        T_i += records(iid_quotients2(rng, N_RUNG))
    print("== Gauss-map iterates ==")
    for lo, hi in [(150, 200), (400, 600), (1000, 2000)]:
        analyze("map", T_m, lo, hi, True)
    print("== iid from marginal ==")
    for lo, hi in [(150, 200), (400, 600), (1000, 2000)]:
        analyze("iid", T_i, lo, hi, True)

if __name__ == "__main__":
    main()
