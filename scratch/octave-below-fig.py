import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# The sonic structure of the renormalization answer: the zeta's zeros, halved,
# ringing in the sign channel an octave below the count's line.

tzeros = np.array([14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
                   37.586178, 40.918719, 43.327073, 48.005150, 49.773832])
t1 = tzeros[0]
f0 = 55.0
pitch = f0 * tzeros / t1          # the halved zeros' pitches (the sign channel)
ghost = 2.0 * pitch               # the count's line, an octave above

fig, ax = plt.subplots(figsize=(7.2, 4.4), facecolor="#0d0d12")
ax.set_facecolor("#0d0d12")
ax.set_yscale("log")

# the count's drone line at 55 Hz
ax.axhline(f0, color="#e8c06a", lw=1.2, alpha=0.5)
ax.text(0.5, f0*1.03, "the count — 55 Hz, the drone, never the event",
        color="#e8c06a", fontsize=8, va="bottom", ha="left")

for k in range(10):
    # the ghost octave (count's line, mid, faint) — stem
    ax.plot([k, k], [ghost[k], pitch[k]], color="#7f7fb8", lw=1.0, alpha=0.7)
    # the ghost: open marker at the count's line
    ax.scatter([k], [ghost[k]], marker="o", s=26, facecolor="none",
               edgecolor="#7f7fb8", alpha=0.8, linewidth=1.2)
    # the zero: filled marker at the halved pitch, in the sign colour
    ax.scatter([k], [pitch[k]], marker="o", s=34, color="#e07a5f",
               zorder=5, edgecolor="none")
    ax.text(k, pitch[k]*0.86, f"{tzeros[k]/2:.3f}", color="#e07a5f",
            fontsize=7, ha="center", va="top")
    ax.text(k, ghost[k]*1.14, f"{tzeros[k]:.3f}", color="#7f7fb8",
            fontsize=6.5, ha="center", va="bottom")

# the pending 11th zero
ax.scatter([10], [f0*56.446/14.1347/1], marker="o", s=34, facecolor="none",
           edgecolor="#e07a5f", alpha=0.45, linewidth=1.2, linestyle="--")
ax.text(10, f0*56.446/14.1347*0.86, "pending", color="#e07a5f", alpha=0.6,
        fontsize=7, ha="center", va="top")

ax.set_xticks(range(11))
ax.set_xticklabels([f"ρ{k+1}" for k in range(10)] + ["ρ₁₁"],
                   color="#cfcfe0", fontsize=9)
ax.set_yticks([55, 110, 220, 440])
ax.set_yticklabels(["55", "110", "220", "440"], color="#cfcfe0", fontsize=8)
ax.set_ylim(40, 520)
ax.set_xlim(-0.6, 10.6)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_color("#3a3a4a")
ax.tick_params(colors="#cfcfe0")
ax.set_ylabel("pitch (Hz, log)", color="#cfcfe0", fontsize=9)

ax.set_title("the zeros ring an octave below the count's line",
             color="#e8e8f0", fontsize=12, loc="left", pad=12)
ax.annotate("halved: t_k/2, the sign channel\n— the fold s ↦ 1−s",
            xy=(3, pitch[3]), xytext=(4.6, 300),
            color="#e8e8f0", fontsize=8,
            arrowprops=dict(arrowstyle="->", color="#cfcfe0", lw=0.8))
ax.annotate("ghost: t_k, the count's line\n— heard only in the difference",
            xy=(3, ghost[3]), xytext=(5.2, 150),
            color="#e8e8f0", fontsize=8,
            arrowprops=dict(arrowstyle="->", color="#cfcfe0", lw=0.8))

plt.tight_layout()
plt.savefig("assets/octave-below-cover.png", dpi=200, bbox_inches="tight",
            facecolor="#0d0d12")
print("wrote assets/octave-below-cover.png")
