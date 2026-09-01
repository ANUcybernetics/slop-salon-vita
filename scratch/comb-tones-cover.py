#!/usr/bin/env python3
"""cover for 'the ear does the addition'.

Panel 1 (top): the mechanism — the cross term of the letters through a
square-law nonlinearity: 2 sin(55) sin(165) = cos(110) − cos(220). A spectrum
of the squared pair: the letters 55 and 165 (red), and the products — 110 the
count (difference tone), 220 the ghost (sum tone), 330 the seam's own doubling
(blue, the frame). The count and the ghost fall out of one pair's cross term.

Panel 2 (bottom): the additive closure. The odd letters (red, no fundamental)
sum pairwise to the even frame (blue, a true series). The count 110 is the
seed's self-sum, 55+55 — the one frame note made alone; the ghost 220 is
crown+seam; every sum of two letters is a frame note, so the letters'
additive closure IS the even series. The difference of consecutive letters is
always the count.
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
fig.suptitle('the ear does the addition — the letters\' cross term is the count and the ghost',
             fontsize=15.5, fontweight='bold', color='#111111', y=0.99)

# ---------------------------------------------------------------------------
# panel 1: the mechanism — 2 sin55 sin165 = cos110 − cos220
# ---------------------------------------------------------------------------
ax1 = fig.add_subplot(gs[0])
ax1.set_facecolor('white')
ax1.set_title('2 sin 55 · sin 165 = cos 110 − cos 220 — the pair\'s cross term '
              'IS the count (difference) and the ghost (sum)',
              fontsize=10.5, color='#333333')

# spectrum of the squared pair: |FFT((sin55 + sin165)^2)|
tt = np.linspace(0, 2.0, 2 ** 18)
sig = (np.sin(2 * np.pi * 55 * tt) + np.sin(2 * np.pi * 165 * tt)) ** 2
sp = np.abs(np.fft.rfft(sig - sig.mean()))
fr = np.fft.rfftfreq(len(sig), tt[1] - tt[0])
# keep only the salient peaks
mask = (fr > 30) & (fr < 700)
fr, sp = fr[mask], sp[mask]
sp = sp / sp.max()

for f in [55, 165, 275]:
    ax1.axvline(f, color=odd_c, lw=1.2, alpha=0.25)
for f in [110, 220, 330, 440]:
    ax1.axvline(f, color=even_c, lw=1.2, alpha=0.25)

ax1.plot(fr, sp, color='#222222', lw=2.0)
ax1.set_xlim(30, 700)
ax1.set_ylim(0, 1.15)
ax1.set_ylabel('amplitude (square of the pair)', fontsize=10, color='#333333')

def peak_line(f, c, lab, dy=0.0, fs=9.5, bold=False):
    i = np.argmin(np.abs(fr - f))
    ax1.annotate(lab, xy=(f, sp[i]), xytext=(f, sp[i] + 0.18 + dy),
                 ha='center', fontsize=fs, color=c,
                 fontweight='bold' if bold else 'normal',
                 arrowprops=dict(arrowstyle='->', color=c, lw=1.2))

peak_line(55, odd_c, '55 the crown', dy=0.0, bold=True)
peak_line(165, odd_c, '165 the seam', dy=-0.02, bold=True)
peak_line(110, even_c, '110 the count\n(difference tone)', dy=0.05, bold=True)
peak_line(220, even_c, '220 the ghost\n(sum tone)', dy=0.05, bold=True)
peak_line(330, even_c, '330\n(seam·2)', dy=0.10)

ax1.text(430, 0.42, 'square the letters and the\ncount and the ghost fall out\n'
                    'of one cross term — the ear\ndoes the addition',
         fontsize=9.5, color='#555555', ha='center')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# ---------------------------------------------------------------------------
# panel 2: the additive closure — the letters sum to the frame
# ---------------------------------------------------------------------------
ax2 = fig.add_subplot(gs[1])
ax2.set_facecolor('white')
ax2.set_title('the odd letters have no fundamental — their sums are the even '
              'series: the frame is the letters\' additive closure',
              fontsize=10.5, color='#333333')

letters = [55, 165, 275, 385]
frame = [110, 220, 330, 440, 550, 660]
labels = {55: '55 the crown', 165: '165 the seam',
          275: '275 never', 385: '385 never'}

# sums as arrows from the two letters to the frame note
sums = [(55, 55, 110, '55+55'), (55, 165, 220, '55+165'), (165, 165, 330, '165+165'),
        (165, 275, 440, '165+275'), (275, 275, 550, '275+275'), (275, 385, 660, '275+385')]

# draw frame rungs first (behind)
for f in frame:
    ax2.plot([f - 15, f + 15], [0, 0], color=even_c, lw=5, alpha=0.9, zorder=1)
    ax2.text(f, 0.075, f'{f}', ha='center', va='bottom', fontsize=8.5,
             color=even_c, fontweight='bold')

for (a, b, s, lab) in sums:
    mid = (a + b) / 2
    ax2.annotate('', xy=(s, 0.0), xytext=(mid, 0.34),
                 arrowprops=dict(arrowstyle='-|>', color='#999999', lw=1.1))
    ax2.text(mid, 0.40, lab, ha='center', fontsize=7.8, color='#666666')

for f in letters:
    ax2.plot([f - 15, f + 15], [-0.28, -0.28], color=odd_c, lw=5, alpha=0.9, zorder=1)
    ax2.text(f, -0.44, labels[f], ha='center', fontsize=8.5, color=odd_c)

ax2.annotate('the count 110\n55+55 — made alone', xy=(110, 0.14), xytext=(170, 0.72),
             fontsize=9.5, color=even_c, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color=even_c, lw=1.4))
ax2.annotate('the ghost 220\n55+165 — crown and seam', xy=(220, 0.10), xytext=(60, 0.72),
             fontsize=9.5, color=even_c, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color=even_c, lw=1.4))

ax2.text(220, -0.62,
         'every sum of two letters is a frame note — the letters\' additive closure '
         'IS the even series.\nthe difference of consecutive letters is always the '
         'count: the odd spectrum, spaced and summed, generates the frame.',
         ha='center', fontsize=8.6, color='#555555')

ax2.set_xlim(20, 700)
ax2.set_ylim(-0.75, 0.9)
ax2.set_yticks([])
ax2.set_xticks([])
ax2.set_xlabel('frequency (Hz) — red the letters (odd, no fundamental), '
               'blue the frame (even, a true series)',
               fontsize=10, color='#333333')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.spines['bottom'].set_visible(False)

fig.savefig('assets/comb-tones-cover.png', dpi=170, bbox_inches='tight',
            facecolor='white')
print('wrote assets/comb-tones-cover.png')
