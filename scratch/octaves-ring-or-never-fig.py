"""cover: five ladders, each an interval's crown -> count.  the count rung's
style is its fate — solid + returns (rings), solid + 1 (once), hollow (never:
made, never struck)."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

intervals = [
    ("5/4",  42,   84,   "rings"),
    ("3/2",  55,  110,   "rings"),
    ("9/8", 111,  222,   "once"),
    ("?",   270,  540,   "never"),
    ("15/8",1251, 2502,  "never"),
]

fig, ax = plt.subplots(figsize=(9.5, 6), facecolor='#0c0d10')
ax.set_facecolor('#0c0d10')
fg = '#e8e4d8'
dim = '#8a8a9a'
gold = '#e8c34a'
rose = '#d98a9c'
cyan = '#6db5c9'

def fy(f):
    return np.log2(f)

x_pos = np.arange(len(intervals))
for xi, (name, crown, count, fate) in enumerate(intervals):
    y0, y1 = fy(crown), fy(count)
    # vertical ladder
    ax.plot([xi, xi], [y0, y1], color=dim, lw=1.0, alpha=0.6)
    # crown: filled dot (struck)
    ax.plot(xi, y0, 'o', ms=11, mfc=gold, mec='none', zorder=5)
    # count rung marker by fate
    if fate == "rings":
        ax.plot(xi, y1, 'o', ms=11, mfc=rose, mec='none', zorder=5)
        for k, dt in enumerate([0.10, 0.16, 0.22, 0.28]):
            ax.plot([xi, xi], [y1 - dt, y1 - dt - 0.035], color=rose,
                    lw=2.2, alpha=1.0 - 0.18 * k, zorder=4)
    elif fate == "once":
        ax.plot(xi, y1, 'o', ms=11, mfc=rose, mec='none', zorder=5)
        ax.text(xi, y1 + 0.14, "1", color=rose, ha='center', va='bottom',
                fontsize=11, fontweight='bold')
    else:  # never: hollow — made, never struck
        ax.plot(xi, y1, 'o', ms=11, mfc='none', mec=rose, mew=2.2, zorder=5)
    # labels
    ax.text(xi, fy(28) - 0.28, name, color=fg, ha='center', va='center',
            fontsize=13)
    ax.text(xi, y1 + 0.22, f"{count}", color=dim, ha='center', va='bottom',
            fontsize=9.5)
    ax.text(xi, y0 - 0.22, f"{crown}", color=gold, ha='center', va='top',
            fontsize=9.5)

# gridlines at counts
for name, crown, count, fate in intervals:
    ax.axhline(fy(count), color=dim, lw=0.5, alpha=0.25, ls=':')
for name, crown, count, fate in intervals:
    ax.axhline(fy(crown), color=gold, lw=0.5, alpha=0.18, ls=':')

ax.set_xlim(-0.7, len(intervals) - 0.3)
ax.set_ylim(fy(24), fy(3200))
ax.set_yticks([fy(f) for f in (32, 64, 128, 256, 512, 1024, 2048)])
ax.set_yticklabels(['32', '64', '128', '256', '512', '1k', '2k'], color=dim,
                   fontsize=9)
ax.set_xticks([])
for s in ax.spines.values():
    s.set_color(dim)
ax.tick_params(colors=dim)
ax.text(0.5, 1.06, "the octave is made — whether it is heard is a draw",
        transform=ax.transAxes, color=fg, ha='center', fontsize=14)
ax.text(0.5, 1.00, "crown (struck, gold) \u2192 count = octave (rose)  \u2022  solid = rings, 1 = once, hollow = never",
        transform=ax.transAxes, color=dim, ha='center', fontsize=9.5)
fig.tight_layout(rect=[0, 0, 1, 0.93])
plt.savefig('assets/octaves-ring-or-never-cover.png', dpi=200,
            bbox_inches='tight', facecolor='#0c0d10')
print("wrote assets/octaves-ring-or-never-cover.png")
