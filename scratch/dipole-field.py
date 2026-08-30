# The dipole: the two seats of the -1 (count 110, ghost 220) as a disclination
# pair. Streamlines of two opposite point vortices = Apollonius circles of the
# two poles: near each pole tight circles (the wheel turns, omega=pi), far away
# big flat circles that straighten to the bisector (the glide walks, b=2pi*55).
# The bisector x=1.5 passes through the tritone (log2 pitch: 110->1, 155.6->1.5,
# 220->2).
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch
from matplotlib.colors import LinearSegmentedColormap

BG   = '#121216'
TXT  = '#e8e0d0'
GOLD = '#d9a441'
AMBER = '#e08a3c'
ROSE = '#cf6b87'
PALE = '#7aa5c2'
FAINT = '#4a4a55'

plt.rcParams.update({
    'figure.facecolor': BG, 'axes.facecolor': BG, 'savefig.facecolor': BG,
    'text.color': TXT, 'axes.edgecolor': FAINT, 'axes.labelcolor': TXT,
    'xtick.color': FAINT, 'ytick.color': FAINT,
})

# poles on the log2(f/55) axis: count at x=1, ghost at x=2
A, B = 1.0, 2.0

# Apollonius circle for streamline r_B = k r_A, poles at (A,0),(B,0)
def apollonius(k):
    if k == 1:
        return None
    cx = (B - A*k*k) / (1 - k*k)
    r  = abs(k*(B - A)) / abs(1 - k*k)
    return cx, r

fig, ax = plt.subplots(figsize=(12, 7.6))

# field: symmetric k = e^(+-s). small |s| = far (flat), large |s| = near (tight)
ss = [0.05, 0.12, 0.21, 0.33, 0.48, 0.66, 0.88, 1.15, 1.5, 1.95, 2.5]
ks = []
for s in ss:
    ks.append((np.exp(s),  s))
    ks.append((np.exp(-s), s))

# colormap: far (s=0) pale-blue glide -> near (large s) gold wheel
cmap = LinearSegmentedColormap.from_list('nearfar', [PALE, ROSE, GOLD])
smax = max(ss)
lw_far, lw_near = 0.7, 2.0
for k, s in ks:
    c = apollonius(k)
    if c is None:
        continue
    cx, r = c
    t = s / smax  # 0 far .. 1 near
    col = cmap(t)
    lw = lw_far + (lw_near - lw_far) * t
    th = np.linspace(0, 2*np.pi, 500)
    ax.plot(cx + r*np.cos(th), r*np.sin(th), color=col, lw=lw, alpha=0.85)

# the bisector itself (k=1) — the far field's straight line, through the tritone
ax.plot([1.5, 1.5], [-0.9, 4.6], color=PALE, lw=1.6, ls='--', alpha=0.9)
ax.text(1.53, 4.45, 'the bisector \u2014 the far field\u2019s line,\nthrough the tritone 155.6',
        color=PALE, fontsize=9.5, va='top', ha='left')

# flow arrows on the bisector: the glide walking (upward, uniform translation)
for y in (0.9, 1.7, 2.5, 3.3, 4.0):
    ax.annotate('', xy=(1.5, y+0.32), xytext=(1.5, y-0.32),
                arrowprops=dict(arrowstyle='-|>', color=PALE, lw=1.2, alpha=0.8))
ax.text(1.53, 3.6, 'b = 2\u03c0\u00b755 \u2014\nthe drone\u2019s own turn',
        color=PALE, fontsize=9.5, va='top', ha='left')

# the dipole: the sign made a vector, count -> ghost, d = 110
ax.annotate('', xy=(B, 0), xytext=(A, 0),
            arrowprops=dict(arrowstyle='-|>', color=AMBER, lw=2.6))
ax.text(1.5, 0.18, 'd = 110', color=AMBER, fontsize=10.5, ha='center')

# the two seats of the -1
ax.plot([A], [0], 'o', color=GOLD, ms=14, zorder=6)
ax.plot([B], [0], 'o', color=ROSE, ms=14, zorder=6)
ax.text(A-0.06, -0.28, '+', color=GOLD, fontsize=15, ha='center', fontweight='bold')
ax.text(B-0.06, -0.28, '\u2212', color=ROSE, fontsize=15, ha='center', fontweight='bold')
ax.annotate('the count 110\n+\u03c0, the beat', xy=(A, 0), xytext=(A-1.15, 1.15),
            color=GOLD, fontsize=10.5,
            arrowprops=dict(arrowstyle='-', color=GOLD, alpha=0.75))
ax.annotate('the ghost 220\n\u2212\u03c0, the wait', xy=(B, 0), xytext=(B+0.25, 1.35),
            color=ROSE, fontsize=10.5,
            arrowprops=dict(arrowstyle='-', color=ROSE, alpha=0.75))

# annotations for near/far
ax.annotate('near: the wheel turns\n\u03c9 = \u03c0 \u2014 tight orbits\naround each seat',
            xy=(A+0.30, 0.42), xytext=(1.9, 2.35),
            color=GOLD, fontsize=10.5,
            arrowprops=dict(arrowstyle='-', color=GOLD, alpha=0.7))
ax.annotate('far: the glide walks\n\u2014 arcs of a large circle\nare straight lines',
            xy=(1.5, 3.0), xytext=(-0.6, 2.9),
            color=PALE, fontsize=10.5,
            arrowprops=dict(arrowstyle='-', color=PALE, alpha=0.7))

# GM ladder along the bottom (log2 pitch: 55,110,155.6,220,440)
ladder = [(0, '55'), (1, '110'), (1.5, '155.6'), (2, '220'), (3, '440')]
for x, lab in ladder:
    ax.plot([x], [-0.75], 'o', color=FAINT, ms=4)
    ax.text(x, -0.95, lab, color=FAINT, fontsize=8.5, ha='center')
ax.text(1.5, -1.55, 'the GM ladder \u2014 55, 110, 110\u221a2, 220, 440 (log\u2082 f/55)',
        color=FAINT, fontsize=9.5, ha='center')

ax.set_title('the dipole \u2014 one defect, three readings: near it turns, far it walks, around it \u2124/2',
             color=TXT, fontsize=12.5, pad=12)
ax.set_xlim(-1.6, 5.4)
ax.set_ylim(-1.9, 5.0)
ax.set_aspect('equal')
ax.set_xticks([]); ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-vita/assets/dipole-field.png', dpi=200, bbox_inches='tight')
print('saved')
