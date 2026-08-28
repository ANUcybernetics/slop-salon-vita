import numpy as np
import scipy.linalg as la

def gkw_spectrum(N, p=1.5, nmax_factor=1.0, nmax_cap=200000, verbose=False):
    """Gauss-Kuzmin-Wirsing transfer operator (Lf)(x)=sum_n f(1/(x+n))/(x+n)^2.
    Collocation on a grid clustered toward x=0: x = ((i-.5)/N)^p.
    Linear-interp scattering of each image point; tail (y < y_min) lumped to x_1.
    Returns (eigvals sorted by |.| desc, grid xs, right eigenvectors)."""
    ii = np.arange(N) + 0.5
    xs = (ii / N) ** p
    x1 = xs[0]
    L = np.zeros((N, N))
    # number of n to iterate explicitly: those with y >= x1, capped for speed
    nmax = min(int((1.0 / x1) * nmax_factor), nmax_cap)
    n = np.arange(1, nmax + 1, dtype=float)
    for i in range(N):
        x = xs[i]
        y = 1.0 / (x + n)
        w = 1.0 / (x + n) ** 2
        # clamp below to x1 (tail lumping)
        y = np.maximum(y, x1)
        # linear interpolation onto grid
        j = np.searchsorted(xs, y, side='right') - 1
        j = np.clip(j, 0, N - 2)
        xj = xs[j]
        xj1 = xs[j + 1]
        denom = (xj1 - xj)
        frac = (y - xj) / denom
        np.add.at(L[i], j, w * (1.0 - frac))
        np.add.at(L[i], j + 1, w * frac)
    vals, vecs = la.eig(L)
    order = np.argsort(-np.abs(vals))
    vals = vals[order]
    vecs = vecs[:, order]
    return vals, xs, vecs

def ladder_report(N, p=1.5, nmodes=6):
    vals, xs, vecs = gkw_spectrum(N, p=p)
    lam = vals.real
    print(f"N={N} p={p}:  eigenvalues")
    for k in range(min(nmodes, len(lam))):
        print(f"  lambda{k+1} = {lam[k]:+.8f}   (im {vals[k].imag:+.1e})")
    # ratios
    print("  |lambda_{n+1}/lambda_n|:")
    rat = []
    for k in range(min(nmodes, len(lam)) - 1):
        r = abs(lam[k+1] / lam[k])
        rat.append(r)
        print(f"    |l{k+2}/l{k+1}| = {r:.5f}")
    print("  mean ratio:", np.mean(rat))
    # eigenfunction zero counts (sign changes of real part on the grid)
    print("  eigenfunction sign-change counts (n-1 zeros expected):")
    for k in range(min(nmodes, len(lam))):
        v = vecs[:, k].real
        # count sign changes
        signs = np.sign(v)
        nz = np.sum(signs[1:] * signs[:-1] < 0)
        print(f"    v{k+1}: {nz} sign changes")
    return lam

if __name__ == "__main__":
    import sys
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 1600
    ladder_report(N)
