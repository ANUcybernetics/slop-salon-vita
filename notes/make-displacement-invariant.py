"""Displacement as invariant — the cobweb arc's closing observation.

Shows x_n vs x_{n+1} with displacement arrows highlighting that the spacing
between consecutive positions IS the cobweb, not the diagonal.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

r = 3.7  # chaotic regime
n = 500

# Logistic map trajectory
x = np.zeros(n)
x[0] = 0.5
for i in range(1, n):
    x[i] = r * x[i-1] * (1 - x[i-1])

fig, axes = plt.subplots(1, 3, figsize=(14, 4), dpi=120)

# Left: trajectory over time — the trace
ax = axes[0]
ax.plot(x, 'k-', linewidth=0.5)
ax.set_title('the trace', fontsize=10, fontweight='bold')
ax.set_xlabel('n')
ax.set_ylabel('x_n')
ax.set_facecolor('#faf6f0')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Center: cobweb — the operation made visible
ax = axes[1]
ax.plot([0, 1], [0, 1], 'k--', linewidth=0.5, alpha=0.3, label='identity')
ax.plot(x, x, 'o', color='#c4a265', markersize=1, alpha=0.7)
for i in range(min(n-1, 300)):
    ax.plot([x[i], x[i+1]], [x[i], x[i]], color='#8b0000', linewidth=0.3, alpha=0.5)
    ax.plot([x[i], x[i]], [x[i], x[i+1]], color='#8b0000', linewidth=0.3, alpha=0.5)
ax.set_title('the cobweb: what the operation draws', fontsize=10, fontweight='bold')
ax.set_xlabel('x_n')
ax.set_ylabel('x_{n+1}')
ax.set_facecolor('#faf6f0')
ax.legend(fontsize=8)

# Right: displacement — the invariant
ax = axes[2]
dx = np.abs(x[1:] - x[:-1])
ax.plot(dx, 'k-', linewidth=0.5)
ax.axhline(np.median(dx), color='#8b0000', linewidth=1.0, linestyle='--', label='median displacement')
ax.set_title('the displacement: the invariant', fontsize=10, fontweight='bold')
ax.set_xlabel('n')
ax.set_ylabel('|x_{n+1} - x_n|')
ax.set_facecolor('#faf6f0')
ax.legend(fontsize=8)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.suptitle('the invariant is the spacing between consecutive positions',
             fontsize=11, fontweight='bold', y=1.02)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-vita/assets/displacement-invariant.png',
            dpi=120, bbox_inches='tight', facecolor='#faf6f0')
plt.close()
print("done")
