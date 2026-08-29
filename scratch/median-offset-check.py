"""Pin down the exact median offset: med(Q|R) - 2R = ?

mina: 2R+1/2 (weak-tail convention m=1/(sqrt(1+1/R)-1))
strict >: 2R+1   (from log2((K+2)/(K+1)) tail)
lou: 2R+2 (lattice shift)

Use tight R bins and lots of samples; measure median of Q in each bin and
subtract 2*R_mid.
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

def main():
    rng = default_rng(20260829)
    N_SAMP, N_RUNG = 12000, 8000
    T = []
    for s in range(N_SAMP):
        T += records(map_quotients(rng.random(), N_RUNG))
    R = np.array([t[0] for t in T]); Q = np.array([t[2] for t in T])

    print("tight bins: med(Q) - 2R_center")
    for lo, hi in [(190, 210), (490, 510), (990, 1010), (1990, 2010)]:
        msk = (R >= lo) & (R <= hi)
        n = msk.sum()
        if n < 100: print(f"[{lo},{hi}] n={n} skip"); continue
        Rm = R[msk].mean(); Qm = np.median(Q[msk])
        print(f"[{lo},{hi}] n={n:5d}: Rbar={Rm:6.1f} med(Q)={Qm:7.1f} "
              f"med-2R={Qm-2*Rm:+6.2f}  2R+1/2-2R={0.5:+4.1f}  2R+1-2R={1.0:+4.1f}")

    # exact survival crossing vs theory with strict tail
    msk = (R >= 990) & (R <= 1010)
    if msk.sum() > 100:
        Qc = Q[msk]; R0 = R[msk].mean()
        print(f"\nP(Q > K) for R~{R0:.0f}, theory = log2((K+2)/(K+1))/log2((R+2)/(R+1)):")
        for mult in [2.0, 2.02, 2.05]:
            K = mult * R0
            emp = (Qc > K).mean()
            th = np.log2((K+2)/(K+1)) / np.log2((R0+2)/(R0+1))
            print(f"  K={mult:.2f}R0={K:6.0f}: emp {emp:.4f} th {th:.4f}")

if __name__ == "__main__":
    main()
