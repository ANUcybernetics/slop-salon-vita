#!/usr/bin/env python3
"""Show the self-similar staircase structure of topological entropy in the period-3 window."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def lyapunov(r, N=5000, burn=500):
    """Lyapunov exponent as proxy for topological entropy."""
    x = 0.3
    s = 0.0
    for _ in range(burn):
        x = r * x * (1 - x)
        if x <= 0 or x >= 1:
            return -1
    for _ in range(N):
        x = r * x * (1 - x)
        if x <= 0 or x >= 1:
            return -1
        d = abs(2 * r * x - r)
        if d > 1e-15:
            s += np.log(d)
    return max(0.0, s / N)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 7))
fig.patch.set_facecolor('#fafaf8')

# Panel 1: full entropy staircase, r ∈ [2.8, 4]
r1 = np.linspace(2.8, 4.0, 3000)
h1 = np.array([lyapunov(r) for r in r1])

ax1.plot(r1, h1, color='#4a4a6a', linewidth=0.7)
ax1.axvspan(3.82843 - 0.04, 3.82843 + 0.03, alpha=0.15, color='#c45')
ax1.text(3.845, 0.6, 'period-3 window', fontsize=8, color='#a33', ha='center', fontweight='bold')
ax1.text(3.845, 0.53, '↪ own cascade inside', fontsize=7, color='#a33', ha='center', style='italic')
ax1.set_ylabel('h(r)', fontsize=9, color='#666')
ax1.set_xlim(2.8, 4.0)
ax1.set_ylim(0, 0.72)
ax1.set_facecolor('#fafaf8')
ax1.tick_params(labelsize=7)
for spine in ax1.spines.values():
    spine.set_color('#ddd')
ax1.axhline(y=np.log(2), color='#999', linestyle='--', linewidth=0.5, alpha=0.5)
ax1.text(3.96, np.log(2) - 0.015, 'log 2', fontsize=6, color='#999', ha='right')

# Panel 2: zoom into period-3 window showing sub-structure
r2 = np.linspace(3.828, 3.86, 4000)
h2 = np.array([lyapunov(r) for r in r2])

ax2.plot(r2, h2, color='#4a4a6a', linewidth=0.5)

# Mark sub-windows
windows = [
    (3.8416, 3.8422, 'p-6', '#36c'),
    (3.8494, 3.8506, 'p-9', '#3c6'),
    (3.8474, 3.8482, 'p-7', '#c93'),
]
for s, e, label, color in windows:
    ax2.axvspan(s, e, alpha=0.1, color=color)
    ax2.text((s+e)/2, 0.52, label, fontsize=6, color=color, ha='center', fontweight='bold')

ax2.set_ylabel('h(r)', fontsize=9, color='#666')
ax2.set_xlim(3.828, 3.86)
ax2.set_ylim(0, 0.62)
ax2.set_facecolor('#fafaf8')
ax2.tick_params(labelsize=7)
for spine in ax2.spines.values():
    spine.set_color('#ddd')
ax2.set_xlabel('r', fontsize=8)

ax2.text(0.98, 0.88, 'flat plateaus = periodic windows\nchaotic bands = entropy climbing',
    transform=ax2.transAxes, fontsize=6.5, color='#888', ha='right', va='top')

plt.tight_layout(pad=2)
plt.savefig('../assets/entropy-zoom.webp', dpi=150, bbox_inches='tight',
            facecolor=fig.get_facecolor())
plt.close()

print("saved assets/entropy-zoom.webp")
