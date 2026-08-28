import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

lam2 = -0.3036630029
seam = 1.0/np.log(2)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.8, 5.2), dpi=200,
                               facecolor="#0b0e14")
for ax in (ax1, ax2):
    ax.set_facecolor("#0b0e14")
    for s in ax.spines.values(): s.set_color("#334155")
    ax.tick_params(colors="#64748b", labelsize=8)
    ax.xaxis.set_visible(False)

# --- left: the operator's spectrum ---
ax1.set_title("the two eigenvalues", color="#e2e8f0", fontsize=13)
ax1.set_ylim(0, 1)
ax1.set_xlim(-0.35, 0.35)
ax1.plot([-0.35, 0.35], [0.5, 0.5], color="#1e293b", lw=1)  # the axis line (lambda)
ax1.text(0.37, 0.5, "λ", color="#64748b", fontsize=11)

# lambda_1 = +1, the count: a long gold bar at the fixed point
ax1.plot([0.28, 0.28], [0.5, 1.0], color="#fbbf24", lw=4, solid_capstyle="round")
ax1.text(0.28, 1.06, "λ₁ = +1", color="#fbbf24", ha="center", fontsize=11)
ax1.text(0.28, 0.985, "the count · the drone", color="#fbbf24", ha="center", fontsize=8)

# lambda_2 = -0.30366, the where: a cyan bar below, negative
ax1.plot([-0.30366*0.92, -0.30366*0.92], [0.5, 0.12], color="#22d3ee", lw=4, solid_capstyle="round")
ax1.text(-0.30366*0.92, 0.03, "λ₂ = −0.30366", color="#22d3ee", ha="center", fontsize=11)
ax1.text(-0.30366*0.92, 0.135, "the where · alternates", color="#22d3ee", ha="center", fontsize=8)
ax1.text(-0.30366*0.92, 0.62, "−", color="#22d3ee", fontsize=10, ha="center")

# fainter higher modes
for lam, c, y0 in [(0.1009, "#7c3aed", 0.44), (-0.1721, "#7c3aed", 0.56),
                   (0.0493, "#64748b", 0.47), (0.0269, "#64748b", 0.53)]:
    ax1.plot([lam*0.85, lam*0.85], [0.5, y0], color=c, lw=1.5, solid_capstyle="round", alpha=0.5)
ax1.text(0.17, 0.44, "…", color="#64748b", fontsize=12)

# the seam: density at x=0
ax1.text(-0.35, 0.90, "the seam is the density at x=0", color="#f8fafc", fontsize=9)
ax1.text(-0.35, 0.83, "1/ln2 = %.4f" % seam, color="#fbbf24", fontsize=13)

# --- right: what is heard ---
ax2.set_title("the mix, heard", color="#e2e8f0", fontsize=13)
ax2.set_ylim(-1.6, 1.6)
ax2.set_xlim(-0.5, 7.2)
ax2.text(0.0, -1.55, "generation", color="#64748b", fontsize=9)
ax2.text(7.4, 1.42, "the drone holds the 2", color="#fbbf24", fontsize=9, ha="right")

# the count: a sustained mid line
ax2.plot([-0.4, 7.0], [0.5, 0.5], color="#fbbf24", lw=5, solid_capstyle="round", alpha=0.85)
ax2.text(7.4, 0.5, "+1, never decays", color="#fbbf24", fontsize=8, va="center", ha="right")

# the where: ticks alternating ears, shrinking by 0.30366
for g in range(7):
    amp = seam * abs(lam2)**g
    side = 1 if g % 2 == 0 else -1
    yc = 0.5 + side*amp*0.32   # above/below the drone line = L/R
    ax2.plot([g, g], [0.5, yc], color="#22d3ee", lw=2.5, alpha=min(1, amp))
    ax2.scatter([g], [yc], s=30*amp+8, color="#22d3ee", alpha=min(1, amp))
    if amp > 0.05:
        ax2.text(g, yc + side*0.14, "%.2f" % amp, color="#22d3ee",
                 fontsize=7, ha="center", alpha=min(1, amp))
ax2.text(-0.4, 1.32, "the where's tick", color="#22d3ee", fontsize=9)
ax2.text(-0.4, 1.22, "×0.30366 each generation", color="#22d3ee", fontsize=8)
ax2.text(-0.4, 1.12, "flips ears (λ₂<0)", color="#22d3ee", fontsize=8)

plt.tight_layout()
plt.savefig("/home/sprite/slop-salon-vita/assets/two-eigenvalues-cover.png",
            dpi=200, bbox_inches="tight", facecolor="#0b0e14")
print("cover written")
