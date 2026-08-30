import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, (axL, axR) = plt.subplots(1, 2, figsize=(12, 5.6), gridspec_kw={"width_ratios": [1.15, 1]})

# ---------- left: the mean projection matrix ----------
n = 6
P = np.full((n, n), 1.0 / n)  # mean projection: every voice to the count
axL.imshow(P, cmap="YlOrBr", vmin=0, vmax=1, aspect="equal")
for i in range(n + 1):
    axL.axhline(i - 0.5, color="#666", lw=0.8)
    axL.axvline(i - 0.5, color="#666", lw=0.8)
# the trace: diagonal, boxed in gold
for i in range(n):
    axL.add_patch(mpatches.Rectangle((i - 0.5, i - 0.5), 1, 1, fill=False,
                  ec="#b8860b", lw=3.0))
axL.text(-0.5, n - 0.5, "P", ha="right", va="center", fontsize=22, weight="bold", color="#333")
axL.set_xticks(range(n))
axL.set_yticks(range(n))
axL.set_xticklabels([])
axL.set_yticklabels([])
axL.set_title("the fold: every voice to the count\n"
              "diagonal boxed = the trace", fontsize=12, color="#222")
axL.text(n / 2 - 0.5, n + 0.7,
         "trace(P) = 6·(1/6) = 1", ha="center", fontsize=14,
         weight="bold", color="#b8860b")

# ---------- right: the spectrum ----------
axR.axis("off")
axR.set_xlim(-1.5, 1.5)
axR.set_ylim(-1.9, 1.6)
# a horizontal number line
yl = 0.5
axR.annotate("", xy=(1.02, yl), xytext=(-1.02, yl),
             arrowprops=dict(arrowstyle="->", lw=1.3, color="#444"))
axR.text(1.06, yl, "λ", fontsize=15, color="#444")
for t in (-1, 0, 1):
    axR.text(t, yl - 0.07, f"{t}", ha="center", fontsize=11, color="#444")
    axR.plot([t, t], [yl - 0.02, yl + 0.02], color="#444", lw=1)

# the count: one +1
axR.add_patch(mpatches.Circle((1, yl + 0.42), 0.16, fc="#e8a33d", ec="#b8860b", lw=2))
axR.text(1, yl + 0.82, "the count", ha="center", fontsize=13, weight="bold", color="#8a5a10")
axR.text(1, yl + 0.60, "λ=1 — trace = rank = 1", ha="center", fontsize=9.5, color="#8a5a10")

# the five zeros: the homes
for k in range(5):
    x = -0.6 + k * 0.3
    axR.add_patch(mpatches.Circle((x, yl + 0.42), 0.13, fill=False, ec="#999", lw=1.8))
axR.text(-0.0, yl + 0.82, "the homes", ha="center", fontsize=13, color="#777")
axR.text(-0.0, yl + 0.60, "λ=0 ×5 — the nullity n−1", ha="center", fontsize=9.5, color="#777")

# the sign's −1, living in the kernel, summing to 0
axR.add_patch(mpatches.Circle((-1, yl + 0.42), 0.13, fill=False, ec="#3d6be8", lw=2))
axR.text(-1, yl + 0.82, "the sign", ha="center", fontsize=13, color="#3d6be8")
axR.text(-1, yl + 0.60, "λ=−1 in the kernel — sums to 0", ha="center", fontsize=9.5, color="#3d6be8")

# the trace equation
axR.text(0.0, yl - 0.72,
         "Σ eigenvalues  =  1 + 0 + 0 + 0 + 0 + 0  =  1\n"
         "the count is the trace of the fold — a count, not a value.",
         ha="center", va="center", fontsize=13.5, weight="bold", color="#222")

# rank-nullity
axR.text(0.0, yl - 1.62,
         "rank-nullity:  n = 1 + (n−1)     n voices, n−1 homes",
         ha="center", va="center", fontsize=12, color="#333")

plt.tight_layout()
plt.savefig("assets/trace-of-fold.png", dpi=200, bbox_inches="tight", facecolor="white")
print("wrote assets/trace-of-fold.png")
