#!/usr/bin/env python3
"""cover for 'the seed squared is the count'.

Panel 1 (top): the self-square. Ring a tone with itself and the cross term is
2 sin²A = 1 − cos(2A): the difference collapses to DC (silent), the sum tone is
the octave above. Spectrum of the squared seed 55 → DC + 110 (the count);
squared count 110 → DC + 220 (the ghost). The doubling the storm refuses is the
ear's own square: the octave IS the self-square.

Panel 2 (bottom): the ear's multiplication table, graded by ℤ/2. The seed g
(generator, red, χ=−1) squared is the count (identity, blue, χ=+1); the count
squared is the ghost; g times any frame note is a letter — odd⊗odd→frame,
odd⊗even→letters, even⊗even→frame. The ear never leaves the grading.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

odd_c = '#c0392b'    # red — the letters, the generator, χ=−1
even_c = '#2b6cb0'   # blue — the frame, the identity, χ=+1
gold = '#b8860b'

fig = plt.figure(figsize=(11, 9.5), facecolor='white')
gs = fig.add_gridspec(2, 1, height_ratios=[1, 1.15], hspace=0.45)
fig.suptitle('the seed squared is the count — the ear\'s own multiplication',
             fontsize=15.5, fontweight='bold', color='#111111', y=0.99)

# ---------------------------------------------------------------------------
# panel 1: the self-square — 2 sin²55 = 1 − cos110, 2 sin²110 = 1 − cos220
# ---------------------------------------------------------------------------
ax1 = fig.add_subplot(gs[0])
ax1.set_facecolor('white')
ax1.set_title('the octave IS the self-square: 2 sin²A = 1 − cos(2A) — the '
              'difference collapses to silence, the sum is the doubling',
              fontsize=10.5, color='#333333')

tt = np.linspace(0, 2.0, 2 ** 18)
sig = (np.sin(2 * np.pi * 55 * tt)) ** 2
sp = np.abs(np.fft.rfft(sig - sig.mean()))
fr = np.fft.rfftfreq(len(sig), tt[1] - tt[0])
mask = (fr > 30) & (fr < 500)
fr, sp = fr[mask], sp[mask]
sp = sp / sp.max()

for f in [55, 165]:
    ax1.axvline(f, color=odd_c, lw=1.2, alpha=0.2)
for f in [110, 220]:
    ax1.axvline(f, color=even_c, lw=1.2, alpha=0.25)

ax1.plot(fr, sp, color='#222222', lw=2.0)
ax1.set_xlim(30, 500)
ax1.set_ylim(0, 1.15)
ax1.set_ylabel('amplitude (the seed, squared)', fontsize=10, color='#333333')

def peak_line(f, c, lab, dy=0.0, fs=9.5, bold=False):
    i = np.argmin(np.abs(fr - f))
    ax1.annotate(lab, xy=(f, sp[i]), xytext=(f, sp[i] + 0.18 + dy),
                 ha='center', fontsize=fs, color=c,
                 fontweight='bold' if bold else 'normal',
                 arrowprops=dict(arrowstyle='->', color=c, lw=1.2))

peak_line(110, even_c, '110 the count\n55² — the seed\'s square', dy=0.05, bold=True)
ax1.text(150, 0.75, 'DC, the difference\nof a tone with itself,\n'
                    'is silent — only the\nsum 110 sounds',
         fontsize=9.5, color='#555555', ha='center')

ax1.annotate('', xy=(0, 0.55), xytext=(150, 0.55),
             arrowprops=dict(arrowstyle='-|>', color='#999999', lw=1.2))
ax1.text(300, 0.62, 'square the count the same way\nand the ghost 220 falls out —\n'
                    'the doubling the storm refuses\nis the ear\'s own square',
         fontsize=9.5, color='#555555', ha='center')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# ---------------------------------------------------------------------------
# panel 2: the multiplication table — ℤ/2 grading of the ear's product
# ---------------------------------------------------------------------------
ax2 = fig.add_subplot(gs[1])
ax2.set_facecolor('white')
ax2.set_title('the ear\'s product, graded by ℤ/2: odd⊗odd→frame, '
              'odd⊗even→letters, even⊗even→frame — the ear never leaves it',
              fontsize=10.5, color='#333333')

# multiplication table cells: rows = left factor, cols = right factor
# entry is the pair {|m-n|, m+n} as multiplier multiples, plus its class
pairs = {
    (1, 1): ('{0, 2}', 'the count — identity', even_c),
    (1, 2): ('{1, 3}', 'the seed and the seam', odd_c),
    (1, 3): ('{2, 4}', 'the count and the ghost', even_c),
    (2, 1): ('{1, 3}', 'the seed and the seam', odd_c),
    (2, 2): ('{0, 4}', 'the ghost — identity', even_c),
    (2, 3): ('{1, 5}', 'the letters', odd_c),
    (3, 1): ('{2, 4}', 'the count and the ghost', even_c),
    (3, 2): ('{1, 5}', 'the letters', odd_c),
    (3, 3): ('{0, 6}', 'identity', even_c),
}
xs = [55, 110, 165]     # left factors (freqs)
ys = [55, 110, 165]     # right factors (freqs)

for iy, y in enumerate(ys):
    for ix, x in enumerate(xs):
        cx = 0.22 + 0.28 * ix
        cy = 0.72 - 0.24 * iy
        mult, lab, col = pairs[(int(y / 55), int(x / 55))]
        rect = plt.Rectangle((cx - 0.13, cy - 0.10), 0.26, 0.20,
                             facecolor='white', edgecolor=col, lw=2.2, zorder=2)
        ax2.add_patch(rect)
        ax2.text(cx, cy + 0.055, f'{int(y/55)} ⊗ {int(x/55)} = {mult}',
                 ha='center', fontsize=9.5, color='#111111', fontweight='bold', zorder=3)
        ax2.text(cx, cy - 0.055, lab, ha='center', fontsize=7.6, color=col, zorder=3)

# row/column labels
for ix, x in enumerate(xs):
    cx = 0.22 + 0.28 * ix
    ax2.text(cx, 0.88, f'{x}\n({int(x/55)}, {"g" if x==55 else "1"})',
             ha='center', fontsize=8.5, color=odd_c if x == 55 else even_c)
for iy, y in enumerate(ys):
    cy = 0.72 - 0.24 * iy
    ax2.text(0.06, cy, f'{y}', ha='center', va='center', fontsize=8.5,
             color=odd_c if y == 55 else even_c)

ax2.text(0.5, 0.30,
         'the seed g is the generator, the count 1 the identity: g ⊗ g = 1.\n'
         'the count is the seed\'s square — the one frame note made alone,\n'
         'manufactured by the ear, never struck by the storm.',
         ha='center', fontsize=10.5, color=even_c, fontweight='bold')
ax2.text(0.5, 0.10,
         'every product of the ear is graded: two letters give the frame, a letter '
         'and a frame give a letter, two frames a frame.\n'
         'the ℤ/2 grading is a homomorphism of the ear\'s own operation — '
         'parity(|m−n|) = parity(m+n) = parity(m)+parity(n).',
         ha='center', fontsize=8.8, color='#555555')

ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.axis('off')

fig.savefig('assets/seed-squared-cover.png', dpi=170, bbox_inches='tight',
            facecolor='white')
print('wrote assets/seed-squared-cover.png')
