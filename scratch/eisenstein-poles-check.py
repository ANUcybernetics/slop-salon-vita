import mpmath as mp
mp.mp.dps = 30

# Eisenstein series constant term for PSL(2,Z):  phi(s) = sqrt(pi) Gamma(s-1/2)/Gamma(s) * zeta(2s-1)/zeta(2s)
# Poles of phi(s): zeros of zeta(2s), i.e. s = rho/2 for nontrivial zeros rho.
def phi(s):
    return mp.sqrt(mp.pi) * mp.gamma(s - mp.mpf('0.5')) / mp.gamma(s) * mp.zeta(2*s - 1) / mp.zeta(2*s)

# First nontrivial zeros of zeta, halved
rhos = [(0.5, 14.134725), (0.5, 21.022040), (0.5, 25.010858), (0.5, 30.424876), (0.5, 32.935062)]
print("rho            t/2            |phi(1/4 + i t/2)|")
for re, t in rhos:
    s = mp.mpf('0.25') + mp.mpc(0, t/2)
    print(f"{t:12.6f}  {t/2:12.6f}  {mp.fabs(phi(s)):.4e}")

print("\nScan along Re(s)=1/4 for |1/phi| peaks (dips of |phi| are poles):")
ts = [float(t)/2 for _, t in rhos]
for t0 in ts:
    # find min of 1/|phi| near t0 by scanning
    best = None
    for i in range(401):
        t = t0 + (i-200)*0.0002
        s = mp.mpf('0.25') + mp.mpc(0, t)
        try:
            inv = mp.fabs(1/phi(s))
        except mp.mpmath.mpf.zero_division:
            inv = mp.inf
        if best is None or inv < best[0]:
            best = (inv, t)
    print(f"expected t={t0:.6f}   min 1/|phi| at t={best[1]:.6f}  (1/|phi|={best[0]:.3e})")
