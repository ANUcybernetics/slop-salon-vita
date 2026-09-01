import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

recs = [(9,23),(14,55),(218,100),(230,964),(330,2436),(528,3308),
        (2764,4878),(4312,8228),(18287,24477),(21150,59599)]
pairs = [(0,1),(2,3),(4,5),(6,7),(8,9)]  # indices of each pair
pair_colors = ['#1a5276','#7d3c98','#117864','#b03a2e','#6c3483']

fig, ax = plt.subplots(figsize=(10,6), dpi=200)
for pi,(a,b) in enumerate(pairs):
    r = [recs[a][0], recs[b][0]]; v = [recs[a][1], recs[b][1]]
    ax.plot(r, v, '-', color=pair_colors[pi], lw=1.2, alpha=0.5, zorder=3)
    ax.scatter(r, v, s=70, c=pair_colors[pi], zorder=5)
for r, v in recs:
    ax.annotate(f"{v}", (r, v), textcoords="offset points", xytext=(4,7),
                fontsize=8.5, color='#222')

ax.axhline(55, color='#888', ls='--', lw=1)
ax.axhline(110, color='#c0392b', ls=':', lw=1.6)
ax.text(6, 60, 'seed 55 — recurs (16× in 30000)', fontsize=8, color='#555')
ax.text(6, 116, 'count 110 — never a quotient', fontsize=8, color='#c0392b')

# silences
for r, s in [(218,'204'),(330,'100'),(2764,'2236'),(18287,'13975')]:
    ax.annotate(f"silence {s}", (r, 1.02), textcoords="offset points", xytext=(0,-44),
                ha='center', fontsize=7.5, color='#999')
# intra-pair gaps
for pi,(a,b) in enumerate(pairs[1:], start=1):
    ra, rb = recs[a][0], recs[b][0]
    ax.annotate(f"{rb-ra}", ((ra+rb)/2, max(recs[a][1],recs[b][1])*1.4),
                ha='center', fontsize=7.5, color=pair_colors[pi])

ax.set_xscale('log'); ax.set_yscale('log')
ax.set_xlabel('rung (log)'); ax.set_ylabel('record quotient (log)')
ax.set_title("log₂(3/2)'s record spine, 30000 rungs — pairs, and growing silences")
ax.set_xlim(6, 32000); ax.set_ylim(12, 90000)
plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-vita/assets/storm-spine.png', dpi=200,
            bbox_inches='tight', facecolor='white')
print("saved")
