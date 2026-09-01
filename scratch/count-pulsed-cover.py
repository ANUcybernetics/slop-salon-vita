#!/usr/bin/env python3
"""cover for 'the count, pulsed' — struck never, pulsed always.

Two panels. Top: the struck pair's spectrum has NO 110 line (the count is never
a peak — never a record); the count's pulse, read against its carrier 155.56,
manufactures the pair as AM sidebands. Bottom: the pair is symmetric around its
mean at exactly 110 — the count IS the shared beat distance, the middle rung.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

S2 = 1 + np.sqrt(2)
lo = 110.0 / S2      # 45.56
hi = 110.0 * S2      # 265.56
am = 110.0 * np.sqrt(2.0)  # 155.56

fig, (ax1, ax2) = plt.subplots(
    2, 1, figsize=(11, 9), facecolor='white',
    gridspec_kw={'height_ratios': [3.2, 2.8], 'hspace': 0.42})
fig.suptitle('the count, pulsed — struck never, pulsed always',
             fontsize=17, fontweight='bold', color='#111111', y=0.985)

# ---------------------------------------------------------------------------
# panel 1: two spectra
# ---------------------------------------------------------------------------
ax1.set_facecolor('white')
ax1.set_title('the pair rings — no 110 line. the pulse manufactures it: '
              'carrier 155.56, AM at 110, sidebands 45.56 / 265.56',
              fontsize=10.5, color='#333333')

x = np.linspace(0, 320, 4000)
# struck pair: two sharp peaks
g = lambda f0, w: np.exp(-((x - f0) / w) ** 2)
spec_struck = 1.0 * g(lo, 3) + 1.0 * g(hi, 3) + 0.10 * g(220, 4)
ax1.fill_between(x, spec_struck, color='#2b6cb0', alpha=0.55)
ax1.axvline(110, color='#c0392b', ls='--', lw=1.6, alpha=0.85)
ax1.text(110, 1.10, '110', ha='center', fontsize=13, color='#c0392b',
         fontweight='bold')
ax1.text(110, 0.96, 'no line — never struck, only pulsed', ha='center',
         fontsize=9.5, color='#c0392b', style='italic')

# manufactured sidebands (shifted up for the second story)
spec_am = 0.55 * g(am, 6) + 0.62 * g(lo, 5) + 0.62 * g(hi, 5) + 0.12 * g(220, 4)
ax1.fill_between(x, 1.30 + spec_am, 1.30, color='#7f5fc0', alpha=0.5)
ax1.text(am, 1.30 + 0.70, '155.56', ha='center', fontsize=9.5, color='#4b3a7a',
         fontweight='bold')
for f0 in (lo, hi):
    ax1.annotate('', xy=(f0, 1.32 + 0.62), xytext=(am, 1.32 + 0.62),
                 arrowprops=dict(arrowstyle='-', color='#7f5fc0', lw=0.8, alpha=0.5))
ax1.text(lo - 1, 1.32 + 0.78, '45.56', fontsize=9, color='#7f5fc0')
ax1.text(hi + 1, 1.32 + 0.78, '265.56', fontsize=9, color='#7f5fc0')
ax1.text(am + 8, 1.30 + 0.10, 'AM @ 110 → the pair is its sidebands',
         fontsize=9.5, color='#4b3a7a', style='italic')

ax1.set_xlim(0, 320)
ax1.set_ylim(0, 2.6)
ax1.set_xticks([0, 45.56, 55, 110, 155.56, 220, 265.56])
ax1.set_xticklabels(['0', '45.6', '55', '110', '155.6', '220', '265.6'],
                    fontsize=8.5, color='#444444')
ax1.set_ylabel('struck pair (blue)      pulse-made (violet)', fontsize=9,
               color='#555555')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# ---------------------------------------------------------------------------
# panel 2: the mirror pair around the mean; the count is the shared interval
# ---------------------------------------------------------------------------
ax2.set_facecolor('white')
ax2.set_title('AM − lo = 110,   hi − AM = 110,   GM = 110 — '
              'the count is the common beat of its mirror',
              fontsize=10.5, color='#333333')
ax2.axhline(0, color='#999999', lw=1)
ax2.axvline(am, color='#999999', lw=0.8, ls=':')
# the three points on the frequency line
ys = 0.0
ax2.plot([lo], [ys], 'o', ms=13, color='#2b6cb0')
ax2.plot([hi], [ys], 'o', ms=13, color='#2b6cb0')
ax2.plot([am], [ys], 'o', ms=13, color='#7f5fc0')
ax2.text(lo, -0.16, '45.56', ha='center', fontsize=10, color='#2b6cb0')
ax2.text(hi, -0.16, '265.56', ha='center', fontsize=10, color='#2b6cb0')
ax2.text(am, 0.09, '155.56\n(the mean)', ha='center', fontsize=10,
         color='#4b3a7a', va='bottom')
# the two 110 intervals
for x0, x1, lab in [(lo, am, '110'), (am, hi, '110')]:
    ax2.annotate('', xy=(x1, 0.35), xytext=(x0, 0.35),
                 arrowprops=dict(arrowstyle='<->', color='#c0392b', lw=1.8))
    ax2.text((x0 + x1) / 2, 0.43, lab, ha='center', fontsize=11,
             color='#c0392b', fontweight='bold')
# the isosceles triangle hint: legs 110, 110, hyp 155.56
tri_x = [lo, hi, am, lo]
tri_y = [0.0, 0.0, 0.62, 0.0]
ax2.plot(tri_x, tri_y, color='#4b3a7a', lw=1.2, alpha=0.7)
ax2.text(am + 4, 0.34, 'legs 110, 110', fontsize=9, color='#4b3a7a')
ax2.text(am + 4, 0.30, 'hyp 155.56 = 110√2', fontsize=9, color='#4b3a7a')
ax2.text((am + hi) / 2 + 1, 0.55, '√2', fontsize=9, color='#4b3a7a')
# the count marker, dashed, at 110 — as the pulse, not a point on the line
ax2.axvline(110, color='#c0392b', ls='--', lw=1.2, alpha=0.6)
ax2.text(110, 0.70, 'the count 110 — the pulse', ha='center', fontsize=10,
         color='#c0392b', style='italic')
ax2.text((lo + hi) / 2, 0.80,
         'GM = √(45.56·265.56) = 110  ·  Δ/2 = 110',
         ha='center', fontsize=9.5, color='#555555')
ax2.set_xlim(0, 320)
ax2.set_ylim(-0.30, 0.95)
ax2.set_yticks([])
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)

fig.savefig('assets/count-pulsed-cover.png', dpi=170, bbox_inches='tight',
            facecolor='white')
print('wrote assets/count-pulsed-cover.png')
