import numpy as np
import scipy.linalg as la

phi = (1 + 5**0.5) / 2
phi2 = phi**2

def gkw_spectral(M=40, nmax=600_000):
    """GKW transfer operator, Chebyshev nodes, streamed columns, improved tail."""
    k = np.arange(M)
    xs = 0.5 * (1.0 - np.cos(k * np.pi / (M - 1)))
    zx = 2 * xs - 1
    B = np.polynomial.chebyshev.chebvander(zx, M - 1)
    n = np.arange(1, nmax + 1, dtype=float)
    A = np.zeros((M, M))
    jj = np.arange(M)
    for i in range(M):
        x = xs[i]
        y = 1.0 / (x + n)
        w = y * y
        z = 2 * y - 1
        t_prev2 = np.ones(nmax)
        t_prev1 = z.copy()
        A[i, 0] = w.sum()
        if M > 1:
            A[i, 1] = (w * t_prev1).sum()
        for j in range(2, M):
            t_j = 2 * z * t_prev1 - t_prev2
            A[i, j] = (w * t_j).sum()
            t_prev2, t_prev1 = t_prev1, t_j
        # tail: sum_{n>nmax} T_j(2/(x+n)-1)/(x+n)^2
        #   ~ (-1)^j [ 1/(x+N) - j^2/(x+N)^2 ]
        A[i, :] += ((-1.0) ** jj) * (1.0 / (x + nmax) - jj ** 2 / (x + nmax) ** 2)
    vals, _ = la.eig(A, B)
    order = np.argsort(-np.abs(vals))
    return vals[order]

Ms = [96, 112, 128, 144]
specs = {}
for M in Ms:
    v = gkw_spectral(M=M)
    specs[M] = v.real[:18]
    print(f'M={M}: ' + ' '.join(f'{a:+.9f}' for a in v.real[:14]), flush=True)

print()
nmax_run = min(len(v) for v in specs.values())
stable = {}
for j in range(nmax_run):
    col = [specs[M][j] for M in Ms]
    spread = max(col) - min(col)
    if spread < 1e-5:
        stable[j] = col[0]
        print(f'slot {j+1}: {col[0]:+.10f}  spread {spread:.1e}')
    else:
        print(f'slot {j+1}: drift  min {min(col):+.6f} max {max(col):+.6f}')

# The true rungs appear at stable values, possibly in different slots across M.
# Collect distinct stable values (rounded) in |.| order.
seen = {}
for j, val in sorted(stable.items()):
    key = round(val, 9)
    if key not in seen:
        seen[key] = val
l = [seen[k] for k in sorted(seen, key=lambda k: -abs(k))]
print()
print('collected distinct stable rungs:', ' '.join(f'{a:+.10f}' for a in l))

C = 1.1019785625880999
print()
print('n  l_n                p_n=|l|phi^2n   d=n(p-1-C/sqrt n)   d*sqrt n   D_n*phi^-2ratio-def  D*n^1.5')
for k, lk in enumerate(l):
    n = k + 1
    p = abs(lk) * phi2 ** n
    d = n * (p - 1 - C / n ** 0.5)
    if k + 1 < len(l):
        r = abs(lk / l[k + 1])
        D = r - phi2
        Dn = D * n ** 1.5
        print(f'{n:2d} {lk:+.10f}  {p:.6f}  {d:.4f}  {d*n**0.5:.4f}  {D:.6f}  {Dn:.4f}')
    else:
        print(f'{n:2d} {lk:+.10f}  {p:.6f}  {d:.4f}  {d*n**0.5:.4f}')
print()
print(f'predicted K = phi^2*C/2 = {phi2*C/2:.4f}   (ratio-defect constant if no higher term)')
