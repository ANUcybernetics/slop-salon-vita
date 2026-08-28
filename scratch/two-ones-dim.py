import numpy as np

def spectral_radius(s, K, N=4096, iters=400, tol=1e-9):
    """Top eigenvalue lambda_s of (L_s f)(r) = sum_{a=1..K} (1/(a+r))^{2s} f(1/(a+r)).
    r in (0,1], uniform midpoint grid of size N. Power iteration, L1-normalised.
    lambda_s = 1 marks the Hausdorff dimension of C_K = {digits <= K}."""
    grid = (np.arange(N) + 0.5) / N
    # precompute for each a: position of T_a(r) on the grid + weight exponent base
    pos = []
    wbase = []
    for a in range(1, K + 1):
        Ta = 1.0 / (a + grid)
        p = Ta * N - 0.5
        i0 = np.floor(p).astype(np.int64)
        np.clip(i0, 0, N - 2, out=i0)
        fr = p - i0
        pos.append((i0, fr))
        wbase.append(Ta)  # weight = Ta^(2s)
    f = np.ones(N)
    lam = 0.0
    for _ in range(iters):
        Lf = np.zeros(N)
        for a in range(K):
            i0, fr = pos[a]
            fTa = f[i0] * (1.0 - fr) + f[i0 + 1] * fr
            Lf += wbase[a] ** (2 * s) * fTa
        new_lam = Lf.sum()
        # relative change
        if abs(new_lam - lam) < tol * abs(new_lam) + 1e-12:
            lam = new_lam
            break
        lam = new_lam
        f = Lf / lam
    return lam


def dim_digit_bounded(K, N=4096, iters=400):
    """Hausdorff dimension of {x in (0,1): all partial quotients <= K}."""
    if K == 1:
        return 0.0
    # lambda_s decreasing in s; bisect s in [0,1] where lambda_s = 1
    lo, hi = 0.0, 1.0
    l_lo = spectral_radius(lo, K, N, iters)
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        l_mid = spectral_radius(mid, K, N, iters)
        if l_mid > 1.0:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-6:
            break
    return 0.5 * (lo + hi)


if __name__ == "__main__":
    import time
    for K in [1, 2, 3, 4, 5]:
        t0 = time.time()
        d = dim_digit_bounded(K)
        print(f"K={K:2d}  dim={d:.4f}   ({time.time()-t0:.1f}s)")
