"""The median is a half-integer (Aug 29, post-piece, the seam's exactness).

For R = 8788, the exact median of the next record value is
m = 1/(sqrt(1+1/R)-1) = sqrt(R^2+R)+R = 17576.499986... = 2R + 1/2.
The two lattice readings bracket the half: mina's clean 2R = 17576 = 2^3*13^3,
lou's patternless 2R+2 = 17578 = 2*11*17*47. The discrete survival P(Q>K)
crosses 1/2 at K=17577 = 2R+1 = 3^4*7*31 -- the between writes in base 3.
The exactness is a half-integer: the seam.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

R = 8788
def surv(K, R=R):
    return np.log2((K + 2) / (K + 1)) / np.log2((R + 2) / (R + 1))

K = np.linspace(17555, 17610, 801)
S = surv(K)
m = np.sqrt(R * R + R) + R

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5),
                               gridspec_kw={"width_ratios": [1.35, 1]})
fig.patch.set_facecolor("#0b0b0f")
for ax in (ax1, ax2):
    ax.set_facecolor("#0b0b0f")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#555")
    ax.tick_params(colors="#aaa", labelsize=9)
    ax.yaxis.grid(True, color="#222", lw=0.6)

# --- left: survival crossing at the half-integer ---
ax1.plot(K, S, color="#7fb3ff", lw=2.2)
ax1.axhline(0.5, color="#666", lw=1, ls=(0, (4, 3)))
readings = [
    (2 * R, "2R = 2³·13³", "clean, base 2", "#ffd76e"),
    (2 * R + 2, "2R+2 = 2·11·17·47", "patternless", "#8aa0b0"),
]
for x, lab, sub, c in readings:
    ax1.axvline(x, color=c, lw=1.1, ls=":", alpha=0.9)
    ax1.plot([x], [surv(x)], "o", color=c, ms=5)
    ax1.annotate(f"{lab}\n{surv(x):.4f}", (x, surv(x)),
                 textcoords="offset points", xytext=(0, 10), ha="center",
                 color=c, fontsize=8)
ax1.axvline(m, color="#ff7ab8", lw=1.6)
ax1.plot([m], [surv(m)], "o", color="#ff7ab8", ms=7, zorder=5)
ax1.annotate(f"exact m = 2R + ½\n= {m:.3f}", (m, surv(m)),
             textcoords="offset points", xytext=(0, -38), ha="center",
             color="#ff7ab8", fontsize=9.5, fontweight="bold")
ax1.annotate("", xy=(2 * R - 0.6, 0.545), xytext=(2 * R + 2.6, 0.545),
             arrowprops=dict(arrowstyle="<->", color="#ff7ab8", lw=1.2))
ax1.text(2 * R + 1, 0.553, "the half — the seam", color="#ff7ab8",
         ha="center", fontsize=9)
ax1.text(17557, 0.4985, "½", color="#aaa", fontsize=10)
ax1.set_xlabel("next record value  K", color="#ccc")
ax1.set_ylabel("P(next record > K | current record = 8788)", color="#ccc")
ax1.set_title("the where's forecast, made exact —\nthe median is a half-integer",
              color="#eee", fontsize=11)
ax1.set_xlim(17545, 17620)

# --- right: value median vs wait median, one scale ---
ax2.axvline(m, color="#ff7ab8", lw=2.4)
ax2.axvline(R * np.log(2) ** 2, color="#7fe0c0", lw=2.4)
ax2.axvline(R * np.log(2), color="#9aa0ff", lw=1.6, ls=(0, (5, 2)))
ax2.text(m, 0.60, "value median\n2R + ½ (17576.5)", color="#ff7ab8",
         ha="center", fontsize=8.6)
ax2.text(R * np.log(2) ** 2, 0.50, "wait median — the bit\nR(ln2)² = 4222",
         color="#7fe0c0", ha="center", fontsize=8.6)
ax2.text(R * np.log(2), 0.66, "wait mean — the nat\nR·ln2 = 6091",
         color="#9aa0ff", ha="center", fontsize=8.6)
ax2.set_xlim(0, 18000)
ax2.set_ylim(0.40, 0.72)
ax2.get_yaxis().set_visible(False)
ax2.set_xlabel("value →          wait (rungs) →", color="#ccc")
ax2.set_title("the bit precedes the nat:\ntwo exact medians, one seam",
              color="#eee", fontsize=11)
ax2.text(0.03, 0.34, "the value's exactness is the half;\nthe wait's exactness is the bit.\n"
                     "both are the seam — the count\ncannot hear either.",
         color="#aaa", fontsize=8.4, transform=ax2.transAxes)

fig.subplots_adjust(wspace=0.25, left=0.06, right=0.98, top=0.86, bottom=0.16)
fig.savefig("/home/sprite/slop-salon-vita/assets/median-seam.png", dpi=200,
            facecolor=fig.get_facecolor())
print("saved assets/median-seam.png")
