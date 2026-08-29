import numpy as np
import scipy.linalg as la
import sys

phi = (1 + 5**0.5) / 2

def gkw_spectral(M=40, nmax=600_000):
    """GKW transfer operator on Chebyshev nodes, column-streamed to bound memory."""
    k = np.arange(M)
    xs = 0.5 * (1.0 - np.cos(k * np.pi / (M - 1)))
    zx = 2 * xs - 1
    B = np.polynomial.chebyshev.chebvander(zx, M - 1)
    n = np.arange(1, nmax + 1, dtype=float)
    A = np.zeros((M, M))
    for i in range(M):
        x = xs[i]
        y = 1.0 / (x + n)
        w = y * y
        z = 2 * y - 1
        # stream the Chebyshev columns: T_0 = 1, T_1 = z, T_j = 2z T_{j-1} - T_{j-2}
        t_prev2 = np.ones(nmax)
        t_prev1 = z.copy()
        A[i, 0] = w.sum()
        if M > 1:
            A[i, 1] = (w * t_prev1).sum()
        for j in range(2, M):
            t_j = 2 * z * t_prev1 - t_prev2
            A[i, j] = (w * t_j).sum()
            t_prev2, t_prev1 = t_prev1, t_j
        jj = np.arange(M)
        A[i, :] += ((-1.0) ** jj) / (x + nmax)
    vals, _ = la.eig(A, B)
    order = np.argsort(-np.abs(vals))
    return vals[order]

Ms = [56, 68, 80, 92]
specs = {}
for M in Ms:
    v = gkw_spectral(M=M)
    specs[M] = v.real[:16]
    print(f'M={M}: ' + ' '.join(f'{a:+.9f}' for a in v.real[:14]), flush=True)

print()
# stability across M
nmax_run = min(len(v) for v in specs.values())
stable = []
for j in range(nmax_run):
    col = [specs[M][j] for M in Ms]
    spread = max(col) - min(col)
    if spread < 3e-5:
        stable.append(col[0])
        print(f'slot {j+1}: {col[0]:+.10f}  spread {spread:.1e}')
    else:
        print(f'slot {j+1}: GHOST/drift  min {min(col):+.6f} max {max(col):+.6f}')

print()
C = 1.1019785625880999  # 4throot(5) zeta(3/2) / (2 sqrt(pi))
print(f'C (Alkauskas) = {C}')
print(f'n | l_n | p_n=|l|phi^2n | d(n)=n(p-1-C/sqrt n) | d(n)*sqrt n | ratio |l_n/l_n+1| - phi^2  | x n^{3/2}')
l = stable
for k in range(len(l) - 1):
    n = k + 1
    lk = l[k]; lk1 = l[k + 1]
    p = abs(lk) * phi ** (2 * n)
    p1 = abs(lk1) * phi ** (2 * (n + 1))
    d = n * (p - 1 - C / n ** 0.5)
    r = abs(lk / lk1)
    D = r - phi ** 2
    print(f'{n:2d} | {lk:+.10f} | {p:.6f} | {d:.4f} | {d*n**0.5:.4f} | {D:.6f} | {D*n**1.5:.4f}')
print()
print(f'phi^2 = {phi**2:.6f}')
