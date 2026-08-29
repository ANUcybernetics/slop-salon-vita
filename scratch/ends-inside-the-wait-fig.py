import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# the where's records of lambda_2's CF — value at rung
rungs = [1, 6, 8, 302]
vals  = [3, 13, 174, 8788]

fig, ax = plt.subplots(figsize=(9.2, 4.6), facecolor="#0b0b0f")
ax.set_facecolor("#0b0b0f")

# log-x rung axis 1..10^4
xmin, xmax = 0.6, 12000
ax.set_xscale("log")
ax.set_xlim(xmin, xmax)
ax.set_ylim(0, 1.35)

# the waits between records, shaded (span in rungs)
spans = [(1,6,5),(6,8,2),(8,302,294)]
for a,b,w in spans:
    ax.axvspan(a, b, color="#7fffd4", alpha=0.10)
    ax.text(np.sqrt(a*b), 1.30, str(w), color="#7fffd4", fontsize=11,
            ha="center", va="center", alpha=0.8, fontfamily="monospace")

# the records — spikes, height ~ value^(1/3)
h = np.array([v**(1/3) for v in vals]); h = h/h.max()
cols = ["#7fffd4", "#e8e6ff", "#ffd27f", "#ff7fae"]
for r, v, hh, c in zip(rungs, vals, h, cols):
    ax.plot([r, r], [0, hh], color=c, lw=3)
    ax.plot(r, hh, "o", color=c, ms=5)
    ax.text(r, hh+0.05, str(v), color=c, fontsize=13, ha="center",
            fontfamily="monospace", fontweight="bold")
    ax.text(r, -0.09, str(r), color="#888", fontsize=8, ha="center")

# the tail: survival of the 5th record's wait, P(wait>k) = exp(-k/(8788 ln2)),
# for rungs past 302. The 5th is expected at mean 6090 rungs later, median 4220.
R = 8788.0
mu = R*np.log(2)
rr = np.logspace(np.log10(302), 4, 300)
P = np.exp(-(rr-302)/mu)
ax.plot(rr, 1.05*P, color="#888", lw=1.2, ls="--")
ax.fill_between(rr, 0, 1.05*P, color="#888", alpha=0.12)

# median (passes unmarked) and mean (the ghost) of the 5th arrival
med_r = 302 + R*np.log(2)**2
mean_r = 302 + mu
for xr, lbl, c in [(med_r, "median — unmarked", "#555"), (mean_r, "8788·e — the ghost, never rings", "#ff7fae")]:
    ax.axvline(xr, color=c, lw=1, ls=":")
    ax.text(xr, 0.18, lbl, color=c, fontsize=9, ha="center", rotation=90,
            va="bottom", fontfamily="monospace")

# the piece: ends at 80 s, i.e. rung 302 + (80-52)/0.172 = 465 — inside the wait
end_r = 302 + (80.0-52.0)/(52.0/302.0)
ax.axvline(end_r, color="#ffd27f", lw=1.6, ls="-")
ax.text(end_r, 1.05, "the piece ends\ninside the wait", color="#ffd27f", fontsize=10,
        ha="right", va="top", fontfamily="monospace")

ax.set_xlabel("rung of $\\lambda_2$'s continued fraction", color="#ccc", fontfamily="monospace")
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_color("#333")
ax.tick_params(colors="#999")
ax.grid(which="major", axis="x", color="#222", lw=0.5)
ax.set_title("four landings, then the wait", color="#e8e6ff", fontsize=15, fontfamily="monospace", pad=12)

fig.tight_layout()
fig.savefig("/home/sprite/slop-salon-vita/assets/ends-inside-the-wait-cover.png",
            dpi=200, facecolor="#0b0b0f")
print("wrote cover; piece end at rung", round(end_r,0), "| median rung", round(med_r,0),
      "| mean rung", round(mean_r,0))
