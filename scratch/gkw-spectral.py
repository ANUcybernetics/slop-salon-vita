import numpy as np
import scipy.linalg as la

def gkw_spectral(M=28, nmax=1_000_000, tail=True):
    """GKW transfer operator (Lf)(x)=sum_{a>=1} f(1/(x+a))/(x+a)^2, x in [0,1].
    Chebyshev collocation: basis T_j(2x-1), nodes x_k = 0.5(1-cos(k pi/(M-1))).
    Returns eigenvalues sorted by |.| descending, plus the collocation data."""
    # Chebyshev-Gauss-Lobatto nodes on [0,1]
    k = np.arange(M)
    xs = 0.5 * (1.0 - np.cos(k * np.pi / (M - 1)))
    # basis matrix B[k,j] = T_j(2 x_k - 1)
    zx = 2 * xs - 1
    B = np.polynomial.chebyshev.chebvander(zx, M - 1)   # (M, M)
    n = np.arange(1, nmax + 1, dtype=float)
    A = np.zeros((M, M))
    for i in range(M):
        x = xs[i]
        y = 1.0 / (x + n)          # image points, (nmax,)
        w = 1.0 / (x + n) ** 2     # weights
        z = 2 * y - 1              # Chebyshev argument
        # all T_j(z), j=0..M-1, via recurrence (vectorized over n)
        T = np.empty((nmax, M))
        T[:, 0] = 1.0
        if M > 1:
            T[:, 1] = z
        for j in range(2, M):
            T[:, j] = 2 * z * T[:, j - 1] - T[:, j - 2]
        A[i, :] = T.T @ w           # sum_n w_n T_j(z_n), each j
        if tail:
            # T_j(2*0-1)=(-1)^j ; tail sum ~ (-1)^j / (x+nmax)
            jj = np.arange(M)
            A[i, :] += ((-1.0) ** jj) / (x + nmax)
    # generalized eigenproblem A c = lambda B c
    vals, vecs = la.eig(A, B)
    order = np.argsort(-np.abs(vals))
    return vals[order], vecs[:, order], xs, B

if __name__ == "__main__":
    import sys
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 28
    vals, vecs, xs, B = gkw_spectral(M=M)
    print(f"M={M}  GKW eigenvalues")
    for k in range(min(8, M)):
        print(f"  lambda{k+1} = {vals[k].real:+.10f}   im {vals[k].imag:+.1e}")
    print("  ratios |l_{n+1}/l_n|:")
    for k in range(min(7, M - 1)):
        print(f"    |l{k+2}/l{k+1}| = {abs(vals[k+1]/vals[k]):.6f}")
