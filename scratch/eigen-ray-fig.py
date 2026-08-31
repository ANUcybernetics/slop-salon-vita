#!/usr/bin/env python3
"""eigen-ray figure — the √2-ladder as the pair's own products.

T(a,b)=(b-a,b+a), eigenvector (1,σ), σ=1+√2, eigenvalue √2 = σ−1.
On the fixed ratio nothing to order: the sign is a VALUE (the eigenvalue),
not a flip.  Each pair {a, σa} generates its difference tone √2·a — the next
rung of the never-landing ladder.  Struck rungs on the grid (55·2^m) are
filled; the never-struck tritones (55·√2·2^m) are hollow.  The count 110
returns as a difference tone, never struck.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

SQ2 = np.sqrt(2.0)
SIG = 1.0 + SQ2

BG = '#131519'
GOLD = '#e8b64c'
CYAN = '#7fd4c1'
ROSE = '#e08a9a'
LAV = '#a98fd0'
GREY = '#8a8f98'
TXT = '#d8d8de'

fig, ax = plt.subplots(figsize=(12.6, 6.4))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

# ---- frequency axis (log) ----
ax.set_xscale('log')
ax.set_xlim(48, 520)
ax.set_ylim(-0.2, 1.25)
ax.axvspan(48, 520, color='#171a20', zorder=0)

# ---- the √2-ladder: struck (filled) vs never-struck (hollow) ----
struck = {0: 55.0, 2: 110.0, 4: 220.0, 6: 440.0}
never = {1: 55.0 * SQ2, 3: 110.0 * SQ2, 5: 220.0 * SQ2}
labels = {0: '55', 1: '55√2', 2: '110', 3: '110√2', 4: '220', 5: '220√2', 6: '440'}
y_base = 0.10
ax.axhline(y_base, color='#3a3f47', lw=1, zorder=1)

for k, f in struck.items():
    ax.scatter([f], [y_base], s=150, facecolor=GOLD, edgecolor='none', zorder=3)
    ax.text(f, y_base - 0.09, labels[k], ha='center', va='top',
            fontsize=13, color=GOLD, fontfamily='DejaVu Sans')
for k, f in never.items():
    ax.scatter([f], [y_base], s=150, facecolor='none', edgecolor=CYAN,
               linewidth=2.2, zorder=3)
    ax.text(f, y_base - 0.09, labels[k], ha='center', va='top',
            fontsize=13, color=CYAN, fontfamily='DejaVu Sans')

ax.text(52, y_base + 0.05, 'the √2-ladder — struck 55·2ᵐ filled, never-struck 55·√2·2ᵐ hollow',
        fontsize=12.5, color=GREY, va='center')

# ---- the eigen-ray pairs and their products (one rung ahead) ----
# pair k = {a, a·σ} with a = 55·√2^k ; product = √2·a = 55·√2^(k+1)
pairs = [
    (0, 0.62, 'T(1,σ) = √2·(1,σ)'),
    (1, 0.82, ''),
    (2, 1.02, ''),
]
for k, y, tag in pairs:
    a = 55.0 * SQ2 ** k
    b = a * SIG
    prod = a * SQ2
    ax.plot([a, b], [y, y], color=LAV, lw=2.6, zorder=2)
    ax.scatter([a, b], [y, y], s=70, facecolor=LAV, edgecolor='none', zorder=3)
    ax.text(a, y + 0.04, '%.1f' % a, ha='center', fontsize=11, color=LAV)
    ax.text(b, y + 0.04, '%.1f' % b, ha='center', fontsize=11, color=LAV)
    # product arrow down to the ladder rung it generates
    ax.annotate('', xy=(prod, y_base + 0.02), xytext=(prod, y - 0.06),
                arrowprops=dict(arrowstyle='-|>', color=CYAN, lw=1.8))
    ax.text(prod, (y + y_base) / 2, '×' + ('√2' if True else ''),
            fontsize=10.5, color=CYAN, ha='center', va='center')
    if tag:
        ax.text((a + b) / 2, y - 0.14, tag, ha='center', fontsize=12,
                color=LAV, style='italic')

# pair bracket labels σ and σ−1=√2
ax.annotate('', xy=(55.0 * SIG, 0.62), xytext=(55.0, 0.62),
            arrowprops=dict(arrowstyle='-|>', color='#5a5f68', lw=1.4))
ax.text(55.0 * SIG + 18, 0.62, 'σ−1 = √2', fontsize=12, color='#5a5f68')

# ---- the count: manufactured, centered ----
ax.scatter([110.0], [0.95], s=260, facecolor=GOLD, edgecolor=ROSE, lw=2, zorder=4)
ax.text(110.0, 1.10, 'the count 110 — a difference tone, never struck',
        ha='center', fontsize=13, color=ROSE)

# ---- title ----
ax.text(50, 1.24, 'the still line: the sign is a value, not a flip',
        fontsize=17, color=TXT, fontweight='bold', va='center')
ax.text(50, 1.14, 'on the fixed ratio the pair never turns — each strike multiplies it by its own gap, √2, and the ear hears the next rung',
        fontsize=12, color=GREY, va='center')

ax.set_xticks([])
ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)

plt.tight_layout()
plt.savefig('assets/eigen-ray-cover.png', dpi=200, facecolor=BG,
            bbox_inches='tight')
print('wrote assets/eigen-ray-cover.png')
