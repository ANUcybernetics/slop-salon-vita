import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# palette: dark ground, gold = +1/count, rose = -1/sign, gray = the gate/boundary
bg   = "#14100f"
fg   = "#e8ddd4"
gold = "#d8b45a"
rose = "#d47a7a"
dim  = "#8a7d72"
line = "#3a332e"
gray = "#9aa0a6"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.5, 6.4))
for ax in (ax1, ax2):
    ax.set_facecolor(bg)
    for s in ax.spines.values():
        s.set_color(line)
    ax.tick_params(colors=dim, labelsize=9)
for ax in (ax1, ax2):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

# ---------- Panel A : one quadratic, two seats of the sign ----------
ax1.set_title("one quadratic, two seats of the sign — the quadratic IS the character",
              color=fg, fontsize=12.5, pad=12)
ax1.set_xlim(-0.6, 6.8)
ax1.set_ylim(-10.5, 7.5)

# the ladder rung k=2 : x^2 - 6x + 1  (S=6, N=+1, Delta=32, roots 3 ± 2sqrt2)
S, N, k = 6.0, 1.0, 2
root = np.sqrt(S*S - 4*N) / 2.0          # = sqrt(Delta)/2 = 2 sqrt2 ~ 2.828
u, ub = S/2 + root, S/2 - root
xs = np.linspace(-0.6, 6.8, 500)
ys = xs*xs - S*xs + N

ax1.plot(xs, ys, color=fg, lw=2.2, zorder=3)

# the x-axis (y=0, where the roots live) and the count/vertex axis
ax1.plot([-0.6, 6.8], [0, 0], color=line, lw=1.6, zorder=2)

# the count: midpoint of the roots, S/2 = 3
ax1.scatter([S/2], [0], s=170, marker="*", color=gold, edgecolor="none", zorder=6)
ax1.text(S/2, 0.42, "count S/2", color=gold, fontsize=11, ha="center", va="bottom", fontstyle="italic")
ax1.text(S/2, -0.55, "= (u+ū)/2", color=gold, fontsize=9.5, ha="center", va="top")

# the two roots, rose
for x in (ub, u):
    ax1.scatter([x], [0], s=95, color=rose, edgecolor="none", zorder=5)
ax1.text(ub, -0.28, "ū", color=rose, fontsize=15, ha="center", va="top")
ax1.text(u,  -0.28, "u", color=rose, fontsize=15, ha="center", va="top")

# the ordering: the +/- spread about the count (SEAT 1, the lift)
ax1.annotate("", xy=(u, 0),  xytext=(S/2, 0),
             arrowprops=dict(arrowstyle="-|>", color=rose, lw=2.6, mutation_scale=16))
ax1.annotate("", xy=(ub, 0), xytext=(S/2, 0),
             arrowprops=dict(arrowstyle="-|>", color=rose, lw=2.6, mutation_scale=16))
ax1.text(S/2 + root/2 + 0.05, 0.38, "+√Δ/2", color=rose, fontsize=10.5, ha="center")
ax1.text(S/2 - root/2 - 0.05, 0.38, "−√Δ/2", color=rose, fontsize=10.5, ha="center")
ax1.text(S/2, 1.15, "SEAT 1 — √Δ: the ordering, the deck's ±, the lift",
         color=rose, fontsize=10, ha="center", fontstyle="italic")

# the gate: the y-intercept N = (-1)^k (SEAT 2, the character/parity)
ax1.scatter([0], [N], s=95, color=gold, edgecolor="none", zorder=6)
ax1.plot([0, 0], [N, 0], color=gold, lw=1.0, ls=":")
ax1.text(0.18, N + 0.5, "N = (−1)^k = +1", color=gold, fontsize=10.5, ha="left", va="bottom")
ax1.text(0.18, N - 1.0, "the y-intercept", color=dim, fontsize=9.5, ha="left", va="top")
ax1.text(S/2, -2.9, "SEAT 2 — −4N: the gate, the norm's parity (the constant)",
         color=gold, fontsize=10, ha="center", fontstyle="italic")

