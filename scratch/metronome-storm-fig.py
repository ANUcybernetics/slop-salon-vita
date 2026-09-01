#!/usr/bin/env python3
"""cover for metronome/storm — the two phantoms, on and off the grid.

The metals' metronome (sigma_2) clicks its phantom onto the count 110 — a
narrowing zigzag, the miss a unit fraction shrinking each beat, the sign
alternating.  The comma's storm clicks its phantom onto 61.85 — between the
seed 55 and the count 110, on no 55n.  Its tallest beats are the quotients 23
and 55 (gert): the seed's own number, counted but never struck.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

F55 = 55.0

def diff_tone(p, q):
    return 55.0 * abs(p * p - q * q) / (p * q)

# metals: sigma_2 convergents, constant waits 3.2s
S2 = [(2, 1), (5, 2), (12, 5), (29, 12), (70, 29), (169, 70), (408, 169)]
t_m = [3.2 * k for k in range(len(S2))]
f_m = [diff_tone(p, q) for p, q in S2]

# storm: log_2(3/2) convergents, storm waits
ST = [(1, 1), (1, 2), (3, 5), (7, 12), (24, 41), (31, 53), (179, 306),
      (389, 665), (9126, 15601), (18641, 31867), (46408, 79335),
      (65049, 111202), (111457, 190537), (6195184, 10590737)]
ST_QUOT = [1, 1, 2, 2, 3, 1, 5, 2, 23, 2, 2, 1, 1, 55]
t_s, tt = [], 0.0
for k in range(1, len(ST)):
    t_s.append(tt)
    tt += ST_QUOT[k] * 0.3
f_s = [diff_tone(p, q) for p, q in ST[1:]]

fig, ax = plt.subplots(figsize=(9.5, 5.2))
fig.patch.set_facecolor('white')

# grid: the harmonic rulers 55n
for g in [55.0, 110.0, 165.0, 220.0]:
    ax.axhline(g, color='#d8d3c8', lw=1.0, zorder=1)
    ax.text(45.5, g + 2, '55' if g == 55 else str(int(g)),
            ha='right', va='bottom', fontsize=8, color='#8a8578')

# storm phantoms (right side, off-grid, giants bigger)
for (tt, ff, k) in zip(t_s, f_s, range(1, len(ST))):
    big = 90 if (k in (8, 13)) else 46
    ax.plot(tt + 45, ff, 'o', color='#c2573a', ms=big / 7,
            alpha=0.9, zorder=3)
# the storm's off-grid limit
ax.axhline(61.85, color='#c2573a', lw=1.1, ls=(0, (3, 3)), alpha=0.7, zorder=2)

# metals phantoms (left side, zigzag converging to 110)
for i, (tt, ff) in enumerate(zip(t_m, f_m)):
    ax.plot(tt, ff, 's', color='#2a5a8a', ms=7, zorder=3)
ax.plot(t_m, f_m, '-', color='#2a5a8a', lw=1.0, alpha=0.5, zorder=2)
ax.axhline(110.0, color='#2a5a8a', lw=1.2, ls=(0, (3, 3)), alpha=0.8, zorder=2)

# labels
ax.text(14, 236, 'the metals\' metronome', color='#2a5a8a', fontsize=10,
        fontstyle='italic', ha='right')
ax.text(45, 236, 'the comma\'s storm', color='#c2573a', fontsize=10,
        fontstyle='italic', ha='left')
ax.text(14, 128, 'phantom → 110\non the grid', color='#2a5a8a', fontsize=8,
        ha='center', va='bottom')
ax.text(45, 66, 'phantom → 61.85\noff every 55n', color='#c2573a', fontsize=8,
        ha='center', va='bottom')
ax.text(46.8, 61.85 + 8, 'the storm\'s tallest beats: 23, 55',
        color='#c2573a', fontsize=8, ha='left', va='bottom')
ax.text(29.5, 116, 'the seed 55, never struck', color='#8a8578', fontsize=8,
        ha='center')

ax.set_xlim(0, 60)
ax.set_ylim(0, 250)
ax.set_xlabel('metronome time →      (each mark a beat)      → storm time',
              fontsize=9, color='#555')
ax.set_ylabel('the ear\'s phantom (Hz)', fontsize=9, color='#555')
for s in ['top', 'right']:
    ax.spines[s].set_visible(False)
ax.tick_params(colors='#555', labelsize=8)
ax.set_xticks([])
ax.set_yticks([])

plt.tight_layout()
plt.savefig('assets/metronome-storm-cover.png', dpi=200, bbox_inches='tight',
            facecolor='white')
print("wrote assets/metronome-storm-cover.png")
