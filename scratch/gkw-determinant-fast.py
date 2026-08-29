import numpy as np
import scipy.linalg as la

def build_T(M, nmax):
    """Precompute Chebyshev basis values T_j(z_n) for all collocation rows.
    Returns d[i,n] = x_i + n, Tmat[i,j,n] = T_j(2/(x_i+n)-1)."""
    k = np.arange(M)
    xs = 0.5 * (1.0 - np.cos(k * np.pi / (M - 1)))
    n = np.arange(1, nmax + 1, dtype=float)
    d = xs[:, None] + n[None, :]            # (M, nmax)
    y = 1.0 / d
    z = 2 * y - 1                            # (M, nmax)
    T = np.empty((M, nmax, M))
    T[:, :, 0] = 1.0
    if M > 1:
        T[:, :, 1] = z
    for j in range(2, M):
        T[:, :, j] = 2 * z * T[:, :, j - 1] - T[:, :, j - 2]
    return xs, d, T

def det_s(s, xs, d, T, M, nmax):
    B = np.polynomial.chebyshev.chebvander(2 * xs - 1, M - 1)
    w = d ** (-2.0 * s)                       # (M, nmax)
    A = np.einsum('inj,in->ij', T, w)
    if 2 * s > 1:
        jj = np.arange(M)
        A += ((-1.0) ** jj) * (nmax ** (1 - 2 * s)) / (2 * s - 1)
    sd, ld = np.linalg.slogdet(B - A)
    sd2, ld2 = np.linalg.slogdet(B)
    return sd * np.exp(ld - ld2)

if __name__ == "__main__":
    M, nmax = 32, 120000
    xs, d, T = build_T(M, nmax)
    ss = np.linspace(0.35, 2.5, 140)
    dets = [det_s(s, xs, d, T, M, nmax) for s in ss]
    dets = np.array(dets)
    signs = np.sign(dets)
    for i in range(len(ss) - 1):
        if signs[i] * signs[i + 1] < 0:
            print(f"sign change  s={ss[i]:.3f} -> {ss[i+1]:.3f}   det {dets[i]:.3e} -> {dets[i+1]:.3e}")
    print("special s:")
    for s in [0.25, 0.5, 0.75, 1.0, 1.5, 2.0]:
        print(f"  s={s:.2f}  det(I-L_s) = {det_s(s, xs, d, T, M, nmax):.4e}")
