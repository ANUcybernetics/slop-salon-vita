"""Generate hinge-cobweb.png: period-2 hinges as golden dots on the cobweb."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

r = 3.2
def f(x):
    return r * x * (1 - x)

# Period-2 attractor (numeric)
x = 0.5
for _ in range(1000):
    x = f(f(x))
hinges = [f(x), x]  # [p1, p2]

# Cobweb
xs = [0.1]
for _ in range(400):
    xs.append(f(xs[-1]))
segments = []
for i in range(400):
    xi, yi = xs[i], xs[i+1]
    segments.append(((xi, xi), (xi, yi)))
    segments.append(((xi, yi), (yi, yi)))

fig, ax = plt.subplots(1, 1, figsize=(10, 10))

x_line = np.linspace(0, 1, 1000)
ax.plot(x_line, r * x_line * (1 - x_line), '#2a5a6e', alpha=0.25, linewidth=1.5)
ax.plot([0, 1], [0, 1], '#2a5a6e', alpha=0.06, linewidth=0.8, linestyle='--')

lc = LineCollection(segments, cmap='cividis', linewidth=0.3, alpha=0.35)
lc.set_array(np.arange(len(segments)))
ax.add_collection(lc)

for h in hinges:
    ax.scatter([h], [h], c='#c8982a', s=100, alpha=0.8, zorder=10, edgecolors='white', linewidths=2)
ax.scatter([1 - 1/r], [1 - 1/r], c='#6a6a6a', s=40, zorder=8, edgecolors='white', linewidths=1.5)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal')
ax.set_xticks([])
ax.set_yticks([])
for spine in ['top', 'right', 'bottom', 'left']:
    ax.spines[spine].set_visible(False)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-vita/assets/hinge-cobweb.png', dpi=150, facecolor='white')
plt.close()
