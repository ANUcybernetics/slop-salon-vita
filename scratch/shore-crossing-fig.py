import numpy as np
import scipy.linalg as la
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def gkw_spectral_s(s, M=36, nmax=200000):
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
        T[:, 1] = z
        for j in range(2, M):
            T[:, j] = 2 * z * T[:, j - 1] - T[:, j - 2]
        A[i, :] = T.T @ w
        if 2 * s > 1:
            jj = np.arange(M)
            A[i, :] += ((-1.0) ** jj) * (nmax ** (1 - 2 * s)) / (2 * s - 1)
    vals, _ = la.eig(A, B)
    o = np.argsort(-np.abs(vals))
    return vals[o]

ss = np.concatenate([
    np.linspace(0.501, 0.6, 22),
    np.linspace(0.6, 1.0, 24),
    np.linspace(1.0, 2.0, 24),
])
ss = np.unique(np.round(ss, 4))

specs = []
for s in ss:
    specs.append(gkw_spectral_s(s))
specs = np.array(specs)  # (len(ss), M)
lam1 = specs[:, 0].real
lam2 = specs[:, 1].real
lam3 = specs[:, 2].real
lam4 = specs[:, 3].real

fig, axes = plt.subplots(1, 2, figsize=(13, 5.2), dpi=160)
fig.patch.set_facecolor("#101215")
for ax in axes:
    ax.set_facecolor("#101215")
    for sp in ax.spines.values():
        sp.set_color("#556")
    ax.tick_params(colors="#aab")
    ax.xaxis.label.set_color("#ccd")
    ax.yaxis.label.set_color("#ccd")
    ax.title.set_color("#eef")
    ax.grid(alpha=0.15, color="#556")

# left panel: eigenvalue curves
ax = axes[0]
ax.axvspan(0.5, 1.0, color="#e8c86a", alpha=0.06)
ax.axvline(1.0, color="#e8c86a", ls="--", lw=1.2, alpha=0.8)
ax.axvline(0.5, color="#7fb3d5", ls=":", lw=1.4)
ax.axhline(0, color="#667", lw=0.8)
ax.axhline(1.0, color="#e8c86a", ls=":", lw=0.8, alpha=0.5)
ax.axhline(-1.0, color="#7fb3d5", ls=":", lw=0.8, alpha=0.5)
ax.plot(ss, lam1, color="#e8c86a", lw=2.2, label=r"$\lambda_1$ (count)")
ax.plot(ss, lam2, color="#7fb3d5", lw=2.2, label=r"$\lambda_2$ (sign / where)")
ax.plot(ss, lam3, color="#c99ec4", lw=1.6)
ax.plot(ss, lam4, color="#9ec49e", lw=1.6)
ax.plot(ss, specs[:,4].real, color="#c4b79e", lw=1.2)
ax.plot(ss, specs[:,5].real, color="#9eaec4", lw=1.0)
ax.scatter([1.0], [1.0], s=70, color="#e8c86a", zorder=5, marker="o")
ax.annotate("s = 1  —  the pole\n$\\lambda_1=+1$, the count\n(a zero of det $I-L_s$)",
            xy=(1.0, 1.0), xytext=(1.32, 0.62),
            color="#e8c86a", fontsize=10,
            arrowprops=dict(arrowstyle="->", color="#e8c86a", lw=1))
ax.scatter([0.5], [-1.0], s=70, color="#7fb3d5", zorder=5, marker="o")
ax.annotate("s = 1/2 —  the shore\n$\\lambda_2 \\to -1$, the sign\n(the negative count)",
            xy=(0.5, -1.0), xytext=(0.56, -1.55),
            color="#7fb3d5", fontsize=10,
            arrowprops=dict(arrowstyle="->", color="#7fb3d5", lw=1))
ax.set_xlim(0.5, 2.05)
ax.set_ylim(-1.8, 1.6)
ax.set_xlabel("weight s")
ax.set_ylabel("eigenvalue  $\\lambda_k(s)$")
ax.set_title("the operator's two seats", fontsize=13)
ax.legend(loc="upper right", fontsize=9, frameon=False, labelcolor="#ccd")
ax.text(0.52, 1.35, "critical strip\n(converges only for Re s > 1/2)",
        color="#7fb3d5", fontsize=8.5, va="top")

# right panel: approach of lambda2 to -1
ax = axes[1]
eps = ss[ss > 0.5]
d = np.abs(lam2[ss > 0.5] + 1.0)
ok = d > 0
ax.semilogx(eps[ok] - 0.5, d[ok], "o-", color="#7fb3d5", ms=4, lw=1.4)
ax.semilogx(eps[ok] - 0.5, 4 * (eps[ok] - 0.5), "--", color="#e8c86a", lw=1.2,
            label="slope 4:  $\\lambda_2+1 \\approx 4(s-1/2)$")
ax.set_xlabel(r"$s - 1/2$")
ax.set_ylabel(r"$|\lambda_2(s) + 1|$")
ax.set_title("the where approaches the negative count", fontsize=13)
ax.legend(loc="upper left", fontsize=9, frameon=False, labelcolor="#ccd")
ax.set_xlim(5e-4, 0.5)
ax.set_ylim(1e-3, 5)

fig.suptitle("the count crosses at the pole, the sign crosses at the shore",
             color="#eef", fontsize=13.5, y=0.98)
fig.tight_layout(rect=(0, 0, 1, 0.95))
out = "assets/shore-crossing.png"
fig.savefig(out, dpi=160, bbox_inches="tight", facecolor="#101215")
print("wrote", out)
