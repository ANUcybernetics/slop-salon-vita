import numpy as np
import scipy.linalg as la

phi = (1 + 5**0.5) / 2
rho = 1 / phi**2  # 0.381966

def gkw_spectral(M=40, nmax=600_000):
    k = np.arange(M)
    xs = 0.5 * (1.0 - np.cos(k * np.pi / (M - 1)))
    zx = 2 * xs - 1
    B = np.polynomial.chebyshev.chebvander(zx, M - 1)
    n = np.arange(1, nmax + 1, dtype=float)
    A = np.zeros((M, M))
    for i in range(M):
        x = xs[i]
        y = 1.0 / (x + n); w = 1.0 / (x + n) ** 2
        z = 2 * y - 1
        T = np.empty((nmax, M)); T[:, 0] = 1.0
        if M > 1: T[:, 1] = z
        for j in range(2, M):
            T[:, j] = 2 * z * T[:, j - 1] - T[:, j - 2]
        A[i, :] = T.T @ w
        jj = np.arange(M)
        A[i, :] += ((-1.0) ** jj) / (x + nmax)
    vals, vecs = la.eig(A, B)
    order = np.argsort(-np.abs(vals))
    return vals[order]

# multi-M stability: only stable slots are true rungs
Ms = [46, 52, 58, 64, 70, 76]
specs = {}
for M in Ms:
    v = gkw_spectral(M=M)
    specs[M] = v.real[:16]
    print(f'M={M}: ' + ' '.join(f'{a:+.9f}' for a in v.real[:16]))

print()
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
print('the subdominant correction: p_n = |l_n| * phi^{2n}')
l = stable
for k, lk in enumerate(l):
    n = k + 1
    p = abs(lk) * phi**(2*n)
    print(f'  n={n}:  l_n = {lk:+.10f}   |l_n| = {abs(lk):.10f}   p_n = {p:.6f}')
    if k >= 1:
        r = abs(l[k-1]/lk) if lk != 0 else float('nan')
        print(f'        |l_{n-1}/l_n| = {r:.6f}   (-> {rho:.6f} if pure golden)')

print()
print('signed check: s_n = (-1)^{n+1} * l_n  (should be positive)')
for k, lk in enumerate(l):
    n = k + 1
    s = ((-1)**(n+1)) * lk
    print(f'  n={n}: s_n = {s:+.10f}')

print()
print('fits for p_n:')
p = np.array([abs(lk)*phi**(2*(k+1)) for k, lk in enumerate(l)])
ns = np.arange(1, len(p)+1)

# model A: p ~ C (pure), C = mean of last half
# model B: p ~ C + a/n
# model C: p ~ C * n^b  -> log p = log C + b log n
# model D: p ~ C * (1 + a phi^{-n})
import numpy.polynomial.polynomial as P

def fit_linear(x, y):
    c = np.polyfit(x, y, 1)
    return c

# B: p vs 1/n
A_B = np.vstack([np.ones(len(ns)), 1.0/ns]).T
cB, resB, *_ = np.linalg.lstsq(A_B, p, rcond=None)
predB = A_B @ cB
ssB = np.sum((p - predB)**2)
print(f'  B: p ~ {cB[0]:.4f} + {cB[1]:.4f}/n   residual ss {ssB:.4f}')

# C: log p vs log n
logp = np.log(p); logn = np.log(ns)
cC = np.polyfit(logn, logp, 1)
residC = logp - np.polyval(cC, logn)
print(f'  C: log p ~ {cC[1]:.4f} + {cC[0]:.4f} log n   (C0={np.exp(cC[1]):.4f})  resid sd {np.std(residC):.4f}')

# D: p ~ C + a phi^{-n} -> p as affine in phi^{-n}
ph = phi**(-ns)
A_D = np.vstack([np.ones(len(ns)), ph]).T
cD, resD, *_ = np.linalg.lstsq(A_D, p, rcond=None)
predD = A_D @ cD
ssD = np.sum((p - predD)**2)
print(f'  D: p ~ {cD[0]:.4f} + {cD[1]:.4f}*phi^-n   residual ss {ssD:.4f}')

# E: p ~ C + a/phi^{2n}
ph2 = phi**(-2*ns)
A_E = np.vstack([np.ones(len(ns)), ph2]).T
cE, resE, *_ = np.linalg.lstsq(A_E, p, rcond=None)
predE = A_E @ cE
ssE = np.sum((p - predE)**2)
print(f'  E: p ~ {cE[0]:.4f} + {cE[1]:.4f}*phi^-2n  residual ss {ssE:.4f}')

print()
print(f'  pure-limit guesses: 1/ln2 = {1/np.log(2):.4f}, ln2 = {np.log(2):.4f}, 2/ln2 = {2/np.log(2):.4f}')
