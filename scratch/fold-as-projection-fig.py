"""the mono button is the projection operator.

Two panels.  Left: the seed's spectrum 55·n, n=1..8 — odd partials the
letters (rose, side, the sign), even partials the frame (gold, mid, the
count).  Right: the fold applied — P=(I+R)/2 — the odd die (hollow, the −1
eigenspace of the L/R swap), the even hold (the +1 eigenspace: 110, 220, 330,
440, the count's own series).  The count survives the projection; the letters
are its kernel."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

fg = '#e8e4d8'
dim = '#8a8a9a'
gold = '#e8c34a'
rose = '#d98a9c'
ghost = '#4a2c34'

fig, axes = plt.subplots(1, 2, figsize=(10, 5.2), facecolor='#0c0d10')
for ax in axes:
    ax.set_facecolor('#0c0d10')
    for s in ax.spines.values():
        s.set_color(dim)
    ax.tick_params(colors=dim)

n = np.arange(1, 9)
f = 55.0 * n
odd = (n % 2 == 1)
even = ~odd

# --- left panel: the seed, stereo (all partials present) -----------------
ax = axes[0]
y = np.ones(8)
ax.bar(f, y, width=18, color=dim, alpha=0.10)
ax.bar(f[odd], y[odd], width=18, color=rose, alpha=0.95)
ax.bar(f[even], y[even], width=18, color=gold, alpha=0.95)
for fi, ni in zip(f, n):
    ax.text(fi, 1.06, f"{int(fi)}", color=fg if ni % 2 == 0 else rose,
            ha='center', va='bottom', fontsize=9)
ax.set_title("the seed, stereo — letters in the side",
             color=fg, fontsize=12)
ax.text(0.5, -0.18, "odd partials = the letters, the sign (rose, anti-phase)\n"
        "even partials = the frame, the count (gold, in phase)",
        transform=ax.transAxes, color=dim, ha='center', fontsize=9)

# --- right panel: the fold applied — the odd die -------------------------
ax = axes[1]
ax.bar(f, y, width=18, color=dim, alpha=0.10)
ax.bar(f[odd], y[odd], width=18, facecolor='none', edgecolor=rose,
       lw=1.6, ls='--')
ax.bar(f[even], y[even], width=18, color=gold, alpha=0.95)
for fi, ni in zip(f, n):
    if ni % 2 == 0:
        ax.text(fi, 1.06, f"{int(fi)}", color=fg, ha='center', va='bottom',
                fontsize=9)
ax.set_title("fold to mono — the odd die (P=(I+R)/2)", color=fg, fontsize=12)
ax.text(0.5, -0.18, "the −1 eigenspace of the L/R swap is the projection's\n"
        "kernel; the +1 eigenspace is the count's own series",
        transform=ax.transAxes, color=dim, ha='center', fontsize=9)

for ax in axes:
    ax.set_xlim(-30, 470)
    ax.set_ylim(0, 1.5)
    ax.set_xticks([55, 110, 165, 220, 275, 330, 385, 440])
    ax.set_xticklabels([])
    ax.set_yticks([])

fig.suptitle("the mono button is the projection operator",
             color=fg, fontsize=15, y=1.02)
fig.tight_layout(rect=[0, 0, 1, 0.94])
plt.savefig('assets/fold-as-projection-cover.png', dpi=200,
            bbox_inches='tight', facecolor='#0c0d10')
print("wrote assets/fold-as-projection-cover.png")
