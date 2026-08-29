import numpy as np
import scipy.linalg as la
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

def gkw_spectral_s(s, M=36, nmax=200000):
    k = np.arange(M)
    xs = 0.5*(1.0-np.cos(k*np.pi/(M-1)))
    zx = 2*xs-1
    B = np.polynomial.chebyshev.chebvander(zx, M-1)
    n = np.arange(1, nmax+1, dtype=float)
    A = np.zeros((M,M))
    for i in range(M):
        x = xs[i]; d = x+n; y = 1.0/d; w = d**(-2.0*s); z = 2*y-1
        T = np.empty((nmax,M)); T[:,0]=1.0; T[:,1]=z
        for j in range(2,M): T[:,j]=2*z*T[:,j-1]-T[:,j-2]
        A[i,:] = T.T@w
        if 2*s>1:
            jj = np.arange(M)
            A[i,:] += ((-1.0)**jj)*(nmax**(1-2*s))/(2*s-1)
    vals,_ = la.eig(A,B)
    o = np.argsort(-np.abs(vals))
    return vals[o]

ss = np.concatenate([np.linspace(0.503,0.6,40), np.linspace(0.6,1.0,30), np.linspace(1.0,2.0,24)])
ss = np.unique(np.round(ss,4))
specs = np.array([gkw_spectral_s(s) for s in ss])
lam1 = specs[:,0].real
lam2 = specs[:,1].real
lam3 = specs[:,2].real

fig, ax = plt.subplots(figsize=(11,6.4), dpi=170)
fig.patch.set_facecolor("#101215")
ax.set_facecolor("#101215")
for sp in ax.spines.values(): sp.set_color("#556")
ax.tick_params(colors="#aab")
ax.xaxis.label.set_color("#ccd"); ax.yaxis.label.set_color("#ccd")
ax.title.set_color("#eef")
ax.grid(alpha=0.15, color="#556")

# the piece's sweep region: s from 1.0 down to 0.505
ax.axvspan(0.5, 0.505, color="#3a2a5a", alpha=0.0)  # placeholder
rect = Rectangle((0.503, -3.2), 1.0-0.503, 4.0, facecolor="#1c2333", edgecolor="none", zorder=0)
ax.add_patch(rect)
# the shore
ax.axvline(0.5, color="#6688ff", alpha=0.9, lw=2, ls="--", zorder=3)
ax.text(0.5, 3.1, "s = 1/2  the shore", color="#8aa8ff", ha="center", fontsize=11)
# the pole
ax.axvline(1.0, color="#ffcc66", alpha=0.9, lw=2, ls="--", zorder=3)
ax.text(1.0, 3.1, "s = 1  the pole", color="#ffddaa", ha="center", fontsize=11)

# lambda_1 (count): diverges at 1/2, crosses +1 at s=1
ax.plot(ss, lam1, color="#ffcc66", lw=2.6, label=r"$\lambda_1$  the count  ($\to+\infty$ at the shore)", zorder=4)
ax.plot(1.0, 1.0, "o", color="#ffcc66", ms=9, mec="none", zorder=5)
ax.text(1.045, 1.05, "+1", color="#ffcc66", fontsize=12)
# lambda_2 (sign): -0.30366 at s=1, to -1 at the shore
ax.plot(ss, lam2, color="#66bbff", lw=2.6, label=r"$\lambda_2$  the sign  ($\to-1$ at the shore)", zorder=4)
ax.plot(1.0, -0.30366, "o", color="#66bbff", ms=9, mec="none", zorder=5)
ax.text(1.03, -0.32, "−0.30366", color="#66bbff", fontsize=11)
ax.plot(0.503, lam2[0], "o", color="#66bbff", ms=9, mec="none", zorder=5)
# lambda_3 (even)
ax.plot(ss, lam3, color="#66ddbb", lw=2.0, label=r"$\lambda_3$  the even  ($\to+0.223$)")

# the sweep arrow: from s=1 down to 0.505, riding lambda_2
ar = FancyArrowPatch((1.0, -0.30366), (0.505, -0.98042), arrowstyle="-|>",
                     mutation_scale=22, lw=2.2, color="#ff88cc", zorder=6)
ax.add_patch(ar)
ax.text(0.62, -1.32, "the piece\nsweeps the strip,\nends inside the approach", color="#ff88cc", fontsize=10, ha="center")

# the end point (gap 0.0196): the sign at -0.98042
ax.plot(0.505, -0.98042, "*", color="#ff88cc", ms=15, mec="none", zorder=7)

ax.set_xlim(0.5, 2.0)
ax.set_ylim(-3.2, 3.6)
ax.set_xlabel(r"weight $s$   (the operator $L_s = \sum_a (a+x)^{-2s}$)")
ax.set_ylabel("real eigenvalues")
ax.legend(loc="upper right", facecolor="#161a22", edgecolor="#334", labelcolor="#ccd", fontsize=10)
ax.set_title("the operator's two seats — the count marginal at the pole, the sign at the shore", color="#eef")

# inset: the approach |lambda_2+1| ~ 4(s-1/2)
axin = ax.inset_axes([0.55, 0.16, 0.34, 0.34])
axin.set_facecolor("#141822")
for sp in axin.spines.values(): sp.set_color("#556")
axin.tick_params(colors="#99a", labelsize=8)
d = lam2 + 1.0
m = (ss > 0.5035) & (ss < 0.6)
axin.loglog(ss[m]-0.5, np.abs(d[m]), "o", color="#66bbff", ms=4)
axin.loglog(ss[m]-0.5, 4.0*(ss[m]-0.5), color="#ffcc66", lw=1.6, ls="--", label="slope 1 (gap = 4(s−1/2))")
axin.plot(0.505-0.5, 0.01958, "*", color="#ff88cc", ms=12)
axin.set_xlabel(r"$s-1/2$", color="#99a", fontsize=9)
axin.set_ylabel(r"$|\lambda_2+1|$", color="#99a", fontsize=9)
axin.legend(loc="lower right", facecolor="#141822", edgecolor="#334", labelcolor="#ccd", fontsize=7)
axin.grid(alpha=0.15, color="#556")

plt.tight_layout()
plt.savefig("assets/two-seats-cover.png", dpi=170, bbox_inches="tight", facecolor="#101215")
print("wrote assets/two-seats-cover.png")
