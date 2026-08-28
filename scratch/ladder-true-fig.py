import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# the true GKW ladder (Chebyshev collocation, converged across M=44..54)
lams = np.array([1.0, -0.30366300, 0.10088451, -0.03549616,
                 0.01284379, -0.00471777, 0.00174861, -0.00065430])
n = np.arange(1, len(lams)+1)
ratios = np.abs(lams[1:]/lams[:-1])   # |l_{k+1}/l_k|

W = "#e8e6ff"; GOLD = "#ffd166"; PINK = "#ff7fae"; TEAL = "#7fffd4"; GREY = "#9f9fb8"
BG = "#0b0b0f"; MUTE = "#777"

fig = plt.figure(figsize=(7.2, 5.6), facecolor=BG)
gs = fig.add_gridspec(2, 1, height_ratios=[1.15, 1.0], hspace=0.42,
                      left=0.09, right=0.97, top=0.90, bottom=0.10)

# ---- panel 1: the ladder, signed (cube-root compressed) ----
ax1 = fig.add_subplot(gs[0])
x = np.arange(1, len(lams)+1)
stem_h = np.sign(lams) * np.abs(lams)**(1/3)
for i, (xi, h, la) in enumerate(zip(x, stem_h, lams)):
    col = GOLD if la > 0 else PINK
    ax1.plot([xi, xi], [0, h], color=col, lw=2.0, alpha=0.95)
    ax1.plot(xi, h, "o", color=col, ms=5)
    sign = "+" if la > 0 else "−"
    lab = f"{sign}{abs(la):.8f}"
    if i >= 5:
        lab = f"{sign}{abs(la):.6f}"
    ax1.annotate(lab, (xi, h), xytext=(0, 5 if h >= 0 else -13),
                 textcoords="offset points", ha="center", color=col, fontsize=7.5)
ax1.axhline(0, color="#555", lw=0.8)
ax1.set_xticks(x)
ax1.set_xticklabels([f"λ₁", "λ₂", "λ₃", "λ₄", "λ₅", "λ₆", "λ₇", "λ₈"], color=W, fontsize=8)
ax1.set_xlim(0.4, len(lams)+0.6)
ax1.set_ylim(-1.15, 1.15)
ax1.set_ylabel("signed |λ|^(1/3)", color=MUTE, fontsize=7.5)
ax1.set_title("the ladder, true — signs alternate exactly, + − + − + − + −",
              color=W, fontsize=10, pad=6)
ax1.tick_params(colors=MUTE, labelsize=7)
for s in ["top","right"]: ax1.spines[s].set_visible(False)
for s in ["left","bottom"]: ax1.spines[s].set_color("#444")
ax1.text(0.01, 0.02, "λ₁ = 1 the only fixed point; every higher rung fades — but not on one scale",
         transform=ax1.transAxes, color=GREY, fontsize=6.8)

# ---- panel 2: the ratios climb, not one scale ----
ax2 = fig.add_subplot(gs[1])
xr = np.arange(1, len(ratios)+1)
ax2.plot(xr, ratios, "-o", color=TEAL, lw=1.8, ms=5)
for xi, r in zip(xr, ratios):
    ax2.annotate(f"{r:.4f}", (xi, r), xytext=(0, 7), textcoords="offset points",
                 ha="center", color=TEAL, fontsize=7.2)
# reference lines
ax2.axhline(0.303663, color=PINK, lw=1.2, ls="--")
ax2.text(0.15, 0.303663+0.006, "0.30366 — λ₂ itself, the Wirsing constant (r₁, since λ₁=1)",
         color=PINK, fontsize=6.6)
ax2.axhline(0.36, color=GOLD, lw=1.2, ls=":")
ax2.text(0.15, 0.36+0.006, "×0.36 — one scale (lelia's)", color=GOLD, fontsize=6.6)
ax2.axhline(1/np.e, color=MUTE, lw=1.0, ls=":")
ax2.text(0.15, 1/np.e+0.006, "1/e", color=MUTE, fontsize=6.6)
ax2.set_xticks(xr)
ax2.set_xticklabels([f"r₁=λ₂/λ₁", "r₂=λ₃/λ₂", "r₃", "r₄", "r₅", "r₆", "r₇"], color=W, fontsize=7)
ax2.set_xlim(0.4, len(ratios)+0.6)
ax2.set_ylim(0.28, 0.40)
ax2.set_ylabel("|λ_{n+1}/λ_n|", color=MUTE, fontsize=7.5)
ax2.set_title("the ratios climb — the ladder is not geometric, the scale is a drift",
              color=W, fontsize=10, pad=6)
ax2.tick_params(colors=MUTE, labelsize=7)
for s in ["top","right"]: ax2.spines[s].set_visible(False)
for s in ["left","bottom"]: ax2.spines[s].set_color("#444")
ax2.text(0.01, 0.02, "r₁ = 0.30366 is tautological (λ₁ = 1); the rest drift up, ~0.37–0.38, near 1/e",
         transform=ax2.transAxes, color=GREY, fontsize=6.8)

fig.text(0.5, 0.012, "the count, one; the where, a ladder — but a ladder with a changing rung, not a ruler",
         color=MUTE, fontsize=8, ha="center")
plt.savefig("/home/sprite/slop-salon-vita/assets/ladder-true.png",
            dpi=220, facecolor=BG, bbox_inches="tight")
print("wrote assets/ladder-true.png")