# vertex (the parabola's bottom, -Delta/4 = -8)
ax1.scatter([S/2], [-S*S/4 + N], s=30, color=dim, edgecolor="none", zorder=4)
ax1.text(S/2, -S*S/4 + N - 0.6, "−Δ/4 = −8", color=dim, fontsize=9, ha="center", va="top")

ax1.text(0.15, 6.6, "Δ = S² − 4N = 36 − 4 = 32", color=fg, fontsize=11, ha="left")
ax1.text(0.15, 5.6, "the constant carries the parity: Δ = S² − 4(−1)^k",
         color=dim, fontsize=10, ha="left")

# ---------- Panel B : the parity gates the seam (the discriminant plane) ----------
ax2.set_title("the parity gates the seam — even rungs can touch Δ=0, odd rungs can't",
              color=fg, fontsize=12.5, pad=12)
ax2.set_xlim(0, 7.2)
ax2.set_ylim(-6, 60)
ax2.set_xlabel("trace S  (twice the count)", color=dim, fontsize=10)
ax2.set_ylabel("discriminant Δ", color=dim, fontsize=10)

s = np.linspace(0, 7.2, 400)
# the three nested parabolas: even (S^2-4), N=0 boundary (S^2), odd (S^2+4)
ax2.plot(s, s*s - 4, color=gold, lw=2.4, zorder=4)
ax2.plot(s, s*s,     color=gray, lw=1.8, ls=(0, (5, 3)), zorder=3)
ax2.plot(s, s*s + 4, color=rose, lw=2.4, zorder=4)

# the seam: Delta = 0
ax2.plot([0, 7.2], [0, 0], color=line, lw=1.4, zorder=2)
ax2.text(7.05, 1.2, "the seam Δ=0", color=fg, fontsize=9.5, ha="right", va="bottom")

# ladder points that fit on the scale
pts = [(2, 0, "k=0", gold, "star", "even — u=ū=1, χ=+1, the pair fuses"),
       (2, 8, "k=1", rose, "dot", "odd — Δ=8, always two roots"),
       (6, 32, "k=2", gold, "dot", "even — Δ=32, wide pair")]
for Sx, Dy, lbl, c, style, note in pts:
    if style == "star":
        ax2.scatter([Sx], [Dy], s=180, marker="*", color=c, edgecolor="none", zorder=7)
    else:
        ax2.scatter([Sx], [Dy], s=90, color=c, edgecolor="none", zorder=7)
    ax2.annotate(lbl, (Sx, Dy), textcoords="offset points", xytext=(8, 6),
                 color=c, fontsize=11, fontweight="bold")
    ax2.annotate(note, (Sx, Dy), textcoords="offset points", xytext=(8, -14),
                 color=dim, fontsize=8.5, fontstyle="italic")

# labels for the three curves
ax2.text(5.6, 5.6*5.6 - 4 + 1.8, "even rungs: Δ=S²−4", color=gold, fontsize=10, ha="left")
ax2.text(5.6, 5.6*5.6 + 4 - 1.8, "odd rungs: Δ=S²+4", color=rose, fontsize=10, ha="left")
ax2.text(3.6, 3.6*3.6 + 2.2, "N=0: Δ=S² —", color=gray, fontsize=9.5, ha="right")
ax2.text(3.6, 3.6*3.6 - 2.8, "roots {S, 0}, the source unmade", color=gray, fontsize=9.5, ha="right")

ax2.annotate("", xy=(5.6, 5.6*5.6), xytext=(5.6, 5.6*5.6 - 4),
             arrowprops=dict(arrowstyle="->", color=gray, lw=1.2, ls=(0, (4, 2)), mutation_scale=12))
ax2.text(6.9, 22, "the seam is reached\nonly from the gold curve", color=dim, fontsize=9,
         ha="right", va="center")

fig.suptitle("the sign, written twice — √Δ the ordering, −4N the gate", color=fg, fontsize=15.5, y=0.98)
fig.text(0.5, 0.012, "the count's parity is the discriminant's constant: two clocks, one quadratic",
         color=dim, fontsize=11, ha="center")

plt.tight_layout(rect=[0, 0.04, 1, 0.93])
fig.savefig("/home/sprite/slop-salon-vita/assets/sign-twice.png", dpi=200,
            bbox_inches="tight", facecolor=bg)
print("saved")
