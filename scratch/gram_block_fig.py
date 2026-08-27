import mpmath as mp
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

mp.mp.dps = 20

t_lo, t_hi = 275.0, 290.0
zs  = [float(mp.zetazero(k).imag) for k in range(125, 133)]   # gold rings
gs  = [float(mp.grampoint(n)) for n in range(122, 131)]        # grey clicks
ts  = np.linspace(t_lo, t_hi, 5000)
Z   = np.array([float(mp.siegelz(t)) for t in ts])

empty = (gs[3], gs[4])   # 280.802 .. 282.455  (no ring)
dbl   = (gs[4], gs[5])   # 282.455 .. 284.104  (two rings)

fig, ax = plt.subplots(figsize=(13.5, 6.4), dpi=200)
fig.patch.set_facecolor('#0b0d12'); ax.set_facecolor('#0b0d12')

# bands
ax.axvspan(empty[0], empty[1], color='#8a3a30', alpha=0.30, zorder=1)
ax.axvspan(dbl[0],   dbl[1],   color='#b8862e', alpha=0.20, zorder=1)

# curve + seam
ax.axhline(0, color='#d4a94a', lw=1.5, alpha=0.9, zorder=2)
ax.plot(ts, Z, color='#5a6a9a', lw=1.2, alpha=0.95, zorder=3)

# gram clicks (small ticks on the seam, drawn upward)
for g in gs:
    ax.plot([g, g], [0, 0.45], color='#8a8f98', lw=2.2, solid_capstyle='butt', zorder=5)

# zero rings (gold circles on the seam)
for z in zs:
    ax.plot([z, z], [0, -0.45], color='#e8c869', lw=2.2, solid_capstyle='butt', zorder=5)
    ax.scatter([z], [0], s=70, facecolor='none', edgecolor='#e8c869', linewidth=2.0, zorder=6)

# labels with arrows
def lbl(x, y, text, color, ax_target, target_y=0):
    ax.annotate(text, xy=(x, target_y), xytext=(x, y), ha='center', va='center',
                fontsize=11.5, color=color, fontfamily='serif', fontweight='bold', zorder=7,
                arrowprops=dict(arrowstyle='-', color=color, lw=1.0, alpha=0.8,
                                shrinkA=6, shrinkB=6))
lbl((empty[0]+empty[1])/2, 3.3, 'no ring — the empty gap', '#d98a7a', ax)
lbl((dbl[0]+dbl[1])/2,     2.7, 'two rings — the doubled gap', '#e8c869', ax)

# title
ax.text(0.5, 0.975, 'the never-touch, and its first trip', transform=ax.transAxes,
        ha='center', va='top', fontsize=17, color='#e6e0d0', fontfamily='serif', fontweight='bold')
ax.text(0.5, 0.92, 'the two clocks on the seam — Z(t) near t = 282.5', transform=ax.transAxes,
        ha='center', va='top', fontsize=11.5, color='#9aa0ac', fontfamily='serif')

# footer
ax.text(0.985, 0.045,
        'for 126 gaps the rings and clicks alternate, one ring per gap.\n'
        'then, once: a gap with no ring, a gap with two rings.\n'
        'the count of rings is preserved — home.\n'
        'the local reading trips — ghost.',
        transform=ax.transAxes, ha='right', va='bottom', fontsize=10.5,
        color='#c8ccd6', fontfamily='serif', linespacing=1.6,
        bbox=dict(boxstyle='round,pad=0.55', fc='#14161d', ec='#2a2e3a', alpha=0.97))

ax.set_xlim(t_lo, t_hi); ax.set_ylim(-8.5, 4.2)
ax.set_yticks([])
ax.set_xticks(gs); ax.set_xticklabels(['']*len(gs))
ax.tick_params(colors='#8a8f98', length=0)
for sp in ax.spines.values(): sp.set_visible(False)
ax.set_xlabel('t on the critical line — gold ticks the zeros, grey ticks the Gram points',
              color='#9aa0ac', fontsize=10, fontfamily='serif')
plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-vita/assets/first-trip.png', facecolor=fig.get_facecolor(), bbox_inches='tight')
print('saved')
