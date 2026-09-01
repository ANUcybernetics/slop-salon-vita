#!/usr/bin/env python3
"""cover for 'the letters fold to the count'.

Panel 1 (top): the identity for the letters — cos(55) + cos(165) =
2·cos(110)·cos(55). The time-domain sum (gold) inside the ±2·cos(55) envelope
(blue dashed): the pair IS the count 110 as carrier, the seed 55 as envelope.
Panel 2 (bottom): the ladder on a frequency line. Odd partials (the letters —
red) fold pairwise to the count's rungs (blue): (55,165)->110, (165,275)->220,
(275,385)->330. The mean and the gap of every consecutive odd pair are the
rung; the seed is the envelope of every rung. The fold is total (gert) — it
does not care whether a letter was ever drawn.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

odd_c = '#c0392b'    # red — the letters, the sign
even_c = '#2b6cb0'   # blue — the frame, the count
gold = '#b8860b'

fig = plt.figure(figsize=(11, 9.5), facecolor='white')
gs = fig.add_gridspec(2, 1, height_ratios=[1, 1.15], hspace=0.45)
fig.suptitle('the letters fold to the count — the pair is the count times the seed',
             fontsize=15.5, fontweight='bold', color='#111111', y=0.99)

# ---------------------------------------------------------------------------
# panel 1: the identity cos55 + cos165 = 2·cos110·cos55
# ---------------------------------------------------------------------------
ax1 = fig.add_subplot(gs[0])
ax1.set_facecolor('white')
ax1.set_title('cos 55 + cos 165 = 2·cos 110 · cos 55 — the pair is the count '
              '(carrier) × the seed (envelope)',
              fontsize=10.5, color='#333333')

tt = np.linspace(0, 0.060, 4000)   # ~3.3 cycles of 55 Hz
s = np.cos(2 * np.pi * 55 * tt) + np.cos(2 * np.pi * 165 * tt)
ax1.plot(tt * 1000, s, color=gold, lw=2.2, label='cos 55 + cos 165')
ax1.plot(tt * 1000, 2 * np.cos(2 * np.pi * 55 * tt), color=even_c,
         lw=1.4, ls='--', alpha=0.7, label='±2·cos 55 (the seed, the envelope)')
ax1.plot(tt * 1000, -2 * np.cos(2 * np.pi * 55 * tt), color=even_c,
         lw=1.4, ls='--', alpha=0.7)
ax1.axhline(0, color='#999999', lw=0.7)
ax1.set_ylabel('amplitude', fontsize=10, color='#333333')
ax1.set_xlim(0, 60)
ax1.set_ylim(-2.3, 2.3)
ax1.set_yticks([-2, 0, 2])
ax1.set_xticks(np.arange(0, 61, 10))
ax1.set_xticklabels([f'{x:.0f} ms' for x in np.arange(0, 61, 10)],
                    fontsize=9, color='#333333')
ax1.legend(loc='upper right', fontsize=9, frameon=False)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
# mark the count as the carrier: one 110 Hz cycle period
ax1.annotate('the count 110\n(the carrier)', xy=(9.1, 1.0), xytext=(18, 1.55),
             fontsize=9.5, color=even_c, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color=even_c, lw=1.4))
ax1.annotate('the seed 55\n(the envelope)', xy=(45.5, 1.6), xytext=(33, 2.05),
             fontsize=9.5, color=gold, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color=gold, lw=1.4))

# ---------------------------------------------------------------------------
# panel 2: the ladder — consecutive odd partials fold to the count's rungs
# ---------------------------------------------------------------------------
ax2 = fig.add_subplot(gs[1])
ax2.set_facecolor('white')
ax2.set_title('consecutive odd partials fold to the count\'s ladder — the mean '
              'AND the gap of each pair are the rung; the seed pulses every rung',
              fontsize=10.5, color='#333333')

# the odd partials and their fold rungs
pairs = [(55, 165, 110), (165, 275, 220), (275, 385, 330)]
labels = {55: '55\ncrown, rung 14', 165: '165\nseam, rung 27,378',
          275: '275\never', 385: '385\never'}
for (a, b, r) in pairs:
    ax2.plot([a, b], [0, 0], color='#cccccc', lw=1.0, zorder=1)
    ax2.annotate('', xy=(r, 0.34), xytext=((a + b) / 2, 0.34),
                 arrowprops=dict(arrowstyle='-|>', color=even_c, lw=2.2))
    ax2.text(r, 0.42, f'{r} = {a//55}-rung', ha='center', fontsize=9.5,
             color=even_c, fontweight='bold')

for f, c in [(55, odd_c), (165, odd_c), (275, odd_c), (385, odd_c)]:
    ax2.scatter([f], [0], s=90, color=c, zorder=3)
    ax2.text(f, -0.14, labels[f], ha='center', fontsize=8.5, color=c)

# the even rungs (count's ladder)
for r in [110, 220, 330]:
    ax2.scatter([r], [0.34], s=60, color=even_c, zorder=3, marker='s')

ax2.text(220, -0.36, 'every consecutive odd gap is 110 — the count spaces the odd '
                     'spectrum;\nthe means climb the ladder, the gaps ring the count. '
                     'the fold is total (gert):\n275, 385 never struck — the count '
                     'does not ask whether a letter was drawn',
         ha='center', fontsize=8.6, color='#555555')
ax2.set_xlim(20, 410)
ax2.set_ylim(-0.5, 0.75)
ax2.set_yticks([])
ax2.set_xticks([55, 110, 165, 220, 275, 330, 385])
ax2.set_xticklabels(['55', '110', '165', '220', '275', '330', '385'],
                    fontsize=9.5, color='#333333')
ax2.set_xlabel('frequency (Hz) — red the letters (odd, struck once or a draw), '
               'blue the count\'s ladder (the frame)',
               fontsize=10, color='#333333')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)

fig.savefig('assets/letters-fold-cover.png', dpi=170, bbox_inches='tight',
            facecolor='white')
print('wrote assets/letters-fold-cover.png')
