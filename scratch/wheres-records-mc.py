"""The where's records (Aug 29): verify λ₂ CF records + quantify the wait/weight.

λ₂ = Wirsing constant, -0.303663... The CF records are 3@1, 13@6, 174@8,
8788@302, nothing larger to rung 387 (verified against the OEIS A007515 b-file).

Getting λ₂'s digits: the OEIS A007515 entry's %o PARI line carries Briggs's
382-digit decimal; walking it with Decimal(prec=520) reproduces the whole
388-term b-file. The 5th record is beyond rung 387 and needs 480+ digits.

The wait/weight statistics below are Monte Carlo over stationary Gauss-measure
digit sequences (draw u~U(0,1), x=2^u-1, iterate the Gauss map). Results:
- 4th-record position: median rung 24, p90 140, P(>302) ~ 2%
- max partial quotient by rung 302: median ~ n/ln²2 = 629, P(>=8788) ~ 5%
- record count by rung 302: median 6, P(<=4) ~ 24%

Dead end recorded for future: the monomial-zeta matrix
A[m,k]=(-1)^m C(k+1+m,m) zeta(k+2+m) is catastrophically ill-conditioned at
mpmath precision (small eigenvalues collapse to ~0). Don't retry without a
balanced basis.
"""
import numpy as np

def stationary_digits(u, n):
    """n Gauss-measure digits of a stationary CF, starting from u~U(0,1)."""
    x = np.exp2(u) - 1.0
    out = []
    for _ in range(n):
        xi = 1.0 / x
        a = int(xi)
        out.append(a)
        x = xi - a
    return out

def record_stats(n_samp=40000, n_rung=400):
    rng = np.random.default_rng(20260829)
    pos4, max302, cnt302 = [], np.empty(n_samp), np.empty(n_samp, dtype=int)
    for s in range(n_samp):
        ds = stationary_digits(rng.random(), n_rung)
        m = cnt = p4 = 0
        for i, d in enumerate(ds):
            if d > m:
                m = d; cnt += 1
                if cnt == 4 and p4 == 0:
                    p4 = i + 1
        if p4: pos4.append(p4)
        max302[s] = max(ds[:302])
        m = cnt = 0
        for d in ds[:302]:
            if d > m: m = d; cnt += 1
        cnt302[s] = cnt
    pos4 = np.array(pos4)
    print(f"4th-record position: median {np.median(pos4):.0f}, p90 {np.percentile(pos4,90):.0f}, "
          f"P(>302)={(pos4 > 302).mean():.3f}")
    print(f"max@302: median {np.median(max302):.0f} (n/ln²2={302/np.log(2)**2:.0f}), "
          f"P(>=8788)={(max302 >= 8788).mean():.3f}")
    print(f"record count@302: median {np.median(cnt302):.0f}, P(<=4)={(cnt302 <= 4).mean():.3f}")

if __name__ == "__main__":
    record_stats()
