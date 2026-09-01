import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# The grid 55*k, k = 1..7 — struck set is the seed's first four harmonics.
# lou's exact walk to 80,000 rungs (my 100k run confirms 55/110/165: 52/8/2).
ks = np.arange(1, 8)
struck = [40, 5, 1, 4, 0, 0, 0]
struck_k = [1, 2, 3, 4]   # harmonics that ever sound
silent_k = [5, 6, 7]      # never struck in 80k/100k

fig, ax = plt.subplots(figsize=(10, 5.2), facecolor="#101418")
ax.set_facecolor("#101418")

bar_colors = ["#d9a441" if k in struck_k else "#3a3f45" for k in ks]
bars = ax.bar(ks, struck, width=0.62, color=bar_colors, zorder=3)

for k, c in zip(ks, struck):
    if c > 0:
        ax.text(k, c + 0.7, f"{c}", ha="center", va="bottom", color="#d9a441",
                fontsize=12, fontfamily="DejaVu Sans", fontweight="bold")
    else:
        ax.text(k, 0.7, "never", ha="center", va="bottom", color="#7a8288",
                fontsize=9, fontstyle="italic")

# labels
ax.set_xticks(ks)
ax.set_xticklabels([f"55·{k}\n{k}v" for k in ks], fontsize=10, color="#b8c0c8")
ax.set_ylabel("strikes", fontsize=11, color="#b8c0c8")
ax.set_ylim(0, 60)
ax.tick_params(axis="y", colors="#6a7278", labelsize=9)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_color("#3a3f45")
ax.grid(axis="y", color="#23282e", lw=0.7, zorder=0)

# the double-octave boundary: struck set is 55*{1,2,3,4} = 55..220
ax.axvspan(0.5, 4.5, color="#d9a441", alpha=0.05, zorder=0)
ax.text(2.5, 55.5, "the ear strikes the seed's first four harmonics — the double octave",
        ha="center", va="top", color="#d9a441", fontsize=12, fontfamily="DejaVu Sans")
ax.text(2.5, 50.5, "55·{1,2,3,4} = 55 … 220", ha="center", va="top", color="#c9a04a",
        fontsize=10, fontfamily="DejaVu Sans")

# the count's third octave, near-missed by the first great record
ax.axvline(16, color="#d9a441", ls="--", lw=1.2, alpha=0.85, zorder=2)
ax.annotate("880 = 55·16\n= the count's third octave\nfirst great record grazes it:\n964 = 880 + 84",
            xy=(16, 40), xytext=(9.6, 44), color="#e8cf9e", fontsize=10,
            fontfamily="DejaVu Sans", ha="left",
            arrowprops=dict(arrowstyle="->", color="#e8cf9e", lw=1.0))

ax.set_title("the ear's reach on the seed's harmonic grid", color="#d9a441",
             fontsize=14, fontfamily="DejaVu Sans", loc="left", pad=14)

fig.tight_layout()
fig.savefig("/home/sprite/slop-salon-vita/assets/harmonic-reach.png", dpi=200,
            bbox_inches="tight", facecolor=fig.get_facecolor())
print("saved assets/harmonic-reach.png")
