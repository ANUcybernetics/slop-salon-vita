import numpy as np, scipy.linalg as la

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

# collect spectra over a range of M; the ghost drifts, true rungs are stable
Ms = [40, 46, 52, 58, 64, 70]
specs = {}
for M in Ms:
    v = gkw_spectral(M=M)
    specs[M] = v.real[:14]
    print(f'M={M}: ' + ' '.join(f'{a:+.8f}' for a in v.real[:14]))

# stability: eigenvalue at a sorted slot that changes < 1e-5 across M is a true rung
print()
print('true ladder (stable across M):')
nmax_run = min(len(v) for v in specs.values())
stable = []
for j in range(nmax_run):
    col = [specs[M][j] for M in Ms]
    spread = max(col) - min(col)
    if spread < 2e-5:
        stable.append(col[0])
        print(f'  slot {j+1}: {col[0]:+.10f}  (spread {spread:.1e})')
    else:
        print(f'  slot {j+1}: GHOST/drift  min {min(col):+.6f} max {max(col):+.6f}')

print()
print('ratio |l_{n+1}/l_n| on the true ladder (signed negatives preserved):')
l = stable
for k in range(len(l) - 1):
    if l[k] != 0:
        print(f'  |l{k+2}/l{k+1}| = {abs(l[k+1]/l[k]):.6f}   signed l{k+2}/l{k+1} = {l[k+1]/l[k]:+.6f}')
print(f'  1/phi^2 = {1/((1+5**0.5)/2)**2:.10f}   1/e = {1/np.e:.10f}')
