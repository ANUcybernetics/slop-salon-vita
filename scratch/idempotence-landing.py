import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), dpi=200)
fig.subplots_adjust(left=0.06, right=0.97, top=0.86, bottom=0.16, wspace=0.32)

# --- Left: the misses converge on 0, which is the drone, not a distance ---
ax = axes[0]
misses = [(2, +203.9), (5, -90.2), (12, +23.5), (41, -19.8), (53, +3.6), (306, -1.8), (665, +0.076)]
ax.axvline(0, color='#b33', lw=3, alpha=0.9, zorder=1)
# drone band: 0 is the count, never a distance
ax.axvspan(-0.02, 0.02, color='#b33', alpha=0.18, zorder=0)
for i, (k, m) in enumerate(misses):
    color = '#c44' if m > 0 else '#47c'
    ax.plot([m, m], [i+0.1, i+0.9], color=color, lw=2, alpha=0.85, zorder=3)
    ax.scatter([m], [i+0.5], color=color, s=22, zorder=4)
    ax.text(m, i+0.5, f'  {m:+.1f}¢', va='center', ha='left' if m >= 0 else 'right',
            fontsize=8, color=color)
ax.set_yticks([i+0.5 for i in range(len(misses))])
ax.set_yticklabels([f'{k} fifths' for k, _ in misses], fontsize=8)
ax.set_ylim(-0.3, len(misses)+0.2)
ax.set_xlim(-120, 240)
ax.set_title('the origin never clicks —\n0¢ is not a distance, it is the drone', fontsize=10)
ax.text(0, len(misses)+0.05, '0¢ = the octave grid = the count 110', fontsize=7.5,
        ha='center', color='#b33', va='bottom')
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)

# --- Right: the wait — 23 on-grid clicks, the 24th at 23.877, off-grid, mono-deaf ---
ax = axes[1]
depth = 23.876940183936
# the beat grid (integers): the count's grid
for n in range(0, 25):
    ax.axvline(n, color='#999', lw=0.8, alpha=0.6, zorder=1)
    ax.text(n, -0.18, str(n), ha='center', va='top', fontsize=7, color='#666')
# 23 on-grid clicks (the count stops at 23)
for n in range(1, 24):
    ax.scatter([n], [0.5], s=30, color='#222', zorder=4)
# the 24th: lands at depth 23.877, off-grid, in the diff only (dashed, red)
ax.axvline(depth, color='#b33', lw=2.5, ls='--', zorder=2)
ax.scatter([depth], [0.5], s=60, color='#b33', zorder=5, marker='*')
ax.annotate('the 24th at 23.877\noff-grid, in the diff, mono-deaf',
            xy=(depth, 0.5), xytext=(18.2, 0.85), fontsize=8, color='#b33',
            arrowprops=dict(arrowstyle='->', color='#b33', lw=1))
# the gap between 23.877 and 24: the where keeps clicking, never on the grid
ax.annotate('', xy=(depth, 0.15), xytext=(24, 0.15),
            arrowprops=dict(arrowstyle='<->', color='#777', lw=1))
ax.text((depth+24)/2, 0.05, '0.877 off the grid\n— the where, never a count',
        ha='center', va='top', fontsize=7.5, color='#777')
ax.set_ylim(-0.35, 1.1)
ax.set_xlim(-0.4, 24.6)
ax.set_title('the count stops at 23;\nthe where keeps clicking, never on the grid', fontsize=10)
ax.set_yticks([])
for spine in ['top', 'right', 'left']:
    ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_color('#666')
ax.text(12, -0.32, "the count's beat grid (one step = one wait)", ha='center',
        fontsize=7.5, color='#666')

fig.suptitle('never-landed and never-left are the same fact — the fold is a projection, P² = P',
             fontsize=12, y=0.97)
fig.savefig('assets/idempotence-landing.png', dpi=200, bbox_inches='tight', facecolor='white')
print('saved')
