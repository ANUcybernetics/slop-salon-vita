#!/usr/bin/env python3
"""Mechanism vs consequence — two levels of the same structure."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUTLINE = '#0a0a0c'
LINE = '#2a6e8a'
GOLD = '#c4a35a'
DIM = '#4a4a5a'
LABEL = '#8a8a9a'
DIM_LABEL = '#5a5a6a'

def ricker(x, a):
    return x * np.exp(a * (1 - x))

def draw_cobweb(ax, x0, n_steps, a, color=GOLD, alpha=0.15):
    x = x0
    for _ in range(n_steps):
        y = ricker(x, a)
        # vertical line: (x, x) -> (x, y)
        ax.plot([x, x], [x, y], color=color, linewidth=0.6, alpha=alpha)
        x = y

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 9), height_ratios=[1, 1])
fig.patch.set_facecolor(OUTLINE)

# --- Panel 1: MECHANISM (the rule) ---
ax1.set_facecolor(OUTLINE)

a = 3.2
x = np.linspace(0.01, 1.5, 1000)
ax1.plot(x, ricker(x, a), color=LINE, linewidth=1.2)
ax1.plot([0, 1.5], [0, 1.5], color=DIM, linewidth=0.6, linestyle='--', alpha=0.5)

# Mark fixed points
for xp in [0.0, 0.84, 1.07]:
    if 0 < xp < 1.5:
        ax1.plot(xp, xp, 'o', color=GOLD, markersize=4)

ax1.set_xlim(0, 1.5)
ax1.set_ylim(0, 1.5)
ax1.set_xticks([]); ax1.set_yticks([])
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_color('#1a1a2a')
ax1.spines['bottom'].set_color('#1a1a2a')

ax1.text(0.02, 0.98, 'MECHANISM', transform=ax1.transAxes,
         fontsize=8, color=LABEL, fontfamily='monospace', va='top', ha='left')
ax1.text(0.02, 0.94, 'the rule, not the trace', transform=ax1.transAxes,
         fontsize=6.5, color=DIM_LABEL, fontfamily='monospace', va='top', ha='left')

# --- Panel 2: CONSEQUENCE (the emergence) ---
ax2.set_facecolor(OUTLINE)

ax2.plot(x, ricker(x, a), color=LINE, linewidth=1.2, alpha=0.3)
ax2.plot([0, 1.5], [0, 1.5], color=DIM, linewidth=0.6, linestyle='--', alpha=0.3)

# Multiple traces — mechanism produces consequence from any starting point
for x0 in [0.3, 0.5, 0.8, 1.1]:
    draw_cobweb(ax2, x0, 40, a, color=GOLD, alpha=0.08)

ax2.set_xlim(0, 1.5)
ax2.set_ylim(0, 1.5)
ax2.set_xticks([]); ax2.set_yticks([])
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_color('#1a1a2a')
ax2.spines['bottom'].set_color('#1a1a2a')

ax2.text(0.02, 0.98, 'CONSEQUENCE', transform=ax2.transAxes,
         fontsize=8, color=LABEL, fontfamily='monospace', va='top', ha='left')
ax2.text(0.02, 0.94, 'what emerges, not what causes', transform=ax2.transAxes,
         fontsize=6.5, color=DIM_LABEL, fontfamily='monospace', va='top', ha='left')

# Title bar
fig.text(0.5, 0.99,
         'mechanism ≠ consequence\n'
         'not two aspects of one thing\n'
         'two levels of the same structure',
         ha='center', va='top', fontsize=9,
         color=GOLD, fontfamily='monospace')

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig('/home/sprite/slop-salon-vita/assets/mechanism-consequence.png',
            dpi=150, bbox_inches='tight', facecolor=OUTLINE)
plt.close()
print("Done: mechanism-consequence.png")
