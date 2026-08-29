import numpy as np
import scipy.linalg as la

def gkw_spectral_s(s, M=30, nmax=400000, tail=True):
    k = np.arange(M)
    xs = 0.5 * (1.0 - np.cos(k * np.pi / (M - 1)))
    zx = 2 * xs - 1
    B = np.polynomial.chebyshev.chebvander(zx, M - 1)
    n = np.arange(1, nmax + 1, dtype=float)
    A = np.zeros((M, M))
    for i in range(M):
        x = xs[i]
        d = x + n
        y = 1.0 / d
        w = d ** (-2.0 * s)
        z = 2 * y - 1
        T = np.empty((nmax, M))
        T[:, 0] = 1.0
        if M > 1:
            T[:, 1] = z
        for j in range(2, M):
            T[:, j] = 2 * z * T[:, j - 1] - T[:, j - 2]
        A[i, :] = T.T @ w
        if tail and 2 * s > 1:
            jj = np.arange(M)
            A[i, :] += ((-1.0) ** jj) * (nmax ** (1 - 2 * s)) / (2 * s - 1)
    vals, vecs = la.eig(A, B)
    order = np.argsort(-np.abs(vals))
    return vals[order]

# trace the leading eigenvalues down to s=1/2 from above
print("s        lambda1       lambda2      lambda3      lambda4      (lambda2+1)  |l2|/l1")
for s in [0.60, 0.55, 0.53, 0.51, 0.505, 0.5005, 0.5001]:
    vals = gkw_spectral_s(s, M=34)
    print(f"{s:.4f}  {vals[0].real:+.6f}  {vals[1].real:+.6f}  "
          f"{vals[2].real:+.6f}  {vals[3].real:+.6f}   {vals[1].real+1:+.2e}  {abs(vals[1]/vals[0]):.5f}")
