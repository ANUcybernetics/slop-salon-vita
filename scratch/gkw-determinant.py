import numpy as np
import scipy.linalg as la

def gkw_det_s(s, M=40, nmax=300000, tail=True):
    """Return det(I - L_s) where L_s is the deformed GKW operator at weight s,
    via Chebyshev collocation: A c = lam B c  =>  det(I - L_s) = det(B-A)/det(B)."""
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
    sign_det, logdet = np.linalg.slogdet(B - A)
    sign_detB, logdetB = np.linalg.slogdet(B)
    return sign_det * np.exp(logdet - logdetB), (logdet - logdetB)

if __name__ == "__main__":
    ss = np.linspace(0.35, 2.5, 120)
    dets = []
    for s in ss:
        d, _ = gkw_det_s(s, M=36)
        dets.append(d)
    dets = np.array(dets)
    # find sign changes (zeros)
    signs = np.sign(dets)
    for i in range(len(ss) - 1):
        if signs[i] * signs[i + 1] < 0:
            # bisect-ish
            s0, s1 = ss[i], ss[i + 1]
            print(f"sign change between s={s0:.3f} and s={s1:.3f}   det {dets[i]:.3e} -> {dets[i+1]:.3e}")
    # also print det near special points
    for s in [0.25, 0.5, 0.75, 1.0, 1.5, 2.0]:
        d, _ = gkw_det_s(s, M=36)
        print(f"s={s:.2f}  det(I-L_s) = {d:.4e}")
