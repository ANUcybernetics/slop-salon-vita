import numpy as np
import scipy.linalg as la

def gkw_spectral_s(s, M=28, nmax=400000, tail=True):
    """Deformed GKW transfer operator:
       (L_s f)(x) = sum_{a>=1} f(1/(x+a)) / (x+a)^(2s),  x in [0,1].
    s=1 is the Gauss-Kuzmin-Wirsing operator (leading eig = 1, Gauss measure).
    Chebyshev collocation on [0,1]. Returns eigenvalues sorted by |.| desc."""
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
        if tail:
            jj = np.arange(M)
            # tail of sum_n n^(-2s) T_j(~-1) ~ (-1)^j * integral_{nmax}^inf n^{-2s}
            if 2 * s > 1:
                A[i, :] += ((-1.0) ** jj) * (nmax ** (1 - 2 * s)) / (2 * s - 1)
            # for s<=1/2 the tail diverges; truncation is the definition
    vals, vecs = la.eig(A, B)
    order = np.argsort(-np.abs(vals))
    return vals[order], vecs[:, order], xs, B

if __name__ == "__main__":
    ss = np.array([0.51, 0.55, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.4, 1.6, 1.8, 2.0])
    print("s       lambda1     lambda2     lambda3     lambda4     |l2/l1|")
    for s in ss:
        vals, *_ = gkw_spectral_s(s, M=28)
        print(f"{s:5.2f}  {vals[0].real:+.8f}  {vals[1].real:+.8f}  "
              f"{vals[2].real:+.8f}  {vals[3].real:+.8f}  {abs(vals[1]/vals[0]):.5f}")
