"""Figure: the record schedules its successor.

The four records of lambda_2's CF: 3@1, 13@6, 174@8, 8788@302.
Each record R sets an exponential wait to the next record:
    P(wait > t) = exp(-t/(R ln2)),   mean R ln2, median R (ln2)^2.
The actual next waits land: 5 (after 3), 2 (after 13), 294 (after 174).
The 5th record (after 8788) is pending: mean 6090, median 4220.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ln2 = np.log(2)
records = [3, 13, 174, 8788]
rungs   = [1, 6, 8, 302]
waits   = [5, 2, 294, None]   # observed wait to next record

fig, ax = plt.subplots(figsize=(9, 6), facecolor="#0e0e12")
ax.set_facecolor("#0e0e12")

t = np.linspace(0, 8000, 4000)
colors = ["#b08f5a", "#c9a86a", "#e0c183", "#f0d9a0"]

for R, w, c in zip(records, waits, colors):
    mean = R * ln2
    surv = np.exp(-t / mean)
    ax.plot(t, surv, color=c, lw=2,
            label=f"after {R}  (mean {mean:.0f})")
    if w is not None:
        s = np.exp(-w / mean)
        ax.plot([w], [s], "o", color=c, ms=8, mec="none")
        ax.annotate(f"actual wait {w}",
                    (w, s), textcoords="offset points",
                    xytext=(8, 4), color=c, fontsize=10)

# the pending 8788 case: mean & median markers
R = 8788
mean = R * ln2
med = R * ln2**2
ax.axhline(np.exp(-med/mean), color="#f0d9a0", ls=":", lw=1, alpha=0.5)
ax.annotate(f"median {med:.0f}", (0, np.exp(-med/mean)), textcoords="offset points",
            xytext=(6, 4), color="#f0d9a0", fontsize=10)
ax.annotate("next after 8788:\nmean 6090, median 4220",
            xy=(mean*0.55, np.exp(-0.55)), color="#f0d9a0", fontsize=11,
            ha="center")
ax.plot([mean], [np.exp(-1)], "d", color="#f0d9a0", ms=8)
ax.annotate("mean", (mean, np.exp(-1)), textcoords="offset points",
            xytext=(8, 4), color="#f0d9a0", fontsize=10)

ax.set_ylim(0, 1.02)
ax.set_xlim(0, 8000)
ax.set_xlabel("wait to next record (rungs)", color="#d9d3c0")
ax.set_ylabel("P(wait > t)   survival", color="#d9d3c0")
ax.set_title("the record schedules its successor — P(a≥R) = 1/(R·ln2)",
             color="#e8e2d0", fontsize=13)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#6a675a")
ax.spines["left"].set_color("#6a675a")
ax.tick_params(colors="#d9d3c0")
ax.legend(facecolor="#0e0e12", edgecolor="#6a675a", labelcolor="#e8e2d0", fontsize=10)
ax.grid(alpha=0.15, color="#6a675a")

plt.tight_layout()
plt.savefig("assets/wait-schedule.png", dpi=200, bbox_inches="tight")
print("saved assets/wait-schedule.png")
