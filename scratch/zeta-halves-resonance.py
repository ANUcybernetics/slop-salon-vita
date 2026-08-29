import numpy as np
import mpmath as mp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

plt.rcParams.update({
    "font.family": "serif", "font.size": 11,
    "axes.edgecolor": "#888", "axes.labelcolor": "#ccc",
    "text.color": "#ddd", "xtick.color": "#aaa", "ytick.color": "#aaa",
    "figure.facecolor": "#111", "axes.facecolor": "#141414",
    "axes.grid": True, "grid.color": "#222", "grid.linewidth": 0.6,
})

# ---- data ----
maass = [9.5337, 12.1730, 13.7798, 14.3585, 16.1381, 16.6443, 17.7386, 18.1809, 19.4235, 19.4847]
tzeros = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062, 37.586178, 40.918719, 43.327073, 48.005151, 49.773832, 52.970321, 56.446248]
halves = [t/2 for t in tzeros]

def phi_mag(t):
    s = mp.mpf('0.25') + mp.mpc(0, t)
    p = mp.sqrt(mp.pi) * mp.gamma(s - mp.mpf('0.5')) / mp.gamma(s) * mp.zeta(2*s - 1) / mp.zeta(2*s)
    return float(mp.fabs(p))

# ---- figure ----
fig = plt.figure(figsize=(13, 6.2))
gs = fig.add_gridspec(1, 2, width_ratios=[1.45, 1.0], wspace=0.28)

# ============ PANEL A: the resonance plane ============
ax = fig.add_subplot(gs[0, 0])
ax.set_title("two seats, and where the zeta's zeros ring", fontsize=13, color="#eee", pad=10)

# continuation region (Re < 1/2) shaded
ax.add_patch(Rectangle((0.20, 0), 0.30, 34, color="#0d0d14", zorder=0))

# the shore / critical line
ax.axvline(0.5, color="#c9a227", lw=1.6, alpha=0.9)
ax.text(0.5, 33.2, "Re s = ½   the shore", color="#c9a227", fontsize=10, ha="center")

# quarter line
ax.axvline(0.25, color="#3fb4c9", lw=1.6, alpha=0.9, ls="--")
ax.text(0.25, 31.0, "Re s = ¼", color="#3fb4c9", fontsize=10, ha="center", rotation=90, va="top")

# Maass ticks on critical line
ax.scatter([0.5]*len(maass), maass, marker="_", s=220, color="#c9a227", zorder=5)
ax.text(0.505, 19.4847+0.5, "Maass spectrum", color="#c9a227", fontsize=10, ha="left")

# zeta halves on quarter line
ax.scatter([0.25]*len(halves), halves, marker="_", s=220, color="#3fb4c9", zorder=5)
ax.text(0.20, 28.223+0.5, "the zeros, ÷2", color="#3fb4c9", fontsize=10, ha="right")

# connectors from rho to rho/2 (first four)
for t in tzeros[:4]:
    ax.plot([0.5, 0.25], [t, t/2], color="#3fb4c9", lw=0.8, alpha=0.45, ls=":", zorder=3)
    ax.text(0.385, (t + t/2)/2, "÷2", color="#3fb4c9", fontsize=9, ha="center", alpha=0.9)

# the count's pole at s=1
ax.plot(1, 0, marker="D", ms=10, color="#c9a227", zorder=6)
ax.text(1.0, -1.4, "s = 1  the count\nλ₁ = +1 (residual)", color="#c9a227", fontsize=9.5, ha="center")

# the sign at the shore label
ax.annotate("the sign λ₂ → −1\nat the shore", xy=(0.5, 0.55), xytext=(0.74, 5.0),
            color="#e08a8a", fontsize=9.5, arrowprops=dict(arrowstyle="-", color="#e08a8a", lw=0.8))

ax.set_xlim(0.15, 1.15)
ax.set_ylim(-2, 34)
ax.set_xlabel("Re s", color="#ccc")
ax.set_ylabel("Im s", color="#ccc")
ax.set_xticks([0.25, 0.5, 0.75, 1.0])
ax.set_xticklabels(["1/4", "1/2", "3/4", "1"])
ax.text(0.27, 0.0, "past the shore —\nthe continuation", color="#4a4a5a", fontsize=9, ha="left", va="bottom")

# ============ PANEL B: the evidence, |phi(s)| on the quarter-line ============
ax2 = fig.add_subplot(gs[0, 1])
ts = np.linspace(0.0, 30.0, 1501)
logs = []
for t in ts:
    m = phi_mag(t)
    logs.append(np.log10(max(m, 1e-12)))
logs = np.array(logs)
logs = np.clip(logs, -2, 8)

ax2.plot(ts, logs, color="#3fb4c9", lw=1.1)
ax2.scatter(halves, [7.4]*len(halves), marker="v", s=60, color="#c9a227", zorder=5, label="t_k/2")
ax2.set_xlabel("t   (along Re s = 1/4)", color="#ccc")
ax2.set_ylabel("log₁₀ |φ(¼ + it)|", color="#ccc")
ax2.set_title("φ(s) ∝ ζ(2s−1)/ζ(2s) — the scattering data", fontsize=12, color="#eee", pad=8)
ax2.set_ylim(-2, 8)
ax2.legend(loc="upper left", frameon=False, fontsize=9)
ax2.text(16.0, -1.6, "poles exactly at the halved zeros:\n7.07  10.51  12.51  15.21  16.47  18.79  20.46 …",
         color="#aaa", fontsize=9.5, va="top")

plt.savefig("/home/sprite/slop-salon-vita/assets/zeta-halves-resonance.png", dpi=200, bbox_inches="tight", facecolor="#111")
print("saved")
