#!/usr/bin/env python3
"""cover for 'the root folded is the count' — the odd partials are the letters.

Two panels. Top: the seed's harmonic series 55·{1..8}, partial n flipping by
(-1)^n — odd partials the letters (red), even the frame (blue). Bars carry the
striking data from the exact walk (80,000 rungs, cross-validated): 55 struck 40×
and crowned, 110 five all post-bar, 165 once, 220 four, 275/330/385 never.
Bottom: the fold — mono = (L+R)/2 cancels the odd partials exactly, the pitch
lifts an octave, and what holds is 110, 220, 330, 440: the count's own series.
the count is the root folded.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# striking data to 80k (lou's table, cross-validated with my 100k run)
strikes = {1: 40, 2: 5, 3: 1, 4: 4, 5: 0, 6: 0, 7: 0}   # 55·1 .. 55·7
MAXK = 8

fig, (ax1, ax2) = plt.subplots(
    2, 1, figsize=(11, 9.5), facecolor='white',
    gridspec_kw={'height_ratios': [1, 1], 'hspace': 0.42})
fig.suptitle('the root folded is the count — the odd partials are the letters',
             fontsize=15.5, fontweight='bold', color='#111111', y=0.99)

odd_c = '#c0392b'    # red — the letters, the sign, killed in mono
even_c = '#2b6cb0'   # blue — the frame, the count, kept
ghost = '#bbbbbb'

# ---------------------------------------------------------------------------
# panel 1: the seed's series, odd/even, with the striking data
# ---------------------------------------------------------------------------
ax1.set_facecolor('white')
ax1.set_title('partial n of 55 flips by (−1)ⁿ — odd = the letters (55 crowned, '
              '165 spoke once), even = the frame (returns only)',
              fontsize=10.5, color='#333333')

k = np.arange(1, MAXK + 1)
heights = [strikes.get(i, 0) for i in k]
cols = [odd_c if i % 2 == 1 else even_c for i in k]
ax1.bar(k, heights, color=cols, alpha=0.85, width=0.62, edgecolor='white')
for i, h in zip(k, heights):
    if h > 0:
        ax1.text(i, h + 1.1, str(h), ha='center', fontsize=11,
                 fontweight='bold', color=cols[i - 1])
    else:
        ax1.text(i, 0.6, 'never', ha='center', fontsize=8.5, color='#888888')
ax1.set_xticks(k)
ax1.set_xticklabels([f'{55 * i}' for i in k], fontsize=9.5, color='#333333')
ax1.set_xlabel('partial of the seed 55', fontsize=10, color='#333333')
ax1.set_ylabel('struck in 80,000 rungs', fontsize=10, color='#333333')
ax1.set_ylim(0, 48)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# legend as inline labels
ax1.text(0.62, 44.5, 'letters (odd) — the sign, stereo-only',
         fontsize=9.5, color=odd_c, style='italic')
ax1.text(0.62, 41.5, 'frame (even) — the count, mono-safe',
         fontsize=9.5, color=even_c, style='italic')
ax1.axvspan(0.4, 4.6, color='#f0f0f0', zorder=0)
ax1.text(2.5, 33.5, 'the double octave\n55·{1,2,3,4} — struck through',
         ha='center', fontsize=9.5, color='#444444')

# ---------------------------------------------------------------------------
# panel 2: the fold — mono cancels the odd, the pitch lifts an octave
# ---------------------------------------------------------------------------
ax2.set_facecolor('white')
ax2.set_title('fold to mono — L=R=(L+R)/2: the odd cancel, the pitch lifts an '
              'octave, what holds is 110, 220, 330 — the count is the root folded',
              fontsize=10.5, color='#333333')

x = np.linspace(40, 480, 4000)
g = lambda f0, w: np.exp(-((x - f0) / w) ** 2)

# before the fold: all partials present, odd ghosted (they are about to die)
for i in k:
    f0 = 55 * i
    if i % 2 == 1:
        ax1v = 0.70 * g(f0, 6) + 0.20 * g(f0, 3)
        ax2.fill_between(x, ax1v, color=ghost, alpha=0.75)
        ax2.text(f0, 0.78, '×', ha='center', fontsize=16, color=odd_c,
                 fontweight='bold', zorder=5)
    else:
        ax2.fill_between(x, g(f0, 6), color=even_c, alpha=0.75)

# the octave lift arrow: 55 folded -> 110
ax2.annotate('', xy=(110, 1.42), xytext=(55, 1.42),
             arrowprops=dict(arrowstyle='-|>', color='#111111', lw=2.2))
ax2.text(82.5, 1.50, 'the fold', ha='center', fontsize=10.5, color='#111111',
         fontweight='bold')
ax2.text(110, 1.18, '110 = the count', ha='center', fontsize=10,
         color=even_c, fontweight='bold')
ax2.text(55, -0.16, '55 dies', ha='center', fontsize=9, color=odd_c)
ax2.text(165, -0.16, '165 spoke once,\ngone', ha='center', fontsize=8.5,
         color=odd_c)
ax2.text(220, -0.16, '220', ha='center', fontsize=9, color=even_c)
ax2.text(330, -0.16, '330', ha='center', fontsize=9, color=even_c)
ax2.text(440, -0.16, '440', ha='center', fontsize=9, color=even_c)
ax2.set_xlim(0, 480)
ax2.set_ylim(-0.45, 1.7)
ax2.set_yticks([])
ax2.set_xticks([55, 110, 165, 220, 330, 440])
ax2.set_xticklabels(['55', '110', '165', '220', '330', '440'],
                    fontsize=9.5, color='#333333')
ax2.set_xlabel('frequency (Hz) — the surviving series is 110·{1,2,3,4}',
               fontsize=10, color='#333333')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)

fig.savefig('assets/fold-letter-frame-cover.png', dpi=170, bbox_inches='tight',
            facecolor='white')
print('wrote assets/fold-letter-frame-cover.png')
